### Import external modules
import os
import random
import colorama as c

class Console():
    def __init__(self, colored=True):
        # Color used per message Type
        self.COLOR = {
            "STANDARD": c.Style.RESET_ALL,
            "BANNER": c.Fore.LIGHTGREEN_EX,
            "ERROR": c.Fore.RED,
            "WARNING": c.Fore.YELLOW,
            "INFO": c.Fore.CYAN,
            "SUCCESS": c.Fore.GREEN,
            "APP_VERSION": c.Fore.LIGHTYELLOW_EX,
            "DESIGNED_BY": c.Fore.LIGHTRED_EX
        }

        self.MSG_SEVERITY = {
            "STANDARD": "",
            "BANNER": "",
            "ERROR": "[ERROR] ",
            "WARNING": "[WARNING] ",
            "INFO": "[INFO] ",
            "SUCCESS": "[OK] ",
            "APP_VERSION": "",
            "DESIGNED_BY": ""
        }

        self.app_banner=""
        self.colored=colored
        c.init()

    def clear_screen(self):
        os.system("cls||clear")

    def get_app_banner(self, selection="random", banner_lst=[], appversion="", creator=""):
        """ Construct an AppBanner from a possible list toghether with application version and application creator

        Args:
            selection (str, optional): _description_. Defaults to "random".
            banner_lst (list, optional): _description_. Defaults to [].
            appversion (str, optional): Add application version below the banner. Defaults to "".
            creator (str, optional): Add creator name below the banner. Defaults to "".

        Returns:
            str: a formatted banner
        """
        app_banner = ""
        if selection is not None:
            selection = selection.lower() 
            if selection == "random":
                app_banner = banner_lst[random.randrange(len(banner_lst))]
            elif selection.isdecimal():
                i = int(selection) % len(banner_lst)
                app_banner = banner_lst[i]
            else:
                app_banner = banner_lst[0]

            if app_banner and not self.colored:
                app_banner = (app_banner
                            + "\n" + appversion
                            + "\t"*6 + creator
                            + "\n"
                        )
            elif app_banner and self.colored:
                app_banner = (self.COLOR["BANNER"] + app_banner
                            + "\n" + self.COLOR["APP_VERSION"] + appversion
                            + "\t"*6 + self.COLOR["DESIGNED_BY"] + creator
                            + self.COLOR["STANDARD"] + "\n"
                        )
        return app_banner

    def print_msg(self, severity, msg):
        """ Print a message in appropriate color depending of a severity criteria (ERROR, WARNING, INFO, etc)."""
        severity = severity.upper()
        msg = self.MSG_SEVERITY[severity] + msg
        if self.colored:
            msg = self.COLOR[severity] + msg + self.COLOR["STANDARD"]
        # else:
        #     msg = self.MSG_SEVERITY[severity] + msg
        print(msg)
