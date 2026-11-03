import numpy as np

def calculate_metrics(actual, pred, scale=1.0):
    """
    Calculates RMSE, MAE, and MAPE.
    - scale: if data was scaled up (e.g., Mackey-Glass by 10000), divide by scale to return to original units.
    """
    rmse = np.sqrt(np.mean((actual - pred) ** 2)) / scale
    mae = np.mean(np.abs(actual - pred)) / scale
    
    # Avoid division by zero in MAPE
    mape = np.mean(np.abs((actual - pred) / (actual + 1e-8))) * 100
    
    return rmse, mae, mape