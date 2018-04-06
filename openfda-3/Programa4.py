from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
import requests

app = Flask(__name__)

r = requests.get('https://api.fda.gov/drug/label.json?search=manufacturer_name:pfizer&limit=10')
main_input = r.json()['results']

@app.route('/drugnames',methods=['GET'])
def getBrandNames():
    brand_list = [str(elem['openfda']['brand_name']).strip("['']") for elem in main_input]

    html_str = """
    <!DOCTYPE html>
    <html>
    <body>

    <p>10 Drug's brand names:</p>
    <p>{brands}</p>

    </body>
    </html>
    """

    with open("templates/brand.html","w") as main_output:
        html_str_mod = html_str.format(brands=', '.join(brand_list))
        main_output.write(html_str_mod)

    return render_template('brand.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=1936)
