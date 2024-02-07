from modules import colors
from modules import clrscr
 
class Banner:
    def __init__(self):
        print(colors.bcolors.WARNING + '''
        
                 ███████                                     ██   ████         
                ░██░░░░██                                   ░░   ░██░   ██   ██
                ░██    ░██  ██████   ██████  ██████   ██████ ██ ██████ ░░██ ██ 
                ░██    ░██ ░░░░░░██ ░░██░░█ ░░░░░░██ ░░░░██ ░██░░░██░   ░░███  
                ░██    ░██  ███████  ░██ ░   ███████    ██  ░██  ░██     ░██   
                ░██    ██  ██░░░░██  ░██    ██░░░░██   ██   ░██  ░██     ██    
                ░███████  ░░████████░███   ░░████████ ██████░██  ░██    ██     
                ░░░░░░░    ░░░░░░░░ ░░░     ░░░░░░░░ ░░░░░░ ░░   ░░    ░░   
    ''' + colors.bcolors.ENDC)

        print(f'''

                                        {colors.bcolors.RED}♥{colors.bcolors.ENDC} v 1.01 {colors.bcolors.RED}♥{colors.bcolors.ENDC}
                                Created by : {colors.bcolors.OKGREEN}RaNa MazHar Naseer{colors.bcolors.ENDC}
                                  {colors.bcolors.OKBLUE}https://github.com/mazuu06{colors.bcolors.ENDC}
                                    
            {colors.bcolors.BOLD}Welcome to {colors.bcolors.ENDC}

            {colors.bcolors.NOTICE}This tool is for educational purposes only and the creator is not responsible for any actions performed by the users.{colors.bcolors.ENDC}
            
        ''')

        temp = input(f'{colors.bcolors.LOGGING}Your output also save in {colors.bcolors.BOLD}{colors.bcolors.OKGREEN}output.txt{colors.bcolors.ENDC}{colors.bcolors.LOGGING} file.{colors.bcolors.ENDC} Press ENTER to continue: ')
