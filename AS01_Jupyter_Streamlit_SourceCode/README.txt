Overview
This repository contains a data science workflow focused on analyzing a dataset of nearly 1,000 video games released in 2022. The project involves comprehensive data preparation, feature extraction, and a "Metadata Volume" analysis to categorize games based on the richness of their descriptive tags (platforms, genres, and developers).

Project Structure
The project is contained within the 24FTT1856_MUHDDANISH.ipynb notebook and follows these key stages:

Data Ingestion: Loading raw video game data from video-games-2022.csv.

Data Cleaning:

Standardizing column names (lowercase and underscore formatting).

Handling missing values and removing duplicate entries.

Data Validation:

Running integrity checks on release dates to ensure calendar validity for the year 2022.

Filtering out entries with missing critical information like game titles.

Feature Engineering:

Platform/Genre/Developer Counts: Calculating the number of associated tags per game.

Metadata Volume: Categorizing games into "Low", "Medium", or "High" metadata richness based on total tags.

Seasonality Encoding: Generating one-hot encoded variables for months to support trend analysis.

Interactive Visualization: A built-in Streamlit application allows users to filter games by month and metadata volume, accompanied by visual bar charts showing the top-performing games in those categories.

Key Features
Total Entries: 987 video game records.

Attributes: Month, Day, Title, Platforms, Genres, Developers, and Publishers.

Advanced Analytics: Includes "Platform Ratio" analysis to determine the density of platform-specific metadata relative to other game tags.