from TwitterAPI import (TwitterAPI, TwitterOAuth, TwitterRequestError, 
	TwitterConnectionError, TwitterPager, HydrateType)


# NOTE: If any of the conversation is over a week old then it will not get 
# returned unless you are using academic credentials.
CONVERSATION_ID = '20'


#
# UTILITY CLASS
#

class TreeNode:
	"""TreeNode is used to organize tweets as a tree structure"""

	def __init__(self, data):
		"""data is a tweet's json object"""
		self.data = data
		self.children = []
		self.replied_to_tweet = None
		if 'referenced_tweets' in self.data:
			for tweet in self.data['referenced_tweets']: 
				if tweet['type'] == 'replied_to':
					self.replied_to_tweet = tweet['id']
					break

	def id(self):
		"""a node is identified by its tweet id"""
		return self.data['id']

	def parent(self):
		"""the reply-to tweet is the parent of the node"""
		return self.replied_to_tweet

	def find_parent_of(self, node):
		"""append a node to the children of it's parent tweet"""
		if node.parent() == self.id():
			self.children.append(node)
			return True
		for child in self.children:
			if child.find_parent_of(node):
				return True
		return False

	def print_tree(self, level):
		"""level 0 is the root node, then incremented for subsequent generations"""
		created_at = self.data['created_at']
		username = self.data['author_id']['username']
		text_80chars = self.data['text'][0:80].replace('\n', ' ')
		print(f'{level*"_"}{level}: [{created_at}][{username}] {text_80chars}')
		level += 1
		for child in reversed(self.children):
			child.print_tree(level)


#
# PROGRAM BEGINS HERE
#

try:
	o = TwitterOAuth.read_file()
	api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type='oAuth2', api_version='2')

	# GET ROOT OF THE CONVERSATION

	r = api.request(f'tweets/:{CONVERSATION_ID}',
		{
			'expansions':'author_id',
			'tweet.fields':'author_id,conversation_id,created_at,referenced_tweets'
		},
		hydrate_type=HydrateType.REPLACE)

	root = None
	for item in r:
		root = TreeNode(item)
		print(f'ROOT {root.id()}')
	if not root:
		print(f'Conversation ID {CONVERSATION_ID} does not exist')
		exit()

	# GET ALL REPLIES IN CONVERSATION
	# (RETURNED IN REVERSE CHRONOLOGICAL ORDER)

	pager = TwitterPager(api, 'tweets/search/recent', 
		{
			'query':f'conversation_id:{CONVERSATION_ID}',
			'expansions':'author_id',
			'tweet.fields':'author_id,conversation_id,created_at,referenced_tweets'
		},
		hydrate_type=HydrateType.REPLACE)

	# "wait=2" means wait 2 seconds between each request.
	# The rate limit is 450 requests per 15 minutes, or 1 request every 15*60/450 = 2 seconds. 

	orphans = []

	for item in pager.get_iterator(wait=2):
		node = TreeNode(item)
		print(f'{node.id()} => {node.parent()}', item['author_id']['username'])
		# COLLECT ANY ORPHANS THAT ARE CHILDREN OF THE NEW NODE
		orphans = [orphan for orphan in orphans if not node.find_parent_of(orphan)]
		# IF THE NEW NODE CANNOT BE PLACED IN TREE, ORPHAN IT UNTIL ITS PARENT IS FOUND
		if not root.find_parent_of(node):
			orphans.append(node)

	print('\nTREE...')
	root.print_tree(0)

	# YOU MIGHT GET ORPHANS WHEN PART OF THE CONVERSATION IS OLDER THAN A WEEK
	assert len(orphans) == 0, f'{len(orphans)} orphaned tweets'

except TwitterRequestError as e:
	print(e.status_code)
	for msg in iter(e):
		print(msg)

except TwitterConnectionError as e:
	print(e)

except Exception as e:
	print(e)
