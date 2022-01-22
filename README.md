# Konane
Python method that plays one side of a Konane game. This is written
in Python3. This class is called from a driver program for playing against a human:
konaneman.py. You also have program player.py which plays random konane
moves.
Most of the material you will need has been constructed for you, in the random-move
version. You will need to implement minimax with alpha-beta cutoffs, and a scoring
function.
The skeleton player.py contains:
  A class. The instance variables of the class contain the current board, as well as
the current player (a string ’x’ or ’o’), and the opposing player.
  A method move(). It returns the best move. You will put your minimax, alphabeta
algorithm in move (or you will put it in a method which is called from
move). The sample move() method picks a random move.
  A method gameDone(). It returns true or false if (in your opinion) the game is
done, based on the current board and your own player.
  A sample method simple_score(board) which computes a score for a
board, from the point of view of your player.
