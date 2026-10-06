from pynbs import *
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename
instrument_map = {
    0: "harp",
    1: "bass",
    2: "basedrum",
    3: "snare",
    4: "hat",
    5: "bell",
    6: "guitar",
    7: "chime",
    8: "xylophone",
    9: "iron_xylophone",
    10: "cow_bell",
    11: "didgeridoo",
    12: "bit",
    13: "banjo",
    14: "pling"
}



class Window(Tk):
    def __init__(self):
        super().__init__()
        # root
        self.geometry(f"500x400")
        self.title("Minecraft NBS Music Converter")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.finish)
        self.attributes("-fullscreen", False)
        self.attributes("-alpha", 1.0)
        self.attributes("-toolwindow", False)
        #####

        self.main_label = Label(text="Minecraft NBS Music Converter", font=("Arial", 12))
        self.main_label.place(anchor=NW, relx=0, rely=0)

        self.label_converted_file_name = Label(text="Имя конвертированного файла:", font=("Arial", 10))
        self.label_converted_file_name.place(relx=0, rely=0.1)
        self.entry_converted_file_name = Entry()
        self.entry_converted_file_name.place(relx=0, rely=0.15)
        self.entry_converted_file_name.insert(0, "Test Name")

        self.btn_create_particle = ttk.Button(text="Выбрать файл и конвертировать", command=self.choose_file)
        self.btn_create_particle.place(relx=0.8, rely=0.8)

        ###
        self.mainloop()

    def finish(self):
        self.destroy()


    def convert_nbs_to_mcfunction(self, nbs_file_path, converted_file_name):
        name = converted_file_name
        song = read(nbs_file_path)
        base_note = 45
        header = song.header
        #header.tempo
        text = ''
        for tick, chord in song:
            for note in chord:
                # Конвертация pitch
                pitch = 2 ** ((note.key - base_note) / 12)
                # Ограничение диапазона (0.01 ≤ pitch ≤ 2.0)
                pitch = max(0.01, min(pitch, 2.0))
                pitch = round(pitch, 5)
                volume = note.velocity / 100
                volume *= 2
                # Определение инструмента (пример для пианино)
                sound = instrument_map[note.instrument]
                # Генерация команды
                text += f"execute if score @s mp.tick matches {tick} run playsound minecraft:block.note_block.{sound} record @a ~ ~ ~ {volume} {pitch}\n"

        create_file(text, name)


    def choose_file(self):
        new_name = self.entry_converted_file_name.get()
        filetypes = (("Note Block Studio", "*.nbs"),)
        filename = askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetypes)
        if filename:
            print(filename)
            self.convert_nbs_to_mcfunction(filename, new_name)

def create_file(text, name):
    file = open(f"{name}.mcfunction", "w")
    file.write(text)
    file.close()


Main_Window = Window()
