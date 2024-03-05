# AudioAugmentor
### Python library for augmenting audio data
This library is designed to augment audio data for machine learning purposes. 
It combines several tools and libraries for audio data augmentation and provides unified interface which can be used to apply large set of audio augmentations in one place.

The library is designed to be used with the [PyTorch](https://pytorch.org) machine learning framework.
It can also work solely on just simple audio waveforms and augment those.

This library specifically combines theese libraries and tools:

- [torchaudio](https://pytorch.org/audio/stable/index.html)
- [audiomentations](https://github.com/iver56/audiomentations)
- [torch-audiomentations](https://github.com/asteroid-team/torch-audiomentations)
- [pyroomacoustics](https://github.com/LCAV/pyroomacoustics)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)



Table below shows which library was used to apply specific audio augmentation/codec.

|                                  | audiomentations | torch-audiomentations | torchaudio | pyroomacoustics | ffmpeg |
|----------------------------------|:---------------:|:---------------------:|:----------:|:---------------:|:------:|
| AddBackgroundNoise               |                 |           ✅          |            |                 |        |
| AddColoredNoise / AddGaussianSNR |                 |           ✅          |            |                 |        |
| AddGaussianNoise                 |        ✅       |                       |            |                 |        |
| AddShortNoises                   |        ✅       |                       |            |                 |        |
| AdjustDuration                   |        ✅       |                       |            |                 |        |
| AirAbsorption                    |        ✅       |                       |            |                 |        |
| ApplyImpulseResponse             |                 |           ✅          |            |                 |        |
| BandPassFilter                   |                 |           ✅          |            |                 |        |
| BandStopFilter                   |                 |           ✅          |            |                 |        |
| ClippingDistortion               |        ✅       |                       |            |                 |        |
| Volume / Gain                    |                 |                       |     ✅     |                 |        |
| GainTransition                   |        ✅       |                       |            |                 |        |
| HighPassFilter                   |                 |           ✅          |            |                 |        |
| HighShelfFilter                  |        ✅       |                       |            |                 |        |
| Lambda                           |                 |                       |            |                 |        |
| Limiter                          |        ✅       |                       |            |                 |        |
| LoudnessNormalization            |        ✅       |                       |            |                 |        |
| LowPassFilter                    |                 |           ✅          |            |                 |        |
| LowShelfFilter                   |        ✅       |                       |            |                 |        |
| Mp3Compression                   |        ✅       |                       |            |                 |        |
| Normalize                        |        ✅       |                       |            |                 |        |
| Padding                          |        ✅       |                       |            |                 |        |
| PeakNormalization                |                 |           ✅          |            |                 |        |
| PeakingFilter                    |        ✅       |                       |            |                 |        |
| PitchShift                       |                 |                       |     ✅     |                 |        |
| PolarityInversion                |                 |           ✅          |            |                 |        |
| RepeatPart                       |                 |                       |            |                 |        |
| Resample                         |                 |                       |            |                 |        |
| Time inversion / Reverse         |                 |           ✅          |            |                 |        |
| RoomSimulator                    |                 |                       |            |        ✅       |        |
| SevenBandParametricEQ            |       ✅        |                       |            |                 |        |
| Shift                            |                 |           ✅          |            |                 |        |
| Speed                            |                 |                       |     ✅     |                 |        |
| SpecChannelShuffle               |                 |                       |            |                 |        |
| SpecFrequencyMask                |                 |                       |     ✅     |                 |        |
| TanhDistortion                   |       ✅        |                       |            |                 |        |
| TimeMask                         |                 |                       |     ✅     |                 |        |
| TimeStretch                      |                 |                       |            |                 |        |
| Trim                             |                 |                       |            |                 |        |
| ac3                              |                 |                       |     ✅     |                 |        |
| adpcm_ima_wav                    |                 |                       |     ✅     |                 |        |
| adpcm_ms                         |                 |                       |     ✅     |                 |        |
| adpcm_yamaha                     |                 |                       |     ✅     |                 |        |
| eac3                             |                 |                       |     ✅     |                 |        |
| flac                             |                 |                       |     ✅     |                 |        |
| libmp3lame                       |                 |                       |     ✅     |                 |        |
| mp2                              |                 |                       |     ✅     |                 |        |
| pcm_alaw                         |                 |                       |     ✅     |                 |        |
| pcm_f32le                        |                 |                       |     ✅     |                 |        |
| pcm_mulaw                        |                 |                       |     ✅     |                 |        |
| pcm_s16le                        |                 |                       |     ✅     |                 |        |
| pcm_s24le                        |                 |                       |     ✅     |                 |        |
| pcm_s32le                        |                 |                       |     ✅     |                 |        |
| pcm_u8                           |                 |                       |     ✅     |                 |        |
| wmav1                            |                 |                       |     ✅     |                 |        |
| wmav2                            |                 |                       |     ✅     |                 |        |
| g726                             |                 |                       |            |                 |   ✅   |
| gsm                              |                 |                       |            |                 |   ✅   |
| amr                              |                 |                       |            |                 |   ✅   |
|                                  |                 |                       |            |                 |        |
|                                  |                 |                       |            |                 |        |
|                                  |                 |                       |            |                 |        |
|                                  |                 |                       |            |                 |        |
|                                  |                 |                       |            |                 |        |
|                                  |                 |                       |            |                 |        |
|                                  |                 |                       |            |                 |        |
|                                  |                 |                       |            |                 |        |
|                                  |                 |                       |            |                 |        |
|                                  |                 |                       |            |                 |        |
