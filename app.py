import pickle
import flask
import pandas as pd

data = pd.read_csv("dataset/cardio_train.csv",sep = ';')
data = data.drop('id', axis = 1)
X = data.drop('cardio', axis = 1 )
#You can covert the target variable to numpy
y = data['cardio'].values


with open('models/finalized_pipeline5_model.pkl','rb') as f:
    fil = pickle.load(f)

loaded_model = fil.fit(X,y)
app = flask.Flask(__name__, template_folder='templates')
@app.route('/')
def main():
    return (flask.render_template('index.html'))

@app.route('/report')
def report():
    return (flask.render_template('report.html'))

@app.route("/Individual", methods=['GET', 'POST'])
def Individual():
    
    if flask.request.method == 'GET':
        return (flask.render_template('Individual.html'))
    
    if flask.request.method =='POST':
        
        #get input
        
        #age as integer
        age = int(flask.request.form['age'])
        #gender as integer
        gender = int(flask.request.form['gender'])
        #height as integer
        height = int(flask.request.form['height'])
        #weight as float
        weight = float(flask.request.form['weight'])
        #Systolic blood pressure as integer
        ap_hi = int(flask.request.form['ap_hi'])
        #Diastolic blood pressure as integer
        ap_lo = flask.request.form['ap_lo']
        #Cholesterol as integer
        cholesterol = int(flask.request.form['cholesterol'])
        #Glucose as  integer
        gluc = float(flask.request.form['gluc'])
        #Smoke as integer
        smoke = int(flask.request.form['smoke'])
        #Alcohol intake as integer
        alco = int(flask.request.form['alco'])
        #Physical activity as integer
        active = float(flask.request.form['active'])
        
        temp = pd.DataFrame(index=[1])
        #temp['fico'] = fico
        
        temp['age']=age
        temp['gender']=gender
        temp['height']= height
        temp['weight']=weight
        temp['ap_hi']=ap_hi
        temp['ap_lo']=ap_lo
        temp['cholesterol']=cholesterol
        temp['gluc'] = gluc
        temp['smoke']= smoke
        temp['alco']= alco
        temp['active']=active
        
        
        #create original output dict
        output_dict= dict()
        a = str(age) + " days "
        output_dict['Age'] = a
        if gender == 1:
           gen  = "Male"
        else:
           gen  = "Female"

        output_dict['Gender'] = gen
        h = str(height)+ " cm  "
        output_dict['Height'] = h
        w = str(weight)+ " kg "
        output_dict['Weight']=w
        output_dict['Systolic blood pressure'] = ap_hi
        output_dict['Diastolic blood pressure']= ap_lo
        if cholesterol == 1:
            chol = "Normal"
        elif cholesterol == 2:
            chol = "Above Normal"
        else:
            chol = " Well Above"
        output_dict['Cholesterol']= chol
        if gluc == 1:
            glu = "Normal"
        elif gluc == 2:
            glu = "Above Normal"
        else:
            glu = " Well Above"
        output_dict['Glucose'] = glu
        if smoke == 0:
            smok= "No"
        else:
            smok = "Yes"
        output_dict['Smoking'] = smok
        if alco == 0:
            alc = "No"
        else:
            alc = "Yes"
        output_dict['Alcohol intake'] = alc
        if active == 0:
            act = "No"
        else:
            act = "yes"
        output_dict['Physical activity'] = act
        
            
        #make prediction
        pred = loaded_model.predict(temp)
        
        if pred == 0:
            res = 'patient has no Cardiovascular Disease!'
        else:
            res = 'patient has Cardiovascular Disease!'
                
        #render form again and add prediction
        return flask.render_template('Individual.html',
                                     original_input=output_dict,
                                     result=res,
                                     )
               
if __name__ == '__main__':
    app.run(debug=True)