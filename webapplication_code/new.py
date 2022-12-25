import datetime
import numpy as np
import pandas as pd
import base64
from io import BytesIO
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import PIL #importing pillow for image processing
from PIL import Image#importing image from pillow library
import skimage#importing skimage library
import os#importing os library
import time#importing time library
import pickle 
import pyreadstat as psav
from app import app
from sklearn.preprocessing import Normalizer
import io

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H2(
        # code for initial column in the navigation bar
        "Tomato leaf disease detection using Machine Learning",style={'textAlign':'center','background-color':'#ff0066'}
    ),
    html.H5(
        # code for initial column in the navigation bar
        "This application is capable to detect 9 tomato leave diseases and healthy leaves with 85 percent accuracy.",style={'textAlign':'center'}
    ),
    html.H6(
        # code for initial column in the navigation bar
        "Please drop a tomato leaf image in the below box to check the disease.",style={'textAlign':'center'}
    ),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])

def parse_contents(contents, filename, date):
    model = 'D://DKIT//dissertation//Dataset_of_Tomato_Leaves//plantvillage//Preprocessed_data//svm_norm.sav'
    
    loaded_model = pickle.load(open(model, 'rb'))
    
    
    encoded_image = contents.split(",")[1]
    decoded_image = base64.b64decode(encoded_image)
    img = Image.open(io.BytesIO(decoded_image))
    img = img.resize((64,64))
    #img1,img2 = Image.open(img).convert('RGB')
    
    data1 = []
    data = []
    #changing the dimensions
    size = (64,64)
    data = np.array(img)
    #image = image.resize(size)
    #saving it to the array
    #data = np.array(data1)
    data = data.ravel()
    scaler = Normalizer()
    '''testing_data = pd.DataFrame()
    testing_data.loc[len(testing_data)] = data
    test_data = testing_data.values'''
    testing_data = []
    testing_data.append(data)
    scaled_data = scaler.fit_transform(testing_data)
    
    prediction = loaded_model.predict(scaled_data)
    prediction = prediction[0].replace('_',' ')
    return html.Div([
        html.H6(filename),
       # html.H6(datetime.datetime.fromtimestamp(date)),
        

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Disease Predicted by the machine learning model is:'),
        html.H4(prediction)
    ])

@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)