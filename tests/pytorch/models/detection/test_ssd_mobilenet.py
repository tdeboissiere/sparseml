import os
from typing import Callable, Union

import pytest
import torch

from sparseml.pytorch.models import ModelRegistry, ssd300lite_mobilenetv2
from tests.pytorch.models.utils import compare_model


@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_PYTORCH_TESTS", False),
    reason="Skipping pytorch tests",
)
@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_MODEL_TESTS", False),
    reason="Skipping model tests",
)
@pytest.mark.parametrize(
    "key,pretrained,pretrained_backbone,test_input,match_const",
    [("ssd300lite_mobilenetv2", False, True, True, ssd300lite_mobilenetv2)],
)
def test_ssd_resnsets(
    key: str,
    pretrained: Union[bool, str],
    pretrained_backbone: Union[bool, str],
    test_input: bool,
    match_const: Callable,
):
    model = ModelRegistry.create(key, pretrained)
    diff_model = match_const(pretrained_backbone=pretrained_backbone)

    if pretrained:
        compare_model(model, diff_model, same=False)
        match_model = ModelRegistry.create(key, pretrained)
        compare_model(model, match_model, same=True)

    if pretrained_backbone is not True:
        compare_model(model.feature_extractor, diff_model.feature_extractor, same=False)
        match_model = ModelRegistry.create(key, pretrained_backbone=pretrained_backbone)
        compare_model(
            diff_model.feature_extractor, match_model.feature_extractor, same=True
        )

    if test_input:
        input_shape = ModelRegistry.input_shape(key)
        batch = torch.randn(1, *input_shape)
        model.eval()
        boxes, scores = model(batch)
        assert isinstance(boxes, torch.Tensor)
        assert isinstance(scores, torch.Tensor)
        assert boxes.dim() == 3
        assert scores.dim() == 3
        assert boxes.size(0) == 1
        assert boxes.size(1) == 4
        assert scores.size(0) == 1
        assert boxes.size(2) == scores.size(2)  # check same num default boxes
