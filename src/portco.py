class Portco:

    def __init__(self, portcoNum: int, portCoName: str, outcomeType):
        self.num = portcoNum
        self.name = portCoName
        self.type = outcomeType
        self.totalRaised = 0.0
        self.totalInvested = 0.0
        self.lastValuation = 0.0
        self.lastOwnershipStake = 0.0
        self.initialInvestmentDate = 0
        self.avgRoundMultiple = 1.5

    def __str__(self):
        return "name:" + self.name + \
               " type:" + str(self.type.name) + \
               " valuation:" + str(self.lastValuation) + \
               " raised:" + str(self.totalRaised) + \
               " invested:" + str(self.totalInvested) + \
               " stake:" + str(self.lastOwnershipStake) + \
               " roundMult: " + str(round(self.avgRoundMultiple,2))
