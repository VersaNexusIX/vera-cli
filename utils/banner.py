from colorama import Fore, Style

def show_success_banner(file_path):
    print(Fore.GREEN + """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ✅  DOWNLOAD SELESAI WOK!   
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
""" + Style.RESET_ALL)
    print(f"📁 File disimpan di:\n{Fore.CYAN}{file_path}{Style.RESET_ALL}\n")
    print("🧃 Teh tanpa gula siap diminum.\n🌿 Ritual selesai. VERA standby.\n")

def show_error_banner(message):
    print(Fore.RED + """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃   ❌  DOWNLOAD GAGAL WAK 😿 
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
""" + Style.RESET_ALL)
    print(f"📛 Pesan error:\n{Fore.YELLOW}{message}{Style.RESET_ALL}\n")
    print("🔍 Cek koneksi, API key, atau struktur URL.\n")