import requests
try:
  r = requests.get('https://api.fda.gov/drug/label.json')
  main_dict = r.json()['results'][0]
  id_info = str(main_dict['openfda']['spl_id']).strip("['']")
  man_info = str(main_dict['openfda']['manufacturer_name']).strip("['']")
  pur_info = str(main_dict['purpose']).strip("['']")
  print("ID del producto:",id_info)
  print("Información del fabricante:",man_info)
  print("Usos:",pur_info)
  except requests.exceptions.RequestException:
    print("Connection refused (Check URL for mistypings)")
