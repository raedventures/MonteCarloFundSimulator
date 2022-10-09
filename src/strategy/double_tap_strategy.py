import math
import random

from src.params import FundParams, PortfolioSelectionParams
from src.round import Round
from src.strategy.simple_prorata_strategy import SimpleProRataStrategy


class DoubleTapStrategy(SimpleProRataStrategy):
    def __init__(self, ratio=0.5, fund_params=FundParams(), portfolio_params=PortfolioSelectionParams()):
        self.ratio = ratio
        self.initial_ticket = 0
        self.followon_ticket = 0
        super().__init__(fund_params, portfolio_params)


    def setNumPortCos(self, num: int):
        self.num_portcos = num

        # Find total value of tickets based on the number of companies
        total_tickets = 1.0 * self.fundParams.investable_capital / num

        # Use ratio to split between initial and follow on
        self.initial_ticket = self.ratio * total_tickets
        self.followon_ticket = (1-self.ratio) * total_tickets

        self.maximum_initial_ticket = self.minimum_initial_ticket = self.initial_ticket
        self.maximum_followon_ticket = self.minimum_followon_ticket = self.followon_ticket

        return num

    def shouldFollowOn(self, r: Round):
        """ double down once only for the second round """
        return super().shouldFollowOn(r) and r.roundNumber <= 2
