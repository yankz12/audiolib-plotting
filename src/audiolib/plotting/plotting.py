import matplotlib.pyplot as plt
import numpy as np 
import scipy.signal as scsp
import scipy.io.wavfile as scio

from matplotlib import ticker
from scipy.fftpack import fftshift

# TODO: Try to write plotting as pyplot wrapper

# Function to plot x- and y-axis with k for kilo and M for Mega
# TODO: Fix MKFUNC for yscale around 0
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
) 

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
    return fig, ax,

def plot_rfft_freq(
        f,
        data,
        xscale='lin',
        yscale='lin',
        scient_scale=True,
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
    if xscale == 'lin' and yscale == 'log':
        ax.semilogy(f, data, **line_kwargs)
    if xscale == 'log' and yscale == 'log':
        ax.loglog(f, data, **line_kwargs)
    if scient_scale and (xscale == 'log'):
        ax.xaxis.set_major_formatter(mkformatter)
        # TODO: Insert yaxis scient scale as soon as fixed
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude')  
    ax.grid(True, which='both')
    ax.legend()
    return fig, ax,

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

def plot_rfft_ir(t, ir, ):
    # TODO: Implement
    print('To be implemented.')
    pass
