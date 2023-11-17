## Abstract
There are two types of users: extensive raters and occasional raters. It is reasonable to question whether this difference has an impact on the ratings. These extensive raters could be some kind of experts, such as people working in a brewery, but they can also be beer enthusiasts without professional skills. As a beer company releasing a new product, the following question may arise: *Should the company place more trust in ratings from these extensive raters?* To answer this question, analyses of the ratings statistics have to be done to find if the experts have an impact on the ratings. The analysis is first focused on finding relevant differences that can assess whether the difference between the two classes is significant. Secondly, the analysis is focused on more precise questions to understand if extensive raters are responsible for the success of a beer or not.  
## Research 
1. Are there significant differences in the main ratings between experts and non-experts ? \
   a) Do experts and non-experts exhibit preferences for specific beer styles ? \
   b) Is the distribution of ratings similar between expert and casual users ?
2. Do high volume reviewers have an outside impact on ratings on certain beer ?
3. By constructing a model taking into account the difference between experts and casual raters, can we produce a model that can predict the rating of a beer ?
## Methods
### Step 1: Data-loading and filtering
* Convert first the ``.txt`` files into ``.csv`` for readability.
* Convert and store all files into pickle format to compress datas.
* Remove duplicate IDs in user DataFrame.
* Remove rows where beer IDs, user IDs and rating are missing (other missing values are not important for now but has to be taken into consideration for further analysis).
* Merge the two Dataset BeerAdvocate and RatedBeer together. As there are users on both platforms, it is more relevant to take into account the ratings from both platforms for our definition of “experts”.
### Step 2: Inital Analyses
* Define who is a massive rater\
 In order to separate people in two groups, a definition of a massive rater, called from now an "expert" has to be found. The choice was made here to consider the number of ratings per year and aggregate scores from the past 3 years with the formula:
$S_{Y_j} = 2 * R_{Y_{j}} + 0.5 * R_{Y_{j-1}} + 0.25 * R_{Y_{j-2}} + 0.1 * R_{Y_{j-3}}$
, where $R_{Y_j}$ denotes the number of ratings for the year j and $S_{Y_j}$ is the score of the user for the year j.
* The experts are then people from the 0.995 quantile of the score calculate previously (among those who have a non-zero score i.e active users).
* Hence, merging the datasets was necessary, as a user may have done only few ratings on a platform but a lot on the other one. As we want to consider him an expert regardless of a platform, taking into account the number of ratings on both platforms is necessary.
* Analyzing the distribution of ratings over the years made by an expert and non-expert.
* Analysis of the behavior of the two categories,The purpose of this section is to analyze if the experts are more severe than the rest of the population on the global rating (column 'rating' in the DataFrame).
* Focus on whether experts and the general population share similar preferences when it comes to rating beers. For this investigation, the beers are sorted based on the number of times they were rated. A comparison is then made between the top 10 beers for the two groups.
* See what kind (in terms of popularity)of beer casuals and expert rate.
* Analysis on the beers styles rated by experts and casuals.
* Analysis on how their ratings differentiate (values of the ratings).
* Analysis of the ratings for specific beers.
* Ratings at the beginning of a beer (time evolution analysis).
* Evolution of ratings over time, impact of the experts (bis). \
  Try to find beers which have been rated by expert and non experts at different years in order to identify if an expert tends to influence the ratings or not
(all the results of the analysis are in the notebook).



## Timeline:
* 11/24: Evolution of ratings over time, impact of the experts, continue analysis on low rated beers. (end)
* 11/24 : Analyze reviews (words) used by an expert and casual. (start)
* 11/24: Interactive map of the location of the experts. (start)
* 12/08: Machine learning to predict the ratings of a beer (start)
* 12/08: Reviews analysis (end) + access how to display the results in an insightful way. (start)
* 12/08: Interactive map. (end)
* 12/08 : Building the website page with the data story. (start).
* 12/15 Machine learning to predict the ratings of a beer (end)
* 12/21 Finish the website, clean the code and share our data story
## Organization within the team, for the milestone 3 we decided to split the work as follows :
* Vincent Roduit :  Evolution of ratings over time, impact of the experts, continue analysis on low rated beers. (end)
* Vincent Roh : Interactive map of the location of the experts. (start)
* Fabio Palmisano : Machine learning to predict the ratings of a beer (start)
* Yannis Laaroussi : Analyze reviews (words) used by an expert and casual. (start)
* Alexi Semiz : Building the website page with the data story. (start)

	 
## Questions for TA's
For the expert analysis, both sites were considered, regardless of where the ratings were submitted, as the rating grades were similar for both sites. However, for milestone 3, incorporating additional grading parameters (aroma, palate) raised the necessity of treating each site separately. This was due to the differing scales of these parameters between the sites; some ranged from 1 to 10, while others ranged from 1 to 5. Despite attempts to rescale them, statistical tests revealed a significant difference. Consequently, we conclude that merging the sites is not viable, and the analysis needs to be conducted separately for each site. Is this approach relevant for the analysis with these additional parameters?
