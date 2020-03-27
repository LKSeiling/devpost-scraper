import sys
import argparse
from devpost_scraper import DevpostScraper

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--devpost-hackathon", help="url of the devpost hackathon")
	parser.add_argument("--filename", help="name of csv in which data is stored")
	args = parser.parse_args()
	if args.devpost_hackathon == None or args.filename == None:
		print("please supply the url for the devpost hackathon you want to scrape as well as the filename of the csv to safe the results to")
		sys.exit()
	else:
		devpost_scraper = DevpostScraper(str(args.devpost_hackathon), str(args.filename))
