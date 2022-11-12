import util 
from util import Belief, pdf 
from engine.const import Const
import random
import math

# Class: Estimator
#----------------------
# Maintain and update a belief distribution over the probability of a car being in a tile.
class Estimator(object):
    def __init__(self, numRows: int, numCols: int):
        self.belief = util.Belief(numRows, numCols) 
        self.transProb = util.loadTransProb()
        self._time = 1
            
    ##################################################################################
    # [ Estimation Problem ]
    # Function: estimate (update the belief about a StdCar based on its observedDist)
    # ----------------------
    # Takes |self.belief| -- an object of class Belief, defined in util.py --
    # and updates it *inplace* based onthe distance observation and your current position.
    #
    # - posX: x location of AutoCar 
    # - posY: y location of AutoCar 
    # - observedDist: current observed distance of the StdCar 
    # - isParked: indicates whether the StdCar is parked or moving. 
    #             If True then the StdCar remains parked at its initial position forever.
    # 
    # Notes:
    # - Carefully understand and make use of the utilities provided in util.py !
    # - Remember that although we have a grid environment but \
    #   the given AutoCar position (posX, posY) is absolute (pixel location in simulator window).
    #   You might need to map these positions to the nearest grid cell. See util.py for relevant methods.
    # - Use util.pdf to get the probability density corresponding to the observedDist.
    # - Note that the probability density need not lie in [0, 1] but that's fine, 
    #   you can use it as probability for this part without harm :)
    # - Do normalize self.belief after updating !!

    ###################################################################################
    def estimate(self, posX: float, posY: float, observedDist: float, isParked: bool) -> None:
        # BEGIN_YOUR_CODE
        numRows = self.belief.getNumRows()
        numCols = self.belief.getNumCols()
        sd = Const.SONAR_STD
        d = sd
        self._time += 1
        for i in range(numRows):
            for j in range(numCols):
                gridX = util.colToX(j)
                gridY = util.rowToY(i)
                # approach 1
                # if((observedDist*(1-d))**2 <= abs(posX-gridX)**2 + abs(posY-gridY)**2 <= (observedDist*(1+d))**2):
                #     self.belief.setProb(i,j,1000000)
                # else:
                #     self.belief.setProb(i,j,0.00000001)
                # approach 2
                self.belief.setProb(i,j,util.pdf(observedDist,d,math.sqrt(abs(posX-gridX)**2 + abs(posY-gridY)**2)))
        self.belief.normalize()
        # END_YOUR_CODE
        return
  
    def getBelief(self) -> Belief:
        return self.belief