import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table
import Conectividadbd as bd
from sqlalchemy import create_engine

def dibujar(data_pokedex: pd.DataFrame, data_tipos: pd.DataFrame, data_regiones: pd.DataFrame):
    fig_pokedex = px.scatter(data_pokedex, x='Numero_de_pokemonn', y='Numero_de_pokedex', title='Pokémon')
    fig_pokedex.update_layout(xaxis_title="Nombre de Pokémon", yaxis_title="Número de Pokedex")
    fig_tipos = px.bar(data_tipos, x='Nombre', title='Tipos de Pokémon')
    fig_tipos.update_layout(xaxis_title="Tipo de Pokémon", yaxis_title="Frecuencia")
    fig_regiones = px.bar(data_regiones, x='Nombre', title='Regiones de Pokémon')
    fig_regiones.update_layout(xaxis_title="Región de Pokémon", yaxis_title="Frecuencia")


    body = html.Div([
        html.H2("Datos de Pokémon", style={"textAlign": "center", "color": "Yellow"}),
        html.P("Visualización de datos de la Pokedex, Tipos y Regiones de Pokémon."),
        html.Hr(),
        dcc.Graph(figure=fig_pokedex),
        dcc.Graph(figure=fig_tipos),
        dcc.Graph(figure=fig_regiones),
        html.H3("Tabla de Pokedex"),
        dash_table.DataTable(data=data_pokedex.to_dict("records"), page_size=5),
        html.H3("Tabla de Tipos"),
        dash_table.DataTable(data=data_tipos.to_dict("records"), page_size=5),
        html.H3("Tabla de Region"),
        dash_table.DataTable(data=data_regiones.to_dict("records"), page_size=5)
    ], style={"background": "blue"})

    return body

if __name__ == "__main__":
    conexion = bd.conexion()
    if conexion:
        engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/Pokemon')
        query_pokedex = "SELECT * FROM pokedex"
        query_tipos = "SELECT * FROM tipos"
        query_region = "SELECT * FROM region"

        data_pokedex = pd.read_sql(query_pokedex, engine)
        data_tipos = pd.read_sql(query_tipos, engine)
        data_regiones = pd.read_sql(query_region, engine)
        app = Dash(__name__)
        app.layout = dibujar(data_pokedex, data_tipos, data_regiones)
        app.run(debug=True)
    else:
        print("No se pudo conectar a la base de datos")