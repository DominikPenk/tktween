from __future__ import annotations

import tkinter as tk
import uuid
from typing import Any, Literal, Optional

import numpy as np

from .base import ObjectId, TweenAnimator
from .scene import SceneObject
from .tween import TweenDirector
from .utils import Color, lerp, lerp_color, rgb_to_hex

__all__ = [
    'Translate',
    'Rotate',
    'FillColor'
]

class CanvasTweenAnimator(TweenAnimator):    
    def start(self, obj: SceneObject) -> Any:
        return None

    def step(self, obj: SceneObject, t: float, animation_data: Any) -> None:
        pass        

    def __call__(self, widget:tuple[tk.Canvas, ObjectId], t:float, animation_id:uuid.UUID) -> None:
        canvas, element = widget
        # Get the animated object
        scene = TweenDirector.get().get_scene(canvas)
        target = scene.get_object(element)

        if animation_id not in self.animation_data:
            self.animation_data[animation_id] = self.start(target)
        animation_data = self.animation_data[animation_id]
        
        # This should update the target
        self.step(target, t, animation_data)


class Translate(CanvasTweenAnimator):
    def __init__(
        self,
        dx:int | None = None,
        dy:int | None = None,
    ) -> None:
        super().__init__()
        self.dx = dx
        self.dy = dy

    def start(self, obj:SceneObject) -> tuple[float, float]:
        return obj.translation.copy()

    def step(self, obj: SceneObject, t: float, animation_data: tuple[float, float]) -> None:
        x0, y0 = animation_data
        x = lerp(x0, x0 + self.dx, t) if self.dx else x0
        y = lerp(y0, y0 + self.dy, t) if self.dy else y0
        obj.translation = np.array([x, y])


class Rotate(CanvasTweenAnimator):
    def __init__(self, angle:float) -> None:
        super().__init__()
        self.angle=angle

    def start(self, obj:SceneObject) -> float:
        return obj.rotation
    
    def step(self, obj: SceneObject, t: float, a0: float) -> None:
        a = lerp(a0, a0+self.angle, t)
        obj.rotation = a


class FillColor(CanvasTweenAnimator):
    def __init__(
        self, 
        start_color:Optional[Color]=None,
        end_color:Optional[Color]=None,
        mode:Literal['rgb', 'hsv']='rgb',
        clockwise:Optional[bool]=None
    ) -> None:
        super().__init__()
        self.start_color = start_color
        self.end_color = end_color
        self.mode = mode
        self.clockwise = clockwise

    def start(self, obj: SceneObject) -> tuple[Color, Color]:
        canvas = obj.scene.canvas
        current_color = canvas.itemconfigure(obj.idx, "fill")[-1]

        c1 = self.start_color or current_color
        c2 = self.end_color or current_color

        return c1, c2
    
    def step(self, obj: SceneObject, t: float, animation_data: tuple[Color, Color]) -> None:
        c1, c2 = animation_data
        c = lerp_color(c1, c2, t, mode=self.mode, clockwise=self.clockwise)
        obj.scene.canvas.itemconfigure(obj.idx, fill=rgb_to_hex(c))
        