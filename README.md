# nopCommerce Automation Framework

Basic test automation framework for nopCommerce using Playwright + Python.

## Installation

```bash
pip install -r requirements.txt
playwright install
```

## Allure reports

1. Run tests and collect results

    ```bash
    pytest tests/ --alluredir=reports/allure-results -v
    ```

2. Generate reports

    ```bash
    allure generate reports/allure-results -o reports/allure-report --clean
    ```

3. Open report

    ```bash
    allure open reports/allure-report
    ```

## Parallel running tests
For parallel running use command:
```bash
pytest -n auto # Run tests on all available CPU cores
```
```bash
pytest -n 2 # Run tests on 2 cores
```
