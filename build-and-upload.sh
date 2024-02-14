#!/usr/bin/env bash

python -m build --wheel
python -m build --sdist
twine upload --config-file .pypirc --skip-existing dist/*