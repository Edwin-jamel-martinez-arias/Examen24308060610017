from flask import Flask, render_template, request, redirect, url_for
from gestortareas import GestorTareas
import bcrypt 

app = Flask(__name__)

MONGO_URI = "mongodb://localhost:27017/"

db_admin = GestorTareas(MONGO_URI)

@app.route('/')
def home():
    return render_template('inicio.html')

@app.route('/crear-cuenta', methods=['GET', 'POST'])
def crear_cuenta():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        gmail = request.form.get('gmail')
        password = request.form.get('contraseña')
        razon = request.form.get('razon')

        usuario_id = db_admin.crear_usuario(nombre, gmail, password, razon)
        
        if usuario_id:
            return redirect(url_for('tareas'))
        else:
            return "<h3>Error: su correo ya esta registrado..</h3> <a href='/crear-cuenta'>Volver</a>"

    return render_template('crearcuenta.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        gmail_ingresado = request.form.get('gmail')
        password_ingresado = request.form.get('contraseña')

        usuario_en_db = db_admin.obtener_usuario_por_gmail(gmail_ingresado)

        if usuario_en_db:
            es_valida = bcrypt.checkpw(
                password_ingresado.encode('utf-8'), 
                usuario_en_db['contraseña']
            )
            
            if es_valida:
                return redirect(url_for('tareas'))
        
        return "<h3>Correo o contraseña incorrecto =/" \
        ".</h3> <a href='/registro'>Volver a intentar</a>"
    
    return render_template('registro.html')

@app.route('/tareas')
def tareas():
    return render_template('tareas.html')

if __name__ == '__main__':
    app.run(debug=True)
