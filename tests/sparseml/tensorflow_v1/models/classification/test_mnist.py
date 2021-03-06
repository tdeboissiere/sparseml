# Copyright (c) 2021 - present / Neuralmagic, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import Union

import numpy
import pytest

from sparseml.tensorflow_v1.models import ModelRegistry, mnist_net
from sparseml.tensorflow_v1.utils import tf_compat


@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_TENSORFLOW_TESTS", False),
    reason="Skipping tensorflow_v1 tests",
)
@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_MODEL_TESTS", False),
    reason="Skipping model tests",
)
def test_mnist():
    with tf_compat.Graph().as_default():
        inputs = tf_compat.placeholder(
            tf_compat.float32, [None, 28, 28, 1], name="inputs"
        )
        logits = mnist_net(inputs)

        with tf_compat.Session() as sess:
            sess.run(tf_compat.global_variables_initializer())
            out = sess.run(
                logits, feed_dict={inputs: numpy.random.random((1, 28, 28, 1))}
            )
            assert out.sum() != 0


@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_TENSORFLOW_TESTS", False),
    reason="Skipping tensorflow_v1 tests",
)
@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_MODEL_TESTS", False),
    reason="Skipping model tests",
)
@pytest.mark.parametrize(
    "key,pretrained,test_input",
    [
        ("mnistnet", False, True),
        ("mnistnet", True, False),
        ("mnistnet", "base", False),
    ],
)
def test_mnist_registry(key: str, pretrained: Union[bool, str], test_input: bool):
    with tf_compat.Graph().as_default():
        inputs = tf_compat.placeholder(
            tf_compat.float32, [None, 28, 28, 1], name="inputs"
        )
        logits = ModelRegistry.create(key, inputs)

        with tf_compat.Session() as sess:
            if test_input:
                sess.run(tf_compat.global_variables_initializer())
                out = sess.run(
                    logits, feed_dict={inputs: numpy.random.random((1, 28, 28, 1))}
                )
                assert out.sum() != 0

            if pretrained:
                ModelRegistry.load_pretrained(key, pretrained)

                if test_input:
                    out = sess.run(
                        logits, feed_dict={inputs: numpy.random.random((1, 28, 28, 1))}
                    )
                    assert out.sum() != 0
