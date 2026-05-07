# Clipboard HTML Wrapper

This Python script reads lines of text from the clipboard, prompts the user for an HTML start tag (which may include attributes), wraps each line with the start tag and its corresponding end tag, and copies the result back to the clipboard.

## Requirements

- Python 3.x
- pyperclip library (install via `pip install pyperclip`)

## Usage

1. Copy some text to the clipboard (multiple lines are supported).
2. Run the script: `python clipboard_html_wrapper.py`
3. Enter the starting HTML tag when prompted, e.g., `<p class="highlight">`
4. The script will wrap each line and copy the result back to the clipboard.

## Example

Clipboard content:
```
Line 1
Line 2
```

User enters: `<strong>`

Output copied to clipboard:
```
<strong>Line 1</strong>
<strong>Line 2</strong>
```

## Troubleshooting

- Ensure pyperclip is installed: `pip install pyperclip`
- The script assumes the clipboard contains text. If it contains other data, it may not work as expected.
- The HTML tag must be properly formatted, starting with `<` and ending with `>`.
- If the tag has attributes, ensure there are no spaces in the tag name part.