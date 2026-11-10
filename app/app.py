import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import requests
import json
from loguru import logger
import os


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

api_url = os.getenv('API_URL')
api_port = os.getenv('API_PORT')
api_url = "http://{}:{}/api/v1/predict".format(api_url, api_port)

app.layout = html.Div(
    [
    html.H6("Ingrese la información del cliente:"),
    html.Div(["Número de meses inactivo en los últimos 12 meses: ",
              dcc.Dropdown(id='inactivo', value='1',
                           options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])]),
    html.Br(),
    html.Div(["Número de servicios tomados por el cliente: ",
              dcc.Dropdown(id='servicios', value='1',
                           options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])]),
    html.Br(),
    html.Div(["Valor total de las transacciones: ",
              dcc.Input(id='transac', value='10', type='number')]),
    html.Br(),
    html.Div(["Número de transacciones: ",
              dcc.Input(id='num_transac', value='10', type='number')]),
    html.Br(),
    html.Button('Predecir', id='btn-predecir', n_clicks=0),
    html.Br(),
    html.Br(),
    html.H6(html.Div(id='resultado')),
    ]
)

@app.callback(
    Output(component_id='resultado', component_property='children'),
    Input(component_id='btn-predecir', component_property='n_clicks'),
    [State(component_id='inactivo', component_property='value'),
     State(component_id='servicios', component_property='value'),
     State(component_id='transac', component_property='value'),
     State(component_id='num_transac', component_property='value')]
)
def update_output_div(n_clicks, inactivo, servicios, transac, num_transac):
    if n_clicks == 0:
        return "Presiona Predecir para obtener el resultado."

    myreq = {
        "inputs": [
            {
            "Customer_Age": 57,
            "Gender": "M",
            "Dependent_count": 4,
            "Education_Level": "Graduate",
            "Marital_Status": "Single",
            "Income_Category": "$120K +",
            "Card_Category": "Blue",
            "Months_on_book": 52,
            "Total_Relationship_Count": int(servicios) if servicios else 1,
            "Months_Inactive_12_mon": int(inactivo) if inactivo else 1,
            "Contacts_Count_12_mon": 2,
            "Credit_Limit": 25808,
            "Total_Revolving_Bal": 0,
            "Avg_Open_To_Buy": 25808,
            "Total_Amt_Chng_Q4_Q1": 0.712,
            "Total_Trans_Amt": int(transac) if transac else 0,
            "Total_Trans_Ct": int(num_transac) if num_transac else 0,
            "Total_Ct_Chng_Q4_Q1": 0.843,
            "Avg_Utilization_Ratio": 0
            }
        ]
      }
    headers = {"Content-Type": "application/json", "accept": "application/json"}

    response = requests.post(api_url, data=json.dumps(myreq), headers=headers)
    data = response.json()
    logger.info("Response: {}".format(data))

    result = "ALTO riesgo de abandono" if round(data["predictions"][0]) == 1 else "BAJO riesgo de abandono"

    return result


if __name__ == '__main__':
    logger.info("Running dash")
    app.run_server(debug=True)