import requests
import pandas as pd
from sqlalchemy import create_engine

# Scraping Multiple Pages (here: ~5000results)
brand_ny = []
model_ny = []
mileage_ny = []
year_ny = []
price_ny = []

for i in range(1, 170):
    headers = {
        'authority': 'www.truecar.com',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'x-xsrf-token': 'Uc5teaHPCw5lAZqhrfN59nq4IGZXjcfcK39/5JviFyiQetLCmUo0CyIl52EHrnwYhbsUinRzkvUtkze1/W8Dww==',
        'sec-gpc': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.truecar.com/used-cars-for-sale/listings/location-new-york-ny/',
        'accept-language': 'ru-RU,ru;q=0.9',
        'if-none-match': 'W/"b989a027fc1ae6c64044c670a11bab01"',
    }

    params = (
        ('city', 'new-york'),
        ('collapse', 'true'),
        ('fallback', 'true'),
        ('include_incentives', 'true'),
        ('include_targeted_incentives', 'true'),
        ('new_or_used', 'u'),
        ('page', str(i)),
        ('per_page', '30'),
        ('postal_code', '10001'),
        ('search_event', 'true'),
        ('sort/[/]', 'best_match'),
        ('sponsored', 'true'),
        ('state', 'ny'),
    )

    # response
    response = requests.get('https://www.truecar.com/abp/api/vehicles/used/listings', headers=headers, params=params)

    # json object
    results_json = response.json()

    # result items (30 items per page)
    results_items = results_json['listings']

    for result in results_items:
        # brand
        brand_ny.append(result['vehicle']['make'])

        # model
        model_ny.append(result['vehicle']['model'])

        # mileage
        mileage_ny.append(result['vehicle']['mileage'])

        # year
        year_ny.append(result['vehicle']['year'])

        # price
        price_ny.append(result['pricing']['list_price'])
    
df_ny_multiple = pd.DataFrame({'Brand': brand_ny, 'Model': model_ny, 'Mileage': mileage_ny,
                               'Year': year_ny, 'Price': price_ny})

# save data to excel file
df_ny_multiple.to_excel('output_5k.xlsx', index=False)

# Extract San Francisco's data
brand_sf = []
model_sf = []
mileage_sf = []
year_sf = []
price_sf = []

for i in range(1, 170):
    headers = {
        'authority': 'www.truecar.com',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'x-xsrf-token': 'klQe8AsU4VWZh2Wt+LccV1Y+j6senwcueQUuua/6scVT4KFLM5HeUN6jGG1S6hm5qT27Rz1hUgd/6WboyXelLg==',
        'sec-gpc': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.truecar.com/used-cars-for-sale/listings/location-san-francisco-ca/',
        'accept-language': 'ru-RU,ru;q=0.9',
        'if-none-match': 'W/"e798de94d7f33205674c2b80b4247f2e"',
    }

    params = (
        ('city', 'san-francisco'),
        ('collapse', 'true'),
        ('fallback', 'true'),
        ('include_incentives', 'true'),
        ('include_targeted_incentives', 'true'),
        ('new_or_used', 'u'),
        ('page', str(i)),
        ('per_page', '30'),
        ('postal_code', '94102'),
        ('search_event', 'true'),
        ('sort/[/]', 'best_match'),
        ('sponsored', 'true'),
        ('state', 'ca'),
    )

    # response
    response = requests.get('https://www.truecar.com/abp/api/vehicles/used/listings', headers=headers, params=params)

    # json object
    results_json = response.json()

    # result items (30 items per page)
    results_items = results_json['listings']

    for result in results_items:
        # brand
        brand_sf.append(result['vehicle']['make'])

        # model
        model_sf.append(result['vehicle']['model'])

        # mileage
        mileage_sf.append(result['vehicle']['mileage'])

        # year
        year_sf.append(result['vehicle']['year'])

        # price
        price_sf.append(result['pricing']['list_price'])
    
df_sf_multiple = pd.DataFrame({'Brand': brand_sf, 'Model': model_sf, 'Mileage': mileage_sf,
                               'Year': year_sf, 'Price': price_sf})

# Combine Data & Connect to Database - PostgreSQL

# merge dataframes
merged_dataframes = pd.concat([df_ny_multiple, df_sf_multiple], ignore_index=True)
# change type of price column
merged_dataframes['Price'] = merged_dataframes['Price'].astype('Int64')
# save data to excel file
merged_dataframes.to_excel('merged_dataframes.xlsx', index=False)
# connect to postgresql database
engine = create_engine('postgresql://postgres:1u1sb02839y@localhost:5432')
# save extracted data to database
merged_dataframes.to_sql('cars_results', engine)
