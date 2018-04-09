import requests
try:
    r = requests.get('https://api.fda.gov/drug/label.json?search=manufacturer_name:pfizer&limit=10')
    main_dict = r.json()['results']
    print('IDs de 10 medicamentos:')
    for elem in main_dict:
        print(str(elem['openfda']['spl_id']).strip("['']"))
except requests.exceptions.RequestException:
    print("Connection refused (Check URL for mistypings)")
