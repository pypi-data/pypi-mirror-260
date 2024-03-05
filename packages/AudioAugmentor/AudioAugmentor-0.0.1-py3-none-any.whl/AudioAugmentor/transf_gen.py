"""
File containing functions that generate transformations from the user input

@author: Ladislav Vašina, github: LadislavVasina1
"""

import torch
import torchaudio
import torchaudio.transforms as T
import torchaudio.io as TIO
import os
from IPython.display import Audio, display
import torch_audiomentations as TA
import audiomentations as AA
import soundfile as sf
import pyroomacoustics as pra
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import fftconvolve
import torch.multiprocessing as mp

# Build pip package with this uncommented
from . import torchaudio_transf_wrapper as TTW
from .rir_setup import ApplyRIR, get_all_materials_info

# Test source with this uncommented
# import torchaudio_transf_wrapper as TTW
# from rir_setup import ApplyRIR, get_all_materials_info

transformations = []

PRA_TRANSF = [
    'ApplyRIR'
]

TTW_TRANSF = [
    'pitchshift',
    'speed',
    'vol',
    'frequencymasking',
    'timemasking',
    'spectrogram',
    'melspectrogram',
]

# MelSpectrogram, Spectrogram, TimeMasking, FrequencyMasking augmentations
# should be used as last augmentation method
T_TRANSF = [
    'PitchShift',
    'Speed',
    'Vol',
    'FrequencyMasking',
    'TimeMasking',
    'Spectrogram',
    'MelSpectrogram',
]

TA_TRANSF = [
    'AddColoredNoise',
    'AddBackgroundNoise',
    'BandPassFilter',
    'BandStopFilter',
    'HighPassFilter',
    'ApplyImpulseResponse',
    'LowPassFilter',
    'PeakNormalization',
    'PolarityInversion',
    'Shift',
    'TimeInversion',
]

AA_TRANSF = [
    'AddGaussianNoise',
    'AddShortNoises',
    'AdjustDuration',
    'AirAbsorption',
    'ClippingDistortion',
    'Gain',
    'GainTransition',
    'HighShelfFilter',
    'Limiter',
    'LoudnessNormalization',
    'LowShelfFilter',
    'Mp3Compression',
    'Normalize',
    'Padding',
    'PeakingFilter',
    'SevenBandParametricEQ',
    'TanhDistortion',
    'TimeStretch',
]

# Codecs should be used as last augmentation method.
# Only exception is using SpecAugment, in that cas SpecAugment should be used as last method.
CODECS = [
    "ac3",              # torchaudio
    "adpcm_ima_wav",    # ---| |----
    "adpcm_ms",         # ---| |----
    "adpcm_yamaha",     # ---| |----
    "eac3",             # ---| |----
    "flac",             # ---| |----
    "libmp3lame",       # ---| |----
    "mp2",              # ---| |----
    "pcm_alaw",         # ---| |----
    "pcm_f32le",        # ---| |----
    "pcm_f64le",        # ---| |----
    "pcm_mulaw",        # ---| |----
    "pcm_s16le",        # ---| |----
    "pcm_s24le",        # ---| |----
    "pcm_s32le",        # ---| |----
    "pcm_u8",           # ---| |----
    "wmav1",            # ---| |----
    "wmav2",            # torchaudio
    'g726',             # ffmpeg - supported bitrates 16k, 24k, 32k, 40k
    'gsm',              # ffmpeg - GSM-FR = 13k bitrate
    'amr',              # ffmpeg - supported bitrates 4.75k, 5.15k, 5.90k, 6.70k, 7.40k, 7.95k, 10.20k, 12.20k
]


CODECS_AFFECTORS_LIST = []

for codec in CODECS:
    globals()[f"{codec}_effector"] = TIO.AudioEffector(
        format="wav", encoder=codec)
    CODECS_AFFECTORS_LIST.append(globals()[f"{codec}_effector"])


def verbose_out(key, value, transf_list):
    print(f'ADDED: {get_transf(key, transf_list)}, \n\t\t{value}\n')


def get_transf(user_input, list_of_transformations):
    '''
    Args:
        user_input: user input
        list_of_transformations: list of transformations
    Returns:
        specific transformation from the list of available transformations listed above
        or None if the transformation is not in the list

    This function takes user input and returns the name of the transformation.
    It can handle user input in any case (for better UX) and returns the name of the transformation.
    '''
    user_input_lower = user_input.lower()
    for item in list_of_transformations:
        if item.lower() == user_input_lower:
            return item
    return None


def transf_gen(verbose=False, **kwargs):
    '''
    Args:
        kwargs: dictionary containing transformation with its arguments

    Returns: transfoarmations chain (list)
    '''
    pass

    for key, value in kwargs.items():
        # Handle string input of the transformation parameters
        if type(value) is str:
            value = eval('dict(' + value + ')')

        # Check the type of the current transformation from the user
        pra_flag = get_transf(key, PRA_TRANSF) in PRA_TRANSF
        t_flag = get_transf(key, T_TRANSF) in T_TRANSF
        ta_flag = get_transf(key, TA_TRANSF) in TA_TRANSF
        aa_flag = get_transf(key, AA_TRANSF) in AA_TRANSF
        codec_flag = get_transf(key, CODECS) in CODECS

        # Handle list input of the transformation parameters
        match key:
            # Handle transformations from PYROOMACOUSTICS
            case key if pra_flag:
                transformations.append(
                    eval(get_transf(key, PRA_TRANSF))(**value)
                )
                verbose_out(key, value, PRA_TRANSF) if verbose else None

            # Handle transformations from TORCH_AUDIOMENTATIONS
            case key if ta_flag:
                transformations.append(
                    getattr(TA, get_transf(key, TA_TRANSF))(**value)
                )
                verbose_out(key, value, TA_TRANSF) if verbose else None

            # Handle transformations from AUDIOMENTATIONS
            case key if aa_flag:
                transformations.append(
                    getattr(AA, get_transf(key, AA_TRANSF))(**value)
                )
                verbose_out(key, value, AA_TRANSF) if verbose else None

            # Handle transformations from TORCHAUDIO
            case key if t_flag:
                # print(get_transf(key, TTW_TRANSF))
                # check if values contain "p" key
                if 'p' in value.keys():
                    # save the p value and delete it from value dictionary
                    p = value['p']
                    del value['p']
                    transformations.append(
                        # core.torch_randomizer(
                        #     getattr(TTW, get_transf(key, TTW_TRANSF))(**value),
                        #     p=p
                        # )
                        {get_transf(key, TTW_TRANSF): {**value}, 'p': p}
                    )

                elif 'p' not in value.keys():
                    transformations.append(
                        getattr(T, get_transf(key, T_TRANSF))(**value)
                    )

                verbose_out(key, value, T_TRANSF) if verbose else None

            # Handle codecs
            case key if codec_flag:
                if key != 'g726' and key != 'gsm' and key != 'amr':
                    transformations.append(
                        CODECS_AFFECTORS_LIST[CODECS.index(key)]
                    )
                else:
                    if key == 'g726':
                        # Check if the bitrate is correct
                        correct_g726_bitrates = ['16k', '24k', '32k', '40k']
                        if value['audio_bitrate'] not in correct_g726_bitrates:
                            raise ValueError(
                                f'''!!!INVALID BITRATE FOR G726: {value["audio_bitrate"]}!!!\n
                                Bitrate must be one of: 16k, 24k, 32k, 40k'''
                            )
                    elif key == 'amr':
                        # Check if the bitrate is correct
                        correct_amr_bitrates = ['4.75k', '5.15k', '5.90k', '6.70k', '7.40k', '7.95k', '10.20k', '12.20k']
                        if value['audio_bitrate'] not in correct_amr_bitrates:
                            raise ValueError(
                                f'''!!!INVALID BITRATE FOR AMR: {value["audio_bitrate"]}!!!\n
                                Bitrate must be one of: 4.75k, 5.15k, 5.90k, 6.70k, 7.40k, 7.95k, 10.20k, 12.20k'''
                            )
                        
                    transformations.append((key, value))

                verbose_out(key, value, CODECS) if verbose else None

            # Handle unknown transformation
            case _:
                raise ValueError(f'!!!UNKNOWN TRANSFORMATION: {key} !!!')
    # Verbose out
    print(
        f'\n\nFINAL TRANSFORMATIONS LIST:\n' + '\n'.join(str(transformation) for transformation in transformations)
    ) if verbose else None 

    return transformations


# rir_kwargs = {
#     'audio_sample_rate': 16000,
#     'corners_coord': [[0, 0], [0, 3], [5, 3], [5, 1], [3, 1], [3, 0]],
#     'walls_mat': 'curtains_cotton_0.5',
#     'room_height': 2.0,
#     'max_order': 3,
#     'floor_mat': 'carpet_cotton',
#     'ceiling_mat': 'hard_surface',
#     'ray_tracing': True,
#     'air_absorption': True,
#     'source_coord': [[1.0], [1.0], [0.5]],
#     'microphones_coord': [[3.5], [2.0], [0.5]],
# }
# transformations = transf_gen(verbose=True,
#            ApplyRIR=rir_kwargs,
#            Vol={'gain': [0.9, 1.5, 0.1],
#                 'p': 0.9},
#            PitchShift={'sample_rate': 16000,
#                        'n_steps': [-1, 1, 0.1],
#                        'p': 0.9},
#            Speed={'orig_freq': 16000,
#                   'factor': [0.9, 1.1, 0.1],
#                   'p': 0.9},
#            speed='orig_freq=16000, factor=0.9',
#            Mp3Compression={'min_bitrate': 8,
#                            'max_bitrate': 64,
#                            'backend': 'pydub',
#                            'p': 1},
#            #    TimeInversion='p=1, sample_rate=16000',
#            #    TimeMasking='time_mask_param=80',
#            #    FrequencyMasking='freq_mask_param=80',
#            TimeInversion={'p': 1, 'sample_rate': 16000},
#            pcm_alaw=True,
#            MelSpectrogram={'sample_rate': 16000},
#            TimeMasking={'time_mask_param': 80},
#            FrequencyMasking={'freq_mask_param': 80},
#            g726={'audio_bitrate': '40k'},
#            gsm=True,
#            )