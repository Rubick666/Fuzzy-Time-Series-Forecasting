import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import ORDER, PARTITIONS, MACKEY_GLASS_PATH
from fts_core import fuzzify, build_FLRG, forecast, gaussian
from metrics import calculate_metrics

def run_mackey_glass():
    # ======================================================
    # Step 1: Load dataset
    # ======================================================
    df = pd.read_csv(MACKEY_GLASS_PATH)
    values = df["value"].values

    # ======================================================
    # Step 2: Train / Test split (80% / 20%)
    # ======================================================
    n = len(values)
    cut = int(0.8 * n)

    train = values[:cut]
    test  = values[cut:]

    print("Train size:", len(train))
    print("Test size :", len(test))

    # ======================================================
    # Step 3: Scaling
    # ======================================================
    scale = 10000
    train_s = (train*scale).astype(int)
    test_s = (test*scale).astype(int)

    dmin, dmax = train_s.min(), test_s.max()
    Umin = (dmin//1000)*1000   # round down
    Umax = ((dmax//1000)+1)*1000  # round up

    m = PARTITIONS
    intervals = np.linspace(Umin, Umax, m+1).astype(int)
    midpoints = ((intervals[:-1] + intervals[1:])//2).astype(int)

    print("Universe:", Umin, "-", Umax)
    print("Intervals:", intervals)
    print("Midpoints:", midpoints)

    # ======================================================
    # Step 6: Fuzzification
    # ======================================================
    train_labels = fuzzify(train_s, intervals, midpoints, shape="gaussian")
    test_labels  = fuzzify(test_s, intervals, midpoints, shape="gaussian")

    # ======================================================
    # Step 7: Build FLRGs
    # ======================================================
    FLRG = build_FLRG(train_labels, ORDER)

    print("\nFLRGs:")
    for k, v in FLRG.items():
        print(k, "->", v)

    # ======================================================
    # Step 8: Forecasting
    # ======================================================
    pred_scaled = forecast(test_labels, FLRG, midpoints, ORDER)

    # ======================================================
    # Step 9: Error metrics
    # ======================================================
    actual = test_s[ORDER:]
    
    # We pass scale to return RMSE and MAE to original units
    rmse, mae, mape = calculate_metrics(actual, pred_scaled, scale=scale)

    print("\nPerformance:")
    print("RMSE:", rmse)
    print("MAE :", mae)
    print("MAPE:", mape, "%")

    # ======================================================
    # Step 10: Plot prediction
    # ======================================================
    plt.figure(figsize=(8,4))
    plt.plot(actual, label="Actual", marker='o')
    plt.plot(pred_scaled, label="Predicted", marker='x')
    plt.title(f"FTS Forecasting (Order = {ORDER})")
    plt.xlabel("Test sample index")
    plt.ylabel("Scaled value")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"results/mackey_glass_prediction_order_{ORDER}.png", dpi=150, bbox_inches='tight')
    plt.close()

    # ======================================================
    # Step 11: Plot membership functions
    # ======================================================
    xs = np.linspace(Umin, Umax, 500)
    plt.figure(figsize=(8,4))

    for j in range(len(midpoints)):
        ys = []
        for x in xs:
            sigma = (intervals[j+1] - intervals[j]) / 2
            ys.append(gaussian(x, midpoints[j], sigma))
        plt.plot(xs, ys, label="A" + str(j+1))

    plt.title("Gaussian Membership Functions")
    plt.xlabel("Universe")
    plt.ylabel("Membership degree")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("results/mackey_glass_membership_functions.png", dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    import os
    os.makedirs("results", exist_ok=True)
    run_mackey_glass()