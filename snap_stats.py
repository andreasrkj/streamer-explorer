import os
import streamlit as st
st.set_page_config(layout="wide")
import numpy as np
import pandas as pd
import plotly.express as px

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

unconverged_sinkdict = {
    "6"  : [],
    "13" : [2210,2220,2230,2240,2250,2260,2270,2280,2290,2300,2310,2320,2330,2430,2440,2450,2460,2470,2480,2490,2500,2510,2520,2530,2540,2550,2560,2570,2580,2590,2600],
    "24" : [390,400,410,420,430,440,450,460,470,480,490,1010],
    "82" : [1140,1150,1160,1170,1180,1240,1260,1270,1290],
    "122": [],
    "162": [],
    "180": [],
    "225": []
}

total_calculation_time = { # total CPU hours
    "6"  : 83369.79,
    "13" : 150414.5199,
    "24" : 146770.4968,
    "82" : 77031.37545,
    "122": 93333.53278,
    "162": 85745.96947,
    "180": 41178.78426,
    "225": 58922.46438
}

def basic_stats(sink_id):
    # Show snapshot range, count, unconverged count
    snap_min, snap_max = sink_dict[str(sink_id)]
    unconverged_list = unconverged_sinkdict[str(sink_id)]
    total_snaps = len(np.arange(snap_min, snap_max+1, 10))
    unconverged_count = len(unconverged_list)
    st.markdown(f"**Calculation Time (CPU hrs):** {np.round(total_calculation_time[str(sink_id)],2)}")
    st.markdown(f"**Snapshot Range:** {snap_min} - {snap_max}")
    st.markdown(f"**Total Snapshots:** {total_snaps}")
    st.markdown(f"**Unconverged Snapshots:** {unconverged_count}")
    if unconverged_count > 0:
        st.markdown(f"**Unconverged Snapshot List:** {unconverged_list}")

def completion_plot(sink_id):
    # Create graph showing how much is finished of column densities, temperatures, images, etc.
    sink_stats = {
        "Convergence": len(os.listdir("./convergence_plots/sink{:>03}/".format(int(sink_id)))) / len(np.arange(sink_dict[str(sink_id)][0], sink_dict[str(sink_id)][1]+1, 10)) * 100,
        "Column Density": len(os.listdir("./column_densities/sink{:>03}/".format(int(sink_id)))) / len(np.arange(sink_dict[str(sink_id)][0], sink_dict[str(sink_id)][1]+1, 10)) * 100,
        "Temperature": len(os.listdir("./temperatures/sink{:>03}/".format(int(sink_id)))) / len(np.arange(sink_dict[str(sink_id)][0], sink_dict[str(sink_id)][1]+1, 10)) * 100,
        "RADMC-3D Imgs": len(os.listdir("./molecular_imgs/radmc/sink{:>03}/".format(int(sink_id)))) / len(np.arange(sink_dict[str(sink_id)][0], sink_dict[str(sink_id)][1]+1, 10)) * 100,
        "SimALMA Imgs": 0, #len(os.listdir("./molecular_imgs/casa/sink{:>03}/".format(int(isink)))) / len(snapshots) * 100
    }
    stats_df = pd.DataFrame.from_dict(sink_stats, orient='index', columns=["Completion Percentage"])
    st.bar_chart(stats_df, y="Completion Percentage", y_label="Percentage of snapshots completed")


def convergence(sink_id):
    (nstart, nend) = sink_dict[str(sink_id)]
    snapshots = np.arange(nstart, nend+1, 10)
    df = pd.read_csv("sink_histories/sink{:>03}_history.dat".format(int(sink_id)), names=["Sink Age", "Mass", "Accretion Rate"], header=1)
    df["Sink Age"] /= 1.0e3  # Convert to kyr
    df["Accretion Rate"] *= 1.0e3  # Convert to Msun/kyr

    unconverged_list = unconverged_sinkdict[str(sink_id)]
    fig1 = px.line(df, x="Sink Age", y="Mass", labels={'Sink Age':'Sink Age [kyr]', 'Mass':'Mass [Msun]'})
    
    # Create line segments with different colors for converged/unconverged
    for i in range(len(df) - 1):
        color = '#DC3912' if snapshots[i] in unconverged_list else '#3366CC'
        fig1.add_scatter(
            x=df["Sink Age"].iloc[i:i+2], 
            y=df["Mass"].iloc[i:i+2], 
            mode='lines', 
            line=dict(color=color, width=2),
            showlegend=False,
            hovertemplate=f"<b style='color:{color}'>Snapshot %{{customdata:04d}}</b><br>Sink Age: %{{x:.2f}} kyr<br>Mass: %{{y:.4f}} Msun<extra></extra>",
            customdata=snapshots[i:i+2]
        )
    fig1.data[0].visible = False  # Hide the original line from px.line
    st.plotly_chart(fig1)

st.title("Investigate Snapshot Statistics")
sink_buttons, option_buttons = st.columns(2, gap=None, width=800)

with sink_buttons:
    # Initialize selected_sinks from session state if not already set
    if st.session_state.selected_sinks is None:
        default_sinks = list(sink_dict.keys())
    else:
        # Ensure default_sinks are strings to match the options type
        default_sinks = [str(s) for s in st.session_state.selected_sinks]
    
    selected_sinks = st.pills("Select Sinks to View", options=list(sink_dict.keys()), default=default_sinks, selection_mode="multi")
    
    # Save to session state for persistence (keep as strings to match options)
    st.session_state.selected_sinks = selected_sinks
    
    # Convert to integers for processing
    selected_sinks = [int(sink) for sink in selected_sinks]
    selected_sinks.sort()

with option_buttons:
    selected_stats = st.pills("Select Statistics to View", options=["Basic Stats", "Completion Plot", "Convergence"], default=["Basic Stats"], selection_mode="single")

if selected_sinks != []:
    sink_cols = st.columns(int(len(selected_sinks)))

    for icol, sink_id in zip(sink_cols, selected_sinks):
        with icol:
            # Make header for each sink
            st.header(f"Sink {sink_id}")
            if selected_stats == "Basic Stats":
                basic_stats(sink_id)
            elif selected_stats == "Completion Plot":
                completion_plot(sink_id)
            elif selected_stats == "Convergence":
                convergence(sink_id)
                if icol == sink_cols[0]:
                    st.write("**Note:** Red segments indicate unconverged snapshots.")