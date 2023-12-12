from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Literal, Optional

from .base import TweenAnimator
from .utils import Color, lerp, lerp_color, rgb_to_hex

__all__ = [
    'Translate',
    'Background'
]

# Animation types
class Translate(TweenAnimator):
    def __init__(
        self,
        x:Optional[int] = None,
        y:Optional[int] = None
    ) -> None:
        super().__init__()
        self.x = x
        self.y = y


    def start(self, widget: tk.Widget) -> Any:
        x0 = widget.winfo_x()
        y0 = widget.winfo_y()
        return x0, y0

    
    def step(self, widget: tk.Widget, t: float) -> None:
        x0, y0 = self.animation_data[widget]
        dx = lerp(0, self.x, t)
        dy = lerp(0, self.y, t)
        widget.place(
            x=x0 + dx,
            y=y0 + dy
        )

    def inverse(self) -> Translate:
        return Translate(
            x = -self.x if self.x else None,
            y = -self.y if self.y else None
        )


class StyleAnimator(TweenAnimator):
    def __init__(self) -> None:
        super().__init__()
        self.style = ttk.Style()


    def get_animated_style(self, widget: tk.Widget) -> str:
        if not isinstance(widget, ttk.Widget):
            raise ValueError("Style Animation only implemented for ttk Widgets")
        
        return f"tktween.{widget.winfo_id()}.{widget.winfo_class()}"


class Background(StyleAnimator):
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


    def start(self, widget: tk.Widget) -> Any:
        style_name = self.get_animated_style(widget)
        
        current_style = widget['style']

        # Get the current color
        current_color = self.style.lookup(current_style, "background")
        current_color = tuple((x>>8) / 255 for x in widget.winfo_rgb(current_color))

        if current_style != style_name:
            config = self.style.configure(current_style)
            if config:
                self.style.configure(style_name, **config)
            widget.configure(style=style_name)

        c1 = self.start_color or current_color
        c2 = self.end_color or current_color

        return c1, c2, style_name
    
    
    def step(self, widget: tk.Widget, t: float) -> None:
        c1, c2, style = self.animation_data[widget]
        c = lerp_color(c1, c2, t, mode=self.mode, clockwise=self.clockwise)
        self.style.configure(style, background=rgb_to_hex(c))
