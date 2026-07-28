import readline
import os
import subprocess
import sys
import curses
import shutil

class TextEditor:
    def __init__(self, filename=None):
        self.filename = filename
        self.lines = [""]
        
        if filename and os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read().splitlines()
                    if content:
                        self.lines = content
            except Exception:
                pass

    def run(self):
        curses.wrapper(self._main_editor)

    def _main_editor(self, stdscr):
        curses.cbreak()
        stdscr.keypad(True)
        
        y, x = 0, 0
        
        while True:
            stdscr.clear()
            max_h, max_w = stdscr.getmaxyx()
            
            for idx, line in enumerate(self.lines):
                if idx < max_h - 2:
                    stdscr.addstr(idx, 0, line[:max_w-1])
            
            status = f" [File: {self.filename or 'New'}] F2: Save | Ctrl+Q: Quit "
            try:
                stdscr.addstr(max_h - 1, 0, status[:max_w-1], curses.A_REVERSE)
            except curses.error:
                pass

            stdscr.move(y, x)
            stdscr.refresh()
            
            key = stdscr.getch()
            
            if key == 17:  
                break
                
            elif key == curses.KEY_F2:
                self._save_file_prompt(stdscr)
                
            elif key == curses.KEY_UP:
                if y > 0:
                    y -= 1
                    x = min(x, len(self.lines[y]))
                    
            elif key == curses.KEY_DOWN:
                if y < len(self.lines) - 1:
                    y += 1
                    x = min(x, len(self.lines[y]))
                    
            elif key == curses.KEY_LEFT:
                if x > 0:
                    x -= 1
                elif y > 0:
                    y -= 1
                    x = len(self.lines[y])
                    
            elif key == curses.KEY_RIGHT:
                if x < len(self.lines[y]):
                    x += 1
                elif y < len(self.lines) - 1:
                    y += 1
                    x = 0
                    
            elif key in (10, 13, curses.KEY_ENTER):
                current_line = self.lines[y]
                self.lines[y] = current_line[:x]
                self.lines.insert(y + 1, current_line[x:])
                y += 1
                x = 0
                
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                if x > 0:
                    self.lines[y] = self.lines[y][:x-1] + self.lines[y][x:]
                    x -= 1
                elif y > 0:
                    prev_len = len(self.lines[y-1])
                    self.lines[y-1] += self.lines[y]
                    del self.lines[y]
                    y -= 1
                    x = prev_len
                    
            elif 32 <= key <= 126:
                char = chr(key)
                self.lines[y] = self.lines[y][:x] + char + self.lines[y][x:]
                x += 1

    def _save_file_prompt(self, stdscr):
        max_h, max_w = stdscr.getmaxyx()
        
        if not self.filename:
            try:
                stdscr.addstr(max_h - 2, 0, "Save as filename: ")
                stdscr.refresh()
                
                curses.echo()
                fn = stdscr.getstr(max_h - 2, 18, 50).decode("utf-8").strip()
                curses.noecho()
                
                if fn:
                    self.filename = fn
            except curses.error:
                pass
                
        if self.filename:
            message = ""
            try:
                with open(self.filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(self.lines) + "\n")
                message = f" Saved to {self.filename} "
            except Exception as e:
                message = f" Error saving: {e} "
            
            try:
                stdscr.addstr(max_h - 1, 0, message[:max_w - 1], curses.A_REVERSE)
            except curses.error:
                pass
                
            stdscr.refresh()
            curses.napms(1000)

logo_file = "logo.txt"

sad=' '+':('

with open(logo_file, 'r') as f:
    logo = f.read()

enable_VD=1

if enable_VD==1:
    os.makedirs("virtualdisk", exist_ok=True)
    os.chdir("virtualdisk")
else:
    pass

commands='''--main
help
clear
ls
cd
mkdir
exec(.py)
rm

--work
cat
edit

--system
quit
reboot'''

empty=""

version='0.1'

username="kernel"

enable_clear_run=1
clearwhen_quit=1
logo_when_clear=1
helptitle=1
showver=1

gapf='-'*50
gapf2='|'
gap=gapf+gapf2

if enable_clear_run==1:
    os.system('clear')
else:
    pass


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

while True:
    inp=input(username+"> ")

    if not inp:
        continue
    
    if inp=="ls":
        print(os.listdir())
        
    elif inp=='help':
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
        
    elif inp=="quit":
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
            print(f"cd: no such file or directory: {target_dir}")
        except NotADirectoryError:
            print(f"cd: not a directory: {target_dir}")
        except PermissionError:
            print(f"cd: permission denied: {target_dir}")

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
            print('error: missing file name. Use: cat <file>')
            continue

        try:
            with open(filename, "r", encoding="utf-8") as file:
                print(file.read())
        except FileNotFoundError:
            print(f"error: file '{filename}' not found.")
        except PermissionError:
            print(f"error: perm denied to read '{filename}'.")
        except Exception as e:
            print(f"unexpected error occurred: {e}")

    elif inp.startswith('edit'):
            parts = inp.split(' ', 1)
            filename = parts[1].strip() if len(parts) > 1 else None
            
            editor = TextEditor(filename)
            editor.run()

    elif inp == "reboot":
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
                    shutil.rmtree(filepath)
                    print(f'directory "{filepath}" was removed!')
                else:
                    os.remove(filepath)
                    print(f'file "{filepath}" was removed!')
            else:
                print(f'there is no file or directory called "{filepath}"' + sad)
        
    else:
        print(empty)
        print(f"unknown command: '{inp}' write help to see commands")
        print(empty)
