import matplotlib.pyplot as plt
import numpy as np 
import scipy.signal as scsp
import scipy.io.wavfile as scio

from matplotlib import ticker
from scipy.fftpack import fftshift

MKFUNC = (
    lambda x, pos: '%1.1fM' % (x * 1e-6)
    if x >= 1e6 else '%1.1fk'
    % (x * 1e-3) if x >= 1e3 else '%1.1f'
    % x
    % (x * 1e3) if x >= 1e-3 else '%1.1fm'
    % (x * 1e6) if x >= 1e-6 else '%1.1fµ'
    % (x * 1e9) if x >= 1e-9 else '%1.1fn'
    % (x * 1e12) if x >= 1e-12 else '%1.1fp'
    % x
) # Function to plot x- and y-axis with k for kilo and M for Mega

def plot_time(t, data, fig=None, ax=None, interactive_on=False, **line_kwargs):
    if interactive_on:
        plt.ion()
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = plt.gca()
    ax.plot(t, data, **line_kwargs)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude')  
    ax.grid(True, which='both')
    if 'label' in line_kwargs:
        ax.legend()
    # plt.show(block=False)
    return fig, ax,

def plot_rfft_freq(
        f,
        data,
        xscale='lin',
        yscale='lin',
        fig=None,
        ax=None,
        interactive_on=False,
        **line_kwargs,
):
    mkformatter = ticker.FuncFormatter(MKFUNC)
    if interactive_on:
        plt.ion()
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = plt.gca()
        
    if xscale == 'lin' and yscale == 'lin':
        ax.plot(f, data, **line_kwargs)
    if xscale == 'log' and yscale == 'lin':
        ax.semilogx(f, data, **line_kwargs)
        ax.xaxis.set_major_formatter(mkformatter)
    if xscale == 'lin' and yscale == 'log':
        ax.semilogy(f, data, **line_kwargs)
        ax.yaxis.set_major_formatter(mkformatter)
    if xscale == 'log' and yscale == 'log':
        ax.loglog(f, data, **line_kwargs)
        ax.xaxis.set_major_formatter(mkformatter)
        ax.yaxis.set_major_formatter(mkformatter)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude')  
    ax.grid(True, which='both')
    ax.legend()
    # plt.show(block=False)
    return fig, ax,

def get_rfft_power_spec(x, fs, Nfft=None):
    if Nfft is None:
        Nfft = len(x)
    freq = np.arange(Nfft/2+1)/(Nfft/2+1)*fs/2
    Sxx = np.abs(np.fft.rfft(x, Nfft) / Nfft)**2
    return freq, Sxx

def plot_h_full(freq_h, freq_msc, magnitude, phase_deg, msc,):
    plt.figure()
    plt.subplot(311)
    ax0 = plt.gca()
    ax0.set_title('Transfer Function Mic2/Mic1')
    ax0.plot(freq_h, magnitude)
    ax0.grid(which='both')
    ax0.set_ylabel('Magnitude [dB]')
    plt.subplot(312, sharex=ax0)
    ax1 = plt.gca()
    ax1.plot(freq_h, phase_deg,)
    ax1.set_ylabel('Phase [Deg]')
    ax1.grid(which='both')
    plt.subplot(313, sharex=ax0)
    ax2 = plt.gca()
    ax2.plot(freq_msc, msc,)
    ax2.set_ylabel('MSC')
    ax2.grid(which='both')
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylim([.5, 1.2])
    _ = plt.setp(ax0.get_xticklabels(), visible=False)
    _ = plt.setp(ax1.get_xticklabels(), visible=False)
    pass

def get_ir_from_rfft(freq, cplx_data_spec, fs, nfft):
    centered_ir = fs*fftshift(np.fft.irfft(cplx_data_spec))
    t = np.arange(-int(nfft/2),int(nfft/2))/nfft
    return t, centered_ir

def get_ir_from_rawdata(t, x, y, fs, nfft):
    print('To be implemented.')
    return

def plot_rfft_ir(t, ir, ):
    print('To be implemented.')
    pass

def get_msc(sig_0, sig_1, fs, blocklen, ):
    print('Not tested, use with caution!')
    freq_msc, msc = scsp.coherence(
        sig_0,
        sig_1,
        fs,
        nperseg=blocklen,
    )
    return freq_msc, msc

def uint_to_float(arr_uint, bit_depth):
    num_neg_bits = 2**(bit_depth-1)
    num_pos_bits = num_neg_bits - 1
    arr_wo_offset = arr_uint.astype(float) - num_neg_bits
    arr_float = np.array([])

    for num in arr_wo_offset:
        if num >= 0:
            arr_float = np.append(arr_float, num/num_pos_bits)
        else:
            arr_float = np.append(arr_float, num/num_neg_bits)

    return arr_float

def sint_to_float(arr_sint, bit_depth):
    num_bits = 2**(bit_depth-1)
    return arr_sint/num_bits

def import_wav(fnames, ):
    files = {}
    float_sig = {}
    for fname in fnames:
        wav = scio.read(fname)
        dt = str(wav[1].dtype)
        if dt.startswith('int'):
            to_float = sint_to_float
        elif dt.startswith('uint'):
            to_float = uint_to_float
        bit_depth = int(str(wav[1].dtype)[-2:])
        files[fname] = wav
        fs = wav[0]
        if np.size(wav[1][0]) == 2:
            is_stereo = True
        else:
            is_stereo = False
        if is_stereo:
            left = np.array([stereo[0] for stereo in files[fname][1]])/((2**15)-1)
            left = to_float(left, bit_depth)
            right = np.array([stereo[1] for stereo in files[fname][1]])/((2**15)-1)
            right = to_float(right, bit_depth)
            float_sig[fname] = [fs, left, right,]
        else:
            left = np.array([stereo for stereo in files[fname][1]])/((2**15)-1)
            float_sig[fname] = [fs, left,]
        files[fname] = float_sig[fname]
    return files