import os
import streamlit as st
st.set_page_config(layout="wide")
import numpy as np
from _dictionaries import sink_dict, view_keys, mol_keys, candidate_dir, candidatenote_dir
from collections import Counter

st.title("Explore Streamer Candidates", anchor=False)

# Create columns (one for selection, another for the data itself)
col1, col2, col3 = st.columns(3)

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
        for i, event in enumerate(candidate_dir[int(isink)]):
            (nstart, nend, event_views, event_mols) = event
            fname = "sc_s{:03d}_{:04d}_{:04d}".format(int(isink), nstart, nend)
            events.append(fname)
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
        # Reset values if event is changed
        if ievent != st.session_state.selected_event:
            st.session_state.selected_event = ievent
            st.session_state.candidate_viewpoint = None
            st.session_state.candidate_molecule = None
            
if st.session_state.selected_event is not None:
    # Unpack the values of ievent
    (nstart, nend, event_views, event_mols) = candidate_dir[int(isink)][events.index(st.session_state.selected_event)]
    candidate_note = candidatenote_dir[int(isink)][events.index(st.session_state.selected_event)]
    with col2:
        # Create the buttons for possible selections
        if len(event_views) > 1: # If more than one view available
            view_options = [key for key, value in view_keys.items() if value in event_views]
            candidate_viewpoint = st.pills("Choose viewpoint", view_options, default=st.session_state.candidate_viewpoint)
            st.session_state.candidate_viewpoint = candidate_viewpoint
        else:
            st.session_state.candidate_viewpoint = list(view_keys.keys())[list(view_keys.values()).index(event_views[0])]

        if len(event_mols) > 1: # If more than one molecule available
            mol_options = [key for key, value in mol_keys.items() if value in event_mols]
            candidate_molecule = st.pills("Choose molecules", mol_options, default=st.session_state.candidate_molecule)
            st.session_state.candidate_molecule = candidate_molecule
        else:
            st.session_state.candidate_molecule = list(mol_keys.keys())[list(mol_keys.values()).index(event_mols[0])]

    if st.session_state.candidate_viewpoint is not None and st.session_state.candidate_molecule is not None:
        # If we have the viewpoint and molecule, we can get the 

        # Get molecule name as [-4:] to get "ph2co" -> "h2co"
        iview = view_keys[st.session_state.candidate_viewpoint]
        imol = mol_keys[st.session_state.candidate_molecule][-4:]

        anim_name = "sc_s{:03d}_{:04d}_{:04d}_{}_{}".format(int(isink), nstart, nend, iview, imol)
        output_path = "./candidate_animations/sink{:03d}/".format(int(isink))+anim_name+".mp4"
        
        # Add the video playback
        st.video(output_path, loop=True, autoplay=True, muted=True)

        st.info("**Note attributed to this candidate:\n"+candidate_note, icon=":material/note_stack:")

    with col3:
        # This column displays info that seems necessary to know when you get the video
        message = "**Once viewpoint and molecule is selected, a video of the candidate will appear.**\n" \
                  "The video below displays **one** snapshot per second.\n" \
                  "The moments from left to right: 0, 1, 2, 8 and 9.\n" \
                  "The video automatically loops when it reaches the final snapshot.\n"

        st.info(message, icon=":material/info:")