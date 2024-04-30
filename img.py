import os
import sys
import msvcrt
import ctypes
from tkinter import filedialog
from colorama import Fore, init
from PIL import Image as PilImage
import pystray
from pystyle import System, Center, Anime, Colors, Colorate

init(autoreset=True)

STD_OUTPUT_HANDLE = -11
HANDEL = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def gotoxy(x, y):
    position = y * 100 + x
    ctypes.windll.kernel32.SetConsoleCursorPosition(HANDEL, position)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text, width):
    return text.center(width)

def await_enter():
    while True:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 13:
                break

def convert_image():
    img_path = select_image()
    if img_path:
        new_extensions = ["PNG", "JPEG", "GIF", "ICO", "BMP", "TIFF", "WEBP", "JP2", "JPC", "PGF", "RAS", "TGA", "TIFF", "WBMP", "XBM"]  
        selected_option = select_option(new_extensions)
        new_extension = new_extensions[selected_option].strip(f"{Fore.RED}")
        if new_extension == "ICO":
            image = PilImage.open(img_path)
            menu_icon = pystray.Icon("Byte - Image")
            menu_icon.icon = image
            ico_path = img_path.rsplit(".", 1)[0] + ".ico"
            with open(ico_path, "wb") as ico_file:
                menu_icon.icon.save(ico_file, format="ICO")
            print(f"Image successfully converted to ICO: {ico_path}")
        else:
            new_path = img_path.rsplit(".", 1)[0] + f".{new_extension.lower()}"
            image = PilImage.open(img_path)
            image.save(new_path)
            print(f"Image successfully converted to {new_extension}!")
    else:
        print("No file selected.")

def select_image():
    img_path = filedialog.askopenfilename()
    return img_path

def resize_image():
    img_path = select_image()
    if img_path:
        try:
            width = int(input("Enter the desired width for the image: "))
            height = int(input("Enter the desired height for the image: "))
            if width <= 0 or height <= 0:
                raise ValueError("Width and height must be positive integers.")
            image = PilImage.open(img_path)
            image_resized = image.resize((width, height))
            image_resized.save(img_path)
            print("Image successfully resized!")
        except ValueError as ve:
            print(f"Error: {ve}")
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Permission denied to access the file.")
        except Exception as e:
            print(f"An error occurred while resizing the image: {e}")
    else:
        print("No file selected.")

def select_option(options):
    selected_option = 0
    show_menu(options, selected_option)

    while True:
        key = ord(msvcrt.getch())

        if key == 72:  
            selected_option = (selected_option - 1) % len(options)
        elif key == 80:  
            selected_option = (selected_option + 1) % len(options)
        elif key == 13:  
            return selected_option

        show_menu(options, selected_option)

def show_menu(options, selected_option):
    clear_screen()
    window_width, _ = os.get_terminal_size()
    print(center_text(f"{Fore.RED}Byte - Image", window_width))
    print()

    for i, option in enumerate(options):
        if i == selected_option:
            print(f"{Fore.RED}> {Fore.LIGHTBLACK_EX}{option}")
        else:
            print(f"  {option}")

    print()  

def print_intro():
    byte = r'''                                                                                                                                                
 ██▓ ███▄ ▄███▓ ▄▄▄        ▄████ ▓█████    
▓██▒▓██▒▀█▀ ██▒▒████▄     ██▒ ▀█▒▓█   ▀    
▒██▒▓██    ▓██░▒██  ▀█▄  ▒██░▄▄▄░▒███      
░██░▒██    ▒██ ░██▄▄▄▄██ ░▓█  ██▓▒▓█  ▄    
░██░▒██▒   ░██▒ ▓█   ▓██▒░▒▓███▀▒░▒████▒   
░▓  ░ ▒░   ░  ░ ▒▒   ▓▒█░ ░▒   ▒ ░░ ▒░ ░   
 ▒ ░░  ░      ░  ▒   ▒▒ ░  ░   ░  ░ ░  ░   
 ▒ ░░      ░     ░   ▒   ░ ░   ░    ░      
 ░         ░         ░  ░      ░    ░  ░   

        
'''
    System.Size(80, 25)
    System.Clear()
    Anime.Fade(Center.Center(byte), Colors.red_to_black,  Colorate.Vertical, interval=0.085, enter=True)

def main():
    print_intro()

    while True:
        System.Size(42, 7)
        options = [
            f"Convert Image {Fore.RED}",
            "Resize image",
            "Exit the program"
        ]
        selected_option = select_option(options)

        if selected_option == 0:
            System.Size(77, 19)
            convert_image()
        elif selected_option == 1:
            resize_image()
        elif selected_option == 2:
            print(f"{Fore.WHITE}Exiting program...")
            sys.exit()

if __name__ == "__main__":
    main()
