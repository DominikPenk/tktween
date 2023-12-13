from __future__ import annotations

import abc
import tkinter as tk
import uuid
from typing import Any, Optional, TypeAlias

ObjectId: TypeAlias = int
TweenAble: TypeAlias = tk.Widget | tuple[tk.Canvas, ObjectId] 

class TweenAnimator(abc.ABC):
    def __init__(self):
        self.started = False
        self.animation_data: dict[uuid.UUID, Any] = dict()


    @abc.abstractmethod
    def start(self, widget:TweenAble) -> Any:
        """Called when a new animation using this animator is started.

        Args:
            widget (TweenAble): The widget to be animated

        Returns:
            Any: Data needed for animation
        """
        pass


    @abc.abstractmethod
    def step(self, widget:TweenAble, t:float, animation_data:Any) -> None:
        pass


    def inverted(self) -> TweenAnimator:
        raise NotImplementedError("'inverted' not implemented for this Animator")


    def finalize(self, widget:TweenAble, animation_id:uuid.UUID) -> None:
        self.animation_data.pop(animation_id)


    def __call__(self, widget:TweenAble, t:float, animation_id:uuid.UUID) -> None:
        if animation_id not in self.animation_data:
            self.animation_data[animation_id] = self.start(widget)
        animation_data = self.animation_data[animation_id]
        self.step(widget, t, animation_data)
    
