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
    pylab.axvline(x=numpy.percentile(m, 75), ymin=0, color='red', linestyle='dotted', linewidth=1.5, label="Upper Quartile")
    pylab.axvline(x=numpy.percentile(m, 25), ymin=0, color='yellow', linestyle='dotted', linewidth=1.5, label="Lower Quartile")
    pylab.axvline(x=numpy.percentile(m, 50), ymin=0, color='cyan', linestyle='dotted', linewidth=1.5, label="Median")
    pylab.legend(loc='upper right')
    pylab.xlabel('MOIC '
                 + '(mean: ' + str(round(float(numpy.mean(m)), 2))
                 + ', median: ' + str(round(float(numpy.median(m)), 2))
                 + ', upper Q: ' + str(round(numpy.percentile(m, 75), 2))
                 + ', lower Q: ' + str(round(numpy.percentile(m, 25), 2))
                 + ', stdev: ' + str(round(float(numpy.std(m)), 2))
                 + ')')
    pylab.title('MOIC Distribution')

    pylab.subplot(1, 3, 2)
    pylab.hist(t, bins=60, weights=[1 / len(t)] * len(t))
    pylab.axvline(x=numpy.percentile(t, 75), ymin=0, color='red', linestyle='dotted', linewidth=1.5, label="Upper Quartile")
    pylab.axvline(x=numpy.percentile(t, 25), ymin=0, color='yellow', linestyle='dotted', linewidth=1.5, label="Lower Quartile")
    pylab.axvline(x=numpy.percentile(t, 50), ymin=0, color='cyan', linestyle='dotted', linewidth=1.5, label="Median")
    pylab.legend(loc='upper right')
    pylab.xlabel('TVPI '
                 + '(mean: ' + str(round(float(numpy.mean(t)), 2))
                 + ', median: ' + str(round(float(numpy.median(t)), 2))
                 + ', upper Q: ' + str(round(numpy.percentile(t, 75), 2))
                 + ', lower Q: ' + str(round(numpy.percentile(t, 25), 2))
                 + ', stdev: ' + str(round(float(numpy.std(t)), 2))
                 + ')')
    pylab.title('TVPI Distribution')

    pylab.subplot(1, 3, 3)
    pylab.pie(d, labels=['Initial Tickets', 'Follow-On'], startangle=110, autopct='%1.1f%%', textprops={'fontsize': 7})
    pylab.title('Initial vs Follow-On Split (by $)')

    pylab.show()
    pass


def plot_sweep_stats(x, y, plot_label):
    # set figure size
    pylab.rcParams["figure.figsize"] = (15, 4)
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

    pylab.subplot(1, 4, 1)
    pylab.title(plot_label + ' median')
    pylab.plot(x, y["median"], label=str(plot_label + " median"), color="blue")

    pylab.subplot(1, 4, 2)
    pylab.title(plot_label + ' top decile')
    pylab.plot(x, y["top"], label=str(plot_label + " top decile"), color="green")

    pylab.subplot(1, 4, 3)
    pylab.title(plot_label + ' bottom decile')
    pylab.plot(x, y["bottom"], label=str(plot_label + " bottom decile"), color="red")

    pylab.subplot(1, 4, 4)
    pylab.title(plot_label + ' combined')
    pylab.plot(x, y["median"], label=str(plot_label + " median"), color="blue")
    pylab.plot(x, y["top"], label=str(plot_label + " top decile"), color="green")
    pylab.plot(x, y["bottom"], label=str(plot_label + " bottom decile"), color="red")

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
    pylab.plot(x, y_both[1]["median"], label=str(plot_label_both[1]), color="dodgerblue")
    pylab.legend(loc='upper left')

    pylab.subplot(1, 3, 2)
    pylab.title(title + ' top decile')
    pylab.plot(x, y_both[0]["top"], label=str(plot_label_both[0]), color="green")
    pylab.plot(x, y_both[1]["top"], label=str(plot_label_both[1]), color="limegreen")
    pylab.legend(loc='upper left')

    pylab.subplot(1, 3, 3)
    pylab.title(title + ' bottom decile')
    pylab.plot(x, y_both[0]["bottom"], label=str(plot_label_both[0]), color="red")
    pylab.plot(x, y_both[1]["bottom"], label=str(plot_label_both[1]), color="darkorange")
    pylab.legend(loc='upper left')

    pylab.show()
