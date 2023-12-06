import miditoolkit
import mido
import os
from tqdm import tqdm
import pickle
from parallelbar import progress_map

import argparse

def is_solo_piano(midi_file):

    try:

        piano_paths = []
        
        mid = mido.MidiFile(midi_file)
        check = False # check based on track names
        check2 = True # check based on MIDI programs
    
        # Track name check
        
        # Keep track of unique track names
        track_names = set()
        if len(mid.tracks) > 1:
            for i, track in enumerate(mid.tracks[1:]):
                for msg in track:
                    if msg.type == 'track_name':
                        # 'track_name' messages indicate the name of the track
                        track_names.add(msg.name)
                        continue
        else:
            for msg in mid.tracks[0]:
                if msg.type == 'track_name':
                    # 'track_name' messages indicate the name of the track
                    track_names.add(msg.name)
                    continue
        
        # Check if all track names indicate keyboard
        piano_like_instruments = {'piano', 'keyboard', 'clavichord', 'harpsichord', 'celesta', 'fortepiano'}
        if len(track_names) > 0:
            check =  all(any(keyword in name.lower() for keyword in piano_like_instruments) for name in track_names) # True if all tracks are keyboards
    
        # MIDI Program check
    
        piano_instruments = {0,1,2,3,4,5,6,7} # keyboard instruments
    
        for track in mid.tracks:
            instruments_in_track = set()
            for msg in track:
                if msg.type == 'program_change':
                    instruments_in_track.add(msg.program)
                    
            if not instruments_in_track.issubset(piano_instruments):
                check2 = False # set check2 to False if there is a MIDI program not in piano_instruments
    
        if check or check2: # Return True if either check is satsfied 
            return midi_file
    except:
        pass
        
if __name__=='__main__':

    # Define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_in", type=str, help="Specify the in path")
    args = parser.parse_args()

    filez_path = args.path_in
    filez = list()
    for (dirpath, dirnames, filenames) in os.walk(filez_path):
        filez += [os.path.join(dirpath, file) for file in filenames if file.lower().endswith((".mid", ".midi"))]
    
    res = progress_map(is_solo_piano, filez, process_timeout=50, n_cpu=60)
    pickle.dump(res, open("piano_paths.p", "wb"))


