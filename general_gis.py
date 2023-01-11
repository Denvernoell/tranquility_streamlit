def to_decimal_degrees(coord):
	from re import split
	import numpy as np
	delims = ['°','⁰', "\'", '"',' ']
	C = split('|'.join(delims), coord)
	C = [c for c in C if c != '']
	if len(C) == 4:
		decimal_degree = (float(C[0])) + (float(C[1]) / 60) + (float(C[2]) / 60 / 60)
		if C[3] == 'W':
			return decimal_degree * -1
		else:
			return decimal_degree
	else:
		return C[0]
import pandas as pd
# df = pd.read_clipboard()
df = df.dropna(subset=['latitude','longitude'])

df[['latitude','longitude']].applymap(to_decimal_degrees).to_clipboard(index=False)