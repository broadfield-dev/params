#!/usr/bin/env python3
import ast
import sys
import argparse
from pathlib import Path

def get_docstring_summary(node):
    doc = ast.get_docstring(node)
    if not doc:
        return ""
    lines = [line.strip() for line in doc.splitlines() if line.strip()]
    return lines[0] if lines else ""

def format_param(param, defaults_dict):
    name = param.arg
    annotation = "any"
    if param.annotation:
        annotation = ast.unparse(param.annotation).strip()

    default = defaults_dict.get(name)
    if default is not ...:
        default_str = f" = {ast.unparse(default)}" if default is not None else " = None"
        required = "optional"
    else:
        default_str = ""
        required = "**required**"

    return f"`{name}`: {annotation}{default_str}  ({required})"

def process_function(node, class_name=""):
    lines = []
    qualname = f"{class_name + '.' if class_name else ''}{node.name}"
    header = f"### `{'async ' if isinstance(node, ast.AsyncFunctionDef) else ''}{qualname}()`"
    lines.append(header)

    args = node.args
    defaults = {}
    pos_args = args.posonlyargs + args.args

    if args.defaults:
        offset = len(pos_args) - len(args.defaults)
        for i, default in enumerate(args.defaults):
            param_name = pos_args[offset + i].arg
            defaults[param_name] = default

    if args.vararg:
        defaults[args.vararg.arg] = ...

    if args.kwonlyargs:
        for i, arg in enumerate(args.kwonlyargs):
            default = args.kw_defaults[i] if i < len(args.kw_defaults) else ...
            defaults[arg.arg] = default

    if args.kwarg:
        defaults[args.kwarg.arg] = ...

    param_lines = []
    for arg in args.posonlyargs:
        param_lines.append(format_param(arg, defaults))
    for arg in args.args:
        param_lines.append(format_param(arg, defaults))
    if args.vararg:
        ann = ast.unparse(args.vararg.annotation) if args.vararg.annotation else "any"
        param_lines.append(f"`*{args.vararg.arg}`: {ann}  (variadic)")
    for arg in args.kwonlyargs:
        param_lines.append(format_param(arg, defaults))
    if args.kwarg:
        ann = ast.unparse(args.kwarg.annotation) if args.kwarg.annotation else "any"
        param_lines.append(f"`**{args.kwarg.arg}`: {ann}  (kwargs)")

    if param_lines:
        lines.append("")
        lines.append("**Parameters:**")
        for p in param_lines:
            lines.append(f"- {p}")

    if node.returns:
        lines.append("")
        lines.append(f"**Returns:** `{ast.unparse(node.returns).strip()}`")

    summary = get_docstring_summary(node)
    if summary:
        lines.append("")
        lines.append(f"**Summary:** {summary}")

    lines.append("")
    return lines

def add_parent_references(node, parent=None):
    node.parent = parent
    for child in ast.iter_child_nodes(node):
        add_parent_references(child, node)

def generate_markdown(filepath: Path):
    content = filepath.read_text(encoding="utf-8")
    try:
        tree = ast.parse(content, filename=str(filepath))
    except SyntaxError as e:
        print(f"Error parsing {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

    add_parent_references(tree)

    lines = [f"# Function Documentation – {filepath.name}", "", ""]

    current_class = ""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            lines.append(f"## Class `{node.name}`")
            summary = get_docstring_summary(node)
            if summary:
                lines.append(f"**Summary:** {summary}")
            lines.append("")
            current_class = node.name

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not isinstance(node.parent, (ast.Module, ast.ClassDef)):
                continue
            md_lines = process_function(node, current_class)
            lines.extend(md_lines)

    return "\n".join(lines)

def parse_to_markdown(filepath: Path | str) -> str:
    """Main function that can be called programmatically"""
    return generate_markdown(Path(filepath))
  
def main():
    parser = argparse.ArgumentParser(description="Generate Markdown docs from Python functions")
    parser.add_argument("file", type=Path, help="Python file to parse")
    parser.add_argument("--output", "-o", type=Path, help="Output markdown file (default: stdout)")
    args = parser.parse_args()

    md_content = generate_markdown(args.file)

    if args.output:
        args.output.write_text(md_content, encoding="utf-8")
        print(f"Written to: {args.output}", file=sys.stderr)
    else:
        print(md_content)

if __name__ == "__main__":
    main()
