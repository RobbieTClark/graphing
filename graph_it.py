from __future__ import annotations
from typing import List, Dict
from abc import ABC
import pandas as pd
import numpy as np
from tkinter import (
    Tk, Frame, Listbox, Scrollbar, Label, 
    Toplevel, Button, filedialog, Radiobutton,
    IntVar
)
from tkinter.constants import N, EW, DISABLED, NORMAL, END
from os import listdir, getcwd
from os.path import isfile, join
from threading import Thread
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

fonts = {
    "btn_text": ("Calibri", 12, "bold"),
    "list_text": ("Calibri", 10),
}

class Window(ABC):
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
    rbtn_map = {1: 'red', 2: 'green', 3: 'blue'} # Value: Color
    vars: List[str] # Variable names
    selected_indexes: List[int] = []
    
    def __init__(self, root: Tk) -> None:
        super().__init__(root)
        self.root.title('Variables')
        self.axis_var = IntVar()
        self.axis_var.set(1)
        # Widgets
        # x axis button --------------
        x_rbtn = Radiobutton(
            self.root,
            text = 'x',
            font = fonts['btn_text'],
            fg = self.rbtn_map[1],
            value = 1,
            variable = self.axis_var
        )
        x_rbtn.grid(
            row = 0,
            column = 0,
        )
        # ----------------------------
        # y axis button --------------
        y_rbtn = Radiobutton(
            self.root,
            text = 'y',
            font = fonts['btn_text'],
            fg = self.rbtn_map[2],
            value = 2,
            variable = self.axis_var
        )
        y_rbtn.grid(
            row = 0,
            column = 1,
        )
        # -----------------------------
        # z axis button ---------------
        z_rbtn = Radiobutton(
            self.root,
            text = 'z',
            font = fonts['btn_text'],
            fg = self.rbtn_map[3],
            value = 3,
            variable = self.axis_var
        )
        z_rbtn.grid(
            row = 0,
            column = 2,
        )
        #------------------------------

        # Variable list ----------------
        self.vars_list = Listbox(
            self.root,
            width = 20,
            font = fonts['list_text'],
            selectmode = 'multiple',
            exportselection = False,
            activestyle = 'none',
        )
        self.vars_list.bind("<<ListboxSelect>>", self.var_selection)
        self.vars_list.grid(
            row = 1,
            column = 0,
            columnspan = 3,
            padx = 4,
            pady = (4, 4)
        )
        # ------------------------------
    def var_selection(self, event) -> None:
        for i in self.vars_list.curselection():
            self.vars_list.select_clear(i)
            if i not in self.selected_indexes:
                self.vars_list.itemconfig(i, {'bg': self.rbtn_map[self.axis_var.get()]})
                self.selected_indexes.append(i)
            else:
                self.vars_list.itemconfig(i, {'bg': 'white'})
                self.selected_indexes.remove(i)

    def update(self, variables: List[str]) -> None:
        self.vars_list.delete(0, END)
        self.selected_indexes = []
        for var in variables:
            self.vars_list.insert(END, var)
        self.vars = variables

class Help_Win(Window):
    def __init__(self, root: Tk) -> None:
        super().__init__(root)
        self.root.title('Help')

class Main_App:
    directory: str = ''
    data: pd.DataFrame
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
            font = fonts['list_text'],
            exportselection = False
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
        self.directory = filedialog.askdirectory() + '/'
        self.get_files()
    
    def file_selection(self, event) -> None:
        filename = self.files.get(self.files.curselection()[0])
        file_path = self.directory + filename
        Thread(target = self.get_variable_names, args = (file_path,) ,daemon = True).start()
    
    def get_variable_names(self, file_path: str) -> None:
        if file_path[-3:] == 'csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        # Store the data in a numpy array, more computationally efficient
        self.data = df.to_numpy()
        self.vars_win.update(df.columns)

    def start_graphing(self) -> None:
        pass
    
    def get_files(self) -> None:
        self.files.delete(0, END)
        for file in listdir(self.directory):
            if isfile(join(self.directory, file)) and (file[-3:] == 'csv' or file[-3:] == 'xls' or file[-4:] == 'xlsx'):
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