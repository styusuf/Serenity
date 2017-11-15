class User(object):
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def verify(self):
		# verify username and password here
		return False