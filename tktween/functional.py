import tkinter as tk
import uuid

from typing import Callable
from .scene import Scene
from .tween import Tween, TweenDirector, TweenHandle

__all__ = [
    'get_fps',
    'set_fps',
    'is_running',
    'get_root',
    'set_root',
    'get_scene',
    'on_tween_finished',
    'remove_on_tween_finised'
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

def on_tween_finished(callback: Callable[[TweenHandle], None]) -> uuid.UUID:
    return TweenDirector.get().add_callback(callback)

def remove_on_tween_finised(uid: uuid.UUID) -> None:
    TweenDirector.get().remove_callback(uid)
