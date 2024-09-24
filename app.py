import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H3("Hola mundo"),
    dcc.Graph(
        id = 'Mi_primer_gráfico',
        figure = {
            'data' : [
                {'x':[1,2,3], 'y':[24,22,31], 'type':'bar', 'name':'bar'}
            ],
            'layout' : {
                'title' : 'Mi primer gráfico Jonathan 2'
            }
        }
    )
]

)

if __name__ == "__main__":
    app.run_server(debug=True)

