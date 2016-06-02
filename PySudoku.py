import sys, os, random, pygame
sys.path.append(os.path.join("objects"))
import SudokuSquare
import SudokuGrid
from GameResources import *

def getSudoku(puzzleNumber=None):
    """This function defines the solution and the inital view.
    Returns two lists of lists, inital first then solution."""
    inital = SudokuGrid.SudokuGrid()
    current = SudokuGrid.SudokuGrid()
    solution = SudokuGrid.SudokuGrid()
    
    inital.createGrid(27, puzzleNumber)
    current.createGrid(27, puzzleNumber)
    solution.createGrid(81, puzzleNumber)

    return inital, current, solution
    
    # Old Version
    # ===========
    # theFile = open(os.path.join("data", "sudokusample.xml"), "r")
    # theData = theFile.read()
    # theFile.close()
    # 
    # inital = []
    # theLines = theData.split("\n")
    # for line in theLines:
    #   inital.append(line.split())
    # inital.pop()
    # 
    # print inital
    # 
    # solution = inital[:]
    # return inital, solution


def main():
    pygame.init()

    size = width, height = 400, 500
    screen = pygame.display.set_mode(size)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    board, boardRect = load_image("SudokuBg.png")
    boardRect = boardRect.move(10, 80)

    # XUXU load logo image
    logo, logoRect = load_image("PySudoku.png")
    logoRect = logoRect.move(40, 0)

    clock = pygame.time.Clock()

    # The puzzleNumber sets a seed so either generate
    # a random number to fill in here or accept user
    # input for a duplicatable puzzle.
    puzzleNumber = int(random.random() * 20000) + 1
    pygame.display.set_caption("PySudoku  -  Puzzle #" + str(puzzleNumber))    
    inital, current, solution = getSudoku(puzzleNumber)

    theSquares = []
    initXLoc = 10
    initYLoc = 80
    startX, startY, editable, number = 0, 0, "N", 0
    for y in range(9):
        for x in range(9):
            if x in (0, 1, 2):  startX = (x * 41) + (initXLoc + 2)
            if x in (3, 4, 5):  startX = (x * 41) + (initXLoc + 6)
            if x in (6, 7, 8):  startX = (x * 41) + (initXLoc + 10)
            if y in (0, 1, 2):  startY = (y * 41) + (initYLoc + 2)
            if y in (3, 4, 5):  startY = (y * 41) + (initYLoc + 6)
            if y in (6, 7, 8):  startY = (y * 41) + (initYLoc + 10)
            number = inital.getNum(y, x)
            if number != None:
                editable = "N"
            else:
                editable = "Y"
            theSquares.append(SudokuSquare.SudokuSquare(number, startX, startY, editable, x, y))

    currentHighlight = theSquares[0]
    currentHighlight.highlight()

    screen.blit(background, (0, 0))
    screen.blit(board, boardRect)
    # XUXU
    # screen.blit(logo, logoRect)
    pygame.display.flip()

    load_music("PySudokuTheme1.ogg")

    theNumbers = { pygame.K_0 : "0", pygame.K_1 : "1", pygame.K_2 : "2", 
                 pygame.K_3 : "3", pygame.K_4 : "4", pygame.K_5 : "5", 
                 pygame.K_6 : "6", pygame.K_7 : "7", pygame.K_8 : "8", 
                 pygame.K_9 : "9", pygame.K_SPACE : "", pygame.K_BACKSPACE : "",
                 pygame.K_DELETE : "" }

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                for x in theSquares:
                    if x.checkCollide(mousepos):
                        currentHighlight.unhighlight()
                        currentHighlight = x
                        currentHighlight.highlight()
            if event.type == pygame.KEYDOWN and event.key in theNumbers:
                #currentHighlight.change(theNumbers[event.key])
                print "[ %s, %s ]" % currentHighlight.currentLoc()
                xLoc, yLoc = currentHighlight.currentLoc()

                # XUXU
                if current.checkAll (yLoc, xLoc,theNumbers[event.key]):
                    currentHighlight.unhighlight()
                    currentHighlight.highlight_wrong()
                else:
                    currentHighlight.change(theNumbers[event.key])
                    current.setNum(yLoc, xLoc, theNumbers[event.key])

                current.printGrid()

        for num in theSquares:
            num.draw()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
    sys.exit()
