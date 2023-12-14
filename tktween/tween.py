from __future__ import annotations

import time
import tkinter as tk
import uuid
from typing import Callable

from .base import ObjectId, TweenAble, TweenAnimator
from .easing import Easing, get_easing
from .scene import Scene


class AnimationBlock:
    """
    A block of animations to be processed grouped together.

    Attributes:
        animators (list[TweenAnimator]): List of animators to be used in block.
        duration (float): Number of frames specifying block's duration.
        offset (float): Number of frames specifying block's offset.
        easing (Easing | None): An easing function applied to block. If None, no easing applied.
        uid (uuid.UUID): A unique identifier for animation block.
    """

    def __init__(
        self,
        animators:  list[TweenAnimator],
        duration:   float,
        offset:     float,
        easing:     Easing | None
    ) -> None:
        self.animators = animators
        self.time_duration = duration 
        self.time_offset   = offset
        self.easing = get_easing(easing)

    @property
    def duration(self) -> int:
        return int(round(self.time_duration * TweenDirector.get().fps))

    
    @property
    def offset(self) -> int:
        return int(round(self.time_offset * TweenDirector.get().fps))

    def finalize(self, handle:TweenHandle):
        """
        Finalize the animation block.

        Args:
            handle (TweenHandle): Handle of the tween.
        """
        for animator in self.animators:
            animator.finalize(handle.widget, handle.id)


class TweenHandle(object):
    def __init__(
        self,
        widget:tk.Widget,
        tween:Tween,
        loop:bool
    ) -> None:
        self.widget = widget
        self.tween = tween
        self.loop = loop
        self.frame_0 = None
        self.id = uuid.uuid4()


    def cancel(self, revert:bool=False) -> bool:
        """Cancel the tween represented by this handle

        Returns:
            True if the tween was canceled or False if it was already terminated 
        """
        director = TweenDirector.get()
        return director.cancel_tween(self, revert)


class TweenDirector(object):
    """
    Singleton class that manages Tweens and handles animations.
    """
    _instance:TweenDirector = None
    
    def __init__(self):
        self._active_tweens: dict[uuid.UUID, TweenHandle] = {}
        self._after_id: int | None = None
        self._root: tk.Tk | None = None
        self._scenes: dict[tk.Canvas, Scene] = {}
        self._callbacks: dict[uuid.UUID, Callable[[TweenHandle], None]] = {}
        self.fps: int = 30

    @property
    def root(self) -> tk.Tk:
        """
        Get the root widget.

        Returns:
            tk.Tk: The root widget.
        """
        if self._root is None:
            self._root = tk._default_root
        return self._root
    
    @root.setter
    def root(self, root:tk.Tk) -> None:
        """
        Set the root widget.
        
        Args:
            root (tk.Tk): The Tk widget to be set as root.
        """
        self._root = root

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = TweenDirector()
        return cls._instance

    def start_animation(self, widget: tk.Widget, tween: Tween, loop:bool):
        """
        Start the animation by creating a TweenHandle, storing it, and scheduling the first animation frame.

        Args:
            widget (tk.Widget): Target widget of the tween.
            tween (Tween): Tween object.
        """
        tween_handle = TweenHandle(widget, tween, loop)
        self._active_tweens[tween_handle.id] = tween_handle
        if self._after_id is None:
            self._after_id = self.root.after_idle(self._animation_heartbeat, time.time(), -1)
        return tween_handle

    def cancel_tween(self, handle:TweenHandle, revert:bool) -> bool:
        if handle.id not in self._active_tweens:
            return False
        
        if self._active_tweens.pop(handle.id) != handle:
            raise RuntimeError("Tween UIDs are mixed up")
        handle.tween.cancel(handle, revert)
        return True

    def is_active(self, tween:Tween, widget: tk.Widget) -> bool:
        return any(
            h.tween == tween and h.widget.winfo_id() == widget.winfo_id()  
            for h in self._active_tweens.values()
        )

    def get_scene(self, canvas:tk.Canvas) -> Scene:
        if canvas not in self._scenes:
            self._scenes[canvas] = Scene(canvas)
        return self._scenes[canvas]

    def add_callback(self, callback: Callable[[TweenHandle], None]) -> uuid.UUID:
        uid = uuid.uuid4()
        self._callbacks[uid] = callback
        return uid
    
    def remove_callback(self, uid:uuid.uuid4) -> None:
        self._callbacks.pop(uid)

    def _animation_heartbeat(self, t0: float, last_frame_id:int):
        """
        Handle one animation frame, updating all active tweens.

        Args:
            t0 (float): The first time this method was called.

        Returns:
            None
        """
        finished_tweens = []

        t = time.time() - t0
        frame_id = int(round(t * self.fps))

        for tween_id, tween_handle in self._active_tweens.items():
            running = tween_handle.tween.animation_frame(frame_id, last_frame_id, tween_handle)
            if not running:
                finished_tweens.append(tween_id)

        for scene in self._scenes.values():
            scene.update()

        for tween_id in finished_tweens:
            h = self._active_tweens.pop(tween_id)
            for callback in h.tween._callbacks.values():
                callback(h)

            for callback in self._callbacks.values():
                callback(h)
            
        if self._active_tweens:
            next_frame_time = t0 + (frame_id + 1) / self.fps 
            delay = max(10, int(1000 * (next_frame_time - time.time())))
            self._after_id = self.root.after(delay, self._animation_heartbeat, t0, frame_id)
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
        self._callbacks: dict[uuid.UUID, Callable[[TweenHandle], None]] = {}


    def animation_frame(
        self, 
        global_frame_id: int,
        last_global_frame_id: int,
        handle: TweenHandle
    ) -> bool:
        """
        Process one frame of all blocks in the animation sequence.

        Args:
            global_frame_id (int): The frame id relative to the start of the application.
            handle (TweenHandle): Handle of the tween.

        Returns:
            bool: False if all animations are finished, True otherwise.
        """
        
        if handle.frame_0 is None:
            handle.frame_0 = global_frame_id

        frame_id = global_frame_id - handle.frame_0
        last_frame_id = last_global_frame_id - handle.frame_0 

        if handle.loop:
            num_frames = self.get_num_frames()
            iteration, frame_id = divmod(frame_id, num_frames)
            if iteration % 2 == 1:
                frame_id = num_frames - frame_id
        else:
            # Handle the edge case, that we are beyond the last frame of the animation 
            # In this case, we skipped the last frame previously, so just clamp the frame back
            frame_id = max(0, min(self.get_num_frames(), frame_id))


        # If we loop, we are always running
        running = handle.loop

        for block in self.animation_sequence:

            duration = block.duration
            offset   = block.offset
            
            rel_frame = frame_id - offset
            last_rel_frame = last_frame_id - offset
            
            t_rel = None

            if 0 <= rel_frame <= duration:
                t_rel = (frame_id - offset) / duration
                t_rel = block.easing(t_rel)
            elif rel_frame > duration and last_rel_frame < duration:
                t_rel = 1.0
                
            if t_rel is not None:
                for animator in block.animators:
                    animator(handle.widget, t_rel, handle.id)

                if t_rel == 1 and not handle.loop:
                    block.finalize(handle)
                
                running = running or rel_frame < block.duration 

        
        return running


    def cancel(self, handle:TweenHandle, revert:bool) -> None:
        if revert:
            self.animation_frame(handle.frame_0, handle)
        for block in self.animation_sequence:
            block.finalize(handle)


    def then(
        self,
        *animations,
        duration:int,
        easing:Easing|None=None
    ) -> Tween:
        """
        Add new animations which are starting after the previous ones.
        
        Args:
            *animations: Animation objects.
            duration (int): Duration of the animation in seconds.
            easing (Easing | None, optional): Easing function to apply. Defaults to None.
            
        Returns:
            Tween: The current Tween instance for chaining.
        """
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
        """
        Run the given animations or tween in parallel.

        Args:
            *animations: Animation objects.
            duration (float | None, optional): Duration of animation in seconds. Defaults to same as previous block.
            easing (Easing | None, optional): Easing function to apply. Defaults to None.
        
        Returns:
            Tween: The current Tween instance for chaining.
        """
        duration = duration or self._then_offset
        self.animation_sequence.append(AnimationBlock(
            animators=animations,
            duration=duration,
            offset=self._parallel_offset,
            easing=easing
        ))
        return self


    def synchronize(self) -> Tween:
        """
        Wait until all animation blocks are finished before starting new blocks.

        Returns:
            Tween: The current Tween instance for chaining.
        """
        t = self.get_duration()
        self._parallel_offset = t
        self._then_offset = t
        return self


    def pause(self, duration:float) -> Tween:
        self._then_offset += duration
        return self


    def run(
        self,
        target: TweenAble,
        loop:bool=False
    ) -> TweenHandle:
        """
        Run the animation on a target.

        Args:
            target (TweenAble): The target widget to animate.

        Returns:
            TweenHandle: Handle of the tween.
        """
        return TweenDirector.get().start_animation(target, self, loop)


    def add_callback(self, callback: Callable[[TweenHandle], None]) -> uuid.UUID:
        uid = uuid.uuid4()
        self._callbacks[uid] = callback
        return uid
    

    def remove_callback(self, uid: uuid.UUID) -> None:
        self._callbacks.pop(uid)


    def is_running(self, widget:tk.Widget) -> bool:
        return TweenDirector.get().is_active(self, widget)


    def get_duration(self) -> float:
        return self.get_num_frames() / TweenDirector.get().fps


    def get_num_frames(self) -> int:
        max_frames = 0
        for block in self.animation_sequence:
            end_frame = block.offset + block.duration
            max_frames = max(max_frames, end_frame)
        return max_frames


class CanvasTween(Tween):
    def run(self, canvas: tk.Canvas, target: ObjectId, loop:bool=False) -> TweenHandle:
        return TweenDirector.get().start_animation((canvas, target), self, loop)