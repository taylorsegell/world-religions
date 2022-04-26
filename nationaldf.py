country= pd.read_csv('national.csv')
reduced_cols= ['year','state','code','population','religion_all','christianity_all','islam_all','hinduism_all','buddhism_all','noreligion_all','syncretism_all','judaism_all', 'sikhism_all']
df= country[reduced_cols]
df.sort_values(by='year', inplace = True)
df.reset_index(drop=True, inplace=True)


gdp = pd.read_excel('worldgdp1960.xlsx')
gdp.columns = gdp.columns.str.replace(r"\(.*\)","")
gdp = gdp.rename(columns={'United States':'United States of America'})
gdp = gdp.rename(columns ={'Country Name':'year'}).set_index('year')
stack = gdp.stack()
stack  =pd.DataFrame(stack) #
stack.index.names=['year', 'country'] 
stack.columns = ['gdp_per_capita']
stack.reset_index(inplace=True)

df = df[df.state != 'Yugoslavia']
df[df.state == 'German Federal Republic']= 'Germany'
df[df.state == 'German Democratic Republic']= 'Germany'
df[df.state == 'Republic of Vietnam'] = 'Vietnam'


import country_converter as coco
cc = coco.CountryConverter()
states = list(df.state)
states2 = list(stack.country)
iso3 = cc.convert(states)
iso = cc.convert(states2)
df['country_code'] = iso3
stack['country_code'] = iso
non_countries = stack[stack['country_code']=='not found'].index
stack.drop(non_countries, inplace=True)

from pycountry_convert import country_alpha2_to_continent_code, country_alpha3_to_country_alpha2


codes = list(df.country_code)

def get_continent(col):
    try:
        cn_a2_code =  country_alpha3_to_country_alpha2(col)
    except:
        cn_a2_code = 'NaN' 
    try:
        cn_continent = country_alpha2_to_continent_code(cn_a2_code)
    except:
        cn_continent = 'NaN' 
    return (cn_continent)

df["continent"] = df["country_code"].apply(lambda col: get_continent(col))
stack["continent"] = stack["country_code"].apply(lambda col: get_continent(col))

def continent_code_name(row):
    if row['continent'] == 'AS':
        return 'Asia'
    elif row['continent'] == 'OC':
        return 'Oceania'
    elif row['continent'] == 'EU':
        return 'Europe'
    elif row['continent'] == 'AF':
        return 'Africa'
    elif row['continent'] == 'SA':
        return 'South America'
    elif row['continent'] == 'NA':
        return 'North America'
    else:
        return 'Unknown'
    
df['continent'] = df.apply(continent_code_name, axis = 1)
stack['continent'] = stack.apply(continent_code_name, axis = 1)




major = df.merge(stack, how='inner', left_on=['year','state'] , right_on=['year','country'],suffixes=('', '_y'))
major.drop(major.filter(regex='_y$').columns.tolist(),axis=1, inplace=True)
major.drop(major[['country','code']], axis=1, inplace=True)

major.columns = major.columns.str.capitalize().str.replace('_all','').str.replace('Gdp_per_capita','GDP per Capita').str.replace('Country_code','Code').str.replace('Religion','Total Religous')
major = major.infer_objects()
total=major[['Year', 'State', 'Population', 'Total Religous', 'Code', 'Continent', 'GDP per Capita']]

total=major[['Year', 'State', 'Population', 'Total Religous', 'Code', 'Continent', 'GDP per Capita']]

data = major.set_index(['Year', 'State','Code', 'Population', 'Continent', 'GDP per Capita']).stack().reset_index()
data.rename(columns={'level_6':'Religon',0:'Followers'}, inplace=True)

major.sort_values(by=['Year','State'], inplace=True)

major.to_csv('countries_religon.csv', index=False)