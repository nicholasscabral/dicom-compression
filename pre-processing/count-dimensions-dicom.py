import os
import pydicom
from collections import defaultdict


def count_dicom_resolutions(root_dir):
    resolutions = defaultdict(int)
    i = 0

    # Verifica se o diretório raiz existe
    if not os.path.isdir(root_dir):
        print(f"O diretório {root_dir} não existe.")
        return

    # Percorre todos os diretórios e arquivos a partir da raiz
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            # Verifica se o arquivo tem a extensão .dcm
            if file.lower().endswith(".dcm"):
                i += 1
                # Caminho completo do arquivo
                file_path = os.path.join(subdir, file)

                try:
                    # Carrega a imagem DICOM
                    dicom_image = pydicom.dcmread(file_path)

                    # Obtém a resolução
                    rows = dicom_image.Rows
                    columns = dicom_image.Columns
                    resolution = f"{columns}x{rows}"
                    print(f"{i} File: {file_path}, Resolution: {resolution}")

                    # Conta a resolução
                    resolutions[resolution] += 1

                except Exception as e:
                    print(f"Erro ao processar {file_path}: {e}")

    # Exibe as contagens de resolução
    for resolution, count in resolutions.items():
        print(f"Resolução {resolution}: {count} arquivos")


# Exemplo de uso
if __name__ == "__main__":
    # Substitua 'seu_diretorio' pelo caminho para o diretório desejado
    import sys

    if len(sys.argv) != 2:
        print("Uso: python script.py /caminho/para/o/diretorio")
        sys.exit(1)

    root_dir = sys.argv[1]
    count_dicom_resolutions(root_dir)

# LUNG
# 51651 - 512x512


# BREAST
# Resolução 384x384: 20799 arquivos
# Resolução 432x432: 2484 arquivos
# Resolução 512x512: 9813 arquivos
# Resolução 448x448: 3760 arquivos
# Resolução 480x480: 19863 arquivos
# Resolução 400x400: 5111 arquivos
# Resolução 352x352: 2452 arquivos
# Resolução 256x256: 2857 arquivos
# Resolução 1024x1024: 1840 arquivos
# Resolução 320x320: 3994 arquivos
# Resolução 416x416: 2361 arquivos
# Resolução 568x568: 605 arquivos
# Resolução 144x144: 374 arquivos
# Resolução 360x320: 160 arquivos
# Resolução 372x384: 384 arquivos
# Resolução 288x288: 530 arquivos
# Resolução 484x484: 15 arquivos
# Resolução 432x384: 70 arquivos

# brain
# Resolução 512x512: 11225 arquivos
# Resolução 256x256: 28049 arquivos
# Resolução 216x256: 5692 arquivos
# Resolução 240x256: 1232 arquivos
# Resolução 320x320: 2046 arquivos
# Resolução 224x256: 2047 arquivos
# Resolução 439x599: 1 arquivos
# Resolução 560x560: 174 arquivos
# Resolução 348x384: 136 arquivos
# Resolução 756x896: 32 arquivos
# Resolução 200x256: 560 arquivos
# Resolução 448x512: 185 arquivos
# Resolução 210x224: 176 arquivos
# Resolução 208x256: 1136 arquivos
# Resolução 432x512: 368 arquivos
# Resolução 784x896: 298 arquivos
# Resolução 11x12: 2 arquivos
# Resolução 753x624: 1 arquivos
# Resolução 324x384: 56 arquivos
# Resolução 280x320: 522 arquivos
# Resolução 736x628: 1 arquivos
# Resolução 1046x732: 1 arquivos
# Resolução 528x528: 42 arquivos
# Resolução 52x80: 1 arquivos
# Resolução 813x638: 1 arquivos
# Resolução 288x320: 64 arquivos
# Resolução 270x320: 181 arquivos
# Resolução 256x240: 176 arquivos
# Resolução 248x256: 176 arquivos
# Resolução 1038x704: 1 arquivos
# Resolução 192x256: 192 arquivos
# Resolução 757x615: 1 arquivos
# Resolução 260x320: 66 arquivos
# Resolução 805x609: 1 arquivos
# Resolução 758x571: 1 arquivos
# Resolução 234x306: 2 arquivos
# Resolução 384x512: 29 arquivos
# Resolução 793x607: 1 arquivos
# Resolução 53x74: 1 arquivos
# Resolução 734x593: 1 arquivos
# Resolução 797x650: 1 arquivos
# Resolução 240x240: 56 arquivos
# Resolução 49x57: 1 arquivos
# Resolução 40x37: 1 arquivos
# Resolução 29x35: 1 arquivos
# Resolução 40x71: 1 arquivos
# Resolução 695x692: 1 arquivos
# Resolução 41x51: 1 arquivos
# Resolução 45x70: 1 arquivos
# Resolução 73x83: 1 arquivos
# Resolução 16x27: 1 arquivos
# Resolução 256x314: 1 arquivos
# Resolução 38x47: 2 arquivos
# Resolução 763x587: 1 arquivos
# Resolução 54x63: 1 arquivos
# Resolução 799x624: 1 arquivos
# Resolução 66x61: 1 arquivos
# Resolução 156x139: 1 arquivos
# Resolução 709x621: 1 arquivos
# Resolução 164x234: 1 arquivos
# Resolução 703x578: 1 arquivos
# Resolução 705x574: 1 arquivos
# Resolução 156x210: 1 arquivos
# Resolução 38x67: 1 arquivos
# Resolução 26x23: 1 arquivos
# Resolução 752x663: 1 arquivos
# Resolução 769x642: 1 arquivos
# Resolução 761x598: 1 arquivos
# Resolução 742x632: 1 arquivos
# Resolução 316x407: 1 arquivos
# Resolução 334x462: 1 arquivos
# Resolução 715x595: 1 arquivos
# Resolução 709x591: 1 arquivos
# Resolução 700x585: 1 arquivos
# Resolução 9x9: 2 arquivos
# Resolução 270x336: 1 arquivos
# Resolução 44x52: 1 arquivos
# Resolução 231x348: 1 arquivos
# Resolução 276x350: 1 arquivos
# Resolução 736x598: 1 arquivos
# Resolução 59x69: 1 arquivos
# Resolução 763x606: 1 arquivos
# Resolução 252x324: 1 arquivos
# Resolução 701x574: 1 arquivos
# Resolução 787x575: 1 arquivos
# Resolução 732x584: 1 arquivos
# Resolução 13x16: 1 arquivos
# Resolução 750x605: 1 arquivos
# Resolução 703x581: 1 arquivos
# Resolução 737x638: 1 arquivos
# Resolução 716x577: 1 arquivos
# Resolução 875x615: 1 arquivos
# Resolução 770x624: 1 arquivos
# Resolução 165x257: 1 arquivos
# Resolução 251x140: 1 arquivos
# Resolução 1002x676: 1 arquivos
# Resolução 757x656: 1 arquivos
# Resolução 757x652: 1 arquivos
# Resolução 725x596: 2 arquivos
# Resolução 37x56: 1 arquivos
# Resolução 742x563: 1 arquivos
# Resolução 142x216: 1 arquivos
# Resolução 859x602: 1 arquivos
# Resolução 314x440: 1 arquivos
# Resolução 793x688: 1 arquivos
# Resolução 423x540: 1 arquivos
# Resolução 753x589: 1 arquivos
# Resolução 227x404: 1 arquivos
# Resolução 731x759: 1 arquivos
# Resolução 789x627: 1 arquivos
# Resolução 922x618: 1 arquivos
# Resolução 783x589: 1 arquivos
# Resolução 711x609: 1 arquivos
# Resolução 180x116: 1 arquivos
# Resolução 724x592: 1 arquivos
# Resolução 24x15: 1 arquivos
# Resolução 44x40: 1 arquivos
# Resolução 830x639: 1 arquivos
# Resolução 738x595: 1 arquivos
# Resolução 747x620: 1 arquivos
# Resolução 813x656: 1 arquivos
# Resolução 814x613: 1 arquivos
# Resolução 716x572: 1 arquivos
# Resolução 180x212: 1 arquivos
# Resolução 856x625: 1 arquivos
# Resolução 152x214: 2 arquivos
# Resolução 18x40: 1 arquivos
# Resolução 748x717: 1 arquivos
# Resolução 726x567: 1 arquivos
# Resolução 34x30: 1 arquivos
# Resolução 76x36: 1 arquivos
# Resolução 744x620: 1 arquivos
# Resolução 48x73: 1 arquivos
# Resolução 234x309: 1 arquivos
# Resolução 162x238: 1 arquivos
# Resolução 806x649: 1 arquivos
# Resolução 132x176: 1 arquivos
# Resolução 21x19: 1 arquivos
# Resolução 765x593: 1 arquivos
# Resolução 75x103: 1 arquivos
# Resolução 27x27: 1 arquivos
# Resolução 44x41: 1 arquivos
# Resolução 185x302: 1 arquivos
# Resolução 975x659: 1 arquivos
# Resolução 28x52: 1 arquivos
# Resolução 268x336: 1 arquivos
# Resolução 78x110: 1 arquivos
# Resolução 47x73: 1 arquivos
# Resolução 743x581: 1 arquivos
# Resolução 6x6: 1 arquivos
# Resolução 38x71: 1 arquivos
# Resolução 743x638: 1 arquivos
# Resolução 49x51: 1 arquivos
# Resolução 893x687: 1 arquivos
# Resolução 449x547: 1 arquivos
# Resolução 459x576: 1 arquivos
# Resolução 328x388: 1 arquivos
# Resolução 744x608: 1 arquivos
# Resolução 797x693: 1 arquivos
# Resolução 705x565: 1 arquivos
# Resolução 768x592: 1 arquivos
# Resolução 718x722: 1 arquivos
# Resolução 13x10: 1 arquivos
# Resolução 200x290: 1 arquivos
# Resolução 396x483: 1 arquivos
# Resolução 842x679: 1 arquivos
# Resolução 34x27: 1 arquivos
# Resolução 769x595: 1 arquivos
# Resolução 252x339: 1 arquivos
# Resolução 38x44: 1 arquivos
# Resolução 825x652: 1 arquivos
# Resolução 251x331: 1 arquivos
# Resolução 831x796: 1 arquivos
# Resolução 40x86: 1 arquivos
# Resolução 795x609: 1 arquivos
# Resolução 42x40: 1 arquivos
# Resolução 28x34: 1 arquivos
# Resolução 40x29: 1 arquivos
# Resolução 800x615: 1 arquivos
# Resolução 95x117: 1 arquivos
# Resolução 15x34: 1 arquivos
# Resolução 43x59: 1 arquivos
# Resolução 751x735: 1 arquivos
# Resolução 748x702: 1 arquivos
# Resolução 16x17: 1 arquivos
# Resolução 786x600: 1 arquivos
# Resolução 411x531: 1 arquivos
# Resolução 43x68: 1 arquivos
# Resolução 743x595: 1 arquivos
# Resolução 408x495: 1 arquivos
# Resolução 21x24: 1 arquivos
# Resolução 738x566: 1 arquivos
# Resolução 262x348: 1 arquivos
# Resolução 888x649: 1 arquivos
# Resolução 17x16: 1 arquivos
# Resolução 750x749: 1 arquivos
# Resolução 11x8: 1 arquivos
# Resolução 713x618: 1 arquivos
# Resolução 794x635: 1 arquivos
# Resolução 846x803: 1 arquivos
# Resolução 86x97: 1 arquivos
# Resolução 284x344: 1 arquivos
# Resolução 793x576: 1 arquivos
# Resolução 866x795: 1 arquivos
# Resolução 570x710: 1 arquivos
# Resolução 32x41: 1 arquivos
# Resolução 1010x635: 1 arquivos
# Resolução 207x279: 1 arquivos
# Resolução 748x687: 1 arquivos
# Resolução 709x574: 1 arquivos
# Resolução 29x36: 1 arquivos
# Resolução 22x21: 1 arquivos
# Resolução 125x174: 1 arquivos
# Resolução 308x377: 1 arquivos
# Resolução 832x780: 1 arquivos
# Resolução 81x103: 1 arquivos
# Resolução 429x556: 1 arquivos
# Resolução 320x401: 1 arquivos
# Resolução 709x577: 1 arquivos
# Resolução 47x88: 1 arquivos
# Resolução 743x579: 1 arquivos
# Resolução 30x33: 1 arquivos
# Resolução 771x670: 1 arquivos
# Resolução 711x564: 1 arquivos
# Resolução 805x638: 1 arquivos
# Resolução 27x38: 1 arquivos
# Resolução 41x50: 1 arquivos
# Resolução 30x38: 1 arquivos
# Resolução 44x51: 1 arquivos
# Resolução 746x607: 1 arquivos
# Resolução 714x615: 1 arquivos
# Resolução 692x575: 1 arquivos
# Resolução 942x671: 1 arquivos
# Resolução 71x85: 1 arquivos
# Resolução 751x632: 1 arquivos
# Resolução 772x598: 1 arquivos
# Resolução 848x628: 1 arquivos
# Resolução 738x618: 1 arquivos
# Resolução 53x68: 1 arquivos
# Resolução 25x20: 1 arquivos
# Resolução 272x324: 1 arquivos
# Resolução 225x336: 1 arquivos
# Resolução 52x50: 1 arquivos
# Resolução 267x401: 1 arquivos
# Resolução 728x589: 1 arquivos
# Resolução 901x672: 1 arquivos
# Resolução 777x596: 1 arquivos
# Resolução 96x57: 1 arquivos
# Resolução 723x585: 1 arquivos
# Resolução 21x27: 1 arquivos
# Resolução 715x597: 1 arquivos
# Resolução 35x58: 1 arquivos
# Resolução 852x610: 1 arquivos
# Resolução 829x624: 1 arquivos
# Resolução 408x486: 1 arquivos
# Resolução 245x364: 1 arquivos
# Resolução 725x594: 1 arquivos
# Resolução 39x19: 1 arquivos
# Resolução 21x36: 1 arquivos
# Resolução 815x616: 1 arquivos
# Resolução 735x588: 1 arquivos
# Resolução 821x655: 1 arquivos
# Resolução 702x590: 1 arquivos
# Resolução 264x326: 1 arquivos
# Resolução 820x615: 1 arquivos
# Resolução 361x436: 1 arquivos
# Resolução 335x415: 1 arquivos
# Resolução 718x578: 1 arquivos
# Resolução 738x599: 1 arquivos
# Resolução 39x78: 1 arquivos
# Resolução 429x569: 1 arquivos
# Resolução 10x8: 1 arquivos
# Resolução 408x507: 1 arquivos
# Resolução 754x679: 1 arquivos
# Resolução 771x609: 1 arquivos
# Resolução 757x622: 1 arquivos
# Resolução 789x687: 1 arquivos
# Resolução 27x40: 2 arquivos
# Resolução 16x19: 1 arquivos
# Resolução 49x27: 1 arquivos
# Resolução 268x340: 1 arquivos
# Resolução 58x74: 1 arquivos
# Resolução 728x611: 1 arquivos
# Resolução 49x73: 1 arquivos
# Resolução 748x593: 1 arquivos
# Resolução 420x495: 1 arquivos
# Resolução 55x76: 1 arquivos
# Resolução 234x312: 1 arquivos
# Resolução 160x224: 1 arquivos
# Resolução 20x39: 1 arquivos
# Resolução 711x561: 1 arquivos
# Resolução 32x49: 1 arquivos
# Resolução 754x615: 1 arquivos
# Resolução 821x616: 1 arquivos
# Resolução 750x703: 1 arquivos
# Resolução 408x525: 1 arquivos
# Resolução 767x666: 1 arquivos
# Resolução 772x613: 1 arquivos
# Resolução 592x756: 1 arquivos
# Resolução 356x464: 1 arquivos
# Resolução 783x691: 1 arquivos
# Resolução 206x359: 1 arquivos
# Resolução 225x324: 1 arquivos
# Resolução 31x31: 1 arquivos
# Resolução 414x510: 1 arquivos
# Resolução 739x674: 1 arquivos
# Resolução 753x588: 1 arquivos
# Resolução 780x592: 1 arquivos
# Resolução 42x56: 1 arquivos
# Resolução 800x621: 1 arquivos
# Resolução 40x46: 1 arquivos
# Resolução 703x595: 1 arquivos
# Resolução 270x328: 1 arquivos
# Resolução 749x698: 1 arquivos
# Resolução 99x126: 1 arquivos
# Resolução 1016x866: 1 arquivos
# Resolução 33x20: 1 arquivos
# Resolução 31x70: 1 arquivos
# Resolução 826x703: 1 arquivos
# Resolução 308x444: 1 arquivos
# Resolução 759x593: 1 arquivos
# Resolução 384x495: 1 arquivos
# Resolução 90x78: 1 arquivos
# Resolução 100x115: 1 arquivos
# Resolução 320x408: 1 arquivos
# Resolução 936x688: 1 arquivos
# Resolução 284x328: 1 arquivos
# Resolução 23x36: 1 arquivos
# Resolução 19x37: 1 arquivos
# Resolução 57x47: 1 arquivos
# Resolução 725x610: 1 arquivos
# Resolução 806x701: 1 arquivos
# Resolução 44x29: 1 arquivos
# Resolução 792x694: 1 arquivos
# Resolução 777x639: 1 arquivos
# Resolução 168x204: 1 arquivos
# Resolução 36x38: 1 arquivos
# Resolução 734x621: 1 arquivos
# Resolução 733x607: 1 arquivos
# Resolução 832x641: 1 arquivos
# Resolução 810x662: 1 arquivos
# Resolução 29x54: 1 arquivos
# Resolução 130x169: 1 arquivos
# Resolução 782x587: 1 arquivos
# Resolução 713x600: 1 arquivos
# Resolução 262x344: 1 arquivos
# Resolução 723x581: 1 arquivos
# Resolução 19x75: 1 arquivos
# Resolução 851x636: 1 arquivos
# Resolução 702x600: 1 arquivos
# Resolução 718x603: 1 arquivos
# Resolução 31x47: 1 arquivos
# Resolução 62x89: 1 arquivos
# Resolução 50x59: 1 arquivos
# Resolução 715x590: 1 arquivos
# Resolução 24x29: 1 arquivos
# Resolução 330x430: 1 arquivos
# Resolução 719x634: 1 arquivos
# Resolução 37x53: 1 arquivos
# Resolução 91x60: 1 arquivos
# Resolução 825x695: 1 arquivos
# Resolução 284x340: 1 arquivos
# Resolução 775x743: 1 arquivos
# Resolução 720x573: 1 arquivos
# Resolução 742x598: 1 arquivos
# Resolução 794x606: 1 arquivos
# Resolução 719x591: 1 arquivos
# Resolução 142x156: 1 arquivos
# Resolução 737x596: 1 arquivos
# Resolução 832x604: 1 arquivos
# Resolução 79x101: 1 arquivos
# Resolução 708x595: 1 arquivos
# Resolução 202x273: 1 arquivos
# Resolução 24x21: 1 arquivos
# Resolução 195x267: 1 arquivos
# Resolução 92x76: 1 arquivos
# Resolução 925x640: 1 arquivos
# Resolução 17x24: 1 arquivos
# Resolução 865x763: 1 arquivos
# Resolução 721x617: 1 arquivos
# Resolução 730x602: 1 arquivos
# Resolução 729x589: 1 arquivos
# Resolução 225x330: 1 arquivos
# Resolução 327x417: 1 arquivos
# Resolução 50x98: 1 arquivos
# Resolução 717x569: 1 arquivos
# Resolução 764x625: 1 arquivos
# Resolução 23x16: 1 arquivos
# Resolução 37x12: 1 arquivos
# Resolução 61x63: 1 arquivos
# Resolução 414x504: 1 arquivos
# Resolução 425x567: 1 arquivos
# Resolução 71x57: 1 arquivos
# Resolução 783x608: 1 arquivos
# Resolução 760x618: 1 arquivos
# Resolução 14x12: 1 arquivos
# Resolução 290x375: 1 arquivos
# Resolução 35x30: 2 arquivos
# Resolução 28x26: 1 arquivos
# Resolução 734x575: 1 arquivos
# Resolução 787x608: 1 arquivos
# Resolução 930x712: 1 arquivos
# Resolução 722x581: 1 arquivos
# Resolução 443x612: 1 arquivos
# Resolução 66x68: 1 arquivos
# Resolução 731x622: 1 arquivos
# Resolução 246x309: 1 arquivos
# Resolução 77x117: 1 arquivos
# Resolução 10x7: 1 arquivos
# Resolução 306x320: 1 arquivos
# Resolução 851x808: 1 arquivos
# Resolução 38x76: 1 arquivos
# Resolução 733x615: 1 arquivos
# Resolução 790x623: 1 arquivos
# Resolução 399x513: 1 arquivos
# Resolução 317x461: 1 arquivos
# Resolução 738x660: 1 arquivos
# Resolução 14x18: 1 arquivos
# Resolução 414x495: 1 arquivos
# Resolução 45x43: 1 arquivos
# Resolução 33x28: 1 arquivos
# Resolução 713x586: 1 arquivos
# Resolução 31x27: 1 arquivos
# Resolução 889x673: 1 arquivos
# Resolução 37x48: 1 arquivos
# Resolução 875x639: 1 arquivos
# Resolução 739x613: 1 arquivos
# Resolução 705x617: 1 arquivos
# Resolução 63x119: 1 arquivos
# Resolução 290x346: 1 arquivos
# Resolução 33x53: 1 arquivos
# Resolução 384x453: 1 arquivos
# Resolução 40x61: 1 arquivos
# Resolução 809x737: 1 arquivos
# Resolução 65x89: 1 arquivos
# Resolução 762x669: 1 arquivos
# Resolução 761x630: 1 arquivos
# Resolução 747x611: 1 arquivos
# Resolução 876x728: 1 arquivos
# Resolução 888x666: 1 arquivos
# Resolução 1098x816: 1 arquivos
# Resolução 453x588: 1 arquivos
# Resolução 820x629: 1 arquivos
# Resolução 749x605: 1 arquivos
# Resolução 28x19: 1 arquivos
# Resolução 36x23: 1 arquivos
# Resolução 7x6: 1 arquivos
# Resolução 31x39: 1 arquivos
# Resolução 111x85: 1 arquivos
# Resolução 424x538: 1 arquivos
# Resolução 26x31: 1 arquivos
# Resolução 274x336: 1 arquivos
# Resolução 768x625: 1 arquivos
# Resolução 860x665: 1 arquivos
# Resolução 22x36: 1 arquivos
# Resolução 462x513: 1 arquivos
# Resolução 907x590: 1 arquivos
# Resolução 34x36: 1 arquivos
# Resolução 516x624: 1 arquivos
# Resolução 709x606: 1 arquivos
# Resolução 55x62: 1 arquivos
