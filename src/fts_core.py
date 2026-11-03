import numpy as np

# ======================================================
# Membership functions
# ======================================================
def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif x == b:
        return 1
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)

def gaussian(x, mean, sigma):
    return np.exp(-0.5 * ((x - mean) / sigma) ** 2)

# ======================================================
# Fuzzification
# ======================================================
def fuzzify(series, intervals, midpoints, shape="gaussian"):
    labels = []
    for v in series:
        memberships = []
        for j in range(len(midpoints)):
            if shape == "triangular":
                mu = triangular(v, intervals[j], midpoints[j], intervals[j+1])
            else:
                sigma = (intervals[j+1] - intervals[j]) / 2
                mu = gaussian(v, midpoints[j], sigma)
            memberships.append(mu)
        labels.append("A" + str(np.argmax(memberships) + 1))
    return labels

# ======================================================
# Build FLRGs (FOFTS or HOFTS)
# ======================================================
def build_FLRG(labels, order):
    FLRG = {}
    for i in range(len(labels) - order):
        antecedent = tuple(labels[i:i+order])
        consequent = labels[i+order]
        if antecedent not in FLRG:
            FLRG[antecedent] = []
        if consequent not in FLRG[antecedent]:
            FLRG[antecedent].append(consequent)
    return FLRG

# ======================================================
# Forecasting
# ======================================================
def forecast(labels, FLRG, midpoints, order):
    preds = []
    for i in range(len(labels) - order):
        antecedent = tuple(labels[i:i+order])
        consequents = FLRG.get(antecedent, [])

        if len(consequents) == 0:
            idx = int(antecedent[-1][1:]) - 1
            preds.append(midpoints[idx])
        else:
            values = []
            for c in consequents:
                idx = int(c[1:]) - 1
                values.append(midpoints[idx])
            preds.append(np.mean(values))
    return np.array(preds)