# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
import requests
import ast
import yaml
# create the application object
app = Flask(__name__)

user = ""
firstName = "hi"

account = {
    "marytan" : "mary",
    "limzeyang" : "limz",
    "prasannaghali" : "pras"
}

accountID_dict = {
    "marytan" : "10",
    "limzeyang" : "74",
    "prasannaghali" : "32"
}

customerID_dict = {
    "marytan" : "2",
    "limzeyang" : "1",
    "prasannaghali" : "3"
}

# use decorators to link the function to a url
@app.route('/')
def home():
    url = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/credit/2"

    headers = {
        'identity' : 'Group26',
        'token': 'c6d25aa1-2b48-48e6-ab19-89ef6bed22e2'
    }

    try:
        response = requests.get(url, headers=headers)
        # return response
    except requests.ConnectionError:
       return "Connection Error"  
    return render_template('welcome.html')

    # if user == "":
    #     return "Hello, World!"  # return a string
    # else:
    #     string = "Hello " + user
    #     return string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/viewMonthly')
def viewMonthly():
    # return render_template('home.html',value = firstName)

    url3 = 'http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/transactions/' + accountID_dict[user] + '?from=01-01-2018&to=12-31-2018'

    headers = {
    'identity' : 'Group26',
    'token': 'c6d25aa1-2b48-48e6-ab19-89ef6bed22e2'
    }

    params = {
        'from' : '01-01-2018',
        'to' : '12-31-2018'
    }
    response3 = requests.get(url3, headers = headers, params = params)
    # response3_dict = yaml.load(response3.content[1:-1])
    jan = 0.0
    feb = 0.0
    mar = 0.0
    apr = 0.0
    may = 0.0
    jun = 0.0
    jul =0.0
    aug = 0.0
    sep = 0.0
    octb = 0.0
    nov =0.0
    dec = 0.0

    # lst = ast.literal_eval(response3.content)[0]['date'][0:2]
    for dct in ast.literal_eval(response3.content):

        # dct = yaml.load(i)
        if dct["type"] == "DEBIT" and dct["date"][5:7] == "01":
            jan += float(dct["amount"])
        elif dct["type"] == "DEBIT" and dct["date"][5:7] == "02":
            feb += float(dct["amount"])
        elif dct["type"] == "DEBIT" and dct["date"][5:7] == "03":
            mar += float(dct["amount"])
        elif dct["type"] == "DEBIT" and dct["date"][5:7] == "04":
            apr += float(dct["amount"])
        elif dct["type"] == "DEBIT" and dct["date"][5:7] == "05":
            may += float(dct["amount"])
        elif dct["type"] == "DEBIT" and dct["date"][5:7] == "06":
            jun += float(dct["amount"])
        elif dct["type"] == "DEBIT" and dct["date"][5:7] == "07":
            jul += float(dct["amount"])
        elif dct["type"] == "DEBIT" and dct["date"][5:7] == "08":
            aug += float(dct["amount"])
        elif dct["type"] == "DEBIT" and dct["date"][5:7] == "09":
            sep += float(dct["amount"])
        elif dct["type"] == "DEBIT" and dct["date"][5:7] == "10":
            octb += float(dct["amount"])
        elif dct["type"] == "DEBIT" and dct["date"][5:7] == "11":
            nov += float(dct["amount"])
        elif dct["type"] == "DEBIT" and dct["date"][5:7] == "12":    
            dec += float(dct["amount"])
    return render_template('viewMonthly.html', jan = jan, feb = feb, mar=mar,apr=apr,may=may,jun=jun,jul=jul, aug=aug,sep=sep,octb=octb,nov=nov,dec=dec, firstName = firstName)



    # return render_template('home.html', value = lst)

    # return render_template('viewMonthly.html', firstName = firstName)

@app.route('/userInfo')
def userInfo():
    url1 = 'http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/' + customerID_dict[user] +'/details'
    url2 = 'http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/deposit/' + customerID_dict[user]

    headers = {
        'identity' : 'Group26',
        'token': 'c6d25aa1-2b48-48e6-ab19-89ef6bed22e2'
    }

    # params = {
    #     'from' : '12-01-2018',
    #     'to' : '01-01-2019'
    # }
    try:
        response1 = requests.get(url1, headers=headers)#, params = params)
        response2 = requests.get(url2, headers=headers)
        user_dict1 = yaml.load(response1.content)
        user_dict2 = yaml.load(response2.content[1:-1])

        gender = user_dict1["gender"]
        dob = user_dict1["dateOfBirth"][:10]
        firstName = user_dict1["firstName"]
        lastName = user_dict1["lastName"]
        accType = user_dict2["type"]
        accName = user_dict2["displayName"]
        accID = user_dict2["accountId"]
        accNo = user_dict2["accountNumber"]

        # number = len(response.content)
    except requests.ConnectionError:
       return "Connection Error"  
            # return render_template('welcome.html')
            # return render_template('home.html',user = user, value = type(response2.content))

    return render_template('userInfo.html',gender = gender, dob = dob, firstName = firstName, lastName = lastName, accType = accType, accName = accName, accID = accID, accNo = accNo)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        global user
        user = request.form['username']
        if user not in account or request.form['password'] != account[user]:
        # if request.form['username'] != 'shengxiang' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            # url = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/marytan"
            url1 = 'http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/' + customerID_dict[user] +'/details'
            url2 = 'http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/deposit/' + customerID_dict[user] 

            headers = {
                'identity' : 'Group26',
                'token': 'c6d25aa1-2b48-48e6-ab19-89ef6bed22e2'
            }

            # params = {
            #     'from' : '12-01-2018',
            #     'to' : '01-01-2019'
            # }
            try:
                response1 = requests.get(url1, headers=headers)#, params = params)
                response2 = requests.get(url2, headers=headers)
                # user = request.form['username']
                user_dict1 = yaml.load(response1.content)
                user_dict2 = yaml.load(response2.content[1:-1])

                gender = user_dict1["gender"]
                dob = user_dict1["dateOfBirth"][:10]
                global firstName 
                firstName= user_dict1["firstName"]
                lastName = user_dict1["lastName"]
                accType = user_dict2["type"]
                accName = user_dict2["displayName"]
                accID = user_dict2["accountId"]
                accNo = user_dict2["accountNumber"]

                # number = len(response.content)
            except requests.ConnectionError:
               return "Connection Error"  
            # return render_template('welcome.html')
            # return render_template('home.html',user = user, value = type(response2.content))

            return render_template('userInfo.html',gender = gender, dob = dob, firstName = firstName, lastName = lastName, accType = accType, accName = accName, accID = accID, accNo = accNo)
            # return redirect(url_for('home'))
    return render_template('login.html', error=error)



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)