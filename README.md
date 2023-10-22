# browser-python

https://browser.engineering/

## Getting started

Prerequisites:

- Bash
- Python 3

```bash
# Create virtual environment
python -m venv venv
. venv/bin/activate || . venv/Scripts/activate

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Check types
mypy browser

# Run only unit tests
pytest

# Run all tests
INTEGRATION_TESTS=1 pytest

# Produce code coverage
coverage run -m pytest && coverage html

# Browse code coverage
open htmlcov/index.html || start htmlcov/index.html

# Run browser
python browser http://example.org/

# Exit virtual environment
deactivate
```