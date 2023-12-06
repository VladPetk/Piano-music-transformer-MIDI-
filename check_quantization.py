import miditoolkit
import mido
import os
import pickle
from parallelbar import progress_map

from functools import partial

import argparse


def get_bar_positions_h(midi):

    try:
        
        time_division = midi.ticks_per_beat
        time_sigs = midi.time_signature_changes
        
        sig_change_ts = [x.time for x in time_sigs]
        sig_change_ts.append(midi.max_tick) #add end of MIDI
        sig_change_ts = sig_change_ts[1:] # start from second element as first one is 0 (not a change)
        
        bars = [0] # add first bar
        last_bar = 0
        last_bar_t = 0
        bar_lengths = []
        for i, time_sig in enumerate(time_sigs):
            bar_length = int(time_division * 4 * time_sig.numerator / time_sig.denominator) #miditok
            bar_count = int((sig_change_ts[i] - last_bar_t) / bar_length) # how many bars fit before the signature changes
            bars.extend([last_bar_t + i * bar_length for i in range(bar_count+1)][1:]) # based on the count of bars create a range of step bar_length
            bar_lengths.extend([bar_length]*bar_count)
            last_bar_t = sig_change_ts[i] # change time of last bar
        
        return bars, bar_lengths
    except:
        return None

def bar_quant_score_p(midi_file, return_array = False, standardize = True):
    try:
        midi = miditoolkit.MidiFile(midi_file)
    
        bars, bar_lengths = get_bar_positions_h(midi)
        bar_lengths.insert(1, bar_lengths[0])
        
        errors = []
        for bar, bar_length in zip(bars, bar_lengths):
            closest_note = min(midi.instruments[0].notes, key=lambda note: (abs(note.start - bar), -note.pitch))
            error = abs(closest_note.start - bar)
            if error >= bar_length/2:
                continue
            if error <= 1:
                error = 0
            errors.append(error)
        
        if return_array:
            return errors
        else:
            if standardize:
                zero_count = errors.count(0)
                return zero_count/len(errors)
            else:
                return (sum(errors[:-1])/len(errors[:-1]))
    except:
        return None

def get_quant_paths(midi_file, threshold = 0.5):
    try:
        threshold = bar_quant_score_p(midi_file)
        if threshold > 0.5:
            with open('good_paths.txt', 'a') as file:
                file.write(f"{midi_file}\n")
            return midi_file
    except:
        return None

if __name__=='__main__':

    # Define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_in", type=str, help="Specify the path of the input directory")
    parser.add_argument("--threshold", type=float, help="Please specify the threshold value (0-1); higher = stricter; default = 0.5")
    args = parser.parse_args()

    partial_get_quant_paths = partial(get_quant_paths, threshold = args.threshold)

    filez_path = args.dir_in
    filez = list()
    for (dirpath, dirnames, filenames) in os.walk(filez_path):
        filez += [os.path.join(dirpath, file) for file in filenames if file.lower().endswith((".mid", ".midi"))]
    
    res = progress_map(partial_get_quant_paths, filez, process_timeout=50, n_cpu=60)
    res = [x for x in res if x is not None]
    pickle.dump(res, open("paths_quantized.p", "wb"))