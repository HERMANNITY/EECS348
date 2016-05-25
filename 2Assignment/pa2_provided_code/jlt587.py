# File: jlt587.py
# Author(s) names AND netid's: Guixing Lin glv321, Junhan Liu jlt587, Sixuan Yu sjy099
# Date: April 22, 2016
# Group work statement: All group members were present and contributing during all work
# on this project.
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *
# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            again = nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)

            
            s = opp.minValuePruned(nb, ply-1, turn, -INFINITY, INFINITY)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move, self.num

    def maxValuePruned(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        alp = alpha
        bet = beta
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            again = nextBoard.makeMove(self, m)
            s = opponent.minValuePruned(nextBoard, ply-1, turn, alp, bet)
            #print "s in maxValuePruned is: " + str(s)
            score = max(score, s)
            if bet < score:
                return score
            alp = max(alp, score)
        return score
    
    def minValuePruned(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        alp = alpha
        bet = beta
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            again = nextBoard.makeMove(self, m)
            s = opponent.maxValuePruned(nextBoard, ply-1, turn, alp, bet)
            #print "s in minValue is: " + str(s)
            score = min(s, score)
            if alp > score:
                return score
            bet = min(bet, score)
        return score

    def minimaxBonus(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            again = nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)

            if again:
                s = self.customMax(nb, ply-1, turn, -INFINITY, INFINITY)#If move m can make it go another step, then call customMax
                                                                        #by maximize the huristic function for next step
            else:
                s = opp.customMin(nb, ply-1, turn, -INFINITY, INFINITY) #Else, call customMin
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move, self.num

    def abPruneBonusMaxValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        alp = alpha
        bet = beta
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            again = nextBoard.makeMove(self, m)
            if again:
                s = self.customMax(nextBoard, ply - 1, turn, alp, bet)  #If move m can make it go another step, then call customMax
                                                                        #by maximize the huristic function for next step
            else:
                s = opponent.customMin(nextBoard, ply-1, turn, alp, bet) # Else, call customMin
            print "s in maxValuePruned is: " + str(s)
            score = max(score, s)
            if bet < score:
                return score
            alp = max(alp, score)
        return score
    
    def abPruneBonusMinValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        alp = alpha
        bet = beta
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            again = nextBoard.makeMove(self, m)
            if again:
                s = self.customMin(nextBoard, ply - 1, turn, alp, bet)  #If move m can make it go another step, then call customMin
                                                                        #by minimize the huristic function for next step
            else:
                s = opponent.customMax(nextBoard, ply-1, turn, alp, bet) # Else, call customMax
            #print "s in minValue is: " + str(s)
            score = min(s, score)
            if alp > score:
                return score
            bet = min(bet, score)
        return score

    def custom(self, board):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        cupOfThis = board.getPlayersCups(self.num)
        cupOfOppo = board.getPlayersCups(self.opp)
        ply = 9 - (sum(cupOfThis) + sum(cupOfOppo)) / 10
        if cupOfThis.count(4) == 6:
            return 6, 3, self.num, ply
        if cupOfThis.count(4) == 2 and cupOfThis.count(0) == 1 and cupOfThis.count(5) == 3:
            return 6, 6, self.num, ply
        if cupOfOppo.count(4) == 2 and cupOfOppo.count(0) == 2 and cupOfOppo.count(5) == 2:
            return 7, 5, self.num, ply
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score1(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            again = nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            if again:
                s = self.customMax(nb, ply-1, turn, -INFINITY, INFINITY) #If move m can make it go another step, then call customMax
                                                                        #by maximize the huristic function for next step
            else:
                s = opp.customMin(nb, ply-1, turn, -INFINITY, INFINITY) #Else, call customMin
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move, self.num, ply

    def customMax(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        alp = alpha
        bet = beta
        if board.gameOver():
            return turn.score1(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score1(board) in max value is: " + str(turn.score1(board))
                return turn.score1(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            again = nextBoard.makeMove(self, m)
            if again:
                s = self.customMax(nextBoard, ply - 1, turn, alp, bet)  #If move m can make it go another step, then call customMax
                                                                        #by maximize the huristic function for next step
            else:
                s = opponent.customMin(nextBoard, ply-1, turn, alp, bet) # Else, call customMin
            #print "s in customMax is: " + str(s)
            score = max(score, s)
            if bet <= score:
                return score
            alp = max(alp, score)
        return score
    
    def customMin(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        alp = alpha
        bet = beta
        if board.gameOver():
            return turn.score1(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score1(board) in min Value is: " + str(turn.score1(board))
                return turn.score1(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            again = nextBoard.makeMove(self, m)
            if again:
                s = self.customMin(nextBoard, ply - 1, turn, alp, bet)  #If move m can make it go another step, then call customMin
                                                                        #by minimize the huristic function for next step
            else:
                s = opponent.customMax(nextBoard, ply-1, turn, alp, bet) # Else, call customMax
            #print "s in minValue is: " + str(s)
            score = min(s, score)
            if alp >= score:
                return score
            bet = min(bet, score)
        return score
                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move, player = self.minimaxBonus(board, self.ply)
            print "player", player, "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            val, move, player, py = self.custom(board)
            print "player", player, "chose move", move, " with value", val, "with ply", py
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class jlt587(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player, the differece of 
        balls in mancala and each side is considered. This function is
        used in part one. """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        # print "Calling score in MancalaPlayer"
        # return Player.score(self, board)
        if self.num == 1:
            sumOfCups = sum(board.P1Cups)
            sumOfCupsO = sum(board.P2Cups)
        else:
            sumOfCups = sum(board.P2Cups)
            sumOfCupsO = sum(board.P1Cups)
        return board.scoreCups[self.num - 1] - board.scoreCups[self.opp - 1] + sumOfCups - sumOfCupsO

    def score1(self, board):
        """ Evaluate the Mancala board for this player, only the differece of
        balls in mancala is considered. This function is used in custom player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        # print "Calling score in MancalaPlayer"
        # return Player.score(self, board)
        if self.num == 1:
            sumOfCups = sum(board.P1Cups)
            sumOfCupsO = sum(board.P2Cups)
        else:
            sumOfCups = sum(board.P2Cups)
            sumOfCupsO = sum(board.P1Cups)
        scorediff = board.scoreCups[self.num - 1] - board.scoreCups[self.opp - 1]
        numdiff = sumOfCups - sumOfCupsO
        zeroOfThis = 0
        zeroOfOppo = 0
        for x in board.getPlayersCups(self.num):
            if x == 0:
                zeroOfThis += 1
        for x in board.getPlayersCups(self.opp):
            if x == 0:
                zeroOfOppo += 1
        zeroDiff = zeroOfThis - zeroOfOppo
        return scorediff

        
