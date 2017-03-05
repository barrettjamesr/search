import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if currentNumberOfAttacks <= newNumberOfAttacks:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        
        minNumOfAttack = self.getNumberOfAttacks()
        newBoard = self
        newCol, newRow = 0, 0

        for curCol in range(len(newBoard.squareArray)):
            queenRow = [row[curCol] for row in newBoard.squareArray].index(1)
            for curRow in range(len(newBoard.squareArray)):
                if (curCol != curRow) and (curCol != len(newBoard.squareArray) - 1 - curRow) and (len(newBoard.squareArray) - 1 - curCol != curRow):
                    #make previous queen empty
                    newBoard.squareArray[[row[curCol] for row in newBoard.squareArray].index(1)][curCol] = 0
                    newBoard.squareArray[curRow][curCol] = 1

                    if newBoard.getNumberOfAttacks() < minNumOfAttack:
                        newCol = curCol
                        newRow = curRow
                        minNumOfAttack = newBoard.getNumberOfAttacks()

            newBoard.squareArray[[row[curCol] for row in newBoard.squareArray].index(1)][curCol] = 0
            newBoard.squareArray[queenRow][curCol] = 1

        newBoard.squareArray[[row[newCol] for row in newBoard.squareArray].index(1)][newCol] = 0
        newBoard.squareArray[newRow][newCol] = 1

        return (newBoard, minNumOfAttack, newRow, newCol)
        util.raiseNotDefined()

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        numAttacks = 0

        rowTotals = [ sum(row) for row in self.squareArray ]
        colTotals = [ sum(col) for col in zip(*self.squareArray) ]

        for total in rowTotals:
            numAttacks += (total*(total-1))/2
        for total in colTotals:
            numAttacks += (total*(total-1))/2

        #each square in the board has potentially diagonals, leftdown, leftup, rightdown, right up
        #this loop uses the top row and bottom row as starting points to calculate the sum of each diagonal
        #don't need to check the final col because that would duplicate
        for col in range(len(self.squareArray)-1) :
            leftDown = 0
            offset = 0
            while col - offset >= 0:
                leftDown += self.squareArray[offset][col-offset]
                offset+=1
            numAttacks += (leftDown*(leftDown-1))/2

            leftUp = 0
            offset = 0
            while col - offset >= 0:
                leftUp += self.squareArray[len(self.squareArray)-1-offset][col-offset]
                offset+=1
            numAttacks += (leftUp*(leftUp-1))/2

            rightDown = 0
            offset = 0
            while col + offset  < len(self.squareArray):
                rightDown += self.squareArray[offset][col+offset]
                offset+=1
            numAttacks += (rightDown*(rightDown-1))/2

            rightUp = 0
            offset = 0
            while col + offset < len(self.squareArray):
                rightUp += self.squareArray[len(self.squareArray)-1-offset][col+offset]
                offset+=1
            numAttacks += (rightUp*(rightUp-1))/2

        return int(numAttacks)
        util.raiseNotDefined()

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
