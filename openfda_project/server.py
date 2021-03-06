from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import redirect
from functools import wraps
import http.client
import json

app = Flask(__name__)

MAIN_INPUT = "api.fda.gov"
headers = {'User-Agent': 'http-client'}
DEBUG = True

main_conn = http.client.HTTPSConnection(MAIN_INPUT)

@app.route ("/searchDrug", methods = ['GET']) # Busca hasta 100 medicamentos con el principio activo especificado
def getActIng():

    name = request.args.get('active_ingredient')
    limit = request.args.get('limit')

    if limit is None:

        openfda_input = '/drug/label.json?search=active_ingredient:{acting}&limit=10'.format(acting=name)

    else:

        openfda_input = '/drug/label.json?search=active_ingredient:{acting}&limit={lim}'.format(acting=name,lim=limit)

    main_conn.request('GET', openfda_input, None, headers)

    data_stage1 = main_conn.getresponse()

    data_stage2 = data_stage1.read()
    main_conn.close()

    data_final = json.loads(data_stage2.decode('utf-8'))

    main_dict = data_final['results']
    name_list=[]
    for elem in main_dict:
        if 'brand_name' in elem['openfda']:
            name_list.append("<li>" + str(elem['openfda']['brand_name']).strip("['']") + "</li>")
        else:
            name_list.append("<li>Desconocido</li>")

    name_str = str(''.join(name_list))

    def print_ul(elements):
        print("<ul>")
        for s in elements:
            ul = "<li>" + str(s) + "</li>"
        print(ul)
        print("</ul>")

    html_str = """
        <!DOCTYPE html>
        <html>
        <body>
        <p>Nombres comerciales disponibles para medicamentos con {r} como principio activo en openFDA:</p>
        <p>Mostrando {l} resultados</p>
        <ul>
        <p>{mans}</p>
        </ul>
        </body>
        </html>
        """

    with open("templates/getActIng.html","w") as main_output:
        main_output.write("")
        html_str_mod = html_str.format(r=name, l=limit, mans=name_str)
        main_output.write(html_str_mod)

    return render_template('getActIng.html')

@app.route ("/searchCompany", methods = ['GET']) # Busca hasta 100 medicamentos fabricados por la empresa especificada
def getComName():

    company_name = request.args.get('company')
    limit = request.args.get('limit')

    if limit is None:

        openfda_input = '/drug/label.json?search=openfda.manufacturer_name:{comnam}&limit=10'.format(comnam=company_name)

    else:

        openfda_input = '/drug/label.json?search=openfda.manufacturer_name:{comnam}&limit={lim}'.format(comnam=company_name,lim=limit)

    main_conn.request('GET', openfda_input, None, headers)

    data_stage1 = main_conn.getresponse()

    data_stage2 = data_stage1.read()
    main_conn.close()

    data_final = json.loads(data_stage2.decode('utf-8'))

    main_dict = data_final['results']
    med_list=[]
    for elem in main_dict:
        if 'manufacturer_name' in elem['openfda']:
            med_list.append("<li>" + str(elem['openfda']['brand_name']).strip("['']") + "</li>")
        else:
            med_list.append("<li>Desconocido</li>")

    med_str = str(''.join(med_list))

    html_str = """
        <!DOCTYPE html>
        <html>
        <body>
        <p>Medicamentos fabricados por {r} en openFDA:</p>
        <p>Mostrando {l} resultados</p>
        <ul>
        <p>{meds}</p>
        </ul>
        </body>
        </html>
        """

    with open("templates/getComName.html","w") as main_output:
        html_str_mod = html_str.format(r=company_name,l=limit,meds=med_str)
        main_output.write(html_str_mod)

    return render_template('getComName.html')

@app.route ("/listDrugs", methods = ['GET']) # Devuelve una cantidad aleatoria de medicamentos
def getListDrugs():

    limit = request.args['limit']

    try:
        openfda_input = '/drug/label.json?limit={amount}'.format(amount=limit)
        main_conn.request('GET', openfda_input, None, headers)
    except:
        print("Error")
        exit(1)

    data_stage1 = main_conn.getresponse()

    data_stage2 = data_stage1.read()
    main_conn.close()

    data_final = json.loads(data_stage2.decode('utf-8'))

    main_dict = data_final['results']
    ran_list=[]
    for elem in main_dict:
        if 'brand_name' in elem['openfda']:
            ran_list.append("<li>" + str(elem['openfda']['brand_name']).strip("['']") + "</li>")
        else:
            ran_list.append("<li>Desconocido</li>")

    ran_str = str(''.join(ran_list))

    html_str = """
        <!DOCTYPE html>
        <html>
        <body>
        <p>Nombres comerciales de {r} medicamentos de openFDA:</p>
        <p>Mostrando {l} resultados</p>
        <ul>
        <p>{rans}</p>
        </ul>
        </body>
        </html>
        """

    with open("templates/getListDrugs.html","w") as main_output:
        html_str_mod = html_str.format(r=limit,l=limit, rans=ran_str)
        main_output.write(html_str_mod)

    return render_template('getListDrugs.html')

@app.route ("/listCompanies", methods = ['GET']) # Devuelve una cantidad especificada de empresas con uno de sus productos
def getListCom():

    limit = request.args['limit']

    try:
        openfda_input = '/drug/label.json?limit={amount}'.format(amount=limit)
        main_conn.request('GET', openfda_input, None, headers)
    except:
        print("Error")
        exit(1)

    data_stage1 = main_conn.getresponse()

    data_stage2 = data_stage1.read()
    main_conn.close()

    data_final = json.loads(data_stage2.decode('utf-8'))

    main_dict = data_final['results']
    com_list=[]
    for elem in main_dict:
        if 'manufacturer_name' in elem['openfda']:
            com_list.append("<li>" + str(elem['openfda']['manufacturer_name']).strip("['']") + "</li>")
        else:
            com_list.append("<li>Desconocido</li>")

    com_str = str(''.join(com_list))

    html_str = """
        <!DOCTYPE html>
        <html>
        <body>
        <p>Nombres de {r} fabricantes (y sus respectivos productos) de openFDA:</p>
        <p>Mostrando {l} resultados</p>
        <ul>
        <p>{prod}</p>
        </ul>
        </body>
        </html>
        """

    with open("templates/getListCom.html","w") as main_output:
        html_str_mod = html_str.format(r=limit,l=limit, prod=com_str)
        main_output.write(html_str_mod)

    return render_template('getListCom.html')

@app.route ("/listWarnings", methods = ['GET']) # Devuelve una cantidad aleatoria de medicamentos
def getListWar():

    limit = request.args['limit']

    try:
        openfda_input = '/drug/label.json?limit={amount}'.format(amount=limit)
        main_conn.request('GET', openfda_input, None, headers)
    except:
        print("Error")
        exit(1)

    data_stage1 = main_conn.getresponse()

    data_stage2 = data_stage1.read()
    main_conn.close()

    data_final = json.loads(data_stage2.decode('utf-8'))

    main_dict = data_final['results']
    war_list=[]
    for elem in main_dict:
        if 'warnings' in elem:
            war_list.append("<li>" + str(elem['warnings']).strip("['']") + "</li>")
        else:
            war_list.append("<li>Desconocido</li>")

    war_str = str(''.join(war_list))

    html_str = """
        <!DOCTYPE html>
        <html>
        <body>
        <p>Advertencias:</p>
        <p>Mostrando {l} resultados</p>
        <ul>
        <p>{wars}</p>
        </ul>
        </body>
        </html>
        """

    with open("templates/getListWars.html","w") as main_output:
        html_str_mod = html_str.format(l=limit, wars=war_str)
        main_output.write(html_str_mod)

    return render_template('getListWars.html')

@app.route('/secret', methods = ['GET'])
def getSecret():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Not Authorized"'})

@app.route('/redirect', methods = ['GET'])
def getRedirect():
    return redirect("http://127.0.0.1:8000/", code=302)

@app.route('/', methods=['GET', 'POST'])
def index():

    return """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>OpenFDA-project</title>
        </head>
        <body>
        <form action = "listDrugs" method="get">
          <input type="submit" value="Listar fármacos">
            Limite: <input type="text" name="limit" value="">
        </form>
        <form action = "listCompanies" method="get">
          <input type="submit" value="Listar empresas">
            Limite: <input type="text" name="limit" value="">
        </form>
        <form action = "searchDrug" method="get">
          <input type="submit" value="Buscar fármaco">
            Campo: <input type="text" name="active_ingredient" value="">
            Limite Drug: <input type="text" name="limit" value="">
        </form>
        <form action = "searchCompany" method="get">
          <input type="submit" value="Buscar empresas">
            Campo: <input type="text" name="company" value="">
            Limite Com: <input type="text" name="limit" value="">
        </form>
        <form action = "listWarnings" method="get">
          <input type="submit" value="Advertencias">
            Limite: <input type="text" name="limit" value="">
        </form>
        </body>
        </html>
        """

if __name__ == "__main__":
    app.run('127.0.0.1', port = 8000, debug = True, use_reloader = False)
