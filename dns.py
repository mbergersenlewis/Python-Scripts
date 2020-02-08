import pandas as pd
df = pd.read_excel('pvg11.xlsx')
for i in df.iterrows():
    print('dnscmd 10.33.48.10 /RecordAdd XYZ.com ' + i[1][1] +' A ' + i[1][0], file=open("dns.bat", "a"))
