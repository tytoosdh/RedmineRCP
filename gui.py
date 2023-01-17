from tkinter import *

root = Tk()
root.title('Makieta gui Redmine RCP')
root.iconbitmap('redmine_ico.ico')

frame_up = LabelFrame(root, text='Ramka górna', padx=5, pady=5)
frame_down = LabelFrame(root, text='Ramka dolna', padx=5, pady=5)
frame_up.pack(side=TOP)
frame_down.pack(side=BOTTOM)

frame_calendar = LabelFrame(frame_up, text='Kalendarz', padx=5, pady=5)
frame_calendar.pack(side=LEFT)

root.mainloop()
