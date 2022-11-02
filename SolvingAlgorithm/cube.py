class RubiksCube:
	"""
		Initialize the Rubiks Cube with an array
		
		Input - Array size 54
		Output - None
	"""
	def __init__(self, state):
		self.CurrentArray = [""] * 54
		
		if state == "":
			self.reset()
		else:
			for i in range(54):
				self.CurrentArray[i] = state[i]
		
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
