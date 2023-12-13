from __future__ import annotations

from typing import Any
import tkinter as tk
import numpy as np

class SceneObject:
    """
    Represents an object within a scene on a Tkinter canvas.

    Attributes:
        pts (np.ndarray): The points defining the object.
        idx (int): The object's identifier in the scene.
        scene (Scene): The scene to which the object belongs.
    """

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


    def configure(self, *args, **kwargs):
        """
        Configures the appearance of the object on the canvas.

        This method is a wrapper for `self.scene.canvas.itemconfigure(self.idx)`.

        Args:
            *args: Variable-length argument list passed to `canvas.itemconfigure()`.
            **kwargs: Arbitrary keyword arguments passed to `canvas.itemconfigure()`.
        """
        self.scene.canvas.itemconfigure(self.idx, *args, **kwargs)

    
    def get_config(self, cfg:str) -> Any:
        """
        Gets the configuration value of the object on the canvas.

        This method is a wrapper for `self.canvas.itemconfigure(self.index, cfg)`.

        Args:
            cfg (str): The configuration option to retrieve.

        Returns:
            Any: The value of the specified configuration option.
        """
        return self.scene.canvas.itemconfigure(self.idx, cfg)[-1]


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
        """
        Scale factor of the object.

        Returns:
            float: The scale factor.
        """
        return self._scale
    
    @scale.setter
    def scale(self, s:float):
        self._scale = s
        self.scene.dirty.add(self.idx)

    @property
    def rotation(self) -> float:
        """
        Rotation angle of the object.

        Returns:
            float: The rotation angle in degrees.
        """
        return self._rotation
    
    @rotation.setter
    def rotation(self, angle: float):
        self._rotation = angle
        self.scene.dirty.add(self.idx)

    @property
    def translation(self) -> np.ndarray:
        """
        Translation vector of the object.

        Returns:
            np.ndarray: The translation vector.
        """
        return self._translation
    
    @translation.setter
    def translation(self, vector: np.ndarray):
        self._translation = vector
        self.scene.dirty.add(self.idx)

class Scene:
    """
    Represents a scene containing objects on a Tkinter canvas.

    Attributes:
        canvas (tk.Canvas): The canvas associated with the scene.
        objects (dict[int, SceneObject]): A dictionary of objects in the scene, indexed by their identifiers.
        dirty (set[int]): A set of object identifiers that need updating.
    """

    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas
        self.objects: dict[int, SceneObject] = {}
        self.dirty: set[int] = set()


    def get_object(self, element:int) -> SceneObject:
        """
        Gets a SceneObject associated with a canvas element.

        Args:
            element (int): The identifier of the canvas element.

        Returns:
            SceneObject: The associated SceneObject.
        """
        if element not in self.objects:
            self.add_object(element)
        return self.objects[element]


    def add_object(self, element: int) -> SceneObject:
        """
        Adds a new object to the scene based on a canvas element.

        Args:
            element (int): The identifier of the canvas element.

        Returns:
            SceneObject: The newly added SceneObject.
        """
        if element in self.objects:
            msg = f"Object with ID {element} already in scene"
            raise KeyError(msg)
        obj = SceneObject.from_element(self.canvas, element, self)
        self.objects[element] = obj
        return obj
    

    def update(self):
        """
        Updates the scene by applying transformations to dirty objects on the canvas.
        """
        for element in self.dirty:
            new_pts = self.objects[element].get_transformed()
            self.canvas.coords(element, *new_pts.flatten())
        self.dirty = set()
