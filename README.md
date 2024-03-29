<p align="center">
  <img width="700" alt="architecture" src="Plot_im/cir_bar.png">
</p>

# Music-Popularity-Analysis
## Desciption
In this project, we will analyze the most popular songs on Youtube and Spotify
based on their various features. We hope we’ll be able to identify important trends, patterns and
insights that can impact a songs’ performance and popularity.
## Project structure
Directories:
 - Scrape: source code for data scraping
   + Spotify: source code for scraping Spotify
    * utils.py: python module containing necessary functions to scrape Spotify data
    * download_har.py: main python module to scrape our Spotify data
   + Wikipedia: source code for scraping Wikipedia
     * get_wiki_url.py: python module to retrieve wikipedia articles for songs
     * wiki_scrape_genre.py: python module to scrape the genres from the articles
   + YouTube: source code for scraping YouTube
     * api.py: call the YouTube api to get response
     * check.py: check to see if all the responses are there
     * title_filtering.py: filtering our keywords before searching
     * extract_link.py: retrieve the URL for YouTube videos
     * get_view.py: scrape YouTube information from the URL
   
 - Analysis: 
   + analysis.ipynb: notebook containing our source code for the eda and visualization 
   + merge.py: contains our source code for data integration
   + data_no_genre: data without the feature genre
   + data_with_genre: data with the feature genre

## Architecture
<p align="center">
  <img width="700" alt="architecture" src="Plot_im/architecture.png">
</p>

## Analysis result
See [charts](Plot_im) for all the visualisation and [report](report.pdf) for detailed analysis
