from enum import Enum


class RoundNames(Enum):
    PreSeed = 1,
    Seed = 2,
    SeriesA = 3,
    SeriesB = 4,
    SeriesC = 5,
    SeriesD = 6,
    SeriesE = 7

    @staticmethod
    def getAvgDilution(valuation):
        """ Returns average dilution for a src at a certain valuation """
        for i in normalizedRound:
            if i[0] >= valuation:
                return i[1]


"""
A normalized stage attributes dictionary 
key: src name
value: a tuple containing the average src dilution for each valuation range
"""
normalizedRound = (
    (25_000_000, 0.20),
    (90_000_000, 0.20),
    (250_000_000, 0.20),
    (500_000_000, 0.18),
    (1_000_000_000, 0.17),
    (2_000_000_000, 0.15),
    (6_000_000_000, 0.13),
)
