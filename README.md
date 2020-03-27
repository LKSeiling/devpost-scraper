# devpost-scraper
Python-based webscraper to extract project and participant information from a devpost.com hackathon webpage.
The resulting table can be used to gain an overview over projects and partcipants to ease inter-project coordination and communication.

## Data Collected
From a given hackathon.devpost.com webpage data is collected for all submissions. This includes
* associated challenge
* heading and subheading of submission
* submission description (story)
* urls to videos in story
* languages used in submission
* links in submission
* number of participants on submission

## Usage
Please execute the main script passing both the url of the devpost hackathon as well as the filename for the csv:
```python3 src/main.py --devpost-hackathon https://wirvsvirushackathon.devpost.com --filename virvswirus_submissions.csv```
