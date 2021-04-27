"""
Class: MA346
Name: Rashmi Rajesh
Description: Final Project
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#In order to create the dashboard, I first included code that would set up the title and explain how the dashboard would work
st.title("Factors that Influence the Gender Pay Gap")
st.write("By: Rashmi Rajesh")
st.subheader("About the Gender Pay Gap")
st.write("The gender wage gap is the difference between the wages earned by men versus those by women. There are a multitude of factors "
         "that create this gap including differences in industries or jobs worked, differences in years of experience, differences in hours "
         "worked, and discrimination which is the focus of this dashboard.")
st.write("In order to utilize this dashboard, you can select the factor of discrimination in the select boxes on the right to look at the data used"
         "while also using the select box to look at heatmap analyses of how significant each factor of discrimination is to exacerbating the pay gap"
         "in the United States")
st.write("The diversity factors include political affiliation, political ideology, and diversity by state. Political Affiliation is defined as Number "
         "of Citizens in a State that Identify as 'Democrat', 'Republican', or 'Independent'. Political Ideology is defined by the Number of Citizens that Identify"
         "as 'Moderate', 'Conservative', or 'I don't know.' Lastly, Diversity is represented via a variety of races: 'Hispanic (of any race)', 'Non-Hispanic White', "
         "'Non-Hispanic Black', 'Non-Hispanic Asian', 'Non-Hispanic American Indian'")
st.write("It is important to understand all data was provided in percentages of the population that identified as a particular factor. Another important aspect is to appropriately define the term percent gap as it is used in this report. The percent gap represents the amount of pay a woman receives expressed in a percent of that received by her male counterpart. For example, in the state of Massachusetts, the percent gap is 81.28%. This means a Massachusetts woman, on average, receives 81.28% if the pay her male counterpart receives, or simply about 82 cents for every 1 dollar earned by her male counterpart.")
# I added a selectbox to the sidebar so that users can manipulate the dataframe on the dashboard so that they can look at each dataframe separately:
selectbox1 = st.sidebar.selectbox(
    'Category of Dataframe',
    ('Political Affiliation By State', 'Political Ideology By State', 'Diversity By State', 'Pay Gap By State')
)
#The dataframes represent the different datasets I used to manipulate the data. These will be displayed on the dashboard so users can look through the data themselves

#I added another selectbox to isolate the heatmaps so users can select a particular factor to then generate a heatmap
selectbox2 = st.sidebar.selectbox(
    'Analysis of Factors',
    ('Political Affiliation', 'Political Ideology', 'Diversity')
)
#Each of the heatmaps will have an analytical explanation for the user

#next I imported the csv files for all of the data
affiliation = pd.read_csv('political_affiliation_by_state.csv', index_col=False)
paygap = pd.read_csv('pay_gap_by_state.csv', index_col=False)
ideology = pd.read_csv('political_ideology_by_state.csv', index_col=False)
diversity = pd.read_csv('diversity_by_state.csv', index_col=False)
#I labeled each of the excel files as the factor of diversity they represented

#I started with cleaning affiliation datframe by renaming the three political factors into Republican, Democrat, and Independent
affiliation.rename(columns={'Republican/lean Rep.':'Republican', 'No lean':'Independent', 'Democrat/lean Dem.':'Democratic'}, inplace=True)
affiliation.drop('Sample Size', axis=1, inplace=True)
affiliation['Republican'] = affiliation['Republican'].replace({'%': ''}, regex=True)
affiliation['Independent'] = affiliation['Independent'].replace({'%': ''}, regex=True)
affiliation['Democratic'] = affiliation['Democratic'].replace({'%': ''}, regex=True)
#I also removed the % at the ends of each number and at the end of the cleaning, I will make them floats to use in my heatmaps

#Next, I cleaned the paygap dataframe by renaming the columns into State and Percent Gap.
paygap.rename(columns={'U.S. gender pay gap by state 2019':'State', 'Unnamed: 1':'Percent Gap'}, inplace=True)
paygap = paygap.iloc[2:]
paygap.drop('Unnamed: 2', axis=1, inplace=True)
#I dropped the last column as it did not have any data I needed

#Next, I cleaned the ideology dataframe
ideology.drop('Sample Size', axis=1, inplace=True)
ideology['Conservative'] = ideology['Conservative'].replace({'%': ''}, regex=True)
ideology['Moderate'] = ideology['Moderate'].replace({'%': ''}, regex=True)
ideology['Liberal'] = ideology['Liberal'].replace({'%': ''}, regex=True)
ideology["Don't know"] = ideology["Don't know"].replace({'%': ''}, regex=True)
#I didn't have to rename anything, but I did have to remove the % at the ends of each number and at the end of the cleaning, I will make them floats to use in my heatmaps

#Lastly, I cleaned the diversity dataframe
diversity['Hispanic (of any race)'] = diversity['Hispanic (of any race)'].replace({'%': ''}, regex=True)
diversity['Non-Hispanic White'] = diversity['Non-Hispanic White'].replace({'%': ''}, regex=True)
diversity['Non-Hispanic Black'] = diversity['Non-Hispanic Black'].replace({'%': ''}, regex=True)
diversity['Non-Hispanic Asian'] = diversity['Non-Hispanic Asian'].replace({'%': ''}, regex=True)
diversity['Non-Hispanic American Indian'] = diversity['Non-Hispanic American Indian'].replace({'%': ''}, regex=True)
#Once again, I didn't have to rename anything, but I did have to remove the % at the ends of each number and at the end of the cleaning, I will make them floats to use in my heatmaps

#Now I needed to merge all dataframes. Since all the dataframes had the unique key of state, I did an outer join on state in a new dataframe I called combine
combined = affiliation.merge(ideology, how='outer', on = 'State')
combined = combined.merge(diversity, how='outer', on = 'State')
combined = combined.merge(paygap, how='outer', on = 'State')

#Next, I worked to clean the data, by turning all the objects into float numbers to be able to manipulate in my heatmaps
combined['Republican'] = combined['Republican'].astype(float)
combined['Independent'] = combined['Independent'].astype(float)
combined['Democratic'] = combined['Democratic'].astype(float)
combined['Conservative'] = combined['Conservative'].astype(float)
combined['Moderate'] = combined['Moderate'].astype(float)
combined['Liberal'] = combined['Liberal'].astype(float)
combined["Don't know"] = combined["Don't know"].astype(float)
combined['Hispanic (of any race)'] = combined['Hispanic (of any race)'].astype(float)
combined['Non-Hispanic White'] = combined['Non-Hispanic White'].astype(float)
combined['Non-Hispanic Black'] = combined['Non-Hispanic Black'].astype(float)
combined['Non-Hispanic Asian'] = combined['Non-Hispanic Asian'].astype(float)
combined['Non-Hispanic American Indian'] = combined['Non-Hispanic American Indian'].astype(float)


#Now, in order to display dataframes of each fact, based on user selection I used streamlit to set the selectbox as each factor
if selectbox1 == 'Political Affiliation By State':
    st.subheader(f'The dataframe for Political Affiliation By State :')
    st.dataframe(affiliation)
if selectbox1 == 'Political Ideology By State':
    st.subheader(f'The dataframe for Political Ideology By State :')
    st.dataframe(ideology)
if selectbox1 == 'Diversity By State':
    st.subheader(f'The dataframe for Diversity By State :')
    st.dataframe(diversity)
if selectbox1 == 'Pay Gap By State':
    st.subheader(f'The dataframe for Pay Gap By State :')
    st.dataframe(paygap)
#when the user selects a factor in the side bar, the dashboard will display the appropriate dataframe

#I did the same user selection in the sidebar, but this time for the heatmaps and their corresponding analysis based on the discrimination factor selected
st.subheader("What does the Data Mean?")
st.write("In order to determine how variables the variables were correlated, I utilized correlation coefficients to identify the extent to which the variables influence the pay gap. A positive correlation means that the more a state identifies with a particular factor, the higher the percent gap. This is not a bad thing, as the percent gap in this report is defined as the of pay a woman receives as a percent of the pay of her a male counterpart. A high percentage means that the dollar amount of man and woman worker is about equal. In the same regard, if the factor is negatively correlated with the pay gap, that means the more a state identifies with a particular factor, the lesser the percent gap, which indicated that the dollar amount a woman receives is significantly less than a male.  ")
if selectbox2 == 'Political Affiliation':
    st.subheader(f'Political Affiliation:')
    combined_political = combined[['Republican', 'Independent', 'Democratic', 'Percent Gap']]
    correlation_coefficients_b = np.corrcoef(combined_political, rowvar=False)
    sns.heatmap(correlation_coefficients_b, annot=True)
    plt.xticks(np.arange(4)+0.5, combined_political.columns, rotation=90)
    plt.yticks(np.arange(4)+0.5, combined_political.columns, rotation=0)
    plt.title('Political Party')
    st.write("Analysis of Heatmap: The correlation heatmap illustrated significant results for political affiliation. To start, the data illustrated that identification as democratic tend to result in a higher percent paygap, while identification as republican tend to result in a lower percent paygap. There is a high positive correlation of 0.62 between the factor democratic and paygap versus a negative correlation of -0.68 between the factor republican and paygap. This means that states that identified as democratic tended to have women who received a high percentage of the pay received by their male counterpart as opposed to republican states. ")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
if selectbox2 == 'Political Ideology':
    st.subheader(f'Political:')
    combined_ideology = combined[['Conservative', 'Liberal', 'Moderate', 'Percent Gap']]
    correlation_coefficients_a = np.corrcoef(combined_ideology, rowvar=False)
    sns.heatmap(correlation_coefficients_a, annot=True)
    plt.xticks(np.arange(4)+0.5, combined_ideology.columns, rotation=90)
    plt.yticks(np.arange(4)+0.5, combined_ideology.columns, rotation=0)
    plt.title('Political Ideology')
    st.write("Analysis of Heatmap: The correlation heatmap illustrated significant results for political ideology. To start, the data illustrated that identification as liberal tend to result in a higher percent paygap, while identification as conservative tend to result in a lower percent paygap. There is a high positive correlation of 0.58 between the factor liberal and paygap versus a negative correlation of -0.61 between the factor conservative and paygap. This means that states that identified as liberal tended to have women who received a high percentage of the pay received by their male counterpart as opposed to conservative states. ")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
if selectbox2 == 'Diversity':
    st.subheader(f'Diversity:')
    combined_diversity = combined[['Hispanic (of any race)', 'Non-Hispanic White', 'Non-Hispanic Black', 'Non-Hispanic Asian', 'Non-Hispanic American Indian', 'Percent Gap']]
    correlation_coefficients_c = np.corrcoef(combined_diversity, rowvar=False)
    sns.heatmap(correlation_coefficients_c, annot=True)
    plt.xticks(np.arange(6)+0.5, combined_diversity.columns, rotation=90)
    plt.yticks(np.arange(6)+0.5, combined_diversity.columns, rotation=0)
    plt.title('Diversity')
    st.write("Analysis of Heatmap: The correlation heatmap illustrated mixed results for diversity. To start, the data illustrated that identification as liberal tend to result in a higher percent paygap, while identification as conservative tend to result in a lower percent paygap. There is a moderate positive correlation of 0.22 between the factor Hispanic (of any race), a negative correlation of -0.38 between the factor Non-Hispanic White and paygap, a small positive correlation of 0.02 between the factor Non-Hispanic Black and paygap, a positive correlation of 0.49 between Non-Hispanic Asian and paygap, and a small negative correlation between Non-Hispanic American Indian. The correlations are too small to definitively identify any significant correlation for all ethic groups. However, the moderate -0.38 correlation in the Non-Hispanic White and moderate 0.49 correlation in the Non-Hispanic "
             "Asian group, tend to concur with typical trends where white women face the gender wage gap more often than Asian women, which can illustrate that there are instances where Asian women are paid a wage much more closer to that of their male counterparts than white women.")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
#when the user selects a factor in the side bar, the dashboard will display the appropriate heatmap and corresponding analysis


