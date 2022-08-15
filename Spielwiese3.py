import pandas as pd


df = pd.DataFrame({"x": [1,2,3], "y": [10,20,30]})

print(sum(df["x"]))