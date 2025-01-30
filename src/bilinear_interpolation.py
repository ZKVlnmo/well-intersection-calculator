import math
def bilinear_interpolation_4terms(x, y, x1, y1, x4, y4, z):
    """
    Выполняет билинейную интерполяцию для заданной точки (x, y) внутри прямоугольной области,
    используя значения функции в 4 угловых точках, хранящиеся в массиве z.

    Параметры:
    - x, y: координаты точки, для которой нужно вычислить значение функции
    - x1, y1: координаты первой точки (нижний левый угол)
    - x4, y4: координаты второй точки (верхний правый угол)
    - z: массив значений функции в 4 угловых точках [f11, f12, f21, f22]

    Возвращает:
    - Интерполированное значение функции в точке (x, y)
    """
    f11, f12, f21, f22 = z

    if x4-x1 != 0 and y4-y1 != 0:
        term1 = f11 * (x4 - x) * (y4 - y) / ((x4 - x1) * (y4 - y1))
        term2 = f12 * (x4 - x) * (y - y1) / ((x4 - x1) * (y4 - y1))
        term3 = f21 * (x - x1) * (y4 - y) / ((x4 - x1) * (y4 - y1))
        term4 = f22 * (x - x1) * (y - y1) / ((x4 - x1) * (y4 - y1))
        return term1 + term2 + term3 + term4
    else:
        return None

def bilinear_interpolation_4terms_with_angle(angle_rad, x, y,x1,y1,x2,y2,x3,y3,x4,y4, z):

    x0 = (x1+x2+x3+x4)/4
    y0 = (y1+y2+y3+y4)/4
    cos = math.cos(angle_rad)
    sin = math.sin(angle_rad)
    x1_new = (x1 - x0) * cos - (y1 - y0) * sin + x0
    y1_new = (x1 - x0) * sin + (y1 - y0) * cos + y0
    x4_new = (x4 - x0) * cos - (y4 - y0) * sin + x0
    y4_new = (x4 - x0) * sin + (y4 - y0) * cos + y0
    x_new = (x - x0) * cos - (y - y0) * sin + x0
    y_new = (x - x0) * sin + (y - y0) * cos + y0


    return bilinear_interpolation_4terms(x_new, y_new, x1_new, y1_new, x4_new, y4_new, z)

