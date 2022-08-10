from os import listdir

res = []
path = ""
outputPath = "data.sql"

def main():
	files = listdir()

	for file in files:
		if file.endswith(".csv"):
			res.append(file)

	if len(res) > 1:
		print("too many files found. Please include just one CSV file in the same directory as this script.")
		exit(1)
	else:
		path = res[0]
		print("attempting to convert %s" % path)
		f = open(path, 'r')
		convertCSV(f, outputPath)
		print("all done!")
		exit(0)

def convertCSV(inputFile, outputPath): # be sure to pass in a file object and a path which would be a string. 
	count = 1
	id = 0 # unique incremented int
	linecount = sum(1 for line in inputFile)
	print("read ", linecount, " lines")

	line = inputFile.readline()

	#with open(outputPath, 'a') as output:
	output = open(outputPath, 'a')	

	while line:
		print("reading line: %d" % count)
		#special case for first line
		if count == 1:
			columns = line.split(",")
		
			print("columns detected: ")
			print(columns)
		
			count+=1
		# special case for last line
		elif count == linecount:
			values = line.split(",")

			writeClosingBlock(id, values, output)
		
		else:
			values = line.split(",")
			
			print("values detected: ")
			print(values)	

			writeToSQL(id, values, output)

			count+=1
			id += 1
		
		line = inputFile.readline()

def writeToSQL(n, vals, file):
		category = vals[0]
		vocabWord = vals[1]
		data = " ".join(vals[2:])
		print("writing data...")
		file.write("(%d, %s,%s,%s)," % n, category, vocabWord, data)
		
def writeClosingBlock(n, vals, file):
		category = vals[0]
		vocabWord = vals[1]
		data = data[0:-1]
		file.write("(%d, %s,%s,%s);" % n, category, vocabWord, data)
		file.write("\\nCOMMIT;")


if __name__ == "__main__":
	main()
