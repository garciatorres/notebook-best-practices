# Databricks Notebook Best Practices — COVID EDA

This project is based on the Microsoft Learn article **[Software engineering best practices for notebooks (Azure Databricks)](https://learn.microsoft.com/en-us/azure/databricks/notebooks/best-practices)**. It demonstrates version-controlled notebooks, shared Python modules, unit tests, and automated runs via a **Databricks Asset Bundle (DAB)**.

## What’s in this repo

- **Notebooks**: Raw EDA (`covid_eda_raw`), modular EDA using shared code (`covid_eda_modular`), and a test runner (`run_unit_tests`).
- **Shared module**: `covid_analysis/transforms.py` with reusable transform functions.
- **Tests**: `tests/` with pytest and sample data for the transforms.
- **Bundle**: `databricks.yml` defines a job that runs unit tests first, then the main EDA notebook.

Technologies: **Databricks**, **Python**, **pandas**, **PySpark**, **pytest**, **Databricks Asset Bundles**.

---

## Prerequisites

- A **Databricks workspace** (Azure Databricks or Databricks on AWS/GCP).
- **Databricks CLI** installed and configured (e.g. `databricks configure` or profile in `~/.databrickscfg`).
- **Git** (for pushing to your GitHub account).

### Cloud-agnostic targets

The bundle is cloud-agnostic. Choose the target that matches your workspace:

| Target   | Use for        | Node type / config      |
|----------|----------------|--------------------------|
| **dev**  | Databricks on **AWS** (default) | `m5.large` + EBS volume |
| **azure**| **Azure** Databricks           | `Standard_DS3_v2`       |

- **AWS**: `databricks bundle deploy` (default) or `databricks bundle deploy -t dev`
- **Azure**: `databricks bundle deploy -t azure`

---

## Step-by-step: Run the project

### 1. Clone or use this folder

If you already have the repo locally:

```bash
cd notebook-best-practices
```

Otherwise clone from your GitHub (after you’ve pushed, see “Deploy to your GitHub” below):

```bash
git clone https://github.com/garciatorres/notebook-best-practices.git
cd notebook-best-practices
```

### 2. Configure the Databricks CLI (if needed)

Ensure the CLI can talk to your workspace:

```bash
databricks configure
# Or use a profile: databricks configure --profile myprofile
```

Use the same profile in the next steps if you configured one (e.g. `--profile myprofile`).

### 3. Validate the bundle

From the project root (where `databricks.yml` lives):

```bash
databricks bundle validate
```

Fix any reported errors before deploying.

### 4. Deploy the bundle

Deploy to the default target (e.g. `dev`). This syncs the project to your workspace and creates/updates the job:

```bash
databricks bundle deploy
```

When prompted, confirm. After deployment, notebooks and the `covid_analysis` module will be under the workspace path defined in `databricks.yml` (e.g. `/Workspace/Users/<you>/notebook-best-practices-bundle/`).

### 5. Run the job (tests + main notebook)

Trigger the bundle job that runs unit tests then the COVID EDA notebook:

```bash
databricks bundle run covid_report
```

Or run the same job from the Databricks UI: **Workflows → Jobs → “[dev] COVID Report (tests + EDA)”** → **Run now**.

- The **first task** runs `notebooks/run_unit_tests.py` (pytest on `covid_analysis.transforms`).
- The **second task** runs `notebooks/covid_eda_modular.py` (fetch data, transform, write Delta table `covid_stats`).

### 6. Run notebooks interactively (optional)

1. In the workspace, go to **Workspace** and open the bundle folder (e.g. `notebook-best-practices-bundle` under your user).
2. Attach a cluster to `notebooks/covid_eda_raw.py` or `notebooks/covid_eda_modular.py`.
3. Run cells to explore or modify the EDA.

---

## Deploy to your GitHub

1. Create a **new repository** on GitHub (e.g. `notebook-best-practices`). Do not add a README if you’re pushing this repo.

2. From the project root:

   ```bash
   git init
   git add .
   git commit -m "Initial commit: notebook best practices bundle (COVID EDA)"
   git remote add origin https://github.com/garciatorres/notebook-best-practices.git
   git branch -M main
   git push -u origin main
   ```

3. This pushes to **garciatorres**. Use SSH if you prefer: `git@github.com:garciatorres/notebook-best-practices.git`.

---

## Project layout

```
notebook-best-practices/
├── databricks.yml          # Bundle config and job definition
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── covid_analysis/         # Shared module
│   ├── __init__.py
│   └── transforms.py
├── notebooks/
│   ├── covid_eda_raw.py       # In-notebook EDA (USA)
│   ├── covid_eda_modular.py   # EDA using covid_analysis (e.g. DZA)
│   └── run_unit_tests.py      # Pytest runner
└── tests/
    ├── testdata.csv
    └── transforms_test.py
```

---

## Reference

- **Source article**: [Software engineering best practices for notebooks - Azure Databricks | Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/notebooks/best-practices)
- **Databricks Asset Bundles**: [Bundle documentation](https://docs.databricks.com/dev-tools/bundles/)
- **COVID-19 data**: [OWID COVID-19 Data](https://github.com/owid/covid-19-data) (hospitalizations CSV used by the notebooks)
