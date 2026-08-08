#!/usr/bin/env python3

import readline
import os
import subprocess
import sys
import curses
import shutil
import stat
import time

base_dir = os.path.dirname(os.path.abspath(__file__))

logo_file = "logo.txt"

sad=' '+':('

def login_screen():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(base_dir, "disk", "_sys", "boxshell.obsidOS")
    
    config = {
        "username": "kernel"
        "password:" "kernel"
    }
    
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    config[key.strip()] = val.strip()

    target_user = config.get("username", "kernel")
    show_logo = int(config.get("log_screen_logo", "1"))

    att = 3
    
    if show_logo == 1:
        print(gap)
        print(logo)
        print(gap)

    while att > 0:
        lsinp = input("login : ")
        if lsinp == target_user:
            os.system('clear')
            break
        else:
            att -= 1
            os.system('clear')
            print("nope try again\sad")
            
            if show_logo == 1:
                print(gap)
                print(logo)
                print(gap)

    if att == 0:
        print('failed try again later')
        sys.exit(1)

with open(logo_file, 'r') as f:
    logo = f.read()

enable_VD=1

if enable_VD==1:
    os.makedirs("disk", exist_ok=True)
    os.chdir("disk")
else:
    pass

commands='''help
clear
ls
cd
mkdir
exec(.py)
rm
touch
cat
date
pwd
cp
vim
make

pkgs_list
pkgs_rel

:q
:rb'''

empty=""

version='0.2'

username="kernel"

log_screen_logo=1

def reload_packages():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pkgs_dir = os.path.join(base_dir, "disk", "_pkgs")
    pkg_file = os.path.join(base_dir, "disk", "_sys", "packages.obsidOS")
    
    active_packages = {}
    if os.path.exists(pkg_file):
        with open(pkg_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    name, url = line.split("=", 1)
                    active_packages[name.strip()] = url.strip()

    if os.path.exists(pkgs_dir):
        for pkg in os.listdir(pkgs_dir):
            if pkg not in active_packages:
                remove_path = os.path.join(pkgs_dir, pkg)
                print(f"removing old package: {pkg}...")
                if os.path.isdir(remove_path):
                    shutil.rmtree(remove_path)

    os.makedirs(pkgs_dir, exist_ok=True)

    for repo_name, url in active_packages.items():
        dest_path = os.path.join(pkgs_dir, repo_name)
        
        if not os.path.exists(dest_path):
            cmd = f"git clone {url} {dest_path}"
            print(f"cloning {repo_name}...")
            os.system(cmd)

        cmake_file = os.path.join(dest_path, "CMakeLists.txt")
        if os.path.exists(cmake_file):
            build_cmd = f"cd {dest_path} && mkdir -p build && cd build && cmake -D CMAKE_BUILD_TYPE=Release -D ENABLE_VULKAN=OFF .. && make"
            print(f"building {repo_name}...")
            os.system(build_cmd)

    print("packages sync & reload complete!")

def read_packageses():
    with open('_sys/packages.obsidOS', 'r', encoding='utf-8') as file:
        print(file.read())

def login_screen():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(base_dir, "disk", "_sys", "boxshell.obsidOS")
    
    target_user = "kernel"
    target_pass = "kernel"
    show_logo = 1

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    k = key.strip()
                    v = val.strip()
                    if k == "username":
                        target_user = v
                    elif k == "password":
                        target_pass = v
                    elif k == "log_screen_logo":
                        show_logo = int(v)

        att = 3
    
        if show_logo == 1:
            print(gap)
            print(logo)
            print(gap)

        while att > 0:
            lsinp = input("login : ")
            pwdinp = input("password : ")
        
            if lsinp == target_user and pwdinp == target_pass:
                os.system('clear')
                break
            else:
                att -= 1
                os.system('clear')
                print("nope try again")
            
            if show_logo == 1:
                print(gap)
                print(logo)
                print(gap)

        if att == 0:
            print('failed try again later')
            sys.exit(1)

enable_clear_run=1
clearwhen_quit=1
logo_when_clear=1
helptitle=1
showver=1
auto_pkgrel_when_login=1

gapf='-'*60
gapf2='|'
gap=gapf+gapf2

if enable_clear_run==1:
    os.system('clear')
else:
    pass

#login
login_screen()

username = "kernel"
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "disk", "_sys", "boxshell.obsidOS")

if os.path.exists(config_file):
    with open(config_file, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("username"):
                if "=" in line:
                    _, val = line.split("=", 1)
                    username = val.strip()

#auto reload
if auto_pkgrel_when_login==1:
    os.system('clear')
    reload_packages()
    os.system('clear')

def logo_inf():
    if helptitle==1:
        print(gap)
        print('write help to see commands')
    else:
         pass

    print(gap)

    if showver==1:
        print('version: '+version)
        print(gap)
    else:
        pass

    print(logo)
    print(gap)
    print("")

logo_inf()

#boxshell
while True:
    #os.system('clear')
    inp=input(username+": >>> ")
    
    pkgs_base = os.path.join(base_dir, "disk", "_pkgs")
    executed = False
        
    if os.path.exists(pkgs_base):
        for pkg in os.listdir(pkgs_base):
            possible_paths = [
                os.path.join(pkgs_base, pkg, inp),
                os.path.join(pkgs_base, pkg, "build", inp)
            ]
            for p in possible_paths:
                if os.path.exists(p) and os.access(p, os.X_OK):
                    os.system(p)
                    executed = True
                    break
            if executed:
                break
        
    if executed:
        continue

    if not inp:
        continue
    
    if inp=="ls":
        for item in os.listdir():
    
            st = os.stat(item)
            mode = stat.filemode(st.st_mode)
            size = st.st_size
            mtime = time.strftime("%b %d %H:%M", time.localtime(st.st_mtime))
            
            print(f"{mode} {size:>6} {mtime} {item}")
        print(empty)

         
        continue

    if inp=='help':
        print(empty)
        print(commands)
        print(empty)
        
    elif inp=="clear":
        os.system('clear')
        if logo_when_clear==1:
            print(logo)
            print(gap)
        else:
            pass
        
    elif inp==":q":
        if clearwhen_quit==1:
            os.system('clear')
        else:
            pass
        
        break
        
    elif inp.startswith('mkdir'):
        name = inp.split(' ')[1]
        orig_name=name
        counter=0

        while os.path.exists(name):
            name=f'{orig_name}_{counter}'
            counter +=1
            
        os.mkdir(name)
        print(f'made directory: {name}')

    elif inp.startswith('cd'):
        parts=inp.split(' ',1)
        if len(parts) < 2 or not parts[1].strip():
            print("use: cd <dir>")
            continue
        target_dir=parts[1].strip()

        try:
            os.chdir(target_dir)
            print(f"changed cd to: {os.getcwd()}")
        except FileNotFoundError:
            print(f"cd: no such file or directory: {target_dir}"+sad)
        except NotADirectoryError:
            print(f"cd: not a directory: {target_dir}"+sad)
        except PermissionError:
            print(f"cd: permission denied: {target_dir}"+sad)

    elif inp.startswith('exec'):
        fn=inp[5:].strip()
        try:
            print('running {filename}...')
            print(gap)
            subprocess.run([sys.executable, fn], check=True)
            print(gap)
        except FileNotFoundError:
            print(f"error: file '{filename}' was not found :(\n")
        except subprocess.CalledProcessError:
            print(f"error: '{filename}' failed during execution :(\n")

    elif inp.startswith('cat '):
        filename = inp[4:].strip()

        if not filename:
            print('error: missing file name use: cat <file>'+sad)
            continue

        try:
            with open(filename, "r", encoding="utf-8") as file:
                print(file.read())
        except FileNotFoundError:
            print(f"error: file '{filename}' not found"+sad)
        except PermissionError:
            print(f"error: perm denied to read '{filename}'"+sad)
        except Exception as e:
            print(f"unexpected error occurred: {e}"+sad)

    elif inp.startswith('vim'):
        parts = inp.path.split(' ', 1) if hasattr(inp, 'path') else inp.split(' ', 1)
        filename = parts[1].strip() if len(parts) > 1 else None
    
        cmd = ['vim', filename] if filename else ['vim']
    
        try:
            subprocess.run(cmd)
        except FileNotFoundError:
            print("'vim' is not installed on this system"+sad)

    elif inp == ":rb":
            print("rebooting")
            if clearwhen_quit == True or 1:
                os.system('clear')
                
            current_script = os.path.abspath(__file__)
            
            try:
                os.chdir(os.path.dirname(current_script))
            except Exception:
                pass
                
            os.execv(sys.executable, [sys.executable, current_script] + sys.argv[1:])

    elif inp.startswith('rm'):
            filepath = inp[3:].strip()
            if not filepath:
                print("use: rm <file_or_dir>")
                continue
                
            if filepath.startswith('_'):
                print(f'file "{filepath}" cannot be removed because its system OR file that user dont want to delete' + sad)
                
            elif os.path.exists(filepath):
                if os.path.isdir(filepath):
    # Create target directory if it doesn't exist
                    shutil.rmtree(filepath)
                    print(f'directory "{filepath}" was removed!')
                else:
                    os.remove(filepath)
                    print(f'file "{filepath}" was removed!')
            else:
                print(f'there is no file or directory called "{filepath}"' + sad)
                
    elif inp.startswith("touch "):
                    name = inp.split(" ")[1]
                    filepath = os.path.join(name)
                    with open(filepath, 'w') as f:
                        f.write("")
                    print(f"file '{filepath}' created.")

    elif inp==('date'):
        from datetime import date
        from datetime import datetime

        print("")
        print(datetime.now())
        print("")
    
    elif inp==('pwd'):
        print(os.getcwd())

    elif inp.startswith('cp'):
        parts = inp.split(' ', 2)
        if len(parts) < 3:
            print("use > cp <source> <destination>")
            continue
    
        src, dest = parts[1], parts[2]
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dest)
                print(f"copied directory '{src}' to '{dest}'")
            else:
                shutil.copy2(src, dest)
                print(f"copied file '{src}' to '{dest}'")
        except Exception as e:
            print(f"cp error: {e}")
    
    elif inp.startswith('pkgs_rel'):
        print('reloading packages...')
        reload_packages()

    elif inp.startswith('make'):
        command_make()
    
    elif inp.startswith('./') or os.path.exists(inp):
        os.system(inp)
    
    elif inp.startswith('pkgs_list'):
        read_packageses()

    else:
        print(empty)
        print(f"unknown command: '{inp}' write help to see commands")
        print(empty)
