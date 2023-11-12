import os
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import datetime
import statsmodels.api as sm
from dateutil.relativedelta import relativedelta
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go


migrant_App = pd.read_csv('migrant_clean.csv', index_col=None)
timeseriesdf = pd.read_csv('timeseriesdf.csv')
migrant_API_RESTAURANTS =  pd.read_csv('venue_data_RESTAURANTS.csv', index_col=None)
migrant_API_NORESTAURANTS =  pd.read_csv('venue_data_NORESTAURANTS.csv', index_col=None)
timeseriesdf['date'] = pd.to_datetime(timeseriesdf['date'])
timeseriesdf.set_index('date', inplace=True)

column_names = migrant_App.columns
print(column_names)

st.set_page_config(page_title="Migrant Web App", page_icon=":tada:", layout="wide")

# Create a multiselect for navigation
selected_sections = st.sidebar.selectbox("Select Section", ["Introduction","Data Exploration (EDA)", "Modeling"])

introduction ="""
        
         Migration is a globally significant phenomenon with far-reaching impacts on 
         economies and societies. Our project analyzes the Global Missing Migrants 
         dataset to uncover the key factors contributing to migration incidents and 
         develop predictions for future occurrences. This application empowers users 
         to understand the likelihood of such incidents, providing valuable insights 
         for a safer migration experience and informed policy development.
         
         Introducing our app, it offers two core features: Exploratory Data Analysis 
         (EDA) and Time Series Analysis. Our EDA section provides insights into the 
         dataset, while the Time Series component allows users to predict future 
         migration incidents based on input parameters. """

if "Data Exploration (EDA)" in selected_sections:
    # Main content
    st.header("Migrant Data Analysis")
    st.write("""To provide an overview of the historical data related to missing migrants, 
    we present an initial exploration of the dataset before applying specific filters. Below, 
    you'll find a comprehensive table, bar chart, and geographic map summarizing key statistics 
    aggregated across all regions of incident. This preliminary analysis aims to offer a broad 
    perspective on the dataset's characteristics.""")
    
    st.markdown("<h1 style='text-align: left; color: blue; font-size: 21px;'>Preliminary Analysis:</h1>", unsafe_allow_html=True)
    1
    # Survival rate throughout the year
    migrant_App['incident year'] = migrant_App['incident year'].astype(int)
    overall_survival_rate_by_year = migrant_App.groupby('incident year').apply(lambda x: x['number of survivors'].sum() / (x['total number of dead and missing'].sum() + x['number of survivors'].sum())).reset_index(name='overall_survival_rate')
    st.markdown("<p style='text-align: center; color: yellow; font-size: 18px;'>Overall Survival Rate Throughout the Years:</p>", unsafe_allow_html=True)
    st.line_chart(overall_survival_rate_by_year.set_index('incident year')['overall_survival_rate'], use_container_width=True)

    # Country with most migrants
    st.markdown("<p style='text-align: center; color: yellow; font-size: 18px;'>Number of Migrants Per Country:</p>", unsafe_allow_html=True)
    country_counts = migrant_App['country of origin'].value_counts()
    st.bar_chart(country_counts)

    # Most migration route
    st.markdown("<p style='text-align: center; color: yellow; font-size: 18px;'>Migration Route Distribution:</p>", unsafe_allow_html=True)
    migration_route_counts = migrant_App['migration route'].value_counts()
    st.bar_chart(migration_route_counts)

    top_regions_origin = migrant_App['region of origin'].value_counts().head(15)
    #st.write(top_regions_origin)
    top_countries_origin = migrant_App['country of origin'].value_counts().head(15)
    #st.write(top_countries_origin)
    top_extracted_countries = migrant_App['extracted country'].value_counts().head(15)
    #st.write(top_extracted_countries)

     
    # Assuming 'region of incident' contains the regions where incidents occurred
    top_countries = migrant_App['extracted country'].value_counts().head(15)

    # Plotting the distribution
    st.markdown("<p style='text-align: center; color: yellow; font-size: 18px;'>Top 15 Countries Where Migrants Died:</p>", unsafe_allow_html=True)
    fig_bar = px.bar(top_countries, x=top_countries.index, y=top_countries.values, labels={'y': 'Number of Incidents'})
    fig_bar.update_xaxes(title_text='')
    st.plotly_chart(fig_bar)

       
    # Sidebar
    st.sidebar.header("User Inputs")
    incident_year = st.sidebar.slider("Select Incident Year", 2014, 2023)
    region_of_origin = st.sidebar.selectbox("Select Region of Incident", migrant_App["region of incident"].unique())
    #number_of_males = st.sidebar.number_input("number of males", min_value=0)

       
    #  data by "Region of Origin"
    filtered_data = migrant_App.by("region of incident").agg({
        "number of males": "sum",
        "number of females": "sum",
        "number of children": "sum"
    })

    st.markdown("<p style='text-align: center; color: yellow; font-size: 18px;'>Geopraphical Distribution of Incidents:</p>", unsafe_allow_html=True)
    # Display the geo map 
    fig = px.scatter_geo(
        migrant_App,
        lat='latitude',
        lon='longitude',
        color='total number of dead and missing', 
        size='total number of dead and missing',
        hover_name='region of incident',
        hover_data=['number of dead', 'number of survivors', 'country of origin'],  
        projection='natural earth',
        #title='Geographical Distribution of Incidents',
        labels={'total number of dead and missing': 'Incident Count'},
        height=600,  
        width=800,   
        size_max=15,  
        
    )
    st.write("""For a spatial perspective, the interactive map below displays incident locations. Each point on the map 
    represents a specific incident, allowing users to explore the geographical distribution of missing migrant cases.
    This visual tool adds another layer of insight to the initial dataset exploration.""")
    #fig.update_layout(title=dict(text='Geographical Distribution of Incidents', font=dict(size=20, color='blue')))
    
    st.plotly_chart(fig, use_container_width=True)
        
    # Display the aggregated data
    st.markdown("<p style='text-align: center; color: yellow; font-size: 18px;'>Aggregated Data by Region:</p>", unsafe_allow_html=True)
  
    st.write(f"The table below aggregates number of incidents, categorized by region of incidents and gender across all recorded years.")
    ed_data.columns = [f"{col.upper()}" for col in ed_data.columns]
    st.dataframe(ed_data)
    
    #st.markdown("<h1 style='text-align: left; color: blue; font-size: 21px;'>Population Breakdown by Gender and Region:</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: yellow; font-size: 18px;'>Population Breakdown by Gender and Region:</p>", unsafe_allow_html=True)
    st.write(f"""Complementing the table above, this bar chart visually represents the distribution of incidents across different regions. 
    Each bar corresponds to a region of incident, and its height indicates the total number of incidents in that region. This visualization
    aids in identifying regions with higher incident rates.""")

    # Plot the results (we can customize other chart types)
    st.bar_chart(ed_data)

    st.markdown("<p style='font-size: 15px; font-style: italic;'>Note: The above statistics and visualizations provide a preliminary understanding of the dataset. For a more focused analysis, feel free to use the sidebar filters to explore data for a specific incident year and region of incident</p>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: left; color: blue; font-size: 21px;'>Analysis Results:</h1>", unsafe_allow_html=True)
    st.write("""To the left, you will find a menu of user inputs where you can explore and analyze the historical data related to missing migrants. 
    You can filter the data based on two criterias: year and region of incident. This analysis will help you gain insights into the patterns and 
    characteristics of incidents involving missing migrants. Additionally, we present visualizations depicting the geographical distribution of incidents,
    along with an overview of demographic data by region.  """)
    
    # User inputs
    st.markdown("<p style='text-align: left; color: Yellow; font-size: 18px; font_weight: bold'>User Inputs:</p>", unsafe_allow_html=True)
    st.write(f"Incident Year Of: <span style='color:yellow;font-weight: bold'>{incident_year}</span>", unsafe_allow_html=True)
    st.write(f"Incident Origin: <span style='color:yellow; font-weight: bold'>{region_of_origin}</span>", unsafe_allow_html=True)
    st.write(f"The information below represents the statistics and categories of the specified seletions")
       
    # Filter data based on user inputs
    filtered_data = migrant_App[(migrant_App["incident year"] == incident_year) &
                            (migrant_App["region of incident"] == region_of_origin)]
    
    if not filtered_data.empty:
        # Display filted data
        st.write("Number of dead and missing:", filtered_data["total number of dead and missing"].sum())
        st.write("Number of survivors:", filtered_data["number of survivors"].sum())
        
        filtered_data_1 = migrant_App[(migrant_App['incident year'] == incident_year) & (migrant_App['region of incident'] == region_of_origin)]
        unique_countries = filtered_data_1["country of origin"].unique()
        styled_regions = ", ".join([f"<span style='color:green;'>{region}</span>" for region in unique_countries])


        # Display the styled list
        st.write("Countries of origin include:")
        st.write(styled_regions, unsafe_allow_html=True)

        if not filtered_data_1.empty:
            main_cause = filtered_data_1['cause of death category'].value_counts().idxmax()
            styled_main_cause = f"<span style='color:green;'>{main_cause}</span>"
            st.markdown(f"The main cause of death for this year is: {styled_main_cause}", unsafe_allow_html=True)
    
    # Survival rate for the filtered data
    if not filtered_data.empty:
        st.markdown("<p style='text-align: left; color: yellow; font-size: 18px;'>Survival Rate:</p>", unsafe_allow_html=True)
        total_incidents = int(filtered_data['total number of dead and missing'].sum() + filtered_data['number of survivors'].sum())
        total_survivors = filtered_data['number of survivors'].sum()
        survival_rate = total_survivors / total_incidents if total_incidents != 0 else 0
        styled_survival_rate = f"<span style='color:green;'>{survival_rate:.2%}</span>"
        st.markdown(f"Survival Rate for this region in this year is: {styled_survival_rate}", unsafe_allow_html=True)

    else:
        st.warning("No data available for the selected inputs.")

    # Foursquare API
    st.markdown("<h1 style='text-align: left; color: blue; font-size: 21px;'>Migrant Support Services Finder:</h1>", unsafe_allow_html=True)
    st.write("""To determine where to focus on finding agencies, we utilize Four Square API to identify hotspots of activity in
                this case agencies for migrant's needs. Given our scenario, where the most frequent migration route is from Mexico 
                the United States, and the location of death often occurs in the United States, it makes sense to prioritize this 
                variable values to specifically focus on incidents in the United States.""")
    
    st.write("""Essential Services Hub:
                This category provides a unique set of hot spots that go beyond traditional services, focusing on establishments
                crucial for daily life and well-being. These spots include supermarkets, restaurants, and retail stores like Sam's Club,
                providing essential goods and services. Recognizing these locations is important in ensuring that migrants have 
                access to fundamental resources, such as groceries and essential items, contributing to their overall quality of 
                life and stability in a new community.""")
               
    st.write("""Comprehensive Migrant Support:
                In addition to essential services, the broader category "Hospital, Community Center, Refugee Support, Migrant 
                Support" captures a comprehensive range of resources catering to the diverse needs of migrants. This provides 
                healthcare facilities, community centers, and specialized support services for refugees and migrants. Identifying
                these hot spots is crucial for creating a network of comprehensive support, offering migrants a spectrum of 
                assistance, from medical care to community integration. This comprehensive approach aims to enhance the overall
                well-being of migrants by addressing both immediate necessities and long-term integration challenges.""")

    # Input for the user to select the query category
    category_options = ['Essentials', 'Hospital, Community Center, Refugee Support, Migrant Support']
    selected_category = st.selectbox("Select category", category_options)
    
    if st.button("Search"):
        if selected_category == 'Essentials':
            result = migrant_API_RESTAURANTS
            
        else:
            
            result = migrant_API_NORESTAURANTS

        st.write("Nearby Venues:")
        st.write(result)
        


# Additional features..............
# Check if "Modeling" is in the selected sections
elif "Modeling" in selected_sections:
    # Header
    st.subheader("Time Series Model")
    st.write("To the left you will see a menu of user inputs where you can input the time and migration route you are planning on taking, this will then output an estimation of number of incidents based on the historicals. To the right of this timeseries you will also see the main causes of death in the migration route")
    # Sidebar
    st.sidebar.header("User Inputs")
    planned_migration_date = st.sidebar.date_input("Input planned migration date", value="today", min_value=None, max_value=None, format="YYYY-MM-DD")

    migration_route = st.sidebar.selectbox("Select Migration Route", timeseriesdf["migration route"].unique())
    
    #function that returns the level of the migration route inputted
    def getLevelOfRoute(route, timeseriesdf):
        level = timeseriesdf[timeseriesdf['migration route'] == route]['label_level'].values[0]
        return level

    #run the function with the migration route inputted   
    ts_level = getLevelOfRoute(migration_route, timeseriesdf)
    
    #function to get all the df entries with the same level 
    def getClusterLabel(level, timeseries):
        return (timeseries[timeseries['label_level'] == level])

    #function that extracts all the routes in the same cluster and groups them by the target variable.
    def preprocess_level_timeseries(level, timeseries):
        # Get the 'level' timeseries
        level_timeseries = getClusterLabel(level, timeseries)
    
        # Drop the 'date' column
        level_timeseries = level_timeseries.drop(['date.1'], axis=1)
    
        # Group by date and sum the 'total number of dead and missing'
        level_timeseries = level_timeseries.groupby(level_timeseries.index)['total number of dead and missing'].sum()
    
        return level_timeseries

    leveldf = preprocess_level_timeseries(ts_level, timeseriesdf)
    
    #the parameters will depend on the level selected 
    #if ts_level = 'level1' or then app_order = (0, 1, 1) 
    #if ts_level = 'level2' or ts_level = 'level5' then app_order = (1, 0, 0) 
    #if ts_level = 'level3' or ts_level = 'level4' then app_order = (0, 1, 1) 
    if ts_level == 'level1':
        app_order = (1, 1, 1)
    elif ts_level == 'level2' or ts_level == 'level5':
        app_order = (1, 0, 0)
    elif ts_level == 'level3' or ts_level == 'level4':
        app_order = (0, 1, 1)

    #function that gets the number of periods for the sarima model 

    def calculate_months_difference(date1, date2):
        date1 = pd.to_datetime(date1, format="%Y-%m-%d")
        date2 = pd.to_datetime(date2, format="%Y-%m-%d")

        rdelta = relativedelta(date2, date1)
        months_difference = rdelta.years * 12 + rdelta.months

        return months_difference

    last_date = leveldf.index[-1]
    target_date = planned_migration_date
    months_difference = calculate_months_difference(last_date, target_date)

    #function that sets the sarima timeseries model 
    def sarima_forecast(level_timeseries,forecast_months, order, seasonal_order, plot_title="Forecast"):
        # Create the SARIMA model
        level_sarima_model = sm.tsa.SARIMAX(level_timeseries, order=order, seasonal_order=seasonal_order)
        level_sarima_model_fit = level_sarima_model.fit()

        # Make forecasts
        forecasts = level_sarima_model_fit.get_forecast(steps=forecast_months)
        predicted_values = forecasts.predicted_mean
        predicted_values.index = pd.date_range(start=last_date, periods=forecast_months, freq='M')

        return predicted_values
    #run the sarima function
    predicted_values = sarima_forecast(leveldf, months_difference, order=app_order, seasonal_order=(1, 1, 1, 12), plot_title="Migrant Incident Forecast")

    #function to retrieve the output of the timeseries for the inputted date
    def get_values_for_year_month(indexes, values, year, month):
        matching_values_string = ""  # Initialize an empty string
        for i, date_index in enumerate(indexes):
            if date_index.year == year and date_index.month == month:
                matching_values_string += str(values[i])  # Convert values to strings and append to the string
        return matching_values_string

    # Example usage:
    year_to_find = planned_migration_date.year
    month_to_find = planned_migration_date.month
    matching_values = get_values_for_year_month(predicted_values.index, predicted_values, year_to_find, month_to_find)
    st.write(f"Estimated number of incidents for the planned migration date {month_to_find}/{year_to_find}: {matching_values}")

    #declaration of columns
    col1, col2 = st.columns(2)
    
    col1.subheader(f'{migration_route} Number of Incidents Forecast')
    col1.write(f"The migration route was classified as a danger {ts_level}.")

    # Create a new figure using Plotly Express
    fig = px.line()
    # Add historical data to the plot
    fig.add_scatter(x=leveldf.index, y=leveldf, name="Historical Data")
    # Add SARIMA forecast to the plot
    fig.add_scatter(x=predicted_values.index, y=predicted_values, name="SARIMA Forecast", line=dict(color='red'))
    # Customize the layout (titles, labels, etc.)
    fig.update_layout(
        title="Migrant Incident Forecast",
        xaxis_title="Year",
        yaxis_title="Total Number of Incidents",
        width=500,  # Set the width in pixels
        height=400  # Set the height in pixels
    )
    
    # Show the interactive plot
    col1.plotly_chart(fig)

    # Create a time slider
    #time_range = col2.slider("Select a time range", 0, 14, (0, 23))
 
    # Update the datetime slider based on the selected time range
    #start_date = datetime(2014, 1, 1, time_range[0])
    #end_date = datetime(2025, 12, 30)
    #end_date = start_date + timedelta(hours=time_range[1] - time_range[0])
 
    # selected_date = slider_placeholder.slider(
    #     "Select a date range",
    #     min_value=start_date,
    #     max_value=end_date,
    #     value=(start_date, end_date),
    #     step=timedelta(hours=1),
    # )

    #link to slider code i found https://docs.kanaries.net/topics/Python/streamlit-datetime-slider

    #visualizing COD
    #col2.title('Cause of Death per migration route')

    # Creates route selection dropdown
    #migration_routes = migrant_App['migration route'].unique()
    #commented out this dropdown and set up the cause of death to be determined by the selection of route in the user input side menu
    #selected_route = st.selectbox('Please Select a Migration Route', migration_routes)

    # Filters the data based on the selected migration route
    filtered_data_ts = timeseriesdf[timeseriesdf['migration route'] == migration_route]
    # filtered_data = migrant_App[migrant_App['cause of death category'] == cause_of_death]

    # Creates the histogram
    col2.subheader(f'Causes of Death for {migration_route}')
    fig = px.histogram(filtered_data_ts, x='Cause of Death Category')
    fig.update_layout(
        width=600,  # Set the width in pixels
        height=400  # Set the height in pixels
    )
    col2.plotly_chart(fig)

else: 
    # Header Section
    st.header("Migration Data Analysis")
    st.subheader("Welcome to the Migration Incident Prevention App")
    st.write(introduction)
    
    
# Footer
st.sidebar.text("© 2023 Migrant Data Analysis App")



