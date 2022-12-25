#importing all the libraries needed for this layout
import dash
from dash import dcc
import os
from dash import html
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
import sqlite3
import time#importing time library
import PIL #importing pillow for image processing
from PIL import Image#importing image from pillow library
import skimage#importing skimage library
import os#importing os library
import time#importing time library
import pickle 
import pyreadstat as psav
from app import app
from sklearn.preprocessing import Normalizer


layout = html.Div(style={'backgroundColor': 'white'},children=[
    dbc.Row([html.H4('Please upload the picture using the below and wait for result',className="text-center"),
        ]),
   dcc.Upload(
       id='upload-data',
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
       multiple=False
   ),
        dbc.Row([html.H4(id='time_taken',style={'textAlign':'center'})],justify="center",className="mt-3",)     
        ])
#this runs when the button is pressed
@app.callback([Output(component_id='time_taken', component_property='children')],
              [Input(component_id='upload-data', component_property='contents')])
#code to take input and update the data
def update_graphs(selected_date = 0):
    ctx = dash.callback_context
    out = []
    msg = ''
    if selected_date == 0:
        return ' '
    else:
        #changing the working directory for loading the model
        model = 'D://DKIT//dissertation//Dataset_of_Tomato_Leaves//plantvillage//Preprocessed_data//svm_norm.sav'
        #loading the model
        loaded_model = pickle.load(open(model, 'rb'))
        data1 = []
        data = []
        #reading input image
        image = selected_date
        #changing the dimensions
        size = (64,64)
        image = image.resize(size)
        #extracting RGB values
        data1 = image.convert('RGB')
         #saving it to the array
        data = np.array(data1)
        data = data.ravel()
        scaler = Normalizer()
        scaled_data = scaler.fit_transform(data)
        prediction = loaded_model.predict(data)
        return prediction