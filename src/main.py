import random
import numpy as np
import pandas as pd
from midiutil import MIDIFile
from scipy.signal import savgol_filter

# a0 = 21
# c8 = 108

# Cria um novo arquivo MIDI com 1 trilha
midi = MIDIFile(1)  # O número é a quantidade de trilhas

# Adiciona informações básicas
track = 0
time = 0
midi.addTrackName(track, time, "Minha Música")
midi.addTempo(track, time, 120)  # 120 BPM

# Adiciona notas
channel = 0
volume = 100
duration = 1  # Em beats

def extract_ndvi_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    ndvi_values = df['NDVI'].to_numpy()
    return ndvi_values
    # ndvi_savgol_result = savgol_filter(ndvi_values, 5, 2, deriv=1) 
    # return ndvi_savgol_result

def extract_ndvi_from_csv_savgol(csv_path):
    df = pd.read_csv(csv_path)
    ndvi_values = df['NDVI'].to_numpy()
    ndvi_savgol_result = savgol_filter(ndvi_values, 5, 2, deriv=1) 
    return ndvi_savgol_result

def ndvi_to_major_chord(ndvi_value):
    # Normaliza o NDVI de [-1, 1] para [0, 1]
    normalized = (ndvi_value + 1) / 2
    root_index = np.round(normalized * (108 - 21) + 21).astype(int)
    chord_size = random.choice([3, 4])
    if chord_size == 3:
        # Intervalos de tríade maior: fundamental, terça maior, quinta justa
        major_chord = np.array([root_index, root_index + 4, root_index + 7])
    else:
        # Intervalos de tétrade maior: fundamental, terça maior, quinta justa, sétima maior
        major_chord = np.array([root_index, root_index + 4, root_index + 7, root_index + 11])
    # Verifica se algum valor do acorde é maior ou igual a 88 (maior que a capacidade de um piano padrão)
    if np.any(major_chord >= 88):
        # Encontrar o valor mínimo no array
        valor_minimo = np.min(major_chord)
        # Criar novo array com todos valores iguais ao mínimo
        major_chord = np.full_like(major_chord, valor_minimo)
        return list(major_chord)
    else:
        return list(major_chord)

if __name__ == "__main__":
    # Extraindo valores NDVI do CSV sem Savgol
    ndvi_values = extract_ndvi_from_csv("/Users/eduardolacerda/code/ndvi2midi/data/NDVI_Tijuca_v2.csv")
    
    for ndvi in ndvi_values:
        chord = ndvi_to_major_chord(ndvi)
        print(f"NDVI {ndvi} -> Chord MIDI notes: {chord}")
        # Adiciona o acorde ao MIDI
        for note in chord:
            midi.addNote(track, channel, note, time, duration, volume)
        time += duration
    # Adiciona acordes baseados nos valores NDVI
    for i, ndvi_value in enumerate(ndvi_values):
        chord = ndvi_to_major_chord(ndvi_value)
        for note in chord:
            midi.addNote(track, channel, note, time + i, duration, volume)
            
    # Salva o arquivo MIDI atualizado
    with open("/Users/eduardolacerda/code/ndvi2midi/midi_files/minha_musica_com_acordes_tijuca_savgol_v2.mid", "wb") as output_file:
        midi.writeFile(output_file)
