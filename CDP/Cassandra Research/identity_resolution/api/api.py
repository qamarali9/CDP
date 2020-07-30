import flask
from flask import request, jsonify

from cassandra_db_calls import connection
from cassandra_db_calls import identities
from cassandra_db_calls import config

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/get_id', methods=['GET','POST'])
def api_get_id():
    #print("request.json : {}".format(request.json))
    #print("request.args : {}".format(request.args))
    #print("request.data : {}".format(request.data))
    #print("request.form : {}".format(request.form))


    if 'identity' in request.json:
        identity = str(request.json['identity'])
    else:
        return "Error: No identity field provided. Please specify an id."
    
    if 'identity_type' in request.json:
        identity_type = str(request.json['identity_type'])
    else:
        return "Error: No identity_type field provided. Please specify an identity_type."

    if 'cid' in request.json:
        cid = int(request.json['cid'])
    else:
        return "Error: No cid field provided. Please specify an cid."

    uid,exists = identities.get_uid(connection.get_connection({},config.CASSANDRA_KEYSPACE),identity,identity_type,cid)
    return jsonify({'uid':uid, 'exists':exists})


app.run()
