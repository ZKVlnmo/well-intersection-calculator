from pydantic import BaseModel, ValidationError

from src.model.DataModel import DataModel


class WellIntersectionCalculator:
     data = None
     result = []
     def __init__ (self, point_z):
         try:
             self.data = DataModel(**point_z)
             self.checkBoundaryValues()
         except ValidationError as e:
             print("❌ Ошибка валидации данных:")
             print(e.json())

     def checkBoundaryValues(self):
         for i in range(len( self.data.trajectories)):
             max_trajec_z = max(sublist[2] for sublist in self.data.trajectories[i])
             min_trajec_z = min(sublist[2] for sublist in self.data.trajectories[i])
             max_grid_z = max(max(row) for row in self.data.grid.height_matrix)
             min_grid_z = max(max(row) for row in self.data.grid.height_matrix)
             if max_trajec_z >min_grid_z or min_trajec_z<max_grid_z:
                 self.result.append(-1)
             else:
                 self.result.append(None)
         print(self.result)


