# Retail Transaction ETL & Optimization Pipeline

This project is a Python-based Data Engineering pipeline built using a retail transaction dataset.

The pipeline takes raw CSV data, cleans and transforms it, performs data quality checks, optimizes the data types to reduce memory usage, and finally stores the processed data in Parquet format.

The main purpose of this project was to get hands-on experience with the basic ETL workflow and understand how raw data is prepared for further analysis and data engineering tasks.

---

## Architecture & Data Flow

```text
┌───────────┐      ┌──────────────────────┐      ┌─────────────────────────────┐      ┌─────────────────────┐      ┌─────────────────┐
│  Raw CSV  │ ───► │ Ingestion & Cleaning │ ───► │ Transformation & Validation │ ───► │ Memory Optimization │ ───► │ Parquet Storage │
└───────────┘      └──────────────────────┘      └─────────────────────────────┘      └─────────────────────┘      └─────────────────┘
                                                             │
                                                             └──► pipeline.log
```

## What the Pipeline Does

- **Data Ingestion:** Loads the raw CSV file using Pandas with `cp1252` encoding.
- **Data Inspection:** Checks the dataset structure, data types, missing values, and duplicate records.
- **Data Cleaning:** Removes duplicate rows, handles missing product descriptions, converts dates, and removes invalid negative `UnitPrice` values.
- **Negative Values:** Negative `Quantity` values are kept because they can represent returns or cancelled transactions. Negative `UnitPrice` values are removed because they were treated as invalid pricing records for this project.
- **Feature Engineering:** Creates `TotalAmount` using `Quantity × UnitPrice` and extracts `Year`, `Month`, and `Day` from `InvoiceDate`.
- **Data Validation:** Checks duplicates, invalid dates, negative prices, calculation errors, missing values, and required columns.
- **Memory Optimization:** Optimizes numeric and categorical columns to reduce the DataFrame's memory usage.
- **Parquet Output:** Saves the final processed dataset as a Parquet file.
- **Logging:** Records important pipeline events and results in `pipeline.log`.

---

## Pipeline Benchmarks & Metrics

| Metric | Raw Data | Processed Data | Result |
|---|---:|---:|---|
| Storage Format | CSV | Parquet | Columnar format |
| Rows | 541,909 | 536,639 | 5,268 duplicates + 2 invalid price rows removed |
| Columns | 8 | 12 | 4 new derived columns |
| Memory Usage | ~173.52 MB | ~89.06 MB | ~48.68% reduction |

### Row Processing

The original dataset contained **541,909 rows**.

During cleaning:

- **5,268 duplicate rows** were removed.
- **2 rows with negative `UnitPrice` values** were removed.
- Negative `Quantity` values were kept because they can represent returns or cancelled transactions.

Final row count:

```text
541,909
- 5,268 duplicates
-     2 invalid UnitPrice rows
------------------------------
536,639 final rows
```

### Memory Optimization

The DataFrame memory usage was reduced from approximately **173.52 MB to 89.06 MB**, which is a reduction of approximately **48.68%** in my run.

The optimization included:

- Downcasting `Quantity`
- Converting `UnitPrice` to `float32`
- Converting `TotalAmount` to `float32`
- Converting `CustomerID` to nullable `Int32`
- Converting `Country` to `category`
- Converting `Description` to `category`

---

## Project Structure

```text
retail-etl-pipeline/
│
├── Data/
│   └── Data.csv
│
├── Output/
│   └── clean_ecommerce_data.parquet
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

> The raw dataset and generated output files can be excluded from GitHub using `.gitignore` if required.

---

## Technologies Used

- Python
- Pandas
- PyArrow
- Parquet
- Git
- GitHub

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/retail-etl-pipeline.git
cd retail-etl-pipeline
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Run the pipeline:

```bash
python pipeline.py
```

After the pipeline finishes, the processed Parquet file will be available in the `Output` folder.

Pipeline execution logs will be available in the `logs` folder.

---

## Data Validation

The pipeline performs several checks before generating the final output:

- Duplicate row check
- Negative `UnitPrice` check
- Invalid `InvoiceDate` check
- `TotalAmount` calculation check
- Missing value check
- Required column check

The pipeline reports validation results in the terminal and stores execution information in the log file.

`CustomerID` can contain missing values in the original dataset, so these values were not removed during cleaning.

---

## Pipeline Logging

The pipeline uses Python's `logging` module to keep track of important events during execution.

Example:

```text
Data loading started
Dataset loaded successfully
Data cleaning and transformation started
Removed 5268 duplicate rows
Created TotalAmount column
Created Year, Month and Day columns
Data validation completed
Starting memory optimization
Parquet file saved successfully
```

The actual timestamps and messages depend on the pipeline run.

---

## Why Parquet?

The final data is stored in Parquet instead of CSV because Parquet is a columnar storage format that is well suited for analytical workloads.

It also preserves data types better than a plain CSV file and can be used easily with many data engineering and analytics tools.

---

## What I Learned

This project helped me understand the basic ETL process by actually working with a real-world style dataset.

I practiced:

- Loading and inspecting data with Pandas
- Cleaning messy data
- Handling missing values
- Working with duplicate records
- Handling negative transaction values
- Creating derived columns
- Validating data
- Optimizing DataFrame memory usage
- Working with Parquet
- Adding logging to a pipeline
- Organizing a Data Engineering project
- Using Git and GitHub

The overall workflow is:

**Extract → Transform → Validate → Optimize → Load**

---

## Future Improvements

Some things I would like to add to this project later:

- Automated data quality tests
- Unit tests
- Configuration files
- PostgreSQL integration
- Airflow scheduling
- Cloud storage
- CI/CD

---

## Author

Built as part of my **100-Day Data Engineering learning journey**.