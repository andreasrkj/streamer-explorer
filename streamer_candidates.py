import os
import streamlit as st
st.set_page_config(layout="wide")
import numpy as np
from _dictionaries import sink_dict, view_keys, mol_keys, candidate_dir, candidatenote_dir, data_url
from collections import Counter

# FUNCTION DEFINITIONS
def show_image(radmc=False, simalma=False, view=st.session_state.viewpoint, molecule=st.session_state.molecule, moment=st.session_state.moment):
    if simalma:
        img_path = data_url+"molecular_imgs/casa/sink{:>03}/nout{:>04}/".format(isink, iout) + "simalma_"
        err_msg  = "CASA simalma image not found for this snapshot and viewpoint."
    elif radmc:
        img_path = data_url+"molecular_imgs/radmc/sink{:>03}/nout{:>04}/".format(isink, iout)
        err_msg  = "RADMC-3D image not found for this snapshot and viewpoint."

    # Generate the name using the session state variables
    if molecule == "$^{13}$CO J = 2-1" or molecule == "C$^{18}$O J = 2-1":
        img_name = "moment-{}-map-{}-{}-npix400-5000au-transition2-widthkms8-lines201.png".format(
        moment.split()[-1],
        molecule.replace("$^{13}$CO J = 2-1", "13co").replace("C$^{18}$O J = 2-1", "c18o"),
        view_keys[view]
        )
    elif molecule == "H$_2$CO J = 3$_{0,3}$-2$_{0,2}$":
        img_name = "moment-{}-map-{}-{}-npix400-5000au-transition3-widthkms8-lines201.png".format(
        moment.split()[-1],
        molecule.replace("H$_2$CO J = 3$_{0,3}$-2$_{0,2}$", "ph2co"),
        view_keys[view]
        )
    try:
        st.image(img_path+img_name)
    except:
        st.error(err_msg)

def show_coldens(view=st.session_state.viewpoint):
    try:
        st.image(data_url+"column_densities/sink{:>03}/nout{:>04}/".format(isink, iout)+"coldens-{}-res1000-width5000-dz5000.png".format(view_keys[view]))
    except: 
        st.error("Column density image not found for this snapshot and viewpoint.")

def show_temp(view=st.session_state.viewpoint):
    try:
        st.image(data_url+"temperatures/sink{:>03}/nout{:>04}/".format(isink, iout)+"temperature-{}-res1000-width5000-dz5000.png".format(view_keys[view]))
    except:
        st.error("Temperature image not found for this snapshot and viewpoint.")

title_col, option_col = st.columns([1,2])
with title_col:
    st.title("Explore Streamer Candidates", anchor=False)
with option_col:
    candidate_viewoption = st.pills("Select how to view the candidates", ["As Video", "As Scrollable Images"], selection_mode="single", default=st.session_state.candidate_viewoption)
    st.session_state.candidate_viewoption = candidate_viewoption

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
        st.session_state.selected_point = None

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
            st.write("**View:** "+st.session_state.candidate_viewpoint)

        if len(event_mols) > 1: # If more than one molecule available
            mol_options = [key for key, value in mol_keys.items() if value in event_mols]
            candidate_molecule = st.pills("Choose molecules", mol_options, default=st.session_state.candidate_molecule)
            st.session_state.candidate_molecule = candidate_molecule
        else:
            st.session_state.candidate_molecule = list(mol_keys.keys())[list(mol_keys.values()).index(event_mols[0])]
            st.write("**Molecule:** "+st.session_state.candidate_molecule)

    if st.session_state.candidate_viewpoint is not None and st.session_state.candidate_molecule is not None:
        # Get molecule name as [-4:] to get "ph2co" -> "h2co"
        iview = view_keys[st.session_state.candidate_viewpoint]
        imol = mol_keys[st.session_state.candidate_molecule][-4:]

        # Check if we want to view as video
        if st.session_state.candidate_viewoption == "As Video":
            anim_name = "sc_s{:03d}_{:04d}_{:04d}_{}_{}".format(int(isink), nstart, nend, iview, imol)
            output_path = "candidate_animations/sink{:03d}/".format(int(isink))+anim_name+".mp4"
            
            # Add the video playback
            st.video(data_url+output_path, loop=True, autoplay=True, muted=True)

            st.info("**Note attributed to this candidate:** "+candidate_note, icon=":material/note_stack:")

        elif st.session_state.candidate_viewoption == "As Scrollable Images":
            # Just print all the images at this point
            choice_col, slider_col = st.columns(2)
            with choice_col:
                scrollable_choices = st.pills("Choose which images to view", ["Column Density", "Temperature", "Moment 0", "Moment 1", "Moment 2", "Moment 8", "Moment 9"], 
                                            selection_mode="multi", default=st.session_state.candidate_scrollable_choices)
                st.session_state.candidate_scrollable_choices = scrollable_choices
            with slider_col:
                istart, iend = st.select_slider("Select snapshot range to display", options=np.arange(nstart, nend+1, 10), value=(nstart, nend))

            for iout in np.arange(istart, iend+1, 10):
                st.markdown(f"**Snapshot {iout}**", text_alignment="center")
                img_cols = st.columns(len(st.session_state.candidate_scrollable_choices))

                for i, icol in enumerate(img_cols):
                    with icol:
                        if st.session_state.candidate_scrollable_choices[i] == "Column Density":
                            if iout == istart: st.write("Column Density")
                            show_coldens(view=st.session_state.candidate_viewpoint)
                        elif st.session_state.candidate_scrollable_choices[i] == "Temperature":
                            if iout == istart: st.write("Temperature")
                            show_temp(view=st.session_state.candidate_viewpoint)
                        elif "Moment" in st.session_state.candidate_scrollable_choices[i]:
                            if iout == istart: st.write(st.session_state.candidate_scrollable_choices[i])
                            show_image(simalma=True, view=st.session_state.candidate_viewpoint, 
                                       molecule=st.session_state.candidate_molecule, 
                                       moment=st.session_state.candidate_scrollable_choices[i])

    with col3:
        if st.session_state.candidate_viewoption == "As Video":
            # This column displays info that seems necessary to know when you get the video
            message = "**Once viewpoint and molecule is selected, a video of the candidate will appear.**\n" \
                    "The video below displays **one** snapshot per second.\n" \
                    "The moments from left to right: 0, 1, 2, 8 and 9.\n" \
                    "The video automatically loops when it reaches the final snapshot.\n"

            st.info(message, icon=":material/info:")
        elif st.session_state.candidate_viewoption == "As Scrollable Images":
            st.info("**Note attributed to this candidate:** "+candidate_note, icon=":material/note_stack:")