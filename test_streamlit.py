import streamlit as st
import requests
import folium 
import time
import matplotlib.pyplot as plt
from streamlit_folium import folium_static, st_folium
from folium.plugins import Draw
from folium import plugins
import numpy as np

# Initialize session state
if 'input_data' not in st.session_state:
    st.session_state.input_data = {}
if 'page' not in st.session_state:
    st.session_state.page = 'page_one'


#Define the URL of the FastAPI endpoint
FASTAPI_URL = 'https://immo-eliza-deployment-1-mn9i.onrender.com/predict'

loc_coordinates = {
    "Brussels": (50.8503, 4.3517),
    "Antwerp": (51.2194, 4.4025),
    "Liège": (50.8503, 5.6889),
    "Brugge": (51.2094, 3.2247),
    "Halle-Vilvoorde": (50.8333, 4.3),
    "Gent": (51.0543, 3.7174),
    "Turnhout": (51.3223, 4.9483),
    "Leuven": (50.8792, 4.7009),
    "Nivelles": (50.5974, 4.3279),
    "Oostend": (51.2093, 2.9296),
    "Aalst": (50.9364, 4.0355),
    "Charleroi": (50.4101, 4.4447),
    "Kortrijk": (50.8284, 3.2653),
    "Hasselt": (50.9311, 5.3375),
    "Namur": (50.4669, 4.8675),
    "Mechelen": (51.0259, 4.4773),
    "Sint-Niklaas": (51.1585, 4.1437),
    "Mons": (50.4541, 3.9561),
    "Veurne": (51.0749, 2.6564),
    "Dendermonde": (51.0259, 4.1059),
    "Verviers": (50.5891, 5.8667),
    "Tournai": (50.6052, 3.3879),
    "Oudenaarde": (50.8466, 3.611),
    "Soignies": (50.5796, 4.0714),
    "Thuin": (50.3397, 4.2859),
    "Mouscron": (50.7399, 3.2069),
    "Dinant": (50.2606, 4.9125),
    "Tongeren": (50.7805, 5.4645),
    "Maaseik": (51.0984, 5.7886),
    "Ath": (50.6303, 3.7806),
    "Huy": (50.5201, 5.2394),
    "Marche-en-Famenne": (50.2232, 5.3485),
    "Waremme": (50.6986, 5.256),
    "Neufchâteau": (49.8412, 5.4429),
    "Arlon": (49.6837, 5.8149),
    "Diksmuide": (51.0339, 2.8614),
    "Virton": (49.5665, 5.5232),
    "Bastogne": (50.0039, 5.7215),
    "Philippeville": (50.1669, 4.5475),
    "Roeselare": (50.9489, 3.121),
    "Eeklo": (51.1871, 3.5492),
    "Tielt": (50.999, 3.3396),
    "Ieper": (50.8503, 2.8833),
    "MISSING": (50.8503, 4.3517)  
}
region_province_mapping = {
    "Flanders": ["West Flanders", "East Flanders", "Antwerp", "Limburg", "Flemish Brabant","MISSING"],
    "Wallonia": ["Hainaut", "Liège", "Walloon Brabant", "Namur", "Luxembourg","MISSING"],
    "Brussels-Capital": ["Brussels","MISSING"]
}

# List of localities for each province
province_locality_mapping = {
    "Antwerp": ["Antwerp", "Turnhout", "Mechelen"],
    "East Flanders": ["Gent", "Aalst", "Sint-Niklaas", "Dendermonde", "Oudenaarde", "Eeklo"],
    "Brussels": ["Brussels"],
    "Walloon Brabant": ["Nivelles"],
    "Flemish Brabant": ["Halle-Vilvoorde", "Leuven"],
    "Liège": ["Liège", "Verviers", "Huy", "Waremme"],
    "West Flanders": ["Brugge", "Oostend", "Kortrijk", "Veurne", "Diksmuide", "Roeselare", "Tielt", "Ieper"],
    "Hainaut": ["Charleroi", "Mons", "Tournai", "Soignies", "Thuin", "Mouscron", "Ath"],
    "Luxembourg": ["Marche-en-Famenne", "Neufchâteau", "Arlon", "Virton", "Bastogne"],
    "Limburg": ["Hasselt", "Tongeren", "Maaseik"],
    "Namur": ["Namur", "Dinant", "Philippeville"],
    "MISSING": ["MISSING"]
}

avg_price_per_sqm_loc = {
    "Aalst": 2544.11,
    "Antwerp": 3130.76,
    "Arlon": 2506.79,
    "Ath": 1961.84,
    "Bastogne": 2240.68,
    "Brugge": 6889.06,
    "Brussels": 3741.35,
    "Charleroi": 1281.17,
    "Dendermonde": 2673.14,
    "Diksmuide": 2644.81,
    "Dinant": 1739.27,
    "Eeklo": 2691.39,
    "Gent": 3410.38,
    "Halle-Vilvoorde": 2915.09,
    "Hasselt": 2579.62,
    "Huy": 1912.54,
    "Ieper": 1854.59,
    "Kortrijk": 2629.80,
    "Leuven": 3079.36,
    "Liège": 2148.71,
    "MISSING": 8592.86,
    "Maaseik": 2514.20,
    "Marche-en-Famenne": 1935.64,
    "Mechelen": 2884.99,
    "Mons": 1660.65,
    "Mouscron": 2264.84,
    "Namur": 2280.13,
    "Neufchâteau": 1881.24,
    "Nivelles": 2787.00,
    "Oostend": 3672.29,
    "Oudenaarde": 2374.82,
    "Philippeville": 712.63,
    "Roeselare": 2685.50,
    "Sint-Niklaas": 2790.20,
    "Soignies": 1804.32,
    "Thuin": 1616.10,
    "Tielt": 2586.74,
    "Tongeren": 2204.31,
    "Tournai": 2306.65,
    "Turnhout": 2509.81,
    "Verviers": 2121.32,
    "Veurne": 4149.76,
    "Virton": 2044.47,
    "Waremme": 1665.26
}

Q1_province = {
    "Antwerp": 2165.83,
    "Brussels": 2785.71,
    "East Flanders": 2035.71,
    "Flemish Brabant": 2319.56,
    "Hainaut": 1218.92,
    "Limburg": 1849.08,
    "Liège": 1551.57,
    "Luxembourg": 1547.08,
    "MISSING": 4546.34,
    "Namur": 1554.22,
    "Walloon Brabant": 2166.67,
    "West Flanders": 2474.80
}

Q2_province = {
    "Antwerp": 2752.87,
    "Brussels": 3518.52,
    "East Flanders": 2653.33,
    "Flemish Brabant": 2973.49,
    "Hainaut": 1785.71,
    "Limburg": 2430.56,
    "Liège": 2150.00,
    "Luxembourg": 2210.06,
    "MISSING": 4674.31,
    "Namur": 2257.89,
    "Walloon Brabant": 2820.51,
    "West Flanders": 3421.05
}

Q3_province = {
    "Antwerp": 3423.42,
    "Brussels": 4444.44,
    "East Flanders": 3344.34,
    "Flemish Brabant": 3627.68,
    "Hainaut": 2483.33,
    "Limburg": 3046.58,
    "Liège": 2818.46,
    "Luxembourg": 2857.14,
    "MISSING": 9222.40,
    "Namur": 2950.82,
    "Walloon Brabant": 3451.19,
    "West Flanders": 4775.43}

#Input features for price prediction
html_content = """
<div class="immo-eliza-container">
    <div class = "title_div">
        <h1 class="title">Welcome to</h1>
    </div>
    <h1 class = "immo_name" >IMMO-ELIZA</h1>
</div>
"""

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.markdown(html_content, unsafe_allow_html=True)


def page_one():
    # Input fields or widgets for page one
    st.header("Describe your property for us, and we'll give you a prediction!")
    st.subheader('Navigate through the menus for the location the use the marker on the map for best accuracy')
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        # User selects the region
        region = st.selectbox("Pick region", list(region_province_mapping.keys()))
    
        # Store region in session state
        st.session_state.region = region
    
        # Based on the selected region, dynamically update the options for the province
        provinces_for_region = region_province_mapping.get(region, [])
        province = st.selectbox('Province', provinces_for_region)
    
        # Based on the selected province, dynamically update the options for the locality
        localities_for_province = province_locality_mapping.get(province, [])
        locality = st.selectbox('Locality:', localities_for_province)
    
        for p,c in loc_coordinates.items():
            if p == locality:
                latitude = c[0]
                longitude = c[1]
    with col2:

        # Initial coordinates for Brussels
        st.title("Location (Use Marker)")
    
        #belgium_coords = [50.8503, 4.3517]  # Latitude and Longitude for Brussels, Belgium
        m = folium.Map(location=[latitude,longitude], zoom_start=12)
        Draw(export=True).add_to(m)
        # st_folium(m, height=300) 
        st_data = st_folium(m, width=800, height=300)

        if st_data is not None and st_data.get("last_active_drawing") is not None:
        # Accessing coordinates from the last_active_drawing
            coordinates = st_data["last_active_drawing"].get("geometry", {}).get("coordinates")

            if coordinates is not None and len(coordinates) == 2:
                # Extract latitude and longitude
                latitude, longitude = coordinates
                st.write(f"Last Clicked Latitude: {latitude}")
                st.write(f"Last Clicked Longitude: {longitude}")
        else:
            st.warning("Please select the marker and click on the map to retrieve coordinates")

    if st.button('Next'):
        st.session_state.province = province
        st.session_state.latitude = latitude
        st.session_state.longitude = longitude
        st.session_state.locality = locality
        st.session_state.page = 'page_two'
        st.experimental_rerun()

def page_two():

    nbr_bedrooms = st.number_input('Number of Bedrooms:', min_value=0, max_value=10, value=1)   
    nbr_frontages = st.number_input('Number of Frontages:', min_value=0, max_value=10, value=1)
    total_area_sqm = st.number_input('Living Area (sqm):', min_value=0.0, step=10.0, value=10.0)
    surface_land_sqm = st.number_input('Plot Area (sqm):', min_value=0.0, step=10.0)
    fl_terrace = st.selectbox('Terrace ?:',  [0, 1])
    terrace_sqm = st.number_input('Terrace Area (sqm):', min_value=0.0, step=2.0)
    fl_garden = st.selectbox('Garden ?:',  [0, 1])
    garden_sqm = st.number_input('Garden Area (sqm):', min_value=0.0, step=10.0)
    
    # Additional input fields or widgets for page two
    if st.button('Previous'):
        st.session_state.nbr_bedrooms = nbr_bedrooms
        st.session_state.nbr_frontages = nbr_frontages
        st.session_state.total_area_sqm = total_area_sqm
        st.session_state.surface_land_sqm = surface_land_sqm
        st.session_state.fl_terrace = fl_terrace
        st.session_state.fl_garden = fl_garden
        st.session_state.garden_sqm = garden_sqm
        st.session_state.terrace_sqm = terrace_sqm
        st.session_state.page = 'page_one'
        st.experimental_rerun()

    if st.button('Next'):
        # Store inputs from page two or do further processing
        st.session_state.nbr_bedrooms = nbr_bedrooms
        st.session_state.nbr_frontages = nbr_frontages
        st.session_state.total_area_sqm = total_area_sqm
        st.session_state.surface_land_sqm = surface_land_sqm
        st.session_state.fl_terrace = fl_terrace
        st.session_state.fl_garden = fl_garden
        st.session_state.garden_sqm = garden_sqm
        st.session_state.terrace_sqm = terrace_sqm
        st.session_state.page = 'page_three'
        st.experimental_rerun()
 
        
# Call to render Folium map in Streamlit
def page_three():
    property_type=st.selectbox("Pick property type",['House','appartement'])
    subproperty_type = st.selectbox('Select type of subproperty:',[
        "HOUSE",
        "APARTMENT",
        "VILLA",
        "GROUND_FLOOR",
        "APARTMENT_BLOCK",
        "MIXED_USE_BUILDING",
        "PENTHOUSE",
        "DUPLEX",
        "FLAT_STUDIO",
        "EXCEPTIONAL_PROPERTY",
        "TOWN_HOUSE",
        "SERVICE_FLAT",
        "MANSION",
        "BUNGALOW",
        "KOT",
        "LOFT",
        "FARMHOUSE",
        "COUNTRY_COTTAGE",
        "MANOR_HOUSE",
        "TRIPLEX",
        "OTHER_PROPERTY",
        "CHALET",
        "CASTLE"
    ])

    state_building = st.selectbox('State of building:', [
        "MISSING",
        "GOOD",
        "AS_NEW",
        "TO_RENOVATE",
        "TO_BE_DONE_UP",
        "JUST_RENOVATED",
        "TO_RESTORE"
    ])

    epc = st.selectbox('EPC:', [
        "MISSING",
        "B",
        "C",
        "D",
        "A",
        "F",
        "E",
        "G",
        "A+",
        "A++"
    ])
    heating_type = st.selectbox('Type of heating:', [
        "GAS",
        "MISSING",
        "FUELOIL",
        "ELECTRIC",
        "PELLET",
        "WOOD",
        "SOLAR",
        "CARBON"
    ])
    equipped_kitchen=st.selectbox("Pick kitchen type",['USA_UNINSTALLED','USA_SEMI_EQUIPPED',
                                                'USA_INSTALLED', 'NOT_INSTALLED', 'USA_HYPER_EQUIPPED',
                                                'SEMI_EQUIPPED', 'HYPER_EQUIPPED', 'INSTALLED', 'MISSING'])
    fl_swimming_pool = st.selectbox('Swimming pool ?:',  [0, 1])

    if st.button('Previous'):
        st.session_state.page = 'page_two'
        st.experimental_rerun()
    
    #Button to trigger prediction
    if st.button('Predict Price'):
        # Prepare input data as JSON
        input_data = {
    "nbr_frontages": st.session_state.nbr_frontages,
    "equipped_kitchen": equipped_kitchen,
    "nbr_bedrooms": st.session_state.nbr_bedrooms,
    "latitude": st.session_state.latitude,
    "longitude": st.session_state.longitude,
    "total_area_sqm": st.session_state.total_area_sqm,
    "surface_land_sqm": st.session_state.surface_land_sqm,
    "terrace_sqm": st.session_state.terrace_sqm,
    "garden_sqm": st.session_state.garden_sqm,
    "province": st.session_state.province,
    "heating_type": heating_type,
    "state_building": state_building,
    "property_type": property_type,
    "epc": epc,
    "locality": st.session_state.locality,
    "subproperty_type": subproperty_type,
    "region": st.session_state.region,
    "fl_terrace": st.session_state.fl_terrace,
    "fl_garden": st.session_state.fl_garden,
    "fl_swimming_pool": fl_swimming_pool
    }

    # Make POST request to FastAPI endpoint
        try:
            response = requests.post(FASTAPI_URL, json=input_data)
            predicted_price = response.json()[0]
    
            progress_bar = st.progress(0)
            for perc_completed in range(100):
                time.sleep(0.05)  
                progress_bar.progress(perc_completed + 1)
    
            st.success(f'Predicted Price: €{predicted_price:.2f}')
            col1, col2 = st.columns([1, 2])
            with col1:
                st.subheader("Price per square meters - locality")
                if st.session_state.total_area_sqm != 0:
                    price_per_sqm = predicted_price / st.session_state.total_area_sqm
                    #delta = avg_price_per_sqm_loc[st.session_state.locality]
                    delta = price_per_sqm - avg_price_per_sqm_loc[st.session_state.locality]

                    #delta_color = 'normal' if delta <= 0 else 'inverse'  # 'inverse' for red, if Streamlit version supports it
                    #delta_color = 'normal' if delta > 0 else 'inverse'

                    if abs(delta) >= price_per_sqm:
                        delta_value = f"{delta}"
                    else:
                        delta_value = f"{delta}"

                    # Display the metric with the delta
                    st.metric(
                                label=st.session_state.locality,
                                value=round(price_per_sqm, 2),
                                delta=f"{round((delta), 2)}: Δ from average",
                                delta_color="normal"
                            )                
                else:
                    st.write(f"Locality: {st.session_state.locality}, Total area is zero, cannot calculate price per sqm.")

            with col2:
                st.subheader("Price per square meters - province")
                if st.session_state.total_area_sqm != 0:
                    fig, ax = plt.subplots()

                    q1_value = Q1_province[st.session_state.province]
                    q2_value = Q2_province[st.session_state.province]
                    q3_value = Q3_province[st.session_state.province]

                    sigma = (q3_value - q1_value) / 1.349  # This factor comes from the interquartile range of a normal distribution
                    mu = q2_value

                    # Create a range of values for the x-axis (prices)
                    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)

                    # Create the normal distribution curve for the y-axis
                    y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

                    # Start plotting
                    fig, ax = plt.subplots()

                    # Plot the normal distribution curve
                    ax.plot(x, y, color='blue')

                    ax.plot(price_per_sqm, (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((price_per_sqm - mu) / sigma) ** 2), 'ro', label=f'Actual price = {price_per_sqm:.2f}')
                    ax.annotate(f'{price_per_sqm:.2f}', (price_per_sqm, (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((price_per_sqm - mu) / sigma) ** 2)))

                    # Plot the Q1, Q2, and Q3 points on the curve
                    ax.plot(q1_value, (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((q1_value - mu) / sigma) ** 2), 'go', label=f'Q1 = {q1_value:.2f}')
                    ax.plot(q2_value, (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((q2_value - mu) / sigma) ** 2), 'mo', label=f'Q2 = {q2_value:.2f}')
                    ax.plot(q3_value, (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((q3_value - mu) / sigma) ** 2), 'bo', label=f'Q3 = {q3_value:.2f}')

                    # Add a legend
                    ax.legend()

                    # Set the title and labels
                    ax.set_title(f'Price distribution in {st.session_state.province}')
                    ax.set_xlabel('Price per mÂ²')
                    ax.set_ylabel('Density')

                    # Display the plot in Streamlit
                    st.pyplot(fig)
                else:
                    st.write(f"Locality: {st.session_state.locality}, Total area is zero, cannot calculate price per sqm.")
        except Exception as e:
            st.error(f'An error occurred: {str(e)}')



# Render current page based on session state
if st.session_state.page == 'page_one':
    page_one()
elif st.session_state.page == 'page_two':
    page_two()
elif st.session_state.page == 'page_three':
    page_three()
