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
from pathlib import Path

# Repo root = directory that contains the "notebooks" folder (parent of this notebook's parent).
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
repo_root = str(Path(notebook_path).parent.parent)
# Some workspaces report paths as /Workspace/<username>/... but the real path is /Workspace/Users/<username>/...
# Normalize so we use the actual workspace layout (insert "Users" if missing).
parts = repo_root.split("/")
if len(parts) >= 3 and parts[1] == "Workspace" and parts[2] != "Users":
    repo_root = "/Workspace/Users/" + "/".join(parts[2:])
os.chdir(repo_root)

# Skip writing pyc files on a readonly filesystem.
sys.dont_write_bytecode = True

retcode = pytest.main([".", "-p", "no:cacheprovider", "-v"])

# Fail the cell execution if we have any test failures.
assert retcode == 0, 'The pytest invocation failed. See the log above for details.'
