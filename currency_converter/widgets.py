from tkinter import ttk


class LabelCombobox(ttk.Frame):
    def __init__(self, 
                 master, 
                 label_text, 
                 textvariable,
                 *args,
                 **kwargs):
        super().__init__(master)

        self.label = ttk.Label(self, text=label_text)
        self.combobox = ttk.Combobox(self,
                                     textvariable=textvariable,
                                     state='readonly',
                                     *args,
                                     **kwargs)

        self.label.grid(row=0, column=0, sticky='w')
        self.combobox.grid(row=1, column=0, sticky='we')


class LabelEntry(ttk.Frame):
    def __init__(self, 
                 master, 
                 label_text, 
                 textvariable,
                 *args,
                 **kwargs):
        super().__init__(master)

        self.label = ttk.Label(self, text=label_text)
        self.entry = ttk.Entry(self,
                               textvariable=textvariable,
                               *args,
                               **kwargs)

        self.label.grid(row=0, column=0, sticky='w')
        self.entry.grid(row=1, column=0, sticky='we')
