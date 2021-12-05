from dataclasses import dataclass, field
from math import ceil, sqrt, floor

import numpy as np
import matplotlib.pyplot as plt


@dataclass
class Point:
    x: int
    y: int
    poid: int

    def __key(self):
        return (self.x, self.y, self.poid)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.__key() == other.__key()
        return NotImplemented

    def distance_origin(self) -> int:
        return sqrt(self.x ** 2 + self.y ** 2)

    def distance_point(self, point) -> int:
        return sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)


@dataclass
class Grid:
    nbr: int
    size: int
    points: list[Point] = field(init=False)
    poid_min: int = 2
    poid_max: int = 10
    #greedy: dict = {}

    def __post_init__(self) -> None:
        self.points = [None] * self.nbr
        coordinates = [None] * self.nbr
        [x, y] = [
            np.random.randint(low=-floor(self.size / 2), high=floor(self.size / 2)),
            np.random.randint(low=-floor(self.size / 2), high=floor(self.size / 2)),
        ]
        for i in range(self.nbr):
            while [x, y] in coordinates:
                [x, y] = [
                    np.random.randint(
                        low=-floor(self.size / 2), high=floor(self.size / 2)
                    ),
                    np.random.randint(
                        low=-floor(self.size / 2), high=floor(self.size / 2)
                    ),
                ]
            coordinates[i] = [x, y]
        for i in range(self.nbr):
            self.points[i] = Point(
                coordinates[i][0],
                coordinates[i][1],
                np.random.randint(low=self.poid_min, high=self.poid_max),
            )
        """for point in self.points:
            self.greedy[point] = point.poid / point.distance_origin()"""

    def evaluate_origin(self, current_point = Point(0, 0, 0)) -> dict:
        greedy = {}
        if current_point == Point(0, 0, 0):
            for point in self.points:
                greedy[point] = point.poid / point.distance_origin()
            return greedy
        for point in self.points:
            greedy[point] = point.poid / point.distance_point(current_point)
        return greedy

    def plot(self) -> None:
        ax = plt.subplot(1, 1, 1)
        plt.grid(True)
        plt.xlim(-floor(self.size / 2), floor(self.size / 2))
        plt.ylim(-floor(self.size / 2), floor(self.size / 2))
        for i in self.points:
            ax.plot(i.x, i.y, 'or')


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
