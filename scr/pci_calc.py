import pandas as pd
from matplotlib import pyplot as plt


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
        self.survey_width = 0
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
        self.state_code = p_state_code
        self.section_id = p_section_id
        self.survey_date = p_survey_date
        self.construction_no = p_construction_no
        self.survey_width = p_survey_width
        self.section_length = p_section_length
        self.section_area = p_survey_width * p_section_length

        self.update_density()

    def print_section(self):
        """
        Método para mostrar parámetros de la sección
        :return:
        """
        print(self.state_code, self.section_id, self.survey_date, self.construction_no, self.section_area,
              self.section_length)

    def set_distress(self, p_distress, p_severity, p_data):
        """
        Método para definir daños y severidades
        :param p_distress: número del daño (1... 19)
        :param p_severity: número de severidad (0-low, 1-medium, 2-high)
        :param p_data: valor del daño
        :return:
        """
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
            print("\n- %s" % x, end="  >  ")
            for y_i, y in enumerate(self.distress[x]):
                sev = "n/a"

                if len(self.distress[x]) > 1 and y_i == 0:
                    sev = "Low"
                elif len(self.distress[x]) > 1 and y_i == 1:
                    sev = "Medium"
                elif len(self.distress[x]) > 1 and y_i == 2:
                    sev = "High"

                print("%s: (%s, %s %%)" % (
                    sev, "{:.2f}".format(y[0]).rjust(6, ' '), "{:.2f}".format(y[1]).rjust(6, ' ')), end="  |  ")

        self.distress_dataframe()

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
                    self.distress[x][idx_y][1] = y[0] / self.section_area

        # Si se ha definido un daño en particular,
        # solamente actualiza las densidades de ese daño
        else:
            self.distress[p_distress][p_severity][1] = self.distress[p_distress][p_severity][0] / self.section_area


def import_data(p_data: pd.DataFrame) -> PCI:
    p_obj = PCI()

    state_code = p_data["STATE_CODE"]
    section_id = p_data["SHRP_ID"]
    survey_date = p_data["DATE"]
    construction_no = p_data["CONSTRUCTION_NO"]
    # survey_width = p_data["SURVEY_WIDTH"]

    p_obj.set_section(p_state_code=state_code,
                      p_section_id=section_id,
                      p_survey_date=survey_date,
                      p_construction_no=construction_no,
                      p_survey_width=1)

    # 01. Piel de cocodrilo (3 severidades)
    p_obj.set_distress(1, 0, p_data["GATOR_CRACK_A_L"])
    p_obj.set_distress(1, 1, p_data["GATOR_CRACK_A_M"])
    p_obj.set_distress(1, 2, p_data["GATOR_CRACK_A_H"])

    # 02. Exudación (3 severidades)
    # p_obj.set_distress(2, 0, p_data[""])
    p_obj.set_distress(2, 1, p_data["BLEEDING"])
    # p_obj.set_distress(2, 2, p_data[""])

    # 03. Agrietamiento en bloque (3 severidades)
    p_obj.set_distress(3, 0, p_data["BLK_CRACK_A_L"])
    p_obj.set_distress(3, 1, p_data["BLK_CRACK_A_M"])
    p_obj.set_distress(3, 2, p_data["BLK_CRACK_A_H"])

    # 04. Abultamiento y hundimiento (3 severidades)
    # p_obj.set_distress(4, 0, p_data[""])
    # p_obj.set_distress(4, 1, p_data[""])
    # p_obj.set_distress(4, 2, p_data[""])

    # 05. Corrugación (3 severidades)
    # p_obj.set_distress(5, 0, p_data[""])
    # p_obj.set_distress(5, 1, p_data[""])
    # p_obj.set_distress(5, 2, p_data[""])

    # 06. Depresión (3 severidades)
    # p_obj.set_distress(6, 0, p_data[""])
    # p_obj.set_distress(6, 1, p_data[""])
    # p_obj.set_distress(6, 2, p_data[""])

    # 07. Grieta de borde (3 severidades)
    p_obj.set_distress(7, 0, p_data["EDGE_CRACK_L_L"])
    p_obj.set_distress(7, 1, p_data["EDGE_CRACK_L_M"])
    p_obj.set_distress(7, 2, p_data["EDGE_CRACK_L_H"])

    # 08. Grieta de reflexión de junta (3 severidades)
    # p_obj.set_distress(8, 0, p_data[""])
    # p_obj.set_distress(8, 1, p_data[""])
    # p_obj.set_distress(8, 2, p_data[""])

    # 09. Desnivel carril/berma (3 severidades)
    # p_obj.set_distress(9, 0, p_data[""])
    # p_obj.set_distress(9, 1, p_data[""])
    # p_obj.set_distress(9, 2, p_data[""])

    # 10. Grieta longitudinal/transversal (3 severidades)
    p_obj.set_distress(10, 0,
                       p_data["LONG_CRACK_WP_L_L"] + p_data["LONG_CRACK_WP_SEAL_L_L"] + p_data["LONG_CRACK_NWP_L_L"] +
                       p_data["LONG_CRACK_NWP_SEAL_L_L"] + p_data["TRANS_CRACK_NO_L"] + p_data["TRANS_CRACK_L_L"] +
                       p_data["TRANS_CRACK_SEAL_L_L"])
    p_obj.set_distress(10, 1,
                       p_data["LONG_CRACK_WP_L_M"] + p_data["LONG_CRACK_WP_SEAL_L_M"] + p_data["LONG_CRACK_NWP_L_M"] +
                       p_data["LONG_CRACK_NWP_SEAL_L_M"] + p_data["TRANS_CRACK_NO_M"] + p_data["TRANS_CRACK_L_M"] +
                       p_data["TRANS_CRACK_SEAL_L_M"])
    p_obj.set_distress(10, 2,
                       p_data["LONG_CRACK_WP_L_H"] + p_data["LONG_CRACK_WP_SEAL_L_H"] + p_data["LONG_CRACK_NWP_L_H"] +
                       p_data["LONG_CRACK_NWP_SEAL_L_H"] + p_data["TRANS_CRACK_NO_H"] + p_data["TRANS_CRACK_L_H"] +
                       p_data["TRANS_CRACK_SEAL_L_H"])

    # 11. Parcheo (3 severidades)
    p_obj.set_distress(11, 0, p_data["PATCH_A_L"])
    p_obj.set_distress(11, 1, p_data["PATCH_A_M"])
    p_obj.set_distress(11, 2, p_data["PATCH_A_H"])

    # 12. Pulimento de agregados (1 severidad)
    p_obj.set_distress(12, 0, p_data["POLISH_AGG_A"])

    # 13. Huecos (3 severidades)
    p_obj.set_distress(13, 0, p_data["POTHOLES_NO_L"])
    p_obj.set_distress(13, 1, p_data["POTHOLES_NO_M"])
    p_obj.set_distress(13, 2, p_data["POTHOLES_NO_H"])

    # 14. Cruce de vía férrea (3 severidades)
    # p_obj.set_distress(14, 0, p_data[""])
    # p_obj.set_distress(14, 1, p_data[""])
    # p_obj.set_distress(14, 2, p_data[""])

    # 15. Ahuellamiento (3 severidades)
    # p_obj.set_distress(15, 0, p_data[""])
    # p_obj.set_distress(15, 1, p_data[""])
    # p_obj.set_distress(15, 2, p_data[""])

    # 16. Desplazamiento (3 severidades)
    # p_obj.set_distress(16, 0, p_data[""])
    p_obj.set_distress(16, 1, p_data["SHOVING_A"])
    # p_obj.set_distress(16, 2, p_data[""])

    # 17. Grieta parabólica (3 severidades)
    # p_obj.set_distress(17, 0, p_data[""])
    # p_obj.set_distress(17, 1, p_data[""])
    # p_obj.set_distress(17, 2, p_data[""])

    # 18. Hinchamiento (3 severidades)
    # p_obj.set_distress(18, 0, p_data[""])
    # p_obj.set_distress(18, 1, p_data[""])
    # p_obj.set_distress(18, 2, p_data[""])

    # 19. Desprendimiento de agregados (3 severidades)
    # p_obj.set_distress(19, 0, p_data[""])
    p_obj.set_distress(19, 1, p_data["RAVELING"])
    # p_obj.set_distress(19, 2, p_data[""])

    return p_obj


if __name__ == "__main__":
    df = pd.read_csv("../csv/pci.csv", sep=";", encoding="unicode_escape", decimal=",", low_memory=False)

    for df_i in range(0, len(df.index)):
        pci_obj = import_data(df.iloc[df_i])
        pci_obj.print_distresses()
