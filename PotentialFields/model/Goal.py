__author__ = 'lexic92'

import numpy

class Goal():

    def getDistanceTo(self, x, y):
        '''
        Returns the distance from the given coordinates to this goal.
        :param x: x coordinate of object
        :param y: y cooredinate of object
        :return: d (magnitude of the distance from object to this goal)
        '''
        return numpy.sqrt((x - self._x)**2 + (y - self._y)**2)

    def getAngleToGoalFrom(self, x, y):
        return numpy.arctan2(self._y - y, self._x - x)

    def __init__(self, x, y, radius, spread):
        self._x = x # the x-coordinate of the center of the goal object.
        self._y = y # the y-coordinate of the center of the goal object.
        self.radius = radius
        self._spread = spread