# Matthew Meehan
# RubiksCube Class 

import numpy

def all_combos(choices):
    """
    Given a list of items (a,b,c,...), generates all possible combinations of
    items where one item is taken from a, one from b, one from c, and so on.

    For example, all_combos([[1, 2], ["a", "b", "c"]]) yields:

        [1, "a"]
        [1, "b"]
        [1, "c"]
        [2, "a"]
        [2, "b"]
        [2, "c"]
    """
    if not choices:
        yield []
        return

    for left_choice in choices[0]:
        for right_choices in all_combos(choices[1:]):
            yield [left_choice] + right_choices
            
class Node:
    def __init__(self, value, children=[]):
        self.value    = value
        self.children = children

    def all_subtrees(self, max_depth):
        yield Node(self.value)

        if max_depth > 0:
            # For each child, get all of its possible sub-trees.
            child_subtrees = [list(self.children[i].all_subtrees(max_depth - 1)) for i in range(len(self.children))]

            # Now for the n children iterate through the 2^n possibilities where
            # each child's subtree is independently present or not present. The
            # i-th child is present if the i-th bit in "bits" is a 1.
            for bits in xrange(1, 2 ** len(self.children)):
                for combos in all_combos([child_subtrees[i] for i in range(len(self.children)) if bits & (1 << i) != 0]):
                    yield Node(self.value, combos)

    def __str__(self):
        """
        Display the node's value, and then its children in brackets if it has any.
        """
        if self.children:
            return "%s %s" % (self.value, self.children)
        else:
            return str(self.value)

    def __repr__(self):
        return str(self)
		
class RubiksCube:
	"""
		Initialize the Rubiks Cube with an array
		
		Input - Array size 54
		Output - None
	"""
	def __init__(self, state):
		self.CurrentArray = [""] * 54
		self.sides = numpy.empty((6,9),str)
		
		if state == "":
			self.reset()
		else:
			for i in range(54):
				self.CurrentArray[i] = state[i]
			
			for i in range(54):
				if state[i] == 'F':
					self.CurrentArray[i] = 'r'
				if state[i] == 'B':
					self.CurrentArray[i] = 'o'
				if state[i] == 'U':
					self.CurrentArray[i] = 'y'
				if state[i] == 'D':
					self.CurrentArray[i] = 'w'
				if state[i] == 'R':
					self.CurrentArray[i] = 'g'
				if state[i] == 'L':
					self.CurrentArray[i] = 'b'
			
		self.update()
				
	def update(self):
		# Set up so that FU is an array of two faces
		# Edge FU -> [Front,Up]
		
		self.FU = [self.CurrentArray[20-1],self.CurrentArray[8-1]]
		self.FR = [self.CurrentArray[24-1],self.CurrentArray[31-1]]
		self.FL = [self.CurrentArray[22-1],self.CurrentArray[15-1]]
		self.FD = [self.CurrentArray[26-1],self.CurrentArray[47-1]]
		self.BU = [self.CurrentArray[38-1],self.CurrentArray[2-1]]
		self.BR = [self.CurrentArray[40-1],self.CurrentArray[33-1]]
		self.BL = [self.CurrentArray[42-1],self.CurrentArray[13-1]]
		self.BD = [self.CurrentArray[44-1],self.CurrentArray[53-1]]
		self.RU = [self.CurrentArray[29-1],self.CurrentArray[6-1]]
		self.RD = [self.CurrentArray[35-1],self.CurrentArray[51-1]]
		self.LU = [self.CurrentArray[11-1],self.CurrentArray[4-1]]
		self.LD = [self.CurrentArray[17-1],self.CurrentArray[49-1]]
		
		self.edges = [self.FU,self.RU,self.BU,self.LU,self.FD,self.RD,self.BD,self.LD,self.FR,self.FL,self.BR,self.BL]
		
		self.FRU = [self.CurrentArray[21-1],self.CurrentArray[28-1],self.CurrentArray[9-1]]
		self.DRF = [self.CurrentArray[48-1],self.CurrentArray[34-1],self.CurrentArray[27-1]]
		self.LFU = [self.CurrentArray[12-1],self.CurrentArray[19-1],self.CurrentArray[7-1]]
		self.DFL = [self.CurrentArray[46-1],self.CurrentArray[25-1],self.CurrentArray[18-1]]
		self.RBU = [self.CurrentArray[30-1],self.CurrentArray[37-1],self.CurrentArray[3-1]]
		self.DBR = [self.CurrentArray[53-1],self.CurrentArray[43-1],self.CurrentArray[36-1]]
		self.BLU = [self.CurrentArray[39-1],self.CurrentArray[10-1],self.CurrentArray[1-1]]
		self.DLB = [self.CurrentArray[52-1],self.CurrentArray[16-1],self.CurrentArray[45-1]]
		
		self.corner = [self.FRU,self.RBU,self.BLU,self.LFU,self.DRF,self.DFL,self.DLB,self.DBR]
		
		for i in range(54):
			if i < 9:
				self.sides[0][i] = (self.CurrentArray[i])
			elif i < 18:
				self.sides[1][i-9] = (self.CurrentArray[i])
			elif i < 27:
				self.sides[2][i-18] = (self.CurrentArray[i])
			elif i < 36:
				self.sides[3][i-27] = (self.CurrentArray[i])
			elif i < 45:
				self.sides[4][i-36] = (self.CurrentArray[i])
			elif i < 54:
				self.sides[5][i-45] = (self.CurrentArray[i])
			
		
	"""
		Reset the Rubiks Cube to solve state
		
		Input - None
		Output - None
	"""
	def reset(self):
		temp = [""] * 54
		for i in range(54):
			if i < 9:
				temp[i] = "y"
			elif i < 18:
				temp[i] = "b"
			elif i < 27:
				temp[i] = "r"
			elif i < 36:
				temp[i] = "g"
			elif i < 45:
				temp[i] = "o"
			elif i < 54:
				temp[i] = "w"
		self.CurrentArray = temp
				
	"""
		Determines if the cube is solved or not
		
		Input - None
		Output - None
	"""
	def solved(self):
		solved = RubiksCube("")
		solved.reset()
		if self.CurrentArray == solved.CurrentArray:
			return True
		else:
			return False
				
	"""
		Retruns a string format of the cube state
		
		Input - None
		Output - String
	"""
	def stringify(self):
		state = "".join(self.CurrentArray)
		return state
		
	"""
		return the next step of the cube
		
		Input - none
		Output - Integer
	"""
	def nextstep():
		return self.nextstep
		
	"""
		Reorientate the entire cube
		
		Input - None
		Output - None
	"""
	def CW_Front(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		# Changing every element in the array to its 
		# correct spots after a front face clockwise turn
		temp[21-1] = self.CurrentArray[19-1]
		temp[24-1] = self.CurrentArray[20-1]
		temp[27-1] = self.CurrentArray[21-1]
		temp[26-1] = self.CurrentArray[24-1]
		temp[25-1] = self.CurrentArray[27-1]
		temp[24-1] = self.CurrentArray[26-1]
		temp[19-1] = self.CurrentArray[25-1]
		temp[20-1] = self.CurrentArray[22-1]
		temp[7-1] =  self.CurrentArray[18-1]
		temp[8-1] =  self.CurrentArray[15-1]
		temp[9-1] =  self.CurrentArray[12-1]
		temp[28-1] = self.CurrentArray[7-1]
		temp[31-1] = self.CurrentArray[8-1]
		temp[34-1] = self.CurrentArray[9-1]
		temp[48-1] = self.CurrentArray[28-1]
		temp[47-1] = self.CurrentArray[31-1]
		temp[46-1] = self.CurrentArray[34-1]
		temp[18-1] = self.CurrentArray[48-1]
		temp[15-1] = self.CurrentArray[47-1]
		temp[12-1] = self.CurrentArray[46-1]
		
		self.CurrentArray = temp
		self.update()
		return self.stringify()
		
	def CW_Back(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		# Changing every element in the array to its 
		# correct spots after a back face clockwise turn
		temp[37-1] = self.CurrentArray[43-1]
		temp[38-1] = self.CurrentArray[40-1]
		temp[39-1] = self.CurrentArray[37-1]
		temp[42-1] = self.CurrentArray[38-1]
		temp[45-1] = self.CurrentArray[39-1]
		temp[44-1] = self.CurrentArray[42-1]
		temp[43-1] = self.CurrentArray[45-1]
		temp[40-1] = self.CurrentArray[44-1]
		temp[10-1] = self.CurrentArray[3-1]
		temp[13-1] = self.CurrentArray[2-1]
		temp[16-1] = self.CurrentArray[1-1]
		temp[52-1] = self.CurrentArray[10-1]
		temp[53-1] = self.CurrentArray[13-1]
		temp[54-1] = self.CurrentArray[16-1]
		temp[36-1] = self.CurrentArray[52-1]
		temp[33-1] = self.CurrentArray[53-1]
		temp[30-1] = self.CurrentArray[54-1]
		temp[3-1]  = self.CurrentArray[36-1]
		temp[2-1]  = self.CurrentArray[33-1]
		temp[1-1]  = self.CurrentArray[30-1]
		
		self.CurrentArray = temp
		self.update()
		return self.stringify()
	
	def CW_Right(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		# Changing every element in the array to its 
		# correct spots after a right face clockwise turn
		temp[28-1] = self.CurrentArray[34-1]
		temp[29-1] = self.CurrentArray[31-1]
		temp[30-1] = self.CurrentArray[28-1]
		temp[33-1] = self.CurrentArray[29-1]
		temp[36-1] = self.CurrentArray[30-1]
		temp[35-1] = self.CurrentArray[33-1]
		temp[34-1] = self.CurrentArray[36-1]
		temp[31-1] = self.CurrentArray[35-1]
		temp[9-1]  = self.CurrentArray[27-1]
		temp[6-1]  = self.CurrentArray[24-1]
		temp[3-1]  = self.CurrentArray[21-1]
		temp[37-1] = self.CurrentArray[9-1]
		temp[40-1] = self.CurrentArray[6-1]
		temp[43-1] = self.CurrentArray[3-1]
		temp[54-1] = self.CurrentArray[37-1]
		temp[51-1] = self.CurrentArray[40-1]
		temp[48-1] = self.CurrentArray[43-1]
		temp[27-1] = self.CurrentArray[54-1]
		temp[24-1] = self.CurrentArray[51-1]
		temp[21-1] = self.CurrentArray[48-1]
			
		self.CurrentArray = temp
		self.update()
		return self.stringify()
		
	def CW_Left(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		# Changing every element in the array to its 
		# correct spots after a left face clockwise turn
		temp[10-1] = self.CurrentArray[16-1]
		temp[11-1] = self.CurrentArray[13-1]
		temp[12-1] = self.CurrentArray[10-1]
		temp[15-1] = self.CurrentArray[11-1]
		temp[18-1] = self.CurrentArray[12-1]
		temp[17-1] = self.CurrentArray[15-1]
		temp[16-1] = self.CurrentArray[18-1]
		temp[13-1] = self.CurrentArray[17-1]
		temp[25-1] = self.CurrentArray[7-1]
		temp[22-1] = self.CurrentArray[4-1]
		temp[19-1] = self.CurrentArray[1-1]
		temp[46-1] = self.CurrentArray[19-1]
		temp[49-1] = self.CurrentArray[22-1]
		temp[52-1] = self.CurrentArray[25-1]
		temp[39-1] = self.CurrentArray[52-1]
		temp[42-1] = self.CurrentArray[49-1]
		temp[45-1] = self.CurrentArray[46-1]
		temp[7-1]  = self.CurrentArray[39-1]
		temp[4-1]  = self.CurrentArray[42-1]
		temp[1-1]  = self.CurrentArray[45-1]
			
		self.CurrentArray = temp
		self.update()
		return self.stringify()
		
	def CW_Up(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		# Changing every element in the array to its 
		# correct spots after a up face clockwise turn
		temp[3-1]  = self.CurrentArray[1-1]
		temp[6-1]  = self.CurrentArray[2-1]
		temp[9-1]  = self.CurrentArray[3-1]
		temp[8-1]  = self.CurrentArray[6-1]
		temp[7-1]  = self.CurrentArray[9-1]
		temp[4-1]  = self.CurrentArray[8-1]
		temp[1-1]  = self.CurrentArray[7-1]
		temp[2-1]  = self.CurrentArray[4-1]
		temp[10-1] = self.CurrentArray[19-1]
		temp[11-1] = self.CurrentArray[20-1]
		temp[12-1] = self.CurrentArray[21-1]
		temp[19-1] = self.CurrentArray[28-1]
		temp[20-1] = self.CurrentArray[29-1]
		temp[21-1] = self.CurrentArray[30-1]
		temp[28-1] = self.CurrentArray[37-1]
		temp[29-1] = self.CurrentArray[38-1]
		temp[30-1] = self.CurrentArray[39-1]
		temp[37-1] = self.CurrentArray[10-1]
		temp[38-1] = self.CurrentArray[11-1]
		temp[39-1] = self.CurrentArray[12-1]
			
		self.CurrentArray = temp
		self.update()
		return self.stringify()
		
	def CW_Down(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		# Changing every element in the array to its 
		# correct spots after a down face clockwise turn
		temp[46-1] = self.CurrentArray[52-1]
		temp[47-1] = self.CurrentArray[49-1]
		temp[48-1] = self.CurrentArray[46-1]
		temp[51-1] = self.CurrentArray[47-1]
		temp[54-1] = self.CurrentArray[48-1]
		temp[53-1] = self.CurrentArray[51-1]
		temp[52-1] = self.CurrentArray[54-1]
		temp[49-1] = self.CurrentArray[53-1]
		temp[16-1] = self.CurrentArray[43-1]
		temp[17-1] = self.CurrentArray[44-1]
		temp[18-1] = self.CurrentArray[45-1]
		temp[25-1] = self.CurrentArray[16-1]
		temp[26-1] = self.CurrentArray[17-1]
		temp[27-1] = self.CurrentArray[18-1]
		temp[34-1] = self.CurrentArray[25-1]
		temp[35-1] = self.CurrentArray[26-1]
		temp[36-1] = self.CurrentArray[27-1]
		temp[43-1] = self.CurrentArray[34-1]
		temp[44-1] = self.CurrentArray[35-1]
		temp[45-1] = self.CurrentArray[36-1]
			
		self.CurrentArray = temp
		self.update()
		return self.stringify()
		
	def CCW_Front(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		# Changing every element in the array to its 
		# correct spots after a front face counterclockwise turn
		temp[19-1] = self.CurrentArray[21-1]
		temp[20-1] = self.CurrentArray[24-1]
		temp[21-1] = self.CurrentArray[27-1]
		temp[24-1] = self.CurrentArray[26-1]
		temp[27-1] = self.CurrentArray[25-1]
		temp[26-1] = self.CurrentArray[24-1]
		temp[25-1] = self.CurrentArray[19-1]
		temp[22-1] = self.CurrentArray[20-1]
		temp[18-1] = self.CurrentArray[7-1]
		temp[15-1] = self.CurrentArray[8-1]
		temp[12-1] = self.CurrentArray[9-1]
		temp[7-1]  = self.CurrentArray[28-1]
		temp[8-1]  = self.CurrentArray[31-1]
		temp[9-1]  = self.CurrentArray[34-1]
		temp[28-1] = self.CurrentArray[48-1]
		temp[31-1] = self.CurrentArray[47-1]
		temp[34-1] = self.CurrentArray[46-1]
		temp[48-1] = self.CurrentArray[18-1]
		temp[47-1] = self.CurrentArray[15-1]
		temp[46-1] = self.CurrentArray[12-1]
			
		self.CurrentArray = temp
		self.update()
		return self.stringify()
		
	def CCW_Back(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		# Changing every element in the array to its 
		# correct spots after a back face counterclockwise turn	
		temp[43-1] = self.CurrentArray[37-1]
		temp[40-1] = self.CurrentArray[38-1]
		temp[37-1] = self.CurrentArray[39-1]
		temp[38-1] = self.CurrentArray[42-1]
		temp[39-1] = self.CurrentArray[45-1]
		temp[42-1] = self.CurrentArray[44-1]
		temp[45-1] = self.CurrentArray[43-1]
		temp[44-1] = self.CurrentArray[40-1]
		temp[3-1]  = self.CurrentArray[10-1]
		temp[2-1]  = self.CurrentArray[13-1]
		temp[1-1]  = self.CurrentArray[16-1]
		temp[10-1] = self.CurrentArray[52-1]
		temp[13-1] = self.CurrentArray[53-1]
		temp[16-1] = self.CurrentArray[54-1]
		temp[52-1] = self.CurrentArray[36-1]
		temp[53-1] = self.CurrentArray[33-1]
		temp[54-1] = self.CurrentArray[30-1]
		temp[36-1] = self.CurrentArray[3-1]
		temp[33-1] = self.CurrentArray[2-1]
		temp[30-1] = self.CurrentArray[1-1]
			
		self.CurrentArray = temp
		self.update()
		return self.stringify()
		
	def CCW_Right(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		# Changing every element in the array to its 
		# correct spots after a right face counterclockwise turn	
		temp[34-1] = self.CurrentArray[28-1]
		temp[31-1] = self.CurrentArray[29-1]
		temp[28-1] = self.CurrentArray[30-1]
		temp[29-1] = self.CurrentArray[33-1]
		temp[30-1] = self.CurrentArray[36-1]
		temp[33-1] = self.CurrentArray[35-1]
		temp[36-1] = self.CurrentArray[34-1]
		temp[35-1] = self.CurrentArray[31-1]
		temp[27-1] = self.CurrentArray[9-1]
		temp[24-1] = self.CurrentArray[6-1]
		temp[21-1] = self.CurrentArray[3-1]
		temp[9-1]  = self.CurrentArray[37-1]
		temp[6-1]  = self.CurrentArray[40-1]
		temp[3-1]  = self.CurrentArray[43-1]
		temp[37-1] = self.CurrentArray[54-1]
		temp[40-1] = self.CurrentArray[51-1]
		temp[43-1] = self.CurrentArray[48-1]
		temp[54-1] = self.CurrentArray[27-1]
		temp[51-1] = self.CurrentArray[24-1]
		temp[48-1] = self.CurrentArray[21-1]
			
		self.CurrentArray = temp
		self.update()
		return self.stringify()
		
	def CCW_Left(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		# Changing every element in the array to its 
		# correct spots after a left face counterclockwise turn	
		temp[16-1] = self.CurrentArray[10-1]
		temp[13-1] = self.CurrentArray[11-1]
		temp[10-1] = self.CurrentArray[12-1]
		temp[11-1] = self.CurrentArray[15-1]
		temp[12-1] = self.CurrentArray[18-1]
		temp[15-1] = self.CurrentArray[17-1]
		temp[18-1] = self.CurrentArray[16-1]
		temp[17-1] = self.CurrentArray[13-1]
		temp[7-1]  = self.CurrentArray[25-1]
		temp[4-1]  = self.CurrentArray[22-1]
		temp[1-1]  = self.CurrentArray[19-1]
		temp[19-1] = self.CurrentArray[46-1]
		temp[22-1] = self.CurrentArray[49-1]
		temp[25-1] = self.CurrentArray[52-1]
		temp[52-1] = self.CurrentArray[39-1]
		temp[49-1] = self.CurrentArray[42-1]
		temp[46-1] = self.CurrentArray[45-1]
		temp[39-1] = self.CurrentArray[7-1]
		temp[42-1] = self.CurrentArray[4-1]
		temp[45-1] = self.CurrentArray[1-1]
			
		self.CurrentArray = temp
		self.update()
		return self.stringify()
		
	def CCW_Up(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		# Changing every element in the array to its 
		# correct spots after a up face counterclockwise turn
		temp[1-1]  = self.CurrentArray[3-1]
		temp[2-1]  = self.CurrentArray[6-1]
		temp[3-1]  = self.CurrentArray[9-1]
		temp[6-1]  = self.CurrentArray[8-1]
		temp[9-1]  = self.CurrentArray[7-1]
		temp[8-1]  = self.CurrentArray[4-1]
		temp[7-1]  = self.CurrentArray[1-1]
		temp[4-1]  = self.CurrentArray[2-1]
		temp[19-1] = self.CurrentArray[10-1]
		temp[20-1] = self.CurrentArray[11-1]
		temp[21-1] = self.CurrentArray[12-1]
		temp[28-1] = self.CurrentArray[19-1]
		temp[29-1] = self.CurrentArray[20-1]
		temp[30-1] = self.CurrentArray[21-1]
		temp[37-1] = self.CurrentArray[28-1]
		temp[38-1] = self.CurrentArray[29-1]
		temp[39-1] = self.CurrentArray[30-1]
		temp[10-1] = self.CurrentArray[37-1]
		temp[11-1] = self.CurrentArray[38-1]
		temp[12-1] = self.CurrentArray[39-1]
			
		self.CurrentArray = temp
		self.update()
		return self.stringify()
		
	def CCW_Down(self):
		# Setting a temp variable
		temp = [""] * 54
		for i in range(54):
			temp[i]=self.CurrentArray[i]
		
		
		# Changing every element in the array to its 
		# correct spots after a down face counterclockwise turn
		temp[52-1] = self.CurrentArray[46-1]
		temp[49-1] = self.CurrentArray[47-1]
		temp[46-1] = self.CurrentArray[48-1]
		temp[47-1] = self.CurrentArray[51-1]
		temp[48-1] = self.CurrentArray[54-1]
		temp[51-1] = self.CurrentArray[53-1]
		temp[54-1] = self.CurrentArray[52-1]
		temp[53-1] = self.CurrentArray[49-1]
		temp[43-1] = self.CurrentArray[16-1]
		temp[44-1] = self.CurrentArray[17-1]
		temp[45-1] = self.CurrentArray[18-1]
		temp[16-1] = self.CurrentArray[25-1]
		temp[17-1] = self.CurrentArray[26-1]
		temp[18-1] = self.CurrentArray[27-1]
		temp[25-1] = self.CurrentArray[34-1]
		temp[26-1] = self.CurrentArray[35-1]
		temp[27-1] = self.CurrentArray[36-1]
		temp[34-1] = self.CurrentArray[43-1]
		temp[35-1] = self.CurrentArray[44-1]
		temp[36-1] = self.CurrentArray[45-1]
			
		self.CurrentArray = temp
		self.update()
		return self.stringify()
	
	def traverse(self, state, depth, target,i):
		edge_actions = ['U','D','L','R','Up','Dp','Lp','Rp']
		temp_cube = RubiksCube(state)
		
		if depth == 5:
			print(depth)
			print("Max depth")
			return 1
			
		for a in edge_actions:
			if a == 'U':
				temp_cube.CW_Up()
			if a == 'D':
				temp_cube.CW_Down()
			if a == 'L':
				temp_cube.CW_Left()
			if a == 'R':
				temp_cube.CW_Right()
			if a == 'Up':
				temp_cube.CCW_Up()
			if a == 'Dp':
				temp_cube.CCW_Down()
			if a == 'Lp':
				temp_cube.CCW_Left()
			if a == 'Rp':
				temp_cube.CCW_Right()
			cube_str = temp_cube.stringify()
			print(temp_cube.edges[i])
			
			print(i)
			if temp_cube.edges[i] == target:
				print("Returned")
				return 0
				
			return self.traverse(cube_str,depth + 1,target,i)
						
	def get_orientataion(self):
		state = [0] * 40
		
		#	self.edges = [self.FU,self.RU,self.BU,self.LU,self.FD,self.RD,self.BD,self.LD,self.FR,self.FL,self.BR,self.BL]
		# self.corners = [self.FRU,self.BRU,self.BLU,self.FLU,self.FRD,self.FLD,self.BLD,self.BRD]
		
		# Edges: FU(0), FR(8), FL(9), FD(4), BU(2), BR(10), BL(11), BD(6), RU(1), RD(5), LU(3), LD(7)
		# Edges(Done): RU = 1, FR = 8, FU = 0, FL = 9, FD = 4, BU = 2, LU = 3, RD = 5, BD = 6, LD = 7, BR = 10, BL = 11
		# Corners: FRU(12), FRD(16), FLU(15), FLD(17), BRU(13), BRD(19), BLU(14), BLD(18)
		
		FU = ['r','y']
		RU = ['g','y']
		BU = ['o','y']
		LU = ['b','y']
		FD = ['r','w']
		RD = ['g','w']
		BD = ['o','w']
		LD = ['b','w']
		FR = ['r','g']
		FL = ['r','b']
		BR = ['o','g']
		BL = ['o','b']
	
		a = self.edges
		"""
		if all(value in FU for value in a):
			state[b] = 0
			state[b+20] = self.traverse(self.stringify(),0, ['r', 'y'],0)			
		if all(value in RU for value in a):
			state[b] = 1
			state[b+20] = self.traverse(self.stringify(),0, ['g', 'y'],1)
		if all(value in BU for value in a):
			state[b] = 2
			state[b+20] = self.traverse(self.stringify(),0, ['o', 'y'],2)
		if all(value in LU for value in a):
			state[b] = 3
			state[b+20] = self.traverse(self.stringify(),0, ['b', 'y'],3)
		if all(value in FD for value in a):
			state[b] = 4
			state[b+20] = self.traverse(self.stringify(),0, ['r', 'w'],4)
		if all(value in RD for value in a):
			state[b] = 5
			state[b+20] = self.traverse(self.stringify(),0, ['g', 'w'],5)
		if all(value in BD for value in a):
			state[b] = 6
			state[b+20] = self.traverse(self.stringify(),0, ['o', 'w'],6)
		if all(value in LD for value in a):
			state[b] = 7
			state[b+20] = self.traverse(self.stringify(),0, ['b', 'w'],7)
		if all(value in FR for value in a):
			state[b] = 8
			state[b+20] = self.traverse(self.stringify(),0, ['r', 'g'],8)
		if all(value in FL for value in a):
			state[b] = 9
			state[b+20] = self.traverse(self.stringify(),0, ['r', 'b'],9)
		if all(value in BR for value in a):
			state[b] = 10
			state[b+20] = self.traverse(self.stringify(),0, ['o', 'g'],10)
		if all(value in BL for value in a):
			state[b] = 11
			state[b+20] = self.traverse(self.stringify(),0, ['o', 'b'],11)
		b = b + 1
		"""
		
		#FU
		if a[0] == ['r', 'y']:
			state[0] = 0
			state[0 + 20] = 0
		#RU
		elif a[1] == ['r','y']:
			state[1] = 0
			state[1 + 20] = 0
		#BU
		elif a[2] == ['r','y']:
			state[2] = 0
			state[2 + 20] = 0
		#LU
		elif a[3] == ['r','y']:
			state[3] = 0
			state[3 + 20] = 0
		#FD
		elif a[4] == ['r','y']:
			state[4] = 0
			state[4 + 20] = 0
		#RD
		elif a[5] == ['r','y']:
			state[5] = 0
			state[5 + 20] = 0
		#BD
		elif a[6] == ['r','y']:
			state[6] = 0
			state[6 + 20] = 0
		#LD
		elif a[7] == ['r','y']:
			state[7] = 0
			state[7 + 20] = 0
		#FR
		elif a[8] == ['r','y']:
			state[8] = 0
			state[8 + 20] = 1
		#FL
		elif a[9] == ['r','y']:
			state[9] = 0
			state[9 + 20] = 1
		#BR
		elif a[10] == ['r','y']:
			state[10] = 0
			state[10 + 20] = 1
		#BL
		elif a[11] == ['r','y']:
			state[11] = 0
			state[11 + 20] = 1
		#FU
		if a[0] == ['y', 'r']:
			state[0] = 0
			state[0 + 20] = 1
		#RU
		elif a[1] == ['y', 'r']:
			state[1] = 0
			state[1 + 20] = 1
		#BU
		elif a[2] == ['y', 'r']:
			state[2] = 0
			state[2 + 20] = 1
		#LU
		elif a[3] == ['y', 'r']:
			state[3] = 0
			state[3 + 20] = 1
		#FD
		elif a[4] == ['y', 'r']:
			state[4] = 0
			state[4 + 20] = 1
		#RD
		elif a[5] == ['y', 'r']:
			state[5] = 0
			state[5 + 20] = 1
		#BD
		elif a[6] == ['y', 'r']:
			state[6] = 0
			state[6 + 20] = 1
		#LD
		elif a[7] == ['y', 'r']:
			state[7] = 0
			state[7 + 20] = 1
		#FR
		elif a[8] == ['y', 'r']:
			state[8] = 0
			state[8 + 20] = 0
		#FL
		elif a[9] == ['y', 'r']:
			state[9] = 0
			state[9 + 20] = 0
		#BR
		elif a[10] == ['y', 'r']:
			state[10] = 0
			state[10 + 20] = 0
		#BL
		elif a[11] == ['y', 'r']:
			state[11] = 0
			state[11 + 20] = 0
			
		########################
		
		#FU
		if a[0] == ['g', 'y']:
			state[0] = 1
			state[0 + 20] = 0
		#RU
		elif a[1] == ['g','y']:
			state[1] = 1
			state[1 + 20] = 0
		#BU
		elif a[2] == ['g','y']:
			state[2] = 1
			state[2 + 20] = 0
		#LU
		elif a[3] == ['g','y']:
			state[3] = 1
			state[3 + 20] = 0
		#FD
		elif a[4] == ['g','y']:
			state[4] = 1
			state[4 + 20] = 0
		#RD
		elif a[5] == ['g','y']:
			state[5] = 1
			state[5 + 20] = 0
		#BD
		elif a[6] == ['g','y']:
			state[6] = 1
			state[6 + 20] = 0
		#LD
		elif a[7] == ['g','y']:
			state[7] = 1
			state[7 + 20] = 0
		#FR
		elif a[8] == ['g','y']:
			state[8] = 1
			state[8 + 20] = 1
		#FL
		elif a[9] == ['g','y']:
			state[9] = 1
			state[9 + 20] = 1
		#BR
		elif a[10] == ['g','y']:
			state[10] = 1
			state[10 + 20] = 1
		#BL
		elif a[11] == ['g','y']:
			state[11] = 1
			state[11 + 20] = 1
		#FU
		if a[0] == ['y', 'g']:
			state[0] = 1
			state[0 + 20] = 1
		#RU
		elif a[1] == ['y', 'g']:
			state[1] = 1
			state[1 + 20] = 1
		#BU
		elif a[2] == ['y', 'g']:
			state[2] = 1
			state[2 + 20] = 1
		#LU
		elif a[3] == ['y', 'g']:
			state[3] = 1
			state[3 + 20] = 1
		#FD
		elif a[4] == ['y', 'g']:
			state[4] = 1
			state[4 + 20] = 1
		#RD
		elif a[5] == ['y', 'g']:
			state[5] = 1
			state[5 + 20] = 1
		#BD
		elif a[6] == ['y', 'g']:
			state[6] = 1
			state[6 + 20] = 1
		#LD
		elif a[7] == ['y', 'g']:
			state[7] = 1
			state[7 + 20] = 1
		#FR
		elif a[8] == ['y', 'g']:
			state[8] = 1
			state[8 + 20] = 0
		#FL
		elif a[9] == ['y', 'g']:
			state[9] = 1
			state[9 + 20] = 0
		#BR
		if a[10] == ['y', 'g']:
			state[10] = 1
			state[10 + 20] = 0
		#BL
		elif a[11] == ['y', 'g']:
			state[11] = 1
			state[11 + 20] = 0
			
		########################
		
		#FU
		if a[0] == ['o', 'y']:
			state[0] = 2
			state[0 + 20] = 0
		#RU
		elif a[1] == ['o','y']:
			state[1] = 2
			state[1 + 20] = 0
		#BU
		elif a[2] == ['o','y']:
			state[2] = 2
			state[2 + 20] = 0
		#LU
		elif a[3] == ['o','y']:
			state[3] = 2
			state[3 + 20] = 0
		#FD
		elif a[4] == ['o','y']:
			state[4] = 2
			state[4 + 20] = 0
		#RD
		elif a[5] == ['o','y']:
			state[5] = 2
			state[5 + 20]= 0
		#BD
		elif a[6] == ['o','y']:
			state[6] = 2
			state[6 + 20] = 0
		#LD
		elif a[7] == ['o','y']:
			state[7] = 2
			state[7 + 20] = 0
		#FR
		elif a[8] == ['o','y']:
			state[8] = 2
			state[8 + 20] = 1
		#FL
		elif a[9] == ['o','y']:
			state[9] = 2
			state[9 + 20] = 1
		#BR
		elif a[10] == ['o','y']:
			state[10] = 2
			state[10 + 20] = 1
		#BL
		elif a[11] == ['o','y']:
			state[11] = 2
			state[11 + 20] = 1
		#FU
		if a[0] == ['y', 'o']:
			state[0] = 2
			state[0 + 20] = 1
		#RU
		elif a[1] == ['y', 'o']:
			state[1] = 2
			state[1 + 20] = 1
		#BU
		elif a[2] == ['y', 'o']:
			state[2] = 2
			state[2 + 20] = 1
		#LU
		elif a[3] == ['y', 'o']:
			state[3] = 2
			state[3 + 20] = 1
		#FD
		elif a[4] == ['y', 'o']:
			state[4] = 2
			state[4 + 20] = 1
		#RD
		elif a[5] == ['y', 'o']:
			state[5] = 2
			state[5 + 20] = 1
		#BD
		elif a[6] == ['y', 'o']:
			state[6] = 2
			state[6 + 20] = 1
		#LD
		elif a[7] == ['y', 'o']:
			state[7] = 2
			state[7 + 20] = 1
		#FR
		elif a[8] == ['y', 'o']:
			state[8] = 2
			state[8 + 20] = 0
		#FL
		elif a[9] == ['y', 'o']:
			state[9] = 2
			state[9 + 20] = 0
		#BR
		elif a[10] == ['y', 'o']:
			state[10] = 2
			state[10 + 20] = 0
		#BL
		elif a[11] == ['y', 'o']:
			state[11] = 2
			state[11 + 20] = 0
			
		########################
		
		#FU
		if a[0] == ['b', 'y']:
			state[0] = 3
			state[0 + 20] = 0
		#RU
		elif a[1] == ['b','y']:
			state[1] = 3
			state[1 + 20] = 0
		#BU
		elif a[2] == ['b','y']:
			state[2] = 3
			state[2 + 20] = 0
		#LU
		elif a[3] == ['b','y']:
			state[3] = 3
			state[3 + 20] = 0
		#FD
		elif a[4] == ['b','y']:
			state[4] = 3
			state[4 + 20] = 0
		#RD
		elif a[5] == ['b','y']:
			state[5] = 3
			state[5 + 20] = 0
		#BD
		elif a[6] == ['b','y']:
			state[6] = 3
			state[6 + 20] = 0
		#LD
		elif a[7] == ['b','y']:
			state[7] = 3
			state[7 + 20] = 0
		#FR
		elif a[8] == ['b','y']:
			state[8] = 3
			state[8 + 20] = 1
		#FL
		elif a[9] == ['b','y']:
			state[9] = 3
			state[9 + 20] = 1
		#BR
		elif a[10] == ['b','y']:
			state[10] = 3
			state[10 + 20] = 1
		#BL
		elif a[11] == ['b','y']:
			state[11] = 3
			state[11 + 20] = 1
		#FU
		if a[0] == ['y', 'b']:
			state[0] = 3
			state[0 + 20] = 1
		#RU
		elif a[1] == ['y', 'b']:
			state[1] = 3
			state[1 + 20] = 1
		#BU
		elif a[2] == ['y', 'b']:
			state[2] = 3
			state[2 + 20] = 1
		#LU
		elif a[3] == ['y', 'b']:
			state[3] = 3
			state[3 + 20] = 1
		#FD
		elif a[4] == ['y', 'b']:
			state[4] = 3
			state[4 + 20] = 1
		#RD
		elif a[5] == ['y', 'b']:
			state[5] = 3
			state[5 + 20] = 1
		#BD
		elif a[6] == ['y', 'b']:
			state[6] = 3
			state[6 + 20] = 1
		#LD
		elif a[7] == ['y', 'b']:
			state[7] = 3
			state[7 + 20] = 1
		#FR
		elif a[8] == ['y', 'b']:
			state[8] = 3
			state[8 + 20] = 0
		#FL
		elif a[9] == ['y', 'b']:
			state[9] = 3
			state[9 + 20] = 0
		#BR
		elif a[10] == ['y', 'b']:
			state[10] = 3
			state[10 + 20] = 0
		#BL
		elif a[11] == ['y', 'b']:
			state[11] = 3
			state[11 + 20] = 0
			
		#######################
			
		#FU
		if a[0] == ['r', 'w']:
			state[0] = 4
			state[0 + 20] = 0
		#RU
		elif a[1] == ['r','w']:
			state[1] = 4
			state[1 + 20] = 0
		#BU
		elif a[2] == ['r','w']:
			state[2] = 4
			state[2 + 20] = 0
		#LU
		elif a[3] == ['r','w']:
			state[3] = 4
			state[3 + 20] = 0
		#FD
		elif a[4] == ['r','w']:
			state[4] = 4
			state[4 + 20] = 0
		#RD
		elif a[5] == ['r','w']:
			state[5] = 4
			state[5 + 20] = 0
		#BD
		elif a[6] == ['r','w']:
			state[6] = 4
			state[6 + 20] = 0
		#LD
		elif a[7] == ['r','w']:
			state[7] = 4
			state[7 + 20] = 0
		#FR
		elif a[8] == ['r','w']:
			state[8] = 4
			state[8 + 20] = 1
		#FL
		elif a[9] == ['r','w']:
			state[9] = 4
			state[9 + 20] = 1
		#BR
		elif a[10] == ['r','w']:
			state[10] = 4
			state[10 + 20] = 1
		#BL
		elif a[11] == ['r','w']:
			state[11] = 4
			state[11 + 20] = 1
		#FU
		if a[0] == ['w', 'r']:
			state[0] = 4
			state[0 + 20] = 1
		#RU
		elif a[1] == ['w', 'r']:
			state[1] = 4
			state[1 + 20] = 1
		#BU
		elif a[2] == ['w', 'r']:
			state[2] = 4
			state[2 + 20] = 1
		#LU
		elif a[3] == ['w', 'r']:
			state[3] = 4
			state[3 + 20] = 1
		#FD
		elif a[4] == ['w', 'r']:
			state[4] = 4
			state[4 + 20] = 1
		#RD
		elif a[5] == ['w', 'r']:
			state[5] = 4
			state[5 + 20] = 1
		#BD
		elif a[6] == ['w', 'r']:
			state[6] = 4
			state[6 + 20] = 1
		#LD
		elif a[7] == ['w', 'r']:
			state[7] = 4
			state[7 + 20] = 1
		#FR
		elif a[8] == ['w', 'r']:
			state[8] = 4
			state[8 + 20] = 0
		#FL
		elif a[9] == ['w', 'r']:
			state[9] = 4
			state[9 + 20] = 0
		#BR
		elif a[10] == ['w', 'r']:
			state[10] = 4
			state[10 + 20] = 0
		#BL
		elif a[11] == ['w', 'r']:
			state[11] = 4
			state[11 + 20] = 0
			
		#######################
			
		#FU
		if a[0] == ['g', 'w']:
			state[0] = 5
			state[0 + 20] = 0
		#RU
		elif a[1] == ['g','w']:
			state[1] = 5
			state[1 + 20] = 0
		#BU
		elif a[2] == ['g','w']:
			state[2] = 5
			state[2 + 20] = 0
		#LU
		elif a[3] == ['g','w']:
			state[3] = 5
			state[3 + 20] = 0
		#FD
		elif a[4] == ['g','w']:
			state[4] = 5
			state[4 + 20] = 0
		#RD
		elif a[5] == ['g','w']:
			state[5] = 5
			state[5 + 20] = 0
		#BD
		elif a[6] == ['g','w']:
			state[6] = 5
			state[6 + 20] = 0
		#LD
		elif a[7] == ['g','w']:
			state[7] = 5
			state[7 + 20] = 0
		#FR
		elif a[8] == ['g','w']:
			state[8] = 5
			state[8 + 20] = 1
		#FL
		elif a[9] == ['g','w']:
			state[9] = 5
			state[9 + 20] = 1
		#BR
		elif a[10] == ['g','w']:
			state[10] = 5
			state[10 + 20] = 1
		#BL
		elif a[11] == ['g','w']:
			state[11] = 5
			state[11 + 20] = 1
		#FU
		if a[0] == ['w', 'g']:
			state[0] = 5
			state[0 + 20] = 1
		#RU
		elif a[1] == ['w', 'g']:
			state[1] = 5
			state[1 + 20] = 1
		#BU
		elif a[2] == ['w', 'g']:
			state[2] = 5
			state[2 + 20] = 1
		#LU
		elif a[3] == ['w', 'g']:
			state[3] = 5
			state[3 + 20] = 1
		#FD
		elif a[4] == ['w', 'g']:
			state[4] = 5
			state[4 + 20] = 1
		#RD
		elif a[5] == ['w', 'g']:
			state[5] = 5
			state[5 + 20] = 1
		#BD
		elif a[6] == ['w', 'g']:
			state[6] = 5
			state[6 + 20] = 1
		#LD
		elif a[7] == ['w', 'g']:
			state[7] = 5
			state[7 + 20] = 1
		#FR
		elif a[8] == ['w', 'g']:
			state[8] = 5
			state[8 + 20] = 0
		#FL
		elif a[9] == ['w', 'g']:
			state[9] = 5
			state[9 + 20] = 0
		#BR
		elif a[10] == ['w', 'g']:
			state[10] = 5
			state[10 + 20] = 0
		#BL
		elif a[11] == ['w', 'g']:
			state[11] = 5
			state[11 + 20] = 0
			
		#######################
			
		#FU
		if a[0] == ['o', 'w']:
			state[0] = 6
			state[0 + 20] = 0
		#RU
		elif a[1] == ['o','w']:
			state[1] = 6
			state[1 + 20] = 0
		#BU
		elif a[2] == ['o','w']:
			state[2] = 6
			state[2 + 20] = 0
		#LU
		elif a[3] == ['o','w']:
			state[3] = 6
			state[3 + 20] = 0
		#FD
		elif a[4] == ['o','w']:
			state[4] = 6
			state[4 + 20] = 0
		#RD
		elif a[5] == ['o','w']:
			state[5] = 6
			state[5 + 20] = 0
		#BD
		elif a[6] == ['o','w']:
			state[6] = 6
			state[6 + 20] = 0
		#LD
		elif a[7] == ['o','w']:
			state[7] = 6
			state[7 + 20] = 0
		#FR
		elif a[8] == ['o','w']:
			state[8] = 6
			state[8 + 20] = 1
		#FL
		elif a[9] == ['o','w']:
			state[9] = 6
			state[9 + 20] = 1
		#BR
		elif a[10] == ['o','w']:
			state[10] = 6
			state[10 + 20] = 1
		#BL
		elif a[11] == ['o','w']:
			state[11] = 6
			state[11 + 20] = 1
		#FU
		if a[0] == ['w', 'o']:
			state[0] = 6
			state[0 + 20] = 1
		#RU
		elif a[1] == ['w', 'o']:
			state[1] = 6
			state[1 + 20] = 1
		#BU
		elif a[2] == ['w', 'o']:
			state[2] = 6
			state[2 + 20] = 1
		#LU
		elif a[3] == ['w', 'o']:
			state[3] = 6
			state[3 + 20] = 1
		#FD
		elif a[4] == ['w', 'o']:
			state[4] = 6
			state[4 + 20] = 1
		#RD
		elif a[5] == ['w', 'o']:
			state[5] = 6
			state[5 + 20] = 1
		#BD
		elif a[6] == ['w', 'o']:
			state[6] = 6
			state[6 + 20] = 1
		#LD
		elif a[7] == ['w', 'o']:
			state[7] = 6
			state[7 + 20] = 1
		#FR
		elif a[8] == ['w', 'o']:
			state[8] = 6
			state[8 + 20] = 0
		#FL
		elif a[9] == ['w', 'o']:
			state[9] = 6
			state[9 + 20] = 0
		#BR
		elif a[10] == ['w', 'o']:
			state[10] = 6
			state[10 + 20] = 0
		#BL
		elif a[11] == ['w', 'o']:
			state[11] = 6
			state[11 + 20] = 0
		
		#######################
			
		#FU
		if a[0] == ['b', 'w']:
			state[0] = 7
			state[0 + 20] = 0
		#RU
		elif a[1] == ['b','w']:
			state[1] = 7
			state[1 + 20] = 0
		#BU
		elif a[2] == ['b','w']:
			state[2] = 7
			state[2 + 20] = 0
		#LU
		elif a[3] == ['b','w']:
			state[3] = 7
			state[3 + 20] = 0
		#FD
		elif a[4] == ['b','w']:
			state[4] = 7
			state[4 + 20] = 0
		#RD
		elif a[5] == ['b','w']:
			state[5] = 7
			state[5 + 20] = 0
		#BD
		elif a[6] == ['b','w']:
			state[6] = 7
			state[6 + 20] = 0
		#LD
		elif a[7] == ['b','w']:
			state[7] = 7
			state[7 + 20] = 0
		#FR
		elif a[8] == ['b','w']:
			state[8] = 7
			state[8 + 20] = 1
		#FL
		elif a[9] == ['b','w']:
			state[9] = 7
			state[9 + 20] = 1
		#BR
		elif a[10] == ['b','w']:
			state[10] = 7
			state[10 + 20] = 1
		#BL
		elif a[11] == ['b','w']:
			state[11] = 7
			state[11 + 20] = 1
		#FU
		if a[0] == ['w', 'b']:
			state[0] = 7
			state[0 + 20] = 1
		#RU
		elif a[1] == ['w', 'b']:
			state[1] = 7
			state[1 + 20] = 1
		#BU
		elif a[2] == ['w', 'b']:
			state[2] = 7
			state[2 + 20] = 1
		#LU
		elif a[3] == ['w', 'b']:
			state[3] = 7
			state[3 + 20] = 1
		#FD
		elif a[4] == ['w', 'b']:
			state[4] = 7
			state[4 + 20] = 1
		#RD
		elif a[5] == ['w', 'b']:
			state[5] = 7
			state[5 + 20] = 1
		#BD
		elif a[6] == ['w', 'b']:
			state[6] = 7
			state[6 + 20] = 1
		#LD
		elif a[7] == ['w', 'b']:
			state[7] = 7
			state[7 + 20] = 1
		#FR
		elif a[8] == ['w', 'b']:
			state[8] = 7
			state[8 + 20] = 0
		#FL
		elif a[9] == ['w', 'b']:
			state[9] = 7
			state[9 + 20] = 0
		#BR
		elif a[10] == ['w', 'b']:
			state[10] = 7
			state[10 + 20] = 0
		#BL
		elif a[11] == ['w', 'b']:
			state[11] = 7
			state[11 + 20] = 0
		
		#######################
			
		#FU
		if a[0] == ['r', 'g']:
			state[0] = 8
			state[0 + 20] = 1
		#RU
		elif a[1] == ['r','g']:
			state[1] = 8
			state[1 + 20] = 1
		#BU
		elif a[2] == ['r','g']:
			state[2] = 8
			state[2 + 20] = 1
		#LU
		elif a[3] == ['r','g']:
			state[3] = 8
			state[3 + 20] = 1
		#FD
		elif a[4] == ['r','g']:
			state[4] = 8
			state[4 + 20] = 1
		#RD
		elif a[5] == ['r','g']:
			state[5] = 8
			state[5 + 20] = 1
		#BD
		elif a[6] == ['r','g']:
			state[6] = 8
			state[6 + 20] = 1
		#LD
		elif a[7] == ['r','g']:
			state[7] = 8
			state[7 + 20] = 1
		#FR
		elif a[8] == ['r','g']:
			state[8] = 8
			state[8 + 20] = 0
		#FL
		elif a[9] == ['r','g']:
			state[9] = 8
			state[9 + 20] = 0
		#BR
		elif a[10] == ['r','g']:
			state[10] = 8
			state[10 + 20] = 0
		#BL
		elif a[11] == ['r','g']:
			state[11] = 8
			state[11 + 20] = 0
		#FU
		if a[0] == ['g', 'r']:
			state[0] = 8
			state[0 + 20] = 0
		#RU
		elif a[1] == ['g', 'r']:
			state[1] = 8
			state[1 + 20] = 0
		#BU
		elif a[2] == ['g', 'r']:
			state[2] = 8
			state[2 + 20] = 0
		#LU
		elif a[3] == ['g', 'r']:
			state[3] = 8
			state[3 + 20] = 0
		#FD
		elif a[4] == ['g', 'r']:
			state[4] = 8
			state[4 + 20] = 0
		#RD
		elif a[5] == ['g', 'r']:
			state[5] = 8
			state[5 + 20] = 0
		#BD
		elif a[6] == ['g', 'r']:
			state[6] = 8
			state[6 + 20] = 0
		#LD
		elif a[7] == ['g', 'r']:
			state[7] = 8
			state[7 + 20] = 0
		#FR
		elif a[8] == ['g', 'r']:
			state[8] = 8
			state[8 + 20] = 1
		#FL
		elif a[9] == ['g', 'r']:
			state[9] = 8
			state[9 + 20] = 1
		#BR
		elif a[10] == ['g', 'r']:
			state[10] = 8
			state[10 + 20] = 1
		#BL
		elif a[11] == ['g', 'r']:
			state[11] = 8
			state[11 + 20] = 1
		
		#######################
			
		#FU
		if a[0] == ['r', 'b']:
			state[0] = 9
			state[0 + 20] = 1
		#RU
		elif a[1] == ['r','b']:
			state[1] = 9
			state[b + 20] = 1
		#BU
		elif a[2] == ['r','b']:
			state[2] = 9
			state[2 + 20] = 1
		#LU
		elif a[3] == ['r','b']:
			state[3] = 9
			state[3 + 20] = 1
		#FD
		elif a[4] == ['r','b']:
			state[4] = 9
			state[4 + 20] = 1
		#RD
		elif a[5] == ['r','b']:
			state[5] = 9
			state[5 + 20] = 1
		#BD
		elif a[6] == ['r','b']:
			state[6] = 9
			state[6 + 20] = 1
		#LD
		elif a[7] == ['r','b']:
			state[7] = 9
			state[7 + 20] = 1
		#FR
		elif a[8] == ['r','b']:
			state[8] = 9
			state[8 + 20] = 0
		#FL
		elif a[9] == ['r','b']:
			state[9] = 9
			state[9 + 20] = 0
		#BR
		elif a[10] == ['r','b']:
			state[10] = 9
			state[10 + 20] = 0
		#BL
		elif a[11] == ['r','b']:
			state[11] = 9
			state[11 + 20] = 0
		#FU
		if a[0] == ['b', 'r']:
			state[0] = 9
			state[0 + 20] = 0
		#RU
		elif a[1] == ['b', 'r']:
			state[1] = 9
			state[1 + 20] = 0
		#BU
		elif a[2] == ['b', 'r']:
			state[2] = 9
			state[2 + 20] = 0
		#LU
		elif a[3] == ['b', 'r']:
			state[3] = 9
			state[3 + 20] = 0
		#FD
		elif a[4] == ['b', 'r']:
			state[4] = 9
			state[4 + 20] = 0
		#RD
		elif a[5] == ['b', 'r']:
			state[5] = 9
			state[5 + 20] = 0
		#BD
		elif a[6] == ['b', 'r']:
			state[6] = 9
			state[6 + 20] = 0
		#LD
		elif a[7] == ['b', 'r']:
			state[7] = 9
			state[7 + 20] = 0
		#FR
		elif a[8] == ['b', 'r']:
			state[8] = 9
			state[8 + 20] = 1
		#FL
		elif a[9] == ['b', 'r']:
			state[9] = 9
			state[9 + 20] = 1
		#BR
		elif a[10] == ['b', 'r']:
			state[10] = 9
			state[10 + 20] = 1
		#BL
		elif a[11] == ['b', 'r']:
			state[11] = 9
			state[11 + 20] = 1
		
		#######################
			
		#FU
		if a[0] == ['o', 'g']:
			state[0] = 10
			state[0 + 20] = 1
		#RU
		elif a[1] == ['o','g']:
			state[1] = 10
			state[1 + 20] = 1
		#BU
		elif a[2] == ['o','g']:
			state[2] = 10
			state[2 + 20] = 1
		#LU
		elif a[3] == ['o','g']:
			state[3] = 10
			state[3 + 20] = 1
		#FD
		elif a[4] == ['o','g']:
			state[4] = 10
			state[4 + 20] = 1
		#RD
		elif a[5] == ['o','g']:
			state[5] = 10
			state[5 + 20] = 1
		#BD
		elif a[6] == ['o','g']:
			state[6] = 10
			state[6 + 20] = 1
		#LD
		elif a[7] == ['o','g']:
			state[7] = 10
			state[7 + 20] = 1
		#FR
		elif a[8] == ['o','g']:
			state[8] = 10
			state[8 + 20] = 0
		#FL
		elif a[9] == ['o','g']:
			state[9] = 10
			state[9 + 20] = 0
		#BR
		elif a[10] == ['o','g']:
			state[10] = 10
			state[10 + 20] = 0
		#BL
		elif a[11] == ['o','g']:
			state[11] = 10
			state[11 + 20] = 0
		#FU
		if a[0] == ['g', 'o']:
			state[0] = 10
			state[0 + 20] = 0
		#RU
		elif a[1] == ['g', 'o']:
			state[1] = 10
			state[1 + 20] = 0
		#BU
		elif a[2] == ['g', 'o']:
			state[2] = 10
			state[2 + 20] = 0
		#LU
		elif a[3] == ['g', 'o']:
			state[3] = 10
			state[3 + 20] = 0
		#FD
		elif a[4] == ['g', 'o']:
			state[4] = 10
			state[4 + 20] = 0
		#RD
		elif a[5] == ['g', 'o']:
			state[5] = 10
			state[5 + 20] = 0
		#BD
		elif a[6] == ['g', 'o']:
			state[6] = 10
			state[6 + 20] = 0
		#LD
		elif a[7] == ['g', 'o']:
			state[7] = 10
			state[7 + 20] = 0
		#FR
		elif a[8] == ['g', 'o']:
			state[8] = 10
			state[8 + 20] = 1
		#FL
		elif a[9] == ['g', 'o']:
			state[9] = 10
			state[9 + 20] = 1
		#BR
		elif a[10] == ['g', 'o']:
			state[10] = 10
			state[10 + 20] = 1
		#BL
		elif a[11] == ['g', 'o']:
			state[11] = 10
			state[11 + 20] = 1
		
		#######################
			
		#FU
		if a[0] == ['o', 'b']:
			state[0] = 11
			state[0 + 20] = 1
		#RU
		elif a[1] == ['o','b']:
			state[1] = 11
			state[1 + 20] = 1
		#BU
		elif a[2] == ['o','b']:
			state[2] = 11
			state[2 + 20] = 1
		#LU
		elif a[3] == ['o','b']:
			state[3] = 11
			state[3 + 20] = 1
		#FD
		elif a[4] == ['o','b']:
			state[4] = 11
			state[4 + 20] = 1
		#RD
		elif a[5] == ['o','b']:
			state[5] = 11
			state[5 + 20] = 1
		#BD
		elif a[6] == ['o','b']:
			state[6] = 11
			state[6 + 20] = 1
		#LD
		elif a[7] == ['o','b']:
			state[7] = 11
			state[7 + 20] = 1
		#FR
		elif a[8] == ['o','b']:
			state[8] = 11
			state[8 + 20] = 0
		#FL
		elif a[9] == ['o','b']:
			state[9] = 11
			state[9 + 20] = 0
		#BR
		elif a[10] == ['o','b']:
			state[10] = 11
			state[10 + 20] = 0
		#BL
		elif a[11] == ['o','b']:
			state[11] = 11
			state[11 + 20] = 0
		#FU
		if a[0] == ['b', 'o']:
			state[0] = 11
			state[0 + 20] = 0
		#RU
		elif a[1] == ['b', 'o']:
			state[1] = 11
			state[1 + 20] = 0
		#BU
		elif a[2] == ['b', 'o']:
			state[2] = 11
			state[2 + 20] = 0
		#LU
		elif a[3] == ['b', 'o']:
			state[3] = 11
			state[3 + 20] = 0
		#FD
		elif a[4] == ['b', 'o']:
			state[4] = 11
			state[4 + 20] = 0
		#RD
		elif a[5] == ['b', 'o']:
			state[5] = 11
			state[5 + 20] = 0
		#BD
		elif a[6] == ['b', 'o']:
			state[6] = 11
			state[6 + 20] = 0
		#LD
		elif a[7] == ['b', 'o']:
			state[7] = 11
			state[7 + 20] = 0
		#FR
		elif a[8] == ['b', 'o']:
			state[8] = 11
			state[8 + 20] = 1
		#FL
		elif a[9] == ['b', 'o']:
			state[9] = 11
			state[9 + 20] = 1
		#BR
		elif a[10] == ['b', 'o']:
			state[10] = 11
			state[10 + 20] = 1
		#BL
		elif a[11] == ['b', 'o']:
			state[11] = 11
			state[11 + 20] = 1
		
		"""
		FRU= ['r','g','y']
		BRU= ['o','g','y']
		BLU= ['o','b','y']
		FLU= ['r','b','y']
		FRD= ['r','g','w']
		BRD= ['o','g','w']
		BLD= ['o','b','w']
		FLD= ['r','b','w']
		
		print(self.corners)
		b = 12
		for c in self.corners:
			if all(value in FRU for value in c):
				state[b] =
			if all(value in BRU for value in c):
				state[b] = 13
			if all(value in BLU for value in c):
				state[b] = 14
			if all(value in FLU for value in c):
				state[b] = 15
			if all(value in FRD for value in c):
				state[b] = 16
			if all(value in FLD for value in c):
				state[b] = 17
			if all(value in BLD for value in c):
				state[b] = 18
			if all(value in BRD for value in c):
				state[b] = 19
			b = b + 1
		"""
		
		
		if self.corner[0] == ['r','g','y']:
			state[12] = 12
			state[12 + 20] = 0
		elif self.corner[0] == ['y','r','g']:
			state[12] = 12
			state[12 + 20] = 1
		elif self.corner[0] == ['g','y','r']:
			state[12] = 12
			state[12 + 20] = 2
		elif self.corner[0] == ['g','o','y']:
			state[12] = 13
			state[12 + 20] = 0
		elif self.corner[0] == ['y','g','o']:
			state[12] = 13
			state[12 + 20] = 1
		elif self.corner[0] == ['o','y','g']:
			state[12] = 13
			state[12 + 20] = 2
		elif self.corner[0] == ['o','b','y']:
			state[12] = 14
			state[12 + 20] = 0
		elif self.corner[0] == ['y','o','b']:
			state[12] = 14
			state[12 + 20] = 1
		elif self.corner[0] == ['b','y','o']:
			state[12] = 14
			state[12 + 20] = 2
		elif self.corner[0] == ['b','r','y']:
			state[12] = 15
			state[12 + 20] = 0
		elif self.corner[0] == ['y','b','r']:
			state[12] = 15
			state[12 + 20] = 1
		elif self.corner[0] == ['r','y','b']:
			state[12] = 15
			state[12 + 20] = 2
		elif self.corner[0] == ['w','g','r']:
			state[12] = 16
			state[12 + 20] = 1
		elif self.corner[0] == ['r','w','g']:
			state[12] = 16
			state[12 + 20] = 2
		elif self.corner[0] == ['g','r','w']:
			state[12] = 16
			state[12 + 20] = 0
		elif self.corner[0] == ['w','r','b']:
			state[12] = 17
			state[12 + 20] = 1
		elif self.corner[0] == ['b','w','r']:
			state[12] = 17
			state[12 + 20] = 2
		elif self.corner[0] == ['r','b','w']:
			state[12] = 17
			state[12 + 20] = 0
		elif self.corner[0] == ['w','b','o']:
			state[12] = 18
			state[12 + 20] = 1
		elif self.corner[0] == ['o','w','b']:
			state[12] = 18
			state[12 + 20] = 2
		elif self.corner[0] == ['b','o','w']:
			state[12] = 18
			state[12 + 20] = 0
		elif self.corner[0] == ['w','o','g']:
			state[12] = 19
			state[12 + 20] = 1
		elif self.corner[0] == ['g','w','o']:
			state[12] = 19
			state[12 + 20] = 2
		elif self.corner[0] == ['o','g','w']:
			state[12] = 19
			state[12 + 20] = 0
		
		#####################################
		
		if self.corner[1] == ['r','g','y']:
			state[13] = 12
			state[13 + 20] = 0
		elif self.corner[1] == ['y','r','g']:
			state[13] = 12
			state[13 + 20] = 1
		elif self.corner[1] == ['g','y','r']:
			state[13] = 12
			state[13 + 20] = 2
		elif self.corner[1] == ['g','o','y']:
			state[13] = 13
			state[13 + 20] = 0
		elif self.corner[1] == ['y','g','o']:
			state[13] = 13
			state[13 + 20] = 1
		elif self.corner[1] == ['o','y','g']:
			state[13] = 13
			state[13 + 20] = 2
		elif self.corner[1] == ['o','b','y']:
			state[13] = 14
			state[13 + 20] = 0
		elif self.corner[1] == ['y','o','b']:
			state[13] = 14
			state[13 + 20] = 1
		elif self.corner[1] == ['b','y','o']:
			state[13] = 14
			state[13 + 20] = 2
		elif self.corner[1] == ['b','r','y']:
			state[13] = 15
			state[13 + 20] = 0
		elif self.corner[1] == ['y','b','r']:
			state[13] = 15
			state[13 + 20] = 1
		elif self.corner[1] == ['r','y','b']:
			state[13] = 15
			state[13 + 20] = 2
		elif self.corner[1] == ['w','g','r']:
			state[13] = 16
			state[13 + 20] = 1
		elif self.corner[1] == ['r','w','g']:
			state[13] = 16
			state[13 + 20] = 2
		elif self.corner[1] == ['g','r','w']:
			state[13] = 16
			state[13 + 20] = 0
		elif self.corner[1] == ['w','r','b']:
			state[13] = 17
			state[13 + 20] = 1
		elif self.corner[1] == ['b','w','r']:
			state[13] = 17
			state[13 + 20] = 2
		elif self.corner[1] == ['r','b','w']:
			state[13] = 17
			state[13 + 20] = 0
		elif self.corner[1] == ['w','b','o']:
			state[13] = 18
			state[13 + 20] = 1
		elif self.corner[1] == ['o','w','b']:
			state[13] = 18
			state[13 + 20] = 2
		elif self.corner[1] == ['b','o','w']:
			state[13] = 18
			state[13 + 20] = 0
		elif self.corner[1] == ['w','o','g']:
			state[13] = 19
			state[13 + 20] = 1
		elif self.corner[1] == ['g','w','o']:
			state[13] = 19
			state[13 + 20] = 2
		elif self.corner[1] == ['o','g','w']:
			state[13] = 19
			state[13 + 20] = 0
			
		#####################################
		
		if self.corner[2] == ['r','g','y']:
			state[14] = 12
			state[14 + 20] = 0
		elif self.corner[2] == ['y','r','g']:
			state[14] = 12
			state[14 + 20] = 1
		elif self.corner[2] == ['g','y','r']:
			state[14] = 12
			state[14 + 20] = 2
		elif self.corner[2] == ['g','o','y']:
			state[14] = 13
			state[14 + 20] = 0
		elif self.corner[2] == ['y','g','o']:
			state[14] = 13
			state[14 + 20] = 1
		elif self.corner[2] == ['o','y','g']:
			state[14] = 13
			state[14 + 20] = 2
		elif self.corner[2] == ['o','b','y']:
			state[14] = 14
			state[14 + 20] = 0
		elif self.corner[2] == ['y','o','b']:
			state[14] = 14
			state[14 + 20] = 1
		elif self.corner[2] == ['b','y','o']:
			state[14] = 14
			state[14 + 20] = 2
		elif self.corner[2] == ['b','r','y']:
			state[14] = 15
			state[14 + 20] = 0
		elif self.corner[2] == ['y','b','r']:
			state[14] = 15
			state[14 + 20] = 1
		elif self.corner[2] == ['r','y','b']:
			state[14] = 15
			state[14 + 20] = 2
		elif self.corner[2] == ['w','g','r']:
			state[14] = 16
			state[14 + 20] = 1
		elif self.corner[2] == ['r','w','g']:
			state[14] = 16
			state[14 + 20] = 2
		elif self.corner[2] == ['g','r','w']:
			state[14] = 16
			state[14 + 20] = 0
		elif self.corner[2] == ['w','r','b']:
			state[14] = 17
			state[14 + 20] = 1
		elif self.corner[2] == ['b','w','r']:
			state[14] = 17
			state[14 + 20] = 2
		elif self.corner[2] == ['r','b','w']:
			state[14] = 17
			state[14 + 20] = 0
		elif self.corner[2] == ['w','b','o']:
			state[14] = 18
			state[14 + 20] = 1
		elif self.corner[2] == ['o','w','b']:
			state[14] = 18
			state[14 + 20] = 2
		elif self.corner[2] == ['b','o','w']:
			state[14] = 18
			state[14 + 20] = 0
		elif self.corner[2] == ['w','o','g']:
			state[14] = 19
			state[14 + 20] = 1
		elif self.corner[2] == ['g','w','o']:
			state[14] = 19
			state[14 + 20] = 2
		elif self.corner[1] == ['o','g','w']:
			state[14] = 19
			state[14 + 20] = 0
			
		#####################################
		
		if self.corner[3] == ['r','g','y']:
			state[15] = 12
			state[15 + 20] = 0
		elif self.corner[3] == ['y','r','g']:
			state[15] = 12
			state[15 + 20] = 1
		elif self.corner[3] == ['g','y','r']:
			state[15] = 12
			state[15 + 20] = 2
		elif self.corner[3] == ['g','o','y']:
			state[15] = 13
			state[15 + 20] = 0
		elif self.corner[3] == ['y','g','o']:
			state[15] = 13
			state[15 + 20] = 1
		elif self.corner[3] == ['o','y','g']:
			state[15] = 13
			state[15 + 20] = 2
		elif self.corner[3] == ['o','b','y']:
			state[15] = 14
			state[15 + 20] = 0
		elif self.corner[3] == ['y','o','b']:
			state[15] = 14
			state[15 + 20] = 1
		elif self.corner[3] == ['b','y','o']:
			state[15] = 14
			state[15 + 20] = 2
		elif self.corner[3] == ['b','r','y']:
			state[15] = 15
			state[15 + 20] = 0
		elif self.corner[3] == ['y','b','r']:
			state[15] = 15
			state[15 + 20] = 1
		elif self.corner[3] == ['r','y','b']:
			state[15] = 15
			state[15 + 20] = 2
		elif self.corner[3] == ['w','g','r']:
			state[15] = 16
			state[15 + 20] = 1
		elif self.corner[3] == ['r','w','g']:
			state[15] = 16
			state[15 + 20] = 2
		elif self.corner[3] == ['g','r','w']:
			state[15] = 16
			state[15 + 20] = 0
		elif self.corner[3] == ['w','r','b']:
			state[15] = 17
			state[15 + 20] = 1
		elif self.corner[3] == ['b','w','r']:
			state[15] = 17
			state[15 + 20] = 2
		elif self.corner[3] == ['r','b','w']:
			state[15] = 17
			state[15 + 20] = 0
		elif self.corner[3] == ['w','b','o']:
			state[15] = 18
			state[15 + 20] = 1
		elif self.corner[3] == ['o','w','b']:
			state[15] = 18
			state[15 + 20] = 2
		elif self.corner[3] == ['b','o','w']:
			state[15] = 18
			state[15 + 20] = 0
		elif self.corner[3] == ['w','o','g']:
			state[15] = 19
			state[15 + 20] = 1
		elif self.corner[3] == ['g','w','o']:
			state[15] = 19
			state[15 + 20] = 2
		elif self.corner[3] == ['o','g','w']:
			state[15] = 19
			state[15 + 20] = 0
			
		#####################################
		
		if self.corner[4] == ['r','g','y']:
			state[16] = 12
			state[16 + 20] = 2
		elif self.corner[4] == ['y','r','g']:
			state[16] = 12
			state[16 + 20] = 0
		elif self.corner[4] == ['g','y','r']:
			state[16] = 12
			state[16 + 20] = 1
		elif self.corner[4] == ['g','o','y']:
			state[16] = 13
			state[16 + 20] = 2
		elif self.corner[4] == ['y','g','o']:
			state[16] = 13
			state[16 + 20] = 0
		elif self.corner[4] == ['o','y','g']:
			state[16] = 13
			state[16 + 20] = 1
		elif self.corner[4] == ['o','b','y']:
			state[16] = 14
			state[16 + 20] = 2
		elif self.corner[4] == ['y','o','b']:
			state[16] = 14
			state[16 + 20] = 0
		elif self.corner[4] == ['b','y','o']:
			state[16] = 14
			state[16 + 20] = 1
		elif self.corner[4] == ['b','r','y']:
			state[16] = 15
			state[16 + 20] = 2
		elif self.corner[4] == ['y','b','r']:
			state[16] = 15
			state[16 + 20] = 0
		elif self.corner[4] == ['r','y','b']:
			state[16] = 15
			state[16 + 20] = 1
		elif self.corner[4] == ['w','g','r']:
			state[16] = 16
			state[16 + 20] = 0
		elif self.corner[4] == ['r','w','g']:
			state[16] = 16
			state[16 + 20] = 1
		elif self.corner[4] == ['g','r','w']:
			state[16] = 16
			state[16 + 20] = 2
		elif self.corner[4] == ['w','r','b']:
			state[16] = 17
			state[16 + 20] = 0
		elif self.corner[4] == ['b','w','r']:
			state[16] = 17
			state[16 + 20] = 1
		elif self.corner[4] == ['r','b','w']:
			state[16] = 17
			state[16 + 20] = 2
		elif self.corner[4] == ['w','b','o']:
			state[16] = 18
			state[16 + 20] = 0
		elif self.corner[4] == ['o','w','b']:
			state[16] = 18
			state[16 + 20] = 1
		elif self.corner[4] == ['b','o','w']:
			state[16] = 18
			state[16 + 20] = 2
		elif self.corner[4] == ['w','o','g']:
			state[16] = 19
			state[16 + 20] = 0
		elif self.corner[4] == ['g','w','o']:
			state[16] = 19
			state[16 + 20] = 1
		elif self.corner[4] == ['o','g','w']:
			state[16] = 19
			state[16 + 20] = 2
			
		#####################################
		
		if self.corner[5] == ['r','g','y']:
			state[17] = 12
			state[17 + 20] = 2
		elif self.corner[5] == ['y','r','g']:
			state[17] = 12
			state[17 + 20] = 0
		elif self.corner[5] == ['g','y','r']:
			state[17] = 12
			state[17 + 20] = 1
		elif self.corner[5] == ['g','o','y']:
			state[17] = 13
			state[17 + 20] = 2
		elif self.corner[5] == ['y','g','o']:
			state[17] = 13
			state[17 + 20] = 0
		elif self.corner[5] == ['o','y','g']:
			state[17] = 13
			state[17 + 20] = 1
		elif self.corner[5] == ['o','b','y']:
			state[17] = 14
			state[17 + 20] = 2
		elif self.corner[5] == ['y','o','b']:
			state[17] = 14
			state[17 + 20] = 0
		elif self.corner[5] == ['b','y','o']:
			state[17] = 14
			state[17 + 20] = 1
		elif self.corner[5] == ['b','r','y']:
			state[17] = 15
			state[17 + 20] = 2
		elif self.corner[5] == ['y','b','r']:
			state[17] = 15
			state[17 + 20] = 0
		elif self.corner[5] == ['r','y','b']:
			state[17] = 15
			state[17 + 20] = 1
		elif self.corner[5] == ['w','g','r']:
			state[17] = 16
			state[17 + 20] = 0
		elif self.corner[5] == ['r','w','g']:
			state[17] = 16
			state[17 + 20] = 1
		elif self.corner[5] == ['g','r','w']:
			state[17] = 16
			state[17 + 20] = 2
		elif self.corner[5] == ['w','r','b']:
			state[17] = 17
			state[17 + 20] = 0
		elif self.corner[5] == ['b','w','r']:
			state[17] = 17
			state[17 + 20] = 1
		elif self.corner[5] == ['r','b','w']:
			state[17] = 17
			state[17 + 20] = 2
		elif self.corner[5] == ['w','b','o']:
			state[17] = 18
			state[17 + 20] = 0
		elif self.corner[5] == ['o','w','b']:
			state[17] = 18
			state[17 + 20] = 1
		elif self.corner[5] == ['b','o','w']:
			state[17] = 18
			state[17 + 20] = 2
		elif self.corner[5] == ['w','o','g']:
			state[17] = 19
			state[17 + 20] = 0
		elif self.corner[5] == ['g','w','o']:
			state[17] = 19
			state[17 + 20] = 1
		elif self.corner[5] == ['o','g','w']:
			state[17] = 19
			state[17 + 20] = 2
			
		#####################################
		
		if self.corner[6] == ['r','g','y']:
			state[18] = 12
			state[18 + 20] = 2
		elif self.corner[6] == ['y','r','g']:
			state[18] = 12
			state[18 + 20] = 0
		elif self.corner[6] == ['g','y','r']:
			state[18] = 12
			state[18 + 20] = 1
		elif self.corner[6] == ['g','o','y']:
			state[18] = 13
			state[18 + 20] = 2
		elif self.corner[6] == ['y','g','o']:
			state[18] = 13
			state[18 + 20] = 0
		elif self.corner[6] == ['o','y','g']:
			state[18] = 13
			state[18 + 20] = 1
		elif self.corner[6] == ['o','b','y']:
			state[18] = 14
			state[18 + 20] = 2
		elif self.corner[6] == ['y','o','b']:
			state[18] = 14
			state[18 + 20] = 0
		elif self.corner[6] == ['b','y','o']:
			state[18] = 14
			state[18 + 20] = 1
		elif self.corner[6] == ['b','r','y']:
			state[18] = 15
			state[18 + 20] = 2
		elif self.corner[6] == ['y','b','r']:
			state[18] = 15
			state[18 + 20] = 0
		elif self.corner[6] == ['r','y','b']:
			state[18] = 15
			state[18 + 20] = 1
		elif self.corner[6] == ['w','g','r']:
			state[18] = 16
			state[18 + 20] = 0
		elif self.corner[6] == ['r','w','g']:
			state[18] = 16
			state[18 + 20] = 1
		elif self.corner[6] == ['g','r','w']:
			state[18] = 16
			state[18 + 20] = 2
		elif self.corner[6] == ['w','r','b']:
			state[18] = 17
			state[18 + 20] = 0
		elif self.corner[6] == ['b','w','r']:
			state[18] = 17
			state[18 + 20] = 1
		elif self.corner[6] == ['r','b','w']:
			state[18] = 17
			state[18 + 20] = 2
		elif self.corner[6] == ['w','b','o']:
			state[18] = 18
			state[18 + 20] = 0
		elif self.corner[6] == ['o','w','b']:
			state[18] = 18
			state[18 + 20] = 1
		elif self.corner[6] == ['b','o','w']:
			state[18] = 18
			state[18 + 20] = 2
		elif self.corner[6] == ['w','o','g']:
			state[18] = 19
			state[18 + 20] = 0
		elif self.corner[6] == ['g','w','o']:
			state[18] = 19
			state[18 + 20] = 1
		elif self.corner[6] == ['o','g','w']:
			state[18] = 19
			state[18 + 20] = 2
			
		#####################################
		
		if self.corner[7] == ['r','g','y']:
			state[19] = 12
			state[19 + 20] = 2
		elif self.corner[7] == ['y','r','g']:
			state[19] = 12
			state[19 + 20] = 0
		elif self.corner[7] == ['g','y','r']:
			state[19] = 12
			state[19 + 20] = 1
		elif self.corner[7] == ['g','o','y']:
			state[19] = 13
			state[19 + 20] = 2
		elif self.corner[7] == ['y','g','o']:
			state[19] = 13
			state[19 + 20] = 0
		elif self.corner[7] == ['o','y','g']:
			state[19] = 13
			state[19 + 20] = 1
		elif self.corner[7] == ['o','b','y']:
			state[19] = 14
			state[19 + 20] = 2
		elif self.corner[7] == ['y','o','b']:
			state[19] = 14
			state[19 + 20] = 0
		elif self.corner[7] == ['b','y','o']:
			state[19] = 14
			state[19 + 20] = 1
		elif self.corner[7] == ['b','r','y']:
			state[19] = 15
			state[19 + 20] = 2
		elif self.corner[7] == ['y','b','r']:
			state[19] = 15
			state[19 + 20] = 0
		elif self.corner[7] == ['r','y','b']:
			state[19] = 15
			state[19 + 20] = 1
		elif self.corner[7] == ['w','g','r']:
			state[19] = 16
			state[19 + 20] = 0
		elif self.corner[7] == ['r','w','g']:
			state[19] = 16
			state[19 + 20] = 1
		elif self.corner[7] == ['g','r','w']:
			state[19] = 16
			state[19 + 20] = 2
		elif self.corner[7] == ['w','r','b']:
			state[19] = 17
			state[19 + 20] = 0
		elif self.corner[7] == ['b','w','r']:
			state[19] = 17
			state[19 + 20] = 1
		elif self.corner[7] == ['r','b','w']:
			state[19] = 17
			state[19 + 20] = 2
		elif self.corner[7] == ['w','b','o']:
			state[19] = 18
			state[19 + 20] = 0
		elif self.corner[7] == ['o','w','b']:
			state[19] = 18
			state[19 + 20] = 1
		elif self.corner[7] == ['b','o','w']:
			state[19] = 18
			state[19 + 20] = 2
		elif self.corner[7] == ['w','o','g']:
			state[19] = 19
			state[19 + 20] = 0
		elif self.corner[7] == ['g','w','o']:
			state[19] = 19
			state[19 + 20] = 1
		elif self.corner[7] == ['o','g','w']:
			state[19] = 19
			state[19 + 20] = 2
		
		return state

def main():
	cube = RubiksCube("")
	cube.CW_Front()
	print(cube.stringify())

if __name__ == '__main__':
	main()
