from tkinter import *
from tkinter import messagebox
import clipboard
import googletrans

from pynput.keyboard import Listener
import time


PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
BG_COLOR = "#5E595F"
FONT_NAME = "Courier"
CHECK_MARK = "✅"
ALL_LANGUAGE = list(googletrans.LANGUAGES.keys())
OPTIONS_MAIN = list(googletrans.LANGUAGES.values())
OPTIONS = [x.title()+"  " for x in OPTIONS_MAIN]


def user_input_manage():
    if checked_state.get() == 0:
        input_user = user_test_input.get()
        input_language = option_menu.get().lower().strip()
        translation(input_user, input_language)
    else:
        text_area.delete('1.0', "end")
        user_test_input.delete(0, 'end')
        messagebox.showerror("Error", "Click 'Ctrl + C' to Translate")
    return None


def translation(text_, language):
    if language != "select language":
        translate = googletrans.Translator()
        user_text = text_
        user_language = ALL_LANGUAGE[OPTIONS_MAIN.index(language)]
        output = translate.translate(user_text, dest=user_language)
        output = output.text
        if checked_state.get() == 0:
            text_area.delete('1.0', "end")
            text_area.insert('end', output)
            return None
        else:
            return f"{language.title()} Translation", output
    else:
        messagebox.showerror("Error", "Select the language")


def automatic_translate():
    text = clipboard.paste()
    input_language = option_menu.get().lower().strip()
    a, b = translation(text, input_language)
    create_pop_up(a, b)
    return None


def on_press(key):
    key_passed = str(key)
    value = "'\\x03'"  # return value when click Ctrl + C
    if key_passed == value and checked_state.get() == 1:
        time.sleep(0.1)
        automatic_translate()
    return None


def create_pop_up(text_print, language_print):
    top = Toplevel(window, bg="gray")
    top.geometry("350x100")
    top.lift()
    top.attributes('-topmost', True)
    top.title(text_print)
    top.after_idle(top.attributes, '-topmost', False)
    top.resizable(False, False)
    a = Text(top, width=45, height=5, font=("Helvetica", 10, "bold"))
    a.pack()
    a.insert('end', language_print)
    return None


# -----------------------------------------------------------------------------------------------------


window = Tk()
window.config(padx=100, pady=50)
window.geometry("480x200")
window.title("Auto_Translate")
window.resizable(False, False)

user_test_input = Entry(width=40, font=("Helvetica", 15))
user_test_input.place(x=-80, y=-30)

trans_button = Button(text="    Translate    ", font=("Helvetica", 10, "bold"), command=user_input_manage)
trans_button.place(x=-80, y=16)

variable = StringVar(window)
variable.set(OPTIONS[0])

option_menu = StringVar(window)
drop_list = OptionMenu(window, option_menu, *OPTIONS)
drop_list.config(font=("Helvetica", 10, "bold"))
drop_list.place(x=-83, y=60)
option_menu.set("Select Language")

text_area = Text(window, width=31, height=7)
text_area.place(x=110, y=20)

checked_state = IntVar()
checkbutton = Checkbutton(text="Auto-Translation", variable=checked_state,
                          font=("Helvetica", 10, "bold"))
checked_state.get()
checkbutton.place(x=-83, y=110)

listener = Listener(on_press=on_press)
listener.start()

window.mainloop()
