from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry
import cv2 as cv
import imutils

primary_color = "#EEE1EE"
frame_color = "#FBE1FB"
success_color = "#0FC700"

root = Tk()
root.title("Phần mềm điểm danh")
root.geometry("800x500+250+50") 
video = Label(root)
menuBar = Menu(root)

lblHoten = Label(root, text="Chưa có dữ liệu", relief=RAISED, bg=primary_color,  border=0, font=("Arial", 20))
lblMssv = Label(root, text="a", relief=RAISED, bg=primary_color,  border=0, font=("Arial", 20))


_frame = Frame(root, bg=frame_color, width=400, height=500)
frameLogin = Frame(root, bg="#06173D", width=500, height=300)
label = Label(frameLogin, text="ĐĂNG NHẬP", 
              relief=RAISED, 
              font=("Arial", 24), 
              wraplength=500, 
              border=0)
label.place(relx=0.5, rely=0.05, anchor="n")
frameLogin.place(relx=0.5, rely=0.05, anchor="n")
_frame.configure(bg=frame_color)
lblThongTinSV = Label(_frame, text="THÔNG TIN SINH VIÊN", font=("Arial", 20), justify="center", border=0)

img_search = PhotoImage(file='icons/search.png')

root.configure(bg=primary_color)

def goToHome():
    Loginform()
    root.configure(bg=primary_color)
    showFrameCam(0)
    
    label.place(relx=0.5, rely=0.05, anchor="n")
    frameLogin.place(relx=0.5, rely=0.05, anchor="n")
    
    _frame.place_forget()
    lblHoten.place_forget()
    lblMssv.place_forget()
    
    
def goToCheckData():
    label.place_forget()
    frameLogin.place_forget()
    lblHoten.place(relx=.25, rely=.7, anchor="c")
    lblMssv.place(relx=.25, rely=.8, anchor="c")
    _frame.place(relx=.5, rely=0)
    lblThongTinSV.place(relx=.5, rely=.05, anchor="c")

    lblMasoSV = Label(_frame, text = "MSSV:", font=("Arial", 16))
    edtMSSV = Entry(_frame, font=("Arial", 16))
    btnSearch = Button(_frame, image=img_search,command= myClick, borderwidth=0)
    
    lblHovaTen = Label(_frame, text = "Họ và tên:", font=("Arial", 16))
    edtTen = Entry(_frame, font=("Arial", 16))
    
    lblNgaySinh = Label(_frame, text = "Ngày sinh:", font=("Arial", 16))
    pkNgaySinh = DateEntry(_frame, width= 16, background= "magenta3", foreground= "white", 
                           bd=2, date_pattern='mm/dd/yyyy')
    
    lblSoDienThoai = Label(_frame, text = "Điện thoại:", font=("Arial", 16))
    edtSoDienThoai = Entry(_frame, font=("Arial", 16))
    
    lblEmai = Label(_frame, text = "Email:", font=("Arial", 16))
    edtEmail = Entry(_frame, font=("Arial", 16))
    
    lblMasoSV.place(relx=.05, rely=.2, anchor="w")
    edtMSSV.place(relx=.3, rely=.2, anchor="w")
    btnSearch.place(relx=.97, rely=.2 ,anchor="e")
    
    lblHovaTen.place(relx=.05, rely=.28, anchor="w")
    edtTen.place(relx=.3, rely=.28, anchor="w")
    
    lblNgaySinh.place(relx=.05, rely=.36, anchor="w")
    pkNgaySinh.place(relx=.3, rely=.36, anchor="w")
    
    lblSoDienThoai.place(relx=.05, rely=.44, anchor="w")
    edtSoDienThoai.place(relx=.3, rely=.44, anchor="w")
    
    lblEmai.place(relx=.05, rely=.52, anchor="w")
    edtEmail.place(relx=.3, rely=.52, anchor="w")
    
    
    
    button=Button(_frame, text="Thêm Mới", command=myClick, 
                  font=("Arial", 16), bg=success_color, 
                  justify="center", border=0)
    button.place(relx=.5, rely=1, anchor="c")
    
    root.configure(bg=primary_color)
    showFrameCam(1)
    
    
def goToQuanTri():
    root.configure(bg=primary_color)
    showFrameCam(0)
    label.place_forget()
    frameLogin.place_forget()
    _frame.place_forget()
    lblHoten.place_forget()
    lblMssv.place_forget()
    
face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

def showFrameCam(status):
    global cap
    if(status == 0):
        print("Status = 0")
        if cap is None or not cap.isOpened():
            print("Hong co gi")
        else:
            video.place_forget()
            cap.release()
    else :
        
        cap = cv.VideoCapture(0)
        video.place(relx=0, rely=0)
        
    while(status == 1):
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=400)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video.config(image=imgtk)
        root.update() 
def Loginform():
    print("---login---")
    frameLogin.place(relx=.5, rely=.5, anchor=CENTER)
    
def myClick():
    print("click")

menuBar.add_command(label="Trang chủ", command=goToHome)
menuBar.add_command(label="Kiểm tra", command=goToCheckData)
menuBar.add_command(label="Quản trị", command=goToQuanTri)

root.config(menu=menuBar)
root.mainloop()