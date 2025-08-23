import numpy as np
import pytest

from napari_bootseg._widget import (
    PredictLabels
)

import numpy as np
import pytest

from napari_bootseg._widget import PredictLabels

def test_container_has_children_in_order(make_napari_viewer):
    viewer = make_napari_viewer()
    w = PredictLabels(viewer)

    # Container behaves like a list of its children
    assert len(w) == 2
    # The exact objects you created are present and ordered
    assert w[0] is w._image_layer_combo
    assert w[1] is w._predict_btn

def test_request_prediction_without_selection_raises(make_napari_viewer):
    viewer = make_napari_viewer()
    w = PredictLabels(viewer)

    # No image selected -> should raise a clear error
    with pytest.raises(ValueError):
        w._request_prediction()

@pytest.mark.parametrize("shape", [(32, 32), (8, 16), (4, 4, 4)])
def test_request_prediction_adds_labels_layer(make_napari_viewer, shape):
    viewer = make_napari_viewer()
    img = np.random.random(shape)
    layer = viewer.add_image(img, name="im")

    w = PredictLabels(viewer)
    # select the layer via the combobox widget
    w._image_layer_combo.value = layer

    # act
    w._request_prediction()  # your method should add/replace a labels layer

    # assert
    name = "im_pred"
    assert name in viewer.layers, "Prediction layer not added"
    pred = viewer.layers[name]
    assert pred.data.shape == img.shape
    # labels must be integer-typed in napari
    assert np.issubdtype(pred.data.dtype, np.integer)

def test_button_is_connected_to_action(make_napari_viewer):
    """Lightweight check that clicking the button triggers the action.

    We don't rely on monkeypatching the method; we just observe the side-effect.
    """
    viewer = make_napari_viewer()
    img = np.ones((10, 10))
    layer = viewer.add_image(img, name="im")

    w = PredictLabels(viewer)
    w._image_layer_combo.value = layer

    # programmatically "click" the magicgui PushButton
    w._predict_btn.clicked.emit()  # same effect as a user click

    assert "im_pred" in viewer.layers

