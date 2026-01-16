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

coldens_names = {
    "Face On": "coldens-face-on-res1000-width5000-dz5000.png",
    "Edge On (A)": "coldens-edge-on-A-res1000-width5000-dz5000.png",
    "Edge On (B)": "coldens-edge-on-B-res1000-width5000-dz5000.png"
}

temp_names = {
    "Face On": "temperature-face-on-res1000-width5000-dz5000.png",
    "Edge On (A)": "temperature-edge-on-A-res1000-width5000-dz5000.png",
    "Edge On (B)": "temperature-edge-on-B-res1000-width5000-dz5000.png"
}

st.title("Streamer data")

if "display_iout_options" not in st.session_state:
    st.session_state.display_iout_options = True
if "selected_point" not in st.session_state:
    st.session_state.selected_point = None
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False
if "page" not in st.session_state:
    st.session_state.page = None
if "viewpoint" not in st.session_state:
    st.session_state.viewpoint = None
if "molecule" not in st.session_state:
    st.session_state.molecule = None
if "moment" not in st.session_state:
    st.session_state.moment = None
if "current_sink" not in st.session_state:
    st.session_state.current_sink = None
if "image_type" not in st.session_state:
    st.session_state.image_type = None

# Create columns (one for selection, another for the data itself)
col1, col2 = st.columns(2)

with col1:
    isink = st.selectbox(
        "Select the sink you wish to look at",
        tuple(sink_dict.keys()),
        index=None,
        placeholder="Select the sink you wish to look at",
        accept_new_options=True
    )

    # Reset iout and selected_point if sink changes
    if isink != st.session_state.current_sink:
        st.session_state.current_sink = isink
        st.session_state.selected_point = None

    if isink is not None:
        (nstart, nend) = sink_dict[str(isink)]
        snapshots = np.arange(nstart, nend+1, 10)
        st.session_state.display_iout_options = False
        
        # Set iout based on selected point
        if st.session_state.selected_point is not None:
            iout = snapshots[st.session_state.selected_point]
        else:
            iout = None

        df = pd.read_csv("sink_histories/sink{:>03}_history.dat".format(int(isink)), names=["Sink Age", "Mass", "Accretion Rate"], header=1)
        df["Sink Age"] /= 1.0e3  # Convert to kyr
        df["Accretion Rate"] *= 1.0e3  # Convert to Msun/kyr

        chartcol1, chartcol2 = st.columns(2)
        
        with chartcol1:
            fig1 = px.line(df, x="Sink Age", y="Mass", labels={'Sink Age':'Sink Age [kyr]', 'Mass':'Mass [Msun]'})
            fig1.update_layout(clickmode='select', overwrite=True)
            fig1.update_traces(customdata=snapshots, hovertemplate="<b>Snapshot %{customdata:04d}</b><br>Sink Age: %{x:.2f} kyr<br>Mass: %{y:.4f} Msun<extra></extra>", mode="lines+markers")
            
            # Add selected points if any
            if st.session_state.selected_point is not None:
                fig1.update_traces(selectedpoints=[st.session_state.selected_point])
            
            event1 = st.plotly_chart(fig1, key="chart1", on_select="rerun")
            
            # Update session state if a point was selected in chart1
            if event1.selection.points:
                new_point = event1.selection.point_indices[0]
                if st.session_state.selected_point != new_point:
                    st.session_state.selected_point = new_point
                    st.rerun()

        with chartcol2:
            fig2 = px.line(df, x="Sink Age", y="Accretion Rate", labels={'Sink Age':'Sink Age [kyr]', 'Accretion Rate':'Accretion Rate [Msun/kyr]'})
            fig2.update_layout(clickmode='select', overwrite=True)
            fig2.update_traces(customdata=snapshots, hovertemplate="<b>Snapshot %{customdata:04d}</b><br>Sink Age: %{x:.2f} kyr<br>Accretion Rate: %{y:.4f} Msun/kyr<extra></extra>", mode="lines+markers")
            
            # Add selected points if any
            if st.session_state.selected_point is not None:
                fig2.update_traces(selectedpoints=[st.session_state.selected_point])
            
            event2 = st.plotly_chart(fig2, key="chart2", on_select="rerun")
            
            # Update session state if a point was selected in chart2
            if event2.selection.points:
                new_point = event2.selection.point_indices[0]
                if st.session_state.selected_point != new_point:
                    st.session_state.selected_point = new_point
                    st.rerun()
    
        # Create graph showing how much is finished of column densities, temperatures, images, etc.
        sink_stats = {
            "Dust Temperature": len(os.listdir("./convergence_plots/sink{:>03}/".format(int(isink)))) / len(snapshots) * 100,
            "Column Densities": len(os.listdir("./column_densities/sink{:>03}/".format(int(isink)))) / len(snapshots) * 100,
            "Temperatures": len(os.listdir("./temperatures/sink{:>03}/".format(int(isink)))) / len(snapshots) * 100,
            "RADMC-3D Images": 0, #len(os.listdir("./molecular_imgs/radmc/sink{:>03}/".format(int(isink)))) / len(snapshots) * 100,
            "CASA simalma Images": 0, #len(os.listdir("./molecular_imgs/casa/sink{:>03}/".format(int(isink)))) / len(snapshots) * 100
        }
        stats_df = pd.DataFrame.from_dict(sink_stats, orient='index', columns=["Completion Percentage"])
        st.bar_chart(stats_df, y="Completion Percentage", y_label="Percentage of snapshots completed", horizontal=True)

with col2:
    if isink is not None and iout is not None:
        header_col, selection_col = st.columns(2)
        with header_col:
            st.header("Snapshot {:>04}".format(iout))
        with selection_col:
            page = st.pills("Select data tab", ["Snapshot Data", "Convergence", "Column Density", "Temperature", "Images"], selection_mode="single", default=st.session_state.page, key="page_pills")
            st.session_state.page = page

        if selection_col is not None:
            if page == "Snapshot Data":
                selected_row = df.iloc[st.session_state.selected_point]
                data = {
                    "Sink Age [kyr]": f"{selected_row['Sink Age']:.2f}",
                    "Mass [Msun]": f"{selected_row['Mass']:.4f}",
                    "Accretion Rate [Msun/kyr]": f"{selected_row['Accretion Rate']:.4f}"
                }
                st.dataframe(pd.DataFrame([data]).T, width="stretch")
                if iout in unconverged_sinkdict[str(isink)]:
                    st.warning("This snapshot is unconverged.")
            elif page == "Convergence":   
                img_path = os.path.join("./convergence_plots", "sink{:>03}".format(isink), "o{:>04}.png".format(iout))
                st.image(img_path, caption="WARNING: Please note the error in the legend. Top line should be $1 \\times 10^6$")
                if iout in unconverged_sinkdict[str(isink)]:
                    st.warning("This snapshot is unconverged.")
            elif page == "Column Density":
                viewpoint = st.pills("View Direction", ["Face On", "Edge On (A)", "Edge On (B)"], selection_mode="single", default=st.session_state.viewpoint)
                st.session_state.viewpoint = viewpoint
                if st.session_state.viewpoint is not None:
                    try:
                        st.image("./column_densities/sink{:>03}/nout{:>04}/".format(isink, iout)+coldens_names[st.session_state.viewpoint])
                    except: 
                        st.error("Column density image not found for this snapshot and viewpoint.")
                if iout in unconverged_sinkdict[str(isink)]:
                    st.warning("This snapshot is unconverged.")
            elif page == "Temperature":
                viewpoint = st.pills("View Direction", ["Face On", "Edge On (A)", "Edge On (B)"], selection_mode="single", default=st.session_state.viewpoint)
                st.session_state.viewpoint = viewpoint
                if st.session_state.viewpoint is not None:
                    try:
                        st.image("./temperatures/sink{:>03}/nout{:>04}/".format(isink, iout)+temp_names[st.session_state.viewpoint])
                    except:
                        st.error("Temperature image not found for this snapshot and viewpoint.")
                if iout in unconverged_sinkdict[str(isink)]:
                    st.warning("This snapshot is unconverged.")
            elif page == "Images":
                option_col, img_col = st.columns(2)
                with option_col:
                    viewpoint = st.pills("View Direction", ["Face On", "Edge On (A)", "Edge On (B)"], selection_mode="single", default=st.session_state.viewpoint, key="viewpoint_pills")
                    st.session_state.viewpoint = viewpoint
                    if st.session_state.viewpoint is not None:
                        molecule = st.pills("Molecular Transition", ["H$_2$CO J = 3-2", "$^{13}$CO J = 2-1", "C$^{18}$O J = 2-1"], selection_mode="single", default=st.session_state.molecule, key="molecule_pills")
                        st.session_state.molecule = molecule
                    if st.session_state.molecule is not None and st.session_state.viewpoint is not None:
                        moment = st.pills("Select moment to view", ["Moment 0", "Moment 1", "Moment 8", "Moment 9"], selection_mode="single", default=st.session_state.moment, key="moment_pills")
                        st.session_state.moment = moment
                with img_col:
                    if st.session_state.moment is not None and st.session_state.viewpoint is not None and st.session_state.molecule is not None:
                        img_type = st.pills("Choose image type", ["Image generated by RADMC-3D", "Image run through CASA simalma"], selection_mode="single", default=st.session_state.image_type, 
                                            key="image_type_pills", width="stretch")
                        st.session_state.image_type = img_type
                        if st.session_state.image_type == "Image generated by RADMC-3D":
                            st.write(f"RADMC-3D IMAGE | Showing view: {viewpoint} for molecular transition {molecule} in {moment}")
                        elif st.session_state.image_type == "Image run through CASA simalma":
                            st.write(f"CASA SIMALMA IMAGE | Showing view: {viewpoint} for molecular transition {molecule} in {moment}")
                if iout in unconverged_sinkdict[str(isink)]:
                    st.warning("This snapshot is unconverged.")