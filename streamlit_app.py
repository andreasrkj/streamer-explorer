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
if "selected_event" not in st.session_state:
    st.session_state.selected_event = None
if "candidate_viewpoint" not in st.session_state:
    st.session_state.candidate_viewpoint = None
if "candidate_molecule" not in st.session_state:
    st.session_state.candidate_molecule = None
if "candidate_viewoption" not in st.session_state:
    st.session_state.candidate_viewoption = "As Video"
if "candidate_scrollable_choices" not in st.session_state:
    st.session_state.candidate_scrollable_choices = ["Moment 0", "Moment 1", "Moment 2", "Moment 8", "Moment 9"]

data_page   = st.Page("streamer_data.py", title="Data Explorer", icon=":material/search:")
events_page = st.Page("streamer_candidates.py", title="Streamer Candidates", icon=":material/airwave:")
stats_page  = st.Page("snap_stats.py", title="Snapshot Statistics", icon=":material/bar_chart:")

pg = st.navigation([data_page, events_page, stats_page], position="top")
pg.run()

def add_footer():
    footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
        z-index: 9999;
    }
    </style>
    <div class="footer">
        <p>📝 Part of a MSc Project by Andreas Rasmussen Kjær - Niels Bohr Institute, University of Copenhagen</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)