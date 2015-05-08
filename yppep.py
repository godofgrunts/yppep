#!/bin/python2
# yppep.py
# Your Perfect Python Elo Program
from __future__ import division
import challonge
import json

k = 128
tempelo = 1000

tname = "daytonsmash-417nlgwiiu" #This is just for testing, if the challonge has a subdoamin (in this case "daytonsmash") it has to be in the format SUBDOMAIN-challonge_name
challonge.set_credentials("USER_NAME", "CHALLONGE_API_KEY")
tournament = challonge.tournaments.show(tname)
participants = challonge.participants.index(tournament["id"])
numPlayers = (len(participants))


players = {}
pIDs ={}

def expectedWinRate(x,y):
	e = float(1/(1+10**((x-y)/400)))  #the math for win rates taken from wikipedia
	print e
	return(e)

def eloChange(rank, expectedWinRate, wins, totalGames, numK):
	worth = float(1 / totalGames) # this will give us a decimal number for how much each game is worth. Currently best of 3 is .33333333 I need to fix that
	actualWinRate = float(wins * worth)
	ne = float( (rank + (numK * ( actualWinRate - expectedWinRate) ) ) )
	return(ne) 

#This eventually will be fed into a SQLite table
for x in range(0, numPlayers):
	global players
	
	temp = participants[x]
	name = temp['display-name']
	playerID = temp['id']
	print name
	print playerID
	players[playerID] = name
#Temp solution until I learn SQLite
writer = csv.writer(open('players.csv', 'wb'))
for key, value in players.items():
	writer.writerow([key, value])

matchinfo = challonge.matches.index(tname)
numMatches = len(matchinfo)

#This eventually will be fed into a SQLite table
for x in range (0, numMatches):
	global tempelo
	global k
	print 'Match id is: ' + str((matchinfo[x])['id'])
	print 'Player1 is: ' + str((matchinfo[x])['player1-id'])
	print 'Player2 is: ' + str((matchinfo[x])['player2-id'])
	print 'Final Score was: ' + str((matchinfo[x])['scores-csv'])
	games = str((matchinfo[x])['scores-csv']).split('-', 1)
	print games
	aWins = int(games[0])
	print aWins
	bWins = int(games[1])
	print bWins
	totalGames = int(games[0]) + int(games[1])
	print totalGames
	elo1 = tempelo
	print elo1
	elo2 = tempelo
	print elo2
	eA = float(expectedWinRate(elo2,elo1)) #this calculates player 1's win rate
	eB = float(expectedWinRate(elo1,elo2)) #this calculates player 2's win rate
	
	print u"Expected win rates are :", eA, eB
	
	newElo1 = eloChange(elo1, eA, aWins, totalGames, k)
	newElo2 = eloChange(elo2, eB, bWins, totalGames, k)
	
	print u"New Elos are :", newElo1, newElo2
	
	print '\n'