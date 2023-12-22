<div align="center">
<img src="./ressources/logo-epfl.png" alt="Example Image" width="192" height="108">
</div>

<div align="center">
Ecole Polytechnique Fédérale de Lausanne
</div> 
<div align="center">
CS-401: Applied Data Analysis
</div> 

# 🍺 A journey into expertise
link to the website: https://larouyan.github.io

## Table of Contents

- [Abstract](#abstract)
- [Project Structure](#project-structure)
- [Data Structure](#data-structure)
- [Research](#research)
- [Methods](#methods)
- [Timeline](#timeline)
- [Organization within the team](#organization-within-the-team)
- [Contributors](#contributors)

## Abstract
There are two types of users: extensive and occasional raters. It is reasonable to question whether this difference has an impact on the ratings. These extensive raters could be some kind of experts, such as people working in a brewery, but they can also be beer enthusiasts without professional skills. As a beer company releasing a new product, the following question may arise: *Should the company pay more attention to reviews made by experts?* To answer this question, analyses of the ratings statistics have to be done to find if the experts have an impact on the ratings. The analysis is first focused on finding relevant differences that can assess whether the difference between the two classes is significant. Secondly, the analysis is focused on more precise questions to understand if extensive raters are responsible for the success of a beer or not. Finally, this notebook will highlight why it could be interesting to look at this cluster of people.

## Project structure
```
.
├── README.md
├── code
│   ├── analysis_functions
│   │   ├── compute_experts.py
│   │   ├── create_all_beers.py
│   │   ├── create_all_users.py
│   │   ├── create_rating_statistic.py
│   │   ├── textual_analysis.py
│   │   └── visualization.py
│   ├── cleaning_functions
│   │   ├── advocate.py
│   │   ├── matched_beer.py
│   │   └── rate_beer.py
│   ├── read
│   │   ├── pickle_functions.py
│   │   └── read_functions.py
│   └── main.ipynb
│ 
└── ressources
    ├── learning_attitudes.pdf
    └── logo-epfl.png
```
The folder *code* contains all the files that produce the plots presented on the website. The Jupyter notebook **code/main.ipynb** summarizes all the steps that lead to the analysis.

## Data Structure
In order to use the code efficiently, the following structure is recommended:
```
.
├── BeerAdvocate
│   ├── beers.csv
│   ├── breweries.csv
│   ├── pickles
│   │   ├── df_advocate_beers.pkl
│   │   └──  ...
│   ├── ratings.txt
│   ├── reviews.txt
│   ├── users.csv
├── RateBeer
│   ├── beers.csv
│   ├── breweries.csv
│   ├── pickles
│   │   ├── df_rate_beer_beers.pkl
│   │   └──  ...
│   ├── ratings.txt
│   ├── reviews.txt
│   ├── users.csv
└──  matched_beer_data
    ├── beers.csv
    ├── breweries.csv
    ├── pickles
    │   ├── df_matched_beer_beers.pkl
    │   └──  ...
    ├── ratings.csv
    ├── ratings_ba.txt
    ├── ratings_rb.txt
    ├── ratings_with_text_ba.txt
    ├── ratings_with_text_rb.txt
    ├── users.csv
    └── users_approx.csv

```

## Research 
1. Are there significant differences in the main ratings between experts and non-experts?
   - Do experts and non-experts exhibit preferences for specific beer styles?
   - Is the distribution of ratings similar between expert and casual users?
2. Do high-volume reviewers have an outside impact on ratings on certain beers?
3. Regarding the reviews made by the two classes, do experts and casual raters use the same vocabulary? And is the sentiment equal for the two classes?
   
## Methods
### Step 1: Data-Loading and Filtering
* Convert first the ``.txt`` files into ``.csv`` for readability.
* Convert and store all files into pickle format to compress data.
* Remove duplicate IDs in the user DataFrame.
* Remove rows where beer IDs, user IDs, and rating are missing.
* Merge the two Datasets BeerAdvocate and RatedBeer together. As there are users on both platforms, it is more relevant to take into account the ratings from both platforms for the definition of “experts”.
### Step 2: Initial Analyses
After looking at the distribution of ratings, it is legit to separate users into two classes. The following steps are then performed
* Define who is a massive rater\
 In order to separate people into two groups, a definition of a massive rater, called from now an "expert" has to be found. The choice was made here to consider the number of ratings per year and aggregate scores from the past 3 years with the formula:
$S_{Y_j} = 2 * R_{Y_{j}} + 0.5 * R_{Y_{j-1}} + 0.25 * R_{Y_{j-2}} + 0.1 * R_{Y_{j-3}}$
, where $R_{Y_j}$ denotes the number of ratings for the year j and $S_{Y_j}$ is the score of the user for the year j.
* The experts are then people from the 0.995 quantile of the score calculated previously (among those who have a non-zero score, i.e., active users).
* Hence, merging the datasets was necessary, as a user may have done only a few ratings on a platform but a lot on the other one. As we want to consider him an expert regardless of a platform, taking into account the number of ratings on both platforms is necessary.
* Analyzing the distribution of ratings over the years made by an expert and non-expert.
### Step 3: Rating analysis
* Analysis of the behavior of the two categories, The purpose of this section is to analyze if the experts are more severe than the rest of the population on the global rating (column 'rating' in the DataFrame).
* Focus on whether experts and the general population share similar preferences when it comes to rating beers. For this investigation, the beers are sorted based on the number of times they were rated. A comparison is then made between the top 10 beers for the two groups.
* See what kind (in terms of popularity) of beer casuals and experts rate.
* Analysis of the beers styles rated by experts and casuals.
* Analysis of how their ratings differentiate (values of the ratings).
* Analysis of the ratings for specific beers.
* Ratings at the beginning of a beer (time evolution analysis).
* Evolution of ratings over time, impact of the experts (bis).
  Try to find beers which have been rated by experts and non-experts at different years to identify if an expert tends to influence the ratings or not (all the results of the analysis are in the notebook).
* Impact of experts at the beginning of a beer
### Step 4: Textual analysis
* Compare the length of the reviews done for both classes.
* Using the TF-IDF approach, compare the most common words and adjectives used by the two classes.
* Compare the sentiment of the two reviews.
## Timeline:
* 11/24: Evolution of ratings over time, impact of the experts, continue analysis on low-rated beers.
* 11/24: Analyze reviews (words) used by an expert and casual.
* 12/05: Sentiment analysis
* 12/12: Interactive plots for rating differences and ratings count for the top 16 most rated beers.
* 12/15: Website page with the data story.

## Organization within the team
* Vincent Roduit :  Data processing, textual analysis
* Vincent Roh : Ratings analysis and Website
* Fabio Palmisano : Ratings analysis and Website
* Yannis Laaroussi : Textual analysis and Website
* Alexi Semiz : Interactive plots and ratings analysis
## Contributors
This project has been done by Vincent Roduit, Alexi Semiz, Yannis Laaroussi, Vincent Roh and Fabio Palmisano as a mandatory part of the course "CS-401: Applied Data Analysis" given at Ecole Polytechnique Fédérale de Lausanne during the Fall semester of 2023.
