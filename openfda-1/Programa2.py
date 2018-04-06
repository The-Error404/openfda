import requests
r = requests.get('https://api.fda.gov/drug/label.json?search=manufacturer_name:pfizer&limit=10')
main_dict = r.json()['results']
for elem in main_dict:
    print(str(elem['openfda']['spl_id']).strip("['']"))
