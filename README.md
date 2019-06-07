# WinesUSA

### Group Members
Mary Phillipuk, Rachel Berkowitz, Kathleen Freeberg

## Project Summary



We are creating a website that will give users useful information when they are trying to select a domestic wine based on type of wine, price, rating, score, and/or location.

## Steps To Run 

### Dependencies:
  fromnumpy import genfromtxt
  time
  datetime 
  re
  pandas as pd 
  os  
  pymongo
  json
  splinter import Browser
  bs4 import BeautifulSoup
  requests
  flask_pymongo


1.	Download the git repository
2.	Use terminal to navigate the "Transform-Load-Mongo" folder and run the Jupyter Notebook
3.	Open a terminal and start mongod
4.	Open wine-mongo.ipyb in Jupyter Notebook and Restart the kernel and run through all the data steps
4.	Make sure mongod is still running in terminal
5.	In a new terminal window navigate to the winesUSA/wineUSAapp and run "Python app.py"
6.	When app starts go to http://127.0.0.1:5000/

To update the wine database, click ‘Get Latest’ button on the lower left side of the web page.

## Data Sources:

We scraped data from Wine Enthusiast’s website WineMag.com.  It provided us with ratings for different US wines and is updated periodically as new wines are submitted for review.  It also supplied us with the wine type, vintage, price, rating and vineyard. Ratings are of course subjective but in this case they were determined by one or more wine critics using a 100 point scale. 

We also pulled AVAs - American Vinicultural Areas, from Wikipedia for a comprehensive list of the States and regions of the wines. Also from Wikipedia by AVA, we have information about the grapes, climate, size of the area and year founded. Some additional information about the regions and grapes was supplemented from winesearcher.com. The basic description of the types of wine was pulled from Wines.com. 

## Transformation Step

The information scraped from WineMag, was for the most part, clean.  However, we scanned for and adjusted for some instances of miscategorized data (state in AVA name) and replaced some characters for easier data matching (hyphens replacing, dashes, and replaced accented letters). We also changed dates from string to date format, and prices to numeric.

