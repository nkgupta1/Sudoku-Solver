"""+================================+
   |    Nikhil Gupta                |
   |    Graphics Demo               |
   |    Start: 10/23/13             |
   |    End:   11/15/13             |
   =================================="""

#---------------------------------------------------------------------------
class Cell(object):
    matrix = None
#---------------------------------------------------------------------------
    def __init__(self, val, r, c, matrix):
        if val == 0:
            self.value = set(range(1,MAX+1))
        else:
            self.value = {val,}
        self.row     = r
        self.col     = c
        self.block   = self.blockNumber(r, c)
        Cell.matrix  = matrix
#---------------------------------------------------------------------------
    def __repr__(self):
        if len(self.value) == 1:
            element = str(list(self.value)[0])
        else:
            element = ' '
        return element
#---------------------------------------------------------------------------
    def print(matrix, details = False):     #for DEGUGGING
        print('+---' * MAX + '+')
        for r in range(MAX):
            for c in range(MAX):
                if len(Cell.matrix[r][c].value) == 1:
                    elt = list(Cell.matrix[r][c].value)[0]
                    print('| ',elt, ' ', end = '', sep = '')
                else: print ('|   ', end = '', sep = '')
            print('|')
            print('+---' * MAX + '+')
        print()
        if details == True:
            for f in range(MAX):
                for c in range(MAX):
                    print('matrix[', r, '][', c, '].value =', matrix[r][c].value, sep ='')
                print()
#---------------------------------------------------------------------------
    def blockNumber(self, row, col):
        if      (self.row < 3) and     (self.col < 3): return 0     #Upper  Left Corner
        if      (self.row < 3) and (2 < self.col < 6): return 1     #Middle Top
        if      (self.row < 3) and (5 < self.col):     return 2     #Upper  Right Corner
        if  (2 < self.row < 6) and     (self.col < 3): return 3     #Middle Left Block
        if  (2 < self.row < 6) and (2 < self.col < 6): return 4
        if  (2 < self.row < 6) and (5 < self.col):     return 5
        if      (self.row > 5) and     (self.col < 3): return 6
        if      (self.row > 5) and (2 < self.col < 6): return 7
        if      (self.row > 5) and (5 < self.col):     return 8
#---------------------------------------------------------------------------
    def reduceCellCandidatesByRow(self):
        for r in range(MAX):
            if r != self.row and len(Cell.matrix[r][self.col].value) == 1:
                self.value     -=    Cell.matrix[r][self.col].value
#---------------------------------------------------------------------------
    def reduceCellCandidatesByCol(self):
        for c in range(MAX):
            if c != self.col and len(Cell.matrix[self.row][c].value) == 1:
                self.value     -=    Cell.matrix[self.row][c].value
#---------------------------------------------------------------------------
    def reduceCellDandidatesByBlock(self):
        for r in range(MAX):
            for c in range(MAX):
                if (Cell.matrix[r][c].block == self.block) \
                   and (r != self.row or c != self.col) and len(Cell.matrix[r][c].value) == 1:
                       self.value               -=              Cell.matrix[r][c].value
#---------------------------------------------------------------------------
    def updateCellBasedOnCandidateValuesInItsRowColAndBlock(self):
        rowCandidates = []
        colCandidates = []
        blkCandidates = []

        for c in range(MAX):
            if c != self.col:
                rowCandidates += Cell.matrix[self.row][c].value

        for r in range(MAX):
            if r != self.row:
                colCandidates += Cell.matrix[r][self.col].value

        for r in range(MAX):
            for c in range(MAX):
                if r != self.row or c != self.col:
                    if Cell.matrix[r][c].block == self.block:
                        blkCandidates += Cell.matrix[r][c].value

        for num in self.value:
            if (num not in rowCandidates) or (num not in colCandidates) or (num not in blkCandidates):
                self.value = {num,}
#---------------------------------------------------------------------------
    def TryToReduceCandidateValuesInCell(self):
        oldValue = deepcopy(self.value)

        if len(self.value) == 1:
            return False

        self.reduceCellCandidatesByRow  ()
        self.reduceCellCandidatesByCol  ()
        self.reduceCellDandidatesByBlock()

        self.updateCellBasedOnCandidateValuesInItsRowColAndBlock()

        return self.value != oldValue
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
def setUpCanvas(root):
    root.title("SUDOKU: A Tk/Python Graphics Program by Nikhil Gupta")
    canvas = Canvas(root, width = 1290, height = 710, bg = 'black')
    canvas.pack(expand = YES, fill = BOTH)
    return canvas
#---------------------------------------------------------------------------
def displayTheSudokuBoard(matrix):
    canvas.delete('all')
    canvas.create_rectangle(0, 0, 1370, 710, fill = 'black')

    canvas.create_rectangle(375, 170, 735, 560, width = 4, outline = 'RED', fill = 'BLUE')

    kolor = 'RED'
    for hor in range(MAX):
        if hor % 3 == 0:
            canvas.create_line(375 + 40*hor,170,375 + 40*hor,560, width = 8, fill = kolor)
        else:
            canvas.create_line(375 + 40*hor,170,375 + 40*hor,560, width = 2, fill = kolor)
    for vert in range(MAX):
        if vert % 3 == 0:
            canvas.create_line(375,170 + 43.333*vert,735,170 + 43.333*vert, width = 8, fill = kolor)
        else:
            canvas.create_line(375,170 + 43.333*vert,735,170 + 43.333*vert, width = 2, fill = kolor)

    for r in range(MAX):
        for c in range(MAX):
            if len(matrix[r][c].value) != 1:
                ch = ' '
            else:
                ch = list(matrix[r][c].value)[0]
            canvas.create_text(c*40 + 395, r*42+200, text = ch, fill = 'YELLOW', font = ('Helvetica',20,'bold'))
#---------------------------------------------------------------------------
def createTheSudokuBoard():
    V = [ [0,0,1,0,0,9,0,0,0,],
          [0,0,7,8,0,6,0,4,0,],
          [0,0,0,0,4,3,0,0,0,],
          [0,4,0,1,0,0,0,6,0,],
          [0,7,6,0,0,0,2,5,0,],
          [0,1,0,0,0,2,0,3,0,],
          [0,0,0,2,7,0,0,0,0,],
          [0,5,0,3,0,1,9,0,0,],
          [0,0,0,6,0,0,3,0,0,],] 

    #put in valid starting board in C
    C = [ [0,0,0,0,0,0,0,0,0,],
          [0,0,0,0,0,0,0,0,0,],
          [0,0,0,0,0,0,0,0,0,],
          [0,0,0,0,0,0,0,0,0,],
          [2,0,0,0,0,0,0,0,0,],
          [3,0,0,0,0,0,0,0,0,],
          [0,0,0,3,0,1,0,2,0,],
          [0,0,0,0,2,0,3,0,1,],
          [0,0,0,0,0,0,0,0,0,],] 

    matrix = []

    for r in range(MAX):
        row = []
        for c in range(MAX):
            row.append(Cell(C[r][c],r,c, matrix))
        matrix.append(row)
    return matrix
#---------------------------------------------------------------------------
def badMatrix(matrix):
    for r in range(MAX):
        for c in range(MAX):
            if matrix[r][c].value == set():
                return True
    return False
#---------------------------------------------------------------------------
def solutionIsCorrect(matrix):
    rows = [[],[],[], [],[],[], [],[],[]]
    cols = [[],[],[], [],[],[], [],[],[]]
    blks = [[],[],[], [],[],[], [],[],[]]

    for r in range(MAX):
        for c in range(MAX):
            rows[r].append(matrix[r][c].value)

    for r in range(MAX):
        for c in range(MAX):
            cols[c].append(matrix[r][c].value)

    for r in range(MAX):
        for c in range(MAX):
            blks[matrix[r][c].block].append(matrix[r][c].value)

    for elt in rows:
        for x in range(1, MAX + 1):
            if {x} not in elt: return False

    for elt in cols:
        for x in range(1, MAX + 1):
            if {x} not in elt: return False

    for elt in blks:
        for x in range(1, MAX + 1):
            if {x} not in elt: return False

    return True

    
#---------------------------------------------------------------------------
def printVerification(matrix):
    if solutionIsCorrect(matrix):
        canvas.create_text(700, 600, text = "This Sudoku is correct.", fill = 'WHITE', font = ('Helvetica', 70, 'bold'))
    else:
        canvas.create_text(565, 600, text = "WRONG!", fill = 'RED', font = ('Helvetica', 70, 'bold'))
#---------------------------------------------------------------------------
def makeAllPossibleChangesToMatrix(matrix):
    state = True
    while state:
        state = False
        for r in range(MAX):
            for c in range(MAX):
                if matrix[r][c].TryToReduceCandidateValuesInCell():
                    state = True
#---------------------------------------------------------------------------
def restoreValues(matrix, oldMatrix):
    for r in range(MAX):
        for c in range(MAX):
            matrix[r][c].value = deepcopy(oldMatrix[r][c].value)
    return matrix
#---------------------------------------------------------------------------
def coordinatesofCellWithSmallestValueSet(matrix):
    big     = 10
    sml     = 2
    bestRow = -1
    bestCol = -1
    for r in range(MAX):
        for c in range(MAX):
            length = len(matrix[r][c].value)
            if sml <= length < big:
                big = length
                bestRow = r
                bestCol = c
    return (bestRow, bestCol) 
#---------------------------------------------------------------------------
def solveTheSudoku(matrix):
    makeAllPossibleChangesToMatrix(matrix)
    if solutionIsCorrect(matrix) or badMatrix(matrix):
        return matrix
    oldMatrix = deepcopy(matrix)

    (bestRow,bestCol) = coordinatesofCellWithSmallestValueSet(matrix)
    candidates = list(matrix[bestRow][bestCol].value)
    for number in candidates:
        matrix[bestRow][bestCol].value = {number,}
        matrix = solveTheSudoku(matrix)
        if solutionIsCorrect(matrix):
            return matrix
        matrix = restoreValues(matrix, oldMatrix)
    return matrix
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
from tkinter import Tk, Canvas, YES, BOTH
from time    import clock, sleep
from copy    import deepcopy
root       = Tk()
canvas     = setUpCanvas(root)
MAX        = 9
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
def main():
    matrix = createTheSudokuBoard()
    matrix = solveTheSudoku(matrix)
    displayTheSudokuBoard(matrix)
    printVerification(matrix)
    printElapsedTime()
    root.mainloop()
#---------------------------------------------------------------------------
def printElapsedTime():
    print('\n---Total run time =', round(clock() - startTime, 2), 'seconds.')
#---------------------------------------------------------------------------
if __name__ == '__main__':startTime = clock(); main()
