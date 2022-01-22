# One Konane object contains one player's information in a Konane game.
#
#  At initialization, save the initial state of the game, plus
#  some other useful information:
#    board = game board
#    print_board is a function for printing out a board
#    who = the current player 'o' or 'x'
#    other = the other player 'x' or 'o'
#
import random
class Konane:
    def __init__(self, board, who, print_board):
        self.board = board
        self.print_board = print_board
        self.who = who
        self.other = {'x':'o', 'o':'x'}[who]
   
    #  Dummy move command.  It should return a 4-tuple containing
    #  the move that it thinks is best for the 'who' player
    def move(self):
        # For debugging
        print("Score when move is called:" , self.simple_score(self.board))
        # Pick a random move
        mymoves = genmoves(self.board, self.who)
        random.shuffle(mymoves)
        mymove =mymoves[-1].move
        return mymove


    # Simple scoring function
    #
    # Compute the number of moves available for the 'who' player, minus the
    # number of moves available for the 'other' player.
    # Exception: if this position is a win or a loss, return +/- 1000
    #
    def simple_score(self, board):
        return len(genmoves(board, self.who)) - len(genmoves(board, self.other))

    def gameDone(self, mover):
        return gameDone(self.board, mover)


# Useful CS 345 Konane Board Routines
#
# The Genmove routine returns a list of Node objects.
# There may or may not be any Node methods, it is up to you.
#
# The move is the four-number tuple move that resulted in this board.
# 
class Node:
    def __init__(self, b, mover, move):
        self.b = b
        self.mover = mover
        self.move = move # A tuple of from_row, from_col, to_row, to_col


#  gameDone command
#  It will check whether the game is finished for a particular mover and board
#  Returns boolean True if the game is over
#
def gameDone(b, mover):
    global places
    for from_row, from_col in places[mover]:
        if moveable(from_row, from_col, b):
            return None
    return True

#  Generate all possible moves
#  Returns list of Nodes of successor moves.
#
def genmoves(b, mover):
    global places   # Assuming you put this in a global variable
    successors = []

    # For each places that mover can be
    for from_row, from_col in places[mover]:
        if not moveable(from_row, from_col, b): continue
        
        # generate all the destinations the mover can jump to 
        dests = dests_from(from_row, from_col)

        # And make a successor node for valid move
        for to_row, to_col in dests:
            succ = make_succ(b, mover, from_row, from_col, to_row, to_col)
            if succ:
                successors.append(succ)
    return successors

#  List of all possible board positions for each player
#
#  Returns a dictionary.
#   places['x'] = [ (0,0), (0,2), ... (7,6) ] # All of X player's squares
#   places['o'] = [ (0,1), (0,3), ... (7,7) ] # All of O player's squares
#
#  Call this once at the beginning of your program.
#  (So you don't call it repeatedly every time you want to move)
#
def each_players_places():
    global places
    places = {'x':[], 'o':[]}
    for i in range(8):
        for j in range(0,8,2):
            if i%2 == 0:
                places['x'].append((i, j))
                places['o'].append((i, j+1))
            else:
                places['o'].append((i, j))
                places['x'].append((i, j+1))
    return places

# Populate the global variable
places = each_players_places()

# Determine whether a piece is moveable
#
# b is a board (the list of lists)
#
# Returns None if there are no moves available from
#   (from_row, from_col).
#   
def moveable(from_row, from_col, b):
    if b[from_row][from_col] == ' ': return None
    if from_row > 1:
        if (not b[from_row-1][from_col] == ' ') and \
            (b[from_row-2][from_col] == ' '): return 1
    if from_row < 6:
        if (not b[from_row+1][from_col] == ' ') and \
            (b[from_row+2][from_col] == ' '): return 1
    if from_col > 1:
        if (not b[from_row][from_col-1] == ' ') and \
            (b[from_row][from_col-2] == ' '): return 1
    if from_col < 6:
        if (not b[from_row][from_col+1] == ' ') and \
            (b[from_row][from_col+2] == ' '): return 1
    return None


#  Compute the squares being jumped over in a proposed move.
#  Returns two lists:
#    (i,j) tuples of the jumped-over positions.
#    (i,j) tuples of the intermediate landing positions
#
def jumppath(lorow, locol, hirow, hicol):
    if lorow == hirow:
        jump_over = [(hirow, j) for j in range(locol+1, hicol, 2)]
        jump_land = [(hirow, j) for j in range(locol+2, hicol, 2)]
        return (jump_over, jump_land)
    elif locol == hicol:
        jump_over = [(i, hicol) for i in range(lorow+1, hirow, 2)]
        jump_land = [(i, hicol) for i in range(lorow+2, hirow, 2)]
        return (jump_over, jump_land)
    else:
        return (None, None)

# For one starting position, all possible jump destinations
#
# (This is all possible destinations, regardless of whether
#  they are possible jumps in the current game)
#
def dests_from(from_row, from_col):
    dests = []
    for j in range(from_col%2, 8, 2):
        if not j==from_col:
            dests.append((from_row, j))
            
    for i in range(from_row%2, 8, 2):
        if not i==from_row:
            dests.append((i, from_col))
    return dests

# 
# Make successor node. 
#   Input is curent board and the proposed move (from and to), 
#   Output is one of these:
#       The resulting new board, in a Node object (move is valid)
#       None (the move is not possible)
#
def make_succ(b, mover, from_row, from_col, to_row, to_col):
    if not b[to_row][to_col] == ' ': return None

    locol, hicol = min(from_col, to_col), max(from_col, to_col)
    lorow, hirow = min(from_row, to_row), max(from_row, to_row)

    (jump_over, jump_land) = jumppath(lorow, locol, hirow, hicol)
    if not jump_over: return None
    for i,j in jump_over:
        if b[i][j] == ' ': return None
    for i,j in jump_land:
        if not b[i][j] == ' ': return None

    # Build a copy of the board, copying only those rows that are affected.
    newb = b[:]
    for i in range(lorow, hirow+1):
        newb[i] = b[i][:]

    for i,j in jump_over:
        newb[i][j] = ' '
    newb[to_row][to_col] = mover
    newb[from_row][from_col] = ' '
    return Node(newb, mover, (from_row, from_col, to_row, to_col))
    

 
