import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


def map_call(data):
    # If smaller radius map, else larger map
    # figure = folium.Figure(width="100%", height="50%")
    figure_map = folium.Map(location=[37, -102], zoom_start=2, scrollWheelZoom=False)  # .add_to(figure)
    
    # add Openstreetmap layer
    folium.TileLayer('openstreetmap', name='OpenStreet Map').add_to(figure_map)
    
    # Markers then plot map
    data[::-1].apply(plot_markers, axis=1, args=(figure_map,))
    return figure_map


def plot_markers(point, _figure_map):
    # Private eBird hotspot do not get a hyperlink and are assigned black
    icon_color = folium.Icon(color="black")
    marker = folium.Marker(location=[point.Latitude, point.Longitude], popup=point.Common_Name, icon=icon_color)
    _figure_map.add_child(marker)


def main():
    # Page label and headers
    st.set_page_config(layout='wide')
    st.header('eBird Sightings Mapifier')
    st.caption(
        "Download your data from ebird at this link: "
        "[https://ebird.org/downloadMyData](https://ebird.org/downloadMyData)")
    # st.text('By: Michelle G - November 12, 2023')

    uploaded_file = st.file_uploader("Upload your CSV file downloaded from eBird", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.replace(' ', '_')

        with st.sidebar:
            options = sorted(df['Common_Name'].unique())
            st.selectbox("Species:", options, key="user_choice", index=None)

        df = df.loc[df['Common_Name'] == st.session_state.user_choice]

        complete_map = map_call(df)
        complete_map.save('complete_map.html')
        import webbrowser
        webbrowser.open('complete_map.html')
        #st_data = st_folium(complete_map, width = 725)  # width=700, height=500


        with st.expander("Table"):
            if st.session_state.user_choice is not None:
                st.dataframe(df[['Submission_ID', 'Common_Name', 'Count', 'State/Province',
                                'County', 'Location', 'Date', 'Time']], hide_index=True, use_container_width=True)


# Run main
if __name__ == "__main__":
    main()

# st.session_state
