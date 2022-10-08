import random
from abc import abstractmethod

from src.params import FundParams, PortfolioSelectionParams
from src.round import Round


class BaseStrategy:
    def __init__(self, fund_params=FundParams(), portfolio_params=PortfolioSelectionParams()):
        self.totalCapitalDeployed = self.initialTickets = self.followOnTickets = 0.0
        self.portfolio = []  # List containing all portfolio companies of the fund
        self.investmentRounds = []  # List containing all investment rounds for the fund portfolio

        self.fundParams = fund_params
        self.portfolioSelectionParams = portfolio_params

        self.deployment_period = 3
        self.target_ownership = 0.1
        self.max_concentration = 0.1 * self.fundParams.fund_size
        self.max_valuation = 250000000
        self.minimum_initial_ticket = 1000000
        self.maximum_initial_ticket = 5000000
        self.minimum_followon_ticket = 1500000
        self.maximum_followon_ticket = 5000000
        self.num_portcos = self.setNumPortCos(30)

    def setNumPortCos(self, num: int):
        self.num_portcos = num
        newMax = 1.0 * self.fundParams.investable_capital / num

        # if num portcos is too high then adjust max initial tickets to allow for at least 1 ticket in each portco
        if newMax < self.maximum_initial_ticket:
            self.maximum_initial_ticket = newMax
            if self.minimum_initial_ticket > newMax: # if minimum is too high then cap minimum also
                self.minimum_initial_ticket = newMax

        return num

    def clearAll(self):
        """ Clear all portfolio and investment rounds """
        self.totalCapitalDeployed = self.initialTickets = self.followOnTickets = 0.0
        self.portfolio.clear()
        self.investmentRounds.clear()

    def clearInvestments(self):
        """ Keep current portfolio but clear out all rounds and investments """
        self.totalCapitalDeployed = self.initialTickets = self.followOnTickets = 0.0
        self.investmentRounds.clear()

    def clearPortfolio(self):
        """ Clear out all portfolio and (hence) all associated investment rounds """
        self.clearAll()

    @abstractmethod
    def generateInitialTicket(self, r: Round) -> (int, int, float, int):
        """ Calculate portfolio company initial ticket parameters
        :param r: Round object
        :return: valuation, src size, % allocation, ticket
        """
        return 0, 0, 0.0, 0

    @abstractmethod
    def generateFollowOnTicket(self, r: Round) -> (float, float):
        """
        Make follow-on deployment decision for a src
        :param r: Round object
        :return: Initial tickets, follow-on tickets
        """
        return 0.0, 0.0

    def shouldFollowOn(self, r: Round):
        prob = self.portfolioSelectionParams.followOnProbability[r.portco.type][r.roundNumber - 2]
        if prob >= random.randint(1, 100):
            return True
        return False
