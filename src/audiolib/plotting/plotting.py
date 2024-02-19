import matplotlib.pyplot as plt
import numpy as np 
import scipy.signal as scsp
import scipy.io.wavfile as scio

from matplotlib.ticker import EngFormatter
from scipy.fftpack import fftshift

# TODO: Try to write plotting as pyplot wrapper
ENG_FORMAT = EngFormatter()

def _parse_plot_func(
        ax,
        xscale,
        yscale,
):
    if xscale == 'lin' and yscale == 'lin':
        plot_func = ax.plot
    if xscale == 'log' and yscale == 'lin':
        plot_func = ax.semilogx
    if xscale == 'lin' and yscale == 'log':
        plot_func = ax.semilogy
    if xscale == 'log' and yscale == 'log':
        plot_func = ax.loglog
    return plot_func

def _scale_plot(
        ax,
        scient_scale_x,
        scient_scale_y,
):
    if scient_scale_x:
        ax.xaxis.set_major_formatter(ENG_FORMAT)
    if scient_scale_y:
        ax.yaxis.set_major_formatter(ENG_FORMAT)
    return ax

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
        scient_scale_x=True,
        scient_scale_y=False,
        fig=None,
        ax=None,
        interactive_on=False,
        **line_kwargs,
):

    if interactive_on:
        plt.ion()
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = plt.gca()
    plot_func = _parse_plot_func(
        ax,
        xscale,
        yscale,
    )
    plot_func(f, data, **line_kwargs)
    ax = _scale_plot(ax, scient_scale_x, scient_scale_y, )
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude')  
    ax.grid(True, which='both')
    if 'label' in line_kwargs:
        ax.legend()
    return fig, ax,

def plot_h_full(freq_h, freq_msc, magnitude, phase_deg, msc,):
    fig = plt.figure()
    plt.subplot(311)
    ax_mod = plt.gca()
    ax_mod.set_title('Transfer Function Mic2/Mic1')
    ax_mod.plot(freq_h, magnitude)
    ax_mod.grid(which='both')
    ax_mod.set_ylabel('Magnitude [dB]')
    plt.subplot(312, sharex=ax_mod)
    ax_arg = plt.gca()
    ax_arg.plot(freq_h, phase_deg,)
    ax_arg.set_ylabel('Phase [Deg]')
    ax_arg.grid(which='both')
    plt.subplot(313, sharex=ax_mod)
    ax_msc = plt.gca()
    ax_msc.plot(freq_msc, msc,)
    ax_msc.set_ylabel('MSC')
    ax_msc.grid(which='both')
    ax_msc.set_xlabel('Frequency [Hz]')
    ax_msc.set_ylim([.5, 1.2])
    _ = plt.setp(ax_mod.get_xticklabels(), visible=False)
    _ = plt.setp(ax_arg.get_xticklabels(), visible=False)

    return fig, ax_mod, ax_arg, ax_msc,

def plot_mag_phase():
    print("To be implemented.")
    pass

def plot_ir(
        t,
        ir,
        time_plot_width = None,
        time_plot_center = 0,
        scient_scale_x=True,
        scient_scale_y=False,
        fig=None,
        ax=None,
        interactive_on=False,
        **line_kwargs,
):
    """
    Plot zero-centered impulse response.

    Parameters
    ----------
    t : array
        Time vector
    ir : array
        Impulse response to be plotted
    time_plot_width : float
        Time-Width of the plot. Defaults to None (whole IR plotted)
    time_plot_center : float
        Can only be set if time_plot_width is set.
        Defaults to t = 0.
    scient_scale : boolean
        If True, x-axis is shown using engineering prefixes to represent powers of 1000,
        plus a specified unit, e.g., 10 MHz instead of 1e7.
    fig : matplotlib.figure.Figure
        Figure instance of current IR fig
    ax : matplotlib.axes._axes.Axes
        Axes instance of current IR fig

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure instance of current IR fig
    ax : matplotlib.axes._axes.Axes
        Axes instance of current IR fig
    """

    if interactive_on:
        plt.ion()
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = plt.gca()
    if time_plot_width is None:
        time_plot_width = t[-1] # Plot everything if None
    if (time_plot_center - time_plot_width) < t[0]:
        raise ValueError(
            'Chosen plot end smaller than lowest available timestamp. ' +
            'Adjust time_plot_width or time_plot_center.'
        )
    if (time_plot_center + time_plot_width) > t[-1]:
        raise ValueError(
            'Chosen plot end smaller larger than highest available timestamp. ' +
            'Adjust time_plot_width or time_plot_center.'
        )
    ax = _scale_plot(
        ax,
        scient_scale_x,
        scient_scale_y,
    )
    xlims = [
        time_plot_center - time_plot_width,
        time_plot_center + time_plot_width,
    ]

    fig.set_size_inches([6.4, 3])
    ax = plt.gca()
    ax.set_title('Impulse Response')
    ax.plot(
        t,
        ir,
        '--o',
        **line_kwargs,
    )
    ax.set_xlim(xlims)
    ax.set_xlabel('Time [s]')
    ax.grid()
    plt.tight_layout()
    return fig, ax,
