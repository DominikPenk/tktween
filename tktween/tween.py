from __future__ import annotations

import time
import tkinter as tk
import bisect
from collections import defaultdict
from dataclasses import dataclass

import numpy as np

from .base import ObjectId, TweenAble, TweenAnimator
from .easing import Easing, get_easing


@dataclass
class AnimationBlock:
    animators:  list[TweenAnimator]
    duration:   float
    easing:     Easing | None
    next:       AnimationBlock | None = None

    def finalize(self, handle:TweenHandle):
        for animator in self.animators:
            animator.finalize(handle.widget)


class TweenHandle(object):
    def __init__(
        self,
        widget:tk.Widget,
        after_id:int|None = None
    ) -> None:
        self.after_id = after_id
        self.widget = widget


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


class Tween(object):
    T0s: dict[TweenAble, float] = defaultdict(lambda: time.time())


    def __init__(
        self,
        *animations,
        duration:int,
        easing:Easing|None=None
    ) -> None:
        """Create a Tween where the given animations are run in parallel

        Args:
            duration (int): duration of the animation
            easing (Easing | None, optional): Easing to use. Defaults to None.
        """
        self.animation_sequence: list[AnimationBlock] = [AnimationBlock(
            animations, 
            duration=duration, 
            easing=easing
        )]


    def animation_frame(
        self, 
        handle: TweenHandle
    ):
        cumulative_durations = np.cumsum([block.duration for block in self.animation_sequence])
        def step_fn():
            elapsed_time = time.time() - Tween.T0s[handle.widget]

            # Find the current animation block using bisect
            interval_index = bisect.bisect_left(cumulative_durations, elapsed_time)

            # Ensure block_id is within bounds
            interval_index = max(0, min(interval_index, len(cumulative_durations) - 1))

            current_block = self.animation_sequence[interval_index]
            block_relative_time = elapsed_time - (cumulative_durations[interval_index - 1] if interval_index > 0 else 0)
            block_relative_time = max(0, min(1, block_relative_time / current_block.duration))
            block_relative_time = get_easing(current_block.easing)(block_relative_time)

            for animator in current_block.animators:
                animator(handle.widget, block_relative_time)

            if elapsed_time < cumulative_durations[-1]:
                handle.after_id = handle.widget.after(10, self.animation_frame(handle))
            else:
                handle.after_id = None
                Tween.T0s.pop(handle.widget)
                for block in self.animation_sequence:
                    block.finalize(handle)
        return step_fn


    @classmethod
    def is_widget_currently_animated(cls, target: TweenAble):
        return target in Tween.T0s


    def then(
        self,
        *animations,
        duration:int,
        easing:Easing|None=None
    ) -> Tween:
        self.animation_sequence.append(AnimationBlock(
            animators=animations,
            duration=duration,
            easing=easing
        ))
        return self
    

    def run(
        self,
        target: TweenAble,
    ) -> TweenHandle:
        if Tween.is_widget_currently_animated(target):
            raise RuntimeError("The target is already animated.")
        handle = TweenHandle(widget=target)
        handle.after_id = target.after_idle(self.animation_frame(handle))
        return handle

