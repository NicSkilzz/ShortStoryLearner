import pandas as pd

df = pd.read_csv("pg_catalog_de.csv")
print(type(str(df['Text#'][0])))
