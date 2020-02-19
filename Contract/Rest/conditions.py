from flaskapp import app, db
from flaskapp.models import Conditions
import json


@app.route("/v1/conditions", methods=["GET"])
def get_conditions():
    result = Conditions.query.all()
    returnvalue = {}
    print("hej")
    for condition in result:
        returnvalue[condition.name] = condition.desc
    response = app.response_class(response=json.dumps(returnvalue), mimetype="application/json")
    return response, 200
