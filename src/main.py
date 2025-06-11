import random
import numpy as np
import pandas as pd
from midiutil import MIDIFile
from scipy.signal import savgol_filter

# a0 = 21
# c8 = 108

def extract_ndvi_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    ndvi_values = df['NDVI'].to_numpy()
    return ndvi_values

def extract_ndvi_from_csv_savgol(csv_path):
    df = pd.read_csv(csv_path)
    ndvi_values = df['NDVI'].to_numpy()
    ndvi_savgol_result = savgol_filter(ndvi_values, 5, 2, deriv=1) 
    return ndvi_savgol_result

def ndvi_to_major_chord(ndvi_value):
    # Normalize the NDVI from [-1, 1] to [0, 1]
    normalized = (ndvi_value + 1) / 2
    root_index = np.round(normalized * (108 - 21) + 21).astype(int)
    chord_size = random.choice([3, 4])
    if chord_size == 3:
        # Intervals for a major chord
        major_chord = np.array([root_index, root_index + 4, root_index + 7])
    else:
        # Intervals for a major seventh chord
        major_chord = np.array([root_index, root_index + 4, root_index + 7, root_index + 11])
    # Verify if any value in the chord is greater than or equal to 88 (greater than the capacity of a standard piano)
    if np.any(major_chord >= 88):
        # Find the minimum value in the array
        valor_minimo = np.min(major_chord)
        # Create a new array with all values equal to the minimum
        major_chord = np.full_like(major_chord, valor_minimo)
        return list(major_chord)
    else:
        return list(major_chord)
    
def create_midi(ndvi_values, midi_name = "Minha Música", number_of_tracks = 1, tempo = 120, output_file_path = "output.mid"):

    # Creates a new MIDI file with X number of track
    midi = MIDIFile(number_of_tracks)

    track = 0
    time = 0
    midi.addTrackName(track, time, midi_name)
    midi.addTempo(track, time, tempo)

    # Add note parameters
    channel = 0
    volume = 100
    duration = 1  # Em beats
    
    for ndvi in ndvi_values:
        chord = ndvi_to_major_chord(ndvi)
        print(f"NDVI {ndvi} -> Chord MIDI notes: {chord}")
        
    # Add chords to the MIDI file
    for note in chord:
        midi.addNote(track, channel, note, time, duration, volume)
    time += duration
    
    # Add chords based on NDVI values
    for i, ndvi_value in enumerate(ndvi_values):
        chord = ndvi_to_major_chord(ndvi_value)
        
    for note in chord:
        midi.addNote(track, channel, note, time + i, duration, volume)
            
    # Save the MIDI file
    with open(output_file_path, "wb") as output_file:
        midi.writeFile(output_file)

if __name__ == "__main__":
    # Extracting NDVI values from CSV with Savgol filter
    ndvi_values = extract_ndvi_from_csv("/Users/eduardolacerda/code/ndvi2midi/data/NDVI_Tijuca_v2.csv")
    # Creating MIDI file with the extracted NDVI values
    create_midi(ndvi_values, 
                midi_name="Minha Música Tijuca", 
                number_of_tracks=1,
                tempo=120, 
                output_file_path="/Users/eduardolacerda/code/ndvi2midi/midi_files/minha_musica_com_acordes_tijuca_savgol_v2.mid")

