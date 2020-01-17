import os, sys
import time
from copy import deepcopy
from random import randint

def clear():
    '''Clears user's screen'''

    if os.name == "nt": # Windows
        os.system("cls")
    if os.name == "posix": # Linux
        os.system("clear")

class LifeGame:
    def __init__(self, N=30, M=30, file=None, sleepTime=1., starsInsteadOfDigits=True):
        '''
        GAME OF LIFE

        N(int), M(int) - sizes of fild
        file(str) - path to file, if mode is "from file", either - None
        sleepTime(float) - time between two generations
        starsInsteadOfDigits(bool) - if True, prints pretty stars and voids instead of ones and zeros
        _field(list of list of int) - field in this moment

        '''

        if N <= 0 or M <= 0:
            raise Exception("Wrong field size")

        self.N = N
        self.M = M
        self.sleepTime = sleepTime
        self.starsInsteadOfDigits = starsInsteadOfDigits
        self._field = [[0 for j in range(self.M)] for i in range(self.N)]
        if file:
            self.readFromFile(file)
        else:
            self.setRandom()

    def setRandom(self):
        '''Sets the _field to random position'''

        for i in range(self.N):
            for j in range(self.M):
                self._field[i][j] = randint(0, 1)

    def readFromFile(self, filePath=None):
        '''Sets the _field to position from file [filpath]'''

        if not filePath:
            raise Exception("No file given")

        with open(filePath, 'r') as f:
            self.N, self.M = map(int, f.readline().split())
            if self.N <= 0 or self.M <= 0:
                raise Exception("Wrong field size")
            self._field = [[0 for j in range(self.M)] for i in range(self.N)]
            for i in range(self.N):
                self._field[i] = list(map(int, f.readline().strip()))

    def saveToFile(self, filePath=None):
        '''Saves current _field to file [filpath]'''

        if not filePath:
            raise Exception("No file given")

        with open(filePath, 'w') as f:
            print(self.N, self.M, file=f)
            for i in range(self.N):
                print("".join(map(str, self._field[i])), file=f)

    def printField(self):
        '''Clears terminal and prints current _field'''

        clear()
        for i in range(self.N):
            for j in range(self.M):
                if self.starsInsteadOfDigits:
                    print(" " if self._field[i][j] == 0 else "*", end="")
                else:
                    print(self._field[i][j], end="")
            print()

    def countAliveNeighbours(self, currI, currJ):
        '''Counts, how many of cell (currI, currJ) neighbours are alive'''

        aliveNeighbours = 0
        for neighbI in range(currI - 1, currI + 2):
            for neighbJ in range(currJ - 1, currJ + 2):
                if ((currI, currJ) != (neighbI, neighbJ)) and \
                                    0 <= neighbI < self.N and \
                                    0 <= neighbJ < self.M:
                    if (self._field[neighbI][neighbJ]):
                        aliveNeighbours += 1
        return aliveNeighbours

    def oneStep(self):
        '''Updates current _field to a new generation of cells'''

        _newField = [[0 for j in range(self.M)] for i in range(self.N)]
        for i in range(self.N):
            for j in range(self.M):
                aliveNeighbours = self.countAliveNeighbours(i, j)
                if self._field[i][j] == 1:
                    if 2 <= aliveNeighbours <= 3:
                        _newField[i][j] = 1
                else:
                    if aliveNeighbours == 3:
                        _newField[i][j] = 1
        self._field = _newField

    def startLife(self, steps=-1):
        '''Life starts for [steps] steps. If [steps] is -1, simulates life infinitely. Stops by Ctrl-C'''

        try:
            self.printField()
            time.sleep(self.sleepTime)
            if steps == -1:
                while 1:
                    self.oneStep()
                    self.printField()
                    time.sleep(self.sleepTime)
            else:
                for moveNum in range(steps):
                    self.oneStep()
                    self.printField()
                    time.sleep(self.sleepTime)
        except KeyboardInterrupt:
            print("Got Ctrl+C, exiting!")
            return

if __name__ == "__main__":
    print("Choose mode:")
    print("Read field from file: 0")
    print("Generate random field: 1")
    mode = input("Input mode: ")
    if mode == "0":
        file = input("Input file name (or a full path): ")
        game = LifeGame(file=file)
        game.startLife()

    elif mode == "1":
        sizes = input("Input N and M (or press enter to generate random N and M): ")
        if sizes:
            N, M = map(int, sizes.split())
        else:
            N, M = randint(1, 50), randint(1, 50)
        game = LifeGame(N=N, M=M)
        game.startLife()
        
    else:
        print("Wrong mode!")