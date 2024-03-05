"""
Base default handler to load torchscript or eager mode [state_dict] models
Also, provides handle method per torch serve custom model specification

https://pytorch.org/docs/stable/profiler.html
"""

import abc
import logging
import os
import time

import torch
from torch.profiler import ProfilerActivity, profile, record_function

# from marie.logger import setup_logger
from marie.logging.predefined import default_logger as logger
from marie.registry_base import RegistryHolder

# logger = setup_logger(__name__)

ipex_enabled = False
if os.environ.get("MARIE_IPEX_ENABLE", "false") == "true":
    try:
        import intel_extension_for_pytorch as ipex

        ipex_enabled = True
    except ImportError as error:
        logger.warning(
            "IPEX is enabled but intel-extension-for-pytorch is not installed. Proceeding without IPEX."
        )


class BaseHandler(metaclass=RegistryHolder):
    """
    Base default handler to load torchscript or eager mode [state_dict] models
    Also, provides handle method per torch serve custom model specification
    """

    pass

    def __init__(self):
        self.model = None
        self.mapping = None
        self.device = None
        self.INITIALIZED = False
        self.context = None
        self.manifest = None
        self.map_location = None
        self.explain = False
        self.target = 0
        self.profiler_args = {}

    def initialize(self, context):
        """Initialize function loads the model.pt file and initialized the model object.
           First try to load torchscript else load eager mode state_dict based model.

        Args:
            context (context): It is a JSON Object containing information
            pertaining to the model artifacts parameters.

        Raises:
            RuntimeError: Raises the Runtime error when the model.py is missing

        """
        pass

    def preprocess(self, data):
        """
        Preprocess function to convert the request input to a tensor(Torchserve supported format).
        The user needs to override to customize the pre-processing

        Args :
            data (list): List of the data from the request input.

        Returns:
            tensor: Returns the tensor data of the input
        """
        return torch.as_tensor(data, device=self.device)

    def inference(self, data, *args, **kwargs):
        """
        The Inference Function is used to make a prediction call on the given input request.
        The user needs to override the inference function to customize it.

        Args:
            data (Torch Tensor): A Torch Tensor is passed to make the Inference Request.
            The shape should match the model input shape.

        Returns:
            Torch Tensor : The Predicted Torch Tensor is returned in this function.
        """
        marshalled_data = data.to(self.device)
        with torch.no_grad():
            results = self.model(marshalled_data, *args, **kwargs)
        return results

    def postprocess(self, data):
        """
        The post process function makes use of the output from the inference and converts into a
        Torchserve supported response output.

        Args:
            data (Torch Tensor): The torch tensor received from the prediction output of the model.

        Returns:
            List: The post process function returns a list of the predicted output.
        """

        return data.tolist()

    def handle(self, data, context):
        """Entry point for default handler. It takes the data from the input request and returns
           the predicted outcome for the input.

        Args:
            data (list): The input data that needs to be made a prediction request on.
            context (Context): It is a JSON Object containing information pertaining to
                               the model artefacts parameters.

        Returns:
            list : Returns a list of dictionary with the predicted response.
        """

        # It can be used for pre or post processing if needed as additional request
        # information is available in context
        start_time = time.time()

        self.context = context
        metrics = self.context.metrics

        is_profiler_enabled = os.environ.get("ENABLE_TORCH_PROFILER", None)
        if is_profiler_enabled:
            output, _ = self._infer_with_profiler(data=data)
        else:
            if self._is_describe():
                output = [self.describe_handle()]
            else:
                data_preprocess = self.preprocess(data)

                if not self._is_explain():
                    output = self.inference(data_preprocess)
                    output = self.postprocess(output)
                else:
                    output = self.explain_handle(data_preprocess, data)

        stop_time = time.time()
        metrics.add_time(
            "HandlerTime", round((stop_time - start_time) * 1000, 2), None, "ms"
        )
        return output

    def _infer_with_profiler(self, data):
        """Custom method to generate pytorch profiler traces for preprocess/inference/postprocess

        Args:
            data (list): The input data that needs to be made a prediction request on.

        Returns:
            output : Returns a list of dictionary with the predicted response.
            prof: pytorch profiler object
        """
        # Setting the default profiler arguments to profile cpu, gpu usage and record shapes
        # User can override this argument based on the requirement
        if not self.profiler_args:
            self.profiler_args["activities"] = [
                ProfilerActivity.CPU,
                ProfilerActivity.CUDA,
            ]
            self.profiler_args["record_shapes"] = True

        if "on_trace_ready" not in self.profiler_args:
            result_path = "/tmp/pytorch_profiler"
            dir_name = ""
            try:
                model_name = self.manifest["model"]["modelName"]
                dir_name = model_name
            except KeyError:
                logging.debug("Model name not found in config")

            result_path = os.path.join(result_path, dir_name)
            self.profiler_args[
                "on_trace_ready"
            ] = torch.profiler.tensorboard_trace_handler(result_path)
            logger.info(
                "Saving chrome trace to : ", result_path
            )  # pylint: disable=logging-too-many-args

        with profile(**self.profiler_args) as prof:
            with record_function("preprocess"):
                data_preprocess = self.preprocess(data)
            if not self._is_explain():
                with record_function("inference"):
                    output = self.inference(data_preprocess)
                with record_function("postprocess"):
                    output = self.postprocess(output)
            else:
                with record_function("explain"):
                    output = self.explain_handle(data_preprocess, data)

        logger.info(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))
        return output, prof

    def explain_handle(self, data_preprocess, raw_data):
        """Captum explanations handler

        Args:
            data_preprocess (Torch Tensor): Preprocessed data to be used for captum
            raw_data (list): The unprocessed data to get target from the request

        Returns:
            dict : A dictionary response with the explanations response.
        """
        output_explain = None
        inputs = None
        target = 0

        logger.info("Calculating Explanations")
        row = raw_data[0]
        if isinstance(row, dict):
            logger.info("Getting data and target")
            inputs = row.get("data") or row.get("body")
            target = row.get("target")
            if not target:
                target = 0

        output_explain = self.get_insights(data_preprocess, inputs, target)
        return output_explain

    def _is_explain(self):
        if self.context and self.context.get_request_header(0, "explain"):
            if self.context.get_request_header(0, "explain") == "True":
                self.explain = True
                return True
        return False

    def _is_describe(self):
        if self.context and self.context.get_request_header(0, "describe"):
            if self.context.get_request_header(0, "describe") == "True":
                return True
        return False

    def describe_handle(self):
        """Customized describe handler

        Returns:
            dict : A dictionary response.
        """
        # pylint: disable=unnecessary-pass
        pass
        # pylint: enable=unnecessary-pass

    def unload(self):
        """Unload the model from GPU/CPU"""
        pass
