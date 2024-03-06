# Copyright (c) 2022 NVIDIA CORPORATION.  All rights reserved.
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import unittest

import warp as wp
from warp.tests.unittest_utils import *

wp.init()

from warp.context import runtime  # noqa: E402


@wp.kernel
def scale(
    x: wp.array(dtype=float),
    y: wp.array(dtype=float),
):
    y[0] = x[0] ** 2.0


@wp.kernel(enable_backward=True)
def scale_1(
    x: wp.array(dtype=float),
    y: wp.array(dtype=float),
):
    y[0] = x[0] ** 2.0


@wp.kernel(enable_backward=False)
def scale_2(
    x: wp.array(dtype=float),
    y: wp.array(dtype=float),
):
    y[0] = x[0] ** 2.0


def test_options_1(test, device):
    x = wp.array([3.0], dtype=float, requires_grad=True, device=device)
    y = wp.zeros_like(x)

    wp.set_module_options({"enable_backward": False})

    tape = wp.Tape()
    with tape:
        wp.launch(scale, dim=1, inputs=[x, y], device=device)

    tape.backward(y)
    assert_np_equal(tape.gradients[x].numpy(), np.array(0.0))


def test_options_2(test, device):
    x = wp.array([3.0], dtype=float, requires_grad=True, device=device)
    y = wp.zeros_like(x)

    wp.set_module_options({"enable_backward": True})

    tape = wp.Tape()
    with tape:
        wp.launch(scale, dim=1, inputs=[x, y], device=device)

    tape.backward(y)
    assert_np_equal(tape.gradients[x].numpy(), np.array(6.0))


def test_options_3(test, device):
    x = wp.array([3.0], dtype=float, requires_grad=True, device=device)
    y = wp.zeros_like(x)

    wp.set_module_options({"enable_backward": False})

    tape = wp.Tape()
    with tape:
        wp.launch(scale_1, dim=1, inputs=[x, y], device=device)

    tape.backward(y)
    assert_np_equal(tape.gradients[x].numpy(), np.array(6.0))


def test_options_4(test, device):
    x = wp.array([3.0], dtype=float, requires_grad=True, device=device)
    y = wp.zeros_like(x)

    wp.set_module_options({"enable_backward": True})

    tape = wp.Tape()
    with tape:
        wp.launch(scale_2, dim=1, inputs=[x, y], device=device)

    tape.backward(y)
    assert_np_equal(tape.gradients[x].numpy(), np.array(0.0))


@unittest.skipUnless(runtime.core.is_cutlass_enabled(), "Warp was not built with CUTLASS support")
def test_options_5(test, device):
    wp.set_module_options({"enable_backward": True})

    @wp.kernel
    def loss_kernel(y: wp.array(dtype=float), loss: wp.array(dtype=float)):
        tid = wp.tid()
        wp.atomic_add(loss, 0, y[tid])

    A = wp.array(np.ones((2, 2), dtype=float), dtype=float, requires_grad=True, device=device)
    x = wp.array([[1.0], [2.0]], dtype=float, requires_grad=True, device=device)
    b = wp.zeros_like(x)
    y = wp.zeros_like(x)
    loss = wp.zeros(1, requires_grad=True, device=device)

    tape = wp.Tape()

    with tape:
        wp.matmul(A, x, b, y)
        wp.launch(loss_kernel, dim=2, inputs=[y.flatten(), loss], device=device)

    tape.backward(loss)
    assert_np_equal(x.grad.numpy(), np.array([[2.0], [2.0]]))


@unittest.skipUnless(runtime.core.is_cutlass_enabled(), "Warp was not built with CUTLASS support")
def test_options_6(test, device):
    wp.set_module_options({"enable_backward": False})

    @wp.kernel
    def loss_kernel(y: wp.array(dtype=float), loss: wp.array(dtype=float)):
        tid = wp.tid()
        wp.atomic_add(loss, 0, y[tid])

    A = wp.array(np.ones((2, 2), dtype=float), dtype=float, requires_grad=True, device=device)
    x = wp.array([[1.0], [2.0]], dtype=float, requires_grad=True, device=device)
    b = wp.zeros_like(x)
    y = wp.zeros_like(x)
    loss = wp.zeros(1, requires_grad=True, device=device)

    tape = wp.Tape()

    with tape:
        wp.matmul(A, x, b, y)
        wp.launch(loss_kernel, dim=2, inputs=[y.flatten(), loss], device=device)

    tape.backward(loss)
    assert_np_equal(x.grad.numpy(), np.array([[0.0], [0.0]]))


devices = get_test_devices()


class TestOptions(unittest.TestCase):
    pass


add_function_test(TestOptions, "test_options_1", test_options_1, devices=devices)
add_function_test(TestOptions, "test_options_2", test_options_2, devices=devices)
add_function_test(TestOptions, "test_options_3", test_options_3, devices=devices)
add_function_test(TestOptions, "test_options_4", test_options_4, devices=devices)
add_function_test(TestOptions, "test_options_5", test_options_5, devices=devices)
add_function_test(TestOptions, "test_options_6", test_options_6, devices=devices)


if __name__ == "__main__":
    wp.build.clear_kernel_cache()
    unittest.main(verbosity=2)
