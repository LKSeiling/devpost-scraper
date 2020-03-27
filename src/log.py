from datetime import datetime
import os.path

class Log():

	def __init__(self):
		if not os.path.isfile("log.txt"):
			with open("log.txt", "w") as f:   # Opens file and casts as f 
				f.write(str(datetime.now()))
				f.write("\nLOG for MISSING PIECES OF INFORMATION\n\n")

	def log_failure(self, datapoint, link):
		with open("log.txt", "a") as f:   # Opens file and casts as f 
			f.write("failed to find {} for{}\n".format(datapoint,link))