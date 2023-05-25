from flask import Flask,render_template,request
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "KT2aERFf97wqhPX15pJrcv1GmNLMdg3Lkm02mA7j4xs7"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/login', methods=["POST"])
def login():
    gr=request.form["gr"]
    gi=request.form["gi"]
    sm1=request.form["sm1"]
    sm2=request.form["sm2"]
    sm3=request.form["sm3"]
    
    t=[[float(gr),float(gi),float(sm1),float(sm2),float(sm3)]]
    
    payload_scoring = {"input_data": [{"fields": ["f0","f1","f2","f3","f4"], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/58a4b900-8022-4391-b224-e7a1281870f8/predictions?version=2023-05-20', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    #print(response_scoring.json())
    pred =response_scoring.json()
    print(pred)
    output=pred['predictions'][0]['values'][0][0]
    print(output)
    return render_template("index.html",y="the predicted profit is "+ str(output))
    


@app.route('/user')
def User():
    return 'Hello User'

if __name__ == "__main__":
    app.run(debug=True, port =8080)