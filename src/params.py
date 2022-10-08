import datetime
from enum import Enum
from outcome_names import OutcomeNames


class FundParams:
    """ Fund object holding key fund parameters """

    def __init__(self):
        self.fund_size = 150000000
        self.fund_lifetime = 10
        self.management_fees = 0.018
        self.fund_expenses = 0.01
        self.investable_capital = self.fund_size * (
                1 - (self.management_fees * self.fund_lifetime + self.fund_expenses))
        self.carry = 0.2
        self.deployment_start_date = datetime.date(2023, 1, 1)
        self.recycling = 0.0
        pass


class PortfolioSelectionParams:
    """ Main portfolio selection parameters """
    def __init__(self):
        # Market-driven startup outcomes with eventual exit value and number of rounds to get there
        self.outcomeTypes = {
            OutcomeNames.EarlyStageFail: {"exit_value": 0, "num_rounds": 2},
            OutcomeNames.Failing: {"exit_value": 0, "num_rounds": 3},
            OutcomeNames.Niche: {"exit_value": 100000000, "num_rounds": 3},
            OutcomeNames.AlsoRan: {"exit_value": 300000000, "num_rounds": 4},
            OutcomeNames.CloseChallenger: {"exit_value": 600000000, "num_rounds": 5},
            OutcomeNames.MarketLeader: {"exit_value": 2000000000, "num_rounds": 5},
            OutcomeNames.MarketOutlier: {"exit_value": 5000000000, "num_rounds": 6}
        }

        # Skill of selecting each type of company
        self.outcomeSelection = {
            OutcomeNames.EarlyStageFail: 15,  # 15% prob (15% cum)
            OutcomeNames.Failing: 45,  # 30% prob (45% cum)
            OutcomeNames.Niche: 65,  # 22% prob (65% cum)
            OutcomeNames.AlsoRan: 89,  # 20% prob (87% cum)
            OutcomeNames.CloseChallenger: 95,  # 10% prob (95% cum)
            OutcomeNames.MarketLeader: 98,  # 3% prob (98% cum)
            OutcomeNames.MarketOutlier: 100  # 2% prob (100% cum)
        }

        # Initial target valuation range probability distribution
        self.initialValuationDist = (
            (10000000, 28),  # 28%
            (15000000, 55),  # 28% (56% cumulative)
            (25000000, 87),  # 16% (72% cumulative)
            (35000000, 95),  # 11% (83% cumulative)
            (50000000, 100),  # 17% (100% cumulative)
        )

        # Initial allocation probability distribution
        self.initialAllocationDist = (
            (0.05, 6),  # 6%
            (0.07, 20),  # 22% (28% cumulative)
            (0.10, 85),  # 41% (69% cumulative)
            (0.12, 97),  # 26% (95% cumulative)
            (0.15, 100),  # 5% (100% cumulative)
        )

        # Probability of identifying an outlier for follow-on (not counting initial ticket src)
        # Why have this? As a startup progresses, a fund manager is better able to tell if a particular company is
        # likely to be an outlier and (if fund strategy permits) double down in subsequent rounds
        self.followOnProbability = {
            OutcomeNames.EarlyStageFail: (100, 15, 0, 0, 0, 0, 0),
            OutcomeNames.Failing: (100, 20, 10, 0, 0, 0, 0),
            OutcomeNames.Niche: (100, 30, 20, 10, 0, 0, 0),
            OutcomeNames.AlsoRan: (100, 60, 40, 20, 0, 0, 0),
            OutcomeNames.CloseChallenger: (100, 100, 90, 80, 80, 60, 50),
            OutcomeNames.MarketLeader: (100, 100, 90, 90, 80, 80, 80),
            OutcomeNames.MarketOutlier: (100, 100, 100, 90, 90, 90, 90),
        }



