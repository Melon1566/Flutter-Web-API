import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
import simplejson as json
import datetime as datetime
from datetime import timedelta
import requests
import secrets
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
import concurrent.futures
import operator
import helpers

# OUR SOURCE FILES


accountsEndpoint = "vsbl-prod.cluster-ch0dsenirhlb.us-east-1.rds.amazonaws.com"


def defaultconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


################IF running locally copy the section below and replace above the first if statement################################################
""" 

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/AppDataHandler', methods=['POST', 'GET'])
def requestHandler():
    requestData = request.get_json() 

"""


##################################################################


# IF deploying to production, lambda use this code section to declare the handler otherwise use the above section without passed parameters
""" 
def requestHandler(event, context):
    body = ""
    if(event.get("body") is bytes):
        body = event.get("body").decode("utf-8")
    else:
        body = event.get("body")
    
    requestData = json.loads(body) 
"""
######################################################################################

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/AppDataHandler', methods=['POST', 'GET'])
def requestHandler():
    requestData = request.get_json() 


    ###################################################################################



    ###################################################################################
