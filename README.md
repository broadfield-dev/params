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

# Example output

```
# Function Documentation – parse_py.py


### `get_docstring_summary()`

**Parameters:**
- `node`: any = None  (optional)

### `format_param()`

**Parameters:**
- `param`: any = None  (optional)
- `defaults_dict`: any = None  (optional)

### `process_function()`

**Parameters:**
- `node`: any = None  (optional)
- `class_name`: any = ''  (optional)

### `add_parent_references()`

**Parameters:**
- `node`: any = None  (optional)
- `parent`: any = None  (optional)

### `generate_markdown()`

**Parameters:**
- `filepath`: Path = None  (optional)

### `main()`
```
