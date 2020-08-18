import logging


class Poll():

	def __init__(self, suggestion = {}, isActive = False):

		#List of votes. MovieTitle:[voters]
		self.suggestion = suggestion
		logging.debug(f'Setting suggestion to {suggestion}.')

		#Ordered list of titles for key matching in the suggestion dictionary
		self.titleList = list(suggestion.keys()) #Fuck you, you're a list!
		self.isActive = isActive
		self.votes = 0
		self.winner = ""

	#Return what movie options are being voted on and current vote count
	def status(self):
		response = ""

		if not self.isActive:
			response = "There is no active poll. You should start one!"
			return response

		if not len(self.titleList) > 0:
			response = "There is an active poll but the title list is empty."
			return response

		for entry in self.titleList:
			response = f'{response}`!vote {self.titleList.index(entry)}` to vote for {entry}. This title currently has {len(self.suggestion[entry])} votes.\n'
		logging.debug(f'Returning {response} from Poll.status')
		return response

	#Start a poll by adding selections from the MovieList to the poll.
	#Bot provides selections.
	def start(self, selections: list):

		if self.isActive is True:
			response = 'A poll is already in progress. Use "status" to see the current movie list and vote count.'
			return False

		#Add an empty list as a placeholder for voters to each title. This lets us use append in the vote section.
		for entry in selections:
			self.suggestion[entry] = []
			self.titleList.append(entry)

		self.isActive = True
		return True

	#Add user's ID to the title's list of voters.
	def vote(self, userID: str, movieID: str):

		try:
			choice = int(movieID)
		except ValueError:
			response = f'{choice} is not a number. Please give me a number.'
			return response

		logging.debug(f'self.titleList={self.titleList} {type(self.titleList)}')
		logging.debug(f'choice={choice}')
		logging.debug(f'movieID={movieID}')
		logging.debug(f'userID={userID}')

		foundKey = self.titleList[choice]
		self.suggestion[foundKey].append(userID)
		return None

	#Close the poll. Tally the votes cast and return the winner.
	def close(self):

		for key in self.suggestion:
			if len(self.suggestion[key]) > self.votes:
				self.votes = len(self.suggestion[key])
				self.winner = key
		self.isActive = False
		self.suggestion = {}
		response = (f'The winner is {self.winner} with {self.votes} votes!')
		return response
