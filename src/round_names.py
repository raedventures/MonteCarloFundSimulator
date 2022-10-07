from enum import Enum


class RoundNames(Enum):
    PreSeed = 1,
    Seed = 2,
    SeriesA = 3,
    SeriesB = 4,
    SeriesC = 5,
    SeriesD = 6,
    SeriesE = 7

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
    (25000000, 0.20),
    (90000000, 0.20),
    (250000000, 0.20),
    (500000000, 0.18),
    (1000000000, 0.17),
    (2000000000, 0.15),
    (6000000000, 0.13),
)
