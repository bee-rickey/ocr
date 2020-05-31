outputFile = open("output.txt", "r")
dataDictionary = {}
dataDictionaryArray = []

for index, line in enumerate(outputFile):
	if line in dataDictionary:
		continue
	dataDictionary[line] = line
	dataDictionaryArray.append(dataDictionary)


for key, data in dataDictionary.items():
	print(data, end = "")
