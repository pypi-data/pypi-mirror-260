import re
import html

# Regular expressions for Markdown entities
BOLD_RE = re.compile(r"\*\*(.*?)\*\*")
ITALIC_RE = re.compile(r"__(.*?)__")
CODE_RE = re.compile(r"`(.*?)`")
URL_RE = re.compile(r"\[(.*?)\]\((.*?)\)")

# Simple function to escape HTML
def escape_html(text):
    return html.escape(text)

def parse_markdown(text):
    """Converts Markdown text to HTML."""
    # Escape HTML
    text = escape_html(text)
    
    # Bold
    text = BOLD_RE.sub(r"<b>\1</b>", text)
    
    # Italic
    text = ITALIC_RE.sub(r"<i>\1</i>", text)
    
    # Inline code
    text = CODE_RE.sub(r"<code>\1</code>", text)
    
    # URLs
    text = URL_RE.sub(r'<a href="\2">\1</a>', text)
    
    return text

def unparse_html(text):
    """Converts HTML back to Markdown. This is a simplified approach."""
    # URLs
    text = re.sub(r'<a href="(.*?)">(.*?)</a>', r'[\2](\1)', text)
    
    # Inline code
    text = text.replace("<code>", "`").replace("</code>", "`")
    
    # Italic
    text = text.replace("<i>", "__").replace("</i>", "__")
    
    # Bold
    text = text.replace("<b>", "**").replace("</b>", "**")
    
    return text
