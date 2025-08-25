import numpy as np

from typing import TYPE_CHECKING, Optional, Tuple, Any, List

from magicgui import widgets
from magicgui.widgets import Container, create_widget

from .core.infer import predict_roi

if TYPE_CHECKING:
    import napari


class PredictLabels(Container):
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self._viewer = viewer
        
        # image layer combo
        self._image_layer_combo = create_widget(
            label="Image", annotation="napari.layers.Image"
        )


        # prediction button
        self._predict_btn = widgets.PushButton(text="Predict Labels")
        self._predict_btn.clicked.connect(self._predict)

        

        self.extend(
            [
                self._image_layer_combo,
                self._predict_btn
            ]
        )
    
    def _predict(self):
        image_layer = self._image_layer_combo.value
        print(type(image_layer))
        if image_layer is None:
            raise(ValueError("Select an image layer first."))
        
        prediction = predict_roi(image_layer.data)
        
        name = image_layer.name + "_labels"
        if name in self._viewer.layers:
            self._viewer.layers[name].data += prediction
        
        self._viewer.add_labels(prediction, name=name)
        
