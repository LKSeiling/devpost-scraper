import requests
from bs4 import BeautifulSoup
from html2text import html2text
from log import Log

class Webpage():

	def __init__(self, url):
		self.base_url = url
		req = requests.get(self.base_url)
		self.soup = BeautifulSoup(req.content, "html.parser")
		self.log = Log()


class SubmissionOverview(Webpage):

	def __init__(self, url):
		super().__init__(url)

	"""
	Retrieves basic search urls for each individual challenge. Should only be called on 
	the generic submissions page 'hackathon.devpost.com/submissions'.
	"""
	def get_challenge_urls(self):
		try:
			#retrieve base search url
			checkbox = self.soup.find("input", type="checkbox")
			name_attr = checkbox['name']
			search_filter_url = name_attr.replace(":", "%3A")
			search_url = self.base_url+"search?utf8=✓&"+search_filter_url+"="
			#create url dict
			url_dict = {}
			checkboxes = self.soup.findAll("input", type="checkbox")
			no_num = 99
			for checkbox in checkboxes:
				name = checkbox['value']
				try:
					splits = name.split("-")
					splits = [split.strip() for split in splits]
					num = int(splits[0])
					colname = "-".join(splits[1:])
				except:
					colname = name
					num = no_num
					no_num = no_num+1
				url = name.replace(" ","+")
				url_dict[(num, colname)] = search_url+url

			return url_dict
		except:
			raise ReferenceError("Could not find challenges in project.")

	"""
	Retrieves the links for all projects on the given page.
	"""
	def get_project_urls(self):
		url_list = []
		for link_tag in self.soup.findAll("a", class_="block-wrapper-link fade link-to-software"):
			url_list.append(link_tag["href"])
		return url_list

	"""
	Checks if this page is the last one (not possible to click next), if not, return the url for the next page along with a boolean.
	"""
	def check_if_last(self, website):
		is_last = True
		new_website = None
		urls = self.get_project_urls()
		if len(urls) != 0:
			is_last = False
			new_website = self.get_next_page()
		return new_website, is_last

	"""
	Returns the next url, by adding or incrementing "&page=2" to the url.
	"""
	def get_next_page(self):	
		if len(self.base_url.split("&page=")) == 2:
			base, num = self.base_url.split("&page=")
			num = int(num)+1
			next_page = "&page=".join([base,str(num)])
		else:
			next_page = self.base_url + "&page=2"
		return next_page


class ProjectPage(Webpage):

	def __init__(self, url):
		super().__init__(url)

	def return_info_dict(self):
		info_dict = {}
		info_dict = self.add_header(info_dict)
		info_dict = self.add_story(info_dict)
		info_dict = self.add_videos(info_dict)
		info_dict = self.add_langs(info_dict)
		info_dict = self.add_members(info_dict)
		info_dict = self.add_links(info_dict)
		return info_dict

	def add_header(self, data_dict):
		try:
			header = self.soup.find(id='software-header')
			# try to get title
			try:
				app_title = header.find('h1', id='app-title')
				data_dict['title'] = app_title.get_text()
			except:
				self.log.log_failure("title", self.base_url)
				return data_dict
			# try to get subtitile
			try:
				app_description = header.find(class_='small-12 columns').p
				data_dict['subtitle'] = app_description.get_text().strip()
			except:
				self.log.log_failure("subtitle", self.base_url)				
				return data_dict
			return data_dict
		except:
			self.log.log_failure("header", self.base_url)
			return data_dict

	def add_story(self, data_dict):
		try:
			whole_story = self.soup.find("div", id="app-details-left")
			for div in whole_story.find_all("div", id="gallery"):
				div.decompose()
			for div in whole_story.find_all("div", id="built-with"):
				div.decompose()
			html_text = "".join([str(div) for div in whole_story.find_all("div")])
			readable = html2text(html_text)

			data_dict["story"] = readable
			return data_dict
		except:
			self.log.log_failure("project description", self.base_url)
			return data_dict
	
	def add_videos(self, data_dict):
		try:
			
			whole_story = soup.find("div", id="app-details-left")
			for count, div in enumerate(whole_story.find_all("div", id="gallery")):
				video_str = "video"+str(count+1)
				data_dict[video_str] = div.iframe['src']
			return data_dict
		except:
			self.log.log_failure("video", self.base_url)
			return data_dict

	def add_langs(self, data_dict):
		try:
			
			app_details = self.soup.find(id="app-details-left")
			built_with = app_details.find(id="built-with")
			for count, lang in enumerate(built_with.find_all('a')):
				lang_str = 'lang_'+str(lang)
				data_dict[lang_str] = 1
			data_dict['n_lang'] = count+1
			return data_dict
		except:
			self.log.log_failure("language", self.base_url)
			return data_dict

	def add_links(self, data_dict):
		try:
			app_details = self.soup.find(id="app-details-left")
			app_links = app_details.find('nav', class_='app-links section')
			linklist = []
			for link in app_links.find_all('a'):
				linklist.append(link['href'])
			data_dict['links'] = "; ".join(linklist)
			return data_dict
		except:
			self.log.log_failure("links", self.base_url)
			return data_dict

	def add_members(self, data_dict):
		try:
			app_team = self.soup.find(id='app-team')
			members = app_team.find_all('li', class_='software-team-member')
			data_dict['n_members'] = len(members)
			return data_dict
		except:
			self.log.log_failure("members", self.base_url)
			data_dict['n_members'] = 0
			return data_dict