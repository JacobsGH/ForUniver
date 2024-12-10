import numpy as np
import matplotlib.pyplot as plt

# Определяем максимальное количество точек в многоугольнике
MAX_POINTS = 20

# Функция для нахождения x-координаты точки пересечения двух линий
def x_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    num = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    return num / den

# Функция для нахождения y-координаты точки пересечения двух линий
def y_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    num = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    return num / den

# Функция для отсечения всех ребер относительно одного ребра области отсечения
def clip(poly_points, poly_size, x1, y1, x2, y2):
    new_points = np.zeros((MAX_POINTS, 2), dtype=int)
    new_poly_size = 0

    for i in range(poly_size):
        k = (i + 1) % poly_size
        ix, iy = poly_points[i]
        kx, ky = poly_points[k]

        # Определяем положение первой и второй точки относительно линии отсечения
        i_pos = (x2 - x1) * (iy - y1) - (y2 - y1) * (ix - x1)
        k_pos = (x2 - x1) * (ky - y1) - (y2 - y1) * (kx - x1)

        # Случай 1: Оба конца находятся внутри
        if i_pos < 0 and k_pos < 0:
            new_points[new_poly_size] = [kx, ky]
            new_poly_size += 1

        # Случай 2: Только первая точка вне
        elif i_pos >= 0 and k_pos < 0:
            new_points[new_poly_size] = [x_intersect(x1, y1, x2, y2, ix, iy, kx, ky),
                                         y_intersect(x1, y1, x2, y2, ix, iy, kx, ky)]
            new_poly_size += 1
            new_points[new_poly_size] = [kx, ky]
            new_poly_size += 1

        # Случай 3: Только вторая точка вне
        elif i_pos < 0 and k_pos >= 0:
            new_points[new_poly_size] = [x_intersect(x1, y1, x2, y2, ix, iy, kx, ky),
                                         y_intersect(x1, y1, x2, y2, ix, iy, kx, ky)]
            new_poly_size += 1

    clipped_poly_points = np.zeros((new_poly_size, 2), dtype=int)
    for i in range(new_poly_size):
        clipped_poly_points[i] = new_points[i]

    return clipped_poly_points

# Функция для реализации алгоритма Сазерленда–Ходжмана
def suthHodgClip(poly_points, poly_size, clipper_points):
    for i in range(len(clipper_points)):
        k = (i + 1) % len(clipper_points)
        poly_points = clip(poly_points, poly_size, clipper_points[i][0], clipper_points[i][1], clipper_points[k][0], clipper_points[k][1])
        poly_size = len(poly_points)

    return poly_points

def plot_two_graphs(points_before_clip, points_after_clip, clipper_rect):
    title_before = 'График до отсечения'
    title_after = 'График после отсечения'

    # Разделяем списки на координаты x и y
    xs_before, ys_before = zip(*points_before_clip) if points_before_clip.size > 0 else ([], [])
    xs_after, ys_after = zip(*points_after_clip) if points_after_clip.size > 0 else ([], [])

    # Создаем фигуру и оси
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Первый график
    axs[0].plot(xs_before + (xs_before[0],), ys_before + (ys_before[0],), marker='o', linestyle='-', color='b')
    
    # Добавляем прямоугольник отсечения на первый график
    rect_xs = [clipper_rect[0], clipper_rect[0], clipper_rect[2], clipper_rect[2], clipper_rect[0]]
    rect_ys = [clipper_rect[1], clipper_rect[3], clipper_rect[3], clipper_rect[1], clipper_rect[1]]
    
    axs[0].plot(rect_xs, rect_ys, color='r', linestyle='--', label='Прямоугольник отсечения')
    
    axs[0].set_title(title_before)
    axs[0].set_xlabel('X')
    axs[0].set_ylabel('Y')
    axs[0].grid()
    
    # Второй график
    axs[1].plot(xs_after + (xs_after[0],), ys_after + (ys_after[0],), marker='o', linestyle='-', color='r')
    
    # Добавляем прямоугольник отсечения на второй график
    axs[1].plot(rect_xs, rect_ys, color='r', linestyle='--', label='Прямоугольник отсечения')

    axs[1].set_title(title_after)
    axs[1].set_xlabel('X')
    axs[1].set_ylabel('Y')
    axs[1].grid()

    # Показываем графики
    plt.tight_layout()
    plt.show()

# Основной код
if __name__ == "__main__":
    # Определяем вершины многоугольника по часовой стрелке
    poly_points = np.array([[100, 150], [180, 250], [200, 250], [300, 200]])
    
    # Определяем вершины прямоугольника отсечения по часовой стрелке
    clipper_rect = [125, 150, 200, 200]  # xmin,ymin,xmax,ymax

    # Вызываем функцию отсечения и получаем точки отсеченного многоугольника
    clipped_polygon = suthHodgClip(poly_points.copy(), len(poly_points), np.array([clipper_rect[:2], [clipper_rect[0], clipper_rect[3]], clipper_rect[2:], [clipper_rect[2], clipper_rect[1]]]))

    # Строим графики до и после отсечения с прямоугольником отсечения
    plot_two_graphs(poly_points.copy(), clipped_polygon, clipper_rect)