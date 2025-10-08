import streamlit as st
from multiprocessing import Pool

from components.loc_map_viewer import loc_map_viewer
from components.ori_curve_viewer import ori_curve_viewer


def streamlit_app():
    st.set_page_config(page_title="Map-Reader")
    st.title("Map-Reader")

    if 'loc_map_plots' not in st.session_state:
        st.session_state.loc_map_plots = None
    if 'target_channels' not in st.session_state:
        st.session_state.target_channels = None
    if 'all_maps_plot' not in st.session_state:
        st.session_state.all_maps_plot = None
    if 'ori_curve_plots' not in st.session_state:
        st.session_state.ori_curve_plots = None
    if 'all_curves_plot' not in st.session_state:
        st.session_state.all_curves_plot = None

    tdt_data_file = st.file_uploader("Choose .mat file", key=100)

    loc_map_viewer(tdt_data_file)
    ori_curve_viewer(tdt_data_file)


if __name__ == '__main__':
    streamlit_app()
    