"""
    Импорт нужных библиотек.
    1. Основной код программы
    2. Настройки
    3. Графика для окна программы
"""
from rsa import RSA
from preference import preference
from tkinter import *

class Form: # Основной класс Формы окна
    def __init__(self) -> None: # Инициалиция окна
        """
            16 - 17: Настройка разрешения программы
            20 - 22: Создание формы окна и инициализации объектов
            24     : Запуск окна
        """
        self.__WIDTH__ = preference.get('resolution')[0]
        self.__HEIGHT__ = preference.get('resolution')[1] 

        self.CreateWindow()
        self.SetResolution()
        self.InitObjects()
        self.StartWindow()

    def InitObjects(self): # Инициализация объектов 
        # Создание окна вывода, кнопок и поля ввода
        self.lbl1 = Label(self.window, text='Output window')
        self.ent1 = Entry(self.window, text='write')
        self.btn1 = Button(self.window, text='decode', command=self.decoded)
        self.btn2 = Button(self.window, text='encode', command=self.encoded)
        self.btn3 = Button(self.window, text='Generate keys', command=self.generate)
        self.text1 = Text(self.window)

        # Расположение объектов в форме окна
        self.lbl1.place(x=10, y=45)
        self.ent1.place(x=10, y=10, width=self.__WIDTH__ - 110, height=25)
        self.btn1.place(x=self.__WIDTH__ - 110, y=10, width=50, height=25)
        self.btn2.place(x=self.__WIDTH__ - 60, y=10, width=50, height=25)
        self.btn3.place(x=10, y=self.__HEIGHT__ - 100, width=100, height=50)
        self.text1.place(x=10, y=65, width=self.__WIDTH__ - 20)

    def CreateWindow(self): # Создание формы окна
        self.window = Tk()
        self.window.title('RSA Program')
    
    def StartWindow(self): # Запуск формы окна
        self.window.mainloop()

    def SetResolution(self, resulution: list = preference.get('resolution')): # Установка разрешения программы
        self.window.geometry(f'{resulution[0]}x{resulution[1]}')

    def Print(self, text: str): # Вывод строки в окно 'output'
        self.text1.insert(END, str(text) + '\n')

    def generate(self): # Генерация ключей шифрования
        self.rsa = RSA()
        self.Print('Keys generated!')
        self.Print(self.rsa.GetData())

    def decoded(self): # Зашифровка данных
        self.Print(f'Decoded: {self.rsa.Decode(self.ent1.get())}')
    
    def encoded(self): # Расшифровка данных
        self.Print(f'Encoded: {self.rsa.Encode(self.ent1.get())}')

def main(): # Функция запуска программы
    form = Form()

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        exit(error)