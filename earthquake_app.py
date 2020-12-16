"""
Class: CS230--Section HB1 
Name: Rashmi Rajesh
Description: (Give a brief description for Exercise name--See below)
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""
import matplotlib.pyplot as plt
import time
import streamlit as st
import pandas as pd

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

st.title("Earthquake Data for Data Collecting Regions")
st.write("By: Rashmi Rajesh")
st.subheader(
    "Select a location code from the dropdown box to analyze the location's accuracy in predicting earthquakes")
earthquake = pd.read_csv("earthquakes.csv")
# st.dataframe(earthquake)
"Location Codes: "
var = {"ak": "Alaska Earthquake Center",
       "ci": "California Integrated Seismic Network: Southern California Seismic",
       "nn": "Nevada Seismological Laboratory",
       "nc": "California Integrated Seismic Network: Northern California Seismic",
       "us": "USGS National Earthquake Information Center, PDE",
       "hv": "Hawaii Volcano Observatory",
       "ok": "Oklahoma Earthquake Center",
       "pr": "Puerto Rico Seismic Network",
       "mb": "Montana Bureau of Mines and Geology",
       "uu": "University of Utah Seismograph Stations",
       "uw": "Pacific Northwest Seismic Network",
       "nm": "New Madrid Seismic Network",
       "av": "Alaska Volcano Observatory",
       "se": "Center for Earthquake Research and Information"}
st.write(var)

#function for piechart
def piechart(data, title, labels):
    plt.pie(data, labels=labels, autopct='%1.2f%%')
    plt.title(title)
    plt.show()
    pass

query2_filtered = earthquake[earthquake['type'] == 'earthquake']
option = st.sidebar.selectbox('Pick Location Code', earthquake['locationSource'])
st.title("Region Specific Data")
'You selected:', option, '-', var.get(option)
df = query2_filtered[query2_filtered['locationSource'] == option]
averageRMS = df[['rms']].mean()
st.write("The average RMS: ", averageRMS)

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'Visualization Type',
    ('Dataframe', 'Histogram', 'Map')
)
add_selectbox2 = st.sidebar.selectbox(
    'Overall Data',
    ('Pie Chart', 'Bar Chart')
)

if add_selectbox == 'Dataframe':
    st.subheader(f'The dataframe for {option} :')
    st.dataframe(df)
if add_selectbox == 'Histogram':
    # histogram
    st.subheader("Magnitude of Earthquakes in This Location On Richter Scale")
    queryHist = pd.DataFrame(earthquake, columns=['type', 'mag', 'locationSource', 'latitude', 'longitude'])
    queryHist_filtered = queryHist[queryHist['type'] == 'earthquake']
    queryHist_filtered2 = queryHist_filtered[queryHist_filtered['locationSource'] == option]
    df3 = pd.DataFrame(queryHist_filtered2[:len(queryHist_filtered2)], columns=['mag'])
    st.set_option('deprecation.showPyplotGlobalUse', False)
    df3.hist()
    st.pyplot()
if add_selectbox == 'Map':
    st.subheader("Map of Earthquakes in Selected Region")
    queryHist = pd.DataFrame(earthquake, columns=['type', 'mag', 'locationSource', 'latitude', 'longitude'])
    queryHist_filtered = queryHist[queryHist['type'] == 'earthquake']
    queryHist_filtered2 = queryHist_filtered[queryHist_filtered['locationSource'] == option]
    st.map(queryHist_filtered2)

st.title("Overall Earthquake Data")
if add_selectbox2 == 'Pie Chart':
    #piechart for query 1
    print(query2_filtered['status'].value_counts())
    labels = ("Automatic", "Reviewed")
    CountStatus = query2_filtered['status'].value_counts()
    title = "PieChart"
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(piechart(CountStatus,title, labels))
if add_selectbox2 == 'Bar Chart':
    q2 = pd.DataFrame(earthquake, columns=['type','locationSource','rms'])
    q2_filtered = q2[q2['type'] == 'earthquake']
    query2rms = pd.DataFrame(query2_filtered, columns=['locationSource','rms'])
    d = {k: g["rms"].tolist() for k,g in query2rms.groupby("locationSource")}

    averages = {}

    for location, rms in d.items():
        average = sum(rms)/len(rms)
        averages[location] = average

    #print(averages)
    keys = averages.keys()
    values = averages.values()
    plt.ylabel("Average RMS")
    plt.xlabel("Location Code")
    plt.title("Average RMS values per Locations")
    plt.bar(keys,values)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(plt.show())
st.subheader("Map of All Earthquakes: ")
st.map(query2_filtered)
