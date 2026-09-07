# Retail Transaction ETL & Optimization Pipeline

This project is a Python-based Data Engineering pipeline built using a retail transaction dataset.

The pipeline takes raw CSV data, cleans and transforms it, performs data quality checks, optimizes data types to reduce memory usage, and finally stores the processed data in Parquet format.

The main purpose of this project was to get hands-on experience with the fundamentals of an ETL workflow and understand how raw data is prepared for further analysis and data engineering tasks.

---

## Architecture & Data Flow

```text
┌───────────┐      ┌──────────────────────┐      ┌─────────────────────────────┐      ┌─────────────────────┐      ┌─────────────────┐
│  Raw CSV  │ ───► │ Ingestion & Cleaning │ ───► │ Transformation & Validation │ ───► │ Memory Optimization │ ───► │ Parquet Storage │
└───────────┘      └──────────────────────┘      └─────────────────────────────┘      └─────────────────────┘      └─────────────────┘
                                                                                                   │
                                                                                                   └──► pipeline.log
```

---

## What the Pipeline Does

### 1. Data Ingestion

Loads the raw CSV dataset using Pandas.

The dataset uses `cp1252` encoding because the source file contains special characters such as the `£` symbol.

### 2. Data Inspection

The pipeline inspects:

- Dataset shape
- Column names
- Data types
- Statistical summary
- Missing values
- Duplicate records

### 3. Data Cleaning

The pipeline:

- Removes duplicate rows
- Handles missing product descriptions
- Converts `InvoiceDate` from string to datetime
- Removes invalid negative `UnitPrice` records

### 4. Negative Values

Negative `Quantity` values are retained because they can represent returned or cancelled transactions.

Negative `UnitPrice` values are removed because they were treated as invalid pricing records for this project.

### 5. Feature Engineering

The pipeline creates:

- `TotalAmount` = `Quantity × UnitPrice`
- `Year` extracted from `InvoiceDate`
- `Month` extracted from `InvoiceDate`
- `Day` extracted from `InvoiceDate`

### 6. Data Validation

The pipeline performs checks for:

- Duplicate records
- Negative `UnitPrice`
- Invalid `InvoiceDate`
- Incorrect `TotalAmount` calculations
- Missing values
- Required columns

### 7. Memory Optimization

The pipeline optimizes DataFrame memory usage by using more appropriate data types.

Examples include:

- Downcasting `Quantity`
- Converting `UnitPrice` to `float32`
- Converting `TotalAmount` to `float32`
- Converting `CustomerID` to nullable `Int32`
- Converting `Country` to `category`
- Converting `Description` to `category`

### 8. Parquet Output

The cleaned and optimized dataset is saved as a Parquet file for efficient analytical storage.

### 9. Logging

The pipeline uses Python's `logging` module to record important execution events and results in `pipeline.log`.

---

## Pipeline Benchmarks & Metrics

| Metric | Raw Data | Processed Data | Result |
|---|---:|---:|---|
| Storage Format | CSV | Parquet | Columnar format |
| Rows | 541,909 | 536,639 | 5,268 duplicates + 2 invalid price rows removed |
| Columns | 8 | 12 | 4 new derived columns |
| DataFrame Memory* | 58.89 MB | 38.71 MB | 34.3% reduction |
| Parquet File Size | — | 4.26 MB | Final processed output |

\*Memory figures represent the DataFrame memory measured during the optimization stage of the pipeline.

---

## Row Processing

The original dataset contained:

**541,909 rows**

During the cleaning process:

- **5,268 duplicate rows** were removed.
- **2 rows with negative `UnitPrice` values** were removed.
- Negative `Quantity` values were retained because they can represent returns or cancelled transactions.

The final row count was:

```text
541,909
- 5,268 duplicates
-     2 invalid UnitPrice rows
------------------------------
536,639 final rows
```

The final dataset contains:

- **536,639 rows**
- **12 columns**

---

## Memory Optimization

During the memory optimization stage, DataFrame memory usage was reduced from:

```text
58.89 MB → 38.71 MB
```

This represents a:

```text
34.3% memory reduction
```

The optimization included:

- Downcasting `Quantity`
- Converting `UnitPrice` to `float32`
- Converting `TotalAmount` to `float32`
- Converting `CustomerID` to nullable `Int32`
- Converting `Country` to `category`
- Converting `Description` to `category`

Memory optimization helps reduce the amount of RAM required when processing larger datasets.

---

## Project Structure

```text
retail-etl-pipeline/
│
├── Data/
│   └── Data.csv
│
├── Output/
│   └── Clean_ecommerce_data.parquet
│
├── logs/
│   └── pipeline.log
│
├── docs/
│   └── architecture.png
│
├── pipeline.py
├── requirements.txt
├── .gitignore
└── README.md
```

> The raw dataset and generated output files should be excluded from GitHub using `.gitignore`.

---

## Technologies Used

- **Python**
- **Pandas**
- **PyArrow**
- **Apache Parquet**
- **Git**
- **GitHub**

---

## Repository and Dataset

### Project Repository

[Retail Transaction ETL & Optimization Pipeline](https://github.com/akash3461/retail-etl-pipeline)

### Source Dataset

[E-commerce Data — Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data)

The project uses the **Online Retail** dataset.

The downloaded CSV file should be placed inside the project as:

```text
Data/Data.csv
```

---

## Download the Dataset with KaggleHub

The dataset can also be downloaded using KaggleHub.

Install KaggleHub:

```bash
pip install kagglehub
```

Then run:

```python
import kagglehub

path = kagglehub.dataset_download("carrie1/ecommerce-data")

print("Path to dataset files:", path)
```

Copy the downloaded CSV file to the project's `Data` folder and rename it to:

```text
Data.csv
```

The final location should be:

```text
retail-etl-pipeline/
└── Data/
    └── Data.csv
```

---

## Getting Started

### Prerequisites

Make sure the following are installed:

- Python 3.9 or higher
- pip
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/akash3461/retail-etl-pipeline.git

cd retail-etl-pipeline
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

---

### 3. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

The main dependencies are:

```text
pandas
pyarrow
```

---

### 5. Add the Dataset

Place the downloaded CSV file at:

```text
Data/Data.csv
```

---

### 6. Run the Pipeline

```bash
python pipeline.py
```

After successful execution:

- The processed Parquet file will be created in `Output/`
- Pipeline logs will be created in `logs/`

Expected output structure:

```text
Output/
└── Clean_ecommerce_data.parquet

logs/
└── pipeline.log
```

---

## Data Validation

The pipeline performs several data quality checks before generating the final output.

### Duplicate Check

Checks whether duplicate records remain after cleaning.

### Negative Price Check

Checks whether any negative `UnitPrice` values remain.

### Invoice Date Check

Checks for invalid or unconvertible `InvoiceDate` values.

### Total Amount Check

Verifies that:

```text
TotalAmount = Quantity × UnitPrice
```

### Missing Value Check

Checks for remaining missing values.

`CustomerID` can contain missing values in the original dataset. These records were intentionally retained rather than removing the corresponding transactions.

### Required Column Check

Checks whether all expected columns are present before completing the pipeline.

---

## Pipeline Logging

The pipeline uses Python's built-in `logging` module to record important execution events.

The log file is stored at:

```text
logs/pipeline.log
```

Example log events:

```text
Data loading started

Dataset loaded successfully

Data cleaning and transformation started

Removed 5268 duplicate rows

Handled missing Description values

Created TotalAmount column

Created Year, Month and Day columns

Data validation completed

Starting memory optimization

Parquet file saved successfully
```

The actual timestamps and messages depend on each pipeline execution.

---

## Why Parquet?

The final processed dataset is stored in Parquet instead of CSV.

Parquet is a columnar storage format commonly used for analytical workloads.

Some advantages include:

- Efficient column-based storage
- Better preservation of data types
- Smaller storage footprint
- Faster analytical reads for selected columns
- Compatibility with many Data Engineering and analytics tools

The final Parquet file generated by this pipeline was approximately:

```text
4.26 MB
```

---

## ETL Workflow

The complete workflow implemented in this project is:

```text
Extract
   ↓
Inspect
   ↓
Clean
   ↓
Transform
   ↓
Validate
   ↓
Optimize
   ↓
Load
```

In practical terms:

```text
Raw CSV
   ↓
Pandas DataFrame
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Data Validation
   ↓
Memory Optimization
   ↓
Parquet
```

---

## What I Learned

This project helped me understand the fundamentals of a Data Engineering ETL pipeline by working with a real-world retail transaction dataset.

Through this project, I practiced:

- Loading data with Pandas
- Inspecting a dataset
- Understanding data types
- Handling missing values
- Removing duplicate records
- Handling negative transaction values
- Converting dates
- Creating derived columns
- Performing data validation
- Optimizing DataFrame memory usage
- Working with Parquet
- Adding logging
- Structuring a Data Engineering project
- Using Git and GitHub

The main lesson from this project was that an ETL pipeline is not just about moving data from one place to another.

The data needs to be:

**Clean → Validated → Correctly Typed → Optimized → Stored**

before it is ready for downstream analysis or further processing.

---

## Future Improvements

This project currently focuses on the fundamentals of a batch ETL pipeline.

Possible future improvements include:

- Automated data quality tests
- Unit tests
- Configuration files
- PostgreSQL integration
- Incremental data processing
- Airflow scheduling
- Cloud storage
- CI/CD pipeline
- Containerization with Docker

These improvements can be explored in later Data Engineering projects.

---

## Author

Built as part of my **100-Day Data Engineering learning journey**.

The project focuses on learning the fundamentals of:

**Python → ETL → Data Quality → Optimization → Parquet → Git/GitHub**

---

## License

This project is created for learning and portfolio purposes.