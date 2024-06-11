import webscrappy as wb
import Conectividadbd as db
import dashboard as dash

if __name__ == '__main__':
#Aqui trae las funciones del webscraping para nomas con variable guardar los Dataframes
    region = wb.webscrapingRegion()
    pokedex = wb.webscrapingPokedex()
    tipos = wb.WebscrappingTipos()

 # Aqui va hacer la conexion por eso importe la conectividad y llamando las funciones hace la importacion de datos
    conexion_db = db.conexion()
if conexion_db:
    db.importarDatosRegion(conexion_db,region)
    db.importarDatosPokedex(conexion_db, pokedex)
    db.importarDatosTipos(conexion_db, tipos)
    conexion_db.close()
    print('Conexión cerrada')

#aqui hara los dashboard para la visualizacion de los datos, Ojo me rebe el ejemplo del profe y por eso se ve super sencillo :(
    conexion = dash.conexion()
    if conexion:
        engine = dash.create_engine('mysql+mysqlconnector://root:password@localhost:3306/Pokemon')
        query_pokedex = "SELECT * FROM pokedex"
        query_tipos = "SELECT * FROM tipos"
        query_region = "SELECT * FROM region"

        data_pokedex = dash.pd.read_sql(query_pokedex, engine)
        data_tipos = dash.pd.read_sql(query_tipos, engine)
        data_regiones = dash.pd.read_sql(query_region, engine)
        app = dash.Dash(__name__)
        app.layout = dash.dibujar(data_pokedex, data_tipos, data_regiones)
        app.run(debug=True)
    else:
        print("No se pudo conectar a la base de datos")

