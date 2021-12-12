import dataclasses
import matplotlib.pyplot as plt

from top_heuristic.data_generator import Instance


def Solution(Instance: "Instance"):
    Points = Instance.points.copy()
    current_point = dataclasses.replace(Instance.origin)
    vehicule = 1
    Tours = {}
    for i in range(1, Instance.nb_vehicules + 1):
        Tours[i] = []
    current_distance = 0
    current_capacity = 0

    while Points != []:
        Evaluation = {}
        for point in Points:
            Evaluation[point] = point.poid / point.distance_point(current_point)
        list_point = list(
            dict(
                sorted(Evaluation.items(), key=lambda item: item[1], reverse=True)
            ).keys()
        )
        choice = 0
        while True:
            if Instance.CouldReturn(
                current_point, list_point[choice], current_distance, current_capacity
            ):
                Tours[vehicule].append(list_point[choice])
                Points.remove(list_point[choice])
                current_distance += current_point.distance_point(list_point[choice])
                current_capacity += list_point[choice].poid
                current_point = list_point[choice]
                break
            choice += 1
            if choice >= len(Points):
                current_point = dataclasses.replace(Instance.origin)
                current_distance = 0
                current_capacity = 0
                vehicule += 1
                if vehicule > Instance.nb_vehicules:
                    Points = []
                break
    return Tours


def plot_solution(Istance: "Instance", Tours):
    ax = plt.subplot(1, 1, 1)
    plt.grid(True)
    for i in range(1, len(Tours) + 1):
        ax.plot(Istance.origin.x, Istance.origin.y, "or")
        X = [Istance.origin.x]
        Y = [Istance.origin.y]
        for j in Tours[i]:
            X.append(j.x)
            Y.append(j.y)
        X.append(Istance.finish.x)
        Y.append(Istance.finish.y)
        ax.scatter(X, Y)
        ax.plot(X, Y)


def evaluate_solution(Istance: "Instance", Tours):
    total = 0
    traveled = 0
    for i in Istance.points:
        total += i.poid
    for i in range(1, len(Tours) + 1):
        for j in Tours[i]:
            traveled += j.poid
    print(f"{traveled} / {total} = {traveled/total}")
    return traveled * 100 / total
