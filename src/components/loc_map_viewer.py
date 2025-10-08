import streamlit as st
from multiprocessing import Pool

from functions.get_tdt_data import get_tdt_data
from functions.get_start_time import get_start_time
from functions.get_task_data import get_task_data
from functions.ref_onset_times import ref_onset_times
from functions.get_snip_data import get_snip_data
from functions.get_loc_data import get_loc_data
from functions.get_loc_map import get_loc_map
from functions.plot_loc_map import plot_loc_map
from functions.plot_all_maps import plot_all_maps


def loc_map_viewer(tdt_data_file):
    st.subheader("RF location")
    loc_task_file = st.file_uploader("Choose MapLoc task file")

    if st.button('Submit', key=202):
        if tdt_data_file is None:
            st.warning("Please upload TDT struct file.")
            return
        
        if loc_task_file is None:
            st.warning("Please upload MapLoc task file.")
            return
        
        tdt_data = get_tdt_data(tdt_data_file)
        start_time = get_start_time(tdt_data)

        task_data = get_task_data(loc_task_file)
        task_data = ref_onset_times(task_data, start_time)

        snip_data = get_snip_data(tdt_data)
        loc_data = get_loc_data(task_data, snip_data)

        with Pool() as pool:
            loc_maps = list(pool.map(get_loc_map, loc_data))
            loc_map_plots = list(pool.map(plot_loc_map, loc_maps))

        target_channels = [m['channel'] for m in loc_maps if m['popt'] is not None]
        loc_maps = [m for m in loc_maps if m['channel'] in target_channels]

        all_maps_plot = plot_all_maps(loc_maps)

        st.session_state.loc_map_plots = loc_map_plots
        st.session_state.target_channels = target_channels
        st.session_state.all_maps_plot = all_maps_plot

    loc_map_plots = st.session_state.loc_map_plots

    if loc_map_plots is not None:
        with st.expander("Location Maps", expanded=True):
            
            for plot in loc_map_plots:
                st.pyplot(plot)

    all_maps_plot = st.session_state.all_maps_plot

    if all_maps_plot is not None:
        st.pyplot(all_maps_plot)
