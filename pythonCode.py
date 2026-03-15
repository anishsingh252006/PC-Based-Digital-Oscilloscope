import numpy as np
import serial
import sounddevice as sd
from scipy.fft import rfft, rfftfreq
from scipy.signal import butter, filtfilt, resample_poly
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

# ---------------- SETTINGS ----------------

SERIAL_PORT="COM4"
BAUD=2000000

ARDUINO_FS=76900
AUDIO_FS=44100
BUFFER=1024

frequency=100
amplitude=0.5
waveform="sine"
modulation="None"

generator_running=False
scope_running=True

phase=0

generated_wave=np.zeros(BUFFER)

ser=serial.Serial(SERIAL_PORT,BAUD,timeout=0)

# ---------------- GENERATOR ----------------

def base_wave(t):

    if waveform=="sine":
        return np.sin(2*np.pi*frequency*t)

    if waveform=="square":
        return np.sign(np.sin(2*np.pi*frequency*t))

    if waveform=="triangle":
        return 2*np.arcsin(np.sin(2*np.pi*frequency*t))/np.pi

    if waveform=="saw":
        return 2*(t*frequency-np.floor(0.5+t*frequency))
    

    if waveform=="noise":
        return np.random.randn(len(t))

    return np.zeros(len(t))


def apply_modulation(sig,t):

    if modulation=="AM":
        mod=0.5*np.sin(2*np.pi*50*t)
        return (1+mod)*sig

    if modulation=="FM":
        mod=50*np.sin(2*np.pi*50*t)
        phase_dev=np.cumsum(mod)/AUDIO_FS
        return np.sin(2*np.pi*frequency*t+phase_dev)

    if modulation=="PM":
        mod=np.sin(2*np.pi*50*t)
        return np.sin(2*np.pi*frequency*t+mod)

    if modulation=="ASK":
        mod=(np.sin(2*np.pi*20*t)>0).astype(float)
        return mod*np.sin(2*np.pi*frequency*t)

    if modulation=="FSK":
        f=frequency+200*(np.sin(2*np.pi*20*t)>0)
        return np.sin(2*np.pi*f*t)

    if modulation=="BPSK":
        mod=np.sign(np.sin(2*np.pi*20*t))
        return np.sin(2*np.pi*frequency*t)*mod

    return sig


def generate_wave(frames):

    global phase

    t=(np.arange(frames)+phase)/AUDIO_FS

    sig=base_wave(t)
    sig=apply_modulation(sig,t)

    phase+=frames

    return amplitude*sig


def audio_callback(outdata,frames,time,status):

    global generated_wave

    if not generator_running:
        outdata[:]=0
        return

    wave=generate_wave(frames)

    generated_wave=wave

    outdata[:]=wave.reshape(-1,1)


stream=sd.OutputStream(
    channels=1,
    callback=audio_callback,
    samplerate=AUDIO_FS,
    blocksize=BUFFER
)

# ---------------- GUI ----------------

app=QtWidgets.QApplication([])

win=pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle("Python Lab Instrument")

# Generated signal
gen_plot=win.addPlot(title="Generated Signal")
gen_curve=gen_plot.plot(pen='g')

win.nextRow()

# Observed signal
obs_plot=win.addPlot(title="Observed Signal")
obs_curve=obs_plot.plot(pen='y')

win.nextRow()

# Reconstructed signal
recon_plot=win.addPlot(title="Reconstructed Signal")
recon_curve=recon_plot.plot(pen='r')

# cursors
cursor1=pg.InfiniteLine(angle=90,movable=True,pen='c')
cursor2=pg.InfiniteLine(angle=90,movable=True,pen='c')

cursorV1=pg.InfiniteLine(angle=0,movable=True,pen='m')
cursorV2=pg.InfiniteLine(angle=0,movable=True,pen='m')

recon_plot.addItem(cursor1)
recon_plot.addItem(cursor2)
recon_plot.addItem(cursorV1)
recon_plot.addItem(cursorV2)

win.nextRow()

# FFT
fft_plot=win.addPlot(title="FFT Spectrum")
fft_curve=fft_plot.plot(pen='w')

win.nextRow()

# Waterfall
waterfall=pg.ImageItem()
waterfall_plot=win.addPlot(title="Waterfall Spectrogram")
waterfall_plot.addItem(waterfall)

cmap=pg.colormap.get('viridis')
waterfall.setLookupTable(cmap.getLookupTable())

spectrogram=np.zeros((400,BUFFER//2))

scope_buffer=np.zeros(BUFFER)

# ---------------- RECONSTRUCTION ----------------

def reconstruct(samples):

    samples=(samples-128)/128

    cutoff=5000/(ARDUINO_FS/2)

    b,a=butter(4,cutoff)

    samples=filtfilt(b,a,samples)

    resampled=resample_poly(samples,AUDIO_FS,ARDUINO_FS)

    return resampled[:BUFFER]

# ---------------- MEASURE ----------------

def measure(signal,fs):

    signal-=np.mean(signal)

    crossings=np.where(np.diff(np.sign(signal)))[0]

    if len(crossings)>2:
        periods=np.diff(crossings)
        freq=fs/(2*np.mean(periods))
    else:
        freq=0

    p2p=np.max(signal)-np.min(signal)
    rms=np.sqrt(np.mean(signal**2))

    return freq,p2p,rms

# ---------------- CONTROL PANEL ----------------

control=QtWidgets.QWidget()
layout=QtWidgets.QVBoxLayout()

freq_slider=QtWidgets.QSlider(QtCore.Qt.Horizontal)
freq_slider.setMinimum(1)
freq_slider.setMaximum(5000)
freq_slider.setValue(500)

amp_slider=QtWidgets.QSlider(QtCore.Qt.Horizontal)
amp_slider.setMinimum(1)
amp_slider.setMaximum(100)
amp_slider.setValue(50)

wave_select=QtWidgets.QComboBox()
wave_select.addItems(["sine","square","triangle","saw","noise"])

mod_select=QtWidgets.QComboBox()
mod_select.addItems(["None","AM","FM","PM","ASK","FSK","BPSK"])

start_btn=QtWidgets.QPushButton("Start Generator")
stop_btn=QtWidgets.QPushButton("Stop Generator")

pause_btn=QtWidgets.QPushButton("Run / Pause Scope")

# measurement box
measure_box=QtWidgets.QGroupBox("Measurements")
m_layout=QtWidgets.QVBoxLayout()

gen_f_label=QtWidgets.QLabel()
rec_f_label=QtWidgets.QLabel()
cursor_f_label=QtWidgets.QLabel()

p2p_label=QtWidgets.QLabel()
rms_label=QtWidgets.QLabel()

dt_label=QtWidgets.QLabel()
dv_label=QtWidgets.QLabel()

for w in [gen_f_label,rec_f_label,cursor_f_label,p2p_label,rms_label,dt_label,dv_label]:
    m_layout.addWidget(w)

measure_box.setLayout(m_layout)

layout.addWidget(freq_slider)
layout.addWidget(amp_slider)
layout.addWidget(wave_select)
layout.addWidget(mod_select)

layout.addWidget(start_btn)
layout.addWidget(stop_btn)

layout.addWidget(pause_btn)

layout.addWidget(measure_box)

control.setLayout(layout)
control.show()

# ---------------- CONTROL FUNCTIONS ----------------

def start_gen():
    global generator_running
    generator_running=True

def stop_gen():
    global generator_running
    generator_running=False

def toggle_scope():
    global scope_running
    scope_running=not scope_running

def set_freq(v):
    global frequency
    frequency=v

def set_amp(v):
    global amplitude
    amplitude=v/100

def set_wave(w):
    global waveform
    waveform=w

def set_mod(m):
    global modulation
    modulation=m

freq_slider.valueChanged.connect(set_freq)
amp_slider.valueChanged.connect(set_amp)
wave_select.currentTextChanged.connect(set_wave)
mod_select.currentTextChanged.connect(set_mod)

start_btn.clicked.connect(start_gen)
stop_btn.clicked.connect(stop_gen)

pause_btn.clicked.connect(toggle_scope)

# ---------------- UPDATE LOOP ----------------

def update():

    global spectrogram

    if not scope_running:
        return

    gen_curve.setData(generated_wave)

    data=ser.read(ser.in_waiting or 1)

    if len(data):

        samples=np.frombuffer(data,dtype=np.uint8)

        if len(samples)>BUFFER:
            samples=samples[-BUFFER:]

        n=len(samples)

        scope_buffer[:]=np.roll(scope_buffer,-n)
        scope_buffer[-n:]=samples

    signal=(scope_buffer-128)/128*4.5

    obs_curve.setData(signal)

    recon=reconstruct(scope_buffer)
    recon_curve.setData(recon)

    # -------- FFT (only changed part) --------

    fft_signal = generated_wave * np.hanning(len(generated_wave))

    spectrum = np.abs(rfft(fft_signal))
    freqs = rfftfreq(len(fft_signal), 1/AUDIO_FS)

    fft_curve.setData(freqs, spectrum)

    # -------- Waterfall --------

    spectrogram=np.roll(spectrogram,-1,axis=0)
    spectrogram[-1]=spectrum[:BUFFER//2]

    db=20*np.log10(spectrogram+1e-6)

    waterfall.setImage(db,levels=(-120,0))

    gen_f,_,_=measure(generated_wave,AUDIO_FS)
    rec_f,p2p,rms=measure(recon,AUDIO_FS)

    gen_f_label.setText(f"Generated Frequency: {gen_f:.2f} Hz")
    rec_f_label.setText(f"Reconstructed Frequency: {rec_f:.2f} Hz")

    p2p_label.setText(f"Vpp: {p2p:.2f} V")
    rms_label.setText(f"RMS: {rms:.2f} V")

    dt=abs(cursor1.value()-cursor2.value())/AUDIO_FS
    dv=abs(cursorV1.value()-cursorV2.value())

    dt_label.setText(f"Cursor Δt: {dt:.6f} s")
    dv_label.setText(f"Cursor ΔV: {dv:.3f} V")

    cursor_freq=1/dt if dt>0 else 0

    cursor_f_label.setText(f"Cursor Frequency: {cursor_freq:.2f} Hz")

timer=QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)

stream.start()

app.exec_()
