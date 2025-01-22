# anchor-kenya-waterbasin
Online app commissioned by Anchor Environmental to analyze Kenyan water basins

App takes csv file input which contains 'scores' for different pieces of information about the Kenyan water basins. These scores are used to produce an 'overall score' which tells the user which water basins shuold be invested in. 
App allows the user to choose different weightings for each of the scores, which changes the overall score depending on which components of the score are considered most important.
Once the user has given their chosen weightings, the app generates a choropleth map and various tables and graphs that clearly demonstrate which water basins have higher scores

App uses streamlit to create interface and geopandas to generate choropleth map as well as pandas and plotly for other graphs
