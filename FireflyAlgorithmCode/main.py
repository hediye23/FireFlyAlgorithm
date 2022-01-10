from tkinter import *
from PIL import Image

# create main window
from FireflyAlgorithmCode.FireflyProblemCode import FireflyProblemCode

win = Tk()
win.title('Fire Fly Algorithm')
win.geometry("800x800+10+10")

# create labels, text boxes, buttons
fireflies_number_label = Label(win, text='Ateş Böceği Sayısı')
upper_boundary_label = Label(win, text='Üst Sınır')
lower_boundary_label = Label(win, text='Alt sınır')
alpha_label = Label(win, text='Alfa')
beta_label = Label(win, text='Beta')
gamma_label = Label(win, text='Gama')
iteration_number_label = Label(win, text='Yineleme Sayısı')
result_label = Label(win, text='Sonuç')
result = Text(
    width=50,
    height=50,
)

fireflies_number_entry = Entry(bd=3)
upper_boundary_entry = Entry()
lower_boundary_entry = Entry()
alpha_entry = Entry()
beta_entry = Entry()
gamma_entry = Entry()
iteration_number_entry = Entry()

# place widgets
fireflies_number_label.place(x=100, y=50)
fireflies_number_entry.place(x=200, y=50)
upper_boundary_label.place(x=100, y=100)
upper_boundary_entry.place(x=200, y=100)
lower_boundary_label.place(x=100, y=150)
lower_boundary_entry.place(x=200, y=150)
alpha_label.place(x=100, y=200)
alpha_entry.place(x=200, y=200)
beta_label.place(x=100, y=250)
beta_entry.place(x=200, y=250)
gamma_label.place(x=100, y=300)
gamma_entry.place(x=200, y=300)
iteration_number_label.place(x=100, y=350)
iteration_number_entry.place(x=200, y=350)
result_label.place(x=400, y=30)
result.place(x=400, y=50)


def openImage():
    image = Image.open('firefly_rosenbrock.gif')
    image.show()


def openLog(data):
    result.pack(expand=True)
    result.insert('end', data)
    result.place(x=400, y=50)


def run_firefly_algorithm(interval=500):
    out = FireflyProblemCode(int(fireflies_number_entry.get()), win, int(upper_boundary_entry.get()),
                             int(lower_boundary_entry.get()), float(alpha_entry.get()),
                             int(beta_entry.get()), float(gamma_entry.get()), int(iteration_number_entry.get()), interval)
    out.run()
    out.plot()
    openImage()
    openLog(out.result)


runButton = Button(win, text='Başla', command=run_firefly_algorithm)
runButton.place(x=300, y=400)

# start event loop
win.mainloop()
