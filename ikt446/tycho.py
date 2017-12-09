from pymongo import MongoClient
import flask as f
from flask import request as fr


mongo = MongoClient('localhost')
db = mongo['tycho']

app = f.Flask(__name__)

@app.route('/')
def home_page():

    diseases = db['diseases']
    states = db['states']

    dlist = []
    for d in diseases.find({},{"_id":0}):
        dlist.append(d['disease'])
    slist = []
    for s in states.find({},{"_id":0}):
        slist.append(s.values()[0])

    return f.render_template('index.html', diseases=dlist, states=slist)

@app.route('/disease', methods=['GET', 'POST'])
def disease_case():

    d = fr.form['diseases']
    output = []
    for i in db[d].find({},{"_id":0, "year":1, "week":1, "loc":1, "number":1}):
        output.append(i)


    return f.render_template('disease.html', output=output)

@app.route('/result', methods=['POST'])
def conjugate_case():
    d = fr.form['diseases']
    s = fr.form['states']
    y = fr.form['years']
    w = fr.form['weeks']
    output = []
    query = {}

    if not s == "all":
        query['loc'] = s.upper()
    if not y == "all":
        query['year'] = int(y)
    if not w == "all":
        query['week'] = int(w)

    for i in db[d].find(query,{"_id":0, "year":1, "week":1, "loc":1, "number":1}):
            output.append(i)

    if d == "all":
        for i in db['cases_per_year_and_state'].find({}, {"_id": 0, "year": 1, "loc": 1, "number": 1}):
            output.append(i)




    #total_cases_per_year
    #total_cases_per_state
    #cases_per_year_and_state


    return f.render_template('result.html', output=output)

app.run()


#document.ready