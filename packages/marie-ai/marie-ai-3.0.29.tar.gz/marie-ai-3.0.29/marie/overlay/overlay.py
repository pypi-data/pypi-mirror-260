import os
import sys
import time
import timeit
from typing import Tuple, Union

import cv2
import numpy as np
import torch
from PIL import Image

from marie.base_handler import BaseHandler
from marie.constants import __model_path__
from marie.models.pix2pix.data import create_dataset
from marie.models.pix2pix.models import create_model
from marie.models.pix2pix.options.test_options import TestOptions
from marie.models.pix2pix.util.util import tensor2im
from marie.models.utils import fill_gpu_memory, log_oom, torch_gc
from marie.timer import Timer
from marie.utils.image_utils import hash_frames_fast, imwrite, read_image
from marie.utils.onnx import OnnxModule
from marie.utils.utils import ensure_exists

# Add parent to the search path, so we can reference the module here without throwing and exception
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

debug_visualization_enabled = False


class OverlayProcessor(BaseHandler):
    def __init__(
        self,
        work_dir: str,
        models_dir: str = os.path.join(__model_path__),
        cuda: bool = True,
        **kwargs,
    ) -> None:
        super().__init__()
        checkpoint_dir = os.path.join(models_dir, "overlay")
        self.cuda = cuda
        self.models_dir = models_dir
        self.work_dir = work_dir
        self.opt, self.model = self.__setup(cuda, checkpoint_dir)
        self.initialized = False

    @staticmethod
    def __setup(cuda, checkpoints_dir):
        """Model setup"""

        gpu_id = "0" if cuda else "-1"

        args = [
            "--dataroot",
            "./data",
            "--name",
            # "template_mask_global",
            "claim_mask",  # hicfa_mask_local
            "--model",
            "test",
            "--netG",
            "local",
            # "global",
            # "unet_256_spectral",
            "--direction",
            "AtoB",
            "--model",
            "test",
            "--dataset_mode",
            "single",
            "--gpu_id",
            gpu_id,
            "--norm",
            "instance",
            "--preprocess",
            "none",
            "--checkpoints_dir",
            checkpoints_dir,
            "--ngf",
            "64",  # Default 64
            "--ndf",
            "64",  # Default 64
            # "./model_zoo/overlay",
            "--no_dropout",
        ]

        opt = TestOptions().parse(args)
        # hard-code parameters for test
        if True:
            opt.eval = True
            opt.num_threads = 0  # test code only supports num_threads = 0
            opt.batch_size = 1  # test code only supports batch_size = 1
            opt.serial_batches = True
            opt.no_flip = True
            opt.no_dropout = False
            opt.display_id = -1
            opt.output_nc = 3

        # opt.eval = True
        # opt.num_threads = 0  # test code only supports num_threads = 0
        # opt.batch_size = 1  # test code only supports batch_size = 1
        # opt.serial_batches = True
        # opt.no_flip = False
        # opt.no_dropout = True
        # opt.display_id = -1
        # opt.input_nc = 3
        # opt.output_nc = 3
        # opt.n_layers_D = 3
        # opt.norm = "instance"
        # opt.ndf = 64
        # opt.ngf = 64
        # opt.netD = "n_layers_multi"
        # opt.netG = "local"
        # opt.direction = "AtoB"
        # opt.dataset_mode = "single"
        # opt.model = "test"
        # opt.name = "hicfa_mask_local"
        # opt.gan_mode = "ssim"

        # check if we have a onnx model and load it
        model_path = os.path.expanduser(
            os.path.join(checkpoints_dir, "claim_mask", "model.onnx")
        )

        if False:  # and os.path.exists(model_path):
            print(f"Loading ONNX model :{model_path}")
            model = OnnxModule(model_path, providers=None, use_io_binding=True)
            print("Model setup complete : ONNX")
            return opt, model

        model = create_model(opt)

        model.setup(opt)
        model.eval()

        return opt, model

    def preprocess_mm(self, img: np.ndarray) -> np.ndarray:
        # check if PIL image
        if not isinstance(img, Image.Image):
            img = Image.fromarray(img)
        # make sure image is divisible by 32
        ow, oh = img.size
        base = 32
        if ow % base != 0 or oh % base != 0:
            h = oh // base * base + base
            w = ow // base * base + base
            img = img.resize((w, h), Image.LANCZOS)

        # convert to numpy array
        return np.array(img)

    def preprocess(self, img: np.ndarray) -> np.ndarray:
        # check if PIL image
        # make sure image is divisible by 32
        if len(img.shape) != 3:
            raise Exception("Image must be 3 channel")
        oh, ow, channels = img.shape
        base = 32

        if ow % base != 0 or oh % base != 0:
            h = oh // base * base + base
            w = ow // base * base + base
            overlay = np.ones((h, w, channels), dtype=np.uint8) * 255
            overlay[:oh, :ow, :] = img
            return overlay

        return img

    @Timer(text="__extract_segmentation_mask in {:.4f} seconds")
    def __extract_segmentation_mask(self, img, dataroot_dir):
        """
        Extract overlay segmentation mask for the image
        """
        model = self.model
        opt = self.opt
        opt.dataroot = dataroot_dir
        try:
            if isinstance(self.model, OnnxModule):
                return self.run_onnx(img)

            # create a dataset given opt.dataset_mode and other options
            dataset = create_dataset(opt)
            for i, data in enumerate(dataset):
                model.set_input(data)  # unpack data from data loader
                model.test()
                visuals = model.get_current_visuals()  # get image results
                fake_im_data = visuals["fake"]
                image_numpy = tensor2im(fake_im_data)
                return image_numpy
        finally:
            # clear cuda memory after inference
            torch.cuda.empty_cache()

    def postprocess(
        self, src_img: np.ndarray, real_img: np.ndarray, fake_mask: np.ndarray
    ) -> np.ndarray:
        image_dir = os.path.join(self.work_dir, "debug")
        # Tensor is in RGB format OpenCV requires BGR
        fake_mask_np = cv2.cvtColor(fake_mask, cv2.COLOR_RGB2BGR)
        save_path = os.path.join(image_dir, "fake.png")

        # testing only
        if debug_visualization_enabled:
            imwrite(save_path, fake_mask_np)

        # TODO : Figure out why after the forward pass it is possible
        # to have different sizes(transforms have not been applied).
        # This is a work around for now

        # Causes by forward pass, incrementing size of the output layer
        if real_img.shape != fake_mask_np.shape:
            print(
                "WARNING(FIXME/ADJUSTING): Sizes of input arguments do not match(real,"
                f" fake) : {real_img.shape} != {fake_mask_np.shape}"
            )
            # tmp_img = np.ones((fake.shape[0], fake.shape[1], 3), dtype = np.uint8) * 255
            h = min(real_img.shape[0], fake_mask_np.shape[0])
            w = min(real_img.shape[1], fake_mask_np.shape[1])
            real_img = real_img[:h, :w, :]
            fake_mask_np = fake_mask_np[:h, :w, :]

            print(
                f"Image shapes after(real, fake) : {real_img.shape} : {fake_mask_np.shape}"
            )

        # blend the fake image with the real image
        blended = self.blend_to_text(real_img, fake_mask)

        # crop mask and blended image to original image size
        fake_mask_np = fake_mask_np[: src_img.shape[0], : src_img.shape[1], :]
        blended = blended[: src_img.shape[0], : src_img.shape[1], :]

        return fake_mask_np, blended

    @staticmethod
    def blend_to_text(real_img, mask_img):
        """Blend real and fake(generated) images together to generate extracted text mask

        :param real_img: original image
        :param mask_img: generated image
        :return: blended image
        """
        real = read_image(real_img)
        mask = read_image(mask_img)

        # this happens sometimes after a forward pass, the FAKE image is larger than the input
        # image. This is a workaround for now.
        if real.shape != mask.shape:
            raise Exception(
                f"Sizes of input arguments do not match(real, fake) : {real.shape} != {mask.shape}"
            )

        # original method to blend the images
        # blended_img = cv2.bitwise_or(real, mask)
        # # blended_img[blended_img >= 120] = [255]

        # new method to blend the images
        def __mask_from_hsv_range(hsv_img, hsv_color_ranges) -> np.ndarray:
            low_color = np.array(hsv_color_ranges[0], np.uint8)
            high_color = np.array(hsv_color_ranges[1], np.uint8)
            hsv_mask = cv2.inRange(hsv_img, low_color, high_color)
            return hsv_mask

        # converting from BGR to HSV color space(use hsv_selector.py tool to find the right values)
        hsv = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)
        # define range of red color in HSV color space
        # (hMin = 0, sMin = 0, vMin = 0), (hMax = 179, sMax = 121, vMax = 255)
        red_hsv_range = [[0, 137, 216], [179, 255, 255]]
        hsv_mask_red = __mask_from_hsv_range(hsv, red_hsv_range)
        hsv_mask_red = cv2.bitwise_not(hsv_mask_red)
        hsv_mask_red = cv2.cvtColor(hsv_mask_red, cv2.COLOR_GRAY2BGR)
        hsv_mask_red = cv2.cvtColor(hsv_mask_red, cv2.COLOR_BGR2GRAY)

        # imwrite(
        #     os.path.join("/tmp/form-segmentation", f"hsv_mask_red.png"), hsv_mask_red
        # )

        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        real = cv2.cvtColor(real, cv2.COLOR_BGR2GRAY)
        # imwrite(os.path.join("/tmp/form-segmentation", f"mask.png"), mask)
        # imwrite(os.path.join("/tmp/form-segmentation", f"real.png"), real)

        # OR original and generated mask and then AND with red mask
        blended_img = cv2.bitwise_or(real, mask)
        blended_img = cv2.bitwise_and(blended_img, hsv_mask_red)
        blended_img = cv2.cvtColor(blended_img, cv2.COLOR_GRAY2BGR)

        return blended_img

    def segment(
        self, document_id: str, img_path: str, checksum: str = None, raise_oom=False
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Segment form image and return original, mask, segmented images. If there is no mask extracted we return original
        image as mask and segmented image.

        :param document_id: unique document id
        :param img_path: image to process
        :param checksum: image checksum
        :param raise_oom: raise out of memory exception
        :return: original, mask, segmented tuple of images in numpy format
        """
        with Timer(text="segment in {:.4f} seconds"):

            if not os.path.exists(img_path):
                raise Exception("File not found : {}".format(img_path))

            name = document_id if checksum is None else checksum

            work_dir = ensure_exists(os.path.join(self.work_dir, name, "work"))
            debug_dir = ensure_exists(os.path.join(self.work_dir, name, "debug"))
            dataroot_dir = ensure_exists(
                os.path.join(self.work_dir, name, "dataroot_overlay")
            )
            dst_file_name = os.path.join(dataroot_dir, f"overlay_{name}.png")
            src_img = cv2.imread(img_path)
            if len(src_img.shape) != 3:
                raise Exception("Expected image shape is h,w,c")

            try:
                # TODO : load image from memory rather than disk
                real_img = self.preprocess(src_img)
                imwrite(dst_file_name, real_img)
                fake_mask = self.__extract_segmentation_mask(real_img, dataroot_dir)

                # Unable to segment return empty mask
                if np.array(fake_mask).size == 0:
                    # create dummy white image
                    real_img = np.ones(
                        (src_img.shape[0], src_img.shape[1], 3), dtype=np.uint8
                    )
                    return real_img, fake_mask, real_img

                fake_mask, blended = self.postprocess(src_img, real_img, fake_mask)

                tm = time.time_ns()
                if debug_visualization_enabled:
                    imwrite(
                        os.path.join(debug_dir, "overlay_{}.png".format(tm)), fake_mask
                    )

                return src_img, fake_mask, blended
            except RuntimeError as e:
                if "out of memory" in str(e) and not raise_oom:
                    log_oom(e)
                    if hasattr(torch.cuda, "empty_cache"):
                        torch_gc()
                    return self.segment(document_id, img_path, checksum, raise_oom=True)
                else:
                    raise e
            finally:
                torch_gc()

    def segment_frame(
        self, document_id: str, frame: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Segment from given frame

        :param document_id:
        :param frame:
        """

        frame_checksum = hash_frames_fast(frames=[frame])
        ensure_exists(os.path.join(self.work_dir, frame_checksum))
        img_path = os.path.join(
            self.work_dir, frame_checksum, f"{document_id}_{frame_checksum}.png"
        )
        imwrite(img_path, frame)

        return self.segment(document_id, img_path, frame_checksum)

    def run_onnx(self, img: Union[Image.Image, np.ndarray]) -> np.ndarray:
        """
        Run onnx model on given image
        @param img:
        @return:
        """
        model = self.model
        # check if PIL image
        if isinstance(img, Image.Image):
            data = np.array(img).astype(np.float32)
        else:
            data = img.astype(np.float32)

        # data = np.array(img).astype(np.float32)
        # convert from HWC to CHW
        data = np.transpose(data, (2, 0, 1))
        data = np.expand_dims(data, axis=0)  # add batch dimension  N x C x W x H

        starttime = timeit.default_timer()
        # Output > N x C x W x H
        outputs = model(data)
        batch_output = outputs[0][0]  # get the first batch
        # tensor to numpy
        image_numpy = batch_output.detach().cpu().numpy()
        # convert from CHW to HWC and scale from [-1, 1] to [0, 255]
        image_numpy = (
            (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0
        )  # post-processing: transpose and scaling

        # convert to pillow image
        img = Image.fromarray(image_numpy.astype("uint8")).convert("RGB")
        img.save(f"/tmp/onnx_test.png")
        print("Eval time is :", timeit.default_timer() - starttime)
        return image_numpy.astype("uint8")


class NoopOverlayProcessor(BaseHandler):
    def __init__(
        self,
        work_dir: str,
        models_dir: str = os.path.join(__model_path__),
        cuda: bool = True,
        **kwargs,
    ) -> None:
        super().__init__()

    def segment_frame(
        self, document_id: str, frame: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        NOOP Segment from given frame

        :param document_id:
        :param frame:
        """

        return frame, frame, frame
