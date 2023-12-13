from __future__ import annotations

import tkinter as tk
import uuid

from .base import TweenAble, ObjectId, TweenAnimator
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
        self.duration  = int(round(duration * 30)) 
        self.offset    = int(round(offset * 30))
        self.easing    = get_easing(easing)


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


    def cancel(self) -> bool:
        """Cancel the tween represented by this handle

        Returns:
            True if the tween was canceled or False if it was already terminated 
        """
        # TODO: Actually implement this
        return True


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
            self._after_id = self.root.after_idle(self._animation_heartbeat, 0)

    def get_scene(self, canvas:tk.Canvas) -> Scene:
        if canvas not in self._scenes:
            self._scenes[canvas] = Scene(canvas)
        return self._scenes[canvas]

    def _animation_heartbeat(self, frame_id: int):
        """
        Handle one animation frame, updating all active tweens.

        Args:
            frame_id (int): Frame id.

        Returns:
            None
        """
        finished_tweens = []
        for tween_id, tween_handle in self._active_tweens.items():
            running = tween_handle.tween.animation_frame(frame_id, tween_handle)
            if not running:
                finished_tweens.append(tween_id)

        for scene in self._scenes.values():
            scene.update()

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

        if handle.loop:
            num_frames = self.get_num_frames()
            iteration, frame_id = divmod(frame_id, num_frames)
            if iteration % 2 == 1:
                frame_id = num_frames - frame_id

        # If we loop, we are always running
        running = handle.loop

        for block in self.animation_sequence:
            rel_frame = frame_id - block.offset
            
            if 0 <= rel_frame <= block.duration:
                t_rel = (frame_id - block.offset) / block.duration
                t_rel = block.easing(t_rel)
                
                for animator in block.animators:
                    animator(handle.widget, t_rel, handle.id)

                if rel_frame == block.duration and not handle.loop:
                    block.finalize(handle)

            running = running or (frame_id < block.offset + block.duration) 
        
        return running


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
        self._parallel_offset = self._then_offset
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


    def get_num_frames(self) -> int:
        return int(round(self._then_offset * 30))


class CanvasTween(Tween):
    def run(self, canvas: tk.Canvas, target: ObjectId, loop:bool=False) -> TweenHandle:
        return TweenDirector.get().start_animation((canvas, target), self, loop)