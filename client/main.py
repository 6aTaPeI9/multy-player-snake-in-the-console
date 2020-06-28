import curses

if __name__ == '__main__':
    curses.initscr() # Инициализируем модуль curses в терминале
    win = curses.newwin(25, 100, 0, 0)
    win.keypad(True)
    curses.noecho() # Убираем вывод нажатых клавишь на экран
    curses.curs_set(False) # Убираем подсветку текущей позиции курсора
    # win.border(0)
    # win.nodelay(1)
    win.before
    while True:
        win.addstr(15, 15, str(win.getmaxyx()))
        win.getch()
    # curses.endwin()