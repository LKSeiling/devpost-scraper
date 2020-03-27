import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup
from html2text import html2text
from websites import SubmissionOverview, ProjectPage
from tqdm import tqdm

class DevpostScraper():

	def __init__(self,website,filename):
		self.base_page = SubmissionOverview(website+"/submissions/")
		try:
			self.challenge_urls = self.base_page.get_challenge_urls()
		except error:
			print(error)
			sys.exit()

		try:
			search_results = self.get_data_by_challenge()
		except:
			print("Data collection process failed.")
			sys.exit()

		try:
			search_results.to_csv(filename, index=False)
		except:
			print("Failed to write results to file.")
			sys.exit()
	
	def get_data_by_challenge(self):
		df_list = []

		for num, challenge in tqdm(self.challenge_urls.keys()):
			# get data on all projects in challenge
			all_project_data = self.get_project_data(self.challenge_urls[(num, challenge)])
			# write collected data into dataframe and add challenge-specific columns
			res_df = pd.DataFrame.from_dict(all_project_data, orient='index')
			res_df['url'] = res_df.index
			res_df['challenge_num'] = num
			res_df['challenge'] = challenge
			# add data to list
			df_list.append(res_df)

		# create combined dataframe from lists
		result = pd.concat(df_list, sort=True)
		result = result.reset_index()
		del result['index']
		result = result[['challenge_num', 'challenge', 'title', 'subtitle', 'story', 'n_members', 'links', 'url']]
		return result

	def get_project_data(self, website):
		so = SubmissionOverview(website)
		collected_data = {}

		next_url, is_last = so.check_if_last(website)
		projects_on_page = so.get_project_urls()
		if not is_last:
			collected_data = self.get_project_data(next_url)

		for project_url in projects_on_page:
			pp = ProjectPage(project_url)
			collected_data[project_url] = pp.return_info_dict()

		return collected_data