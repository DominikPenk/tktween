from __future__ import annotations

import tkinter as tk
from typing import Callable

from .base import TweenAnimator, ObjectId
from .utils import lerp
import numpy as np

__all__ = [
    'MoveAnimation',
    'SizeAnimation',
    'LambdaAnimation'
]

class CanvasElementAnimation(TweenAnimator):
    def __init__(
        self,
        element: ObjectId
    ) -> None:
        super().__init__()
        self.element = element

    def get_anchor(self, canvas: tk.Canvas):
        coords = np.array(canvas.coords(self.element)).reshape(-1, 2)
        xmin, ymin = coords.min(axis=0)
        xmax, ymax = coords.max(axis=0)
        return 0.5 * np.array([xmin + xmax, ymin + ymax])


class LinearCanvasElementAnimation(CanvasElementAnimation):
    def __init__(
        self,
        element: ObjectId
    ) -> None:
        super().__init__(element)

    def start(self, canvas: tk.Canvas) -> None:
        self.anchor = self.get_anchor(canvas)
        self._pts = np.array(canvas.coords(self.element)).reshape(-1, 2) 
        self._pts = np.concatenate([
            self._pts,
            np.ones((self._pts.shape[0], 1))
        ], axis=1)


    def get_transform(self, t: float) -> np.matrix:
        pass


    def step(self, canvas: tk.Canvas, t: float) -> None:
        T = self.get_transform(t)
        if T.shape != (2, 3):
            raise RuntimeError("Invalid transformation matrix")
        pts = np.einsum('ij,nj->ni', T, self._pts)
        canvas.coords(self.element, *pts.flatten())


# Animation types
class MoveAnimation(LinearCanvasElementAnimation):
    def __init__(
        self,
        element: ObjectId,
        x:int | None = None,
        y:int | None = None,
        relx: float | None = None,
        rely: float | None = None
    ) -> None:
        super().__init__(element)
        if relx is not None or rely is not None:
            raise ValueError("For now we do not support relative position for canvas items")
        self.x = x
        self.y = y

    def get_transform(self, t:float) -> None:
        x0, y0 = self.anchor
        x = lerp(x0, self.x, t)
        y = lerp(y0, self.y, t)
        return np.array([[1.0, 0.0, (x - x0)], [0.0, 1.0, (y - y0)]])

class SizeAnimation(LinearCanvasElementAnimation):
    def __init__(self, element:ObjectId, width:int|None, height:int|None):
        super().__init__()
        self.width = width
        self.height = height
        self.w0, self.h0 = None, None

    def start(self, canvas: tk.Canvas):
        super().start(canvas)
        x0, y0, x1, y1 = canvas.bbox(self.element)

    def step(self, widget: tk.Widget, t: float) -> None:
        widget.configure(
            width=lerp(self.w0, self.width, t),
            height=lerp(self.h0, self.height, t)
        )


class LambdaAnimation(TweenAnimator):
    def __init__(self, animator:Callable[[tk.Widget, float], None]):
        super().__init__()
        self.animator = animator

    def start(self, widget: tk.Widget):
        pass

    def step(self, widget: tk.Widget, t: float) -> None:
        self.animator(widget, t)
