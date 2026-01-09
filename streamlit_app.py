import os
import streamlit as st
st.set_page_config(layout="wide")
import numpy as np

sink_dict = {
    "6"  : (170,1080),
    "13" : (230,2600),
    "24" : (220,1370),
    "82" : (240,1310),
    "122": (350,1100),
    "162": (410,2040),
    "180": (410,1520),
    "225": (450,1330)
}

st.title("Streamer data")

if "display_iout_options" not in st.session_state:
    st.session_state.display_iout_options = True

# Create columns (one for convergence + options, another for images + options)
col1, col2 = st.columns(2)

with col1:
    isink = st.selectbox(
        "Select the sink you wish to look at",
        tuple(sink_dict.keys()),
        index=None,
        placeholder="Select the sink you wish to look at",
        accept_new_options=True
    )

    if isink is not None:
        (nstart, nend) = sink_dict[str(isink)]
        snapshots = np.arange(nstart, nend+1, 10)
        st.session_state.display_iout_options = False

        iout = st.select_slider(
        "Select the snapshot you wish to look at",
        options=snapshots)

    #iout = st.selectbox(
    #    "Select the snapshot you wish to look at",
    #    tuple(snapshots),
    #    index=None,
    #    placeholder="Select the snapshot you wish to look at",
    #    accept_new_options=False,
    #    disabled=st.session_state.display_iout_options
    #)

    if isink is not None and iout is not None:
        img_path = os.path.join("./convergence_plots", "sink{:>03}".format(isink), "o{:>04}.png".format(iout))
        with st.spinner("Loading image..."):
            st.image(img_path, caption="Please note the error in the legend. Top line should be $1 \\times 10^6$")

with col2:
    if isink is not None and iout is not None:
        st.header("Investigate the sink with viewpoint and image")

        viewpoint = st.pills("View Direction", ["Face On", "Edge On (A)", "Edge On (B)"], selection_mode="single")
        if viewpoint is not None:
            molecule = st.pills("Molecular Transition", ["H$_2$CO J = 3-2", "$^{13}$CO J = 2-1", "C$^{18}$O J = 2-1"], selection_mode="single")
            if molecule is not None:
                moment = st.pills("Select moment to view", ["Moment 0", "Moment 1", "Moment 8", "Moment 9"], selection_mode="single")
                if moment is not None:
                    st.write(f"Showing view: {viewpoint} for molecular transition {molecule} in {moment}")