import numpy as np

from typing import TYPE_CHECKING, Optional, Tuple, Any, List

from magicgui import widgets
from magicgui.widgets import Container, create_widget

if TYPE_CHECKING:
    import napari


class PredictLabels(Container):
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self._viewer = viewer
        self._image_layer_combo = create_widget(
            label="Image", annotation="napari.layers.Image"
        )
        self._predict_btn = widgets.PushButton(text="Predict Labels")
        self._predict_btn.clicked.connect(self._request_prediction)

        self.extend(
            [
                self._image_layer_combo,
                self._predict_btn
            ]
        )
    
    def _request_prediction(self):
        image_layer = self._image_layer_combo.value
        if image_layer is None:
            raise(ValueError("Select an image layer first."))
        
        shape = image_layer.data.shape
        labels = np.random.randint(0, 4, size=shape, dtype=np.uint8) 
        
        name = image_layer.name + "_labels"
        if name in self._viewer.layers:
            self._viewer.layers[name].data += labels
        
        self._viewer.add_labels(labels, name=name)
        
