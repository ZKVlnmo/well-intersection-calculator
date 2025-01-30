from pydantic import BaseModel, ValidationError

from src.model.DataModel import DataModel


class WellIntersectionCalculator:
     point_z = None
     def __init__ (self, point_z):
         try:
             point_z = DataModel(**point_z)
         except ValidationError as e:
             print("❌ Ошибка валидации данных:")
             print(e.json())

     def find_z(x, y):
         point_z