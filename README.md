# About

A sample test automation framework to test Wander's search functionalities. The framework is built using Python and Playwright UI automation library.

## Dependencies
You need the following pre-requisites to run the tests:

1. Python 3.8 or higher
2. Playwright pytest plugin
3. Playwright broswers


## Setup

Git clone this repo.

Install playwright pytest plugin.

```bash
pip install pytest-playwright
```
Install the browsers:
```bash
playwright install
```
Install  pspec test report library
```bash
pip install pytest-pspec
```
## Running the Tests

Navigate to the project directory.

To execute the tests with the browser visible:
```bash
pytest --pspec tests/test_landing_page.py --headed
```

To execute the tests in headless mode (without launching the browser):
```bash
pytest --pspec tests/test_landing_page.py
```