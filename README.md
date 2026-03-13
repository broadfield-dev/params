# params

Generate clean Markdown documentation of functions, parameters, defaults and type hints from any Python file - using only the standard library (`ast`).

## Installation

```bash
pip install git+https://github.com/broadfield-dev/params.git
```

# Print to terminal
```bash
params your_script.py
```

# Save to file
```bash
params src/utils.py --output docs/functions.md
```

# Or with redirection
```bash
params app.py > api.md
```
