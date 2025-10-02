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

