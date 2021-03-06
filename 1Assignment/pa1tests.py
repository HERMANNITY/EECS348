﻿# Programming Assignment 1 Tests
# This file includes a set of tests to make sure that your code behaves as
#    expected. These tests are not at all intended to be exhaustive. You
#    should design more tests for your code in addition to these. 
execfile("jlt587-pa1.py")
print "\nProblem 1: \n"

L = [0,4,6,12,13,25,27]
print "binarySearch test case #1: " + str(binarySearch(L,-1) == (False,2))
print "binarySearch test case #2: " + str(binarySearch(L,12) == (True,0))
print "binarySearch test case #3: " + str(binarySearch(L,25) == (True,1))
# for x in xrange(-1,30):
# 	print binarySearch(L, x)
# print "\nProblem 2: \n"

x = [5,1,2,3,1] 
y = [5,1,2,3,1,4]
print "mean test case #1: " + str(mean(x) == float(12)/float(5))
print "mean test case #2: " + str(mean(y) == float(16)/float(6))
print "median test case #1: " + str(median(x) == 2)
print "median test case #2: " + str(median(y) == 2.5)

print "\nProblem 3: \n"

myTree = [4, [10, [33], [2]], [3], [14, [12]], [1]]
print "bfs test case #1: " + str(bfs(myTree, 1) == True)
print "bfs test case #2: " + str(bfs(myTree, 7) == False)
print "dfs test case #1: " + str(dfs(myTree, 1) == True)
print "dfs test case #2: " + str(dfs(myTree, 7) == False)
L = [4, 10, 33, 2, 3, 14, 12, 1]
pl3pass = True
# for x in xrange(0,35):
# 	temp = bfs(myTree, x)
# 	if x in L:
# 		pl3pass = pl3pass and (temp == True)
# 	else:
# 		pl3pass = pl3pass and (temp == False)
# if pl3pass:
# 	print "\nproblem3 passed"
# else:
# 	print "\nproblem3 failed"

print "\nProblem 4: \n"
            
myB = TTTBoard()
print myB
myB.makeMove("X", 8)
myB.makeMove("O", 7)
myB.makeMove("X", 5)
myB.makeMove("O", 6)
myB.makeMove("X", 2)
print myB

print "tic tac toe test case #1: " + str(myB.hasWon("X") == True)
print "tic tac toe test case #2: " + str(myB.hasWon("O") == False)































