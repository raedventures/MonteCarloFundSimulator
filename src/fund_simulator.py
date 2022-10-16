import datetime
import sys

from simulator_engine import runSimulation, plotStats
from params import FundParams, PortfolioSelectionParams, OutcomeNames
from src.strategy.double_tap_strategy import DoubleTapStrategy
from strategy.base_strategy import BaseStrategy
from strategy.simple_prorata_strategy import SimpleProRataStrategy


def setFundParameters():
    f = FundParams()

    f.fund_size = 50_000_000
    f.fund_lifetime = 10
    f.management_fees = 0.02
    f.fund_expenses = 0.01
    f.investable_capital = f.fund_size * (1 - (f.management_fees * f.fund_lifetime + f.fund_expenses))
    f.carry = 0.2
    f.deployment_start_date = datetime.date(2023, 1, 1)
    f.recycling = 0.0

    return f


def setPortfolioSelectionParameters():
    portSelectionParams = PortfolioSelectionParams()

    # Market-driven startup outcomes with eventual exit value and number of rounds to get there
    portSelectionParams.outcomeTypes = {
        OutcomeNames.EarlyStageFail: {"exit_value": 0, "num_rounds": 2},
        OutcomeNames.Failing: {"exit_value": 0, "num_rounds": 3},
        OutcomeNames.Niche: {"exit_value": 90_000_000, "num_rounds": 3},
        OutcomeNames.AlsoRan: {"exit_value": 200_000_000, "num_rounds": 4},
        OutcomeNames.CloseChallenger: {"exit_value": 500_000_000, "num_rounds": 5},
        OutcomeNames.MarketLeader: {"exit_value": 1_500_000_000, "num_rounds": 5},
        OutcomeNames.MarketOutlier: {"exit_value": 3_000_000_000, "num_rounds": 6}
    }

    # Skill of selecting each type of company (cumulative probability in ascending order)
    portSelectionParams.outcomeSelection = {
        OutcomeNames.EarlyStageFail: 15,  # 15% prob (15% cum)
        OutcomeNames.Failing: 45,  # 30% prob (45% cum)
        OutcomeNames.Niche: 67,  # 22% prob (65% cum)
        OutcomeNames.AlsoRan: 90,  # 20% prob (87% cum)
        OutcomeNames.CloseChallenger: 98,  # 10% prob (95% cum)
        OutcomeNames.MarketLeader: 99,  # 2% prob (98% cum)
        OutcomeNames.MarketOutlier: 100  # 1% prob (100% cum)
    }

    # Initial target valuation range probability distribution (cumulative probability in ascending order)
    portSelectionParams.initialValuationDist = (
        (5_000_000, 28),  # 28%
        (7_500_000, 50),  # 28% (56% cumulative)
        (10_000_000, 65),  # 16% (72% cumulative)
        (15_000_000, 83),  # 11% (83% cumulative)
        (25_000_000, 100),  # 17% (100% cumulative)
    )

    # Initial allocation probability distribution
    portSelectionParams.initialAllocationDist = (
        (0.05, 6),  # 6%
        (0.08, 58),  # 22% (28% cumulative)
        (0.10, 85),  # 41% (69% cumulative)
        (0.12, 97),  # 26% (95% cumulative)
        (0.15, 100),  # 5% (100% cumulative)
    )

    return portSelectionParams


def setStrategyParameters(s: BaseStrategy):
    s.deployment_period = 3
    s.target_ownership = 0.1
    s.max_concentration = 0.1 * s.fundParams.fund_size
    s.max_valuation = 100_000_000
    s.minimum_initial_ticket = 250_000
    s.maximum_initial_ticket = 1_500_000
    s.minimum_followon_ticket = 1_000_000
    s.maximum_followon_ticket = 2_000_000
    s.setNumPortCos(25)

    return s


if __name__ == '__main__':
    fp = setFundParameters()
    psp = setPortfolioSelectionParameters()
    strategy = DoubleTapStrategy(fund_params=fp, portfolio_params=psp)
    strategy = setStrategyParameters(strategy)

    # strategy = SimpleProRataStrategy()

    # Read runtime args (if any) for number of iterations
    num_iterations = 5000 if len(sys.argv) <= 1 else int(sys.argv[1])

    moics, tvpis, outcomes, [it, ft], num_rounds = runSimulation(strategy, num_iterations, show_progress=True)

    # plot fund performance summary
    plotStats(moics, tvpis, outcomes, [it, ft])
    print(f"number of rounds simulated: {num_rounds:,}")

    # strategy.investmentRounds.sort(key=lambda rd: (rd.portco.num, rd.roundDate))
    # for x in strategy.investmentRounds:
    #     print(x)
