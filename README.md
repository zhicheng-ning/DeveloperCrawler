# DeveloperCrawler
DeveloperCrawler is a tool designed to scrape developer information from GitHub. It utilizes multi-threading and employs a token pool to circumvent rate limits imposed by the GitHub API.

# How it Works
This tool utilizes multi-threading to concurrently request information for multiple GitHub developers. To avoid exceeding the API rate limits, it utilizes a token pool mechanism to ensure requests stay within the rate limits.

# Getting Started

## Installation
1.Clone or download the source code of this project.

2.Ensure you have Python 3 installed.

3.Install dependencies:
~~~python
pip install -r requirements.txt
~~~

4.Config your token and run the `main_crawler.py` file:
~~~python
python main_crawler.py
~~~

# Related Work
A Website for Searching GitHub Developer Info.

- Website：https://findgithubuser.nzcer.cn

- Code Repository：https://github.com/zhicheng-ning/FindGitHubDeveloper
