import random
import numpy as np
import pandas as pd
from midiutil import MIDIFile

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

# Adiciona uma escala C maior
ndvi_values = extract_ndvi_from_csv("/Users/eduardolacerda/Downloads/ndvi_sorriso_2020_2023_ponto1.csv")

def ndvi_to_major_chord(ndvi_value):
    """
    Transforma um valor NDVI em um acorde maior (tríade) baseado na escala maior.
    Retorna uma lista de valores de notas MIDI.
    """ 
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
    
for ndvi in ndvi_values:
    chord = ndvi_to_major_chord(ndvi)
    # print(f"NDVI {ndvi} -> Chord MIDI notes: {chord}")
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
with open("minha_musica_com_acordes.mid", "wb") as output_file:
    midi.writeFile(output_file)
    
# Exemplo de uso para apenas uma nota baseada no NDVI:
# normalized = (ndvi_values + 1) / 2
# notes = np.round(normalized * (108 - 21) + 21).astype(int)
# duration = 1  # Em beats
# for i, pitch in enumerate(notes):
#     midi.addNote(track, channel, pitch, time + i, duration, volume)
# with open("minha_musica.mid", "wb") as output_file:
#     midi.writeFile(output_file)