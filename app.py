from flask import Flask, render_template, request, redirect, url_for
# from flask_pymongo import PyMongo
import pymongo
import scrape_windturbine
import jsonify
from flask_wtf import Form
from wtforms import StringField

# Create an instance of Flask
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'our very hard to guess secretfir'

# # Use PyMongo to establish Mongo connection
# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.windturbine_db
collection = db.items


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    destination_data = db.items.find_one()
    # print(destination_data)
    # Return template and data
    return render_template("index.html", wt=destination_data,tables=destination_data['facts_html'])



# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    db.items.drop()
    # Run the scrape function
    wt_data = scrape_windturbine.scrape()
    collection.insert_one(wt_data)
    return redirect("/") # Redirect back to home page

# Route that will trigger the wind turbine  function
@app.route("/map_data")
def wt_map_data():
    destination_data = db.items.find_one()
    # print(destination_data['json_facts_html'])
    return destination_data['json_facts_html']
    
# Route that will trigger the map
@app.route("/map")
def wt_map():
    return render_template("/map_index.html")
# More powerful approach using WTForms
class QueryForm(Form):
    wind_speed = StringField('Wind Speed (m/s) :')
    motor_torque = StringField('Motor Torque (N-m) :')
    generator_temperature = StringField('Generator Temperature (°C) :')
    atmospheric_pressure = StringField('Atmospheric Pressure (Pascal) :')
    area_temperature = StringField('Area Temperature °C :')

@app.route("/predictPower", methods=['GET', 'POST'])
def wt_predict():
    error = ""
    result=""
    form = QueryForm(request.form)
# <!-- ['wind_speed(m/s)', 'motor_torque(N-m)', 'generator_temperature(°C)',
#        'atmospheric_pressure(Pascal)', 'area_temperature -->
    if request.method == 'POST':
        wind_speed = request.form['wind_speed']
        motor_torque = form.motor_torque.data
        generator_temperature=form.generator_temperature.data
        atmospheric_pressure=form.atmospheric_pressure.data
        area_temperature=form.area_temperature.data
        if len(wind_speed) == 0 or len(motor_torque) == 0 or len(generator_temperature)==0 or len(atmospheric_pressure)==0 or len(area_temperature)==0:
             error = "Please supply both first and last name"
        else:
            import pickle
            from sklearn.ensemble import RandomForestRegressor
            wt_model=pickle.load(open('dataset/wt_model','rb'))
            print("predicting")
            result=wt_model.predict([[wind_speed,motor_torque,generator_temperature,atmospheric_pressure,area_temperature]])
            print("RESULT ",result)
            return render_template('predict_index.html',result=result,form=form)
        #     # display result of model
    # else:
    #     result=request.args.get('result')
    #     return render_template('predict_index.html', form=form,result=result, message=error)

    return render_template('predict_index.html', form=form,result=result, message=error)
 

if __name__ == "__main__":
    app.run(debug=True)
