__author__ = 'lexic92'

import matplotlib.pyplot as plt
import numpy
import math
from PotentialFields.model import Obstacle, Goal, TangentialClockwise, TangentialCounterclockwise

class Combined():
    def sign(self, argument):
        '''
        Returns the sign of the argument. Intended for use in multiplication (because you can
        just multiply by a positive or negative 1). This "function" is defined in the repulsive field
        formulas on the Potential Fields PDF on Learning Suite Content Tab.
        :param argument: the number you want the sign of.
        :return: 1 if it's positive, -1 if it's negative.
        '''
        if argument >= 0:
            return 1
        elif argument < 0:
            return -1
        else:
            raise AssertionError()

    def _generateAttractiveAndRepulsiveFieldGraph(self):
        # CODE FROM WALTER'S EXAMPLE IN SIMPLE.PY (UNMODIFIED, except for some parameters Ben might have modified)
        fig = plt.figure()
        ax = fig.add_subplot(111)

        #generate grid
        x = numpy.linspace(-2, 2, 24)
        y = numpy.linspace(-1.5, 1.5, 24)
        x, y = numpy.meshgrid(x, y)


        #--------------------------MY CODE----------------------------
        #To fix a bug (See http://stackoverflow.com/questions/13730468/from-2d-to-1d-arrays)
        x = numpy.reshape(x, (1,numpy.product(x.shape)))[0]
        y = numpy.reshape(y, (1,numpy.product(y.shape)))[0]

        #initialize vectors (actually just lists)
        vx = []
        vy = []

        #Loop from 0 to x.length-1, therefore running x.length times:
        # (ASSUMING THAT x AND y VECTORS HAVE THE SAME NUMBER OF ITEMS (THEY SHOULD))
        for i in range(0, x.size):
            sum_vx = 0 #Add all of the attractive AND repulsive fields and sum them up for each given position
            sum_vy = 0 #Add all of the attractive AND repulsive fields and sum them up for each given position

            #--------------- ONLY CHANGE FROM REPULSIVEFIELDS.PY: ADD THIS TO THE SUMMATION ---------
            for goal in self._goals:
                #calculate distance to goal
                d = goal.getDistanceTo(x[i], y[i])
                r = goal._radius
                s = goal._spread
                theta = goal.getAngleToGoalFrom(x[i], y[i])

                #FOLLOWING FORMULA FROM Potential Fields PDF ON LEARNING SUITE CONTENT TAB
                if d < r:
                    sum_vx += 0
                    sum_vy += 0
                elif d <= (r + s):
                    sum_vx += (goal._alpha*(d - r)*math.cos(theta))
                    sum_vy += (goal._alpha*(d - r)*math.sin(theta))
                elif d > (r + s):
                    sum_vx += (goal._alpha*s*math.cos(theta))
                    sum_vy += (goal._alpha*s*math.sin(theta))

            #theta - 90
            for tangential in self._tangentialsClockwise:
                # calculate distance to obstacle
                d = tangential.getDistanceTo(x[i], y[i])
                r = tangential._radius
                s = tangential._spread
                theta = tangential.getAngleToObstacleFrom(x[i], y[i]) - 90.0

                # FOLLOWING FORMULA FROM Potential Fields PDF ON LEARNING SUITE CONTENT TAB
                if d < r:
                    sum_vx += (-self.sign(math.cos(theta))*float('inf'))
                    sum_vy += (-self.sign(math.sin(theta))*float('inf'))
                elif d <= (r + s):
                    sum_vx += (-tangential._beta)*(s + r - d)*math.cos(theta)
                    sum_vy += (-tangential._beta)*(s + r - d)*math.sin(theta)
                elif d > (r + s):
                    sum_vx += 0
                    sum_vy += 0

            #theta + 90
            for tangential in self._tangentialsCounterclockwise:
                # calculate distance to obstacle
                d = tangential.getDistanceTo(x[i], y[i])
                r = tangential._radius
                s = tangential._spread
                theta = tangential.getAngleToObstacleFrom(x[i], y[i]) + 90.0

                # FOLLOWING FORMULA FROM Potential Fields PDF ON LEARNING SUITE CONTENT TAB
                if d < r:
                    sum_vx += (-self.sign(math.cos(theta))*float('inf'))
                    sum_vy += (-self.sign(math.sin(theta))*float('inf'))
                elif d <= (r + s):
                    sum_vx += (-tangential._beta)*(s + r - d)*math.cos(theta)
                    sum_vy += (-tangential._beta)*(s + r - d)*math.sin(theta)
                elif d > (r + s):
                    sum_vx += 0
                    sum_vy += 0
            #---------------------------------------------------------------------------------------

            for obstacle in self._obstacles:
                #calculate distance to obstacle
                d = obstacle.getDistanceTo(x[i], y[i])
                r = obstacle._radius
                s = obstacle._spread
                theta = obstacle.getAngleToObstacleFrom(x[i], y[i])

                #FOLLOWING FORMULA FROM Potential Fields PDF ON LEARNING SUITE CONTENT TAB
                if d < r:
                    sum_vx += (-self.sign(math.cos(theta))*float('inf'))
                    sum_vy += (-self.sign(math.sin(theta))*float('inf'))
                elif d <= (r + s):
                    sum_vx += (-obstacle._beta)*(s + r - d)*math.cos(theta)
                    sum_vy += (-obstacle._beta)*(s + r - d)*math.sin(theta)
                elif d > (r + s):
                    sum_vx += 0
                    sum_vy += 0
                    
            vx.append(sum_vx)
            vy.append(sum_vy)
        #------------------------------------------------------------

        # CODE FROM WALTER'S EXAMPLE IN SIMPLE.PY (UNMODIFIED, except for the filename it is saved as.)
        ax.quiver(x, y ,vx, vy, pivot='middle', color='r', headwidth=4, headlength=6)
        ax.set_xlabel('$x$') # $ cosmetically changes how the x looks
        ax.set_ylabel('$y$')
        ax.axis('image')
        plt.savefig(self._FILE_NAME)
        plt.show()

    #--------------------------MY CODE----------------------------
    def __init__(self, goals, obstacles, tangentialsClockwise, tangentialsCounterclockwise):
        #Initialize variables first!
        self._FILE_NAME = 'combined.png' #File name to save the figure as.
        self._goals = goals #List of "Goal" objects to make an attractive field of.
        self._obstacles = obstacles #List of "Obstacle" objects to make a repulsive field of.
        self._tangentialsClockwise = tangentialsClockwise #List of "TangentialClockwise" objects to make a tangential field of.
        self._tangentialsCounterclockwise = tangentialsCounterclockwise #List of "TangentialCounterclockwise" objects to make a tangential field of.

        self._alpha = 1 #For scaling the vx and vy values for attractive fields.
        self._beta = 1 #For scaling the vx and vy values for repulsive fields.
        self._tbeta = 3 # for scaling tangential fields.

        #do stuff
        self._generateAttractiveAndRepulsiveFieldGraph()
    #------------------------------------------------------------


if __name__ == "__main__":
    #TEST CASE runs when this file is run individually.
    goals = []
    goals.append(Goal.Goal(0, 0, 1, 2))

    obstacles = []
    obstacles.append(Obstacle.Obstacle(2, 1.5, 1, 2))

    tangentialsClockwise = []
    tangentialsClockwise.append(TangentialClockwise.TangentialClockwise(-1, 1, .2, 2, 1))

    tangentialsCounterclockwise = []
    tangentialsCounterclockwise.append(TangentialCounterclockwise.TangentialCounterclockwise(1, -1, .2, 2, 1))


    Combined(goals, obstacles, tangentialsClockwise, tangentialsCounterclockwise)