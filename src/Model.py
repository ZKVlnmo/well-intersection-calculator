from pydantic import BaseModel, ValidationError
from typing import List, Any

class GridModel(BaseModel):
    x_coords: List[float]
    y_coords: List[float]
    height_matrix: List[List[Any]]

class TrajectoriesModel(BaseModel):
    grid: GridModel
    trajectories: List[List[List[float]]]