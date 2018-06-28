# Carnovo Cases

# Case 1: Google Maps

The results from my Google Maps scraping you can see on http://dennisdemenis.pythonanywhere.com/
The source-code is located in the folder Google Maps: 
- db_setup.py sets up the database to store the name and postal code of cardealers
- GoogleScraper.py looks for Cardealers around Carnovo and saves them in the database
- flask_app.py takes care about setting up a simple webpage, that represents the database-entries
- For the case that the website is down, I also added a screenshot webpage.png

# Case 2: Dumping Dealers
The solution of finding the dumping dealers are in the folder Dumping. 
Originally I coded in Jupyter notebook, but I also attached the solution as python file and pdf.
