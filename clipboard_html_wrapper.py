import pyperclip

def main():
    # Read text from clipboard
    text = pyperclip.paste()
    
    # Split into lines
    lines = text.splitlines()
    
    # Prompt user for starting HTML tag
    start_tag = input("Enter the starting HTML tag (e.g., <p class='myclass'>): ").strip()
    
    # Validate the tag starts with '<' and ends with '>'
    if not start_tag.startswith('<') or not start_tag.endswith('>'):
        print("Invalid HTML tag. It must start with '<' and end with '>'.")
        return
    
    # Extract tag name (everything between < and first space or >)
    tag_content = start_tag[1:-1]  # Remove < and >
    tag_name = tag_content.split()[0]  # Get the tag name before any attributes
    
    # Create end tag
    end_tag = f"</{tag_name}>"
    
    # Wrap each line with the tags
    wrapped_lines = [f"{start_tag}{line}{end_tag}" for line in lines]
    
    # Join the wrapped lines back into a single string
    output = '\n'.join(wrapped_lines)
    
    # Copy the result back to clipboard
    pyperclip.copy(output)
    
    print("Wrapped text has been copied back to the clipboard.")

if __name__ == "__main__":
    main()