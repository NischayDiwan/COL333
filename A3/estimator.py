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
        self._numParticles = 500
        self._particles = [None]*self._numParticles
        self._tMap = {}
            
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
    def __sens_model(self,sr,sc,e,posX,posY,sd):
        spX = util.colToX(sc)
        spY = util.rowToY(sr)
        actual_dist = math.sqrt(abs(posX-spX)**2 + abs(posY-spY)**2)
        p = util.pdf(actual_dist,sd,e)
        return p
    def __state_tran(self,sr,sc,tP,numRows,numCols): 
        flattr = tP[(sr,sc)]
        if(flattr[1] == [0]*len(flattr[1])):
            tr,tc = random.randint(0,numRows-1),random.randint(0,numCols-1)
        else:
            tr,tc = random.choices(flattr[0],flattr[1])[0]
        return (tr,tc)
    def estimate(self, posX: float, posY: float, observedDist: float, isParked: bool) -> None:
        # BEGIN_YOUR_CODE
        t = self._time
        numRows = self.belief.getNumRows()
        numCols = self.belief.getNumCols()
        sd = Const.SONAR_STD
        N = self._numParticles
        prcls = self._particles
        wts = [0]*N
        e = observedDist
        tP = self._tMap
        # setup s0
        if(t == 1):
            flatBelief = [[],[]]
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
                    # self.belief.setProb(i,j,util.pdf(observedDist,d,math.sqrt(abs(posX-gridX)**2 + abs(posY-gridY)**2)))
                    # approach 3
                    flatBelief[0].append((i,j))
                    flatBelief[1].append(util.pdf(e,sd,math.sqrt(abs(posX-gridX)**2 + abs(posY-gridY)**2)))
                    self._tMap[(i,j)] = [[],[]]
                    for i1 in range(numRows):
                        for j1 in range(numCols):
                            if(((i,j),(i1,j1)) in self.transProb):
                                self._tMap[(i,j)][0].append((i1,j1))
                                self._tMap[(i,j)][1].append(self.transProb[((i,j),(i1,j1))])
            # print(self._tMap)
            for k in range(N):
                prcls[k] = random.choices(flatBelief[0],flatBelief[1])[0]
            # print(prcls)
        # step 1
        else:
            for k in range(N):
                prcls[k] = self.__state_tran(prcls[k][0],prcls[k][1],tP,numRows,numCols)
        # step 2
        for k in range(k):
            wts[k] = self.__sens_model(prcls[k][0],prcls[k][1],e,posX,posY,sd)
        # step 3
        prcls1 = prcls.copy()
        for k in range(N):
            prcls[k] = random.choices(prcls1,wts)[0]
        # inferencing from the particles
        for k in range(N):
            self.belief.addProb(prcls[k][0],prcls[k][1],10000)
        self._time += 1
        self._particles = prcls
        self.belief.normalize()
        # END_YOUR_CODE
        return
  
    def getBelief(self) -> Belief:
        return self.belief