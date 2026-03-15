# Python Lab Instrument

### DIY Software Oscilloscope + Signal Generator + Spectrum Analyzer

A Python-based virtual electronics laboratory instrument that combines a **signal generator, oscilloscope, FFT spectrum analyzer, and waterfall spectrogram** in a single GUI application.

The system generates signals through the **PC audio output**, samples them using **Arduino ADC**, and reconstructs the signal in Python for visualization and analysis.

This project demonstrates **digital signal processing, sampling theory, modulation techniques, and real-time signal reconstruction**.

---

# Features

## Signal Generator

The software generator can produce multiple waveforms in real time.

Supported waveforms

* Sine
* Square
* Triangle
* Sawtooth
* Noise

Adjustable parameters

* Frequency (1 – 5000 Hz)
* Amplitude
* Waveform selection

Signals are generated using Python and played through the **PC sound card**.

---

## Digital Modulation Support

The generator can simulate communication signals using modulation techniques.

Supported modulation

* AM (Amplitude Modulation)
* FM (Frequency Modulation)
* PM (Phase Modulation)
* ASK (Amplitude Shift Keying)
* FSK (Frequency Shift Keying)
* BPSK (Binary Phase Shift Keying)

This allows the instrument to demonstrate **basic digital communication systems**.

---

# Oscilloscope Section

The oscilloscope receives sampled data from an **Arduino ADC via serial communication** and displays

* Observed signal (sampled waveform)
* Reconstructed signal
* Generated reference signal

Sampling rate used

Arduino Sampling Rate ≈ 76.9 kHz

Signals are streamed over **high-speed serial communication (2 Mbps)**.

---

# Signal Reconstruction

The sampled signal is reconstructed using DSP techniques

1. Normalization
2. Butterworth Low Pass Filtering
3. Resampling
4. Signal interpolation

Libraries used

* scipy.signal.butter
* scipy.signal.filtfilt
* scipy.signal.resample_poly

This approximates the original analog waveform from sampled data.

---

# Spectrum Analyzer (FFT)

The system computes the **Fast Fourier Transform (FFT)** of the generated signal.

Features

* Real-time spectrum display
* Frequency component visualization
* Windowing using a **Hanning window**

Useful for

* Harmonic analysis
* Signal bandwidth measurement
* Modulation observation

---

# Waterfall Spectrogram

The application also displays a **waterfall spectrogram** showing frequency changes over time.

Benefits

* Time-frequency analysis
* Visualization of modulation effects
* Dynamic spectrum monitoring

---

# Measurement Tools

The instrument automatically calculates

* Generated frequency
* Reconstructed frequency
* Peak-to-Peak voltage
* RMS voltage

Cursor measurement tools

* Δt (time difference)
* ΔV (voltage difference)
* Frequency from cursor measurement

This mimics functionality of professional **Digital Storage Oscilloscopes (DSO)**.

---

# Graphical Interface

The GUI is built using

* PyQt5
* PyQtGraph

Displayed panels

1. Generated Signal
2. Observed Signal
3. Reconstructed Signal
4. FFT Spectrum
5. Waterfall Spectrogram

---

# Hardware Required

* Arduino Uno / compatible board
* PC or Laptop
* Audio cable (PC output to circuit)
* Signal conditioning circuit
* Op-amp amplifier (optional)
* Protection circuit (clamp diodes)

Optional components

* NE5532 amplifier
* Voltage divider
* Low pass filter

---

# Software Requirements

Install dependencies

pip install numpy scipy pyqt5 pyqtgraph sounddevice pyserial

---

# How It Works

1. Python generates a waveform
2. The waveform is played through the **PC audio output**
3. Arduino samples the signal using its **ADC**
4. Samples are sent to Python through **serial communication**
5. Python reconstructs the waveform using DSP
6. The GUI displays the signals and spectrum

---

# Educational Value

This project demonstrates concepts from

* Digital Signal Processing
* Sampling Theory
* Signal Reconstruction
* Communication Systems
* Fourier Analysis
* Embedded Systems

It can act as a **low-cost virtual electronics lab**.

---

# Future Improvements

Possible upgrades

* Trigger modes
* Automatic scaling
* Bode plot analyzer
* Logic analyzer mode
* Network signal streaming
* Higher sampling hardware (ESP32)

---

# Author

Developed as an **electronics and signal processing project** demonstrating how software and low-cost hardware can emulate laboratory instruments.
