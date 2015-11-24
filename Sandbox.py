__author__ = 'Jonathan Spitz'

import numpy as np
import matplotlib.pyplot as plt
import copy
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


def get_front(t_points):
    # Receives a list of tagged points and returns the non-dominated tags
    f_points = copy.copy(t_points)  # create a copy of the data
    cur_point_a = 0
    while True:
        cur_point_b = 0

        while True:
            if cur_point_b == cur_point_a:
                cur_point_b += 1
            if cur_point_b >= len(f_points):
                # Reached the end of the list
                cur_point_a += 1
                break

            # print cur_point_a, cur_point_b
            res = dominates(f_points[cur_point_a][1], f_points[cur_point_b][1])

            if res == 1:
                # Point A dominates point B, remove point B
                f_points.pop(cur_point_b)
            elif res == -1:
                # Point B dominates point A, remove point A
                f_points.pop(cur_point_a)
                break
            else:
                cur_point_b += 1

            if cur_point_a >= len(f_points):
                # Reached the end of the list
                break

        if cur_point_a >= len(f_points):
            # Reached the end of the list
            break

    return [f_points[tid][0] for tid in range(len(f_points))]


def pareto(points):
    # Add an ID tag to the points
    t_points = [[tag, points[tag]] for tag in range(len(points))]

    fronts = []
    while len(t_points) > 0:
        # Get the outer-most Pareto front
        front_ids = get_front(t_points)
        front_ids.sort()
        fronts.append(front_ids)
        print(fronts)

        # Take out the front's points
        j = 0
        k = 0
        while True:
            try:
                if t_points[j][0] == fronts[-1][k]:
                    t_points.pop(j)
                    k += 1
                    if k >= len(fronts[-1]):
                        break
                else:
                    j += 1
                if j >= len(t_points):
                    break
            except:
                print "Shit!"
    return fronts


# Generate random points on concentric layers
R = [0.1*(i+5) for i in range(5)]
N = 20
x = []
y = []
xy_points = []
for r in R:
    for phi in np.random.rand(N)*0.5*np.pi:
        x.append(r*np.cos(phi))
        y.append(r*np.sin(phi))
        xy_points.append([x[-1], y[-1]])
plt.scatter(x, y, 100, [0, 0, 0])

# # Generate simple points
# x = [1, 1, 2, 3, 5, 5, 6, 7, 7, 9]
# y = [9, 3, 4, 7, 3, 2, 5, 4, 1, 4]
# xy_points = [[xp, yp] for xp, yp in zip(x, y)]
#
# plt.scatter(x, y, 100, [0, 0, 0])
# # plt.show()

p_fronts = pareto(xy_points)
colors = [[1, 0, 0], [0.2, 0.7, 0.2], [0, 0, 1], [0.5, 0.5, 0.5], [1, 0, 1], [0.2, 0.6, 0.6], [1, 1, 0]]
for i in range(len(p_fronts)):
    front = p_fronts[i]
    front_x = [xy_points[f][0] for f in front]
    front_y = [xy_points[f][1] for f in front]
    plt.scatter(front_x, front_y, 50, colors[i])
plt.show()