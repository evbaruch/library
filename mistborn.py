from bs4 import BeautifulSoup
import string

# File paths
input_file = "glossaty2.txt"
output_file = "glossary2.html"
base_url = "https://mistborn.fandom.com"

# Read and parse the input file
with open(input_file, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Extract the terms and their links
terms = []
for li in soup.find_all('li'):
    link = li.find('a', href=True)
    if link:
        term = link.text.strip()
        href = base_url + link['href']
        terms.append((term, href))

# Group terms alphabetically
grouped_terms = {}
for term, href in terms:
    first_letter = term[0].upper()
    if first_letter not in string.ascii_uppercase:
        first_letter = "#"
    grouped_terms.setdefault(first_letter, []).append((term, href))

# Generate the HTML structure
new_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glossary</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav>
            <ul class="navbar">
                <li><a href="index.html">Home</a></li>
                <li><a href="catalog.html">Catalog</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <section id="glossary">
            <h1>Glossary</h1>
            <p>Explore terms and concepts from Mistborn:</p>
"""

# Add terms grouped by letter
for letter, entries in sorted(grouped_terms.items()):
    # Add the letter as a header
    new_html += f"            <h2>{letter}</h2>\n"
    for term, href in sorted(entries):
        # Each term is a details block with the term as the summary
        new_html += f"            <details>\n"
        new_html += f"                <summary><a href='{href}'>{term}</a></summary>\n"
        new_html += f"            </details>\n"

# Close the HTML structure
new_html += """
        </section>
    </main>
    <footer>
        <p>&copy; 2024 Mistborn Glossary. All rights reserved.</p>
    </footer>
</body>
</html>
"""

# Write the new HTML file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(new_html)

print(f"Glossary HTML written to {output_file}.")
