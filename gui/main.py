
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
import hashlib
import dataprovider as dp
from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

imagePath = "/icons/check.png"

class LoginScreen(QtWidgets.QMainWindow):
     def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("gui/login.ui",self)
        self.btnDangNhap.clicked.connect(self.action_dangnhap)
        
     def action_dangnhap(self):
        print("Nhan dang nhap")
        tdn = self.edtTenDangNhap.text()
        mk = self.edtMatKhau.text()
        if(str(tdn) == "" or str(mk) == ""):
            return
        sha = hashlib.sha256()
        sha.update(str(mk).encode())
        strg = sha.hexdigest()
        if(dp.login(tdn, strg) == 0):
            print("Dang nhap giang vien")
            
        elif(dp.login(tdn, strg) == 1):
            print("Dang nhap quan tri")
            quantri = QuanTriScreen()
            widget.addWidget(quantri)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            return
 
class ImgWidget(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(ImgWidget, self).__init__(parent)
        pic = QtGui.QPixmap(imagePath)
        self.setPixmap(pic)

class QuanTriScreen(QtWidgets.QMainWindow):
     iTrangThai = 1
     iLoaiTK = 0
     def __init__(self):
        super(QuanTriScreen, self).__init__()
        loadUi("gui/quantri.ui",self)
        self.stackedWidget.setCurrentWidget(self.trangchu)
        self.lblTime.setText(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        
        self.btnTrangChu.clicked.connect(lambda: showQTTrangChu())
        self.btnSinhVien.clicked.connect(lambda: showQTSinhVien())
        self.btnLop.clicked.connect(lambda: showQTLop())
        self.btnNganh.clicked.connect(lambda: showQTNganh())
        self.btnHocPhan.clicked.connect(lambda: showQTHocPhan())
        self.btnGiangVien.clicked.connect(lambda: showQTGiangVien())
        
        self.btnLogout.clicked.connect(lambda: logout())
        
        def logout():
            login = LoginScreen()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
        
        def showQTTrangChu():
            print("Trangchu")   
            self.stackedWidget.setCurrentWidget(self.trangchu)
            #code ở đây
            
        def showQTSinhVien():
            print("Sinhvien")  
            self.stackedWidget.setCurrentWidget(self.sinhvien) 
            
        def showQTLop():
            print("Lop") 
            self.stackedWidget.setCurrentWidget(self.lop)  
            
        def showQTNganh():
            print("Nganh") 
            self.stackedWidget.setCurrentWidget(self.nganh)  
            
        def showQTHocPhan():
            print("Hocphan")  
            self.stackedWidget.setCurrentWidget(self.hocphan)  
            
        def showQTGiangVien():
            print("Giangvien")      
            self.stackedWidget.setCurrentWidget(self.giangvien) 
            cbbTrangThai = self.cbbTrangThai
            cbbTrangThai.addItem("Hoạt động") 
            cbbTrangThai.addItem("Không hoạt động")
            cbbTrangThai.currentIndexChanged.connect(self.changeTrangThai)
            
            cbbLoaiTaiKhoan = self.cbbLoaiTK
            cbbLoaiTaiKhoan.addItem("Giảng viên")
            cbbLoaiTaiKhoan.addItem("Quản trị")
            cbbLoaiTaiKhoan.currentIndexChanged.connect(self.changeLoaiTK)
            
            tukhoa = self.edtSearch.text()
            loadDataGiangVien(self.iTrangThai, self.iLoaiTK, tukhoa)
            
            self.btnTim.clicked.connect(lambda: loadDataGiangVien(self.iTrangThai, self.iLoaiTK, tukhoa))
            
        def loadDataGiangVien(iTrangThai, iLoaiTK, tukhoa):
            print("Lấy dữ liệu nè" + str(iTrangThai) + " - " + str(iLoaiTK))
            #Lấy dữ liệu từ db
            list_gv = dp.getListCanBo(iTrangThai, iLoaiTK, tukhoa)
            row = 0
            header = self.tbGiangVien.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.tbGiangVien.horizontalHeader().setFont(QFont('Arial', weight = QFont.Bold))
            self.tbGiangVien.setRowCount(len(list_gv))
            for gv in list_gv:
                if(str(gv[1]) == ""): continue
                if(iTrangThai==1):
                    strTrangThai = "Đang hoạt động"
                    imagePath = "/icons/check.png"
                else:
                    strTrangThai = "Không hoạt động"
                    imagePath = "/icons/cross.png"
                self.tbGiangVien.setItem(row, 0, QtWidgets.QTableWidgetItem(gv[1]))
                self.tbGiangVien.setItem(row, 1, QtWidgets.QTableWidgetItem(gv[2]))
                self.tbGiangVien.setItem(row, 2, QtWidgets.QTableWidgetItem(gv[3]))
                self.tbGiangVien.setItem(row, 3, QtWidgets.QTableWidgetItem(gv[4]))
                self.tbGiangVien.setItem(row, 4, QtWidgets.QTableWidgetItem(gv[5]))
                self.tbGiangVien.setItem(row, 5, QtWidgets.QTableWidgetItem(gv[6]))
                self.tbGiangVien.setCellWidget(row, 6, ImgWidget(self))
                row += 1
     def changeTrangThai(self, i):
            if(i == 0):
                self.iTrangThai = 1
            else:
                self.iTrangThai = 0
            
     def changeLoaiTK(self, i):
            print(i)
            self.iLoaiTK = i
     
   
   
app = QApplication(sys.argv)
welcome = LoginScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")

