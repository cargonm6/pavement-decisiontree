import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

path_dv = "./tables/pci_curves.csv"
path_cdv = "./tables/pci_cdv.csv"

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


# Numeración de los daños
# 01. Piel de cocodrilo (3 severidades)
# 02. Exudación (3 severidades)
# 03. Agrietamiento en bloque (3 severidades)
# 04. Abultamiento y hundimiento (3 severidades)
# 05. Corrugación (3 severidades)
# 06. Depresión (3 severidades)
# 07. Grieta de borde (3 severidades)
# 08. Grieta de reflexión de junta (3 severidades)
# 09. Desnivel carril/berma (3 severidades)
# 10. Grieta longitudinal/transversal (3 severidades)
# 11. Parcheo (3 severidades)
# 12. Pulimento de agregados (1 severidad)
# 13. Huecos (3 severidades)
# 14. Cruce de vía férrea (3 severidades)
# 15. Ahuellamiento (3 severidades)
# 16. Desplazamiento (3 severidades)
# 17. Grieta parabólica (3 severidades)
# 18. Hinchamiento (3 severidades)
# 19. Desprendimiento de agregados (3 severidades)

# Daños según actuaciones
# Valores de 3D:
# - (A, 3 sev.) Grietas de cocodrilo
# - (A, 3 sev.) Corrugación
# - (A, 3 sev.) Depresión
# - (A, 3 sev.) Ahuellamiento
# - (A, 3 sev.) Desplazamiento vertical
# - (A, 1 sev.) Surgencia de finos
# - (A, 1 sev.) Pulimento de agregados
# - (A, 1 sev.) Desprendimiento de agregados
# - (A, 1 sev.) Exudaciones
# - (L, 3 sev.) Grietas reflejadas
# - (L, 3 sev.) Grietas longitudinales/transversales
# - (N, 3 sev.) Huecos


class PCI:
    def __init__(self):
        """
        Método constructor
        """
        self.state_code = ""
        self.section_id = ""
        self.survey_date = ""
        self.construction_no = 0
        self.survey_width = 50
        self.section_length = 500.0
        self.section_area = self.survey_width * self.section_length

        # Distress_no = [Low/Medium/High: quantity/density/deducted value]
        self.distress = {"distress_01": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_02": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_03": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_04": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_05": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_06": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_07": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_08": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_09": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_10": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_11": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_12": [[0.0, 0.0, 0.0]],
                         "distress_13": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_14": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_15": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_16": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_17": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_18": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                         "distress_19": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]}

    def set_section(self, p_state_code: str = "", p_section_id: str = "", p_survey_date: str = "",
                    p_construction_no: int = 0, p_survey_width: float = 0.0, p_section_length: float = 500.0):
        """
        Método para definir parámetros de la sección
        :param p_state_code: código de estado
        :param p_section_id: ID de sección
        :param p_survey_date: fecha de muestra
        :param p_construction_no: número de construcción
        :param p_survey_width: ancho de muestra
        :param p_section_length: longitud de la sección
        :return:
        """
        self.state_code = p_state_code if not pd.isna(p_state_code) else ""
        self.section_id = p_section_id if not pd.isna(p_section_id) else ""
        self.survey_date = p_survey_date if not pd.isna(p_survey_date) else ""
        self.construction_no = p_construction_no if not pd.isna(p_construction_no) else 0
        self.survey_width = p_survey_width if not pd.isna(p_survey_width) else 0.0
        self.section_length = p_section_length if not pd.isna(p_section_length) else 500.0
        self.section_area = p_survey_width * p_section_length

        self.update_density()

    def print_section(self):
        """
        Método para mostrar parámetros de la sección
        :return:
        """
        print("State code:", self.state_code)
        print("ID:", self.section_id)
        print("Date:", self.survey_date)
        print("CN:", self.construction_no)
        print("Width:", self.survey_width)
        print("Len:", self.section_length)
        print("Area:", self.section_area)

    def set_distress(self, p_distress, p_severity, p_data):
        """
        Método para definir daños y severidades
        :param p_distress: número del daño (1... 19)
        :param p_severity: número de severidad (0-low, 1-medium, 2-high)
        :param p_data: valor del daño
        :return:
        """

        if not pd.isna(p_data) and p_data > 0:
            self.distress["distress_" + str(p_distress).zfill(2)][p_severity][0] = p_data
            self.update_density("distress_" + str(p_distress).zfill(2), p_severity)

    def get_distress(self, p_distress, p_severity):
        """
        Método para devolver daños y severidades
        :param p_distress: número del daño (1... 19)
        :param p_severity: número de severidad (0-low, 1-medium, 2-high)
        :return:
        """
        return self.distress["distress_" + str(p_distress).zfill(2)][p_severity]

    def print_distresses(self):
        """
        Método para mostrar daños y severidades
        :return:
        """
        for x in self.distress:
            print("\n- %s (%s)" % (x, dict_distress[x][0].split(" ")[0]), end="  >  ")
            for y_i, y in enumerate(self.distress[x]):
                sev = "n/a"

                if len(self.distress[x]) > 1 and y_i == 0:
                    sev = "Low"
                elif len(self.distress[x]) > 1 and y_i == 1:
                    sev = "Medium"
                elif len(self.distress[x]) > 1 and y_i == 2:
                    sev = "High"

                if y[0] > 0:
                    print("%s: (%s, %s, %s)" % (sev, "{:.2f}".format(y[0]).rjust(6, ' '),
                                                "{:.2f}".format(y[1]).rjust(6, ' '),
                                                "{:.4f}".format(y[2]).rjust(6, ' ')
                                                ), end="  |  ")

        # self.distress_dataframe()

    def distress_dataframe(self):
        """
        Convierte los daños y severidades en un Dataframe
        :return:
        """

        df_quantity = pd.DataFrame(columns=["Distress", "Quantity"])
        df_density = pd.DataFrame(columns=["Distress", "Density"])

        for x_i, x in enumerate(self.distress):
            for y_i, y in enumerate(self.distress[x]):
                sev = "-"

                if len(self.distress[x]) > 1 and y_i == 0:
                    sev = "L"
                elif len(self.distress[x]) > 1 and y_i == 1:
                    sev = "M"
                elif len(self.distress[x]) > 1 and y_i == 2:
                    sev = "H"

                title = str(x_i + 1).zfill(2) + " " + sev
                df_quantity = pd.concat(
                    [df_quantity, pd.DataFrame.from_records([{"Distress": title, "Quantity": y[0]}])])
                df_density = pd.concat([df_density, pd.DataFrame.from_records([{"Distress": title, "Density": y[1]}])])

        fig, ax = plt.subplots(nrows=2, ncols=1)

        ax_1 = df_quantity.plot(kind='bar', ax=ax[0])
        ax_1.set_xticklabels(df_quantity["Distress"], rotation=90)

        ax_2 = df_density.plot(kind='bar', ax=ax[1])
        ax_2.set_xticklabels(df_quantity["Distress"], rotation=90)

        plt.show()

    def update_density(self, p_distress: str = None, p_severity: int = None):
        """
        Método para actualizar la densidad de un daño
        :param p_distress: etiqueta del daño
        :param p_severity: número de severidad (0-low, 1-medium, 2-high)
        :return:
        """

        # Si no se ha definido un daño en particular,
        # recorre todos los daños y actualiza las densidades
        if p_distress is None and p_severity is None:
            for x in self.distress:
                for idx_y, y in enumerate(self.distress[x]):
                    self.distress[x][idx_y][1] = 100 * y[0] / self.section_area

        # Si se ha definido un daño en particular,
        # solamente actualiza las densidades de ese daño
        else:
            self.distress[p_distress][p_severity][1] = 100 * self.distress[p_distress][p_severity][
                0] / self.section_area

    def update_dv(self):
        """
        Actualiza los Deduct Value (DV) de cada daño, en función de sus densidades
        :return:
        """

        df_curves = pd.read_csv(path_dv, sep=";", encoding="utf-8", decimal=",", low_memory=False)

        for x in self.distress:

            # Si son potholes, se multiplica por 10 para coincidir con las curvas de DV
            density_factor = 10 if x == "distress_13" else 1

            for idx_y, y in enumerate(self.distress[x]):
                density = y[1] * density_factor

                # Si la densidad es mayor que cero
                if density > 0:
                    # Obtenemos las columnas de la tabla de curvas
                    col_distress = dict_distress[x][idx_y]
                    df_curve = df_curves[["DISTRESS", col_distress]]

                    # Busca el primer y último índice válido de cada columna (aquellos no nulos)
                    curve_min_row = df_curve[[col_distress]].first_valid_index()
                    curve_max_row = df_curve[[col_distress]].last_valid_index()

                    # Busca el primer y último valor válido de densidad
                    curve_min_di = df_curve.iloc[curve_min_row]["DISTRESS"]
                    curve_max_di = df_curve.iloc[curve_max_row]["DISTRESS"]

                    # Busca el primer y último valor válido de DV
                    curve_min_dv = df_curve.iloc[curve_min_row][col_distress]
                    curve_max_dv = df_curve.iloc[curve_max_row][col_distress]

                    # Si la densidad excede los límites, o es la menor o la mayor, toma el valor DV extremo
                    if density < curve_min_di:
                        deduct_value = curve_min_dv
                    elif density >= curve_max_di:
                        deduct_value = curve_max_dv
                    else:
                        # Toma el índice del valor de DV igual o inmediatamente inferior al de densidad
                        idx_density = df_curve[df_curve["DISTRESS"].le(density)].index[-1]

                        # Obtiene el contenido del índice y el siguiente elemento
                        di_idx0 = df_curve.iloc[idx_density]["DISTRESS"]
                        di_idx1 = df_curve.iloc[idx_density + 1]["DISTRESS"]

                        dv_idx0 = df_curve.iloc[idx_density][col_distress]
                        dv_idx1 = df_curve.iloc[idx_density + 1][col_distress]

                        # Cálculo del valor deducido
                        deduct_value = dv_idx0 + ((dv_idx1 - dv_idx0) / (di_idx1 - di_idx0)) * (density - di_idx0)

                    # Asignación del valor deducido
                    y[2] = deduct_value

    def get_pci(self) -> float:
        """
        Aplica la corrección de DV y obtiene el PCI
        :return:
        """

        # Crea una lista de daños con DV
        df_data = []
        for x in self.distress:
            for idx_y, y in enumerate(self.distress[x]):
                density = y[1]
                if density > 0:
                    df_row = {"distress": x, "severity": idx_y, "dv": y[2]}
                    df_data.append(df_row)
        df_data = pd.DataFrame(df_data)

        # Si no hay daños, obtiene DV 0 y termina
        total = 0

        # Número de daños registrados
        n = len(df_data.index)

        # Si existen daños
        if not df_data.empty:
            # Organizamos los DV en orden descendente
            df_data = df_data.sort_values(by=["dv"], ascending=False).reset_index(drop=True)

            # Si sólo hay 1 daño o el 2.º daño tiene valor <= 2
            if n == 1 or df_data.iloc[1]["dv"] <= 2:
                # caso 1
                # Obtiene el DV total y termina
                total = df_data["dv"].sum()
            else:
                # caso 2
                df_cdv = pd.read_csv(path_cdv, sep=";", encoding="utf-8", decimal=",", low_memory=False)

                # Valor m (si es > 10, le asigna ese valor máximo)
                m = 1 + 9 / 98 * (100 - df_data.iloc[0]["dv"])
                m = 10 if m > 10 else m
                m_int = int(np.ceil(m))

                # Tabla de valores corregidos
                df_correct = []

                # Si el número de daños no supera el límite
                if n <= (m_int - 1):

                    # caso 2.1

                    # Recorremos la matriz de daños y reasignamos valores < 2 en triángulo
                    aux = 0
                    for i in range(0, n):
                        df_correct.append(df_data["dv"].transpose().to_dict())
                    for i in range(n - 1, 0, -1):
                        if df_correct[0][i] > 2:
                            value_aux = 2
                        else:
                            value_aux = df_correct[0][i]
                        aux += 1
                        for k in range(aux, n):
                            df_correct[k][i] = value_aux

                # Si el número de daños sí supera el límite
                else:

                    # caso 2.2

                    # El valor más pequeño de la primera fila será el de la posición m_int de DV
                    for i in range(0, m_int):
                        df_temp = df_data["dv"].head(m_int - 1)
                        df_temp.loc[m_int - 1] = (m - m_int + 1) * df_data.iloc[m_int - 1]["dv"] if i == 0 else 0
                        df_correct.append(df_temp.transpose().to_dict())

                    aux = 0

                    for i in range(m_int - 1, 0, -1):
                        if df_correct[0][i] > 2:
                            value_aux = 2
                        else:
                            value_aux = df_correct[0][i]
                        aux += 1
                        for k in range(aux, m_int):
                            df_correct[k][i] = value_aux

                # Convertimos la tabla en DataFrame
                df_correct = pd.DataFrame(df_correct)

                # Añadimos columna de totales y valores > 2
                df_correct["total"] = df_correct.sum(axis=1)
                df_correct["q"] = df_correct.drop(columns=["total"]).select_dtypes(np.number).gt(2).sum(axis=1)

                # Descartamos valores de q > 7, su valor máximo
                df_correct.loc[df_correct["q"] > 7, "q"] = 7

                df_cdv_col = []

                for index, row in df_correct.iterrows():
                    # Nota: en Python el índice empieza en 0
                    idx_row = df_cdv[df_cdv["dv"].le(row["total"])].index[-1]
                    idx_col = str(int(row["q"]))

                    # print("FILA: %d, COLUMNA: %s, VALOR: %.2f" % (idx_row, idx_col, df_cdv.iloc[idx_row][idx_col]))

                    # Si no existe una fila siguiente, o el valor CDV de la fila o la siguiente son nulos

                    if not (idx_row + 1) in df_cdv.index or pd.isna(df_cdv.iloc[idx_row][idx_col]) or pd.isna(
                            df_cdv.iloc[idx_row + 1][idx_col]):
                        if idx_row < 49:
                            max_row = df_cdv[[idx_col]].first_valid_index()
                            max_cdv = df_cdv.iloc[max_row][idx_col]
                            df_cdv_col.append(max_cdv)
                        else:
                            df_cdv_col.append(100)

                    else:

                        # Obtiene el contenido del índice y el siguiente elemento
                        cdi_idx0 = df_cdv.iloc[idx_row]["dv"]
                        cdi_idx1 = df_cdv.iloc[idx_row + 1]["dv"]

                        cdv_idx0 = df_cdv.iloc[idx_row][idx_col]
                        cdv_idx1 = df_cdv.iloc[idx_row + 1][idx_col]

                        # Cálculo del valor deducido (corregido)
                        deduct_value = cdv_idx0 + ((cdv_idx1 - cdv_idx0) / (cdi_idx1 - cdi_idx0)) * (
                                row["total"] - cdi_idx0)
                        df_cdv_col.append(deduct_value)

                df_correct["cdv"] = df_cdv_col

                # print("Deduct values (corrected):")
                # print(df_correct)

                total = df_correct["cdv"].max()
                # print("Total: %.2f" % total)

        # Si no hay daños, el PCI es 100
        return 100 - total
