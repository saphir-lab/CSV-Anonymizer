### Import external modules
import random
import colorama as c
c.init()

# Color used per message Type
COLOR = {
    "STANDARD": c.Style.RESET_ALL,
    "BANNER": c.Fore.LIGHTGREEN_EX,
    "ERROR": c.Fore.RED,
    "WARNING": c.Fore.YELLOW,
    "INFO": c.Fore.CYAN,
    "SUCCESS": c.Fore.GREEN,
    "APP_VERSION": c.Fore.LIGHTYELLOW_EX,
    "DESIGNED_BY": c.Fore.LIGHTRED_EX
}

def get_app_banner(selection="random", banner_lst=[], colored=True, appversion="", creator=""):
    """ Construct an AppBanner from a possible list toghether with application version and application creator

    Args:
        selection (str, optional): _description_. Defaults to "random".
        banner_lst (list, optional): _description_. Defaults to [].
        colored (bool, optional): determine if banner should use colors. Defaults to True.
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

        if app_banner and not colored:
            app_banner = (app_banner
                        + "\n" + appversion
                        + "\t"*6 + creator
                        + "\n"
                    )
        elif app_banner and colored:
            app_banner = (COLOR["BANNER"] + app_banner
                        + "\n" + COLOR["APP_VERSION"] + appversion
                        + "\t"*6 + COLOR["DESIGNED_BY"] + creator
                        + COLOR["STANDARD"] + "\n"
                    )
    return app_banner

def print_msg(severity, msg, colored=True):
    """ Print a message in appropriate color depending of a severity criteria (ERROR, WARNING? INFO, etc)."""
    severity = severity.upper()
    if colored:
        msg = COLOR[severity] + msg + COLOR["STANDARD"]
    else:
        msg = "*** " + msg
    print(msg)
