from random import randint
from random import choice
from collections import Counter

class Player:
	def __init__(self):
		"""
		Creates a new Player object with 0 wins and 0 losses.

		Attributes
		----------
		wins : int
			Number of games won by player
		losses : int
			Number of games lost by player
		"""
		self.wins = 0
		self.losses = 0

	def getGamesPlayed(self):
		"""
		Returns the total number of games played by the player

		Returns
		-------
		int
			The number of games played by the player
		"""
		return self.wins + self.losses

	def isFinished(self, rounds):
		"""
		Returns True if player has played the maximum number of games in the 
		tournament or would finish with a losing record, otherwise returns False

		Parameters
		----------
		rounds : int
			The maximum number of games a player can play

		Returns
		-------
		bool
			True if player has played the max number of games or will finish
			with a losing record, otherwise False
		"""
		return self.getGamesPlayed() >= rounds or self.hasDropped(rounds)

	def hasDropped(self, rounds):
		return self.losses > rounds / 2

	def getPrintableRecord(self):
		return str(self.wins) + "-" + str(self.losses)

	def __str__(self):
		return "A Player with a win/loss record of " + getPrintableRecord(self)


def runTourament(entrants, rounds):
	"""
	runTournament(entrants, rounds)

	Simulates a qualifying tournament with random matchmaking. Assumes each 
	player has a 50/50 chance of winning against any opponent. Players drop from
	the	tournament as soon as they no longer have a chance at a winning record.
	Returns a list of Player objects sorted by player wins descending.

	Parameters
	----------
	entrants : int
		Number of players participating in tournament
	rounds : int
		Maximum number of qualifying games played by each participant

	Returns
	-------
	list of Players
		List of Players sorted by number of player wins descending
	"""

	# create the list of Players and a companion list of players who have yet to
	# complete all of their games -- the matchmaking pool
	listOfPlayers = [Player() for i in xrange(entrants)]
	availablePlayers = range(entrants)

	# play games
	for i in xrange(entrants):

		currentPlayer = listOfPlayers[i]

		# remove currentPlayer from matchmaking pool
		if i in availablePlayers:
			availablePlayers.remove(i)

		# if all other players have played their games do not attempt further matchmaking
		if availablePlayers == []:
			break

		# randomly matchmake games for currentPlayer until they have played the
		# maximum number of games or have dropped from the tournament
		while(not currentPlayer.isFinished(rounds)):

			# if all other players have finished their games, end matchmaking
			if availablePlayers == []:
				break

			# matchmake with random available opponenent
			opponentIndex = choice(availablePlayers)
			currentOpponent = listOfPlayers[opponentIndex]

			# flip a coin to see who wins and assign wins/losses to players
			if(randint(0,1) == 0):
				# currentPlayer wins
				currentPlayer.wins += 1
				currentOpponent.losses += 1
			else:
				# currentPlayer loses
				currentPlayer.losses += 1
				currentOpponent.wins += 1

			# if opponent has finished all games or would finish the tournament 
			# with a losing record, remove them from the matchmaking pool
			if currentOpponent.isFinished(rounds):
				availablePlayers.remove(opponentIndex)

	# sort players by wins descending
	listOfPlayers.sort(reverse=True, key=lambda p : p.wins)

	# return sorted list of players
	return listOfPlayers

def printLeaderboard(listOfPlayers, topCut):
	"""
	prints the records of the players who made the top cut
	"""
	print "---LEADERBOARD---"
	for i in xrange(topCut):
		print str(i+1) + ": " + listOfPlayers[i].getPrintableRecord()

def printTopCutInfo(listOfPlayers, topCut):
	"""
	calculates and prints how many players on the "bubble" made the top cut
	"""
	playerWinTotals = [player.wins for player in listOfPlayers]
	bubbleWins = playerWinTotals[topCut - 1]
	bubblePlayersIn = Counter(playerWinTotals[:topCut])[bubbleWins]
	bubblePlayersTotal = Counter(playerWinTotals)[bubbleWins]
	print str(bubblePlayersIn) + " out of " + str(bubblePlayersTotal) + " players with " +\
		str(bubbleWins) + " wins made the cut to top " + str(topCut) + "."

def printNumberOfDrops(listOfPlayers, rounds):
	"""
	calculates and prints how many players dropped from the tournament before 
	completing the maximum number of games
	"""
	nDrops = 0
	for player in listOfPlayers:
		if player.hasDropped(rounds) and player.getGamesPlayed() < rounds:
			nDrops += 1
	print str(nDrops) + " players dropped from the tournament before \
completing all of their games because they were guaranteed to finish with \
a losing record"

def getBubbleRecord(listOfPlayers, topCut):
	return listOfPlayers[topCut-1].getPrintableRecord()

def runTrials(players, rounds, topCut, nTrials=100):
	bubbleRecords = {}
	for x in xrange(nTrials):
		listOfPlayers = runTourament(players, rounds)
		bubbleRecord = getBubbleRecord(listOfPlayers, topCut)
		if bubbleRecord in bubbleRecords:
			bubbleRecords[bubbleRecord] += 1
		else:
			bubbleRecords[bubbleRecord] = 1
	return bubbleRecords

def printTrialsResult(bubbleRecords):
	for key in bubbleRecords.keys():
		print key + " was the cut off " + str(bubbleRecords[key]) + " times."

def main():
	entrants = int(raw_input("Enter number of tournament participants: "))
	rounds = int(raw_input("Enter number of rounds in tournament: "))
	topCut = int(raw_input("Enter the number of players to make the top cut: "))

	# listOfPlayers = runTourament(entrants, rounds)
	# printLeaderboard(listOfPlayers, topCut)
	# print
	# printTopCutInfo(listOfPlayers, topCut)
	# print
	# printNumberOfDrops(listOfPlayers, rounds)
	# print

	printTrialsResult(runTrials(entrants, rounds, topCut))

	raw_input("Press ENTER to EXIT")

main()