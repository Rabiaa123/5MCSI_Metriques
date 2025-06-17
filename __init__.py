from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from collections import Counter
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': round(temp_day_value, 2)})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mon_histogramme():
    return render_template("histogramme.html")

@app.route("/contact/")
def contact_form():
    return render_template("contact.html")

@app.route('/api/commits/')
def api_commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = urlopen(url)
    raw_data = response.read()
    json_data = json.loads(raw_data.decode('utf-8'))

    minutes_list = []
    for commit in json_data:
        date_str = commit.get('commit', {}).get('author', {}).get('date')
        if date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes_list.append(date_obj.minute)

    count_per_minute = dict(Counter(minutes_list))
    results = [{'minute': minute, 'commits': count} for minute, count in sorted(count_per_minute.items())]

    return jsonify(results=results)

# Route pour la page avec le graphique
@app.route('/commits/')
def commits():
    return render_template("commits.html")
  
if __name__ == "__main__":
  app.run(debug=True)
