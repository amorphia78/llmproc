import re


def strip_style_tags(html):
    """
    Remove <style> tags and all their contents from HTML.
    This prevents CSS from appearing in rendered text.
    """
    import re
    # Remove style tags and everything between them (case-insensitive, handles multiline)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.IGNORECASE | re.DOTALL)
    return html


def strip_id_header(html):
    """
    Remove the <h2>ID: ...</h2> header from HTML.
    We'll add the Article ID separately in the table.
    """
    import re
    # Remove <h2>ID: article_id</h2> (case-insensitive)
    html = re.sub(r'<h2>ID:.*?</h2>', '', html, flags=re.IGNORECASE | re.DOTALL)
    return html


def decode_html_entities(text):
    """
    Decode common HTML entities like &#x27; (apostrophe), &quot;, &amp;, etc.
    """
    import html
    return html.unescape(text)


def html_to_rtf_text(html):
    """
    Convert HTML to RTF formatted text.
    Handles the specific HTML structure used in the articles.
    """
    # Strip style tags and ID header first
    html = strip_style_tags(html)
    html = strip_id_header(html)
    
    # Decode HTML entities
    html = decode_html_entities(html)
    
    # Remove leading/trailing whitespace
    html = html.strip()
    
    # Start with plain text
    rtf = ""
    
    # Simple state machine for parsing
    i = 0
    bold_stack = 0
    italic_stack = 0
    in_figure = False
    
    while i < len(html):
        if html[i] == '<':
            # Find the closing >
            close_idx = html.find('>', i)
            if close_idx == -1:
                # Malformed HTML, just add the character
                rtf += html[i]
                i += 1
                continue
            
            tag = html[i:close_idx + 1]
            tag_content = tag[1:-1]
            tag_name = tag_content.split()[0].lower().strip('/')
            is_closing = tag.startswith('</')
            is_self_closing = tag.endswith('/>')
            
            # Handle different tags
            if tag_name == 'b' or tag_name == 'strong':
                if is_closing:
                    rtf += '\\b0 '
                    bold_stack -= 1
                else:
                    rtf += '\\b '
                    bold_stack += 1
            elif tag_name == 'i' or tag_name == 'em':
                if is_closing:
                    rtf += '\\i0 '
                    italic_stack -= 1
                else:
                    rtf += '\\i '
                    italic_stack += 1
            elif tag_name in ['p', 'div']:
                if is_closing:
                    rtf += '\\par\n'
            elif tag_name == 'br':
                rtf += '\\line\n'
            elif tag_name == 'h1':
                if not is_closing:
                    rtf += '\\b\\fs32 '
                else:
                    rtf += '\\b0\\fs24\\par\n'
            elif tag_name == 'h2':
                if not is_closing:
                    rtf += '\\b\\fs28 '
                else:
                    rtf += '\\b0\\fs24\\par\n'
            elif tag_name in ['h3', 'h4', 'h5', 'h6']:
                if not is_closing:
                    rtf += '\\b\\fs26 '
                else:
                    rtf += '\\b0\\fs24\\par\n'
            elif tag_name == 'figure':
                if not is_closing:
                    in_figure = True
                    rtf += '\\par\n'
                else:
                    in_figure = False
                    rtf += '\\par\n'
            elif tag_name == 'figcaption':
                if not is_closing:
                    rtf += '\\i '
                else:
                    rtf += '\\i0\\par\n'
            elif tag_name == 'img':
                # Extract alt text if available
                alt_match = re.search(r'alt=["\']([^"\']*)["\']', tag_content)
                if alt_match:
                    alt_text = alt_match.group(1)
                    rtf += f'[Image: {alt_text}]'
                else:
                    rtf += '[Image]'
            elif tag_name == 'ul' or tag_name == 'ol':
                if is_closing:
                    rtf += '\\par\n'
            elif tag_name == 'li':
                if not is_closing:
                    rtf += '\\bullet  '
                else:
                    rtf += '\\par\n'
            # Ignore html, head, body, style tags
            elif tag_name in ['html', 'head', 'body', 'style']:
                pass
            
            i = close_idx + 1
        else:
            # Regular character - escape special RTF characters
            char = html[i]
            if char == '\\':
                rtf += '\\\\'
            elif char == '{':
                rtf += '\\{'
            elif char == '}':
                rtf += '\\}'
            elif char == '\n':
                # Skip newlines in HTML source
                pass
            else:
                rtf += char
            i += 1
    
    return rtf


def escape_rtf_text(text):
    """
    Escape special RTF characters in plain text (for the HTML source column).
    """
    text = text.replace('\\', '\\\\')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('\n', '\\line\n')
    return text


def create_rtf_review_file(original_articles, summary_articles, output_filename='review.rtf'):
    """
    Create an RTF file with a three-column table for article review.
    
    Args:
        original_articles: dict with article IDs as keys and original HTML as values
        summary_articles: dict with article IDs as keys and summary HTML as values
        output_filename: name of the output RTF file
    """
    
    # RTF header with landscape orientation and 1cm margins
    # Standard US Letter: portrait is 12240x15840 twips, landscape swaps these
    # 1 cm = 567 twips (1 inch = 1440 twips, 1 cm = 0.3937 inches)
    rtf_content = (
        '{\\rtf1\\ansi\\ansicpg1252\\deff0\\deflang1033\n'
        '{\\fonttbl{\\f0\\fswiss\\fcharset0 Arial;}{\\f1\\fmodern\\fcharset0 Courier New;}}\n'
        '{\\colortbl;\\red0\\green0\\blue0;\\red255\\green0\\blue0;}\n'
        '\\viewkind4\\uc1\\pard\\f0\\fs24\n'
        '\\paperw15840\\paperh12240\\margl567\\margr567\\margt567\\margb567\\landscape\n'
    )
    
    # Title
    rtf_content += (
        '\\par\\b\\fs28 Article Review\\b0\\fs24\\par\\par\n'
    )
    
    # Get sorted article IDs for consistent ordering
    article_ids = sorted(original_articles.keys())
    
    # Start the single table with a header row
    rtf_content += (
        '\\trowd\\trgaph108\\trleft0\\trbrdrl\\brdrs\\brdrw10\\trbrdrt\\brdrs\\brdrw10\\trbrdrr\\brdrs\\brdrw10\\trbrdrb\\brdrs\\brdrw10\n'
        '\\clbrdrl\\brdrw10\\brdrs\\clbrdrt\\brdrw10\\brdrs\\clbrdrr\\brdrw10\\brdrs\\clbrdrb\\brdrw10\\brdrs\\cellx4902\n'
        '\\clbrdrl\\brdrw10\\brdrs\\clbrdrt\\brdrw10\\brdrs\\clbrdrr\\brdrw10\\brdrs\\clbrdrb\\brdrw10\\brdrs\\cellx9804\n'
        '\\clbrdrl\\brdrw10\\brdrs\\clbrdrt\\brdrw10\\brdrs\\clbrdrr\\brdrw10\\brdrs\\clbrdrb\\brdrw10\\brdrs\\cellx14706\n'
    )
    
    # Header row
    rtf_content += (
        '\\pard\\intbl\\qc\\b Column 1: Original\\b0\\cell\n'
        '\\pard\\intbl\\qc\\b Column 2: Summary\\b0\\cell\n'
        '\\pard\\intbl\\qc\\b Column 3: Summary HTML (Editable)\\b0\\cell\n'
        '\\row\n'
    )
    
    # Data rows - one per article
    for article_id in article_ids:
        original_html = original_articles.get(article_id, '')
        summary_html = summary_articles.get(article_id, '')
        
        # Convert HTML to RTF-formatted text for columns 1 and 2
        original_rtf = html_to_rtf_text(original_html)
        summary_rtf = html_to_rtf_text(summary_html)
        
        # Keep HTML as plain text for column 3
        summary_html_text = escape_rtf_text(summary_html)
        
        # Define row structure (same column widths as header)
        rtf_content += (
            '\\trowd\\trgaph108\\trleft0\\trbrdrl\\brdrs\\brdrw10\\trbrdrt\\brdrs\\brdrw10\\trbrdrr\\brdrs\\brdrw10\\trbrdrb\\brdrs\\brdrw10\n'
            '\\clbrdrl\\brdrw10\\brdrs\\clbrdrt\\brdrw10\\brdrs\\clbrdrr\\brdrw10\\brdrs\\clbrdrb\\brdrw10\\brdrs\\cellx4902\n'
            '\\clbrdrl\\brdrw10\\brdrs\\clbrdrt\\brdrw10\\brdrs\\clbrdrr\\brdrw10\\brdrs\\clbrdrb\\brdrw10\\brdrs\\cellx9804\n'
            '\\clbrdrl\\brdrw10\\brdrs\\clbrdrt\\brdrw10\\brdrs\\clbrdrr\\brdrw10\\brdrs\\clbrdrb\\brdrw10\\brdrs\\cellx14706\n'
        )
        
        # Column 1: Original (formatted)
        rtf_content += (
            '\\pard\\intbl\n'
            f'{original_rtf}'
            '\\cell\n'
        )
        
        # Column 2: Summary (formatted) with Article ID at top
        rtf_content += (
            f'\\pard\\intbl\\b Article ID: {article_id}\\b0\\par\n'
            f'{summary_rtf}'
            '\\cell\n'
        )
        
        # Column 3: Summary HTML (raw text)
        rtf_content += (
            '\\pard\\intbl\\f1\\fs20\n'
            f'{summary_html_text}'
            '\\f0\\fs24\\cell\n'
        )
        
        # End this data row
        rtf_content += '\\row\n'
    
    # Exit table mode
    rtf_content += '\\pard\\par\n'
    
    # RTF footer
    rtf_content += '}\n'
    
    # Write to file
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(rtf_content)
    
    print(f"RTF review file created: {output_filename}")


# Example usage
if __name__ == "__main__":
    # Sample data
    original_articles = {
        'article_001': '<h1>Breaking News</h1><p>This is the <b>original</b> article text with some <i>formatting</i>.</p><p>Second paragraph here.</p>',
        'article_002': '<h1>Another Story</h1><p>More news content goes here.</p>',
    }
    
    summary_articles = {
        'article_001': '<p><b>Summary:</b> Original article about breaking news with formatting.</p>',
        'article_002': '<p><b>Summary:</b> Another story summarized.</p>',
    }
    
    create_rtf_review_file(original_articles, summary_articles, 'article_review.rtf')
