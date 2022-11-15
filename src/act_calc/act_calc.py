import itertools

import numpy as np
import pandas as pd

from src.pci_calc.pci_calc import PCI

working_directory = ""
min_density = 0.1  # 10 %

path_table_performances = "/src/act_calc/tables/actuaciones.csv"
path_table_trf_category = "/src/act_calc/tables/categorias_trafico.csv"
path_table_road_surface = "/src/act_calc/tables/firmes.csv"
path_table_df_threshold = "/src/act_calc/tables/umbral_deflexion.csv"
path_table_df_thickness = "/src/act_calc/tables/espesor_mezcla_nueva.csv"

dict_distress = {
    "distress_01": ["ALLIGATOR CRACKING LOW", "ALLIGATOR CRACKING MEDIUM", "ALLIGATOR CRACKING HIGH"],
    "distress_02": ["BLEEDING LOW", "BLEEDING MEDIUM", "BLEEDING HIGH"],
    "distress_03": ["BLOCK CRACKING LOW", "BLOCK CRACKING MEDIUM", "BLOCK CRACKING HIGH"],
    "distress_04": ["BUMPS AND SAGS LOW", "BUMPS AND SAGS MEDIUM", "BUMPS AND SAGS HIGH"],
    "distress_05": ["CORRUGATION LOW", "CORRUGATION MEDIUM", "CORRUGATION HIGH"],
    "distress_06": ["DEPRESSION LOW", "DEPRESSION MEDIUM", "DEPRESSION HIGH"],
    "distress_07": ["EDGE CRACKING LOW", "EDGE CRACKING MEDIUM", "EDGE CRACKING HIGH"],
    "distress_08": ["JOINT REFLECTION CRACKING LOW", "JOINT REFLECTION CRACKING MEDIUM",
                    "JOINT REFLECTION CRACKING HIGH"],
    "distress_09": ["LANE-SHOULDER DROP OFF LOW", "LANE-SHOULDER DROP OFF MEDIUM", "LANE-SHOULDER DROP OFF HIGH"],
    "distress_10": ["LONG-TRANS CRACKING LOW", "LONG-TRANS CRACKING MEDIUM", "LONG-TRANS CRACKING HIGH"],
    "distress_11": ["PATCHING LOW", "PATCHING MEDIUM", "PATCHING HIGH"],
    "distress_12": ["POLISHED AGGREGATE ALL"],
    "distress_13": ["POTHOLES LOW", "POTHOLES MEDIUM", "POTHOLES HIGH"],
    "distress_14": ["RAILROAD CROSSING LOW", "RAILROAD CROSSING MEDIUM", "RAILROAD CROSSING HIGH"],
    "distress_15": ["RUTTING LOW", "RUTTING MEDIUM", "RUTTING HIGH"],
    "distress_16": ["SHOVING LOW", "SHOVING MEDIUM", "SHOVING HIGH"],
    "distress_17": ["SLIPPAGE CRACKING LOW", "SLIPPAGE CRACKING MEDIUM", "SLIPPAGE CRACKING HIGH"],
    "distress_18": ["SWELL LOW", "SWELL MEDIUM", "SWELL HIGH"],
    "distress_19": ["WEATHERING AND RAVELING LOW", "WEATHERING AND RAVELING MEDIUM", "WEATHERING AND RAVELING HIGH"]
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


def highest_priority(p_list):
    """
    Elimina actuaciones en favor de las prioritarias
    :param p_list: lista de actuaciones (número y densidad relativa)
    :return: lista de actuaciones
    """

    # Lista de actuaciones (sólo número)
    n_list = [p[0] for p in p_list]

    # Si el número de actuaciones susceptible es mayor a uno
    if sum(el in n_list for el in [1, 2, 3, 6]) > 1:

        # Orden de prioridad de las actuaciones (de menos a más restrictivo)
        order = []

        for i in [[6, 3], [6, 2], [6, 1], [3, 2], [3, 1], [2, 1]]:
            # Si los elementos están en la lista, añade el orden
            order.append(i) if check([i[0]], n_list) and check([i[1]], n_list) else 0

        # Por cada combinación de jerarquía
        for i, comb in enumerate(order):

            # Índices
            idx_0 = n_list.index(comb[0])
            idx_1 = n_list.index(comb[1])

            # Densidades
            density_0 = p_list[idx_0][1]
            density_1 = p_list[idx_1][1]

            # Si la densidad del primero no supera el límite, o sí lo supera pero el segundo también
            if density_0 < min_density or density_1 >= min_density:
                # Marca el primero para eliminar, poniendo la actuación a "0"
                p_list[idx_0][0] = 0

            # Si es la última combinación, el primero supera el límite pero el segundo no
            elif i == len(order) - 1 and density_1 < min_density:
                p_list[idx_1][0] = 0

    good_list = []

    for element in p_list:
        if element[0] != 0:
            good_list.append(element)

    return good_list


def initial_performance(p_damages, p_density):
    """
    Obtiene la lista de actuaciones para un conjunto de daños de entrada
    :param p_density: densidad total de los daños asociados
    :param p_damages: daños asociados (nombre + densidad)
    :return:
    """
    p_dlist = []  # Lista de daños (damage list)
    p_plist = []  # Lista de actuaciones (performance list)

    # Convierte el diccionario en grupos de daños y densidad
    for i, damage in enumerate(p_damages):
        for j, severity in enumerate(p_damages[damage]):

            # Existe un daño particular
            if severity[0] > 0:
                p_dlist.append([list(dict_distress.values())[i][j]])
                p_dlist[-1].append(severity[1])

    table_performance = pd.read_csv(working_directory + path_table_performances, delimiter=";", dtype=object,
                                    index_col='INDEX')

    # Para cada fila (núm. de daño)
    for p_i in p_dlist:

        # Si el nombre de daño no está presente en la tabla (índices o columnas)
        if not p_i[0] in table_performance.index.values.tolist():
            continue

        # Para cada columna (núm. de daño)
        for p_k in p_dlist:
            # Si el nombre de daño no está presente en la tabla (índices o columnas)
            if not p_k[0] in table_performance.columns:
                continue

            performance = table_performance.loc[p_i[0], p_k[0]]

            # Obtenemos la actuación. Si es nula, pasamos. Si son dos, las separamos.
            if pd.isna(performance):
                continue

            for perf in performance.split("+"):
                p_plist.append([int(perf), p_i, p_k])

    p_plist = sorted(p_plist)
    p_perf = []
    p_perf_dif = list(dict.fromkeys([perf[0] for perf in p_plist]))

    # Para cada actuación diferente (i)
    for i in p_perf_dif:

        list_i = []

        # Para cada elemento de actuación en la lista
        for j, val in enumerate(p_plist):
            # Si se corresponde con la actuación i, lo añade
            list_i.extend(val[1:3]) if val[0] == i else 0

        # Elimina daños duplicados de todas las actuaciones añadidas
        list_i.sort()
        list_i = list(k for k, _ in itertools.groupby(list_i))

        # Densidad relativa a la suma de densidades de daños
        perf_density = sum(j[1] for j in list_i) / p_density
        p_perf.append([i, perf_density])

    # Seguimos el orden de prioridad para seleccionar entre las actuaciones obtenidas
    p_perf = highest_priority(p_perf)
    return p_perf


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


def main(pw_dir: str, pci_obj: PCI):
    # Ejemplo (1.1)
    # print("\n== EJEMPLO 1 ==")
    #
    # IMD = 758
    # trf_category = get_traffic_category(IMD)
    # trf_layers = get_pavement_layers(trf_category)
    #
    # print("- IMD seleccionado: %.2f vehículos pesados/día" % IMD)
    # print("- Categoría de firme resultante: %s" % trf_category)
    # print("- Capas del firme:")
    # for trf_layer in trf_layers:
    #     if trf_layer[1] is None:
    #         print("  · %s: espesor y mezcla no determinados" % trf_layer[0])
    #     else:
    #         print("  · %s: espesor de %s cm, mezcla %s" % (trf_layer[0], trf_layer[1], trf_layer[2]))

    # Ejemplo (1.2)

    # deflection = 156
    # road_age = "nuevas"
    # road_thickness = 8
    #
    # if deflection > get_def_threshold(road_thickness, trf_category):
    #     deflection_thick = get_def_thickness(road_age, trf_category)
    #     print("- La vía requiere una actuación con un espesor de %d cm de mezcla nueva bituminosa" % deflection_thick)
    # else:
    #     print("- La vía no requiere una actuación con mezcla nueva bituminosa")
    #
    # input("clic para continuar...")

    # Ejemplo (2)

    global working_directory
    working_directory = pw_dir

    damages = pci_obj.get_all_distresses()
    density = pci_obj.get_density()

    performances = initial_performance(damages, density)
    #
    # print("\nDaños escogidos:")
    # for d in damages:
    #     print("-", d)
    # print("\nActuaciones:")
    # for p in performances:
    #     print("-", p, dict_performances[p])

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
