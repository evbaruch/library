from bs4 import BeautifulSoup

# Read the input HTML file
input_file = "table.html"
output_file = "output.html"
base_url = "https://he.wikipedia.org"

# Parse the HTML file
with open(input_file, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Extract table structure and data
table_data = []
table = soup.find('tbody')

for row in table.find_all('tr'):
    row_data = []
    for cell in row.find_all(['th', 'td']):
        # Update all <a> tags in the cell with the base URL
        for link in cell.find_all('a', href=True):
            link['href'] = base_url + link['href'] if not link['href'].startswith("http") else link['href']

        # Capture content and attributes
        cell_content = cell.decode_contents()  # Keeps all inner HTML (e.g., spans, line breaks)
        attributes = {
            "rowspan": cell.get("rowspan"),
            "colspan": cell.get("colspan")
        }
        row_data.append((cell_content, attributes))
    table_data.append(row_data)

# Generate a new HTML structure
new_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Books Information</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Books Information</h1>
    <table border="1">
"""
for row in table_data:
    new_html += "        <tr>\n"
    for cell_content, attributes in row:
        rowspan = f" rowspan='{attributes['rowspan']}'" if attributes['rowspan'] else ""
        colspan = f" colspan='{attributes['colspan']}'" if attributes['colspan'] else ""
        tag = "th" if any(attributes.values()) else "td"  # Use <th> for header cells
        new_html += f"            <{tag}{rowspan}{colspan}>{cell_content}</{tag}>\n"
    new_html += "        </tr>\n"

new_html += """
    </table>
</body>
</html>
"""

# Write the new HTML file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(new_html)

print(f"Processed HTML data with updated links written to {output_file}.")
