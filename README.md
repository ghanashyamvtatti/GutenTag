# GutenTag

## Description

GutenTag is a big-data application that uses LDA and other NLP magic to automatically tag news articles.

## The need for Automated Tagging

* Constant influx of articles
* Manually tagging  each article is a difficult and time consuming process
* Tags/Keywords are crucial data for search engines
* Tagging helps improve recommendations

## Features

* Consume APIs to fetch articles
* Extract metadata (tags and sentiments)
* The sentiment can be used to determine the overall opinion conveyed by the articles
* Index the metadata to provide improved search

## Setup

1. Install the required packages via `pip install -r requirements.txt`
2. Ensure you have docker installed, and run `scripts\run.cmd` (on Windows) or `scripts\run.sh` (on Mac/Linux)
3. Run `start.cmd` (on Windows) or `start.sh` (on Mac/Linux)
4. Open http://localhost:5000/index.html on your browser

## Usage

### Data Extraction:

1. Click ‘Extract’ on the navbar.
2. Enter the umbrella term and click the ‘Extract’ button.
3. The process will fetch the raw data from ElasticSearch, run it through the ML
pipeline, and store the processed data back into another index on ElasticSearch.

### Search:

1. Go to the ‘Search’ page.
2. Enter the search query and click the search button.
3. The results will appear in the table.