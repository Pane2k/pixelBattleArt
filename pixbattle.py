from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.offset_x = 0
        self.offset_y = 0
        self.image = None
        self.zoomed_image = None
        self.zoom_factor = 6

        # Создание интерфейса
        self.create_interface()

    def create_interface(self):
        # Создание главного меню
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        self.root.geometry("756x756")
        # Создание меню "Файл"
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Открыть", command=self.open_image)
        menubar.add_cascade(label="Файл", menu=filemenu)

        # Создание поля для ввода смещения
        offset_frame = Frame(self.root)
        offset_frame.pack(side=TOP)
        offset_label = Label(offset_frame, text="Смещение:")
        offset_label.pack(side=LEFT)
        self.offset_x_entry = Entry(offset_frame, width=5)
        self.offset_x_entry.pack(side=LEFT)
        self.offset_x_entry.insert(END, "1464")
        offset_label_x = Label(offset_frame, text="X:")
        offset_label_x.pack(side=LEFT)
        self.offset_y_entry = Entry(offset_frame, width=5)
        self.offset_y_entry.pack(side=LEFT)
        self.offset_y_entry.insert(END, "274")
        offset_label_y = Label(offset_frame, text="Y:")
        offset_label_y.pack(side=LEFT)

        # Создание кнопки "Увеличить"
        

        # Создание канвы для отображения изображения
        self.canvas = Canvas(self.root, width=756, height=756)
        self.canvas.pack(side=TOP)

        # Создание обработчика событий для канвы
        self.canvas.bind("<Motion>", self.show_coordinates)

    def open_image(self):
        # Открытие диалогового окна для выбора файла
        file_path = filedialog.askopenfilename()

        if file_path:
            # Загрузка изображения и отображение его на канве
            self.image = Image.open(file_path)
            self.zoomed_image = self.image.resize((756, 756), Image.NEAREST)
            self.show_image()

    def show_image(self):
         # Resize the image to fit the canvas
        self.zoomed_image = self.image.resize((756, 756), Image.NEAREST)

        # Create a PhotoImage object for the resized image
        self.photo_image = ImageTk.PhotoImage(self.zoomed_image)

        # Clear the canvas
        self.canvas.delete("all")

        # Draw the image on the canvas
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)

        # Draw the grid on the canvas
        for x in range(0, 756, self.zoom_factor):
            self.canvas.create_line(x, 0, x, 756, fill="black")

        for y in range(0, 756, self.zoom_factor):
            self.canvas.create_line(0, y, 756, y, fill="black")

   

    def show_coordinates(self, event):
        # Отображение координат пикселя
        x, y = event.x, event.y

        if self.zoomed_image and x >= 0 and x < self.zoomed_image.width and y >= 0 and y < self.zoomed_image.height:
            orig_x = int(x / self.zoom_factor)
            orig_y = int(y / self.zoom_factor)
            pixel = self.zoomed_image.getpixel((x, y))
            self.root.title("Координаты: ({}, {}) Цвет: {}".format(orig_x + int(self.offset_x_entry.get()), orig_y + int(self.offset_y_entry.get()), pixel))


root = Tk()
root.title("Изображение")

image_processor = ImageProcessor(root)

root.mainloop()
