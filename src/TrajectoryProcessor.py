from pydantic import ValidationError
from bilinear_interpolation import bilinear_interpolation_4terms, binary_search_nearest, bresenham_grid_with_corners,is_point_in_rectangle
from src.Model import GridModel,TrajectoriesModel
from spatial_geometry import best_fit_plane,line_plane_intersection,line_from_two_points


class TrajectoryProcessor:
    result = []

    def __init__(self):
        pass
    def calculateIntersections (self, point):
        try:
            # Инициализация данных и проверка граничных значений
            self.data = TrajectoriesModel(**point)
            self.check_boundary_values()
            for i in range(len(self.result)):
                if self.result[i] is not None:
                    # Найти ближайшие точки и пересечения
                    near_point = self.find_near_point(self.data.trajectories[i])
                    self.result[i] = self.find_line_plane_intersection(near_point)
            for i in range(len(self.result)):
                 print(f"result trajectories {i}:" ,self.result[i])
            return  self.result
        except ValidationError as e:
            print("❌ Ошибка валидации данных:")
            print(e.json())

    def check_boundary_values(self):
        """Проверяет граничные значения для каждой траектории."""

        for trajectory in self.data.trajectories:
            # Находим максимальные и минимальные значения высоты траектории
            max_trajec_z = max(sublist[2] for sublist in trajectory)
            min_trajec_z = min(sublist[2] for sublist in trajectory)

            # Обработка height_matrix, игнорируя None значения
            max_grid_z = float('-inf')  # Начальное значение для максимума
            min_grid_z = float('inf')  # Начальное значение для минимума

            for row in self.data.grid.height_matrix:
                for value in row:
                    if value is not None:  # Игнорируем None
                        max_grid_z = max(max_grid_z, value)
                        min_grid_z = min(min_grid_z, value)

            # Если значения траектории выходят за пределы высотной сетки
            if max_trajec_z > max_grid_z or min_trajec_z < min_grid_z:
                self.result.append([])  # Заготовка для точек
            else:
                self.result.append(None)  # Если точек нет

    def find_near_point(self, trajectories):
        """Находит ближайшие точки для заданных траекторий."""
        near_x_trajectories = []
        near_y_trajectories = []
        z_near_xy = []


        for t in trajectories:
            near_x = binary_search_nearest(self.data.grid.x_coords, t[0])
            near_y = binary_search_nearest(self.data.grid.y_coords, t[1])

            # Если все индексы найдены, извлекаем высотные значения
            if all(idx is not None for idx in near_x["index"] + near_y["index"]):
                z_near_xy.append([
                    self.data.grid.height_matrix[near_x["index"][dx]][near_y["index"][dy]]
                    for dx in (0, 1) for dy in (0, 1)
                ])
            else:
                z_near_xy.append([None] * 4)

            near_x_trajectories.append(near_x)
            near_y_trajectories.append(near_y)

        # Анализируем точки на основе их интерполированных значений

        near_point = []
        flag = 0
        if flag == 1:
            for i in range(len(near_x_trajectories) - 1):
                if None not in z_near_xy[i] and None not in z_near_xy[i + 1]:
                    z_vals = [bilinear_interpolation_4terms(
                        trajectories[j][0], trajectories[j][1],
                        near_x_trajectories[j]["value"][0], near_x_trajectories[j]["value"][1],
                        near_y_trajectories[j]["value"][0], near_y_trajectories[j]["value"][1],
                        z_near_xy[j]
                    ) for j in (i, i + 1)]
                    if (z_vals[0] > trajectories[i][2]) != (z_vals[1] > trajectories[i + 1][2]):
                        near_point.append([trajectories[i], trajectories[i + 1]])
        else:
            for i in range(len(near_x_trajectories) - 1):
                if [point is not None for point in z_near_xy[i]].count(False) <= 1 and \
                        [point is not None for point in z_near_xy[i + 1]].count(False) <= 1:
                    # Фильтруем None значения и находим максимумы и минимумы для z_near_xy[j] и z_near_xy[j+1]
                    filtered_z_j = [point for point in z_near_xy[i] if point is not None]
                    filtered_z_jp1 = [point for point in z_near_xy[i + 1] if point is not None]
                    if ((max(filtered_z_j) < trajectories[i][2] and min(filtered_z_jp1) > trajectories[i + 1][2])
                            or (min(filtered_z_j) > trajectories[i][2] and  max(filtered_z_jp1) < trajectories[i + 1][2])):
                        near_point.append([trajectories[i], trajectories[i + 1]])



        return near_point

    def find_line_plane_intersection(self, near_point):
        """Находит пересечения прямых с плоскостью."""
        print("Near_point:", near_point)
        result = []
        for i in range(len(near_point)):
            # Получаем координаты углов, которые пересекает прямая
            corners = bresenham_grid_with_corners(
                near_point[i][0][0], near_point[i][0][1],
                near_point[i][1][0], near_point[i][1][1],
                self.data.grid.x_coords, self.data.grid.y_coords
            )

            for j in range(len(corners)):
                # Формируем список точек с высотами
                points = [
                    [corners[j]["value"][0], corners[j]["value"][1],
                     self.data.grid.height_matrix[int(corners[j]["index"][0])][int(corners[j]["index"][1])]],
                    [corners[j]["value"][0], corners[j]["value"][3],
                     self.data.grid.height_matrix[int(corners[j]["index"][0])][int(corners[j]["index"][3])]],
                    [corners[j]["value"][2], corners[j]["value"][1],
                     self.data.grid.height_matrix[int(corners[j]["index"][2])][int(corners[j]["index"][1])]],
                    [corners[j]["value"][2], corners[j]["value"][3], self.data.grid.height_matrix[int(corners[j]["index"][2])][int(corners[j]["index"][3])]]
                ]

                # Находим коэффициенты плоскости
                plane = best_fit_plane(points)

                # Строим линию по двум точкам
                line_point, line_dir = line_from_two_points(near_point[i][0], near_point[i][1])

                if plane is not None:
                    # Находим точку пересечения
                    intersection = line_plane_intersection(plane, line_point, line_dir)

                    # Проверяем, лежит ли точка пересечения внутри прямоугольника
                    if is_point_in_rectangle(intersection, points):

                       result.append(intersection)

        return result


