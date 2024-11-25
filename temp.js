document.addEventListener('DOMContentLoaded', function() {
  async function populateGlossary() {
      try {
          // Fetch the text file
          const response = await fetch('glossery.txt');
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          const text = await response.text();

          // Parse the text into a glossary object
          const glossaryData = {};
          const termRegex = /<dt>(?:<[^>]+>)?([^<(]+)(?:\s*\(([^)]+)\))?(?:<\/[^>]+>)?<\/dt>\s*<dd>(.*?)<\/dd>/gs;
          
          let match;
          while ((match = termRegex.exec(text)) !== null) {
              const term = match[1].trim();
              const pronunciation = match[2] ? match[2].trim() : '';
              const description = match[3].replace(/<[^>]+>/g, '').trim();

              glossaryData[term] = {
                  pronunciation,
                  description
              };
          }

          // Get all details elements
          const detailsElements = document.querySelectorAll('details');

          // Populate each details element
          detailsElements.forEach(details => {
              const summary = details.querySelector('summary');
              const term = summary.textContent.split('(')[0].trim();

              if (glossaryData[term]) {
                  // Update pronunciation if exists
                  if (glossaryData[term].pronunciation) {
                      const existingPronunciation = summary.textContent.match(/\(([^)]+)\)/);
                      if (!existingPronunciation) {
                          summary.innerHTML += ` <span class="pronunciation">(${glossaryData[term].pronunciation})</span>`;
                      }
                  }

                  // Update description
                  const descriptionContainer = details.querySelector('div') || document.createElement('div');
                  descriptionContainer.innerHTML = `<p>${glossaryData[term].description}</p>`;
                  details.appendChild(descriptionContainer);
              }
          });

      } catch (error) {
          console.error('Error loading glossary:', error);
      }
  }

  // Call the function to parse and populate glossary
  populateGlossary();
});