import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image


st.set_page_config(page_title="Kotug datastory | CIEM 6302", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

mystyle = '''
    <style>
        p {
            text-align: justify;
        }
    </style>
    '''

st.markdown(mystyle, unsafe_allow_html=True)

# ---- LOAD ASSETS ----
lottie_team = load_lottieurl("https://lottie.host/3222fdf4-a2db-402c-8f80-890562c701a3/aOXHckBb8p.json")
img_kotug_tug = Image.open("images/Kotug-tug.jpg")
img_kotug_80s = Image.open("images/Kotug-80s.jpg")

########################################
# ---- END of settings, START of content
########################################

# ---- HEADER ----
with st.container():
    st.subheader("CIEM6302: Project datastory")
    st.title("Tug boats pick-up and drop-off predictions")
    st.divider()

# ---- INTRO chapter ----

with st.container():
    text_column, video_column = st.columns([3,1])
    with text_column:
        st.header("Introduction")
        st.write("""
                 Just as take-off and landing are the most critical phases of air travel, the same can be said for journeys on water. Navigating vessels within a port is no easy task, especially when dealing with large vessels in tight spaces. This is where tugboats come into play, serving to anchor and safely manouver these ships.")
                 
                 In the port of Rotterdam, harbour towage services are provided by KOTUG International. Tugboats, often referred to as tugs, are dispatched to pick up or drop off vessels upon request, and there are no location restrictions. Consequently, the varying locations pose a significant challenge when it comes to estimating the number and location of tugs required in advance. These estimations are vital for efficient work scheduling, minimizing response times, and enhancing fleet utilization.
                 
                 With the aim of living up to its company slogan \"Ahead in maritime excellence,\" KOTUG International seeks to explore alternative approaches and improve prediction accuracy. This endeavour has led to collaboration with students from TU Delft participating in course CIEM 6302.
                 """
                 )
    with video_column:
        st.image(img_kotug_tug)
        st.write("> [KOTUG in 80 seconds (YouTube video)](https://www.youtube.com/watch?v=tj4cJAnWdkg)")

# -- The team --

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Our team")
        st.write(
            """
            This work was created as a group project for the course CIEM 6302 Advanced Data Science for Traffic and Transportation Engineering at TU Delft. Our team members are:
            - Haodong Li
            - Martin Marek
            - Maurik Moerenhout
            - Paolo Pantano
            
            We would like to acknowledge the contribution of a former group member, Merel Loman, who worked on data collection and preparation phases. We would also like to express our gratitude to all the teachers and stakeholders for their continuous support, assistance, and valuable feedback throughout the project.
            """
        )
    with right_column:
        st_lottie(lottie_team, height=300, key="tea")


# ---- DATA chapter ----

with st.container():
    st.divider()
    st.header("Data")
    st.subheader("Data collection")
    st.write("""
             We were able to gather AIS data (with 5-minute step) for whole year 2022 and received towage data of Kotug’s tugs from 6/2022 to 7/2023. Tide data, wind speed and direction comes from weather station at Hoek von Holland, all obtained through KNMI.

             Horizontal visibility is not provided at that station, and we unfortunately haven’t found any (reliable) source in that area. We also haven’t found sufficient data to make a computation how loaded the vessel is. Our idea was that half loaded vessel, for example, may be different to navigate, in terms of manoeuvrability or wind resistance as empty or fully loaded one.

             """)
    st.subheader("Visualization")
    st.write("""
             Main challenge is that the data are heavily corelated. Width of the ship is very much dependant on its length, the same goes for destination of ships. Particular berths are designed for certain type of vessels such as cargo, tanker, etc.
             
             AIS data are also dirty as the coordinates are not rarely placed on land, abruptly jump far away, and come back after a few steps, name of the ships varies and so on. These imperfections make it very hard to correct the data automatically; manual correction isn’t feasible in reasonable time
             
             Taken that into account, the most reliable identifier of a vessel is MMSI. We excluded ships smaller than 120m as these generally don't need tugboats.
             """)
    st.subheader("Data relationships")
    st.write("""
             To see relationships in the data we use dot plots of the pickup and dropoff locations and make heatmaps of these plots. The heatmaps are made by making classification in the data, and then plotting for the pickups and dropoffs of these classes. Differences between the plot can indicate relationships between the data and the locations of pickup and dropoff locations.
             
             Some changes are visible but no clear trend among the pick-up/drop-off locations. Tides and water level have no significant impact and are excluded from further use.
             """)
    st.subheader("Data preparation")
    st.write("""
            For better computation performance, we processed the obtained data in a following way:
             
             - Compress AIS data: we dont need trajectories, only unique properties of each ship and their first timestamp in the area.
             - Weather data should be formatted at the same timestamps as the AIS data
             - Merge the AIS data, KNMI weather data, and historic towage data based on common identifiers or timestamps.
             
             Standard trajectory per haven was computed as they tend to be almost identical, which was confirmed by Kotug. We used our own clustering method based on HDBSCAN and K-means as we haven’t found any sufficient Python package.
             
             Each position on the line is represented in 0 to 1 range of values. 0 stand for start, 1 is the last point (berth).

             """)

# ---- MODEL chapter ----

with st.container():
    st.divider()
    st.header("Model")
    st.subheader("Machine learning model")
    st.write("We use linear regression model since we are predicting the location. As the berth or haven of a vessel is predefined, the solution space for the linear regression model can be compressed significantly.")

with st.expander("Used data"):
    left_column, center_column, right_column = st.columns(3)
    with left_column:
        st.write("""
                AIS:
                 - Time
                 - Length of ship
                 - Draft of ship
                 - Width of ship
                 """)
    with center_column:
        st.write("""
                 Weather KNMI:
                 - FH: Hourly average wind speed in m/s
                 - DD: Wind direction averaged over the last 10 minutes
                """)
    with right_column:
        st.write("""
                 Historic towage data:
                 - Vessel: MMSI
                 - Type: leaving, arriving, switching
                 - From time
                 - To time
                 - Tugs
                 - From location per tug
                 - To location per tug
                 - Berth and haven destination/departure
                 """)


st.subheader("Model training and evaluation")
st.write("We only use data from 2022/06 to 2022/12, as historic towages only has data from 2022/06 to 2023/06, and the weather data is only from 2022. Therefore, the chosen period overlaps these two. This means that we have half a year of data.")

st.write("""
        Model setup
         - Haven as a dummy variable
         - Input from 0 to 1
         - No hidden layers
         - Simple regression model
         - Callback with patience 10
         
         The training dataset is rather small, consisting of thousands of towages as there are only around 30-40 records per day. Some berth locations are also more frequent than others so there is no enough data for proper trajectory training and estimation.
         """)

# ---- RESULTS chapter ----

st.divider()
st.header("Results")



# ---- SUMMARY chapter -----

st.divider()
st.header("Summary")


