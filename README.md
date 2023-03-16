# Barchart API
*Version: 0.0.1*

Unofficial API for https://www.barchart.com/

### API Calls:
- Top Stocks to Own
- Top ETFs to Own

### Usage:
```python
#!/usr/bin/python
# coding: utf-8
import barchart_api

barchart_client = barchart_api.Api(url="https://barchart.com")

top_stocks_top_own = barchart_client.get_top_stocks_top_own()
print(top_stocks_top_own)
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
