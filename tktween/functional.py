import tkinter as tk
from .tween import TweenDirector, Tween
from .scene import Scene

__all__ = [
    'get_fps',
    'set_fps',
    'is_running',
    'get_root',
    'set_root',
    'get_scene'
]

def get_fps() -> int:
    return TweenDirector.get().fps

def set_fps(fps:int) -> None:
    TweenDirector.get().fps = fps

def is_running(tween:Tween, widget:tk.Widget) -> bool:
    return TweenDirector.get().is_active(tween, widget)

def get_root() -> tk.Tk:
    return TweenDirector.get().root

def set_root(root:tk.Tk) -> None:
    TweenDirector.get().root = root

def get_scene(canvas:tk.Canvas) -> Scene:
    return TweenDirector.get().get_scene(canvas)
