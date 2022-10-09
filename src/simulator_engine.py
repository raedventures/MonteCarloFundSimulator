import datetime
import math
import random
import numpy
import pylab

from portco import Portco
from round import Round
from outcome_names import OutcomeNames
from round_names import RoundNames
# from src.params import OutcomeNames, RoundNames
from strategy.base_strategy import BaseStrategy


def constructPortCos(s: BaseStrategy):
    """ Construct random portfolio of size 'num' based on outcome probabilities """
    s.clearPortfolio()
    for i in range(s.num_portcos):
        rand = random.randint(1, 100)
        for j in range(len(OutcomeNames)):
            if s.portfolioSelectionParams.outcomeSelection[OutcomeNames(j + 1)] >= rand:
                newPortCo = Portco(i + 1, "PortCo" + str(i + 1), OutcomeNames(j + 1))
                s.portfolio.append(newPortCo)
                break
    return s.portfolio


def constructRounds(s: BaseStrategy):
    """ Generate all investment rounds and fund participation decisions for the fund lifetime based on a particular
    investment strategy """
    # Initializing
    portCoNumber = 0
    s.clearInvestments()

    # generate initial ticket calculations for each portfolio company
    for p in s.portfolio:
        portCoNumber += 1

        # Pace out the initial ticket deployments evenly throughout the deployment period (roughly quarterly)
        roundDate = s.fundParams.deployment_start_date + datetime.timedelta(
            days=math.floor(1.0 * portCoNumber / math.ceil(1.0 * s.num_portcos / s.deployment_period / 4.0)) * 92)
        p.initialInvestmentDate = roundDate

        initialRound = Round(p, 1, roundDate, 0, 0, 0, 0)
        s.generateInitialTicket(initialRound)

        s.investmentRounds.append(initialRound)

        # generate entries for future rounds (fr) without taking investment decision yet
        numFutureRounds = s.portfolioSelectionParams.outcomeTypes[p.type]["num_rounds"]
        for fr in range(numFutureRounds):
            newRoundValuation = round(initialRound.valuation * (p.avgRoundMultiple ** (fr + 1)))
            newRoundSize = RoundNames.getAvgDilution(newRoundValuation) * newRoundValuation

            # Last src should be 0 for failing companies
            if (p.type == OutcomeNames.EarlyStageFail or p.type == OutcomeNames.Failing) and fr == numFutureRounds - 1:
                newRoundValuation = 0

            # TODO: Current assumption is next fundraise after 1 year. Need to make flexible
            newRound = Round(p, fr + 2, roundDate.replace(year=roundDate.year + fr + 1), newRoundValuation,
                             newRoundSize, 0, 0)
            p.lastValuation = newRoundValuation
            p.totalRaised += newRoundSize
            s.investmentRounds.append(newRound)

    # Sort rounds in place by the src date (asc) to prep for chronological follow-on strategy execution. The logic
    # is that funds usually decide on a deal-by-deal basis as they come (keeping in mind overall fund strategy)
    s.investmentRounds.sort(key=lambda rd: rd.roundDate)

    # Execute on follow-on strategy.
    # Constrained by fund capital, portfolio concentration, and probability of successful investment
    for r in s.investmentRounds:

        # skip the failed companies (0 valuation) and initial tickets already deployed
        if r.valuation == 0 or r.ticket != 0:
            continue

        s.generateFollowOnTicket(r)

    return s.initialTickets, s.followOnTickets


def computeFundStats(s: BaseStrategy):
    fmv = 0.0
    portfolioOutcomes = [0, 0, 0, 0, 0, 0, 0]
    for x in s.portfolio:
        fmv += x.lastOwnershipStake * x.lastValuation
        portfolioOutcomes[x.type.value - 1] += 1
    moic = round(fmv / s.totalCapitalDeployed, 2)
    tvpi = round((fmv - (fmv - s.fundParams.fund_size) * s.fundParams.carry) / s.fundParams.fund_size, 2)
    return moic, tvpi, portfolioOutcomes


def plotStats(m, t, o, d):
    # set figure size
    pylab.rcParams["figure.figsize"] = (12, 7)
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
    pylab.subplot(2, 2, 1)
    pylab.hist(m, bins=60, weights=[1 / len(m)] * len(m))
    pylab.xlabel('MOIC '
                 + '(mean: ' + str(round(float(numpy.mean(m)), 2))
                 + ', median: ' + str(round(float(numpy.median(m)), 2))
                 + ', stdev: ' + str(round(float(numpy.std(m)), 2))
                 + ', max: ' + str(round(numpy.max(m), 2))
                 + ', min: ' + str(round(numpy.min(m), 2))
                 + ')')
    pylab.title('MOIC Distribution')

    pylab.subplot(2, 2, 2)
    pylab.hist(t, bins=60, weights=[1 / len(t)] * len(t))
    pylab.xlabel('TVPI '
                 + '(mean: ' + str(round(float(numpy.mean(t)), 2))
                 + ', median: ' + str(round(float(numpy.median(t)), 2))
                 + ', stdev: ' + str(round(float(numpy.std(t)), 2))
                 + ', max: ' + str(round(numpy.max(t), 2))
                 + ', min: ' + str(round(numpy.min(t), 2))
                 + ')')
    pylab.title('TVPI Distribution')

    # pylab.figure(2)
    pylab.subplot(2, 2, 3)
    pylab.pie(numpy.array(o),
              labels=[
                  OutcomeNames.EarlyStageFail.name,
                  OutcomeNames.Failing.name,
                  OutcomeNames.Niche.name,
                  OutcomeNames.AlsoRan.name,
                  OutcomeNames.CloseChallenger.name,
                  OutcomeNames.MarketLeader.name,
                  OutcomeNames.MarketOutlier.name
              ], startangle=0, autopct='%1.f%%', textprops={'fontsize': 7})
    pylab.title('Distribution of Outcomes')

    pylab.subplot(2, 2, 4)
    pylab.pie(d, labels=['Initial Tickets', 'Follow-On'], startangle=110, autopct='%1.1f%%', textprops={'fontsize': 7})
    pylab.title('Initial vs Follow-On Split (by $)')

    pylab.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.95, wspace=0.11, hspace=0.3)
    pylab.show()
    pass


def showProgressBar(iteration, total, prefix='', suffix='', decimals=2, bar_length=50):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    print(f'\r{prefix} |{bar}| {percents}% {suffix}', end='')

    if iteration == total:
        print('\n')


def runSimulation(s: BaseStrategy, num_iterations, show_progress=True):
    moics = []
    tvpis = []
    outcomes = [0, 0, 0, 0, 0, 0, 0]
    sumInitialTickets = 0
    sumFollowOns = 0

    fill = math.floor(math.log10(num_iterations) + 1)

    for x in range(num_iterations):
        if show_progress:
            showProgressBar(x + 1, num_iterations, "Monte Carlo Fund Simulation # " + str(x + 1).rjust(fill) + " / "
                            + str(num_iterations) + ":")

        constructPortCos(s)  # create initial list of portfolio companies

        i, f = constructRounds(s)  # make all deployment decisions based on the fund strategy
        sumInitialTickets += i
        sumFollowOns += f

        m, t, o = computeFundStats(s)  # compute fund performance stats
        moics.append(m)
        tvpis.append(t)
        outcomes = numpy.add(o, outcomes)

        # print(round(s.initialTickets), round(s.followOnTickets),
        #       round(s.totalCapitalDeployed), m, t, o)

    return moics, tvpis, outcomes, [sumInitialTickets, sumFollowOns]

