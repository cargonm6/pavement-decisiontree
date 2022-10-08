import numpy as np
import pandas as pd

path_table_performances = "./csv/actuaciones.csv"
path_table_trf_category = "./csv/categorias_trafico.csv"
path_table_road_surface = "./csv/firmes.csv"
path_table_df_threshold = "./csv/umbral_deflexion.csv"
path_table_df_thickness = "./csv/espesor_mezcla_nueva.csv"

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
    # Si existen actuaciones de mayor prioridad que 6, la retiramos (casos 1, 2, 3)
    if check([6], p_plist) and (check([3], p_plist) or check([2], p_plist) or check([1], p_plist)):
        p_plist.pop(p_plist.index(6))

    # Si existen actuaciones de mayor prioridad que 3, la retiramos (casos 1, 2)
    if check([3], p_plist) and (check([2], p_plist) or check([1], p_plist)):
        p_plist.pop(p_plist.index(3))

    # Si existen actuaciones de mayor prioridad que 2, la retiramos (caso 1)
    if check([2], p_plist) and check([1], p_plist):
        p_plist.pop(p_plist.index(2))

    return p_plist


def initial_performance(p_damages):
    """
    Obtiene la lista de actuaciones para un conjunto de daños de entrada
    :param p_damages:
    :return:
    """
    p_dlist = []  # Lista numérica de daños (damage list)
    p_plist = []  # Lista numérica de actuaciones (performance list)

    table_performance = pd.read_csv(path_table_performances, delimiter=";", header=None)

    # Obtenemos el número identificativo de cada tipo de daño, y los ordenamos
    for p_damage in p_damages:
        p_dlist.append(dict_damages[p_damage])

    p_dlist.sort()

    # Para cada fila (núm. de daño)
    for p_i in p_dlist:

        # Para cada columna (núm. de daño)
        for p_k in p_dlist:

            # Obtenemos la actuación. Si es nula, pasamos. Si son dos, las separamos.
            performance = table_performance.iloc[p_i, p_k]

            if pd.isna(performance):
                continue
            elif isinstance(performance, str):
                p_plist.extend(int(x) for x in performance.split("+"))
            else:
                p_plist.append(int(performance))

    # Elimina actuaciones repetidas, y prioriza actuaciones
    p_plist = list(dict.fromkeys(p_plist))
    p_plist = highest_priority(p_plist)

    return p_plist


def get_traffic_category(p_imd: float) -> str:
    """
    Obtiene la categoría de tráfico pesado a partir del IMDp
    Fuente: Norma 6.1 IC (p. 15, tablas 1.A-1.B)
    :param p_imd:
    :return:
    """
    p_table = pd.read_csv(path_table_trf_category, delimiter=";", index_col=0)

    for column in p_table:
        imd_min = p_table.loc["IMD_min", column] if not np.isnan(p_table.loc["IMD_min", column]) else 0
        imd_max = p_table.loc["IMD_max", column] if not np.isnan(p_table.loc["IMD_max", column]) else np.inf

        if imd_min <= p_imd < imd_max:
            return column

    return ""


def get_pavement_layers(p_trf_category: str) -> list:
    """
    Obtiene las capas del firme a partir de la categoría de tráfico pesado
    Fuente: Norma 6.1 IC (pp. 22-23, figuras 2.1-2.2, explanada E3)
    :param p_trf_category: categoría de tráfico pesado
    :return: lista de capas (espesor y mezcla)
    """
    p_table = pd.read_csv(path_table_road_surface, delimiter=";", index_col=0)
    p_layers = []

    for p_layer in list(p_table.index.values):
        p_layers.append([p_layer])

        if pd.isnull(p_table.loc[p_layer, p_trf_category]):
            p_layers[-1].extend([None, None])
        else:
            p_layers[-1].extend(p_table.loc[p_layer, p_trf_category].split(","))

    return p_layers


def get_def_threshold(p_thick: float, p_trf_category: str) -> int:
    """
    Obtiene la categoría de tráfico pesado a partir del IMDp
    Fuente: Norma 6.3 IC (p. 33, tabla 3.A)
    :param p_thick: grosor del asfalto
    :param p_trf_category: categoría de tráfico
    :return:
    """
    p_table = pd.read_csv(path_table_df_threshold, delimiter=";", index_col=0)

    for p_bounds in list(p_table.index.values):
        thick_bounds = [0, 5] if p_bounds == "<5" else [5, np.inf]

        if thick_bounds[0] <= p_thick < thick_bounds[1]:
            return p_table.loc[p_bounds, p_trf_category]

    return 0


def get_def_thickness(p_age: str, p_trf_category: str) -> int:
    """
Obtiene la categoría de tráfico pesado a partir del IMDp
    Fuente: Norma 6.3 IC (p. 34, tabla 4)
    :param p_age: edad de la carretera
    :param p_trf_category: categoría de tráfico
    :return:
    """
    p_table = pd.read_csv(path_table_df_thickness, delimiter=";", index_col=0)
    return p_table.loc[p_age, p_trf_category]


if __name__ == "__main__":
    # Ejemplo (1.1)
    print("\n== EJEMPLO 1 ==")

    IMD = 758
    trf_category = get_traffic_category(IMD)
    trf_layers = get_pavement_layers(trf_category)

    print("- IMD seleccionado: %.2f vehículos pesados/día" % IMD)
    print("- Categoría de firme resultante: %s" % trf_category)
    print("- Capas del firme:")
    for trf_layer in trf_layers:
        if trf_layer[1] is None:
            print("  · %s: espesor y mezcla no determinados" % trf_layer[0])
        else:
            print("  · %s: espesor de %s cm, mezcla %s" % (trf_layer[0], trf_layer[1], trf_layer[2]))

    # Ejemplo (1.2)

    deflection = 156
    road_age = "nuevas"
    road_thickness = 8

    if deflection > get_def_threshold(road_thickness, trf_category):
        deflection_thick = get_def_thickness(road_age, trf_category)
        print("- La vía requiere una actuación con un espesor de %d cm de mezcla nueva bituminosa" % deflection_thick)
    else:
        print("- La vía no requiere una actuación con mezcla nueva bituminosa")

    input("clic para continuar...")

    # Ejemplo (2)
    damages = ["GATOR_CRACK_A_M", "EDGE_CRACK_L_H", "BLEEDING_A_M", "PUMPING_A_H"]
    performances = initial_performance(damages)

    print("\n== EJEMPLO 2 ==")

    print("\nDaños escogidos:")
    for d in damages:
        print("-", d)
    print("\nActuaciones:")
    for p in performances:
        print("-", p, dict_performances[p])

    # TODO: Costes asociados a cada actuación (¿se unificarán criterios?)

    """
    Datos de entrada
    Tabla: categoría de firmes (Figura 2.1-2.2 Norma 6.1 IC)

    - IMD pesados: proporcionado por el usuario. Se asocia a un tipo de categoría de tráfico
    - Cada tipo de tráfico determina un conjunto de secciones de firme (ver tabla)
    - Se ve el espesor y la mezcla (valores de interés)

    Para cada categoría de tráfico, tenemos el espesor de las capas y el tipo de material
    """

    """
    Tablas 3.A y 4.A (Norma 6.3 IC)

    - Conocemos la sección de firme (valor por def. o dado)
    - Si conocemos valor de deflexión...
    - Con deflexión y categoría de tráfico pesado (ver IMD pesados), vamos a tabla 3.A
    - Si es superior al valor, hacemos lo de la tabla 4.A (eliminar espesor dado y reponer). Se corresponde con actuaciones 1, 2, 3.
    """
