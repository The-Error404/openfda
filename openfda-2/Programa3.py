import requests
try:  
    r = requests.get('https://api.fda.gov/drug/label.json?search=active_ingredient:aspirin&limit=100&skip')
    main_dict = r.json()['results']
    man_list=[]
    for elem in main_dict:
        if 'manufacturer_name' in elem['openfda']:
            man_list.append(str(elem['openfda']["manufacturer_name"]).strip("['']"))
    print(set(man_list))
except requests.exceptions.RequestException:
    print("Connection refused (Check URL for mistypings)")
