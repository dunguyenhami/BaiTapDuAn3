from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Cấu hình kết nối đến cơ sở dữ liệu PostgreSQL
def ket_noi_csdl():
    conn = psycopg2.connect(
        host="localhost",
        database="web",  
        user="postgres",  
        password="161024" 
    )
    return conn

@app.route('/')
def index():
    conn = ket_noi_csdl()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee_db")  # Sử dụng tên bảng employee_db
    nhan_vien = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', nhan_vien=nhan_vien)

@app.route('/them_nhan_vien', methods=['POST'])
def them_nhan_vien():
    conn = ket_noi_csdl()
    cur = conn.cursor()

    # Nhận các giá trị từ form
    id_nv = request.form['id']
    ten = request.form['ten']
    tuoi = request.form['tuoi']
    chuc_vu = request.form['chuc_vu']

    # Chèn nhân viên vào cơ sở dữ liệu
    cur.execute("INSERT INTO employee_db (id, name, age, position) VALUES (%s, %s, %s, %s)", (id_nv, ten, tuoi, chuc_vu))
    conn.commit()

    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/xoa_nhan_vien/<int:id>', methods=['POST'])
def xoa_nhan_vien(id):
    conn = ket_noi_csdl()
    cur = conn.cursor()
    cur.execute("DELETE FROM employee_db WHERE id = %s", (id,))  # Sử dụng tên bảng employee_db
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/chinh_sua_nhan_vien/<int:id>', methods=['GET', 'POST'])
def chinh_sua_nhan_vien(id):
    conn = ket_noi_csdl()
    cur = conn.cursor()

    if request.method == 'POST':
        ten = request.form['ten']
        tuoi = request.form['tuoi']
        chuc_vu = request.form['chuc_vu']
        cur.execute("UPDATE employee_db SET name = %s, age = %s, position = %s WHERE id = %s", (ten, tuoi, chuc_vu, id))  # Sử dụng tên bảng employee_db
        conn.commit()
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM employee_db WHERE id = %s", (id,))  # Sử dụng tên bảng employee_db
    nhan_vien_chinh_sua = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('index.html', nhan_vien_chinh_sua=nhan_vien_chinh_sua)

if __name__ == '__main__':
    app.run(debug=True)
