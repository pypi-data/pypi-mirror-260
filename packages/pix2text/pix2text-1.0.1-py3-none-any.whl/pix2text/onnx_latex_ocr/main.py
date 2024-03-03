# coding: utf-8
# Copyright (C) 2024, [Breezedeus](https://github.com/breezedeus).
#
# credit to: https://github.com/RapidAI/RapidLaTeXOCR
# Adapted from https://github.com/RapidAI/RapidLaTeXOCR
import argparse
import logging
import os
import re
import time
import traceback
from pathlib import Path
from typing import Tuple, Union, Optional, Dict, Any, List

import numpy as np
import yaml
from PIL import Image
from cnocr.utils import get_default_ort_providers
from cnstd.utils import get_model_file
from pix2tex.utils import in_model_path

from ..consts import LATEX_CONFIG_FP, MODEL_VERSION, AVAILABLE_MODELS, DOWNLOAD_SOURCE
from ..utils import data_dir
from .models import EncoderDecoder
from .utils import PreProcess, TokenizerCls
from .utils_load import InputType, LoadImage, LoadImageError, OrtInferSession


logger = logging.getLogger(__name__)


def download_models(model_info, resizer_model_info, args):
    ckpt_list = [args["resizer_checkpoint"], args["mfr_checkpoint"]]
    for idx, (info, fp) in enumerate(zip([model_info, resizer_model_info], ckpt_list)):
        if idx == 0 and not os.path.exists(fp):
            logger.warning(f'model file {fp} not found, downloading...')
            info['filename'] = info['url']
            get_model_file(
                info, args["model_root_dir"], download_source=DOWNLOAD_SOURCE
            )  # download the .zip file and unzip
        if idx == 1:
            sub_dir = fp
            for fp in ("encoder.onnx", "decoder.onnx"):
                fp = os.path.join(sub_dir, fp)
                if not os.path.exists(fp):
                    logger.warning(f'model file {fp} not found, downloading...')
                    info['filename'] = info['url']
                    get_model_file(
                        info, args["model_root_dir"], download_source=DOWNLOAD_SOURCE
                    )  # download the .zip file and unzip


class LatexOCROnnx(object):
    @in_model_path()
    def __init__(
        self,
            *,
            model_name: str = 'mfr',
            context: str = 'cpu',  # ['cpu', 'gpu', 'cuda']
            ort_providers: Optional[List[str]] = None,
            model_fp: Optional[Union[str, Path]] = None,
            root: Union[str, Path] = data_dir(),
            arguments: Optional[Dict[str, Any]] = None,

            # config_path: Union[str, Path] = DEFAULT_CONFIG,
        # image_resizer_path: Union[str, Path] = None,
        # encoder_path: Union[str, Path] = None,
        # decoder_path: Union[str, Path] = None,
        # tokenizer_json: Union[str, Path] = None,
    ):
        model_root_dir = Path(root) / MODEL_VERSION / 'formula'
        model_info = AVAILABLE_MODELS.get_info(model_name, 'onnx')
        resizer_model_info = AVAILABLE_MODELS.get_info('resizer', 'onnx')
        def_arguments = {
            'config': LATEX_CONFIG_FP,
            'mfr_checkpoint': model_root_dir / model_info['fn'],
            'resizer_checkpoint': model_root_dir / resizer_model_info['fn'],
            'model_root_dir': model_root_dir,
            # 'no_cuda': True,
            # 'no_resize': False,
            # 'device': context,
        }
        if arguments is not None:
            if 'model_fp' in arguments:
                arguments['mfr_checkpoint'] = arguments.pop('model_fp')
            def_arguments.update(arguments)
        if model_fp is not None:
            def_arguments['mfr_checkpoint'] = model_fp
        arguments = def_arguments

        # self.image_resizer_path = image_resizer_path
        self.encoder_path = arguments['mfr_checkpoint'] / 'encoder.onnx'
        self.decoder_path = arguments['mfr_checkpoint'] / 'decoder.onnx'

        download_models(model_info, resizer_model_info, arguments)

        with open(arguments["config"], "r", encoding="utf-8") as f:
            args = yaml.load(f, Loader=yaml.FullLoader)

        self.max_dims = [args.get("max_width"), args.get("max_height")]
        self.min_dims = [args.get("min_width", 32), args.get("min_height", 32)]
        self.temperature = args.get("temperature", 0.25)

        self.load_img = LoadImage()
        self.pre_pro = PreProcess(max_dims=self.max_dims, min_dims=self.min_dims)

        if ort_providers is None:
            ort_providers = get_default_ort_providers()

        self.image_resizer = OrtInferSession(arguments["resizer_checkpoint"], providers=ort_providers)

        self.encoder_decoder = EncoderDecoder(
            encoder_path=self.encoder_path,
            decoder_path=self.decoder_path,
            bos_token=args["bos_token"],
            eos_token=args["eos_token"],
            max_seq_len=args["max_seq_len"],
            ort_providers=ort_providers,
        )
        self.tokenizer = TokenizerCls(args["tokenizer"])

    def __call__(self, img: InputType) -> Tuple[str, float]:
        s = time.perf_counter()

        try:
            img = self.load_img(img)
        except LoadImageError as exc:
            error_info = traceback.format_exc()
            raise LoadImageError(
                f"Load the img meets error. Error info is {error_info}"
            ) from exc

        try:
            resizered_img = self.loop_image_resizer(img)
        except Exception as e:
            error_info = traceback.format_exc()
            raise ValueError(
                f"image resizer meets error. Error info is {error_info}"
            ) from e

        try:
            dec = self.encoder_decoder(resizered_img, temperature=self.temperature)
        except Exception as e:
            error_info = traceback.format_exc()
            raise ValueError(
                f"EncoderDecoder meets error. Error info is {error_info}"
            ) from e

        decode = self.tokenizer.token2str(dec)
        pred = self.post_process(decode[0])

        elapse = time.perf_counter() - s
        return pred, elapse

    def loop_image_resizer(self, img: np.ndarray) -> np.ndarray:
        pillow_img = Image.fromarray(img)
        pad_img = self.pre_pro.pad(pillow_img)
        input_image = self.pre_pro.minmax_size(pad_img).convert("RGB")
        r, w, h = 1, input_image.size[0], input_image.size[1]
        for _ in range(10):
            h = int(h * r)
            final_img, pad_img = self.pre_process(input_image, r, w, h)

            resizer_res = self.image_resizer([final_img.astype(np.float32)])[0]

            argmax_idx = int(np.argmax(resizer_res, axis=-1))
            w = (argmax_idx + 1) * 32
            if w == pad_img.size[0]:
                break

            r = w / pad_img.size[0]
        return final_img

    def pre_process(
        self, input_image: Image.Image, r, w, h
    ) -> Tuple[np.ndarray, Image.Image]:
        if r > 1:
            resize_func = Image.Resampling.BILINEAR
        else:
            resize_func = Image.Resampling.LANCZOS

        resize_img = input_image.resize((w, h), resize_func)
        pad_img = self.pre_pro.pad(self.pre_pro.minmax_size(resize_img))
        cvt_img = np.array(pad_img.convert("RGB"))

        gray_img = self.pre_pro.to_gray(cvt_img)
        normal_img = self.pre_pro.normalize(gray_img)
        final_img = self.pre_pro.transpose_and_four_dim(normal_img)
        return final_img, pad_img

    @staticmethod
    def post_process(s: str) -> str:
        """Remove unnecessary whitespace from LaTeX code.

        Args:
            s (str): Input string

        Returns:
            str: Processed image
        """
        text_reg = r"(\\(operatorname|mathrm|text|mathbf)\s?\*? {.*?})"
        letter = "[a-zA-Z]"
        noletter = r"[\W_^\d]"
        names = [x[0].replace(" ", "") for x in re.findall(text_reg, s)]
        s = re.sub(text_reg, lambda match: str(names.pop(0)), s)
        news = s
        while True:
            s = news
            news = re.sub(r"(?!\\ )(%s)\s+?(%s)" % (noletter, noletter), r"\1\2", s)
            news = re.sub(r"(?!\\ )(%s)\s+?(%s)" % (noletter, letter), r"\1\2", news)
            news = re.sub(r"(%s)\s+?(%s)" % (letter, noletter), r"\1\2", news)
            if news == s:
                break
        return s


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("-img_resizer", "--image_resizer_path", type=str, default=None)
    # parser.add_argument("-encdoer", "--encoder_path", type=str, default=None)
    # parser.add_argument("-decoder", "--decoder_path", type=str, default=None)
    # parser.add_argument("-tokenizer", "--tokenizer_json", type=str, default=None)
    parser.add_argument("img_path", type=str, help="Only img path of the formula.")
    args = parser.parse_args()

    engine = LatexOCROnnx(
        # image_resizer_path=args.image_resizer_path,
        # encoder_path=args.encoder_path,
        # decoder_path=args.decoder_path,
        # tokenizer_json=args.tokenizer_json,
    )

    result, elapse = engine(args.img_path)
    print(result)
    print(f"cost: {elapse:.5f}")


if __name__ == "__main__":
    main()
