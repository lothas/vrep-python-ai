__author__ = 'Jonathan Spitz'

import numpy as np
from matplotlib.pyplot import plot, draw, show

# def make_plot():
#     plot([1,2,3])
#     show(block=False)
#     print 'continue computation'
#
# print('Do something before plotting.')
# # Now display plot in a window
# make_plot()
#
# answer = raw_input('Back to main and window visible? ')
# if answer == 'y':
#     print('Excellent')
# else:
#     print('Nope')

def dominates(point_a, point_b):
    p_len = len(point_a)
    greater = [a > b for a, b in zip(point_a, point_b)]
    geq = [a >= b for a, b in zip(point_a, point_b)]
    if sum(greater) >= 1 and sum(geq) == p_len:
        # Point A dominates Point B
        return 1
    if sum(geq) == 0:
        # Point B strictly dominates Point A
        return -1
    return 0  # no point dominates

def get_front(points):
    # Add an ID tag to the points
    t_points = [[i, points[i]] for i in range(len(points))]

    cur_point_a = 0
    while True:
        cur_point_b = cur_point_a+1
        while True:
            res = dominates(t_points[cur_point_a][1:], t_points[cur_point_b][1:])
            if res == 1:
                # Point A dominates point B, remove point B
                t_points.pop(cur_point_b)
            elif res == -1:
                # Point B dominates point A, remove point A
                t_points.pop(cur_point_a)
                break
            else:
                cur_point_b += 1
                if cur_point_b == len(t_points):
                    # Reached the end of the list
                    cur_point_a += 1
                    break
        if cur_point_a == len(t_points):
            # Reached the end of the list
            break

    return [t_points[i][0] for i in range(len(t_points))]

