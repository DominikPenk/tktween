from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Literal, Optional

from tktween.base import TweenAble

from .base import TweenAnimator
from .utils import Color, lerp, lerp_color, rgb_to_hex

__all__ = [
    'Translate',
    'Resize',
    'StyleAnimator',
    'Background',
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
        widget.update_idletasks()
        x0 = widget.winfo_x()
        y0 = widget.winfo_y()
        return x0, y0

    
    def step(self, widget: tk.Widget, t: float, animation_data: tuple[int, int]) -> None:
        x0, y0 = animation_data
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


class Resize(TweenAnimator):
    def __init__(
        self,
        width:Optional[int] = None,
        height:Optional[int] = None,
        scale_factor_width: Optional[float] = None,
        scale_factor_height: Optional[float] = None
    ) -> None:
        super().__init__()
        if width and scale_factor_width:
            raise ValueError("Only one of 'width' and 'scale_factor_width' can be set.")
        if height and scale_factor_height:
            raise ValueError("Only one of 'height' and 'scale_factor_height' can be set.")
        self.width = width
        self.height = height
        self.scale_factor_width = scale_factor_width
        self.scale_factor_height = scale_factor_height

    def start(self, widget: tk.Widget) -> tuple[int, int, int | float, int | float]:
        widget.update_idletasks()
        w0 = widget.winfo_width()
        h0 = widget.winfo_height()
        w1 = w0 * self.scale_factor_width if self.scale_factor_width else self.width
        h1 = h0 * self.scale_factor_height if self.scale_factor_height else self.height
        return w0, h0, w1, h1
    

    def step(self, widget: TweenAble, t: float, animation_data: Any) -> None:
        w0, h0, w1, h1 = animation_data
        width  = lerp(w0, w1, t)
        height = lerp(h0, h1, t)
        widget.place(width=width, height=height)


class StyleAnimator(TweenAnimator):
    def __init__(self) -> None:
        super().__init__()
        self.style = ttk.Style()

    def start(self, widget: TweenAble) -> str:
        if not isinstance(widget, ttk.Widget):
            raise ValueError("Style Animation only implemented for ttk Widgets")
        return self.set_animated_style(widget)

    def get_current_color(self, widget: ttk.Widget, cfg: str) -> Color:
        current_style = widget['style']
        current_color = self.style.lookup(current_style, cfg)
        current_color = tuple((x>>8) / 255 for x in widget.winfo_rgb(current_color))
        return current_color

    def set_animated_style(self, widget: tk.Widget) -> str:
        style_name = f"tktween.{widget.winfo_id()}.{widget.winfo_class()}"
        current_style = widget['style']
        if current_style != style_name:
            config = self.style.configure(current_style)
            if config:
                self.style.configure(style_name, **config)
            widget.configure(style=style_name)
        return style_name

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


    def start(self, widget: tk.Widget) -> tuple[Color, Color, str]:
        style_name = super().start(widget)
        current_color = self.get_current_color(widget, "background")

        c1 = self.start_color or current_color
        c2 = self.end_color or current_color

        return c1, c2, style_name
    
    
    def step(self, widget: tk.Widget, t: float, animation_data:tuple[Color, Color, str]) -> None:
        c1, c2, style = animation_data
        c = lerp_color(c1, c2, t, mode=self.mode, clockwise=self.clockwise)
        self.style.configure(style, background=rgb_to_hex(c))


    def inverse(self) -> TweenAnimator:
        return Background(
            start_color=self.end_color,
            end_color=self.start_color,
            mode=self.mode,
            clockwise=not self.clockwise
        )
    