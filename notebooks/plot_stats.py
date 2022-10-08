import pylab
import numpy


def plot_stats_notebook(m, t, o, d):
    # set figure size
    pylab.rcParams["figure.figsize"] = (12, 4)
    # set line width
    pylab.rcParams['lines.linewidth'] = 4
    # set font size for titles
    pylab.rcParams['axes.titlesize'] = 12
    # set font size for labels on axes
    pylab.rcParams['axes.labelsize'] = 7
    # set size of numbers on x-axis
    pylab.rcParams['xtick.labelsize'] = 7
    # set size of numbers on y-axis
    pylab.rcParams['ytick.labelsize'] = 7
    # set size of ticks on x-axis
    pylab.rcParams['xtick.major.size'] = 7
    # set size of ticks on y-axis
    pylab.rcParams['ytick.major.size'] = 7
    # set size of markers, e.g., circles representing points
    # set numpoints for legend
    pylab.rcParams['legend.numpoints'] = 1

    pylab.gcf().canvas.manager.set_window_title('Monte Carlo Fund Simulator')

    pylab.figure(1)

    pylab.subplot(1, 3, 1)
    pylab.hist(m, bins=60, weights=[1 / len(m)] * len(m))
    pylab.xlabel('MOIC '
                 + '(mean: ' + str(round(float(numpy.mean(m)), 2))
                 + ', median: ' + str(round(float(numpy.median(m)), 2))
                 + ', stdev: ' + str(round(float(numpy.std(m)), 2))
                 + ', max: ' + str(round(numpy.max(m), 2))
                 + ', min: ' + str(round(numpy.min(m), 2))
                 + ')')
    pylab.title('MOIC Distribution')

    pylab.subplot(1, 3, 2)
    pylab.hist(t, bins=60, weights=[1 / len(t)] * len(t))
    pylab.xlabel('TVPI '
                 + '(mean: ' + str(round(float(numpy.mean(t)), 2))
                 + ', median: ' + str(round(float(numpy.median(t)), 2))
                 + ', stdev: ' + str(round(float(numpy.std(t)), 2))
                 + ', max: ' + str(round(numpy.max(t), 2))
                 + ', min: ' + str(round(numpy.min(t), 2))
                 + ')')
    pylab.title('TVPI Distribution')

    pylab.subplot(1, 3, 3)
    pylab.pie(d, labels=['Initial Tickets', 'Follow-On'], startangle=110, autopct='%1.1f%%', textprops={'fontsize': 7})
    pylab.title('Initial vs Follow-On Split (by $)')

    pylab.show()
    pass


def plot_sweep_stats(x, y, plot_label):
    # set figure size
    pylab.rcParams["figure.figsize"] = (12, 4)
    # set line width
    pylab.rcParams['lines.linewidth'] = 4
    # set font size for titles
    pylab.rcParams['axes.titlesize'] = 12
    # set font size for labels on axes
    pylab.rcParams['axes.labelsize'] = 7
    # set size of numbers on x-axis
    pylab.rcParams['xtick.labelsize'] = 7
    # set size of numbers on y-axis
    pylab.rcParams['ytick.labelsize'] = 7
    # set size of ticks on x-axis
    pylab.rcParams['xtick.major.size'] = 7
    # set size of ticks on y-axis
    pylab.rcParams['ytick.major.size'] = 7
    # set size of markers, e.g., circles representing points
    # set numpoints for legend
    pylab.rcParams['legend.numpoints'] = 1

    pylab.figure(1)

    pylab.subplot(1, 1, 1)
    pylab.plot(x, y["mean"], label=str(plot_label + " mean"))
    pylab.plot(x, y["min"], label=str(plot_label + " min"))
    pylab.plot(x, y["max"], label=str(plot_label + " max"))
    pylab.title(plot_label + ' Sweep across portfolio size')
    pylab.legend(loc='upper left')

    pylab.show()
