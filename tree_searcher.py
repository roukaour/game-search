# This tree searcher uses the lab3 games framework
# to run alpha-beta searches on static game trees
# of the form seen in quiz/recitation/tutorial examples.
#
# (See TEST_1 for an example tree.)
#
# In the directory where lab3.py lives, run:
#
#	~> python tree_search.py
#
# But as prereq, your lab3.py should have def alpha_beta_search
# implemented, and your function signature conforms to the interface
# defined below:
#
# def alpha_beta_search(board, depth,
#                       eval_fn,
#                       get_next_moves_fn,
#                       is_terminal_fn):
#
# In context of tree searches:
#
# board is the current tree node.
#
# depth is the search depth.  If you specify depth as a very large
#   number then your search will end at the leaves of trees.
#
# def eval_fn(board):
#   a function that returns a score for a given board from the
#   perspective of the state's current player.
#
# def get_next_moves(board):
#   a function that takes a current node (board) and generates
#   all next (move, newboard) tuples.
#
# def is_terminal_fn(depth, board):
#   is a function that checks whether to statically evaluate
#   a board/node (hence terminating a search branch).
#
# You can modify the existing alpha_beta_search interface in lab3
# to work with this interface by definining your own is_terminal_fn
# using optional arguments, like so:
#
# def alpha_beta_search(board, depth,
#                       eval_fn,
#                       get_next_moves_fn=get_all_next_moves,
#                       is_terminal_fn=<your_terminal_function>):

from lab3 import minimax as search
#from lab3 import alpha_beta_search as search

class Node:
	"""
	Representation of a generic game tree node.
	Each node holds
	1. a label
	2. a static value (internal nodes
	generally have a None static value)
	3. node type  {MIN, MAX}
	4. list of child nodes.
	"""

	def __init__(self, label, value, node_type, children=None):
		self.label = label
		self.value = value
		self.node_type = node_type
		self.children = children or []

	def set_children(self, child_nodes):
		"""Set the children of this tree node"""
		if not self.children:
			self.children = []
		for child in child_nodes:
			self.children.append(child)

	def get_children(self):
		return self.children

	def __str__(self):
		"""Print the value of this node."""
		if self.value is None:
			return self.label
		else:
			return '%s[%s]' %(self.label, self.value)

	def add(self, child):
		"""Add children to this node."""
		if not self.children:
			self.children = []
		self.children.append(child)

	def num_children(self):
		"""Find how many children this node has."""
		if self.children:
			return len(self.children)
		else:
			return 0

def tree_as_string(node, depth=0):
	"""
	Generates a string representation of the tree
	in a space indented format
	"""
	static_value = tree_eval(node)
	buf = '%s%s:%s\n' % ('  ' * depth, node.label, static_value)
	for elt in node.children:
		buf += tree_as_string(elt, depth+1)
	return buf

def make_tree(tup):
	"""Generates a Node tree from a tuple formatted tree."""
	return make_tree_helper(tup, 'MAX')

def make_tree_helper(tup, node_type):
	"""Generate a Tree from tuple format."""
	n = Node(tup[0], tup[1], node_type)
	children = []
	if len(tup) > 2:
		node_type = 'MIN' if node_type == 'MAX' else 'MAX'
	for c in xrange(2, len(tup)):
		children.append(make_tree_helper(tup[c], node_type))
	n.set_children(children)
	return n

def is_at_depth(depth, node):
	"""
	is_terminal_fn for fixed depth trees
	True if depth == 0 has been reached.
	"""
	return depth <= 0

def is_leaf(depth, node):
	"""
	is_terminal_fn for variable-depth trees.
	Check if a node is a leaf node.
	"""
	return node.num_children() == 0

def tree_get_next_move(node):
	"""
	get_next_move_fn for trees
	Returns the list of next moves for traversing the tree
	"""
	return [(n.label, n) for n in node.children]

def tree_eval(node):
	"""Returns the static value of a node."""
	if node.value is not None:
		if node.node_type == 'MIN':
			return -node.value
		elif node.node_type == 'MAX':
			return node.value
		else:
			raise Exception('Unrecognized node type: %s' %(node.node_type))
	else:
		return None

def test_tree(name, expected, tup_tree):
	tree = make_tree(tup_tree)
	print name + ':'
	print
	print tree_as_string(tree)
	v = search(tree, 10, tree_eval, tree_get_next_move, is_leaf)
	print 'BEST MOVE:', v
	print 'EXPECTED:', expected
	print

# Run basic tests using trees.
if __name__ == '__main__':

	test_tree('TREE_1', 'I',
		('A', None,
			('B', None,
				('C', None,
					('D', 2),
					('E', 2)),
				('F', None,
					('G', 0),
					('H', 4))),
			('I', None,
				('J', None,
					('K', 6),
					('L', 8)
				),
				('M', None,
					('N', 4),
					('O', 6)))))

	test_tree('TREE_2', 'B',
		('A', None,
			('B', None,
				('C', None,
					('D', 6),
					('E', 4)),
				('F', None,
					('G', 8),
					('H', 6))),
			('I', None,
				('J', None,
					('K', 4),
					('L', 0)),
				('M', None,
					('N', 2),
					('O', 2)))))

	test_tree('TREE_3', 'B',
		('A', None,
			('B', None,
				('E', None,
					('K', 8),
					('L', 2)),
				('F', 6)),
			('C', None,
				('G', None,
					('M', None,
						('S', 4),
						('T', 5)),
					('N', 3)),
				('H', None,
					('O', 9),
					('P', None,
						('U', 10),
						('V', 8)))),
			('D', None,
				('I', 1),
				('J', None,
					('Q', None,
						('W', 7),
						('X', 12)),
					('K', None,
						('Y', 11),
						('Z', 15))))))
