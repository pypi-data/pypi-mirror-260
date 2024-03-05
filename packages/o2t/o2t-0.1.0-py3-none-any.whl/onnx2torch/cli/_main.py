from typing import Union

import onnx


def convert(
    model: Union[str, onnx.ModelProto],
    output_model: str = None,
    check: bool = False,
):
    from onnx2torch.core.parser import OnnxPytorchParser

    onnx2torch = OnnxPytorchParser(model)
    onnx2torch.convert()

    if check:
        onnx2torch.check()

    if not output_model:
        return onnx2torch.pytorch_graph_module
    else:
        onnx2torch.save(output_model)


def main():
    import argparse

    from loguru import logger

    import onnx2torch

    parser = argparse.ArgumentParser(
        description="onnx2torch: Onnx to Pytorch Converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input_model", help="input onnx model")
    parser.add_argument(
        "output_model", nargs="?", default=None, help="output onnx model"
    )

    parser.add_argument("--check", action="store_true", help="enable model check")
    parser.add_argument(
        "-v", "--version", action="version", version=onnx2torch.__version__
    )

    args, unknown = parser.parse_known_args()

    if unknown:
        logger.error(f"unrecognized options: {unknown}")
        return 1

    convert(
        args.input_model,
        args.output_model,
        args.check,
    )

    return 0
