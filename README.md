# AI-PyLib
Python library for artificial intelligence

# Usage

```
pip install git+https://github.com/baloise/AI-PyLib.git
```
```python
from baloise_ai_pylib import ai_service
ais = ai_service.AIService()
print(ais.banner())
```

# Setup development environment

```
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade build
python3 -m build
pip install --editable .
```
