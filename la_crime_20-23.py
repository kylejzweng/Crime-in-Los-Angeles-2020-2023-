import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import folium
import re

# Importing data.
data = pd.read_csv('LA Crime 20-23.csv')

# Which area has the most crime.
area_name_counts = data['AREA NAME'].value_counts()
area_name_counts = area_name_counts.sort_values(ascending = False)
area_name_counts.plot(kind = 'bar')
plt.xlabel('Area of Los Angeles')
plt.ylabel('Number of Crimes')
plt.title('Number of Crimes per Los Angeles Area\nJan 2020-June 2023')
plt.xticks(fontsize=8)
plt.tight_layout()
plt.show()

# Which type of crime is the most common.
crime_description_counts = data['Crm Cd Desc'].value_counts().head(25)
crime_description_counts = crime_description_counts.sort_values(ascending = False)
crime_description_counts.plot(kind = 'bar', figsize=(12, 8))
plt.xlabel('Crime Description')
plt.ylabel('Number of Instances')
plt.title('25 Most Common Crime Descriptions in Los Angeles\nJan 2020-June 2023')
plt.xticks(fontsize=8)
plt.tight_layout()
plt.show()

# Grouping the crimes into broader categories
grouping_crimes = {
    'Arson': [r'ARSON'],
    'Assault': [r'ASSAULT', r'BRANDISH', r'CRIMINAL THREATS', r'AGGRAVATED ASSAULT', r'SIMPLE ASSAULT', 
                r'OTHER ASSAULT', r'THREATENING PHONE CALLS', r'THROWING', r'STALKING', r'PROWLER', 
                r'CRIMINAL HOMICIDE', r'MANSLAUGHTER', r'BATTERY', r'LYNCHING'],
    'Theft': [r'THEFT', r'ROBBERY', r'STOLEN', r'BURGLARY', r'GRAND THEFT', r'PETTY THEFT', r'PICKPOCKET', 
              r'PURSE SNATCHING', r'ATTEMPT STOLEN', r'SHOPLIFTING'],
    'Bunco': [r'BUNCO'],
    'Crimes against Children': [r'CHILD', r'CHLD', r'KIDNAPPING'],
    'Crimes against Animals': [r'CRUELTY TO ANIMALS', r'BEASTIALITY'],
    'Fraud': [r'COUNTERFEIT', r'CREDIT CARDS', r'DEFRAUDING'],
    'Firearm Discharge': [r'DISCHARGE FIREARMS', r'SHOTS FIRED'],
    'Drugs': [r'DRUGS'],
    'Driving offenses': [r'RECKELSS DRIVING', r'DRIVING WITHOUT OWNER CONSENT', r'RECKLESS DRIVING'],
    'Sex crimes': [r'HUMAN TRAFFICKING', r'INCEST', r'INDECENT EXPOSURE', r'LETTERS, LEWD', r'RAPE', r'SEX', 
                   r'PEEPING TOM', r'SODOMY', r'LEWD CONDUCT', r'ORAL', r'PIMPING'],
    'Trespassing': [r'TRESPASSING'],
    'Vandalism': [r'VANDALISM'],
    'Violation of Court Orders': [r'VIOLATION OF COURT ORDER', r'VIOLATION OF RESTRAINING ORDER', 
                                  r'VIOLATION OF TEMPORARY'],
    'Resisting arrest': [r'RESISTING ARREST', r'FAILURE TO YIELD']
    # 'Other': [r'BIGAMY', r'BOAT', r'BOMB', r'BRIBERY', r'CONSPIRACY', r'CONTEMPT', r'FALSE POLICE', 
    #           r'DOCUMENT', r'EMBEZZLEMENT', r'EXTORTION', r'FAILURE TO DISPERSE', r'OTHER MESCELLANEOUS', 
    #           r'OTHER MISCELLANEOUS CRIME', r'UNAUTHORIZED COMPUTER ACCESS', r'FALSE IMPRISONMENT', 
    #           r'ILLEGAL DUMPING', r'DISRUPT SCHOOL', r'DISTURBING THE PEACE', r'DISHONEST EMPLOYEE']
}

def map_crime_category(description):
    description = description.upper()
    for category, crimes in grouping_crimes.items():
        for crime in crimes:
            if re.search(crime, description):
                return category
    return 'Other'

data['category of crime'] = data['Crm Cd Desc'].map(map_crime_category)

# Plot crime categories
crime_categories_broad = data['category of crime'].value_counts()
crime_categories_broad = crime_categories_broad.sort_values(ascending = False)
crime_categories_broad.plot(kind = 'bar')
plt.xlabel('Crime Category')
plt.ylabel('Number of Instances')
plt.title('Number of Crimes by Category\nJan 2020-June 2023')
plt.xticks(fontsize=8)
plt.tight_layout()
plt.show()

# Amount of violent vs non-violent crimes.
grouping_violent_crime = {
    'Violent': [r'ARSON', r'ASSAULT', r'BRANDISH', r'CRIMINAL THREATS', r'AGGRAVATED ASSAULT', 
                r'SIMPLE ASSAULT', r'OTHER ASSAULT', r'THREATENING PHONE CALLS', r'THROWING', r'STALKING', 
                r'PROWLER', r'DISCHARGE FIREARMS', r'SHOTS FIRED', r'CRIMINAL HOMICIDE', r'MANSLAUGHTER', 
                r'BATTERY', r'LYNCHING', r'CHILD', r'CHLD', r'KIDNAPPING', r'HUMAN TRAFFICKING', r'INCEST', 
                r'INDECENT EXPOSURE', r'LETTERS, LEWD', r'RAPE', r'SEX', r'PEEPING TOM', r'SODOMY', 
                r'LEWD CONDUCT', r'ORAL', r'PIMPING',r'CRUELTY TO ANIMALS', r'BEASTIALITY']
}

def map_crime_type_category(description):
    description = description.upper()
    for category, crimes in grouping_violent_crime.items():
        for crime in crimes:
            if re.search(crime, description):
                return category
    return 'Non-Violent'

data['crime_type'] = data['Crm Cd Desc'].map(map_crime_type_category)

# Plot crime categories
crime_type = data['crime_type'].value_counts()
crime_type= crime_type.sort_index()
crime_type.plot(kind = 'bar')
plt.xlabel('Type of Crime')
plt.ylabel('Number of Instances')
plt.title('Number of Non-Violent and Violent Crimes in Los Angeles\nJan 2020-June 2023')
plt.xticks(fontsize=8)
plt.tight_layout()
plt.show()

# Violent and non-violent crimes by area
crime_type_by_area = data.groupby([data['AREA NAME'], data['crime_type']]).size().unstack(fill_value=0)
crime_type_by_area = crime_type_by_area.sort_index()  
crime_type_by_area.plot(kind='line')
plt.xlabel('Area of Los Angeles')
plt.ylabel('Number of Instances')
plt.title('Number of Violent and Non-Violent Crimes by Area\nJan 2020-June 2023')
plt.legend(title='Crime Type')
plt.xticks(range(len(crime_type_by_area.index)), crime_type_by_area.index, fontsize=8, rotation=90)
plt.tight_layout()
plt.show()

# What were the most common premise description locations?
premise_description_count = data['Premis Desc'].value_counts().head(30)
premise_description_count = premise_description_count.sort_values(ascending = False)
premise_description_count.plot(kind = 'bar', figsize=(12, 8))
plt.xlabel('Premise Location')
plt.ylabel('Number of Instances')
plt.title('30 Most Common Premise Locations for Crimes in Los Angeles\nJan 2020-June 2023')
plt.xticks(fontsize=8)
plt.tight_layout()
plt.show()

# Most common weapons used?
weapon_used = data['Weapon Desc'].value_counts().head(5)
weapon_used = weapon_used.sort_values(ascending = False)
weapon_used.plot(kind = 'bar', figsize=(12, 8))
plt.xlabel('Weapon Involved')
plt.ylabel('Number of Instances')
plt.title('5 Most Common Weapons Used in Los Angeles\nJan 2020-June 2023')
plt.xticks(fontsize=8)
plt.tight_layout()
plt.show()

# Grouping the weapons into broader categories
grouping_weapons = {
    'Airsoft/BB Gun': [r'AIR PISTOL'],
    'Gun': [r'ANTIQUE FIREARM', r'ASSAULT WEAPON', r'AUTOMATIC WEAPON', r'HAND GUN', r'HECKLER', r'M-14', 
            r'M1-1', r'MAC', r'OTHER FIREARM', r'RELIC FIREARM', r'REVOLVER', r'RIFLE', r'SHOTGUN', 
            r'SEMI-AUTOMATIC', r'SIMULATED GUN', r'PISTOL', r'STUN GUN', r'TOY GUN', r'UNK TYPE', 
            r'UNKNOWN FIREARM', r'UZI'],
    'Knife': [r'BOWIE KNIFE', r'CLEAVER', r'DIRK', r'FOLDING KNIFE', r'KNIFE', r'OTHER CUTTING', 
              r'SWITCH BLADE', r'SWORD', r'UNKNOWN TYPE CUTTING INSTRUMENT'],
    'Tools': [r'AXE', r'BELT', r'BLUNT', r'BOARD', r'BOW AND ARROW', r'BRASS KNUCKLES', r'CLUB', r'BAT', 
              r'CONCRETE BLOCK', r'GLASS', r'HAMMER', r'ICE PICK', r'MACE', r'MACHETE', r'MARTIAL ARTS', 
              r'OTHER KNIFE', r'PIPE', r'RAZOR', r'ROCK', r'ROPE', r'SCISSORS', r'SCREWDRIVER'],
    'Bomb Threat': [r'BOMB', r'EXPLOSIVE', r'STICK', r'TIRE IRON'],
    'Person': [r'STRONG-ARM', r'PHYSICAL PRESENCE'],
    'Fire': [r'FIRE'],
    'Vehicle': [r'VEHICLE'],
    'Verbal Threat': [r'VERBAL THREAT'],
    'Other': [r'BLACKJACK', r'CHEMICAL', r'DEMAND NOTE', r'DOG', r'FIXED OBJECT', r'SYRINGE', r'UNKNOWN WEAPON']
}

def map_weapon_category(description):
    if isinstance(description, str):
        description = description.upper()
        for category, crimes in grouping_weapons.items():
            for crime in crimes:
                if re.search(crime, description):
                    return category
    return 'No Weapon Used'

data['category of weapon'] = data['Weapon Desc'].map(map_weapon_category)

# Plot weapon categories
weapon_category = data['category of weapon'].value_counts()
weapon_category = weapon_category.sort_values(ascending = False)
weapon_category.plot(kind = 'bar')
plt.xlabel('Weapon Category')
plt.ylabel('Number of Instances')
plt.title('Number of Crimes by Weapon Category in Los Angeles\nJan 2020-June 2023')
plt.xticks(fontsize=8)
plt.tight_layout()
plt.show()

# Let's see how crime has changed over the years 2020-2023
data['date'] = pd.to_datetime(data['DATE OCC'], format = '%m/%d/%Y %I:%M:%S %p')
data['year'] = data['date'].dt.year

crimes_per_year = data['year'].value_counts()
crimes_per_year = crimes_per_year.sort_index()  
print(crimes_per_year)
crimes_per_year.plot(kind = 'bar')
plt.xlabel('Year')
plt.ylabel('Number of Crimes')
plt.title('Number of Crimes by Year in Los Angeles\nJan 2020-June 2023')
plt.xticks(fontsize=8)
plt.tight_layout()
plt.show()

# Crime has increased. What about by violent/non-violent
crime_type_by_year = data.groupby([data['year'], data['crime_type']]).size().unstack(fill_value=0)
crime_type_by_year = crime_type_by_year.sort_index()  
print(crime_type_by_year)
ax = crime_type_by_year.plot(kind='line')
ax.xaxis.set_major_locator(ticker.MultipleLocator(base = 1))
plt.xlabel('Year')
plt.ylabel('Number of Crimes')
plt.title('Number of Violent and Non-Violent Crimes by Year in Los Angeles\nJan 2020-June 2023')
plt.legend(title='Crime Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plotting locations of crimes on map.
map_center = [34.0522, -118.2437]  # Latitude and longitude of Los Angeles
map_zoom = 10  
crime_map = folium.Map(location=map_center, zoom_start=map_zoom)

for index, row in data.iterrows():
    lat = row['LAT']
    lon = row['LON']
    crime_description = row['Crm Cd Desc']
    date = row['Date Rptd']
    if index % 1000 == 0:
        popup_content = f"Crime Description: {crime_description}<br>Date: {date}"
        folium.Marker(location=[lat, lon], popup=popup_content).add_to(crime_map)

# Saving the map as .html
crime_map.save('crime_map.html')

# data_df.to_csv('LA Crime 20-22.csv')

