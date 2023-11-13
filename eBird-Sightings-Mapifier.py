import streamlit as st
import pandas as pd
import folium
import os
import pathlib
from os import listdir
from os.path import isfile, join
# from datetime import date, timedelta
from streamlit_folium import st_folium
lat, lng = 37.238947, -76.745847


@st.cache_resource
def map_call(data):
    # If smaller radius map, else larger map
    # figure = folium.Figure(width="100%", height="50%")
    figure_map = folium.Map(location=[37, -102], zoom_start=2, scrollWheelZoom=False)  # .add_to(figure)

    # Markers then plot map
    data[::-1].apply(plot_markers, axis=1, args=(figure_map,))
    return figure_map


def plot_markers(point, _figure_map):
    # Private eBird hotspot do not get a hyperlink and are assigned black
    icon_color = folium.Icon(color="black")
    marker = folium.Marker(location=[point.Latitude, point.Longitude], popup=point.Common_Name, icon=icon_color)
    _figure_map.add_child(marker)


# def save_uploadedfile(uploadedfile):
#    with open(os.path.join("tempDir", uploadedfile.name), "wb") as f:
#        f.write(uploadedfile.getbuffer())
#    return st.success("Saved File:{} to tempDir".format(uploadedfile.name))


def upload(uploaded_file):
    if uploaded_file is None:
        st.session_state["upload_state"] = "Upload a file first!"
    else:
        data = uploaded_file.getvalue().decode('utf-8')
        parent_path = pathlib.Path(__file__).parent.parent.resolve()
        save_path = os.path.join(parent_path, "data")
        complete_name = os.path.join(save_path, uploaded_file.name)
        destination_file = open(complete_name, "w", encoding='utf-8')
        destination_file.write(data)
        destination_file.close()
        st.session_state["upload_state"] = "Saved " + complete_name + " successfully!"


def main():
    # Page label and headers
    st.set_page_config(layout='wide')
    st.header('eBird Sightings Mapifier')
    st.caption(
        "Download your data from ebird at this link: "
        "[https://ebird.org/downloadMyData](https://ebird.org/downloadMyData)")
    # st.text('By: Michelle G - November 12, 2023')

    # holder = st.empty()
    # holder.empty()

    st.write("""
    # File Picker
    """)
    uploaded_file = st.file_uploader("Upload your CSV file downloaded from eBird", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.replace(' ', '_')

        st.write("CSV Preview")
        st.dataframe(df.head(5), hide_index=True, use_container_width=True)

        upload_state = st.text_area("Upload State", "", key="upload_state")
        st.button("Upload file", on_click=upload, args=[uploaded_file])

        parent_path = pathlib.Path(__file__).parent.resolve()
        data_path = os.path.join(parent_path, "data")
        onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
        option = st.sidebar.selectbox('Pick a dataset', onlyfiles)
        file_location = os.path.join(data_path, option)

        # use `file_location` as a parameter to the main script

        with st.sidebar:
            options = sorted(df['Common_Name'].unique())
            st.selectbox("Species:", options, key="user_choice", index=None)

        df = df.loc[df['Common_Name'] == st.session_state.user_choice]

        complete_map = map_call(df)
        st_data = st.folium(complete_map)  # width=700, height=500
        make_map_responsive = """
         <style>
         [title~="st.iframe"] {width: 100%}
         </style>
        """
        st.markdown(make_map_responsive, unsafe_allow_html=True)

        with st.expander("Table"):
            if st.session_state.user_choice is not None:
                st.dataframe(df[['Submission_ID', 'Common_Name', 'Count', 'State/Province',
                                'County', 'Location', 'Date', 'Time']], hide_index=True, use_container_width=True)


# Run main
if __name__ == "__main__":
    main()

# st.session_state
