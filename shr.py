import pandas as pd
import numpy as np
from temp1 import NYpreprocess 
import numpy
from sklearn.preprocessing import StandardScaler
from flask import Flask,abort,jsonify,request
import _pickle as pickle
from sklearn.externals import joblib



clf = joblib.load('final_model.pkl') 

app=Flask(__name__)

@app.route('/')
def index():
	return "Hello"


@app.route('/api',methods=['POST','GET'])
def make_predict():
        data=request.get_json(force=True)
        predict_request=np.array([data["vendor_id"],data["pickup_datetime"],data["passenger_count"],data["pickup_longitude"],data["pickup_latitude"],data["dropoff_longitude"],data["dropoff_latitude"],data["store_and_fwd_flag"],data["trip_duration"]])

        # changing the shape of numpy array
        predict_request=predict_request.reshape((1,9))

        #converting into pandas DataFrame 
        convert_to_pandas=pd.DataFrame(predict_request,columns=["vendor_id","pickup_datetime","passenger_count","pickup_longitude","pickup_latitude","dropoff_longitude","dropoff_latitude","store_and_fwd_flag","trip_duration"])
        print(convert_to_pandas.dtypes)  
        

        # converting dataframe values into numeric values
        convert_to_pandas[['vendor_id','passenger_count','pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','trip_duration']] = convert_to_pandas[['vendor_id','passenger_count','pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','trip_duration']].apply(pd.to_numeric)

        print(convert_to_pandas.dtypes)  



       
        # initilizing the class 
        myclass=NYpreprocess()
        processed_data=myclass.start_preprocess(convert_to_pandas.drop("trip_duration",axis=1))
        print(processed_data.head())
        
        # importing the the saved mean and variance of training dataset
        mean=np.array(pd.read_csv("mean_values.csv")).reshape(1,25)
        var=np.array(pd.read_csv("var_values.csv")).reshape(1,25)

        #Standardizing the test datapoint  
        X_test=(processed_data-mean)/var

        #giving the data for prediction
        y_pred=clf.predict(X_test)
        print(y_pred)
        #returning the output as a json
        print(y_pred[0])
        return jsonify(result=y_pred[0])
	
if __name__=='__main__':
	app.run(host= '0.0.0.0',debug=True,port=9000)
    
