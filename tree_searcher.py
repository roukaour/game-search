#from lab3 import minimax as search
from lab3 import alpha_beta_search as search

class Node(object):
	"""
	Representation of a generic game tree node.

	Each node holds:
	* label
	* value (internal nodes generally have a value of None)
	* node type ('MIN' or 'MAX')
	* children (list of child nodes)
	"""

	def __init__(self, label, value, node_type, children=None):
		"""Initialize this node."""
		self.label = label
		self.value = value
		self.node_type = node_type
		self.children = children or []

	def set_children(self, child_nodes):
		"""Set the children of this node."""
		for child in child_nodes:
			self.children.append(child)

	def get_children(self):
		"""Get the children of this node."""
		return self.children

	def __str__(self):
		"""Return a printable string representation of this node."""
		if self.value is None:
			return self.label
		return '%s[%s]' % (self.label, self.value)

	def add(self, child):
		"""Add a child to this node."""
		self.children.append(child)

	def num_children(self):
		"""Return how many children this node has."""
		return len(self.children)

	def as_tree_string(self, depth=0):
		"""Return a string representation of this node and its children."""
		return '\n'.join(['%s%s:%s' % ('  ' * depth,
			self.label, tree_eval(self))] +
			[child.as_tree_string(depth + 1)
				for child in self.children])


def make_tree(tup):
	"""Generates a Node tree from a tuple formatted tree."""
	return make_tree_helper(tup, 'MAX')

def make_tree_helper(tup, node_type):
	"""Generate a Tree from tuple format."""
	node = Node(tup[0], tup[1], node_type)
	children = []
	child_node_type = 'MIN' if node_type == 'MAX' else 'MAX'
	for child_tup in tup[2:]:
		children.append(make_tree_helper(child_tup, child_node_type))
	node.set_children(children)
	return node


def tree_eval(node):
	"""
	'eval_fn' for tree nodes.
	Return the static value of a node.
	"""
	if node.value is None:
		return None
	if node.node_type == 'MAX':
		return node.value
	if node.node_type == 'MIN':
		return -node.value
	raise Exception('Unrecognized node type: %s' % node.node_type)

def tree_get_next_moves(node):
	"""
	'get_next_moves_fn' for tree nodes.
	Return the list of next moves for traversing the tree.
	"""
	return [(node.label, node) for node in node.children]

def is_leaf(node):
	"""
	'is_terminal_fn' for tree nodes.
	Return whether a node is a leaf node.
	"""
	return node.num_children() == 0


def test_tree(name, expected, tup_tree):
	tree_node = make_tree(tup_tree)
	print name + ':'
	print tree_node.as_tree_string()
	best_move = search(tree_node, 10, tree_eval, tree_get_next_moves, is_leaf)
	print 'BEST MOVE:', best_move
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
