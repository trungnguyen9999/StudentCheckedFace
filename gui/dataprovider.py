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

def insertOrUpdateCanBo(cb_id, cb_ma, cb_ten, cb_dienthoai, cb_email, cb_diachi, cb_trinhdo, cb_trangthai):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")  
    query = "SELECT cb_id FROM tb_canbo where cb_id = ?"
    cursor = conn.execute(query, [cb_id])
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if(isRecordExist == 0):
        query = "INSERT INTO tb_canbo (cb_ma, cb_ten, cb_dienthoai, cb_email, cb_diachi, cb_trinhdo, cb_trangthai) " 
        + "VALUES (?, ?, ?, ?, ?, ?, ?)"
        conn.execute(query, [str(cb_ma), str(cb_ten), str(cb_dienthoai), str(cb_email), str(cb_diachi), str(cb_trinhdo), str(cb_trangthai)])
    else:
        query = "UPDATE tb_canbo set cb_ma=?, cb_ten=?, cb_dienthoai=?, cb_email=?, cb_diachi=?, cb_trinhdo=?, cb_trangthai=? where cb_id=?"
        conn.execute(query, (cb_ma, cb_ten, cb_dienthoai, cb_email, cb_diachi, cb_trinhdo, cb_trangthai, cb_id))
    conn.commit()
    conn.close()

def insertOrUpdateHocPhan(hp_id,hp_ma,hp_ten):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db") 
    query = "SELECT hp_id FROM tb_hocphan where hp_id = ?"
    cursor = conn.execute(query, [hp_id])
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if(isRecordExist == 0):
        query = "INSERT INTO tb_hocphan (hp_ma, hp_ten) VALUES (?, ?)"
        conn.execute(query, [str(hp_ma), str(hp_ten)])
    else:
        query = "UPDATE tb_hocphan set hp_ma=?, hp_ten=? where hp_id=?"
        conn.execute(query, (hp_ma, hp_ten, hp_id))
    conn.commit()
    conn.close()

def insertOrUpdateNganh(nganh_id,nganh_ma,nganh_ten):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db") 
    query = "SELECT nganh_id FROM tb_nganh where nganh_id = ?"
    queryCheckMa = "SELECT nganh_id FROM tb_nganh where nganh_ma = ?"
    cursor = conn.execute(query, [nganh_id])
    cursorCheckMa = conn.execute(query, [nganh_ma])
    isRecordExist = 0
    isRecordCheckExist = 0
    for row in cursor:
        isRecordExist = 1
    for row in cursorCheckMa:
        isRecordCheckExist = 1

    if(isRecordExist == 0 and isRecordCheckExist == 0):
        query = "INSERT INTO tb_nganh (nganh_ma, nganh_ten) VALUES (?, ?)"
        conn.execute(query, [str(nganh_ma), str(nganh_ten)])
    else:
        query = "UPDATE tb_nganh set nganh_ma=?, nganh_ten=? where nganh_id=?"
        conn.execute(query, (nganh_ma, nganh_ten, nganh_id))
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

def login(cb_maso, password):
    loaitaikhoan = -1
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT loaitaikhoan from tb_canbo WHERE cb_ma=? AND cb_password =? and cb_trangthai = 1;"
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
    
def filterListCanBo(iTrangThai, iLoaiTK, tukhoa):
    print(tukhoa)
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT * from tb_canbo where cb_trangthai=? and loaitaikhoan=?"
    if(str(tukhoa) != ""):
        statement += " and (cb_ten like ? OR cb_dienthoai like ? OR cb_email like ? OR cb_diachi like ?)"
        cur = conn.execute(statement, (iTrangThai, iLoaiTK, '%'+str(tukhoa)+'%', '%'+str(tukhoa)+'%', '%'+str(tukhoa)+'%', '%'+str(tukhoa)+'%'))
    else:
        cur = conn.execute(statement, (str(iTrangThai), iLoaiTK))
        print(statement)
    result_set = cur.fetchall()
    return result_set

def getHocPhanByMaHocPhan(hp_ma):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT * from tb_hocphan where hp_ma = ?"
    cur = conn.execute(statement, [hp_ma])
    return cur.fetchall()[0]


def filterListNghanh(tukhoa):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT * from tb_nganh order by nganh_id desc"
    if(str(tukhoa) != ""):
        statement += " where (nganh_ma like ? or nganh_ten like ? )"
        cur = conn.execute(statement, [str("%"+ tukhoa + "%"), str("%"+tukhoa+"%")])
    else:
        cur = conn.execute(statement)
    result_set = cur.fetchall()
    return result_set


def getNganhByMaNganh(nganh_ma):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT * from tb_nganh where nganh_ma = ?"
    cur = conn.execute(statement, [nganh_ma])
    return cur.fetchall()[0]


def getCanBoByTenDN(cb_maso):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT * from tb_canbo where cb_ma = ?"
    cur = conn.execute(statement, [cb_maso])
    return cur.fetchall()[0]

def getCanBoById(cb_id):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT * from tb_canbo where cb_id = ?"
    cur = conn.execute(statement, [cb_id])
    return cur.fetchall()[0]

def getListHocPhan(tukhoa):
    print(tukhoa)
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT * from tb_hocphan"
    if(str(tukhoa) != ""):
        statement += " where hp_ten like ? OR hp_ma like ?"
        cur = conn.execute(statement, ['%'+str(tukhoa)+'%', '%'+str(tukhoa)+'%'])
    else:
        cur = conn.execute(statement)
    return cur.fetchall()


def getLopOfCanbo(cb_maso):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "select DISTINCT lop_id, lop_ten, lop_ma from tb_thoikhoabieu INNER JOIN tb_canbo USING (cb_id) INNER JOIN tb_lop USING (lop_id) where cb_ma = ?"
    cur = conn.execute(statement, [str(cb_maso)])
    return cur.fetchall()
    
def getLopIdByLopMa(lop_ma):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "select DISTINCT lop_id from tb_lop where lop_ma = ?"
    cur = conn.execute(statement, [str(lop_ma).strip()])
    return cur.fetchone()[0]
    
def getListSvOfLop(lop_id):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "select sv_maso OR ' - ' OR sv_hoten from tb_sinhvien where lop_id = ?;"
    cur = conn.execute(statement, [lop_id])
    return cur.fetchall()

def getSinhvienByMaso(sv_maso):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT * from tb_sinhvien where sv_maso = ?"
    cur = conn.execute(statement, [str(sv_maso).strip()])
    return cur.fetchall()[0]

def getSinhvienById(sv_id):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")
    statement = "SELECT * from tb_sinhvien where sv_id = ?"
    cur = conn.execute(statement, [sv_id])
    return cur.fetchall()[0]

def capNhatSinhVien(id, sv_hoten, sv_ngaysinh, sv_dienthoai, sv_email, sv_diachi):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")  
    query = "SELECT * FROM tb_sinhvien where sv_id = ?"
    cursor = conn.execute(query, [id])
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if(isRecordExist==1):
        query = "update tb_sinhvien set sv_hoten = ?, sv_ngaysinh = ?, sv_dienthoai = ?, sv_email = ?, sv_diachi = ? where sv_id = ?"
        conn.execute(query, [str(sv_hoten), str(sv_ngaysinh), str(sv_dienthoai), str(sv_email), str(sv_diachi), id])
    conn.commit()
    conn.close()
    
def capNhatCanBo(id, cb_ten, cb_dienthoai, cb_email, cb_diachi):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")  
    query = "SELECT * FROM tb_canbo where cb_id = ?"
    cursor = conn.execute(query, [id])
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if(isRecordExist==1):
        query = "update tb_canBo set cb_ten = ?, cb_dienthoai = ?, cb_email = ?, cb_diachi = ? where cb_id = ?"
        conn.execute(query, [str(cb_ten), str(cb_dienthoai), str(cb_email), str(cb_diachi), id])
    conn.commit()
    conn.close()
    
def capNhatTrangThaiTKCanBo(id, tt):
    conn = sql.connect(database="database/DatabaseStudentCheckedFace.db")  
    query = "update tb_canBo set cb_trangthai = ? where cb_id = ?"
    conn.execute(query, [str(tt), id])
    conn.commit()
    conn.close()

