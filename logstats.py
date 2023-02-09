#!/usr/bin/python
# you need Levenshtein from https://pypi.org/project/python-Levenshtein/
# and TLSH from https://pypi.org/project/py-tlsh/
# Author : Christophe Briguet

import pickle
import argparse
import tlsh
from Levenshtein import ratio
from Levenshtein import distance

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", dest="file",help="input file name")
parser.add_argument("-o", "--output", dest="output",help="output file name")
parser.add_argument("-m", "--method", dest="method",default="distance",help="method use to evaluate similarity (i.e., distance or tlsh)")
parser.add_argument("-s", "--skip", dest="skip", default="0",type=int,help="Skip n first character from header (0 by default)")
parser.add_argument("-r", "--ratio", dest="ratio", default="	",type=float,help="'distance' or 'distance-ratio' for Levenshtein and 'distance' for TLSH")
parser.add_argument("-p", "--print", dest="sample", default="3",type=int,help="Print n first sample record (3 by default), need verbose mode enabled")
parser.add_argument("-v", "--verbose", dest="verbose",help="Verbose mode",action='store_true')
parser.add_argument("-S", "--stats", dest="stats",help="Statistic mode",action='store_true')

args = parser.parse_args()


msgType={}
msgTypeCounter={}
msgType2ID = {}

verbose= args.verbose
stats=args.stats
# Ideally the ratio threshold should be adjusted according to data set	 	
THR = args.ratio 

sample_size = args.sample

## Open the file with read only permit

f = open(args.file,"r")
## Read the first line 
line = f.readline()
msgType[line] = {}
msgTypeCounter[line] = 1
msgType2ID[line] = 0
currentLineNumber=1
## If the file is not empty keep reading line one at a time
## till the file is empty
line = f.readline()
counter = 0 # used to count the number of unique message associated with a message type
msgType_id = 1 # unique ID for message type

while line:
	# How many lines to analyze?
	if counter >= 50000:
		break
	flag = 0
	for key in msgType:
		# Remove n first characters (e.g. header, timestamp)
		tmpline = line [args.skip:]
		tmpkey = key [args.skip:]
		myresult=0			
		if (args.method == "distance-ratio"):
				# Compute the Levenshtein ratio between the two strings
				myresult = ratio(tmpline,tmpkey)

		if (args.method == "distance"):
				# Compute the Levenshtein distance between the two strings
				myresult = distance(tmpline,tmpkey)
		elif (args.method == "tlsh"):
				# Compute the diff between two hashes
				h1 = tlsh.hash(str.encode(tmpline))
				h2 = tlsh.hash(str.encode(tmpkey))
				if (h1 != "TNULL" and h2 != "TNULL"):
					myresult = tlsh.diff(h1, h2)
					#if verbose: print (line)
					#if verbose: print (h1 + "    "+ h2 + " -> " + str(myresult))
					#if verbose: print ("\n\n\n")

		if (myresult > THR and args.method == "distance-ratio"):
		# Current line is very similar with one from the list
			save_key = key
			save_result = myresult
			flag = 1
			break

		if (myresult <= THR and (args.method == "tlsh" or args.method == "distance")):
		# Current line is very similar with one from the list
			#print (tmpline,tmpkey,myresult)
			save_key = key
			save_result = myresult
			flag = 1
			break

	# Current line is similar with a line from msgType dictionary
	if (flag == 1):	
	 	# the sample dictionary is not full
		#if (len(msgType[save_key].keys()) < sample_size):
		if (len(msgType[key].keys()) < sample_size):

			msgType[save_key][line] = save_result
		else:
			largest_key = ''
			largest_val = -1
			# search for the line with the highest ratio (close to the original one)
			for key in msgType[save_key].keys():
				if (msgType[save_key][key] > largest_val):
					largest_key = key
					larget_val = msgType[save_key][key]
			
			# delete the line with the highest ratio (close to the original one)
			del msgType[save_key][largest_key]
			msgType[save_key][line] = save_result

		msgTypeCounter[save_key] += 1
	# Current line is different enough from ones from the list, so we add it to the dictionary
	else:
		msgType[line] = {}
		msgTypeCounter[line] = 1
		msgType2ID[line] = msgType_id
		msgType_id += 1
		#print ("New type of message discovered line #%s:" %counter)
		#print (line)
		#print ('\n')
				
	line = f.readline()
	if (counter%100 == 0):
		pass
		if verbose: print ("%s lines analyzed..." %counter)
	counter += 1

f.close()

if verbose: print ("%d lines analyzed" %counter)
if verbose: print ("%d message types discovered" %len(msgType))
if stats: print (args.method, THR, len(msgType))

if verbose: input('Type Enter to display discovered types...')

outputfile=open(args.output,"w")
sortedList=[]
#Sort msgType by popularity


for key1 in sorted (iter(msgTypeCounter.items()), reverse=True, key=lambda kv: kv[1]):
	numberOfOccurence = msgTypeCounter[key1[0]]
	msgID = msgType2ID[key1[0]]
	percentageOfOccurence= (numberOfOccurence / float(counter))*100
	stringPercentageOfOccurence="%.2f" % percentageOfOccurence
	if verbose: print ("Message UID = %s" % (msgID))
	outputfile.write("Message UID = %s" % (msgID))
	if verbose: print ("Number of similar message = %s (%s%%)\n" % (numberOfOccurence-1,stringPercentageOfOccurence))
	outputfile.write("\nNumber of similar message = %s (%s%%)\n" % (numberOfOccurence-1,stringPercentageOfOccurence))
	if verbose: print ("Message type:")
	outputfile.write("Message type:\n")
	if verbose: print ("----------------\n")
	outputfile.write("----------------\n")
	if verbose: print (key1[0])
	outputfile.write(key1[0])
	if numberOfOccurence >1:
		if verbose: print ("\n\nOther sample of similar messages:")
		outputfile.write("\n\nOther sample of similar messages:\n")
		if verbose: print ("-----------------------------\n")
		outputfile.write("-----------------------------\n")
		for key2 in sorted(iter(msgType[key1[0]].items()), key=lambda kv: kv[1]):
    	 		if verbose: print (msgType[key1[0]][key2[0]])
    	 		if verbose: print (key2[0])
    	 		outputfile.write(key2[0]+'\n')
        	
	if verbose: print ("______________________________________________________________________________________________________________________________________\n")
	outputfile.write("______________________________________________________________________________________________________________________________________\n\n")
outputfile.close

## fp_out = open(args.output,'wb')
## pickle.dump(msgType,fp_out)
## pickle.dump(msgTypeCounter,fp_out)
## pickle.dump(msgType2ID,fp_out)
## fp_out.close()