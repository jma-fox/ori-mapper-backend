import streamlit as st
from multiprocessing import Pool

from functions.get_tdt_data import get_tdt_data
from functions.get_start_time import get_start_time
from functions.get_task_data import get_task_data
from functions.ref_onset_times import ref_onset_times
from functions.get_snip_data import get_snip_data
from functions.get_ori_data import get_ori_data
from functions.get_ori_curve import get_ori_curve
from functions.plot_ori_curve import plot_ori_curve
from functions.plot_all_curves import plot_all_curves


def ori_curve_viewer(tdt_data_file):
    st.subheader("RF Orientation")
    ori_task_file = st.file_uploader("Choose MapOri task file")

    if st.button('Submit', key=301):
        if tdt_data_file is None:
            st.warning("Please upload TDT struct file.")
            return

        if ori_task_file is None:
            st.warning("Please upload MapOri task file.")
            return
        
        tdt_data = get_tdt_data(tdt_data_file)
        task_data = get_task_data(ori_task_file)
        snip_data = get_snip_data(tdt_data)
        ori_data = get_ori_data(task_data, snip_data)

        with Pool() as pool:
            ori_curves = list(pool.map(get_ori_curve, ori_data))
            ori_curve_plots = list(pool.map(plot_ori_curve, ori_curves))

        target_channels = st.session_state.target_channels
        if target_channels is not None:
            ori_curves = [r for r in ori_curves if r['channel'] in target_channels]

        all_curves_plot = plot_all_curves(ori_curves)

        st.session_state.ori_curve_plots = ori_curve_plots
        st.session_state.all_curves_plot = all_curves_plot

    ori_curve_plots = st.session_state.ori_curve_plots
    all_curves_plot = st.session_state.all_curves_plot

    if ori_curve_plots is not None:
        with st.expander("Orientation Curves", expanded=True):
            for plot in ori_curve_plots:
                st.pyplot(plot)

    if all_curves_plot is not None:
        st.pyplot(all_curves_plot)
