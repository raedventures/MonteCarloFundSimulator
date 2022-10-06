import datetime

from src.portco import Portco


class Round:
    def __init__(self, portco: Portco, roundNumber: int, roundDate: datetime, valuation: int, roundSize: int, ticket: int,
                 ownershipStakePostRound: float):
        self.portco = portco
        self.roundNumber = roundNumber
        self.roundDate = roundDate
        self.valuation = valuation
        self.roundSize = roundSize
        self.ticket = ticket
        self.ownershipStakePostRound = ownershipStakePostRound

    def putTicket(self, amount: float):
        self.portco.totalInvested += amount
        self.ticket = amount
        self.portco.lastOwnershipStake = self.ownershipStakePostRound = self.calculateNewOwnershipStake(amount)
        return self.ownershipStakePostRound

    def calculateNewOwnershipStake(self, amount: float):
        return self.portco.lastOwnershipStake * (1 - 1.0 * self.roundSize / self.valuation) + amount / self.valuation

    def __str__(self):
        return " company:" + str(self.portco.name) + \
               " type:" + str(self.portco.type.name) + \
               " date:" + str(self.roundDate) + \
               " roundNum:" + str(self.roundNumber) + \
               " valuation:" + str(round(self.valuation)) + \
               " roundSize:" + str(round(self.roundSize)) + \
               " ticket:" + str(round(self.ticket)) + \
               " stake:" + str(round(self.ownershipStakePostRound, 4))
