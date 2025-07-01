import os
import pandas as pd

df = pd.read_csv('Entsoe_prices_NL/outfile_imb_15min_NL_20240101_to_20250101.csv', parse_dates=['time_stamp'])

# copy original Long price to new column:
df.insert(2, 'Long_original', df['Long'])

# determine if regeltoestand 2 actief is, vanwege verschil in prijs voor Long en Short in data
df.insert(4, 'reg_2', (df['Long'] == df['Short']).astype(int))

# regeltoestand 2 uren kunnen niet gebruikt worden, zet getal naar €50/MWh, dit is meeste kans dat hier net op geladen/ontladen gaat worden, €0 is minder optimale keus; vaker geladen worden
df['Long'] = df.apply(lambda row: row['Long'] if row['reg_2'] == 1 else float(50), axis=1)

# als bovenstaande problemen geeft met optimizer; zet getal naar €0/MWh (echter is dit imperfect, gezien laden op €0/MWh ook gunstig kan zijn, en we geen laad actie willen op dit tijdstip)
df['imb_price_NaN'] = df.apply(lambda row: row['Long'] if row['reg_2'] == 1 else float('nan'), axis=1)


#df['Long'] = df['imb_price_act']

# Testing prints:
print(df.head())
# hoeveel % regeltoestand 2?
reg2sum = df['reg_2'].sum() / len(df)
print(f"Percentage regeltoestand 2: {(1-reg2sum)*100:.1f}%")


# Write the DataFrame to a CSV file
df.to_csv('Entsoe_prices_NL/outfile_imb_15min_NL_20240101_to_20250101_reg2.csv', index=False)
