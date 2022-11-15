import sys

import pandas as pd

from src.pci_calc.pci_calc import PCI

working_directory = ""

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


def import_ltpp_data(p_data: pd.DataFrame) -> PCI:
    """
    Función para importar daños desde LTPP
    :param p_data:
    :return:
    """
    p_obj = PCI(working_directory)

    # Datos de la sección
    p_obj.set_section(p_state_code=p_data["STATE_CODE"],
                      p_section_id=p_data["SHRP_ID"],
                      p_survey_date=p_data["DATE"],
                      p_construction_no=p_data["CONSTRUCTION_NO"],
                      p_survey_width=p_data["SURVEY_WIDTH"])

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
    p_obj.set_distress(10, 0, p_data["LONG_CRACK_WP_L_L"] + p_data["LONG_CRACK_WP_SEAL_L_L"] +
                       p_data["LONG_CRACK_NWP_L_L"] + p_data["LONG_CRACK_NWP_SEAL_L_L"] +
                       p_data["TRANS_CRACK_L_L"] + p_data["TRANS_CRACK_SEAL_L_L"])
    p_obj.set_distress(10, 1, p_data["LONG_CRACK_WP_L_M"] + p_data["LONG_CRACK_WP_SEAL_L_M"] +
                       p_data["LONG_CRACK_NWP_L_M"] + p_data["LONG_CRACK_NWP_SEAL_L_M"] +
                       p_data["TRANS_CRACK_L_M"] + p_data["TRANS_CRACK_SEAL_L_M"])
    p_obj.set_distress(10, 2, p_data["LONG_CRACK_WP_L_H"] + p_data["LONG_CRACK_WP_SEAL_L_H"] +
                       p_data["LONG_CRACK_NWP_L_H"] + p_data["LONG_CRACK_NWP_SEAL_L_H"] +
                       p_data["TRANS_CRACK_L_H"] + p_data["TRANS_CRACK_SEAL_L_H"])

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

    # Actualización de los Deducted Value (DV)

    p_obj.update_density()
    p_obj.update_dv()
    p_obj.update_pci()

    return p_obj


def get_ltpp_pci(p_file):
    # start_time = time.time()

    # Leemos el fichero de datos de LTPP
    df = pd.read_csv(p_file, sep=";", encoding="utf-8", decimal=",", low_memory=False)

    pci_result = []

    for df_i in range(0, len(df)):
        # Por cada fila, importamos valores y convertimos nulos a ceros
        pci_result.append(import_ltpp_data(df.iloc[df_i].fillna(0)))

        sys.stdout.write("\r- Calculating PCI from LTPP rows... %.2f %%" % (100 * (df_i + 1) / len(df)))

    print("")

    # print("- (%i) predicted pci: %.4f, real pci: %.4f, desv: %.2f" % (
    #     df_i + 1, pci_res, df["PCI_old"].iloc[df_i], df["PCI_old"].iloc[df_i] - pci_res))

    # SUMO FILAS -> SUMO DAÑOS POR SEPARADO Y ANCHO, LARGO...

    # Calculo el PCI del conjunto de fotos (tengo densidades de los daños y valor final de PCI)
    # Obtengo la actuación en función de esas densidades y PCI

    # df["PCI"] = pci_result
    #
    # df.to_csv(p_file, sep=";", decimal=",", index=False)
    #
    # print("--- %s seconds ---" % (time.time() - start_time))

    return pci_result


def main(pw_dir: str):
    global working_directory
    working_directory = pw_dir

    p_file = pw_dir + "/res/ant_pci.csv"
    return get_ltpp_pci(p_file)


if __name__ == "__main__":
    get_ltpp_pci("../../res/ant_pci.csv")
