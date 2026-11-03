import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import ORDER, PARTITIONS, SPECIMENS_PATH, SPECIMENS_COLUMN
from fts_core import fuzzify, build_FLRG, forecast, triangular
from metrics import calculate_metrics

def run_specimens():
    # ======================================================
    # Step 1: Load dataset
    # ======================================================
    # Dynamically choose header based on the column requested
    # TOTAL SPECIMENS uses header=0, while A and B use header=1
    header_row = 0 if SPECIMENS_COLUMN == "TOTAL SPECIMENS" else 1
    df = pd.read_csv(SPECIMENS_PATH, header=header_row)

    df.columns = df.columns.str.strip()
    
    if SPECIMENS_COLUMN not in df.columns:
        raise ValueError(f"Column '{SPECIMENS_COLUMN}' not found in dataset. Available: {df.columns.tolist()}")

    values = pd.to_numeric(df[SPECIMENS_COLUMN], errors="coerce").values
    values = values[np.isfinite(values)]

    # ======================================================
    # Step 2: Normalize data
    # ======================================================
    vmin = values.min()
    vmax = values.max()

    values_norm = (values - vmin) / (vmax - vmin)

    # ======================================================
    # Step 3: Train / Test split
    # ======================================================
    n = len(values_norm)
    cut = int(0.8 * n)

    train = values_norm[:cut]
    test  = values_norm[cut:]

    print("Train size:", len(train))
    print("Test size :", len(test))

    # ======================================================
    # Step 4: Universe of discourse (normalized)
    # ======================================================
    Umin, Umax = 0.0, 1.0
    m = PARTITIONS

    intervals = np.linspace(Umin, Umax, m + 1)
    midpoints = (intervals[:-1] + intervals[1:]) / 2

    print("Universe:", Umin, "-", Umax)
    print("Midpoints:", midpoints)

    # ======================================================
    # Step 6: Fuzzification
    # ======================================================
    train_labels = fuzzify(train, intervals, midpoints, shape="triangular")
    test_labels  = fuzzify(test, intervals, midpoints, shape="triangular")

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
    pred_norm = forecast(test_labels, FLRG, midpoints, ORDER)

    # ======================================================
    # Step 9: Predictions (Denormalize)
    # ======================================================
    pred = pred_norm * (vmax - vmin) + vmin
    actual = test[ORDER:] * (vmax - vmin) + vmin

    # ======================================================
    # Step 10: Error metrics
    # ======================================================
    rmse, mae, mape = calculate_metrics(actual, pred)

    print("\nPerformance:")
    print("RMSE:", rmse)
    print("MAE :", mae)
    print("MAPE:", mape, "%")

    # ======================================================
    # Step 11: Plots
    # ======================================================
    plt.figure(figsize=(8,4))
    plt.plot(actual, label="Actual", marker='o')
    plt.plot(pred, label="Predicted", marker='x')
    plt.title(f"FTS Forecasting – {SPECIMENS_COLUMN} (Order={ORDER})")
    plt.xlabel("Test sample index")
    plt.ylabel("Specimen count")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"results/specimens_{SPECIMENS_COLUMN.replace(' ', '_')}_order_{ORDER}.png", dpi=150, bbox_inches='tight')
    plt.close()

    xs = np.linspace(Umin, Umax, 500)
    plt.figure(figsize=(8,4))

    for j in range(len(midpoints)):
        ys = []
        for x in xs:
            mu = triangular(
                x,
                intervals[j],        # left base
                midpoints[j],        # peak
                intervals[j + 1]     # right base
            )
            ys.append(mu)
        plt.plot(xs, ys, label="A" + str(j+1))

    plt.title("Triangular Membership Functions")
    plt.xlabel("Universe of Discourse")
    plt.ylabel("Membership Degree")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("results/specimens_membership_functions.png", dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    import os
    os.makedirs("results", exist_ok=True)
    run_specimens()