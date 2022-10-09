import pylab
import numpy


def plot_stats_notebook(m, t, o, d):
    # set figure size
    pylab.rcParams["figure.figsize"] = (12, 4)
    # # set line width
    # pylab.rcParams['lines.linewidth'] = 4
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
    # set numpoints for legend
    pylab.rcParams['legend.numpoints'] = 1

    pylab.figure(1)

    pylab.subplot(1, 3, 1)
    pylab.title(plot_label + ' median')
    # pylab.legend(loc='upper left')
    pylab.plot(x, y["median"], label=str(plot_label + " median"), color="blue")

    pylab.subplot(1, 3, 2)
    pylab.title(plot_label + ' top decile')
    # pylab.legend(loc='upper left')
    pylab.plot(x, y["top"], label=str(plot_label + " top decile"), color="green")

    pylab.subplot(1, 3, 3)
    pylab.title(plot_label + ' bottom decile')
    # pylab.legend(loc='upper left')
    pylab.plot(x, y["bottom"], label=str(plot_label + " bottom decile"), color="red")

    # pylab.legend(loc='upper right')
    pylab.show()


def plot_compare_sweeps(x, y_both, title, plot_label_both):
    # set figure size
    pylab.rcParams["figure.figsize"] = (12, 4)
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
    # set numpoints for legend
    pylab.rcParams['legend.numpoints'] = 1

    pylab.figure(1)
    pylab.subplot(1, 3, 1)
    pylab.title(title + ' median')
    pylab.plot(x, y_both[0]["median"], label=str(plot_label_both[0]), color="blue")
    pylab.plot(x, y_both[1]["median"], label=str(plot_label_both[1]), color="dodgerblue", linestyle="--")
    pylab.legend(loc='upper left')

    pylab.subplot(1, 3, 2)
    pylab.title(title + ' top decile')
    pylab.plot(x, y_both[0]["top"], label=str(plot_label_both[0]), color="green")
    pylab.plot(x, y_both[1]["top"], label=str(plot_label_both[1]), color="limegreen", linestyle="--")
    pylab.legend(loc='upper left')

    pylab.subplot(1, 3, 3)
    pylab.title(title + ' bottom decile')
    pylab.plot(x, y_both[0]["bottom"], label=str(plot_label_both[0]), color="red")
    pylab.plot(x, y_both[1]["bottom"], label=str(plot_label_both[1]), color="tomato", linestyle="--")
    pylab.legend(loc='upper left')

    pylab.show()
