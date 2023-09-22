import requests

from tkinter import ttk, messagebox, Event
import tkinter as tk
import time

from .widgets import LabelCombobox, LabelEntry
from .consts import AVAILABLE_CURRENCIES
from .api import get_exchange_rates, get_geolocation



class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_window(self):
        self.title('实时国际汇率转换')
        self.geometry('400x250')


    def init_variables(self):
        self.var_rates_dict = dict() # stores all rates based on EUR

        self.var_from = tk.StringVar()
        self.var_to = tk.StringVar()
        self.var_from_amount = tk.DoubleVar()
        self.var_from_amount.set(1.0)
        self.var_to_amount = tk.StringVar()
        self.var_time = tk.StringVar()
        self.var_time.set(time.strftime(r'%Y-%m-%d %H:%M:%S', time.gmtime()))

    def init_widgets(self):
        self.label_combobox_from = LabelCombobox(self,
                                    '从',
                                    self.var_from,
                                    values=AVAILABLE_CURRENCIES)
        self.label_combobox_from.combobox.current(0)
        self.label_combobox_to = LabelCombobox(self,
                                    '到',
                                    self.var_to,
                                    values=AVAILABLE_CURRENCIES)
        self.label_combobox_to.combobox.current(1)
        self.entry_amount = LabelEntry(self,
                                       '金额',
                                       textvariable=self.var_from_amount)
        self.label_to_amount = ttk.Label(self,
                                       text='目标金额',
                                       textvariable=self.var_to_amount)
        self.label_time = ttk.Label(self,
                                    textvariable=self.var_time)
        self.btn_convert = ttk.Button(self, text='转换')


    def layout_widgets(self):
        self.label_combobox_from.grid(row=0, column=0, sticky='we')
        self.label_combobox_to.grid(row=0, column=1, sticky='we')
        self.entry_amount.grid(row=1, column=0, sticky='we')
        self.label_to_amount.grid(row=2, column=0, columnspan=2, sticky='we')
        self.label_time.grid(row=3, column=0, columnspan=2, sticky='we')
        self.btn_convert.grid(row=3, column=1)

        for widget in self.winfo_children():
            widget.grid(padx=5, pady=10)


    def bind_events(self):
        self.label_combobox_from.combobox.bind('<<ComboboxSelected>>', self.handle_convert)
        self.label_combobox_to.combobox.bind('<<ComboboxSelected>>', self.handle_convert)
        self.btn_convert.bind('<ButtonRelease-1>', self.handle_convert)

        self.var_from_amount.trace("w", self.trace_amount)


    def trace_amount(self, *args) -> None:
        print(self.var_from_amount.get())
        self.handle_convert()

    def handle_convert(self, event: tk.Event=None) -> None:
        "handle event, and trace variable modification"
        # print(self.var_rates_dict)
        from_currency = self.var_from.get()
        from_rate = self.var_rates_dict[from_currency]
        to_currency = self.var_to.get()
        to_rate = self.var_rates_dict[to_currency]
        from_amount = self.var_from_amount.get()
        exchange_ratio = to_rate / from_rate
        to_amount = from_amount * exchange_ratio

        label_str = f"{round(from_amount, 5)} {from_currency} = {round(to_amount, 5)} {to_currency}\n比例 = 1 : {round(exchange_ratio, 5)}"
        self.var_to_amount.set(label_str)


    def update_time(self):
        time_str = time.strftime(r"当地时间: %Y-%m-%d %H:%M:%S", time.gmtime())
        self.var_time.set(time_str)
        self.after(1000, self.update_time)


    def update_exchange_rates(self):
        self.var_rates_dict = get_exchange_rates()
        from_currency = self.var_from.get()
        to_currency = self.var_to.get()
        print(from_currency, to_currency)
        self.after(100_000, self.update_exchange_rates)


    def run(self):
        self.init_window()
        self.init_variables()
        self.init_widgets()
        self.layout_widgets()
        self.bind_events()

        # loops
        self.update_time()

        # try using api
        try:
            self.update_exchange_rates()
        except requests.exceptions.HTTPError as error:
            print(error)
            messagebox.showerror('网络错误', '无法连接至API。')            
        
        self.handle_convert()

        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()