# Barchart API
*Version: 0.5.0*

Unofficial API for https://www.barchart.com/

### API Calls:
- Top Stocks to Own
- Top ETFs to Own

### Usage:
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

#### Install Instructions
Install Python Package

```bash
python -m pip install barchart-api
```

#### Build Instructions
Build Python Package

```bash
sudo chmod +x ./*.py
sudo pip install .
python3 setup.py bdist_wheel --universal
# Test Pypi
twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose -u "Username" -p "Password"
# Prod Pypi
twine upload dist/* --verbose -u "Username" -p "Password"
```
