from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

AQUILIFY_THEME = """
*************** TERMINAL ***************
*          WELCOME TO AQUILIFY         *
*                                      *
* DATETIME - {}      *
* VERSION - 1.15                       *
*                                      *
****************************************
""".format(
    datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
)

AX_VERSION = [
    f"Aquilify v1.10 (previous) ...{Colors.WARNING}Outdated!{Colors.ENDC}",
    f"Aquilify v1.11 (previous-fixed) ...{Colors.WARNING}Outdated!{Colors.ENDC}",
    f"Aquilify v1.12 (--upgrade) ...{Colors.WARNING}Outdated!{Colors.ENDC}",
    f"Aquilify v1.13 (previous-fixed) ...{Colors.OKGREEN}Outdated!{Colors.ENDC}",
    f"Aquilify v1.14 (--upgrade) ...{Colors.OKGREEN}Outdated!{Colors.ENDC}",
    f"Aquilify v1.15 (--upgrade) ...{Colors.OKGREEN}Stable!{Colors.ENDC}",
    f"{Colors.OKGREEN}Aquilify v1.16 (Latest){Colors.ENDC} ...{Colors.OKGREEN}Stable!{Colors.ENDC}"
]