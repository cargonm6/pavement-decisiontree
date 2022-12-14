import os

from src.act_calc import act_calc
from src.pci_calc import load_ltpp

if __name__ == "__main__":
    w_dir = os.getcwd().replace("\\", "/")
    section_list = load_ltpp.main(w_dir)

    for section in section_list:
        print(section.get_pci())
        # performances = act_calc.main(w_dir, section)
