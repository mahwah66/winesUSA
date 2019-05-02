*  Quick Summary
* TO BE EDITED
We provide an ETL pipeline that enables Business Inteligence Analysts at FryCorp Network to determine which shows to promote for advertisements. We used Historical TV Show ratings from tv guide, historical viewership metrics from Nielson ratings, and show production budgets from Wikipedia. We provide our data in a SQL database which exposes, for the most genres, KPIs to determine which genres are underrepresented and could deliver the most value to the FryCorp network if prioritized.

* Steps to run the pipeline:
* TO BE EDITED
Start MySql
Run mysql -u username -p database_name < seed.sql to seed the database and tables
Run python etl.py to extract the data and put it into the Postgres database
????
Profit

* Narrative / Motivation
We are creating a website that will give users usefull information when they are trying to select a domestic wine based on type of wine, price, rating, score, and/or location.

* Final Schema / Data Model / How to use the data
* TO BE EDITED
Explain what the final data model in your database is. Why did you make that decision and how do you expect people to use it. Entity-Relation diagrams would be great (https://dbdiagram.io/home or other online tools)

* Data Sources
We pulled data from Wine Enthusiest's website WineMag.com. It provided us with ratings for different US wines and is updated periodically as new wines are submitted for review. It also supplied us with the vintage, price and vinyard. Ratings are of course subjective but in this case they were determined by one or more wine critics using a 100 point scale. We also pulled AVAs - American Viticultural Areas from wikipedia for a comprehensive list of the States and regions of the wines. Also from Wikipedia by AVA we have information about the grapes, climate, size of the area and year founded. Some additional information about the regions and grapes was supplemented from winesearcher.com. The basic description of the types of wine was pulled from Wines.com. Finally we pulled some cheese pairing for common varietials from WineMonger.com. This information is based on the author's recommendations.

* Transformation Step
* TO BE EDITED
Explain how you got your raw data into the final model. What were the specific steps you had to take to get the data into the final data model.

Example: In order to build our final tables, we had to:

Group the TV Guide ratings by genre and year
Aggregated on the mean and media rating for each group
etc.