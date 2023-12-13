from __future__ import annotations

import tkinter as tk
import numpy as np

class SceneObject:
    def __init__(self, pts: np.ndarray, idx: int, scene: Scene) -> None:
        self.pts = pts
        self.idx = idx

        xmin, ymin = pts.min(axis=0)
        xmax, ymax = pts.max(axis=0)

        self._rotation    = 0.0
        self._scale       = 1.0
        self._translation = 0.5 * np.array([xmin + xmax, ymin + ymax])  
        self.pts -= self._translation[None, :]
        self.scene = scene


    @classmethod
    def from_element(cls, canvas: tk.Canvas, element: int, scene: Scene) -> SceneObject:
        pts = np.array(canvas.coords(element)).reshape(-1, 2).astype(np.float32)
        return SceneObject(pts, element, scene)
    

    def get_transformed(self) -> np.ndarray:
        a = np.radians(self._rotation)
        c, s = np.cos(a), np.sin(a)
        R = np.array([[c, -s], [s, c]])
        transformed_pts = np.einsum('ij,nj->ni', R, self._scale * self.pts) + self._translation[None, :]    
        return transformed_pts
    
    @property
    def scale(self) -> float:
        return self._scale
    
    @scale.setter
    def scale(self, s:float):
        self._scale = s
        self.scene.dirty.add(self.idx)

    @property
    def rotation(self) -> float:
        return self._rotation
    
    @rotation.setter
    def rotation(self, angle: float):
        self._rotation = angle
        self.scene.dirty.add(self.idx)

    @property
    def translation(self) -> np.ndarray:
        return self._translation
    
    @translation.setter
    def translation(self, vector: np.ndarray):
        self._translation = vector
        self.scene.dirty.add(self.idx)

class Scene:
    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas
        self.objects: dict[int, SceneObject] = {}
        self.dirty: set[int] = set()


    def get_object(self, element:int) -> SceneObject:
        if element not in self.objects:
            self.add_object(element)
        return self.objects[element]


    def add_object(self, element: int) -> SceneObject:
        if element in self.objects:
            msg = f"Object with ID {element} already in scene"
            raise KeyError(msg)
        obj = SceneObject.from_element(self.canvas, element, self)
        self.objects[element] = obj
        return obj
    

    def update(self):
        for element in self.dirty:
            new_pts = self.objects[element].get_transformed()
            self.canvas.coords(element, *new_pts.flatten())
        self.dirty = set()
