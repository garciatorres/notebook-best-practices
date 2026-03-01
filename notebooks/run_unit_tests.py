# Databricks notebook source
# MAGIC %md Test runner for `pytest`

# COMMAND ----------

# Install dependencies (requirements.txt at bundle root, one level up from notebooks/)
# MAGIC %pip install -r ../requirements.txt

# COMMAND ----------

# pytest.main runs our tests directly in the notebook environment.
# Restart Python to clear import cache when iterating on tests.
dbutils.library.restartPython()

# COMMAND ----------

import pytest
import os
import sys

# Run all tests from the project root (parent of notebooks/)
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
# Workspace path like /Workspace/Users/.../notebook-best-practices-bundle/notebooks/run_unit_tests
# or repo root when running locally
parts = notebook_path.split('/')
if 'notebooks' in parts:
    idx = parts.index('notebooks')
    repo_root = '/Workspace/' + '/'.join(parts[2:idx])
else:
    repo_root = os.getcwd()
os.chdir(repo_root)

# Skip writing pyc files on a readonly filesystem.
sys.dont_write_bytecode = True

retcode = pytest.main([".", "-p", "no:cacheprovider", "-v"])

# Fail the cell execution if we have any test failures.
assert retcode == 0, 'The pytest invocation failed. See the log above for details.'
