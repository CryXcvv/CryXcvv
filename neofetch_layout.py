import os
import sys
import socket
import platform
import time

# ASCII Art yang kamu berikan
ascii_art = r"""
                                                              
                                                              
                                                              
                                                  *@@@@:                      
                                    :@@%.         @@@@@#                      
                                    @@@@@          @@@=                       
                                    .%@#           #@@@+    =@@@@=            
                                     #@@%.        @@@@@@@  .@@@@@@=           
                                    *@@@@@@@@@@@@@@@@@@@@@  @@@@@@            
                               -@@@@@-  -@@@@@@        @@@@@@@@%.                 
                              -@@@@@@@.  #@@@*          -#-.   @@@@%*+            
                               @@@@@@@.   -@:  %@@@@@@#        @@@@@@@@.          
                                *%@%=         %@@@@@@@@#      =@@@@@@@@.          
                                              #@@@@@@@@*      @@@@@@@@:           
                                @@@@@@@.        +@@@@@@-      @@@@@@@@.            
                              :@@@@@@@@@-                 =@@@@@@@@@@.            
                               =@@@@@@@@@@%-   *@@@@@@@@@@@@@@@@@@@@@=            
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@            
                                  %@@@@@@@@@@@@@@@@@@@@@@@@@@@@   .@@@@*            
                                  -@@@@@@%=@@@@@@@@@@@@@@@@@@@.                     
                                  -@@@@@%   .@@@@@@@@@@@@@@*                      
                                  -@@@@@     =@@@@@@@@@@@@*                       
                                  .@@@@@      .@@@@@@@@@@:                        
                                    :#:        =@@@@@@@@%                         
                                                @@@@@@@@%                         
                                                 #@@@@@@#                         
                                                              
                                                              
                                                              
                                                              
                                                              
"""

def get_gradient_color(start_rgb, end_rgb, step, total_steps):
    """Menghitung warna RGB antara start dan end untuk gradasi"""
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * step / total_steps)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * step / total_steps)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * step / total_steps)
    return f"\033[38;2;{r};{g};{b}m"

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        uptime_minutes = uptime_seconds / 60
        uptime_hours = uptime_minutes / 60
        uptime_days = uptime_hours / 24
        
        if uptime_days > 1:
            return f"{int(uptime_days)} days, {int(uptime_hours % 24)} hours"
        elif uptime_hours > 1:
            return f"{int(uptime_hours)} hours, {int(uptime_minutes % 60)} mins"
        else:
            return f"{int(uptime_minutes)} mins"
    except:
        return "Unknown"

def get_cpu_info():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'Hardware' in line: # Untuk ARM/Android
                    return line.split(':')[1].strip()
                if 'model name' in line: # Untuk x86
                    return line.split(':')[1].strip()
        return "Unknown ARM Processor"
    except:
        return "Unknown CPU"

def get_memory_info():
    try:
        with open('/proc/meminfo', 'r') as f:
            mem_info = f.readlines()
            mem_total = int(mem_info[0].split()[1])
            mem_available = int(mem_info[2].split()[1]) # MemAvailable lebih akurat di kernel baru
            
            used = mem_total - mem_available
            used_mb = used // 1024
            total_mb = mem_total // 1024
            
            return f"{used_mb}MiB / {total_mb}MiB"
    except:
        return "Unknown RAM"

def get_shell():
    return os.environ.get('SHELL', 'Unknown Shell')

def get_terminal_width():
    """Mendapatkan lebar terminal"""
    try:
        return os.get_terminal_size().columns
    except:
        return 120

def center_text(text, width):
    """Memusatkan teks dalam lebar yang diberikan"""
    return text.center(width)

def main():
    # Warna Gradasi: Merah (atas) ke Hitam (bawah)
    start_color = (255, 60, 60)     # Merah terang (atas)
    end_color = (0, 0, 0)           # Hitam (bawah)
    
    # Data Sistem
    user = os.getlogin()
    hostname = socket.gethostname()
    os_name = "Android " + platform.release() # Termux berjalan di Android
    kernel = platform.version()
    uptime = get_uptime()
    cpu = get_cpu_info()
    memory = get_memory_info()
    shell = get_shell()
    
    # Format Info dengan styling lebih besar
    info_lines = [
        f"\033[1;36m{user}@{hostname}\033[0m",
        f"\033[1;33m━━━━━━━━━━━━━━━━━━━━━━━\033[0m",
        f"\033[1;32mOS\033[0m         : {os_name}",
        f"\033[1;32mKernel\033[0m      : {kernel.split()[0]}",
        f"\033[1;32mUptime\033[0m      : {uptime}",
        f"\033[1;32mShell\033[0m       : {shell}",
        f"\033[1;32mCPU\033[0m         : {cpu}",
        f"\033[1;32mMemory\033[0m      : {memory}",
    ]
    
    # Proses ASCII Art
    art_lines = ascii_art.strip('\n').split('\n')
    total_lines = len(art_lines)
    
    # Dapatkan lebar terminal
    terminal_width = get_terminal_width()
    art_width = 50  # Lebar ASCII art
    spacing = 4     # Spasi antar kolom
    info_width = terminal_width - art_width - spacing
    
    reset_color = "\033[0m"
    
    # Cetak ASCII Art + Info secara berdampingan
    for i in range(max(total_lines, len(info_lines))):
        # Ambil baris ASCII art
        if i < total_lines:
            art_line = art_lines[i]
            color = get_gradient_color(start_color, end_color, i, total_lines)
            art_output = f"{color}{art_line}{reset_color}"
        else:
            art_output = ""
        
        # Ambil baris info
        if i < len(info_lines):
            info_output = info_lines[i]
        else:
            info_output = ""
        
        # Padakan panjang art_line agar alignment tetap rapi
        art_line_clean = art_lines[i] if i < total_lines else ""
        padding = art_width - len(art_line_clean)
        
        # Gabungkan art dan info
        sys.stdout.write(f"{art_output}{' ' * padding}{' ' * spacing}{info_output}\n")

if __name__ == "__main__":
    main()
