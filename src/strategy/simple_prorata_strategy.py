import math
import random

from src.params import FundParams, PortfolioSelectionParams
from src.round import Round
from src.round_names import RoundNames
from src.strategy.base_strategy import BaseStrategy


class SimpleProRataStrategy(BaseStrategy):
    def __init__(self, fund_params=FundParams(), portfolio_params=PortfolioSelectionParams()):
        BaseStrategy.__init__(self, fund_params, portfolio_params)

    def generateInitialTicket(self, r):
        """
        Generate a random initial src
        @:returns
            valuation: src valuation
            allocation: fund allocation %
            ticket: fund ticket size (constrained by max and min ticket sizes and total fund size)
        """
        valuation = 0
        allocation = 0.0

        randVal = random.randint(1, 100)
        randAlloc = random.randint(1, 100)

        for i in self.portfolioSelectionParams.initialValuationDist:
            if i[1] >= randVal:
                valuation = i[0]
                break

        for j in self.portfolioSelectionParams.initialAllocationDist:
            if j[1] >= randAlloc:
                allocation = j[0]
                break

        # Calculate round size
        roundSize = RoundNames.getAvgDilution(valuation) * valuation

        ticket = round(allocation * valuation)

        # make sure ticket is within fund ticket size rules
        ticket = min(ticket, self.maximum_initial_ticket)  # does not exceed max initial ticket
        ticket = max(ticket, self.minimum_initial_ticket)  # does not go below min initial ticket size
        ticket = min(ticket, self.fundParams.investable_capital - self.totalCapitalDeployed)  # does not exceed investable capital

        # Safety check: If min ticket requirements exceed round size then cap at 75% of the round
        if ticket >= roundSize:
            ticket = 0.75 * roundSize

        allocation = round(ticket / valuation, 2)

        r.portco.lastValuation = valuation
        r.portco.totalRaised += roundSize
        r.valuation = valuation
        r.roundSize = roundSize
        r.putTicket(ticket)

        self.totalCapitalDeployed += ticket
        self.initialTickets += ticket

        # calculate average src multiplier for future rounds
        numFutureRounds = self.portfolioSelectionParams.outcomeTypes[r.portco.type]["num_rounds"]
        exitValue = self.portfolioSelectionParams.outcomeTypes[r.portco.type]["exit_value"]
        r.portco.avgRoundMultiple = 1.5 if exitValue == 0 \
            else 10 ** (math.log10(1.0 * exitValue / valuation) / numFutureRounds)

        # print(ticket, allocation)
        return valuation, roundSize, allocation, ticket

    def generateFollowOnTicket(self, r: Round):
        """ Calculate pro-rata ticket size while constraining by:
            1) Max investable capital available,
            2) Max concentration by portfolio company, and
            3) Cuttoff maximum src valuation allowed to invest
        """

        if not self.shouldFollowOn(r):
            return 0, r.putTicket(0)

        # Calculate simple prorata
        proRataTicket = 1.0 * r.portco.lastOwnershipStake * r.roundSize

        # If current ownership is below ownership target, up ticket to hit target ownership
        if r.portco.lastOwnershipStake < self.target_ownership:
            proRataTicket += (self.target_ownership - r.portco.lastOwnershipStake) * r.valuation

        # check within follow-on ticket min and max values
        proRataTicket = max(proRataTicket, self.minimum_followon_ticket)
        proRataTicket = min(proRataTicket, self.maximum_followon_ticket)

        # Cap invested amount by:
        # a) cutoff on max valuation and b) available funds and c)max concentration limit per portfolio company
        proRataTicket = min(0 if r.valuation > self.max_valuation else proRataTicket,
                            self.fundParams.investable_capital - self.totalCapitalDeployed,
                            self.max_concentration - r.portco.totalInvested)

        newOwnershipStake = r.putTicket(proRataTicket)

        self.totalCapitalDeployed += proRataTicket
        self.followOnTickets += proRataTicket

        return proRataTicket, newOwnershipStake
