import pandas as pd
import numpy as np

# Load the original dataset
df = pd.read_csv("CUSTOMER_SEGMENTATION_DATA_APR25.csv", on_bad_lines='skip')

df.columns = df.columns.str.replace("'", "").str.strip()
df = df.drop(columns=['TrainID', 'TrainCategory', 'TrainDescription'])

# Replace nulls
df['DiscountCategory'].fillna('NO CONCESSION', inplace=True)
df['DEP_TIME_HR'].fillna(-1, inplace=True)
df['ARR_TIME_HR'].fillna(-1, inplace=True)

# Clean columns
df['AgeGroup'] = df['AgeGroup'].astype(str).str.replace("'", "").str.strip()
df['DistanceGroup'] = df['DistanceGroup'].astype(str).str.replace("'", "").str.strip()
df['Gender'] = df['Gender'].astype(str).str.replace("'", "").str.strip()
df['DiscountCategory'] = df['DiscountCategory'].astype(str).str.replace("'", "").str.strip()
df['ClassType'] = df['ClassType'].str.replace("'", '').str.strip()

# Map AgeGroup
age_group_mapping = {
    "1 Young Children (0 to 5 Years)": "Young Children",
    "2 Children (6 to 11 Years)": "Children",
    "3 Adolescent (12 to 17 Years)": "Adolescent",
    "4 Late Adolescent (18 to 24 Years)": "Late Adolescent",
    "5 Youth (25 to 40 Years)": "Youth",
    "6 Adult (41 to 59 Years)": "Adult",
    "7 Senior Citizen (60-79)": "Senior Citizen",
    "8 Senior Citizen (80-125))": "Adult Senior Citizen"
}
df['AgeGroupMapped'] = df['AgeGroup'].map(age_group_mapping)

# Create Distance features
df['DistanceValue'] = df['DistanceGroup'].str.extract(r"^(\d+)").astype(int)
df['IsLongDistance'] = df['DistanceValue'].apply(lambda x: 0 if x <= 10 else 1)

# df1 creation
boarding_group = df.groupby(['TravelDate', 'OriginCode'])['PassengerCount'].sum().reset_index()
boarding_group.rename(columns={'PassengerCount': 'TOTAL_BOARDING_PSGN'}, inplace=True)

valid_arrival_df = df[df['ARR_TIME_HR'] != -1]
peak_arrival = valid_arrival_df.groupby(['TravelDate', 'OriginCode', 'ARR_TIME_HR'])['PassengerCount'].sum().reset_index()
peak_arrival = peak_arrival.loc[peak_arrival.groupby(['TravelDate', 'OriginCode'])['PassengerCount'].idxmax()]
peak_arrival = peak_arrival[['TravelDate', 'OriginCode', 'ARR_TIME_HR']].rename(columns={'ARR_TIME_HR': 'PEAK_ARRIVAL_HR'})

all_station_dates = df.groupby(['TravelDate', 'OriginCode']).size().reset_index()[['TravelDate', 'OriginCode']]
peak_arrival = pd.merge(all_station_dates, peak_arrival, on=['TravelDate', 'OriginCode'], how='left')
peak_arrival['PEAK_ARRIVAL_HR'] = peak_arrival['PEAK_ARRIVAL_HR'].fillna(-1)

arrival_group = df.groupby(['TravelDate', 'DestCode'])['PassengerCount'].sum().reset_index()
arrival_group.rename(columns={'DestCode': 'OriginCode', 'PassengerCount': 'TOTAL_ARR_PSGN'}, inplace=True)

df1 = pd.merge(boarding_group, peak_arrival, on=['TravelDate', 'OriginCode'], how='left')
df1 = pd.merge(df1, arrival_group, on=['TravelDate', 'OriginCode'], how='left')
df1['TOTAL_ARR_PSGN'] = df1['TOTAL_ARR_PSGN'].fillna(0)
df1['TOTAL_PSGN'] = df1['TOTAL_BOARDING_PSGN'] + df1['TOTAL_ARR_PSGN']
df1['STATION_TAG'] = df1.apply(lambda x: 'A' if x['TOTAL_ARR_PSGN'] > x['TOTAL_BOARDING_PSGN'] else 'D', axis=1)
df1.rename(columns={'OriginCode': 'STATION_CODE', 'TOTAL_PSGN': 'TOTAL_PSGN_DAY'}, inplace=True)

# df2 creation
allowed_concessions = [
    'SENIOR-CITIZEN-NOCONC', 'PHYSICALLY HANDICAPPED', 'CANCER PATIENT',
    'MENTAL PATIENT', 'DISABLED/PATIENT', 'PATIENT', 'HEART PATIENT'
]
ac_classes = ['1A', '2A', '3A', '3E', 'CC', 'EC', 'EA', 'EV', 'FC', 'VS']
non_ac_classes = ['SL', '2S']

group = df.groupby('OriginCode')

df2 = pd.DataFrame({
    'PREDOMINANT_CLASS': group['ClassType'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan),
    'NUM_FEMALE': group['Gender'].count() * 0,  # placeholder, update below
    'NUM_MALE': group['Gender'].apply(lambda x: (x == 'M').sum()),
    'NUM_Young_Children': group['AgeGroupMapped'].apply(lambda x: (x == 'Young Children').sum()),
    'NUM_Children': group['AgeGroupMapped'].apply(lambda x: (x == 'Children').sum()),
    'NUM_Adolescent': group['AgeGroupMapped'].apply(lambda x: (x == 'Late Adolescent').sum()),
    'NUM_SENIOR': group['DiscountCategory'].apply(lambda x: x.isin(allowed_concessions).sum()),
    'IS_AC': group['ClassType'].apply(lambda x: x.isin(ac_classes).sum()),
    'IS_NON_AC': group['ClassType'].apply(lambda x: x.isin(non_ac_classes).sum()),
    'PREDOMINANT_BKG_TYPE': group['BookingType'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan),
    'NUM_Kids': group.apply(lambda g: ((g['AgeGroupMapped'] == 'Young Children') | ((g['AgeGroupMapped'] == 'Children') & (g['IsLongDistance'] == 1))).sum()),
    'TOTAL_PSGN_MONTH': group['PassengerCount'].sum()
}).reset_index()

# Recalculate NUM_FEMALE using a filtered count
female_mask = (df['Gender'] == 'F') & (df['AgeGroupMapped'].isin(['Adolescent', 'Late Adolescent', 'Youth', 'Adult']))
female_group = df[female_mask].groupby('OriginCode')['Gender'].count().reset_index()
female_group.rename(columns={'Gender': 'NUM_FEMALE'}, inplace=True)
df2 = pd.merge(df2.drop(columns='NUM_FEMALE'), female_group, on='OriginCode', how='left')
df2['NUM_FEMALE'] = df2['NUM_FEMALE'].fillna(0)

df2.rename(columns={'OriginCode': 'STATION_CODE'}, inplace=True)

df2['AC_OR_NON_AC'] = df2.apply(lambda row: 1 if row['IS_AC'] >= row['IS_NON_AC'] else 0, axis=1)
avg_kids = df2['NUM_Kids'].mean()
df2['COOLIE_REQ'] = df2['NUM_Kids'].apply(lambda x: 1 if x >= avg_kids else 0)

# Amenities logic
avg_total_psgn = df1['TOTAL_PSGN_DAY'].mean()
avg_total_arr_psgn = df1['TOTAL_ARR_PSGN'].mean()

def recommend_amenities1(row):
    amenities = []
    if row['TOTAL_PSGN_DAY'] > 1.2 * avg_total_psgn: amenities.append('Higher No of Toilet Stalls')
    if row['TOTAL_PSGN_DAY'] > 0.8 * avg_total_psgn: amenities.append('Waiting Room')
    if row['TOTAL_PSGN_DAY'] > 0.5 * avg_total_psgn: amenities.append('Drinking Water')
    if row['TOTAL_PSGN_DAY'] > 1.0 * avg_total_psgn: amenities.append('Food Stalls')
    if row['STATION_TAG'] == 'A' and row['TOTAL_ARR_PSGN'] > 1.1 * avg_total_arr_psgn: amenities.append('Bus Connectivity')
    if row['TOTAL_PSGN_DAY'] > 1.3 * avg_total_psgn: amenities.append('Additional Entries/Exits')
    if row['TOTAL_PSGN_DAY'] > 1.1 * avg_total_psgn: amenities.append('Bigger Cleaning Staff')
    return amenities

avg_senior = df2['NUM_SENIOR'].mean()
avg_female = df2['NUM_FEMALE'].mean()
avg_adolescent = df2['NUM_Adolescent'].mean()
avg_ac_ratio = df2['AC_OR_NON_AC'].mean()

def recommend_amenities2(row):
    recs = []
    if row['AC_OR_NON_AC'] > avg_ac_ratio: recs.append('AC Lounge')
    if row['COOLIE_REQ'] == 1:
        c = min(10, max(5, int(round(row['NUM_Kids'] / 10))))
        recs.append(f"Coolie Required({c})")
    if row['NUM_SENIOR'] > 0:
        w = min(10, max(1, int(round(row['NUM_SENIOR'] / 10))))
        recs.append(f"Wheelchair Access({w})")
    if row['NUM_Kids'] >= avg_kids: recs.append('Kids Play Area')
    if row['NUM_FEMALE'] >= avg_female: recs.append('Sanitary Product')
    return recs

# df3 construction
unique_stations = sorted(set(df1['STATION_CODE']) | set(df2['STATION_CODE']))
df3 = pd.DataFrame({'STATION_CODE': unique_stations})
df3['amenities1'] = [[] for _ in range(len(df3))]
df3['amenities2'] = [[] for _ in range(len(df3))]

df1_lookup = df1.set_index('STATION_CODE')
df2_lookup = df2.set_index('STATION_CODE')

def fill_amenities(row):
    s = row['STATION_CODE']
    if s in df1_lookup.index:
        row['amenities1'] = recommend_amenities1(df1_lookup.loc[s].iloc[0] if isinstance(df1_lookup.loc[s], pd.DataFrame) else df1_lookup.loc[s])
    if s in df2_lookup.index:
        row['amenities2'] = recommend_amenities2(df2_lookup.loc[s].iloc[0] if isinstance(df2_lookup.loc[s], pd.DataFrame) else df2_lookup.loc[s])
    return row

df3 = df3.apply(fill_amenities, axis=1)
df3['ALL_AMENITIES'] = df3['amenities1'] + df3['amenities2']
df3['ALL_AMENITIES'] = df3['ALL_AMENITIES'].apply(lambda lst: [x for x in lst if pd.notna(x) and x != ''])
df3['STATION_CODE'] = df3['STATION_CODE'].str.strip("'").str.strip()

# Add station metadata
station_info = df[['OriginCode', 'OriginName', 'OriginDivision', 'OriginZone']].drop_duplicates().rename(columns={
    'OriginCode': 'STATION_CODE',
    'OriginName': 'STATION_NAME',
    'OriginDivision': 'STATION_DIV',
    'OriginZone': 'STATION_ZONE'
})
station_info = station_info.apply(lambda col: col.str.strip("'").str.strip() if col.dtype == "object" else col)
df3 = pd.merge(df3, station_info, on='STATION_CODE', how='left')
df3['TOTAL_AMENITIES'] = df3['ALL_AMENITIES'].apply(len)

df3 = df3[[ 'STATION_ZONE', 'STATION_DIV', 'STATION_CODE', 'STATION_NAME', 'amenities1', 'amenities2', 'ALL_AMENITIES', 'TOTAL_AMENITIES' ]]

# Save final CSV
df3.to_csv("station_level_data_output.csv", index=False)
