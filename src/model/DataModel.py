from pydantic import BaseModel, ValidationError
from typing import List

class GridModel(BaseModel):
    x_coords: List[float]
    y_coords: List[float]
    height_matrix: List[List[float]]

class DataModel(BaseModel):
    grid: GridModel
    trajectories: List[List[List[float]]]