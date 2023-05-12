from __future__ import annotations
from typing import List, Dict
import pandas as pd


from tkinter import (
    Tk, Frame, Listbox, Scrollbar, Label, 
    Toplevel, Button, filedialog
)
from tkinter.constants import N, EW, DISABLED, NORMAL, END
from os import listdir, getcwd
from os.path import isfile, join

fonts = {
    "btn_text": ("Calibri", 12, "bold"),
    "list_text": ("Calibri", 10),
}


class Window:
    def __init__(self, root: Tk) -> None:
        
        # Window UI is a child of the UI using master root
        self.root = Toplevel(root)
        self.root.withdraw()
        self.root.protocol("WM_DELETE_WINDOW", self.root.withdraw)

    def show(self) -> None:
        if self.root.state() == "withdrawn":
            self.root.deiconify()
        else:
            self.root.withdraw()
    
    def quit(self) -> None:
        self.root.quit()
        self.root.destroy()

class Variables_Win(Window):
    def __init__(self, root: Tk):
        super().__init__(root)
        self.root.title('Variables')
    


class Help_Win(Window):
    def __init__(self, root: Tk):
        super().__init__(root)
        self.root.title('Help')

class Main_App:
    file_directory: str = ''
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.quit_ui)
        self.root.title('Graphing App')
        # Child windows
        self.vars_win = Variables_Win(self.root)
        self.help_win = Help_Win(self.root)
        
        # WIDGETS
        # Update files button --------------
        self.update_files_btn = Button(
            self.root,
            command = self.get_files,
            text = 'Update Files',
            font = fonts["btn_text"]
        )
        self.update_files_btn.grid(
            row = 0,
            column = 0,
            sticky = [N, EW],
            padx = (4, 2),
            pady = (4, 0)
        )
        # ----------------------------------
        # Help button ----------------------
        self.help_btn = Button(
            self.root,
            text = "Help",
            font = fonts["btn_text"],
            command = self.help_win.show
        )
        self.help_btn.grid(
            column = 1,
            row = 0,
            sticky = [N, EW],
            padx = (2, 4),
            pady = (4, 0)
        )
        # ----------------------------------
        # Set directory button
        self.set_dir_btn = Button(
            self.root,
            command = self.set_directory,
            text = "Set Directory",
            font = fonts["btn_text"]
        )
        self.set_dir_btn.grid(
            row = 1,
            column = 0,
            sticky = [N, EW],
            padx = 4,
            pady = (4, 0),
            columnspan = 2
        )
        # ----------------------------------
        # Files list -----------------------
        self.files = Listbox(
            self.root,
            width = 30,
            font = fonts['list_text']
        )
        self.files.bind("<<ListboxSelect>>", self.file_selection)
        self.files.grid(
            column = 0,
            row = 2,
            sticky = [N, EW],
            padx = 4,
            pady = (4, 0),
            columnspan = 2,
        )
        # ----------------------------------
        # Variables button -----------------
        self.vars_btn = Button(
            self.root,
            text = "Variables",
            font = fonts["btn_text"],
            command = self.vars_win.show
        )
        self.vars_btn.grid(
            column = 0,
            row = 3,
            sticky = [N, EW],
            padx = 4,
            pady = (3, 0),
            columnspan = 2,
        )
        #-----------------------------------
        # Graph button ---------------------
        self.graph_btn = Button(
            self.root,
            text = "Graph",
            font = fonts["btn_text"],
            command = self.start_graphing
        )
        self.graph_btn.grid(
            column = 0,
            row = 4,
            columnspan = 2,
            sticky = [N, EW],
            padx = 4,
            pady = (4, 4),
        )
        # ----------------------------------
 
    def set_directory(self) -> None:
        self.file_directory = filedialog.askdirectory() + '/'
        self.get_files()
    def file_selection(self) -> None:
        pass
    def start_graphing(self) -> None:
        pass
    def get_files(self):
        self.files.delete(0, END)
        for file in listdir(self.file_directory):
            if isfile(join(self.file_directory, file)) and (file[-3:] == 'csv' or file[-4:] == 'xlsx'):
                self.files.insert(END, file)
        

    def quit_ui(self) -> None:
        self.vars_win.quit()
        self.help_win.quit()
        self.root.quit()
        self.root.destroy()



if __name__ == '__main__':
    root = Tk()
    Main_App(root)
    root.mainloop()