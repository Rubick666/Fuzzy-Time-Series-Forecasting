import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# FTS Configuration
# -----------------------------
ORDER = int(os.getenv("ORDER", 2))          # 1 = FOFTS, 2 = HOFTS
PARTITIONS = int(os.getenv("PARTITIONS", 8)) # Number of fuzzy sets/intervals
TRAIN_SPLIT = float(os.getenv("TRAIN_SPLIT", 0.8))

# Dataset paths (adjust if your folder structure differs)
MACKEY_GLASS_PATH = os.getenv("MACKEY_GLASS_PATH", "mackey_glass.csv")
SPECIMENS_PATH = os.getenv("SPECIMENS_PATH", "Specimens.csv")
SPECIMENS_COLUMN = os.getenv("SPECIMENS_COLUMN", "TOTAL SPECIMENS")