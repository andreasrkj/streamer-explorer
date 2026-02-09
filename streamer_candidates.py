import os
import streamlit as st
st.set_page_config(layout="wide")
import numpy as np
from _dictionaries import sink_dict, view_keys, mol_keys, event_list, questioned_events
from collections import Counter

st.title("Explore Streamer Candidates", anchor=False)

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
        st.session_state.selected_event = None

    if isink is not None:
        # Format the event list
        events = []
        questionable_events = []
        for i, event in enumerate(event_list[str(isink)]):
            (nstart, nend, event_views, event_mols) = event
            fname = "sc_s{:03d}_{:04d}_{:04d}".format(int(isink), nstart, nend)
            events.append(fname)
        for i, event in enumerate(questioned_events[str(isink)]):
            (nstart, nend, event_views, event_mols) = event
            fname = "sc_s{:03d}_{:04d}_{:04d}".format(int(isink), nstart, nend)
            questionable_events.append(fname)
        # Let's check if there are ones with multiple configs, and rename accordingly
        c = Counter(events)
        dupes = {num: [i for i, x in enumerate(events) if x == num] for num, cnt in c.items() if cnt > 1}

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for iev in dupes.keys():
            # Append a letter if multiple duplicates
            for dupe in dupes[iev]:
                events[dupe] += alphabet[dupes[iev].index(dupe)]

        if st.session_state.selected_event is not None:
            event_index = events.index(st.session_state.selected_event)
        else:
            event_index = None

        ievent = st.selectbox("Select a streamer candidate event", events, index=event_index, 
                              placeholder="Select the streamer candidate event you wish to look at", accept_new_options=True)
        st.session_state.selected_event = ievent
if st.session_state.selected_event is not None:
    # Unpack the values of ievent
    (nstart, nend, event_views, event_mols) = event_list[str(isink)][events.index(st.session_state.selected_event)]
    with col2:
        # Create the buttons for possible selections
        if len(event_views) > 1: # If more than one view available
            view_options = [key for key, value in view_keys.items() if value in event_views]
            candidate_viewpoint = st.pills("Choose viewpoint", view_options, default=st.session_state.candidate_viewpoint)
            st.session_state.candidate_viewpoint = candidate_viewpoint
            
        else:
            st.session_state.candidate_viewpoint = event_views[0]

        if len(event_mols) > 1: # If more than one molecule available
            mol_options = [key for key, value in mol_keys.items() if value in event_mols]
            candidate_molecule = st.pills("Choose molecules", mol_options, default=st.session_state.candidate_molecule)
            st.session_state.candidate_molecule = candidate_molecule
        else:
            st.session_state.candidate_molecule = event_mols[0]

    if st.session_state.candidate_viewpoint is not None and st.session_state.candidate_molecule is not None:
        st.subheader("Temporal evolution :material/arrow_right_alt:", anchor=False)
        # Figure out how many imgs to make
        snaps = np.arange(nstart, nend+1, 10)
        stream_cols = st.columns(len(snaps))
        for i, icol in enumerate(stream_cols):
            with icol:
                for moment in [8,9]:
                    # Generate the name using the session state variables
                    mol_name = st.session_state.candidate_molecule
                    if mol_name in ["13co", "c18o"]:
                        img_name = "simalma_moment-{}-map-{}-{}-npix400-5000au-transition2-widthkms8-lines201.png".format(
                        moment,
                        mol_name,
                        st.session_state.candidate_viewpoint
                        )
                    elif mol_name == "ph2co":
                        img_name = "simalma_moment-{}-map-{}-{}-npix400-5000au-transition3-widthkms8-lines201.png".format(
                        moment,
                        mol_name,
                        st.session_state.candidate_viewpoint
                        )
                    try:
                        st.image("./molecular_imgs/casa/sink{:>03}/nout{:>04}/".format(isink, snaps[i])+img_name)
                    except:
                        st.error("CASA simalma image not found for this snapshot and viewpoint.")
    if st.session_state.selected_event in questionable_events:
        st.warning("This event has been marked as questionable.")