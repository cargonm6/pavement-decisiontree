import pandas as pd

table_performance = None

dict_damages = {
    # Grietas de cocodrilo
    "GATOR_CRACK_A_L": 1, "GATOR_CRACK_A_M": 2, "GATOR_CRACK_A_H": 3,
    # Surgencias de finos
    "PUMPING_A_H": 4,
    # Corrugación (ondulaciones)
    "CORRUGATION_A_L": 5, "CORRUGATION_A_M": 6, "CORRUGATION_A_H": 7,
    # Depresión (hundimiento)
    "DEPRESSION_A_L": 8, "DEPRESSION_A_M": 9, "DEPRESSION_A_H": 10,
    # Grietas de borde (en el eje)
    "EDGE_CRACK_L_L": 11, "EDGE_CRACK_L_M": 12, "EDGE_CRACK_L_H": 13,
    # Grietas reflejadas
    "JOINT_REFL_CRACK_L_L": 14, "JOINT_REFL_CRACK_L_M": 15, "JOINT_REFL_CRACK_L_H": 16,
    # Grietas longitudinales y transversales
    "LONG_TRANS_CRACK_L_L": 17, "LONG_TRANS_CRACK_L_M": 18, "LONG_TRANS_CRACK_L_H": 19,
    # Pulimiento de agregados (pavimento deslizante)
    "POLISH_AGG_A_H": 20,
    # Huecos (baches)
    "POTHOLES_NO_L": 21, "POTHOLES_NO_M": 22, "POTHOLES_NO_H": 23,
    # Ahuellamiento (roderas)
    "RUTTING_A_L": 24, "RUTTING_A_M": 25, "RUTTING_A_H": 26,
    # Desplazamiento vertical (escalón)
    "SHOVING_A_L": 27, "SHOVING_A_M": 28, "SHOVING_A_H": 29,
    # Desprendimiento de agregados
    "RAVELING_A_M": 30,
    # Exudaciones
    "BLEEDING_A_M": 31
}

dict_performances = {
    1: "Fresado y reposición hasta la capa inferior",
    2: "Fresado y reposición hasta la capa intermedia",
    3: "Fresado y reposición en la capa superior",
    4: "Sellado de grietas",
    5: "Capa de recrecimiento",
    6: "Fresado capa de rodadura"
}


def check(list_1, list_2):
    """
    Comprueba si cualquier elemento de una lista se encuentra en otra
    :param list_1: lista 1
    :param list_2: lista 2
    :return: boolean
    """
    if any(x in list_1 for x in list_2):
        return True
    return False


def highest_priority(p_plist):
    """
    Elimina actuaciones en favor de las prioritarias
    :param p_plist: lista de actuaciones
    :return: lista de actuaciones
    """
    # Si existen actuaciones de mayor prioridad que 6
    if check([6], p_plist) and (check([3], p_plist) or check([2], p_plist) or check([1], p_plist)):
        p_plist.pop(p_plist.index(6))

    # Si existen actuaciones de mayor prioridad que 3
    if check([3], p_plist) and (check([2], p_plist) or check([1], p_plist)):
        p_plist.pop(p_plist.index(3))

    # Si existen actuaciones de mayor prioridad que 2
    if check([2], p_plist) and check([1], p_plist):
        p_plist.pop(p_plist.index(2))

    return p_plist


def initial_performance(p_damages):
    """
    Obtiene la lista de actuaciones para un conjunto de daños de entrada
    :param p_damages:
    :return:
    """
    p_dlist = []  # Lista numérica de daños
    p_plist = []  # Lista numérica de actuaciones

    # Obtenemos el número identificativo de cada tipo de daño
    for p_damage in p_damages:
        p_dlist.append(dict_damages[p_damage])

    # Ordenamos los daños
    p_dlist.sort()

    # Para cada fila (núm. de daño)
    for i in p_dlist:

        # Para cada columna (núm. de daño)
        for k in p_dlist:

            # Obtenemos la actuación. Si es nulo, lo rechazamos. Si son dos, las separamos
            performance = table_performance.iloc[i, k]

            if pd.isna(performance):
                continue

            if isinstance(performance, str):
                p_plist.extend(int(x) for x in performance.split("+"))
            else:
                p_plist.append(int(performance))

    # Elimina actuaciones repetidas
    p_plist = list(dict.fromkeys(p_plist))

    # Prioriza actuaciones
    p_plist = highest_priority(p_plist)

    return p_plist


if __name__ == "__main__":
    table_performance = pd.read_csv("actuaciones.csv", delimiter=";", header=None)
    damages = ["GATOR_CRACK_A_M", "EDGE_CRACK_L_H", "BLEEDING_A_M", "PUMPING_A_H"]

    performances = initial_performance(damages)

    print("\nActuaciones:")
    for p in performances:
        print("-", p, dict_performances[p])
