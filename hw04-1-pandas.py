import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import psutil

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
  memory_pre = compute_memory_usage('outputs/hw04-1-pandas-pre.txt')
  print(f'{memory_pre:.2f} MB used pre-computation')
  s3_uri = 's3://dsan6000-data/acled_events.parquet'
  
  acled_df = pd.read_parquet(s3_uri)

  acled_df = acled_df[acled_df['year'].between(2018, 2024)]

  yearly_df = (
      acled_df.groupby('year', as_index=False)['fatalities']
      .sum()
      .sort_values('year')
  )

  os.makedirs('images', exist_ok=True)

  plt.figure(figsize=(10, 6))
  sns.lineplot(
      data=yearly_df,
      x='year',
      y='fatalities',
      marker='o'
  )
  plt.title("ACLED: Yearly Fatality Counts (Pandas)")
  plt.xlabel("Year")
  plt.ylabel("Total Fatalities")
  plt.tight_layout()
  plt.savefig('images/yearly_fatalities_pandas.svg')
  
  memory_post = compute_memory_usage('outputs/hw04-1-pandas-post.txt')
  print(f'{memory_post:.2f} MB used post-computation')
  memory_diff = memory_post - memory_pre
  print(f'=> {memory_diff:.2f} MB added via Pandas operation')
  with open('outputs/hw04-1-pandas-diff.txt', 'w', encoding='utf-8') as outfile:
    outfile.write(f'{memory_diff:.2f} MB')
