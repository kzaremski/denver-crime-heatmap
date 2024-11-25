# Project Proposal
### Introduction & Description
After my car was vandalized in Denver earlier this October, I began ruminating on what makes an area “safe”. Eventually I came upon the Denver Public Crime Map which shows the 1000 most recent incidents on a map. This got me interested in the possibility of using this data in a predictive capacity. I am going to build a Denver crime prediction or likelihood map app, that will predict the likelihood of crime overall, predict the most likely crimes to be committed for different areas, and then present this as a heatmap visualization to the user.

### Dataset
The source dataset for the public crime map is provided by Denver and contains 394,475 data points sourced from the FBI’s NIBRS database. After stripping off useless columns such as database keys and precinct numbers, the usable columns are the date and time of occurrence, type and category of crime, and longitude and latitude. Crimes do not happen because of a longitude and latitude value, so I am enriching the original dataset by adding additional features by querying each data point against Open Street Map data for land use, proximity to residential or main roads, building types, and amenities such as ATMs or RTD stations.

### Model
I will be training two models to make predictions for my app: one model to enable the prediction of the total amount of crimes in an area given input features, and another model to perform multiclass classification to predict what type of crime is most likely to be committed in an area given input features. Since the input data and resulting crime or number of crimes is known and labeled, supervised learning models are best suited for this data. I will be using SciKit Learn’s HistGradientBoostingClassifier to predict crime type and HistGradientBoostingRegressor to predict crime volume. I am electing to use gradient boosting over decision trees or other models since it has a lower bias and should be more sensitive to different crime patterns.
 
### App Functionality
The web app will be a simple map interface with a color heatmap overlay based on the underlying model’s crime predictions. The user will have options for a time delta, where they can view the heatmap/predictions for the current time plus or minus up to 48 hours. The user will have a way to toggle between seeing a multi-color heatmap for the types of crimes that are predicted, a single-color heatmap for the likelihood or predicted frequency of crime, and a heatmap that combines both, with areas having a lower predicted likelihood or frequency of crime being denoted by a more transparent version of the color representing the crime type for that area.
 
### Technical Implementation
Since the app does not have user accounts, the backend can be implemented as a simple Flask app with an API endpoint to retrieve the heatmap overlay based on the map area the client says the user is currently viewing. Predictions will be stored in an SQLite database where they can be quickly retrieved to generate a heatmap at view time. The frontend will be implemented using simple HTML, CSS, and vanilla JavaScript to enable interactions. The map itself will be rendered using the Leaflet JavaScript map library/project.

### Feasibility
Since the app itself is a visualization with only a few buttons/interactions, and no user accounts or user data collection, it will be simple to implement, which will allow for more time to be spent on tuning the models and finding the optimal way to slice the map or bin data.
