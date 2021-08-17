import pandas as pd
df = pd.DataFrame({
        'A' : [1,2,3,4,5],
        'B' : ["5.55","3.33","4.24", "9.88", "12.21"]
    })
# Convert column "A" to float type
df["A"] = df["A"].astype(float) 
# Convert all the columns in the datafrmae to the type float
df = df.astype(float) # Applied to all the columns in a dataframe
# Converts column "A" to string type
df["A"] = df["A"].astype(str)
# Convert multiple columns datatype using astype() method 
df = df.astype({"A":float, "B": str})  # Specifying in the parameter changes the datatype of columns of our choice.
print(df.dtypes) 
#Output 
