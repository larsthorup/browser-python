mypy browser
INTEGRATION_TESTS=1 coverage run -m pytest browser -v
coverage html
coverage report
