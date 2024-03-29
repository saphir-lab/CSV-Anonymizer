import os

APP_VERSION = "V 2.0.0"
DESIGNED_BY = "Designed by P. Saint-Amand"

# Some interresting path
CUR_DIR=os.path.dirname(os.path.abspath(__file__))
DATA_DIR=os.path.join(CUR_DIR,"data")
LOG_DIR=os.path.join(CUR_DIR,"log")
SETTING_FILE = os.path.join(CUR_DIR,"settings.yaml")

# List of Valid choices
VALID_HASHING = ["blake2s", "blake2b", "md5", "sha1", "sha224", "sha256", "sha384", "sha512", "sha3_224", "sha3_256", "sha3_384", "sha3_512"]
VALID_ALGORITHM = ["index", "length"] + VALID_HASHING
INVALID_SEPARATOR = ['<', '>', ':', '"', '/', '\\', '|', '?','*']


banner_lst = [
"""
  ___  ___  _  _      __    _  _  _____  _  _  _  _  __  __  ____  ____  ____  ____ 
 / __)/ __)( \\/ )    /__\\  ( \\( )(  _  )( \\( )( \\/ )(  \\/  )(_  _)(_   )( ___)(  _ \\
( (__ \\__ \\ \\  /    /(__)\\  )  (  )(_)(  )  (  \\  /  )    (  _)(_  / /_  )__)  )   /
 \\___)(___/  \\/    (__)(__)(_)\\_)(_____)(_)\\_) (__) (_/\\/\\_)(____)(____)(____)(_)\\_)
""",
"""
   ____  ____   __     __          _      _   _     U  ___ u  _   _     __   __  __  __              _____ U _____ u   ____     
U /"___|/ __"| u\\ \\   /"/u     U  /"\\  u | \\ |"|     \\/"_ \\/ | \\ |"|    \\ \\ / /U|' \\/ '|u   ___     |"_  /u\\| ___"|/U |  _"\\ u  
\\| | u <\\___ \\/  \\ \\ / //       \\/ _ \\/ <|  \\| |>    | | | |<|  \\| |>    \\ V / \\| |\\/| |/  |_"_|    U / //  |  _|"   \\| |_) |/  
 | |/__ u___) |  /\\ V /_,-.     / ___ \\ U| |\\  |u.-,_| |_| |U| |\\  |u   U_|"|_u | |  | |    | |     \\/ /_   | |___    |  _ <    
  \\____||____/>>U  \\_/-(_/     /_/   \\_\\ |_| \\_|  \\_)-\\___/  |_| \\_|      |_|   |_|  |_|  U/| |\\u   /____|  |_____|   |_| \\_\\   
 _// \\\\  )(  (__) //            \\\\    >> ||   \\\\,-.    \\\\    ||   \\\\,-.-,//|(_ <<,-,,-..-,_|___|_,-._//<<,- <<   >>   //   \\\\_  
(__)(__)(__)     (__)          (__)  (__)(_")  (_/    (__)   (_")  (_/ \\_) (__) (./  \\.)\\_)-' '-(_/(__) (_/(__) (__) (__)  (__) 
""",
"""
        (                                                                         
   (    )\\ )            (                                                         
   )\\  (()/( (   (      )\\                       (        )    (         (   (    
 (((_)  /(_)))\\  )\\  ((((_)(   (      (    (     )\\ )    (     )\\  (    ))\\  )(   
 )\\___ (_)) ((_)((_)  )\\ _ )\\  )\\ )   )\\   )\\ ) (()/(    )\\  '((_) )\\  /((_)(()\\  
((/ __|/ __|\\ \\ / /   (_)_\\(_)_(_/(  ((_) _(_/(  )(_)) _((_))  (_)((_)(_))   ((_) 
 | (__ \\__ \\ \\ V /     / _ \\ | ' \\))/ _ \\| ' \\))| || || '  \\() | ||_ // -_) | '_| 
  \\___||___/  \\_/     /_/ \\_\\|_||_| \\___/|_||_|  \\_, ||_|_|_|  |_|/__|\\___| |_|   
                                                 |__/                             
""",
"""
     c  c  oo_   wWw    wWw           \\\\\\  ///   .-.   \\\\\\  ///wWw  wWw\\\\\\    ///wW  Ww   _oo  wWw ()_()  
     (OO) /  _)-<(O)    (O)       /)  ((O)(O)) c(O_O)c ((O)(O))(O)  (O)((O)  (O))(O)(O)>-(_  \\ (O)_(O o)  
   ,'.--.)\\__ `. ( \\    / )     (o)(O) | \\ || ,'.---.`, | \\ || ( \\  / ) | \\  / |  (..)    / _/ / __)|^_\\  
  / //_|_\\   `. | \\ \\  / /       //\\\\  ||\\\\||/ /|_|_|\\ \\||\\\\||  \\ \\/ /  ||\\\\//||   ||    / /  / (   |(_)) 
  | \\___     _| | /  \\/  \\      |(__)| || \\ || \\_____/ ||| \\ |   \\o /   || \\/ ||  _||_  / (  (  _)  |  /  
  \'.    ) ,-'   | \\ `--' /      /,-. | ||  ||\'. `---' .`||  ||  _/ /    ||    || (_/\\_)(   `-.\\ \\_  )|\\\\  
    `-.' (_..--'   `-..-'      -'   ''(_/  \\_) `-...-' (_/  \\_)(_.'    (_/    \\_)       `--.._)\\__)(/  \\) 
""",
"""
  ___  ____  _  _     __   __ _   __   __ _  _  _  _  _  __  ____  ____  ____ 
 / __)/ ___)/ )( \\   / _\\ (  ( \\ /  \\ (  ( \\( \\/ )( \\/ )(  )(__  )(  __)(  _ \\
( (__ \\___ \\\\ \\/ /  /    \\/    /(  O )/    / )  / / \\/ \\ )(  / _/  ) _)  )   /
 \\___)(____/ \\__/   \\_/\\_/\\_)__) \\__/ \\_)__)(__/  \\_)(_/(__)(____)(____)(__\\_)
""",
"""                                                              
 _____ _____ _____    _____                       _             
|     |   __|  |  |  |  _  |___ ___ ___ _ _ _____|_|___ ___ ___ 
|   --|__   |  |  |  |     |   | . |   | | |     | |- _| -_|  _|
|_____|_____|\\___/   |__|__|_|_|___|_|_|_  |_|_|_|_|___|___|_|  
                                       |___|                    
""",
"""
   ____________    __   ___                                      _                
  / ____/ ___/ |  / /  /   |  ____  ____  ____  __  ______ ___  (_)___  ___  _____
 / /    \\__ \\| | / /  / /| | / __ \\/ __ \\/ __ \\/ / / / __ `__ \\/ /_  / / _ \\/ ___/
/ /___ ___/ /| |/ /  / ___ |/ / / / /_/ / / / / /_/ / / / / / / / / /_/  __/ /    
\\____//____/ |___/  /_/  |_/_/ /_/\\____/_/ /_/\\__, /_/ /_/ /_/_/ /___/\\___/_/     
                                             /____/                               
""",
"""
  ,--,    .---..-.   .-.   .--.  .-. .-. .---.  .-. .-..-.   .-.        ,-. _____  ,---.  ,---.    
.' .')   ( .-._)\\ \\ / /   / /\\ \\ |  \\| |/ .-. ) |  \\| | \\ \\_/ )/|\\    /||(|/___  / | .-'  | .-.\\   
|  |(_) (_) \\    \\ V /   / /__\\ \\|   | || | |(_)|   | |  \\   (_)|(\\  / |(_)   / /) | `-.  | `-'/   
\\  \\    _  \\ \\    ) /    |  __  || |\\  || | | | | |\\  |   ) (   (_)\\/  || |  / /(_)| .-'  |   (    
 \\  `-.( `-'  )  (_)     | |  |)|| | |)|\\ `-' / | | |)|   | |   | \\  / || | / /___ |  `--.| |\\ \\   
  \\____\\`----'           |_|  (_)/(  (_) )---'  /(  (_)  /(_|   | |\\/| |`-'(_____/ /( __.'|_| \\)\\  
                                (__)    (_)    (__)     (__)    '-'  '-'          (__)        (__) 
""",
"""
   ______   ______  ____   ____        _                                                       _                        
 .' ___  |.' ____ \\|_  _| |_  _|      / \\                                                     (_)                       
/ .'   \\_|| (___ \\_| \\ \\   / /       / _ \\     _ .--.   .--.   _ .--.    _   __  _ .--..--.   __   ____  .---.  _ .--.  
| |        _.____`.   \\ \\ / /       / ___ \\   [ `.-. |/ .'`\\ \\[ `.-. |  [ \\ [  ][ `.-. .-. | [  | [_   ]/ /__\\\\[ `/'`\\] 
\\ `.___.'\\| \\____) |   \\ ' /      _/ /   \\ \\_  | | | || \\__. | | | | |   \\ '/ /  | | | | | |  | |  .' /_| \\__., | |     
 `.____ .' \\______.'    \\_/      |____| |____|[___||__]'.__.' [___||__][\\_:  /  [___||__||__][___][_____]'.__.'[___]    
                                                                        \\__.'                                           
""",
"""
 ▄████▄    ██████ ██▒   █▓    ▄▄▄       ███▄    █  ▒█████   ███▄    █▓██   ██▓ ███▄ ▄███▓ ██▓▒███████▒▓█████  ██▀███  
▒██▀ ▀█  ▒██    ▒▓██░   █▒   ▒████▄     ██ ▀█   █ ▒██▒  ██▒ ██ ▀█   █ ▒██  ██▒▓██▒▀█▀ ██▒▓██▒▒ ▒ ▒ ▄▀░▓█   ▀ ▓██ ▒ ██▒
▒▓█    ▄ ░ ▓██▄   ▓██  █▒░   ▒██  ▀█▄  ▓██  ▀█ ██▒▒██░  ██▒▓██  ▀█ ██▒ ▒██ ██░▓██    ▓██░▒██▒░ ▒ ▄▀▒░ ▒███   ▓██ ░▄█ ▒
▒▓▓▄ ▄██▒  ▒   ██▒ ▒██ █░░   ░██▄▄▄▄██ ▓██▒  ▐▌██▒▒██   ██░▓██▒  ▐▌██▒ ░ ▐██▓░▒██    ▒██ ░██░  ▄▀▒   ░▒▓█  ▄ ▒██▀▀█▄  
▒ ▓███▀ ░▒██████▒▒  ▒▀█░      ▓█   ▓██▒▒██░   ▓██░░ ████▓▒░▒██░   ▓██░ ░ ██▒▓░▒██▒   ░██▒░██░▒███████▒░▒████▒░██▓ ▒██▒
░ ░▒ ▒  ░▒ ▒▓▒ ▒ ░  ░ ▐░      ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▒░   ▒ ▒   ██▒▒▒ ░ ▒░   ░  ░░▓  ░▒▒ ▓░▒░▒░░ ▒░ ░░ ▒▓ ░▒▓░
  ░  ▒   ░ ░▒  ░ ░  ░ ░░       ▒   ▒▒ ░░ ░░   ░ ▒░  ░ ▒ ▒░ ░ ░░   ░ ▒░▓██ ░▒░ ░  ░      ░ ▒ ░░░▒ ▒ ░ ▒ ░ ░  ░  ░▒ ░ ▒░
░        ░  ░  ░      ░░       ░   ▒      ░   ░ ░ ░ ░ ░ ▒     ░   ░ ░ ▒ ▒ ░░  ░      ░    ▒ ░░ ░ ░ ░ ░   ░     ░░   ░ 
░ ░            ░       ░           ░  ░         ░     ░ ░           ░ ░ ░            ░    ░    ░ ░       ░  ░   ░     
░                     ░                                               ░ ░                    ░                        
"""
]


if __name__ == "__main__":
    import os
    import random
    os.system('cls||clear')

    print(CUR_DIR)
    print(DATA_DIR)
    print(LOG_DIR)
    print(SETTING_FILE)

    r = random.randrange(len(banner_lst))
    print(banner_lst[r])
    print(r)
