import streamlit as st
from multiprocessing import Pool

from functions.get_task_data import get_task_data
from functions.get_sec_total import get_sec_total
from functions.get_tdt_data import get_tdt_data
from functions.get_event_data import get_event_data
from functions.get_onset_data import get_onset_data
from functions.get_snip_data import get_snip_data
from functions.get_loc_map import get_loc_map
from functions.plot_loc_map import plot_loc_map
from functions.plot_all_maps import plot_all_maps
from functions.get_ori_curve import get_ori_curve
from functions.plot_ori_curve import plot_ori_curve
from functions.plot_all_curves import plot_all_curves


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
    start_time = st.time_input('Set recording start time:')
    start_time = get_sec_total(str(start_time) + ':000')
    time_buffer = 120
    
    st.subheader("RF location")
    loc_task_file = st.file_uploader("Choose .dat file", key=200)
    if st.button('Submit', key=202):

        if tdt_data_file is None:
            st.warning("Please upload a MapWriter file.")
            return

        if loc_task_file is None:
            st.warning("Please upload a MapLoc file.")
            return

        task_data = get_task_data(loc_task_file)
        task_start = (get_sec_total(task_data['Time'].iloc[0]) - time_buffer) - start_time
        task_stop = (get_sec_total(task_data['Time'].iloc[-2]) + time_buffer) - start_time

        tdt_data = get_tdt_data(tdt_data_file)
        snip_data = get_snip_data(tdt_data, task_start, task_stop)
        event_data = get_event_data(tdt_data, task_start, task_stop)
        onset_data = get_onset_data(task_data, event_data)

        channels = [int(chan) for chan in sorted(snip_data['channels'].unique())]
        data_list = [{'chan': chan, 'onset_data': onset_data, 'snip_data': snip_data} for chan in channels]

        with Pool() as pool:
            result_list = list(pool.map(get_loc_map, data_list))
            loc_map_plots = list(pool.map(plot_loc_map, result_list))

        target_channels = [r['chan'] for r in result_list if r['popt'] is not None]
        result_list = [r for r in result_list if r['chan'] in target_channels]

        all_maps_plot = plot_all_maps(result_list)

        st.session_state.loc_map_plots = loc_map_plots
        st.session_state.target_channels = target_channels
        st.session_state.all_maps_plot = all_maps_plot

    loc_map_plots = st.session_state.loc_map_plots
    if loc_map_plots is not None:
        min_height = 540
        height_set = st.slider('Container height:', min_value=min_height, max_value=(min_height * 3), key=203)
        with st.container(height=height_set):
            for plot in loc_map_plots:
                st.pyplot(plot)

    all_maps_plot = st.session_state.all_maps_plot
    if all_maps_plot is not None:
        st.pyplot(all_maps_plot)

    st.subheader("RF orientation")
    ori_task_file = st.file_uploader("Choose .dat file", key=300)
    if st.button('Submit', key=301):

        if tdt_data_file is None:
            st.warning("Please upload a MapWriter file.")
            return

        if ori_task_file is None:
            st.warning("Please upload a MapOri file.")
            return

        task_data = get_task_data(ori_task_file)
        task_start = (get_sec_total(task_data['Time'].iloc[0]) - time_buffer) - start_time
        task_stop = (get_sec_total(task_data['Time'].iloc[-2]) + time_buffer) - start_time

        st.write(task_stop)

        tdt_data = get_tdt_data(tdt_data_file)
        snip_data = get_snip_data(tdt_data, task_start, task_stop)
        event_data = get_event_data(tdt_data, task_start, task_stop)
        onset_data = get_onset_data(task_data, event_data)

        channels = [int(chan) for chan in sorted(snip_data['channels'].unique())]
        data_list = [{'chan': chan, 'onset_data': onset_data, 'snip_data': snip_data} for chan in channels]

        with Pool() as pool:
            result_list = list(pool.map(get_ori_curve, data_list))
            ori_curve_plots = list(pool.map(plot_ori_curve, result_list))

        target_channels = st.session_state.target_channels
        if target_channels is not None:
            result_list = [r for r in result_list if r['chan'] in target_channels]

        all_curves_plot = plot_all_curves(result_list)

        st.session_state.ori_curve_plots = ori_curve_plots
        st.session_state.all_curves_plot = all_curves_plot

    ori_curve_plots = st.session_state.ori_curve_plots
    if ori_curve_plots is not None:
        min_height = 540
        height_set = st.slider('Container height:', min_value=min_height, max_value=(min_height * 3), key=302)
        with st.container(height=height_set):
            for plot in ori_curve_plots:
                st.pyplot(plot)

    all_curves_plot = st.session_state.all_curves_plot
    if all_curves_plot is not None:
        st.pyplot(all_curves_plot)

if __name__ == '__main__':
    streamlit_app()
    