"""
File containg class that handles generating room impulse responses (RIRs) and applying them to the data.

@author: Ladislav Vašina, github: LadislavVasina1
"""


import pyroomacoustics as pra
import torch
import audiomentations as AA
import torchaudio.transforms as T
import numpy as np

def get_all_materials_info():
    '''
    This function prints available absorption and scattering materials
    that are available through the pyroomacoustics library.

    For more details see:
    https://pyroomacoustics.readthedocs.io/en/pypi-release/pyroomacoustics.materials.database.html
    '''
    
    x = pra.materials_data
    center_freqs = x['center_freqs']
    absorption = x['absorption']
    scattering = x['scattering']

    print('@'*79)
    print('CENTER FREQUENCIES:')
    print(f'{center_freqs}')
    print('@'*79)
    print('ABSORPTION:')
    for item in absorption.items():
        key, value = item
        print(f'\t{key}:')

        for key, value in value.items():
            print(f'\t\t{key}: {value}')

    print('@'*79)
    print('SCATTERING:')
    for item in scattering.items():
        key, value = item
        print(f'\t{key}:')

        for key, value in value.items():
            print(f'\t\t{key}: {value}')
    print('@'*79)

# TODO raytracing parametrization, extend all functions according to the documentation
class ApplyRIR:
    def __init__(
        self,
        audio_sample_rate=None,
        corners_coord=None,
        walls_mat=None,
        room_height=None,
        floor_mat=None,
        ceiling_mat=None,
        max_order=None,
        ray_tracing=None,
        air_absorption=None,
        source_coord=None,
        microphones_coord=None,
    ):
        self.audio_sample_rate = audio_sample_rate
        self.core_sample_rate = 16000
        # coordinates going clockwise around the room [[x1, y2], [x2, y2], ...]
        self.corners_coord = np.array(corners_coord).T
        self.walls_mat = walls_mat
        # Height in meters
        self.room_height = room_height
        self.floor_mat = floor_mat
        self.ceiling_mat = ceiling_mat
        # using lower max_order value will result in a quick (but less accurate) RIR
        self.max_order = max_order
        self.ray_tracing = ray_tracing
        self.air_absorption = air_absorption
        # All coordintes must be in form [[x], [y], [z]] or [[x1, x2, ...], [y1, y2, ...], [z1, z2, ...]]
        self.source_coord = source_coord
        self.microphones_coord = microphones_coord

    def __call__(self, waveform):
        # print(f'INITIAL DEVICE: {waveform.device}')
        # Handle device and if waveform is in the form of torch.Tensor convert it to NumPy format
        if isinstance(waveform, torch.Tensor):
            initial_wav_type = waveform.dtype
            initial_device = waveform.device
            if waveform.is_cuda:
                waveform = waveform.squeeze(0).squeeze(0).cpu()
            elif waveform.is_cpu:
                waveform = waveform.squeeze(0).squeeze(0)

        elif isinstance(waveform, np.ndarray):
            initial_wav_type = waveform.dtype

        if not (self.audio_sample_rate == self.core_sample_rate):
            if isinstance(waveform, torch.Tensor):
                waveform = T.Resample(self.audio_sample_rate,
                                    self.core_sample_rate)(waveform)
            else:
                waveform = AA.Resample(min_sample_rate=self.core_sample_rate, max_sample_rate=self.core_sample_rate, p=1.0)(waveform)

        room = pra.Room.from_corners(
            self.corners_coord,
            fs=self.core_sample_rate,
            max_order=self.max_order,
            materials=pra.Material(self.walls_mat),
            ray_tracing=self.ray_tracing,
            air_absorption=self.air_absorption,
        )

        floor_and_ceiling = pra.make_materials(
            ceiling=self.ceiling_mat,
            floor=self.floor_mat
        )
        room.extrude(
            self.room_height,
            materials=floor_and_ceiling
        )

        if self.ray_tracing:
            # set the ray tracing parameters
            room.set_ray_tracing(
                n_rays=10000,
                receiver_radius=0.5,
                energy_thres=1e-5
            )

        # add source and set the signal to WAV file content
        room.add_source(
            self.source_coord,
            signal=waveform.numpy() if isinstance(waveform, torch.Tensor) else waveform,
        )

        # add microphone/s
        R = np.array(self.microphones_coord)  # [[x], [y], [z]]
        room.add_microphone(R)

        # compute image sources
        room.image_source_model()

        # visualize 3D polyhedron room and image sources
        # fig, ax = room.plot(img_order=1)
        # fig.set_size_inches(5, 3)

        room.simulate()
        waveform = room.mic_array.signals[0, :]
        del(room)
        waveform = waveform.astype(np.float32)


        if initial_wav_type == torch.Tensor:
            waveform = torch.from_numpy(waveform)
            # waveform = T.Resample(self.core_sample_rate,
            #                       self.audio_sample_rate)(waveform)
            waveform = waveform.unsqueeze(0).unsqueeze(0).to(initial_device)

        # print(f'FINAL SHAPE: {waveform.shape}')
        # print(f'FINAL TYPE: {type(waveform)}')
        return waveform
