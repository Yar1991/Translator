import tkinter
import customtkinter as ctkinter
import googletrans
from googletrans import Translator
from PIL import Image


class App(ctkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Translator")
        self.geometry("1000x400")
        self.resizable(False, False)
        self.translator = Translator()
        self.languages = [language for language in googletrans.LANGUAGES.values()]
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 3), weight=1)
        
        self.input_one = InputFrame(self, detect=True, languages=self.languages)
        self.input_one.grid(row=0, column=0, padx=(20, 0), pady=20)
        
        self.control_btns = Btns(self, click_handler=self.translate, switch_handler=self.switch_langs)
        self.control_btns.grid(row=0, column=1)

        self.input_two = InputFrame(self, detect=False, languages=self.languages)
        self.input_two.grid(row=0, column=2, padx=(0, 20), pady=20)
        
    
    def translate(self):
        lang_one = self.input_one.choice_box.get()
        lang_two = self.input_two.choice_box.get()
        source_text = self.input_one.input_box.get("0.0", "end")

        if len(source_text) == 1:
            return
        else:
            if lang_one == "auto-detect":
                detect_lang = self.translator.detect(source_text)
                lang_one = googletrans.LANGUAGES[detect_lang.lang]
                self.input_one.choice_box.set(lang_one)
            
            translated = self.translator.translate(source_text, lang_two, lang_one)
            self.input_two.input_box.delete("0.0", "end")
            self.input_two.input_box.insert("0.0", translated.text)
        
        
    def switch_langs(self):
        lang_one = self.input_one.choice_box.get()
        lang_two = self.input_two.choice_box.get()
        source_text = self.input_two.input_box.get("0.0", "end")
        
        if lang_one == "auto-detect" or len(source_text) == 1:
            return
        else:      
            self.input_one.choice_box.set(lang_two)
            self.input_two.choice_box.set(lang_one)
            translated = self.translator.translate(source_text, lang_one, lang_two)
            self.input_one.input_box.delete("0.0", "end")
            self.input_one.input_box.insert("0.0", source_text)
            self.input_two.input_box.delete("0.0", "end")
            self.input_two.input_box.insert("0.0", translated.text)
        
            

class InputFrame(ctkinter.CTkFrame):
    def __init__(self, *args, detect=False, languages=[], **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.configure(fg_color="transparent")
        self.detect = detect
        self.languages = languages
        
        self.choice_variable = tkinter.StringVar(self, value="auto-detect" if self.detect else "english")
        self.choice_box = ctkinter.CTkOptionMenu(self, font=("Verdana", 16),
            values=["auto-detect", *self.languages] if self.detect else self.languages,
            variable=self.choice_variable, fg_color="#111111", dropdown_font=("Verdana", 15))
        self.choice_box.grid(row=0, column=0, sticky="ew")
        
        self.input_box = ctkinter.CTkTextbox(self, corner_radius=10, width=400, height=300, font=("Verdana", 16))
        self.input_box.grid(row=1, column=0, sticky="nsew")
        
        
class Btns(ctkinter.CTkFrame):
    def __init__(self, *args, click_handler=None, switch_handler=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.configure(fg_color="transparent")

        self.switch_img = ctkinter.CTkImage(light_image=Image.open("assets/switch.png"), dark_image=Image.open("assets/switch.png"), size=(50, 30))
        self.switch_btn = ctkinter.CTkButton(self, text="", corner_radius=10, image=self.switch_img, fg_color="#111111",
        width=80, height=40, cursor="hand2", hover_color="#181818",command=switch_handler)
        self.switch_btn.grid(row=0, column=0, padx=20)
        
        self.translate_btn = ctkinter.CTkButton(self, width=100, height=40, text="Translate", corner_radius=10, font=("Verdana", 16, "bold"), cursor="hand2", command=click_handler)
        self.translate_btn.grid(row=1, column=0, padx=20, pady=(30, 0))
        

if __name__ == "__main__":
    ctkinter.set_appearance_mode("dark")
    app = App()
    app.iconbitmap("assets/icon.ico")
    app.mainloop()

