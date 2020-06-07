import sys

dataDictionary = {}
dataDictionaryArray = []
translationDictionary = {}
xInterval = 0
yThreshold = 0
configxInterval = 0
configyInterval = 0
xThreshold = 0
yInterval = 0
startingText = ""
enableTranslation = False
translationFile = ""



def is_number(s):
	try:            
		int(s)
		return True
	except ValueError:
		return False

class cellItem:
	def __init__(self, value, x, y, col, row, index):
		self.value = value
		self.x = x
		self.y = y
		self.col = col
		self.row = row
		self.index = index

def buildCells():
	global xInterval
	global yInterval
	global startingText
	global yThreshold
	global xThreshold
	global configxInterval
	global configyInterval

	testingNumbersFile = open("bounds.txt", "r")
	for index, line in enumerate(testingNumbersFile):
		lineArray = line.split('|')
		if len(lineArray) != 6:
			continue

		lowerLeft = []
		lowerRight = []
		upperRight = []
		upperLeft = []
		
		if not lineArray[0] or not lineArray[2] or not lineArray[4] or not lineArray[5]:
			continue

		value = lineArray[0]
			
		lowerLeft = lineArray[2].split(',')
		lowerRight = lineArray[3].split(',')
		upperRight = lineArray[4].split(',')
		upperLeft = lineArray[5].split(',')

#Get the mid point of the bound where the text matches
		xMean = (int(lowerLeft[0]) + int(lowerRight[0]))/2
		yMean = (int(lowerLeft[1]) + int(upperLeft[1]))/2

		if value == startingText:
			yThreshold = yMean  
			xThreshold = xMean

#Use these intervals as a possible error in mid point calculation
		xInterval = (int(lowerRight[0]) - int(lowerLeft[0]))/2 if (int(lowerRight[0]) - int(lowerLeft[0]))/2 > xInterval else xInterval
		yInterval = (int(upperLeft[1]) - int(lowerLeft[1]))/2 if (int(upperLeft[1]) - int(lowerLeft[1]))/2 > yInterval else yInterval
		dataDictionaryArray.append(cellItem(value, xMean, yMean, 0, 0, index + 1))

def buildReducedArray():
	tempDictionaryArray = []
	global dataDictionaryArray

#Ignore the texts that lie to the left and top of the threshold text. This improves accuracy of output
	for cell in dataDictionaryArray:
		if cell.y < yThreshold - 10 or cell.x < xThreshold - 30:
			continue
		tempDictionaryArray.append(cell)
	
	dataDictionaryArray = tempDictionaryArray

def assignRowsAndColumns():
	global yInterval
	global xInterval
	global configyInterval
	global configxInterval

	if configxInterval != 0:
		xInterval = configxInterval
	if configyInterval != 0:
		yInterval = configyInterval

	for rowIndex, currentCell in enumerate(dataDictionaryArray):           

		if currentCell.row == 0:
			currentCell.row = rowIndex + 1
		for colIndex, restOfTheCells in enumerate(dataDictionaryArray):

			if currentCell.col == 0:
				currentCell.col = rowIndex + 1
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
					restOfTheCells.col = currentCell.col
			

def buildTranslationDictionary():
	with open(translationFile, "r") as metaFile:
		for line in metaFile:
			if line.startswith('#'):
				continue
			lineArray = line.strip().split(',')
			translationDictionary[lineArray[0].strip()] = lineArray[1].strip()
	

def printOutput():
	outputFile = open('output.txt', 'w') 
	global enableTranslation

	for i in range(0, len(dataDictionaryArray)):
		outputString = []
		for cell in dataDictionaryArray:
			if cell.row == i:
				outputString.append(cell)
		outputString.sort(key=lambda x: x.x)

		output = ""
		previousCol = -999
		mergedValue = ""
#<TODO> column verification has to come in here
#Merge those texts separated by spaces - these have the same column value due to proximity but belong to different objects
		columnList = ""
		for index, value in enumerate(outputString):
			if index == 0:
				mergedValue = value.value 
				previousCol = value.col
				columnList = str(value.col)
				continue

			if value.col == previousCol:
				mergedValue = mergedValue + " " + value.value if len(mergedValue) != 0 else value.value
			else:
				if index == len(outputString) - 1:
					mergedValue = mergedValue + ", " + value.value if len(mergedValue) != 0 else value.value
				output += mergedValue if len(output) == 0 else " , " + mergedValue
				previousCol = value.col
				mergedValue = value.value #+ " ---- " + str(value.col)
				columnList = columnList + ", " + str(value.col) if len(columnList) != 0 else str(value.col)

		if len(output) > 0:
			if enableTranslation == False:
				print("{} | {}".format(output, columnList), file = outputFile)
			else:
				outputArray = output.split(',')
				districtIndex = 0
#If the rows are not numberd, this condition can be skipped. For UP bulletin, this makes sense.
				if(is_number(outputArray[0])):
					districtName = outputArray[1].strip()
					distrinctIndex = 1
				else:
					districtName = outputArray[0].strip()
					distrinctIndex = 0

#Do a lookup for district name, if not found, discard the record and print a message.
				try:
					translatedValue = translationDictionary[districtName]
					outputString = translatedValue 
					for index, value in enumerate(outputArray):
						if index > districtIndex:
							outputString += "," + value.strip()
					print("{} | {}".format(outputString, columnList), file = outputFile)
				except KeyError:
					print(districtName + " , " )  
	outputFile.close()

def parseConfigFile(fileName):
	global startingText
	global enableTranslation
	global translationFile
	global configyInterval
	global configxInterval

	configFile = open(fileName, "r")
	for index, line in enumerate(configFile):
		lineArray = line.split(':')
		if len(lineArray) < 2:
			continue

		key = lineArray[0].strip()
		value = lineArray[1].strip()
	
		if key == "startingText":
			startingText = value
		if key == "enableTranslation":
			enableTranslation = eval(value)
		if key == "translationFile":
			translationFile = value
		if key == "xInterval":
			configxInterval = int(value)
		if key == "yInterval":
			configyInterval = int(value)

def main():
	global startingText
	global enableTranslation
# If given, this text will be used to ignore those items above and to the left of this text. This can cause issues if the text is repeated!
	if len(sys.argv) > 1:
		parseConfigFile(sys.argv[1])
				
	if enableTranslation:
		buildTranslationDictionary()

	buildCells()

	if len(startingText) != 0:
		buildReducedArray()

	assignRowsAndColumns()
	printOutput()

if __name__ == '__main__':
  main()
