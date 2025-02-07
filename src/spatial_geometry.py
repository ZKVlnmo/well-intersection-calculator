
import numpy as np


def best_fit_plane_three_points(points):
    # Проверяем, что точки не равны None
    if any(p[2] is None for p in points):
        return None  # Если хотя бы одна точка имеет None в z, возвращаем None

    # Распаковываем координаты точек
    p1, p2, p3 = points
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    # Вектор (P2 - P1) и (P3 - P1)
    v1 = np.array([x2 - x1, y2 - y1, z2 - z1])
    v2 = np.array([x3 - x1, y3 - y1, z3 - z1])

    # Векторное произведение для нахождения нормали плоскости
    normal = np.cross(v1, v2)

    A, B, C = normal  # Коэффициенты нормали

    # Вычисляем D, используя точку P1
    D = -(A * x1 + B * y1 + C * z1)

    return A, B, C, D

def best_fit_plane(points):
    # Разбираем точки на координаты
    x, y, z = np.array(points).T

    # Проверка на количество None в z
    if list(z).count(None) > 1:
        return None  # Если более одного значения None в z, возвращаем None

    # Если есть одно значение None в z, используем только 3 точки для нахождения плоскости
    if list(z).count(None) == 1:
        # Найдем индекс точки с None
        none_index = list(z).index(None)
        # Убираем точку с None
        valid_points = [points[i] for i in range(len(points)) if z[i] is not None]

        return best_fit_plane_three_points(valid_points)  # Используем метод для 3 точек

    # Составляем матрицу M и вектор d для 4 точек
    M = np.c_[x, y, np.ones(len(points))]  # добавляем столбец из 1 для D

    # Решаем систему M @ [A, B, D] = -z методом наименьших квадратов
    ABCD, _, _, _ = np.linalg.lstsq(M, -z, rcond=None)

    # Коэффициенты плоскости
    A, B, D = ABCD
    C = 1  # Нормируем на C = 1, так как уравнение Ax + By + Cz + D = 0

    return A, B, C, D


def line_plane_intersection(plane, line_point, line_dir):
    A, B, C, D = plane
    x0, y0, z0 = line_point
    dx, dy, dz = line_dir

    denom = A * dx + B * dy + C * dz
    if abs(denom) < 1e-10:
        return None  # Прямая параллельна плоскости или лежит в ней

    t = -(A * x0 + B * y0 + C * z0 + D) / denom
    intersection = (x0 + t * dx, y0 + t * dy, z0 + t * dz)
    return intersection


def line_from_two_points(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    direction = (x2 - x1, y2 - y1, z2 - z1)
    return p1, direction



# # Пример: 4 произвольные точки
# points = [
#     (1, 2, 3),
#     (4, 5, 6),
#     (7, 8, 9),
#     (2, 3, 5)
# ]
#
# A, B, C, D = best_fit_plane(points)
# # print(f"Уравнение плоскости: {A:.3f}x + {B:.3f}y + {C:.3f}z + {D:.3f} = 0")
#
# # Пример: строим прямую через A(0, 0, 0) и B(2, -2, 2)
# line_point, line_dir = line_from_two_points((0, 0, 0), (2, -2, 2))
#
# intersection = line_plane_intersection((A, B, C, D), line_point, line_dir)
# # if intersection:
# #     print(f"Точка пересечения: {intersection}")
# # else:
# #     print("Прямая параллельна плоскости или лежит в ней")