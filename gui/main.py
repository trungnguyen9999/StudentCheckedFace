
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QHeaderView, QMessageBox
import hashlib
import dataprovider as dp
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2 as cv
import time
import os
import numpy as np
from PIL import Image

tenDN = ""
id = 0
trangthaiTK = ""
face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

recognizer = cv.face.LBPHFaceRecognizer_create()
pathData = "../StudetnCheckedFace/dataset/"
imagePath = "../StudetnCheckedFace/icons/check.png"

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
        setTenDN(tdn)
        if(dp.login(tdn, strg) == 0):
            print("Dang nhap giang vien")
            giangvien = GiangVienScreen()
            widget.addWidget(giangvien)
            widget.setCurrentIndex(widget.currentIndex()+1)
            
        elif(dp.login(tdn, strg) == 1):
            print("Dang nhap quan tri")
            quantri = QuanTriScreen()
            widget.addWidget(quantri)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            return

def setTenDN(tdn):
    global tenDN   
    tenDN = tdn 
def setImagePath(p):   
    global imagePath
    imagePath = p
def setId(_id):   
    global id
    id = _id
def setTrangThaiTK(_tt):   
    global trangthaiTK
    trangthaiTK = _tt
class ImgWidget(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(ImgWidget, self).__init__(parent)
        pic = QtGui.QPixmap(imagePath)
        picmap = pic.scaled(16, 16)
        self.setPixmap(picmap)

class GiangVienScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(GiangVienScreen, self).__init__()
        loadUi("gui/giangvien.ui",self)
        objCanBo = dp.getCanBoByTenDN(str(tenDN))
        print(objCanBo)
        self.edtMSCB.setText(objCanBo[1])
        self.edtHoTen.setText(objCanBo[2])
        self.edtDienThoai.setText(objCanBo[3])
        self.edtEmail.setText(objCanBo[4])
        self.edtDiaChi.setText(objCanBo[5])
        self.btnChinhSuaCB.clicked.connect(lambda: self.chinhSuaCB(objCanBo[0]))
        self.btnCapNhatCB.clicked.connect(lambda: self.capNhatCB(objCanBo[0]))
        
        list_lop = dp.getLopOfCanbo(str(tenDN))
        print(list_lop)
        for lop in list_lop:
            self.listLop.addItem(lop[2] + " - " + lop[1])
        self.listLop.itemSelectionChanged.connect(self.selectionChangedLop)  
        self.listSinhVien.itemSelectionChanged.connect(self.selectionChangedSinhvien) 
        self.gvLogout.clicked.connect(lambda: logout())
        self.btnChinhSuaSV.clicked.connect(lambda: self.chinhSuaSV())
        self.btnCapNhatSV.clicked.connect(lambda: self.capNhatSV())
        self.btnLayKhuonMatSV.clicked.connect(lambda: self.layKhuonMatSV())
        self.btnKiemTraKhuonMat.clicked.connect(lambda: GiangVienScreen.kiemTraKhuonMatSV())
        
    def kiemTraKhuonMatSV():
        print("kiemTraKhuonMatSV")    
        recognizer.read('../StudetnCheckedFace/recognizer/trainingdata.yml')
        cap = cv.VideoCapture(0)
        while (True):
            ret, frame = cap.read()
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for(x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                id, confidence = recognizer.predict(roi_gray)
                if confidence < 40:
                    cv.rectangle(frame, (x, y), (x+w, y+h), (0, 224, 19), 2)
                    profile = dp.getSinhvienById(id)
                    if profile != None:
                        cv.putText(frame, "" + str(profile[1]), (x+10, y+h+30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 224, 19), 2)
                else:
                    cv.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
                    cv.putText(frame, "Unknown", (x+10, y+h+30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            cv.imshow('My Face' ,frame)
            if (cv.waitKey(1) & 0xFF == ord('q')):
                break
        cap.release()
        cv.destroyAllWindows()
    
    def layKhuonMatSV(self):
        print("Lay khuon mat sinh vi??n") 
        cap = cv.VideoCapture(0)
        index = 0
        mssv = self.listSinhVien.currentItem().text().split('-')[0]
        print(mssv)
        sinhvien = dp.getSinhvienByMaso(mssv)
        print(sinhvien)
        while(True):
            ret, frame = cap.read()
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for(x, y, w, h) in faces:
                cv.rectangle(frame, (x, y), (x+w, y+h), (0, 224, 19), 2)
                cv.putText(frame, str(index) + " %", (x+10, y+h+30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 224, 19), 2)
                if not os.path.exists('../StudetnCheckedFace/dataset/' + str(sinhvien[0]) + '.' + str(sinhvien[1])):
                    os.makedirs('dataset/' + str(sinhvien[0]) + '.' + str(sinhvien[1]))
                    
                
                index += 1
                cv.imwrite('../StudetnCheckedFace/dataset/' + str(sinhvien[0]) + '.' + str(sinhvien[1]) + '/student_'+ str(sinhvien[0]) + '.' + str(sinhvien[1]) + '.' + str(index) + '.jpg', gray[y: y+h, x: x+w])
            cv.imshow("Get face", frame)
            if(cv.waitKey(1) & 0xFF == ord('q')):
                break
            
            if(index >= 100):
                break
            time.sleep(0.1)
        cap.release()
        cv.destroyAllWindows()
        self.trainningData()
        
    def getImageWithMssv(pathData):
        sinhVienPaths = [os.path.join(pathData, f) for f in os.listdir(pathData)]
        print(sinhVienPaths)
        faces = []
        ids = []
        for sinhVienPath in sinhVienPaths:
            print(sinhVienPath)
            imagePaths = [os.path.join(sinhVienPath, f) for f in os.listdir(sinhVienPath)]
            
            for imagePath in imagePaths:
                faceImg = Image.open(imagePath).convert('L')
                faceNp = np.array(faceImg, 'uint8')
                
                faces.append(faceNp)
                ids.append(int(sinhVienPath.split("/")[3].split(".")[0]))
                cv.imshow('Training...', faceNp)
                cv.waitKey(10)
        return faces, ids
     
    def trainningData(self):
        print("Trainning...")
        _faces, _ids = GiangVienScreen.getImageWithMssv(pathData)
        recognizer.train(_faces, np.array(_ids))

        if not os.path.exists('../StudetnCheckedFace/recognizer'):
            os.makedirs('../StudetnCheckedFace/recognizer')
    
        recognizer.save('../StudetnCheckedFace/recognizer/trainingdata.yml')
        
    def chinhSuaCB(self, id):
        print("Chinh sua CB")
        if self.btnChinhSuaCB.text() == 'H???y b???':
            self.btnChinhSuaCB.setText("Ch???nh s???a")
            self.btnCapNhatCB.setEnabled(False)
            self.edtHoTen.setEnabled(False)
            self.edtDienThoai.setEnabled(False)
            self.edtEmail.setEnabled(False)
            self.edtDiaChi.setEnabled(False)
        else:            
            self.btnChinhSuaCB.setText("H???y b???")
            self.btnCapNhatCB.setEnabled(True)
            self.edtHoTen.setEnabled(True)
            self.edtDienThoai.setEnabled(True)
            self.edtEmail.setEnabled(True)
            self.edtDiaChi.setEnabled(True)
     
    def capNhatCB(self, id):
        print("Cap nhat CB")   
        _hoten = self.edtHoTen.text()
        _dienthoai = self.edtDienThoai.text()
        _email = self.edtEmail.text()
        _diachi = self.edtDiaChi.toPlainText()
        dp.capNhatCanBo(id, _hoten, _dienthoai, _email, _diachi)
        setId(0)
        self.btnCapNhatCB.setEnabled(False)
        self.edtHoTen.setEnabled(False)
        self.edtDienThoai.setEnabled(False)
        self.edtEmail.setEnabled(False)
        self.edtDiaChi.setEnabled(False)
        self.btnChinhSuaCB.setText("Ch???nh s???a")
        
    def chinhSuaSV(self):
        print("Chinh sua sinh vi??n") 
        
        if self.btnChinhSuaSV.text() == 'H???y b???':
            print("nhan huy bo")
            self.btnChinhSuaSV.setText("Ch???nh s???a")
            self.btnCapNhatSV.setEnabled(False)
            self.edtMSSV.setEnabled(False)
            self.edtHoTenSV.setEnabled(False)
            self.edtNgaySinhSV.setEnabled(False)
            self.edtDienThoaiSV.setEnabled(False)
            self.edtEmailSV.setEnabled(False)
            self.edtDiaChiSV.setEnabled(False)
        else:
            self.btnChinhSuaSV.setText("H???y b???")
            self.btnCapNhatSV.setEnabled(True)
            #self.edtMSSV.setEnabled(True)
            self.edtHoTenSV.setEnabled(True)
            self.edtNgaySinhSV.setEnabled(True)
            self.edtDienThoaiSV.setEnabled(True)
            self.edtEmailSV.setEnabled(True)
            self.edtDiaChiSV.setEnabled(True)

    def capNhatSV(self):
        print("Cap nhat sinh vi??n")
        self.btnChinhSuaSV.setText("Ch???nh s???a")
        masoSV = self.listSinhVien.currentItem().text().split('-')[0]
        objSinhvien = dp.getSinhvienByMaso(str(masoSV))
        print(objSinhvien)
        # id, sv_hoten, sv_ngaysinh, sv_dienthoai, sv_email, sv_diachi
        _id = objSinhvien[0]
        _hoten = self.edtHoTenSV.text()
        _ngaysinh = self.edtNgaySinhSV.text()
        _dienthoai = self.edtDienThoaiSV.text()
        _email = self.edtEmailSV.text()
        _diachi = self.edtDiaChiSV.toPlainText()
        print(_id)
        x = dp.capNhatSinhVien(_id, _hoten, _ngaysinh, _dienthoai, _email, _diachi)
        print(x)
        self.btnCapNhatSV.setEnabled(False)
        #self.edtMSSV.setEnabled(False)
        self.edtHoTenSV.setEnabled(False)
        self.edtNgaySinhSV.setEnabled(False)
        self.edtDienThoaiSV.setEnabled(False)
        self.edtEmailSV.setEnabled(False)
        self.edtDiaChiSV.setEnabled(False)
       
    def selectionChangedLop(self): 
        lop_ma = self.listLop.currentItem().text().split('-')[0]
        print(lop_ma)
        lop_id = dp.getLopIdByLopMa(lop_ma)
        print("ntn: " + str(lop_id))
        listSv = dp.getListSvOfLop(lop_id) 
        for sv in listSv:
            self.listSinhVien.addItem(sv[0])
            
    def selectionChangedSinhvien(self):
        masoSV = self.listSinhVien.currentItem().text().split('-')[0]
        objSinhvien = dp.getSinhvienByMaso(str(masoSV))
        if objSinhvien is None:
            self.btnCapNhatSV.setEnabled(True)
            self.btnChinhSuaSV.setEnabled(False)
            self.edtMSSV.setEnabled(True)
            self.edtHoTenSV.setEnabled(True)
            self.edtNgaySinhSV.setEnabled(True)
            self.edtDienThoaiSV.setEnabled(True)
            self.edtEmailSV.setEnabled(True)
            self.edtDiaChiSV.setEnabled(True)
        self.edtMSSV.setText(objSinhvien[1])
        self.edtHoTenSV.setText(objSinhvien[2])
        self.edtNgaySinhSV.setText(objSinhvien[4])
        self.edtDienThoaiSV.setText(objSinhvien[5])
        self.edtEmailSV.setText(objSinhvien[6])
        self.edtDiaChiSV.setText(objSinhvien[7])
        self.btnChinhSuaSV.setText("Ch???nh s???a")
        self.btnCapNhatSV.setEnabled(False)
        self.edtMSSV.setEnabled(False)
        self.edtHoTenSV.setEnabled(False)
        self.edtNgaySinhSV.setEnabled(False)
        self.edtDienThoaiSV.setEnabled(False)
        self.edtEmailSV.setEnabled(False)
        self.edtDiaChiSV.setEnabled(False)
     
def logout():
    login = LoginScreen()
    widget.addWidget(login)
    widget.setCurrentIndex(widget.currentIndex()+1)     
   
class QuanTriScreen(QtWidgets.QMainWindow):
     iTrangThai = 1
     iLoaiTK = 0
     
     def __init__(self):
        super(QuanTriScreen, self).__init__()
        loadUi("gui/quantri.ui",self)
        self.setWindowTitle("Qu???n tr???")
        self.stackedWidget.setCurrentWidget(self.trangchu)
        self.lblTime.setText("?? 2022 | ???????c ph??t tri???n b???i Nguy???n Trung Nguy??n - L?? ????ng Kh??i - Ng?? Gia B???o - L?? Minh Lu??n. L???p DC1896N1")
        self.lblTenQuanTri.setText(tenDN)
        
        self.btnTrangChu.clicked.connect(lambda: showQTTrangChu())
        self.btnSinhVien.clicked.connect(lambda: showQTSinhVien())
        self.btnLop.clicked.connect(lambda: showQTLop())
        self.btnNganh.clicked.connect(lambda: showQTNganh())
        self.btnHocPhan.clicked.connect(lambda: showQTHocPhan())
        self.btnGiangVien.clicked.connect(lambda: showQTGiangVien())
        self.btnCapNhatCB.clicked.connect(lambda: capNhatCB())
        self.btnClearNganh.clicked.connect(lambda: clearNganh())
        self.btnCapNhatTTCB.clicked.connect(lambda: capNhatTrangThaiTKCB())

        self.tbGiangVien.itemSelectionChanged.connect(lambda: getRowSelected())


        self.tbHocPhan.itemSelectionChanged.connect(lambda: getRowSelectedHocPhan())
        self.tWNganh.itemSelectionChanged.connect(lambda:getRowSelectedNganh())
        self.btnCapNhatHocPhan.clicked.connect(lambda: capNhatHocPhan())
        self.btnTimKiemHocPhan.clicked.connect(lambda: showQTHocPhanTimKiem())
        self.pBTimNganh.clicked.connect(lambda: showQTNganh())
        self.pBCapNhatNganh.clicked.connect(lambda: capNhatNganh())
        self.btnLogout.clicked.connect(lambda: logout())

        def capNhatCB():
            print("cap nhat cb")
            _mscb = self.edtMaCB.text()
            _htcb = self.edtHoTenCB.text()
            _dtcb = self.edtDienThoaiCB.text()
            _emcb = self.edtEmailCB.text()
            _dccb = self.edtDiaChiCB.text()
            _tdcb = self.edtTrinhDoCB.text()
            dp.insertOrUpdateCanBo(id, _mscb, _htcb, _dtcb, _emcb, _dccb, _tdcb , 1)
            setId(0)
        
        def capNhatHocPhan():
            print("cap nhat hoc phan",id)
            maHocPhan = self.edtMaHocPhan.text()
            tenHocPhan = self.edtTenHocPhan.text()
            dp.insertOrUpdateHocPhan(id, maHocPhan, tenHocPhan)
            
            
        def getRowSelectedHocPhan():
            items = self.tbHocPhan.selectedItems()
            try:
                hp = dp.getHocPhanByMaHocPhan(str(items[0].text()))
                setId(hp[0])
                if(hp is None):
                    print("Chua tim thay")
                else:
                    print(hp)
                    setId(hp[0])
                    self.edtMaHocPhan.setText(hp[1])
                    self.edtTenHocPhan.setText(hp[2])
            except:
                print("")

        def capNhatTrangThaiTKCB():
            # qm = QMessageBox()
            # ret = qm.question(self,'', "Kh??a t??i kho???n n??y '" + tenDN + "' ?", qm.Yes | qm.No)
            # if ret == qm.Yes:
            #     print("xoa cb")
            print(trangthaiTK)
            dp.capNhatTrangThaiTKCanBo(id, trangthaiTK)
            loadDataGiangVien(self.iTrangThai, self.iLoaiTK, self.edtSearch.text())
    
        def getRowSelected():
            items = self.tbGiangVien.selectedItems()
            try:
                cb = dp.getCanBoByTenDN(str(items[0].text()))
                if(cb is None):
                    print("CHua tim thay")
                else:
                    print(cb)
                    setId(cb[0])
                    self.edtMaCB.setText(cb[1])
                    self.edtHoTenCB.setText(cb[2])
                    self.edtDienThoaiCB.setText(cb[3])
                    self.edtEmailCB.setText(cb[4])
                    self.edtDiaChiCB.setText(cb[5])
                    self.edtTrinhDoCB.setText(cb[6])
                    if(cb[7] == '1'):
                        self.btnCapNhatTTCB.setText("Kh??a")
                        setTrangThaiTK("0")
                    else: 
                        self.btnCapNhatTTCB.setText("M???")
                        setTrangThaiTK("1")
            except:
                print()

        def capNhatNganh():
            print("cap nhat nganh",id)
            nganhMa = self.lEMaNganh.text()
            nganhTen = self.lETenNganh.text()
            if(len(nganhMa) != 0 and len(nganhTen) != 0):             
                dp.insertOrUpdateNganh(id, nganhMa, nganhTen)
                loadDataNganh("")
                clearNganh()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Vui l??ng nh???p ?????y ????? th??ng tin !")
                msg.exec_()

        def clearNganh():
            setId(0)
            print("clear nganh !",id)
            self.lEMaNganh.setText("")
            self.lETenNganh.setText("")


        def getRowSelectedNganh():
            items = self.tWNganh.selectedItems()
            try:
                nghanh = dp.getNganhByMaNganh(str(items[0].text()))
                setId(nghanh[0])
                if(nghanh is None):
                    print("CHua tim thay")
                else:
                    print(nghanh)
                    setId(nghanh[0])
                    self.lEMaNganh.setText(nghanh[1])
                    self.lETenNganh.setText(nghanh[2])                 
            except:
                print("")
                
        def showQTTrangChu():
            print("Trangchu")   
            self.stackedWidget.setCurrentWidget(self.trangchu)
            #code ??? ????y
            
        def showQTSinhVien():
            print("Sinhvien")  
            self.stackedWidget.setCurrentWidget(self.sinhvien) 
            
        def showQTLop():
            print("Lop") 
            self.stackedWidget.setCurrentWidget(self.lop)  
            
        def showQTNganh():
            print("Nganh")
            self.stackedWidget.setCurrentWidget(self.nganh)
            tuKhoa = self.lETimKiemNgah.text()
            loadDataNganh(tuKhoa)
            
        def showQTHocPhan():
            print("Hocphan")  
            self.stackedWidget.setCurrentWidget(self.hocphan)  
            loadDataHocPhan("")
            
        def showQTGiangVien():
            print("Giangvien")      
            self.stackedWidget.setCurrentWidget(self.giangvien)
            cbbTrangThai = self.cbbTrangThai
            cbbTrangThai.clear()
            cbbTrangThai.addItem("Ho???t ?????ng") 
            cbbTrangThai.addItem("Kh??ng ho???t ?????ng")
            cbbTrangThai.currentIndexChanged.connect(self.changeTrangThai)
            
            cbbLoaiTaiKhoan = self.cbbLoaiTK
            cbbLoaiTaiKhoan.clear()
            cbbLoaiTaiKhoan.addItem("Gi???ng vi??n")
            cbbLoaiTaiKhoan.addItem("Qu???n tr???")
            cbbLoaiTaiKhoan.currentIndexChanged.connect(self.changeLoaiTK)
            
            tukhoa = self.edtSearch.text()
            loadDataGiangVien(self.iTrangThai, self.iLoaiTK, tukhoa)
            
            self.btnTim.clicked.connect(lambda: loadDataGiangVien(self.iTrangThai, self.iLoaiTK, tukhoa))
            
        def loadDataGiangVien(iTrangThai, iLoaiTK, tukhoa):
            tukhoa = self.edtSearch.text()
            print("L???y d??? li???u n??" + str(iTrangThai) + " - " + str(iLoaiTK) + " - " + tukhoa)
            #L???y d??? li???u t??? db
            list_gv = dp.filterListCanBo(iTrangThai, iLoaiTK, tukhoa)
            row = 0
            header = self.tbGiangVien.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.tbGiangVien.horizontalHeader().setFont(QFont('Arial', weight = QFont.Bold))
            self.tbGiangVien.setRowCount(len(list_gv))
            for gv in list_gv:
                if(str(gv[1]) == ""): continue
                labelImg = QtWidgets.QLabel(self)

                if(iTrangThai==1):
                    strTrangThai = "??ang ho???t ?????ng"
                    setImagePath("../StudetnCheckedFace/icons/check.png")
                else:
                    strTrangThai = "Kh??ng ho???t ?????ng"
                    setImagePath("../StudetnCheckedFace/icons/cross.png")
                print(imagePath)
                header = self.tbGiangVien.horizontalHeader()       
                header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QHeaderView.Stretch)
                header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(3, QHeaderView.Stretch)
                header.setSectionResizeMode(4, QHeaderView.Stretch)
                header.setSectionResizeMode(5, QHeaderView.Stretch)
                header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
                
                self.tbGiangVien.setItem(row, 0, QtWidgets.QTableWidgetItem(gv[1]))
                self.tbGiangVien.setItem(row, 1, QtWidgets.QTableWidgetItem(gv[2]))
                self.tbGiangVien.setItem(row, 2, QtWidgets.QTableWidgetItem(gv[3]))
                self.tbGiangVien.setItem(row, 3, QtWidgets.QTableWidgetItem(gv[4]))
                self.tbGiangVien.setItem(row, 4, QtWidgets.QTableWidgetItem(gv[5]))
                self.tbGiangVien.setItem(row, 5, QtWidgets.QTableWidgetItem(gv[6]))
                self.tbGiangVien.setCellWidget(row, 6, ImgWidget(self))
                row += 1

        def loadDataHocPhan(tuKhoa):
            print("Lay data Hoc Phan")
            #L???y d??? li???u t??? db
            list_hp = dp.getListHocPhan(tuKhoa)
            self.tbHocPhan.setRowCount(len(list_hp))
            row = 0
            header = self.tbHocPhan.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.tbHocPhan.horizontalHeader().setFont(QFont('Arial', weight = QFont.Bold))
            for hp in list_hp:    
                header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QHeaderView.Stretch)
                self.tbHocPhan.setItem(row, 0, QtWidgets.QTableWidgetItem(hp[1]))
                self.tbHocPhan.setItem(row, 1, QtWidgets.QTableWidgetItem(hp[2]))
                row+=1

        def showQTHocPhanTimKiem():
            tuKhoa = self.edtTimKiemHocPhan.text()
            print(tuKhoa)
            loadDataHocPhan(tuKhoa)


        def loadDataNganh(tukhoa):
            print("L???y d??? li???u n??:" + str(tukhoa))
            #L???y d??? li???u t??? db
            list_nghanh = dp.filterListNghanh(tukhoa)
            row = 0
            header = self.tWNganh.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.tWNganh.horizontalHeader().setFont(QFont('Arial', weight = QFont.Bold))
            self.tWNganh.setRowCount(len(list_nghanh))
            for nganh in list_nghanh:
                header = self.tWNganh.horizontalHeader()       
                header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QHeaderView.Stretch)                
                self.tWNganh.setItem(row, 0, QtWidgets.QTableWidgetItem(nganh[1]))
                self.tWNganh.setItem(row, 1, QtWidgets.QTableWidgetItem(nganh[2]))
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

