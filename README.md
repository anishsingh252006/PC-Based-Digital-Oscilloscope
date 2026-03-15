# PC-Based Digital Oscilloscope and Signal Generator

A low-cost software-defined instrumentation system built using Arduino and Python.

This project converts a laptop into a **signal generator, oscilloscope, spectrum analyzer, and measurement instrument**.

## Features

- Real-time oscilloscope display
- Signal generator (sine, square, triangle, saw)
- Arbitrary waveform generation
- AM and FM modulation
- FFT spectrum analyzer
- XY oscilloscope mode
- Bode plot analyzer
- SCPI command interface

## Hardware Used

- Arduino Uno
- NE5532 operational amplifier
- Protection resistor and clamp diodes
- Virtual ground circuit
- USB connection to PC

## Software Stack

- Python
- NumPy
- PySerial
- Matplotlib
- PyQtGraph

## System Architecture

Signal Generator (Python)
↓
Laptop audio DAC
↓
Analog front-end circuit
↓
Arduino ADC sampling
↓
USB serial communication
↓
Python oscilloscope software

## Sampling Performance

- Sampling rate: ~77 kSamples/s
- Resolution: 10-bit
- Maximum measurable frequency: ~20 kHz

## Circuit

![Circuit](Circuit/schematic.png)

## Demo

![Oscilloscope](Images/oscilloscope_demo.png)

## How to Run

### Upload Arduino firmware

```
Arduino/fast_adc_sampling.ino
```

### Run Python software

```
python Python/instrument_suite.py
```

## Applications

- Audio signal analysis
- Electronics experimentation
- Educational DSP demonstrations
- Low-cost instrumentation

## Future Improvements

- Higher-speed ADC
- Multi-channel support
- STM32 upgrade
- GPU-based FFT

## License

MIT License
