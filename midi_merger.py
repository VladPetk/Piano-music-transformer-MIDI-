import miditoolkit
import os
import pickle
from parallelbar import progress_map

from functools import partial

import argparse

def merge_tracks(midi_path, dir_out="merged_midi"):
    try:
        midi_file = miditoolkit.MidiFile(midi_path)
        
        # Check if the MIDI file has more than one instrument
        if len(midi_file.instruments) > 1:
            notes = []
            for inst in midi_file.instruments:
                notes.extend(inst.notes)
            
            # Create a new instrument in the new MIDI file
            new_instrument = miditoolkit.Instrument(0)  # 0 - Piano
            
            # Add the merged notes to the new instrument
            new_instrument.notes = notes
            
            # Add the new instrument to the MIDI file
            midi_file.instruments.append(new_instrument)
    
            # Remove the old instrument
            midi_file.instruments = midi_file.instruments[-1:]
            
            # Save the new MIDI file
            path_out = dir_out + '/' + os.path.basename(midi_path)
            midi_file.dump(path_out)
        else: # write unchanged if only one track
            path_out = dir_out + '/' + os.path.basename(midi_path)
            midi_file.dump(path_out)
    except:
        pass

if __name__=='__main__':


    # Define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_in", type=str, help="Specify the path to the pickle file containing paths to MIDIs")
    parser.add_argument("--dir_out", type=str, help="Specify the out dir path")
    args = parser.parse_args()

    constant_value = args.dir_out

    os.makedirs(constant_value)

    partial_merge_tracks = partial(merge_tracks, dir_out=constant_value)

    paths = pickle.load(open(args.dir_in, 'rb'))
    paths = [x for x in paths if x is not None]
    
    progress_map(partial_merge_tracks, paths, process_timeout=50, n_cpu=60)