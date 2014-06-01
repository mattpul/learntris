#!/usr/bin/env python

import sys

class learntris():
	def __init__(self):	
		self.score = 0
		self.linescleared = 0
		self.selectedshape = ''
		self.shapedata = {
		'I' : [[4,0],['. . . .','c c c c','. . . .','. . . .']] , 
		'O' : [[5,0],['y y','y y']] , 
		'Z' : [[4,0],['r r .','. r r','. . .']] , 
		'S' : [[4,0],['. g g','g g .','. . .']] , 
		'J' : [[4,0],['b . .','b b b','. . .']] , 
		'L' : [[4,0],['. . o','o o o','. . .']] , 
		'T' : [[4,0],['. m .','m m m','. . .']] 
		}
		self.previousmatrixstate = self.emptymatrix()
		self.matrixstate = self.emptymatrix()
		self.xpos = 0
		self.ypos = 0
		self.rm_coordinates = []
	 
	def emptymatrix(self):
		emptymatrix = []
		for row in range(22):
			emptymatrix.append('. . . . . . . . . .'.split(' '))
		return emptymatrix
	
	def separatematrix(self, matrix2split):
		separatedmatrix = []
		for row in matrix2split:
			separatedmatrix.append(row.split(' '))
		return separatedmatrix
	
	def mergematrix(self, matrix2merge):
		mergedmatrix = []
		for row in matrix2merge:
			mergedmatrix.append(' '.join(row))
		return mergedmatrix
	
	def modifymatrix(self, capitalisation = False): # Append Tetramino to matrix.
		self.rmcord()
		for row_number, row in enumerate(self.separatematrix(self.selectedshape)):
				for column_number, column in enumerate(row):
					if row_number + self.ypos < 22 and 0 <= column_number + self.xpos - 1 < 10 and [row_number ,column_number] not in self.rm_coordinates:
						if capitalisation:
							self.matrixstate[row_number + self.ypos][column_number + self.xpos - 1] = self.separatematrix(self.cap(self.selectedshape))[row_number][column_number]
						else:	
							self.matrixstate[row_number + self.ypos][column_number + self.xpos - 1] = self.separatematrix(self.selectedshape)[row_number][column_number]

	def scantetramino(self,orientation): # Value = 0 unecessary in function put in body of movement if statements.
		storage = {}
		for i in range(len(self.selectedshape)):
			if orientation == 'V':
				storage[str(i)] = [row[i] for row in self.separatematrix(self.selectedshape)]
			if orientation == 'H':	
				storage[str(i)] = self.separatematrix(self.selectedshape)[i]
		return storage
		
	def cap(self, d): # Refactor code. This is not repeated therefore not necessary to define as a function.
		b = [x.upper() for x in d]
		return b
			
	def rmcord(self):
		self.rm_coordinates = []
		for row_number, row in enumerate(self.separatematrix(self.selectedshape)):
			for column_number, column in enumerate(row):
				if column == '.':
					self.rm_coordinates.append([row_number,column_number])
							
	def run(self, capturedinput):
		
		if capturedinput not in ['?n','?s']:
			capturedinput = ' '.join(capturedinput)
		
		for command in capturedinput.split(' '):
			
			if command == 'q': # Exit program.
				sys.exit()
			
			elif command == 'p': # Print the current state of the matrix..
				for row in self.mergematrix(self.matrixstate): # Merge matrix. Print modified matrix.
					print(row)
			
			elif command == 'g':
				capturedmatrix = []
				for i in range(22):
					capturedmatrix.append(raw_input())
				self.matrixstate = self.separatematrix(capturedmatrix)
			
			elif command == 'c': # Clear matrix.
				self.matrixstate = self.emptymatrix()
				self.score = 0
				self.linescleared = 0
			
			elif command == 's':
				# Clear a line if it does not contain any empty blocks.	If line was cleared, increment lines cleared.
				for position,recorditem in enumerate(self.matrixstate):
					if '.' not in recorditem:
						self.matrixstate[position] = '. . . . . . . . . .'.split(' ')
						self.linescleared += 1				
				self.score += 100
			
			elif command == '?s': # Print current score.
				print(self.score) 
			
			elif command == '?n': # Print the number of lines cleared.
				print(self.linescleared)
			
			elif command == ';':
				sys.stdout.write('\n')
			
			elif command in ['I','O','Z','S','J','L','T']:
				self.selectedshape = self.shapedata[command][1]
				self.xpos = self.shapedata[command][0][0]
				self.ypos = self.shapedata[command][0][1]
			
			elif command == 't': # Prints the selected tetramino.
				for row in self.selectedshape:
					print(row) 	
			
			elif command == ')': # Rotate selected tetramino clockwise.
				clonedmatrix = self.separatematrix(self.selectedshape)
				tempmatrix = self.separatematrix(self.selectedshape)
				for row_number, row in enumerate(clonedmatrix):
					for column_number, column in enumerate(row):
						tempmatrix[column_number][(len(clonedmatrix)-1) - row_number] = clonedmatrix[row_number][column_number]
				self.selectedshape = self.mergematrix(tempmatrix)
			
			elif command == '(': # Rotate selected tetramino counterclockwise.
				clonedmatrix = self.separatematrix(self.selectedshape)
				tempmatrix = self.separatematrix(self.selectedshape)
				for row_number, row in enumerate(clonedmatrix):
					for column_number,column in enumerate(row):
						tempmatrix[(len(clonedmatrix)-1) - column_number][row_number] = clonedmatrix[row_number][column_number]
				self.selectedshape = self.mergematrix(tempmatrix)
			
			elif command == 'P': # Spawn matrix. Print matrix with active Tetramino.
				self.modifymatrix(True)
				for i in self.mergematrix(self.matrixstate):
					print i
			
			elif command == '<': # Move active Tetramino left by one step.
				
				vertical = self.scantetramino('V')
				
				value = 0
				for i in range(len(vertical)):
					if vertical[str(i)] == ['.' for row in self.selectedshape]:
						value += 1
					else:
						break
				
				position = self.xpos - 1
				maxposition = 1 - value
				if position <= maxposition:
					self.xpos = maxposition
				elif position > maxposition:
					self.xpos = position
			
			elif command == '>': # Move active Tetramino right by one step.
				
				vertical = self.scantetramino('V')
				
				value =0
				for i in reversed(range(len(vertical))):
					if vertical[str(i)] == ['.' for row in self.selectedshape]:
						value += 1
					else:
						break

				position = self.xpos + 1
				blocklength = len(self.separatematrix(self.selectedshape)[0])		
				maxposition = 11 - blocklength + value
				if position <= maxposition:
					self.xpos = self.xpos + 1
				elif position >= maxposition:
					self.xpos = maxposition

			elif command == 'v': # Move active Tetramino down by one step.

				horizontal = self.scantetramino('H')

				value = 0
				for i in reversed(range(len(horizontal))):
					if horizontal[str(i)] == ['.' for row in self.selectedshape]:
						value += 1
					else:
						break
						
				position = self.ypos + 1
				blocklength = len(self.separatematrix(self.selectedshape)[0])
				maxposition = 22 - blocklength + value
				
				if self.ypos + blocklength < 22:
					linebelowblock = self.separatematrix(self.matrixstate[self.ypos	+ blocklength - value + 1])
					bottomlineofblock = self.separatematrix(self.selectedshape)[blocklength - value - 1]
				if position <= maxposition:
					self.ypos += 1
				elif position > maxposition:
					self.ypos = maxposition		
			
			elif command == 'V': # Drop active Tetramino to the bottom of the matrix.
				
				horizontal = self.scantetramino('H')
				
				value = 0
				for i in reversed(range(len(horizontal))):
					if horizontal[str(i)] == ['.' for row in self.selectedshape]:
						value += 1
					else:
						break
				
				position = self.ypos + 1
				blocklength = len(self.separatematrix(self.selectedshape)[0])
				maxposition = 22 - blocklength + value
				self.ypos = maxposition
				
				self.matrixstate = self.emptymatrix() ################
				
				self.modifymatrix(False)
				
			elif command == '@':
				print('Learntris (c) 1992 Tetraminex, Inc.')
				print('Press start button to begin.')
			
			elif command == '!': # Pause.
				print('Paused')
				print('Press start button to continue.')

def main():
	app = learntris()
	while True:
		app.run(raw_input())

if __name__ == "__main__":
	main()
