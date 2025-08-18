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
from functions.plot_ori_curve import plot_ori_curve


def streamlit_ui():
    st.set_page_config(page_title="Map-Reader")
    st.title("Map-Reader")

    if 'loc_data' not in st.session_state:
        st.session_state.loc_data = None
    if 'ori_data' not in st.session_state:
        st.session_state.ori_data = None

    tdt_data_file = st.file_uploader("Choose .mat file", key=100)
    start_time = st.time_input('Set recording start time:')
    start_time = get_sec_total(str(start_time) + ':000')
    time_buffer = 120
    
    st.subheader("RF location")
    loc_task_file = st.file_uploader("Choose .dat file", key=101)
    if st.button('Submit', key=102):

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
            res_list = list(pool.map(get_loc_map, data_list))

        loc_data = {}
        for res in res_list:
            loc_data.update(res)

        st.session_state.loc_data = loc_data

    loc_data = st.session_state.loc_data
    if loc_data is not None:
        chan_id = st.slider("Select channel:", min_value=1, max_value=32, key=103)
        if chan_id in loc_data.keys():
            chan_res = loc_data[chan_id]
            plot_loc_map(chan_id, chan_res)
        else:
            st.warning(f'No data available for channel {chan_id}')

    st.subheader("RF orientation")
    ori_task_file = st.file_uploader("Choose .dat file", key=104)
    if st.button('Submit', key=105):

        if tdt_data_file is None:
            st.warning("Please upload a MapWriter file.")
            return

        if loc_task_file is None:
            st.warning("Please upload a MapOri file.")
            return

        task_data = get_task_data(ori_task_file)
        task_start = (get_sec_total(task_data['Time'].iloc[0]) - time_buffer) - start_time
        task_stop = (get_sec_total(task_data['Time'].iloc[-2]) + time_buffer) - start_time

        tdt_data = get_tdt_data(tdt_data_file)
        snip_data = get_snip_data(tdt_data, task_start, task_stop)
        event_data = get_event_data(tdt_data, task_start, task_stop)
        onset_data = get_onset_data(task_data, event_data)

        channels = sorted(snip_data['channels'].unique())
        data_list = [{'chan': chan, 'onset_data': onset_data, 'snip_data': snip_data} for chan in channels]

        with Pool() as pool:
            res_list = list(pool.map(get_loc_map, data_list))

        ori_data = {}
        for res in res_list:
            ori_data.update(res)

        st.session_state.ori_data = ori_data

    ori_data = st.session_state.ori_data
    if ori_data is not None:    
        chan_id = st.slider("Select channel:", min_value=1, max_value=32, key=106)
        if chan_id in ori_data.keys():
            chan_res = ori_data[chan_id]
            plot_ori_curve(chan_id, chan_res)
        else:
            st.warning(f'No data available for channel {chan_id}')
