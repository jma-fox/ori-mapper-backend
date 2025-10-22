import streamlit as st
from multiprocessing import Pool

from functions.get_tdt_data import get_tdt_data
from functions.get_task_data import get_task_data
from functions.get_snip_data import get_snip_data
from functions.get_ori_data import get_ori_data
from functions.get_ori_curve import get_ori_curve
from functions.plot_ori_curve import plot_ori_curve
from functions.plot_all_curves import plot_all_curves


def streamlit_app():
    st.set_page_config(page_title="Ori Mapper")
    st.title("Ori Mapper")

    if 'ori_curves' not in st.session_state:
        st.session_state.ori_curves = None

    loc_task_file = st.file_uploader("Choose MapLoc task file")
    tdt_data_file = st.file_uploader("Choose TDT data file")

    st.write("")

    event_name = st.text_input("Event Name", value="stim_on_time")

    st.write("")

    if st.button('Load Map Data'):
        tdt_data = get_tdt_data(tdt_data_file)
        task_data = get_task_data(loc_task_file)
        snip_data = get_snip_data(tdt_data)
        ori_data = get_ori_data(task_data, snip_data, event_name)

        with Pool() as pool:
            ori_curves = list(pool.map(get_ori_curve, ori_data))

        st.session_state.ori_curves = ori_curves

    st.write("")

    ori_curves = st.session_state.ori_curves

    if ori_curves is not None:
        drop_channels = []

        with st.expander("Channel Orientation Curves", expanded=True):
            for curve in ori_curves:
                channel, fig = plot_ori_curve(curve)
                drop_channel = st.checkbox(f"Drop Channel {channel}")
                if drop_channel:
                    drop_channels.append(channel)
                st.pyplot(fig)

        ori_curves = [m for m in ori_curves if m['channel'] not in drop_channels]

        with st.expander("All Orientation Curves", expanded=True):
            fig = plot_all_curves(ori_curves)
            st.pyplot(fig)


if __name__ == '__main__':
    streamlit_app()
    