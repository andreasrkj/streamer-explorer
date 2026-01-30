import streamlit as st

st.set_page_config(page_title="Streamer Explorer", page_icon=":material/air:", layout="wide")

# Initialize session state variables for persistence across pages
if "current_sink" not in st.session_state:
    st.session_state.current_sink = None
if "selected_point" not in st.session_state:
    st.session_state.selected_point = None
if "viewpoint" not in st.session_state:
    st.session_state.viewpoint = None
if "molecule" not in st.session_state:
    st.session_state.molecule = None
if "moment" not in st.session_state:
    st.session_state.moment = None
if "image_type" not in st.session_state:
    st.session_state.image_type = None
if "selected_sinks" not in st.session_state:
    st.session_state.selected_sinks = None
if "selected_stats" not in st.session_state:
    st.session_state.selected_stats = None
if "image_viewtype" not in st.session_state:
    st.session_state.image_viewtype = "Single Image"
if "view_comparison" not in st.session_state:
    st.session_state.view_comparison = None
if "multi_moments" not in st.session_state:
    st.session_state.multi_moments = ["Moment 8", "Moment 9"]

data_page  = st.Page("streamer_data.py", title="Streamer Data Explorer", icon=":material/search:")
stats_page = st.Page("snap_stats.py", title="Snapshot Statistics", icon=":material/bar_chart:")

pg = st.navigation([data_page, stats_page], position="top")
pg.run()