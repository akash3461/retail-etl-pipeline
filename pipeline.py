import pandas as pd
from pathlib import Path
import logging


# Project paths

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "Data"
OUTPUT_DIR = BASE_DIR / "Output"
LOG_DIR = BASE_DIR / "logs"


# Logging setup

LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

#Load the dataset(Extract)
logger.info("Data loading started")
df = pd.read_csv(DATA_DIR / "Data.csv", encoding="cp1252")
logger.info("Dataset loaded successfully.")
logger.info(f"row count: {df.shape[0]}, column count: {df.shape[1]}")
logger.info(f"column names: {df.columns.tolist()}")
# Data Inspection
logger.info("Data inspection started")
 
print(df.head())   # Display first few rows
print(df.columns)  # Display column names
print(df.describe())  # Display summary statistics
print(df.info())     # Display information about the dataset
print(df.isnull().sum())  # Display count of missing values in each column
print(df.duplicated().sum())  # Display count of duplicate rows

#=========================================================================
#Data Cleaning and Transformation

before_duplicates = len(df)

df.drop_duplicates(inplace = True) 

after_duplicates = len(df)
logger.info(f"Removed {before_duplicates - after_duplicates} duplicate rows. Remaining rows: {after_duplicates}")



missing_description =df["Description"].isna().sum()
df["Description"] = df["Description"].fillna("Unknown")

logger.info(f"Handeled {missing_description} missing Discription values"
            )

#Converting invoice date into datetime format
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors='coerce')
invalid_dates = df["InvoiceDate"].isna().sum()

logger.info(f"invalid dates after conversion:{invalid_dates}")

#handling negative prices

negative_prices = (df["UnitPrice"] < 0).sum()
df = df[df["UnitPrice"] >= 0]
logger.info(f"Removed {negative_prices} rows with negative prices. Current rows: {len(df)}")

# Create new column of total amount and for important date (year,month,day)

df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]

df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["Day"] = df["InvoiceDate"].dt.day

logger.info("New column added")
logger.info(f"Final row count: {df.shape[0]}, column count: {df.shape[1]}")

print("\nData Cleaning Completed.")
print(f"Final row count: {df.shape[0]}, column count: {df.shape[1]}")
print(df.head())  # Display first few rows after cleaning


#=========================================================================
#=================VALIDATION OF DATA======================================

logger.info("Data validation started") 
validation_errors = [] 
 
# Define scalar checks
scalar_checks = [ 
    ("Duplicate rows", df.duplicated().sum(), "duplicate rows found"), 
    ("UnitPrice", (df["UnitPrice"] < 0).sum(), "negative UnitPrice values found"), 
    ("InvoiceDate", df["InvoiceDate"].isna().sum(), "invalid InvoiceDate values found"), 
    ("TotalAmount", (df["TotalAmount"] != df["Quantity"] * df["UnitPrice"]).sum(), "incorrect TotalAmount values found"), 
] 
 
# Run numeric checks 
for label, count, err_msg in scalar_checks: 
    if count > 0: 
        validation_errors.append(f"{count} {err_msg}") 
    else: 
        logger.info(f"{label} check passed") 
 
# Check missing values dictionary 
if missing_dict := df.isnull().sum().loc[lambda x: x > 0].to_dict(): 
    validation_errors.append(f"Missing values found: {missing_dict}") 
else: 
    logger.info("Missing value check passed") 
 
# Check required columns via set difference 
required_cols = {"InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country", "TotalAmount", "Year", "Month", "Day"} 
if missing_cols := required_cols - set(df.columns): 
    validation_errors.append(f"Missing required columns: {list(missing_cols)}") 
else: 
    logger.info("Required column check passed") 
 
# Output Summary 
status = "completed with warnings" if validation_errors else "passed successfully" 
logger.warning(f"Data validation {status}") if validation_errors else logger.info(f"Data validation {status}") 
 
print(f"\n==============================\nDATA VALIDATION {status.upper()}\n==============================") 
print(f"Rows: {len(df)} | Columns: {len(df.columns)}") 
if validation_errors: 
    print("\n".join(f"- {err}" for err in validation_errors)) 

#Data Optimization
logger.info("Data optimization started")

# ============================================================
# Step 8: Data Optimization
# ============================================================

logger.info("Data optimization started")

# ------------------------------------------------------------
# 8.1 Check memory usage before optimization
# ------------------------------------------------------------

memory_before = df.memory_usage(deep=True).sum() / (1024 ** 2)

print("\nMemory usage before optimization:")
print(f"{memory_before:.2f} MB")

logger.info(
    f"Memory usage before optimization: {memory_before:.2f} MB"
)


# ------------------------------------------------------------
# 8.2 Optimize numeric data types
# ------------------------------------------------------------

df["Quantity"] = pd.to_numeric(
    df["Quantity"],
    downcast="integer"
)

df["UnitPrice"] = pd.to_numeric(
    df["UnitPrice"],
    downcast="float"
)

df["CustomerID"] = pd.to_numeric(
    df["CustomerID"],
    downcast="float"
)


# ------------------------------------------------------------
# 8.3 Optimize categorical column
# ------------------------------------------------------------

df["Country"] = df["Country"].astype("category")


# ------------------------------------------------------------
# 8.4 Check memory usage after optimization
# ------------------------------------------------------------

memory_after = df.memory_usage(deep=True).sum() / (1024 ** 2)

print("\nMemory usage after optimization:")
print(f"{memory_after:.2f} MB")


# ------------------------------------------------------------
# 8.5 Calculate memory reduction
# ------------------------------------------------------------

memory_reduced = memory_before - memory_after

reduction_percentage = (
    (memory_reduced / memory_before) * 100
)

print(f"\nMemory reduced: {memory_reduced:.2f} MB")
print(f"Memory reduction: {reduction_percentage:.2f}%")


# ------------------------------------------------------------
# 8.6 Log optimization results
# ------------------------------------------------------------

logger.info(
    f"Memory usage after optimization: {memory_after:.2f} MB"
)

logger.info(
    f"Memory reduced by: {memory_reduced:.2f} MB "
    f"({reduction_percentage:.2f}%)"
)

logger.info("Data optimization completed")

print("\nData optimization completed successfully.")

# Step 8: Memory Optimization
logger.info("Starting memory optimization")

mem_before = df.memory_usage(deep=True).sum() / 1024**2

# Optimize types
df["Quantity"] = pd.to_numeric(df["Quantity"], downcast="integer")
df["UnitPrice"] = df["UnitPrice"].astype("float32")
df["TotalAmount"] = df["TotalAmount"].astype("float32")
df["CustomerID"] = df["CustomerID"].astype("Int32")  # Keeps IDs as ints while supporting NaNs

df["Country"] = df["Country"].astype("category")
df["Description"] = df["Description"].astype("category")

mem_after = df.memory_usage(deep=True).sum() / 1024**2
reduction = ((mem_before - mem_after) / mem_before) * 100

print(f"Memory: {mem_before:.2f} MB → {mem_after:.2f} MB ({reduction:.1f}% saved)")
logger.info(f"Memory optimized from {mem_before:.2f} MB to {mem_after:.2f} MB ({reduction:.1f}% reduction)")


# Loading into The parquet file (Load)
logger.info("Data loading into parquet file started")

output_file = OUTPUT_DIR / "Clean_ecommerce_data.parquet"
try:
    df.to_parquet(output_file, index=False, engine='pyarrow', compression='snappy')
    size = output_file.stat().st_size / (1024 ** 2)  # Size in MB

    print(f"Parquet data saved to {output_file} ({size:.2f} Mb)")
    logger.info(f"Parquet data saved to {output_file} ({size:.2f})Mb")

except Exception as e:
    logger.error(f"Failed to save parquet file: {e}")
    print(f"failed to save The Parquet file : {e}")

    