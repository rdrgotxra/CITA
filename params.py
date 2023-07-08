params_ZAN = {"coef_min": None, "coef_bas": 1.0, "coef_max": 1.0}
params_ZDS = {"coef_min": 0.1, "coef_bas": 1.0, "coef_max": 2.0}
params_ZC = {"coef_min": 0.5, "coef_bas": 1.0, "coef_max": 5.0}
params_ZRU1 = {"coef_min": 0.4, "coef_bas": 1.0, "coef_max": 5.0}
params_ZAC = {"coef_min": 0.4, "coef_bas": 1.0, "coef_max": 5.0}


def get_params(mun, lote):
    zona_tipo = lote["properties"]["zoneamento"][0]["tipo"]

    match zona_tipo:
        case "Zona Centro - ZC": params = params_ZC
        case "Zona de Ambiente Natural - ZAN": params = params_ZAN
        case "Zona de Desenvolvimento Sustentável - ZDS": params = params_ZDS
        case "Zona de Reestruturação Urbana - ZRU 1": params = params_ZRU1
        case "Zona de Reestruturação Urbana - ZRU 2": params = params_ZAC
        case "Zona do Ambiente Construído - ZAC": params = params_ZAC

    potencial_construtivo = int(lote["properties"]["area_lote"])*params["coef_max"]
    eva = {
        "coef_min": params["coef_min"],
        "coef_bas": params["coef_bas"],
        "coef_max": params["coef_max"],
        "potencial_construtivo": potencial_construtivo,
    }
        
    return eva