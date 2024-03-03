"""
Copyright Wenyi Tang 2024

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

Choose a proper backend to evaluate ONNX models.
1. ReferenceEvaluator: no extra dependency, but extremely slow.
2. OpenVINO runtime: best for Intel platforms.
3. OnnxRuntime: best compatibility and balanced performance.
"""

# pylint: disable=import-outside-toplevel

from contextlib import suppress
from tempfile import TemporaryDirectory
from typing import Literal

import onnx


def _get_eval_backend(backend, model):
    if backend == "onnx":
        from onnx.reference import ReferenceEvaluator

        model = ReferenceEvaluator(model)

        def _run_code(output_names, inputs_feed):
            return model.run(output_names, inputs_feed)

        return _run_code
    elif backend == "onnxruntime":
        import onnxruntime

        with TemporaryDirectory() as tmpdir:
            onnx.save_model(model, f"{tmpdir}/model.onnx")
            sess = onnxruntime.InferenceSession(f"{tmpdir}/model.onnx")

        def _run_code(output_names, inputs_feed):
            return sess.run(output_names, inputs_feed)

        return _run_code
    elif backend == "openvino":
        import openvino

        with TemporaryDirectory() as tmpdir:
            onnx.save_model(model, f"{tmpdir}/model.onnx")
            model = openvino.compile_model(f"{tmpdir}/model.onnx")

        def _run_code(output_names, inputs_feed):
            outputs = model(inputs_feed)
            return [outputs[name] for name in output_names]

        return _run_code

    raise NotImplementedError(f"Unsupported backend: {backend}")


class Evaluator:
    """An evaluator wraps different backends to evaluate ONNX models."""

    def __init__(
        self, model, backend: Literal["AUTO", "OpenVINO", "OnnxRuntime"] = "AUTO"
    ):
        if backend == "AUTO":
            with suppress(ImportError):
                # pylint: disable=unused-import
                import openvino  # noqa: F401

                backend = "OpenVINO"
        if backend == "AUTO":
            with suppress(ImportError):
                # pylint: disable=unused-import
                import onnxruntime  # noqa: F401

                backend = "OnnxRuntime"
        if backend == "AUTO":
            backend = "onnx"

        self._call_fn = _get_eval_backend(backend.lower(), model)

    def __call__(self, output_names, feed_inputs):
        return self._call_fn(output_names, feed_inputs)
