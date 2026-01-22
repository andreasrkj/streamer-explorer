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

view_keys = {
    "Face On": "face-on",
    "Edge On (A)": "edge-on-A",
    "Edge On (B)": "edge-on-B"
}


st.title("Streamer data")

if "display_iout_options" not in st.session_state:
    st.session_state.display_iout_options = True
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False
if "page" not in st.session_state:
    st.session_state.page = None

# Create columns (one for selection, another for the data itself)
col1, col2 = st.columns(2)

with col1:
    # Find the index of the currently selected sink if it exists
    sink_options = tuple(sink_dict.keys())
    current_index = None
    if st.session_state.current_sink is not None:
        try:
            current_index = sink_options.index(str(st.session_state.current_sink))
        except ValueError:
            current_index = None
    
    isink = st.selectbox(
        "Select the sink you wish to look at",
        sink_options,
        index=current_index,
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

        # Snapshot step controls
        prev_col, next_col = st.columns(2)
        with prev_col:
            if st.button("Previous snapshot", use_container_width=True):
                if len(snapshots) > 0:
                    if st.session_state.selected_point is None:
                        st.session_state.selected_point = len(snapshots) - 1
                    else:
                        st.session_state.selected_point = (st.session_state.selected_point - 1) % len(snapshots)
                    st.rerun()
        with next_col:
            if st.button("Next snapshot", use_container_width=True):
                if len(snapshots) > 0:
                    if st.session_state.selected_point is None:
                        st.session_state.selected_point = 0
                    else:
                        st.session_state.selected_point = (st.session_state.selected_point + 1) % len(snapshots)
                    st.rerun()
        
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
    
        # Create graph showing data for bolometric temperature
        if os.path.exists("tbol_data/sink{:>03}.csv".format(int(isink))):
            df_tbol = pd.read_csv("tbol_data/sink{:>03}.csv".format(int(isink)), names=["Sink Age", "Face On", "Edge On (A)", "Edge On (B)"], header=1)
            fig3 = px.line(df_tbol, x="Sink Age", y=df_tbol.columns[1:], labels={'Sink Age': 'Sink Age [kyr]'})
            fig3.add_hline(y=70, line_dash="dot", line_color="grey", annotation_text="Class 0/I", annotation_position="top left")
            fig3.update_layout(clickmode='select', overwrite=True, hovermode="x unified", yaxis_title="Bolometric Temperature [K]", hoverlabel=dict(align="left"),
                                xaxis=dict(showspikes=True,spikemode="across",spikethickness=1,spikecolor="#888"))
            snap_array = np.full(len(df_tbol), np.nan)
            snap_fill = min(len(snapshots), len(df_tbol))
            snap_array[:snap_fill] = snapshots[:snap_fill]  

            hoverdata = np.column_stack((snap_array,df_tbol["Sink Age"],df_tbol["Face On"],df_tbol["Edge On (A)"],df_tbol["Edge On (B)"]))

            fig3.update_traces(customdata=hoverdata,mode="lines+markers",hoverinfo="skip",hovertemplate=None)

            unified_hover = "<b>Snapshot %{customdata[0]:04d}</b><br>" \
                             "Sink Age: %{customdata[1]:.2f} kyr<br>" \
                             "Face On: %{customdata[2]:.2f} K<br>" \
                             "Edge On (A): %{customdata[3]:.2f} K<br>" \
                             "Edge On (B): %{customdata[4]:.2f} K<extra></extra>"

            fig3.add_scatter(x=df_tbol["Sink Age"],y=df_tbol["Face On"],customdata=hoverdata,mode="markers",marker=dict(size=12, color="rgba(0,0,0,0)"),
                             hovertemplate=unified_hover,hoverinfo="text",showlegend=False)
            
            # Add selected points if any
            if st.session_state.selected_point is not None:
                fig3.update_traces(selectedpoints=[st.session_state.selected_point])
            
            event3 = st.plotly_chart(fig3, key="chart3", on_select="rerun")

            # Update session state if a point was selected in chart3
            if event3.selection.points:
                new_point = event3.selection.point_indices[0]
                if st.session_state.selected_point != new_point:
                    st.session_state.selected_point = new_point
                    st.rerun()

with col2:
    if isink is not None and iout is not None:
        header_col, selection_col = st.columns(2)
        with header_col:
            st.header("Snapshot {:>04}".format(iout))
        with selection_col:
            page = st.pills("Select data tab", ["Snapshot Data", "Convergence", "Column Density", "Temperature", "Images"], selection_mode="single", default=st.session_state.page, key="page_pills", width="stretch")
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

            elif page == "Convergence":   
                img_path = os.path.join("./convergence_plots", "sink{:>03}".format(isink), "o{:>04}.png".format(iout))
                st.image(img_path, caption="WARNING: Please note the error in the legend. Top line should be $1 \\times 10^6$")

            elif page in ["Column Density", "Temperature", "Images"]:
                option_col, img_col = st.columns(2)

                with option_col:
                    viewpoint = st.pills("View Direction", ["Face On", "Edge On (A)", "Edge On (B)"], selection_mode="single", default=st.session_state.viewpoint, key="viewpoint_pills", width="stretch")
                    st.session_state.viewpoint = viewpoint
                    if page == "Images" and st.session_state.viewpoint is not None:
                        molecule = st.pills("Molecular Transition", ["H$_2$CO J = 3$_{0,3}$-2$_{0,2}$", "$^{13}$CO J = 2-1", "C$^{18}$O J = 2-1"], selection_mode="single", default=st.session_state.molecule, 
                                            key="molecule_pills", width="stretch")
                        st.session_state.molecule = molecule
                    if page == "Images" and st.session_state.molecule is not None and st.session_state.viewpoint is not None:
                        moment = st.pills("Select moment to view", ["Moment 0", "Moment 1", "Moment 8", "Moment 9"], selection_mode="single", default=st.session_state.moment, key="moment_pills", width="stretch")
                        st.session_state.moment = moment
                    if page == "Images" and st.session_state.molecule is not None and st.session_state.viewpoint is not None and st.session_state.moment is not None:
                        img_type = st.pills("Choose image type", ["Image generated by RADMC-3D", "Image run through CASA simalma"], selection_mode="single", default=st.session_state.image_type, 
                                            key="image_type_pills", width="stretch")
                        st.session_state.image_type = img_type

                with img_col:
                    if page == "Column Density":
                        if st.session_state.viewpoint is not None:
                            try:
                                st.image("./column_densities/sink{:>03}/nout{:>04}/".format(isink, iout)+"coldens-{}-res1000-width5000-dz5000.png".format(view_keys[st.session_state.viewpoint]))
                            except: 
                                st.error("Column density image not found for this snapshot and viewpoint.")
                    elif page == "Temperature":
                        if st.session_state.viewpoint is not None:
                            try:
                                st.image("./temperatures/sink{:>03}/nout{:>04}/".format(isink, iout)+"temperature-{}-res1000-width5000-dz5000.png".format(view_keys[st.session_state.viewpoint]))
                            except:
                                st.error("Temperature image not found for this snapshot and viewpoint.")
                    elif page == "Images":
                        if st.session_state.image_type == "Image generated by RADMC-3D":
                            # Generate the name using the session state variable
                            if st.session_state.molecule == "$^{13}$CO J = 2-1" or st.session_state.molecule == "C$^{18}$O J = 2-1":
                                img_name = "moment-{}-map-{}-{}-npix400-5000au-transition2-widthkms8-lines201.png".format(
                                st.session_state.moment.split()[-1],
                                st.session_state.molecule.replace("$^{13}$CO J = 2-1", "13co").replace("C$^{18}$O J = 2-1", "c18o"),
                                view_keys[st.session_state.viewpoint]
                                )
                            elif st.session_state.molecule == "H$_2$CO J = 3$_{0,3}$-2$_{0,2}$":
                                img_name = "moment-{}-map-{}-{}-npix400-5000au-transition3-widthkms8-lines201.png".format(
                                st.session_state.moment.split()[-1],
                                st.session_state.molecule.replace("H$_2$CO J = 3$_{0,3}$-2$_{0,2}$", "ph2co"),
                                view_keys[st.session_state.viewpoint]
                                )
                            try:
                                st.image("./molecular_imgs/radmc/sink{:>03}/nout{:>04}/".format(isink, iout)+img_name)
                            except:
                                st.error("RADMC-3D image not found for this snapshot and viewpoint.")

                        elif st.session_state.image_type == "Image run through CASA simalma":
                            # Generate the name using the session state variables
                            img_name = "simalma_moment-{}-map-{}-{}-npix400-5000au-transition2-widthkms8-lines201.png".format(
                                st.session_state.moment.split()[-1],
                                st.session_state.molecule.replace("$^{13}$CO J = 2-1", "13co").replace("C$^{18}$O J = 2-1", "c18o").replace("H$_2$CO J = 3$_{0,3}$-2$_{0,2}$", "ph2co"),
                                view_keys[st.session_state.viewpoint]
                            )
                            try:
                                st.image("./molecular_imgs/casa/sink{:>03}/nout{:>04}/".format(isink, iout)+img_name)
                            except:
                                st.error("CASA simalma image not found for this snapshot and viewpoint.")
                        
            if iout in unconverged_sinkdict[str(isink)]:
                st.warning("This snapshot's dust temperature distribution is unconverged.")