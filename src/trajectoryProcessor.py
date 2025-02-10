from pydantic import ValidationError
from typing import List, Dict, Tuple, Optional
from grid_math import (
    bilinear_interpolation_4terms,
    binary_search_nearest,
    bresenham_grid_with_corners,
    is_point_in_rectangle
)
from src.model import GridModel, TrajectoriesModel
from spatial_geometry import best_fit_plane, line_plane_intersection, line_from_two_points


class TrajectoryProcessor:
    """
    Класс для обработки траекторий и нахождения их пересечений с поверхностью.
    """

    def __init__(self) -> None:
        """Инициализация TrajectoryProcessor."""
        pass

    def calculate_intersections(self, data: Dict) -> Optional[List[Optional[List[Tuple[float, float, float]]]]]:
        """
        Вычисляет пересечения траекторий с поверхностью.

        :param data: Входные данные, соответствующие модели TrajectoriesModel.
        :return: Список пересечений для каждой траектории или None при ошибке валидации.
        """
        try:
            self.data = TrajectoriesModel(**data)
            result: List[Optional[List[Tuple[float, float, float]]]] = self.check_boundary_values()

            for i in range(len(result)):
                if result[i] is not None:
                    potential_intersection_points_neighbors = self.find_potential_intersection_points_neighbors(
                        self.data.trajectories[i],1)
                    result[i] = self.find_line_plane_intersection(potential_intersection_points_neighbors)

            return result
        except ValidationError as e:
            print("❌ Ошибка валидации данных:")
            print(e.json())
            return None

    def check_boundary_values(self) -> List[Optional[List[Tuple[float, float, float]]]]:
        """
        Проверяет граничные значения высот траекторий относительно сетки.

        :return: Список результатов: None если выход за границы, [] если в пределах.
        """
        result: List[Optional[List[Tuple[float, float, float]]]] = []

        for trajectory in self.data.trajectories:
            max_trajec_z = max(point[2] for point in trajectory)
            min_trajec_z = min(point[2] for point in trajectory)

            max_grid_z = float('-inf')
            min_grid_z = float('inf')

            for row in self.data.grid.height_matrix:
                for value in row:
                    if value is not None:
                        max_grid_z = max(max_grid_z, value)
                        min_grid_z = min(min_grid_z, value)

            if max_trajec_z > max_grid_z or min_trajec_z < min_grid_z:
                result.append([])
            else:
                result.append(None)

        return result

    def find_potential_intersection_points_neighbors(self, trajectory: List[Tuple[float, float, float]], flag: int) -> \
    List[List[Tuple[float, float, float]]]:
        """
        Находит точки отрезок между которами пересекает поверхность.

        :param trajectory: Список точек траектории [(x, y, z)]. :param x: flag позволяет выбрать, каким обозом
        определять положение относительно плоскости, 0 если использовать интерполяцию и 1 если точку экстремума квадрата
        :return: Список пар точек, где может происходить пересечение.
        """
        neighbors_x_trajectory = []
        neighbors_y_trajectory = []
        z_neighbors_xy = []

        for t in trajectory:
            neighbors_x = binary_search_nearest(self.data.grid.x_coords, t[0])
            neighbors_y = binary_search_nearest(self.data.grid.y_coords, t[1])

            if all(idx is not None for idx in neighbors_x["index"] + neighbors_y["index"]):
                z_neighbors_xy.append([
                    self.data.grid.height_matrix[neighbors_x["index"][dx]][neighbors_y["index"][dy]]
                    for dx in (0, 1) for dy in (0, 1)
                ])
            else:
                z_neighbors_xy.append([None] * 4)

            neighbors_x_trajectory.append(neighbors_x)
            neighbors_y_trajectory.append(neighbors_y)
        potential_intersection_points_neighbors = []

        if flag == 0:
            for i in range(len(near_x_trajectories) - 1):
                if None not in z_near_xy[i] and None not in z_near_xy[i + 1]:
                    z_vals = [bilinear_interpolation_4terms(
                        trajectories[j][0], trajectories[j][1],
                        neighbors_x_trajectory[j]["value"][0], neighbors_x_trajectory[j]["value"][1],
                        neighbors_y_trajectory[j]["value"][0], neighbors_y_trajectory[j]["value"][1],
                        z_near_xy[j]
                    ) for j in (i, i + 1)]
                    if (z_vals[0] > trajectories[i][2]) != (z_vals[1] > trajectories[i + 1][2]):
                        near_point.append([trajectories[i], trajectories[i + 1]])
        elif flag == 1:
            for i in range(len(neighbors_x_trajectory) - 1):
                if [point is not None for point in z_neighbors_xy[i]].count(False) <= 1 and \
                        [point is not None for point in z_neighbors_xy[i + 1]].count(False) <= 1:
                    filtered_z_i = [point for point in z_neighbors_xy[i] if point is not None]
                    filtered_z_ip1 = [point for point in z_neighbors_xy[i + 1] if point is not None]
                    if ((max(filtered_z_i) < trajectory[i][2] and min(filtered_z_ip1) > trajectory[i + 1][2])
                            or (min(filtered_z_i) > trajectory[i][2] and max(filtered_z_ip1) < trajectory[i + 1][
                                2])):
                        potential_intersection_points_neighbors.append([trajectory[i], trajectory[i + 1]])

        return potential_intersection_points_neighbors

    def find_line_plane_intersection(self, near_point: List[List[Tuple[float, float, float]]]) -> List[
        Tuple[float, float, float]]:
        """
        Находит пересечения траекторий с плоскостью используя точки кандидаты найденные в функции find_potential_intersection_points_neighbors.

        :param near_point: Список пар точек кандидатов, образующих прямые.
        :return: Список координат точек пересечения траекторию и поверхности.
        """
        result: List[Tuple[float, float, float]] = []

        for segment in near_point:
            corners = bresenham_grid_with_corners(
                segment[0][0], segment[0][1],
                segment[1][0], segment[1][1],
                self.data.grid.x_coords, self.data.grid.y_coords
            )

            for corner in corners:
                points = [
                    (corner["value"][dx], corner["value"][dy],
                     self.data.grid.height_matrix[int(corner["index"][dx])][int(corner["index"][dy])])
                    for dx in (0, 2) for dy in (1, 3)
                ]

                plane = best_fit_plane(points)
                line_point, line_dir = line_from_two_points(segment[0], segment[1])

                if plane:
                    intersection = line_plane_intersection(plane, line_point, line_dir)
                    if is_point_in_rectangle(intersection, points):
                        result.append(intersection)

        return result
