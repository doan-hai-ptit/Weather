from db.connection import get_engine
import pandas as pd

engine = get_engine()
df = pd.read_sql("SELECT NOW();", engine)
print(df)