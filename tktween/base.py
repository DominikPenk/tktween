from __future__ import annotations

import abc
import tkinter as tk
from typing import Any, TypeAlias

ObjectId: TypeAlias = int
TweenAble: TypeAlias = tk.Widget | ObjectId 

class TweenAnimator(abc.ABC):
    def __init__(self):
        self.started = False
        self.animation_data: dict[TweenAble, Any] = dict()


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
    def step(self, widget:TweenAble, t:float) -> None:
        pass

    def inverted(self) -> TweenAnimator:
        raise NotImplementedError("'inverted' not implemented for this Animator")


    def finalize(self, widget:TweenAble) -> None:
        self.animation_data.pop(widget)


    def __call__(self, widget:TweenAble, t:float) -> None:
        if widget not in self.animation_data:
            self.animation_data[widget] = self.start(widget)
        return self.step(widget, t)
    
