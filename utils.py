from geopy.geocoders import Nominatim
from shapely import union_all, union


def get_coords(endereco: str):
    loc = Nominatim(user_agent="appvia").geocode(endereco)
    if loc is None: return None
    return f'SRID=4326;POINT({loc.longitude} {loc.latitude})'


def check_q(q):
    try:
        int(q)
        if len(q) == 7: return "seq_imovel"
        if len(q) == 14: return "id_prefeitura"
        else: return "inválido"
    except:
        return "endereco"
    
