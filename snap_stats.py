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

def _get_missing_files(sink_id, folder="./temperatures/"):
    # Now check whether any images are missing in the folder
    missing_files = [[],[],[]] # face-on, edge-on (A), edge-on (B)
    (nstart, nend) = sink_dict[str(sink_id)]
    snapshots = np.arange(nstart, nend+1, 10)

    for iout in snapshots:
        try:
            files = os.listdir(os.path.join(folder, "sink{:>03}/nout{:>04}/".format(sink_id, iout)))
            if not any("face-on" in fname for fname in files):
                missing_files[0].append(int(iout))
            if not any("edge-on-A" in fname for fname in files):
                missing_files[1].append(int(iout))
            if not any("edge-on-B" in fname for fname in files):
                missing_files[2].append(int(iout))
        except FileNotFoundError:
            missing_files[0].append(int(iout))
            missing_files[1].append(int(iout))
            missing_files[2].append(int(iout))

    return missing_files

def basic_stats(sink_id):
    # Show snapshot range, count, unconverged count
    snap_min, snap_max = sink_dict[str(sink_id)]
    total_snaps = len(np.arange(snap_min, snap_max+1, 10))
    st.markdown(f"**Calculation Time (CPU hrs):** {np.round(total_calculation_time[str(sink_id)],2)}")
    st.markdown(f"**Snapshot Range:** {snap_min} - {snap_max}")
    st.markdown(f"**Total Snapshots:** {total_snaps}")

def _format_missing_range(missing_list, snapshots):
    """Format missing file list as a string or range."""
    if len(missing_list) == 0:
        return None
    if missing_list == snapshots.tolist():
        return "All"
    if len(missing_list) > 1:
        if missing_list == np.arange(int(missing_list[0]), int(missing_list[-1])+1, 10).tolist():
            return f"{missing_list[0]}-{missing_list[-1]}"
    return missing_list

def _display_missing_files(title, missing_data, snapshots=None):
    """Display missing files in a compact list format."""
    if any(len(missing) > 0 for missing in missing_data):
        st.markdown(f"**{title}:**")
        labels = ["Face-On", "Edge-On (A)", "Edge-On (B)"]
        list_items = []
        for i, label in enumerate(labels):
            if len(missing_data[i]) > 0:
                formatted = _format_missing_range(missing_data[i], snapshots) if snapshots is not None else missing_data[i]
                list_items.append(f"{label}: {formatted}")
        st.markdown("\n".join([f"- {item}" for item in list_items]))

def completion_plot(sink_id):
    (nstart, nend) = sink_dict[str(sink_id)]
    snapshots = np.arange(nstart, nend+1, 10)
    num_snapshots = len(snapshots)
    sink_path = f"sink{int(sink_id):>03}"

    # Calculate completion statistics
    folders = {
        "Convergence": f"./convergence_plots/{sink_path}/",
        "Column Density": f"./column_densities/{sink_path}/",
        "Temperature": f"./temperatures/{sink_path}/",
        "RADMC-3D Imgs": f"./molecular_imgs/radmc/{sink_path}/",
        "SimALMA Imgs": f"./molecular_imgs/casa/{sink_path}/",
    }
    
    sink_stats = {name: len(os.listdir(folder)) / num_snapshots * 100 
                  for name, folder in folders.items() if name != "SimALMA Imgs"}
    sink_stats["SimALMA Imgs"] = 0
    
    stats_df = pd.DataFrame.from_dict(sink_stats, orient='index', columns=["Completion Percentage"])
    st.bar_chart(stats_df, y="Completion Percentage", y_label="Percentage of snapshots completed")

    # Check for missing files
    missing_temps = _get_missing_files(sink_id, folder="./temperatures/")
    missing_coldens = _get_missing_files(sink_id, folder="./column_densities/")
    missing_imgs = _get_missing_files(sink_id, folder="./molecular_imgs/radmc/")
    missing_simalma = _get_missing_files(sink_id, folder="./molecular_imgs/casa/")

    # Display missing files
    _display_missing_files("Missing Temperatures", missing_temps, snapshots)
    _display_missing_files("Missing Column Densities", missing_coldens, snapshots)
    _display_missing_files("Missing RADMC-3D Images", missing_imgs, snapshots)
    _display_missing_files("Missing SimALMA Images", missing_simalma, snapshots)


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

    unconverged_list = unconverged_sinkdict[str(sink_id)]
    unconverged_count = len(unconverged_list)
    st.markdown(f"**Unconverged Snapshots:** {unconverged_count}")
    if unconverged_count > 0:
        st.markdown(f"**Unconverged Snapshot List:** {unconverged_list}")

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
    selected_stats = st.pills("Select Statistics to View", options=["Basic Stats", "Completion Plot", "Convergence"], default=st.session_state.selected_stats if st.session_state.selected_stats else "Basic Stats", selection_mode="single")
    st.session_state.selected_stats = selected_stats

if selected_sinks != []:
    sink_cols = st.columns(int(len(selected_sinks)))

    for icol, sink_id in zip(sink_cols, selected_sinks):
        with icol:
            # Make header for each sink
            st.header(f"Sink {sink_id}")
            if st.session_state.selected_stats == "Basic Stats":
                basic_stats(sink_id)
            elif st.session_state.selected_stats == "Completion Plot":
                completion_plot(sink_id)
            elif st.session_state.selected_stats == "Convergence":
                convergence(sink_id)
                if icol == sink_cols[0]:
                    st.warning("**Note:** Red segments indicate unconverged snapshots.")