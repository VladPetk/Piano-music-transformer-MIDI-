from music21 import converter, meter, stream, key
import pickle
import os
import pickle

from parallelbar import progress_map
from functools import partial
import argparse

import warnings
warnings.simplefilter("ignore")

def transpose_midi(midi_file_path, out_dir):

    try:     
        # Load MIDI file
        midi_stream = converter.parse(midi_file_path)
    
        # Analyze key signature of the original MIDI file
        original_key = midi_stream.analyze('key')
        
        original_mode = original_key.mode  # Get the mode of the original key
    
        # Set the target key based on the mode of the original key
        if original_mode == 'major':
            new_key = key.Key('C')
        elif original_mode == 'minor':
            new_key = key.Key('a')
    
        # Calculate the interval to transpose
        interval = key.interval.Interval(original_key.tonic, new_key.tonic)
    
        # Transpose the entire stream
        transposed_stream = midi_stream.transpose(interval)
    
        base_midi = os.path.basename(midi_file_path)
        output_path = os.path.join(out_dir, base_midi)
    
        transposed_stream.write('midi', fp=output_path)
    except:
        pass

if __name__=='__main__':

    # Define arguments
    parser = argparse.ArgumentParser()
    #parser.add_argument("--dir_in", type=str, help="Specify the path to the pickle")
    parser.add_argument("--dir_out", type=str, help="Specify the out dir path")
    args = parser.parse_args()

    constant_value = args.dir_out

    partial_transpose_midi = partial(transpose_midi, out_dir=constant_value)

    file_path = 'good_paths.txt'

    with open(file_path, 'r') as file:
        # Read lines from the file and strip newline characters
        filez = [line.strip() for line in file.readlines()]


    filez_new = []
    for f in filez:
        base_midi = os.path.basename(f)
        if not os.path.exists(os.path.join(args.dir_out, base_midi)):
            filez_new.append(f)
    progress_map(partial_transpose_midi, filez_new, process_timeout=50, n_cpu=60)