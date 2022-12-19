import sqlite3 as sql
import hashlib

pw_default = hashlib.md5("123".encode())

def insertOrUpdateSinhVien(sv_mssv, sv_ten, lop_id, sv_dienthoai, sv_diachi, sv_email, sv_ngaysinh):
    conn = sql.connect("database/DatabaseStudentCheckedFace.db")
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

def insertOrUpdateCanBo(cb_maso, cb_ten, cb_dienthoai, cb_email, cb_diachi, cb_trinhdo, cb_trangthai):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")  
    query = "SELECT cb_id FROM canbo where cb_maso = ?"
    cursor = conn.execute(query, cb_maso)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    print(isRecordExist)
    if(isRecordExist == 0):
        query = "INSERT INTO canbo (cb_ten, cb_dienthoai, cb_email, cb_password, cb_diachi, cb_trinhdo, cb_trangthai) " 
        + "VALUES (?, ?, ?, ?, ?, ?, ?)"
        conn.execute(query, (cb_ten, cb_dienthoai, cb_email, pw_default.hexdigest, cb_diachi, cb_trinhdo, cb_trangthai))
    else:
        query = "UPDATE canbo set cb_ten=?, cb_dienthoai=?, cb_email=?, cb_diachi=?, cb_trinhdo=?, cb_trangthai=? where cb_maso=?"
        conn.execute(query, (cb_ten, cb_dienthoai, cb_email, cb_diachi, cb_trinhdo, cb_trangthai, cb_maso))
    conn.commit()
    conn.close() 

def updatePassword(cb_maso, cb_password, cb_newpassword):
    print("Update password")
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")  
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
    loaitaikhoan = -1
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT loaitaikhoan from tb_canbo WHERE cb_ma=? AND cb_password =?;"
    cur = conn.execute(statement, (str(cb_maso), str(password)))
    isRecordExist = 0
    result_set = cur.fetchall()
    for row in result_set:
        loaitaikhoan = row[0]
        isRecordExist = 1
    if (isRecordExist == 0):
        return -1
    else:
        return loaitaikhoan
    
def getListCanBo(iTrangThai, iLoaiTK, tukhoa):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT * from tb_canbo where cb_trangthai=? and loaitaikhoan=?"
    if(str(tukhoa) != ""):
        statement += " and (cb_ten ilike ? || cb_dienthoai like ? || cb_email ilike ? || cb_diachi ilike ?)"
        cur = conn.execute(statement, (str(iTrangThai), str(iLoaiTK), str(tukhoa), str(tukhoa), str(tukhoa), str(tukhoa)))
    else:
        cur = conn.execute(statement, (str(iTrangThai), iLoaiTK))
    result_set = cur.fetchall()
    return result_set


def getListLop():
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")  
    query = "SELECT * FROM lop"
    result = conn.execute(query)
    for row in result.fetchall():
        print(row)

def getListNganh():
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")  
    query = "SELECT * FROM nganh"
    result = conn.execute(query)
    for row in result.fetchall():
        print(row)
        
# insertSinhVien("2", "2", 3, "4", "5", "6", "7")