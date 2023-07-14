from sqlalchemy import create_engine, MetaData, Table, select, func
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely import to_geojson
import json
from utils import get_coords, check_q
from params import get_params

# DB_URL = "postgresql+psycopg2://admin:senha2023@127.0.0.1/appvia"
DB_URL = "postgresql+psycopg2://postgres:senha2023@34.95.208.183/postgres"

engine = create_engine(DB_URL)

metadata = MetaData()


def get_zonas(mun: str, geom_lote: Geometry = None):
    zonas = []
    layers = ["zonas","zec", "zeis", "zeph", "pttsn", "iep", "pe"]

    for layer in layers:
        table = Table(layer, metadata, schema=mun, autoload_with=engine)
        geom_layer = func.ST_Transform(table.c.geom, 4326)
        stmt = select(table, geom_layer)

        if geom_lote:
            stmt = stmt.filter(func.ST_Intersects(geom_layer, geom_lote))

        with engine.connect() as conn:
            result = conn.execute(stmt)

        for row in result:
            zona = {
                "tipo": row.tipo,
                "nome": row.nome,
                "obs": row.obs,
            }
            zonas.append(zona)
                
    return zonas


def get_lotes(mun: str, q: list[str], zonas: bool = True, params: bool = True):
    table = Table("lotes", metadata, schema=mun, autoload_with=engine)
    lotes = {"type": "FeatureCollection", "features": []}

    for q_value in q:
        stmt = select(table, func.ST_Transform(table.c.geom, 4326))

        match check_q(q_value):
            case "id_prefeitura":
                stmt = stmt.filter(table.c.id_prefeitura == q_value)
            case "seq_imovel":
                stmt = stmt.filter(table.c.seq_imovel == int(q_value))
            case "endereco":
                coords = get_coords(q_value)
                stmt = stmt.filter(func.ST_Contains(table.c.geom, coords))
            case "invalido":
                print("ENDEREÇO INVÁLIDO")

        with engine.connect() as conn:
            row = conn.execute(stmt).one_or_none()
        
        if row is not None:
            geom = to_shape(row.geom)
            geom = json.loads(to_geojson(geom))
            lote = {
                "type": "Feature",
                "properties": {
                    "id_prefeitura": int(row.id_prefeitura),
                    "endereco": row.endereco,
                    "area_lote": row.area_lote,
                    "testada_principal": row.testada_principal,
                    "seq_imovel": row.seq_imovel,
                    "situação_imovel": row.situacao_imovel,
                    "nome_edif": row.nome_edif,
                    "tipo_empreend": row.tipo_empreend,
                    "area_total_constr": row.area_total_constr,
                    "ano_constr": row.ano_constr,
                    "qtd_pavimentos": row.qtd_pavimentos,
                    "qtd_un_hab_com": row.qtd_un_hab_com,
                    "qtd_blocos": row.qtd_blocos,
                    "tipo_residuo": row.tipo_residuo,
                },
                "geometry": geom
            }

            if zonas: lote["properties"]["zoneamento"] = get_zonas(mun, row.geom)
            if params: lote["properties"]["parametros"] = get_params(mun, lote)

            lotes["features"].append(lote)
    
    return lotes
