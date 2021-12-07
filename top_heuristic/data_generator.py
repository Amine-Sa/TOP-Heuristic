from dataclasses import dataclass, field
from math import ceil, sqrt, floor

import numpy as np
import matplotlib.pyplot as plt


@dataclass
class Point:
    x: float
    y: float
    poid: int

    def __key(self):
        return (self.x, self.y, self.poid)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.__key() == other.__key()
        return NotImplemented

    def distance_origin(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def distance_point(self, point) -> float:
        return sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)


@dataclass
class Grid:
    path: str = False
    size: int = 10
    dimension: int = 10
    points: list[Point] = field(init=False)
    poid_min: int = 2
    poid_max: int = 10

    def __post_init__(self) -> None:
        if not (self.path):
            self.points = [None] * self.size
            coordinates = [None] * self.size
            [x, y] = [
                np.random.randint(
                    low=-floor(self.dimension / 2), high=floor(self.dimension / 2)
                ),
                np.random.randint(
                    low=-floor(self.dimension / 2), high=floor(self.dimension / 2)
                ),
            ]
            for i in range(self.size):
                while ([x, y] in coordinates) or ([x, y] == [0, 0]):
                    [x, y] = [
                        np.random.randint(
                            low=-floor(self.dimension / 2),
                            high=floor(self.dimension / 2),
                        ),
                        np.random.randint(
                            low=-floor(self.dimension / 2),
                            high=floor(self.dimension / 2),
                        ),
                    ]
                coordinates[i] = [x, y]
            for i in range(self.size):
                self.points[i] = Point(
                    coordinates[i][0],
                    coordinates[i][1],
                    np.random.randint(low=self.poid_min, high=self.poid_max),
                )
        else:
            data = open(self.path, "r")
            lines = data.readlines()
            _, size = [i.strip() for i in lines[0].split(" ")]
            self.size = int(size)
            self.dimension = 0
            self.points = [None] * self.size
            for i in range(3, len(lines)):
                if self.dimension < max(
                    abs(float(lines[i].split("\t")[0])),
                    abs(float(lines[i].split("\t")[1])),
                ):
                    self.dimension = max(
                        abs(float(lines[i].split("\t")[0])),
                        abs(float(lines[i].split("\t")[1])),
                    )
                self.points[i - 3] = Point(
                    float(lines[i].split("\t")[0]),
                    float(lines[i].split("\t")[1]),
                    int(lines[i].split("\t")[2]),
                )
            self.dimension = ceil(self.dimension)

    def evaluate(self, current_point=Point(0, 0, 0)) -> dict:
        greedy = {}
        if current_point == Point(0, 0, 0):
            for point in self.points:
                greedy[point] = point.poid / point.distance_origin()
            return greedy
        for point in self.points:
            greedy[point] = point.poid / point.distance_point(current_point)
        return greedy

    def plot(self) -> None:
        if not (self.path):
            ax = plt.subplot(1, 1, 1)
            plt.grid(True)
            plt.xlim(-floor(self.dimension / 2) - 1, floor(self.dimension / 2) + 1)
            plt.ylim(-floor(self.dimension / 2) - 1, floor(self.dimension / 2) + 1)
            ax.plot(0, 0, "og")
            for i in self.points:
                ax.plot(i.x, i.y, "or")
        else:
            ax = plt.subplot(1, 1, 1)
            plt.grid(True)
            plt.xlim(0, ceil(self.dimension))
            plt.ylim(0, ceil(self.dimension))
            ax.plot(self.points[0].x, self.points[0].y, "og")
            ax.plot(self.points[-1].x, self.points[-1].y, "og")
            for i in self.points[1:-1]:
                ax.plot(i.x, i.y, "or")


@dataclass
class Solution:
    nb_vehicules: int
    max_distance: int
    max_capacity: int

    def CouldReturn(
        self, current_point, target_point, current_distance, current_capacity
    ) -> bool:
        if (
            current_distance
            + current_point.distance_point(target_point)
            + target_point.distance_origin()
            > self.max_distance
        ):
            return False
        elif current_capacity + target_point.poid > self.max_capacity:
            return False
        else:
            return True
