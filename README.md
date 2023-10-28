# Barchart API

![PyPI - Version](https://img.shields.io/pypi/v/barchart-api)
![PyPI - Downloads](https://img.shields.io/pypi/dd/barchart-api)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/barchart-api)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/barchart-api)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/barchart-api)
![PyPI - License](https://img.shields.io/pypi/l/barchart-api)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/barchart-api)

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/barchart-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/barchart-api)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/barchart-api)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/barchart-api)

![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/barchart-api)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/barchart-api)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/barchart-api)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/barchart-api)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/barchart-api)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/barchart-api)

*Version: 0.11.0*

API for [Barchart](https://www.barchart.com/)

#### API Calls:
- Top Stocks to Own
- Top ETFs to Own

This repository is actively maintained - Contributions are welcome!

Contribution Opportunities:
- Support more endpoints!


<details>
  <summary><b>Usage:</b></summary>

```python
#!/usr/bin/python
# coding: utf-8
import barchart_api

barchart_client = barchart_api.Api(url="https://www.barchart.com/")
top_stocks_responses = barchart_client.get_top_stocks_top_own(max_pages=1)
top_stocks = []
for top_stocks_response in top_stocks_responses:
    try:
        top_stocks.append(top_stocks_response.json())
    except Exception as e:
        print(f"Top Stocks ERROR: {top_stocks_response}")
print(f"Top Stocks: {top_stocks}")
```
</details>

<details>
  <summary><b>Installation Instructions:</b></summary>

Install Python Package

```bash
python -m pip install barchart-api
```
</details>

<details>
  <summary><b>Repository Owners:</b></summary>


<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)
</details>
