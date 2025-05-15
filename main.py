import curses
import subprocess
import re

def list_installed_programs():
    try:
        result = subprocess.run(["dpkg", "--get-selections"], capture_output=True, text=True)
        programs = result.stdout.split("\n")
        
        # 定義過濾條件，排除核心組件
        exclude_patterns = [
            r"^lib",          # 所有以 lib 開頭的函式庫
            r"^linux-",       # Linux 核心相關
            r"^systemd",      # systemd 相關
            r"^python[0-9.-]*", # Python 內建版本
            r"^gcc",          # GCC 編譯器
            r"^perl",         # Perl 相關
            r"^binutils",     # 開發工具
            r"^dpkg",         # dpkg 本身
            r"^tzdata"        # 時區資料
        ]
        
        filtered_programs = []
        for p in programs:
            pkg = p.split("\t")[0]
            if pkg and not any(re.match(pattern, pkg) for pattern in exclude_patterns):
                filtered_programs.append(pkg)
        
        return ["已安裝的程式:"] + filtered_programs
    except Exception as e:
        return ["錯誤: " + str(e)]

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    menu = list_installed_programs()
    selected = 0
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        for idx, item in enumerate(menu[:h-2]):  # 限制顯示範圍
            x = 5
            y = 2 + idx
            if idx == selected:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, item)
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(menu) - 1:
            selected += 1
        elif key == ord('\n'):
            break
    
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
