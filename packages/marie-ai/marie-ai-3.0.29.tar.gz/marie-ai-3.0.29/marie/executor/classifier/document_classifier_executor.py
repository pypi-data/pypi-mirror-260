from typing import Any, List, Optional, Union

import torch
from docarray import DocList

from marie import Executor, requests, safely_encoded
from marie.api import value_from_payload_or_args
from marie.api.docs import AssetKeyDoc, StorageDoc
from marie.boxes import PSMode
from marie.executor.mixin import StorageMixin
from marie.logging.logger import MarieLogger
from marie.logging.mdc import MDC
from marie.logging.predefined import default_logger as logger
from marie.models.utils import (
    initialize_device_settings,
    setup_torch_optimizations,
    torch_gc,
)
from marie.ocr import CoordinateFormat
from marie.pipe.classification_pipeline import ClassificationPipeline
from marie.utils.docs import docs_from_asset, frames_from_docs
from marie.utils.image_utils import ensure_max_page_size, hash_frames_fast
from marie.utils.network import get_ip_address

# TODO : Refactor this to as it is a duplicate of the one in text_extraction_executor.py


class DocumentClassificationExecutor(Executor, StorageMixin):
    """Executor for document classification"""

    def __init__(
        self,
        name: str = "",
        device: Optional[str] = None,
        num_worker_preprocess: int = 4,
        storage: dict[str, any] = None,
        pipelines: List[dict[str, any]] = None,
        dtype: Optional[Union[str, torch.dtype]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.logger = MarieLogger(
            getattr(self.metas, "name", self.__class__.__name__)
        ).logger

        logger.info(f"Starting executor : {self.__class__.__name__}")
        logger.info(f"Runtime args : {kwargs.get('runtime_args')}")
        logger.info(f"Storage config: {storage}")
        logger.info(f"Pipelines config: {pipelines}")
        logger.info(f"Device : {device}")
        logger.info(f"Num worker preprocess : {num_worker_preprocess}")
        logger.info(f"Kwargs : {kwargs}")

        self.show_error = True  # show prediction errors
        # sometimes we have CUDA/GPU support but want to only use CPU
        resolved_devices, _ = initialize_device_settings(
            devices=[device], use_cuda=True, multi_gpu=False
        )
        if len(resolved_devices) > 1:
            self.logger.warning(
                "Multiple devices are not supported in %s inference, using the first device %s.",
                self.__class__.__name__,
                resolved_devices[0],
            )
        self.device = resolved_devices[0]
        has_cuda = True if self.device.type.startswith("cuda") else False

        setup_torch_optimizations()
        self.pipeline = ClassificationPipeline(
            pipelines_config=pipelines, cuda=has_cuda
        )

        instance_name = "not_defined"
        if kwargs is not None:
            if "runtime_args" in kwargs:
                instance_name = kwargs.get("runtime_args").get("name", "not_defined")

        self.runtime_info = {
            "name": self.__class__.__name__,
            "instance_name": instance_name,
            "model": "",
            "host": get_ip_address(),
            "workspace": self.workspace,
            "use_cuda": has_cuda,
        }

        self.storage_enabled = False
        if storage is not None and "psql" in storage:
            sconf = storage["psql"]
            self.setup_storage(sconf.get("enabled", False), sconf)

    @requests(on="/default")
    def default(self, parameters, **kwargs):
        return {"valid": True}

    @requests(on="/document/classify")
    # @safely_encoded # BREAKS WITH docarray 0.39 as it turns this into a LegacyDocument which is not supportedncoded
    def classify(self, docs: DocList[AssetKeyDoc], parameters: dict, *args, **kwargs):

        """
        Document classification

        EXAMPLE USAGE

            As Executor

            .. code-block:: python

                filename = img_path.split("/")[-1].replace(".png", "")
                checksum = hash_file(img_path)
                docs = docs_from_file(img_path)

                parameters = {
                    "ref_id": filename,
                    "ref_type": "filename",
                    "checksum": checksum,
                    "img_path": img_path,
                }

                results = executor.classify(docs, parameters)


        :param parameters:
        :param docs: Documents to process
        :param kwargs:
        :return:
        """
        if len(docs) == 0:
            return {"error": "empty payload"}
        if len(docs) > 1:
            return {"error": "expected single document"}

        # load documents from specified document asset key
        doc = docs[0]
        docs = docs_from_asset(doc.asset_key, doc.pages)

        src_frames = frames_from_docs(docs)
        changed, frames = ensure_max_page_size(src_frames, max_page_size=(2500, 3000))

        if changed:
            self.logger.warning(f"Page size of frames was changed ")
            for i, (s, f) in enumerate(zip(src_frames, frames)):
                self.logger.warning(f"Frame[{i}] changed : {s.shape} -> {f.shape}")

        if parameters is None or "job_id" not in parameters:
            self.logger.warning(f"Job ID is not present in parameters")
            raise ValueError("Job ID is not present in parameters")

        job_id = parameters.get("job_id")
        MDC.put("request_id", job_id)

        self.logger.info("Starting ICR processing request")
        for key, value in parameters.items():
            self.logger.info("The value of {} is {}".format(key, value))

        queue_id: str = parameters.get("queue_id", "0000-0000-0000-0000")

        try:
            if "payload" not in parameters or parameters["payload"] is None:
                return {"error": "empty payload"}
            else:
                payload = parameters["payload"]

            # https://github.com/marieai/marie-ai/issues/51
            regions = payload["regions"] if "regions" in payload else []
            for region in regions:
                region["id"] = f'{int(region["id"])}'
                region["x"] = int(region["x"])
                region["y"] = int(region["y"])
                region["w"] = int(region["w"])
                region["h"] = int(region["h"])
                region["pageIndex"] = int(region["pageIndex"])

            # due to compatibility issues with other frameworks we allow passing same arguments in the 'args' object
            coordinate_format = CoordinateFormat.from_value(
                value_from_payload_or_args(payload, "format", default="xywh")
            )
            pms_mode = PSMode.from_value(
                value_from_payload_or_args(payload, "mode", default="")
            )

            # output_format = OutputFormat.from_value(
            #     value_from_payload_or_args(payload, "output", default="json")
            # )

            if parameters:
                for key, value in parameters.items():
                    self.logger.debug("The p-value of {} is {}".format(key, value))
                ref_id = parameters.get("ref_id")
                ref_type = parameters.get("ref_type")
                job_id = parameters.get("job_id", "0000-0000-0000-0000")
            else:
                self.logger.warning(
                    f"REF_ID and REF_TYPE are not present in parameters"
                )
                ref_id = hash_frames_fast(frames)
                ref_type = "classify"
                job_id = "0000-0000-0000-0000"

            self.logger.debug(
                "ref_id, ref_type frames , regions , pms_mode, coordinate_format,"
                f" checksum: {ref_id}, {ref_type},  {len(frames)}, {len(regions)}, {pms_mode},"
                f" {coordinate_format}"
            )

            runtime_conf = {}
            if "features" in payload:
                for feature in payload["features"]:
                    if "type" in feature and feature["type"] == "pipeline":
                        runtime_conf = feature

            metadata = self.pipeline.execute(
                ref_id=ref_id,
                ref_type=ref_type,
                frames=frames,
                pms_mode=pms_mode,
                coordinate_format=coordinate_format,
                regions=regions,
                queue_id=queue_id,
                job_id=job_id,
                runtime_conf=runtime_conf,
            )

            del frames
            del regions

            self.persist(ref_id, ref_type, metadata)

            # strip out ocr results from metadata
            include_ocr = True
            if not include_ocr and "ocr" in metadata:
                del metadata["ocr"]

            response = {
                "status": "succeeded",
                "runtime_info": self.runtime_info,
                "metadata": metadata,
            }
            converted = safely_encoded(lambda x: x)(response)
            return converted
        except BaseException as error:
            self.logger.error(f"Extract error : {error}", exc_info=True)
            msg = "inference exception"
            if self.show_error:
                msg = (str(error),)
            return {
                "status": "error",
                "runtime_info": self.runtime_info,
                "error": msg,
            }
        finally:
            torch_gc()
            MDC.remove("request_id")

    def persist(self, ref_id: str, ref_type: str, results: Any) -> None:
        """Persist results"""

        def _tags(index: int, ftype: str, checksum: str):
            return {
                "action": "classifier",
                "index": index,
                "type": ftype,
                "ttl": 48 * 60,
                "checksum": checksum,
                "runtime": self.runtime_info,
            }

        if self.storage_enabled:
            # frame_checksum = hash_frames_fast(frames=[frame])

            docs = DocList[StorageDoc](
                [
                    StorageDoc(
                        content=results,
                        tags=_tags(-1, "metadata", ref_id),
                    )
                ]
            )

            self.store(
                ref_id=ref_id,
                ref_type=ref_type,
                store_mode="content",
                docs=docs,
            )
