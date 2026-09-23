from flask import Flask, request, jsonify
import util

util.load_saved_artifacts()
app = Flask(__name__)

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        "locations" : util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_prices', methods=['POST'])
def predict_home_prices():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = float(request.form['bhk'])
    bath = float(request.form['bath'])

    response = jsonify({
        "estimated_price" : util.get_estimated_prices(location, total_sqft, bhk, bath)
    })

    return response

if __name__ == "__main__":
    print("starting python flask server for home price prediction")
    app.run()