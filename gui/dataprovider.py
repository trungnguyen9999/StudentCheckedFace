import sqlite3 as sql
import hashlib

pw_default = hashlib.md5("123".encode())

def insertOrUpdateSinhVien(sv_mssv, sv_ten, lop_id, sv_dienthoai, sv_diachi, sv_email, sv_ngaysinh):
    conn = sql.connect("database/diemdanhsinhvien.db")
    query = "SELECT * FROM sinhvien where sv_mssv = ?"
    cursor = conn.execute(query, sv_mssv)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    print(isRecordExist)
    if(isRecordExist == 0):
        query = "INSERT INTO sinhvien (sv_mssv, sv_ten, lop_id, sv_dienthoai, sv_diachi, sv_email, sv_ngaysinh) VALUES (?, ?, ?, ?, ?, ?, ?)"
        conn.execute(query, (sv_mssv, sv_ten, lop_id, sv_dienthoai, sv_diachi, sv_email, sv_ngaysinh))
    else:
        query = "UPDATE sinhvien set sv_ten=?, lop_id=?, sv_dienthoai=?, sv_diachi=?, sv_email=?, sv_ngaysinh=? where sv_mssv=?"
        conn.execute(query, (sv_ten, lop_id, sv_dienthoai, sv_diachi, sv_email, sv_ngaysinh, sv_mssv))
    conn.commit()
    conn.close()

def insertOrUpdateCanBo(cb_maso, cb_ten, cb_dienthoai, cb_email):
    conn = sql.connect(database="database/diemdanhsinhvien.db")  
    query = "SELECT * FROM canbo where cb_maso = ?"
    cursor = conn.execute(query, cb_maso)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    print(isRecordExist)
    if(isRecordExist == 0):
        query = "INSERT INTO canbo (cb_ten, cb_dienthoai, cb_email, cb_password) VALUES (?, ?, ?, ?)"
        conn.execute(query, (cb_ten, cb_dienthoai, cb_email, pw_default.hexdigest))
    else:
        query = "UPDATE canbo set cb_ten=?, cb_dienthoai=?, cb_email=? where cb_maso=?"
        conn.execute(query, (cb_ten, cb_dienthoai, cb_email, cb_maso))
    conn.commit()
    conn.close() 

def updatePassword(cb_maso, cb_password, cb_newpassword):
    print("Update password")
    conn = sql.connect(database="database/diemdanhsinhvien.db")  
    query = "SELECT * FROM canbo where cb_maso = ? and cb_password = ?"
    cursor = conn.execute(query, (cb_maso, hashlib.md5(cb_password).hexdigest))
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if(isRecordExist==1):
        query = "update canbo set cb_password = ? where cb_maso = ?"
        conn.execute(query, (hashlib.md5(cb_newpassword).hexdigest, cb_maso))
    conn.commit()
    conn.close()

def login(cb_maso, password):
    conn = sql.connect(database="database/diemdanhsinhvien.db")
    statement = "SELECT cb_maso from canbo WHERE cb_maso=? AND cb_password =?;"
    print(statement)
    cur = conn.execute(statement, (cb_maso, password))
    isRecordExist = 0
    for row in cur:
        isRecordExist = 1
    if (isRecordExist == 0):  # An empty result evaluates to False.
        print("Login failed")
        return False
    else:
        print("Welcome")
        return True
        
        
# insertSinhVien("2", "2", 3, "4", "5", "6", "7")