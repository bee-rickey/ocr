testingNumbersFile = open("bounds.txt", "r")

dataDictionary = {}

dataDictionaryArray = []

class cellItem:
	def __init__(self, value, x, y, col, row, index):
		self.value = value
		self.x = x
		self.y = y
		self.col = col
		self.row = row
		self.index = index

xInterval = 0
yInterval = 0
maxIndex = 0
for index, line in enumerate(testingNumbersFile):
	lineArray = line.split('|')
	lowerLeft = []
	lowerRight = []
	upperRight = []
	upperLeft = []

	value = lineArray[0]
	lowerLeft = lineArray[2].split(',')
	lowerRight = lineArray[3].split(',')
	upperRight = lineArray[4].split(',')
	upperLeft = lineArray[5].split(',')

#Get the mid point of the bound where the text matches
	xMean = (int(lowerLeft[0]) + int(lowerRight[0]))/2
	yMean = (int(lowerLeft[1]) + int(upperLeft[1]))/2

#Use these intervals as a possible error in mid point calculation
	xInterval = (int(lowerRight[0]) - int(lowerLeft[0]))/2 if (int(lowerRight[0]) - int(lowerLeft[0]))/2 > xInterval else xInterval
	yInterval = (int(upperLeft[1]) - int(lowerLeft[1]))/2 if (int(upperLeft[1]) - int(lowerLeft[1]))/2 > yInterval else yInterval

	maxIndex = index + 1 

	dataDictionaryArray.append(cellItem(value, xMean, yMean, 0, 0, index + 1))

for rowIndex, currentCell in enumerate(dataDictionaryArray):           
	if currentCell.row == 0:
		currentCell.row = rowIndex + 1
	for colIndex, restOfTheCells in enumerate(dataDictionaryArray):
		if currentCell.col == 0:
			currentCell.col = colIndex + 1
		if restOfTheCells.index == currentCell.index:
			continue

		yUpperBound = currentCell.y + yInterval
		yLowerBound = currentCell.y - yInterval
#If the y coordinate matches, the texts lie on the same row
		if restOfTheCells.row == 0:
			if yLowerBound <= restOfTheCells.y <= yUpperBound:
				restOfTheCells.row = rowIndex + 1

		xUpperBound = currentCell.x + xInterval
		xLowerBound = currentCell.x - xInterval

#If the x coordinate matches, the texts lie on the same column
		if restOfTheCells.col == 0:
			if xLowerBound <= restOfTheCells.x <= xUpperBound:
				restOfTheCells.col = colIndex + 1
			

	
#Need to figure this printing out <TODO>
for i in range(0, len(dataDictionaryArray)):
	outputString = []
	for cell in dataDictionaryArray:
		if cell.row == i:
			outputString.append(cell)
	outputString.sort(key=lambda x: x.col)

	output = ""
	for value in outputString:
		output += value.value if len(output) == 0 else "," + value.value
	
	print(output)

