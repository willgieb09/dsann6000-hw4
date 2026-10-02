import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import psutil

import duckdb

def compute_memory_usage(filepath=None):
  """
  Uses the `psutil` library to measure the total amount of RAM used by the
  current Python process, in MB. If the optional `filepath` argument is given,
  the amount is written out to a plaintext file (rounded to 2 decimal places).
  """
  process = psutil.Process()
  mem_usage_mb = process.memory_info().rss / (1024 ** 2)
  mem_usage_str = f'{mem_usage_mb:.2f} MB'
  if filepath:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as outfile:
      outfile.write(mem_usage_str)
  return mem_usage_mb

if __name__ == "__main__":
  memory_pre = compute_memory_usage('outputs/hw04-2-duckdb-pre.txt')
  print(f'{memory_pre:.2f} MB used pre-computation')
  s3_uri = 's3://dsan6000-data/acled_events.parquet'
  # Provided code for you: establishes an in-memory DuckDB database and installs
  # the httpfs extension, allowing direct queries of S3 buckets over HTTP
  con = duckdb.connect()
  con.execute("INSTALL httpfs;")
  con.execute("LOAD httpfs;")
  # Your code here: Use DuckDB to run a *single query* on the .parquet file at
  # the given S3 URI, generate the plot from the results as described in the
  # main notebook, then use plt.savefig() to export it as
  # yearly_fatalities_duckdb.svg
  
  yearly_count_query = """
  SELECT * FROM 's3://dsan6000-data/acled_events.parquet'
  LIMIT 5;
  """
  result_df = con.execute(yearly_count_query).df()
  print(result_df)
  
  memory_post = compute_memory_usage('outputs/hw04-2-duckdb-post.txt')
  print(f'{memory_post:.2f} MB used post-computation')
  memory_diff = memory_post - memory_pre
  print(f'=> {memory_diff:.2f} MB added via DuckDB operation')
  with open('outputs/hw04-2-duckdb-diff.txt', 'w', encoding='utf-8') as outfile:
    outfile.write(f'{memory_diff:.2f} MB')
