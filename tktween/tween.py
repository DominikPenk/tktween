from __future__ import annotations

import tkinter as tk
import uuid

from .base import TweenAble, TweenAnimator
from .easing import Easing, get_easing


class AnimationBlock:
    def __init__(
        self,
        animators:  list[TweenAnimator],
        duration:   float,
        offset:     float,
        easing:     Easing | None
    ) -> None:
        self.animators = animators
        self.duration  = int(round(duration * 30)) 
        self.offset    = int(round(offset * 30))
        self.easing    = get_easing(easing)
        self.uid       = uuid.uuid4()


    def finalize(self, handle:TweenHandle):
        for animator in self.animators:
            animator.finalize(handle.widget, self.uid)


class TweenHandle(object):
    def __init__(
        self,
        widget:tk.Widget,
        tween:Tween,
        after_id:int|None = None
    ) -> None:
        self.after_id = after_id
        self.widget = widget
        self.tween = tween
        self.frame_0 = None
        self.id = uuid.uuid4()


    def cancel(self) -> bool:
        """Cancel the tween represented by this handle

        Returns:
            True if the tween was canceled or False if it was already terminated 
        """
        if self.active:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
            return True
        return False


    @property
    def active(self) -> bool:
        return self.after_id is not None


class TweenDirector(object):
    _instance:TweenDirector = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._active_tweens: dict[uuid.UUID, TweenHandle] = {}
        self._after_id: int | None = None
        self._root: tk.Tk | None = None

    @property
    def root(self) -> tk.Tk:
        if self._root is None:
            self._root = tk._default_root
        return self._root
    
    @root.setter
    def root(self, root:tk.Tk) -> None:
        self._root = root

    def start_animation(self, widget: tk.Widget, tween: Tween):
        tween_handle = TweenHandle(widget, tween)
        self._active_tweens[tween_handle.id] = tween_handle
        if self._after_id is None:
            self._after_id = self.root.after_idle(self._animation_heartbeat, 0)

    def _animation_heartbeat(self, frame_id: int):
        finished_tweens = []
        for tween_id, tween_handle in self._active_tweens.items():
            running = tween_handle.tween.animation_frame(frame_id, tween_handle)
            if not running:
                finished_tweens.append(tween_id)
        for tween_id in finished_tweens:
            del self._active_tweens[tween_id]

        if self._active_tweens:
            self._after_id = self.root.after(30, self._animation_heartbeat, frame_id + 1)
        else:
            self._after_id = None


class Tween(object):
    def __init__(
        self,
        *animations,
        duration:float,
        easing:Easing|None=None
    ) -> None:
        """Create a Tween where the given animations are run in parallel

        Args:
            duration (float): duration of the animation in seconds
            easing (Easing | None, optional): Easing to use. Defaults to None.
        """
        self.animation_sequence: list[AnimationBlock] = [AnimationBlock(
            animations, 
            duration=duration,
            offset=0, 
            easing=easing
        )]
        self._then_offset: float = duration
        self._parallel_offset: float = 0


    def animation_frame(
        self, 
        global_frame_id: int,
        handle: TweenHandle
    ) -> bool:
        
        if handle.frame_0 is None:
            handle.frame_0 = global_frame_id

        frame_id = global_frame_id - handle.frame_0
        running = False

        for block in self.animation_sequence:
            rel_frame = frame_id - block.offset
            
            if 0 <= rel_frame <= block.duration:
                t_rel = (frame_id - block.offset) / block.duration
                t_rel = block.easing(t_rel)
                
                for animator in block.animators:
                    animator(handle.widget, t_rel, block.uid)

                if rel_frame == block.duration:
                    block.finalize(handle)

            running = running or (frame_id < block.offset + block.duration) 
        
        return running


    @classmethod
    def get_root_window(cls) -> tk.Tk:
        if Tween.__root is None:
            Tween.__root = tk._default_root
        return Tween.__root


    def then(
        self,
        *animations,
        duration:int,
        easing:Easing|None=None
    ) -> Tween:
        self.animation_sequence.append(AnimationBlock(
            animators=animations,
            duration=duration,
            offset=self._then_offset,
            easing=easing
        ))
        self._then_offset += duration
        return self
    

    def parallel(
        self,
        *animations,
        duration:float|None=None,
        easing:Easing|None=None
    ) -> Tween:
        """Run the given animations or tween in parallel"""
        duration = duration or self._then_offset
        self.animation_sequence.append(AnimationBlock(
            animators=animations,
            duration=duration,
            offset=self._parallel_offset,
            easing=easing
        ))
        return self


    def synchronize(self) -> Tween:
        """Wait untill all animation blocks are finished befor starting new blocks."""
        self._parallel_offset = self._then_offset
        return self


    def run(
        self,
        target: TweenAble,
    ) -> TweenHandle:
        return TweenDirector().start_animation(target, self)

