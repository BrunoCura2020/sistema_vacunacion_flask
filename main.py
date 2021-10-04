from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import flash
import psycopg2
#redirect: redireccionar ruta
#url_for: dar la ruta


app = Flask(__name__)
cadenaConexion="host='localhost' dbname='sistema_vacunacion' user='postgres' password='cura'"
obj=psycopg2.connect(cadenaConexion)
objCursor=obj.cursor()

#Inicializar una sesion: datos que guarda nuestra apllicación de servidor para luego reutilizarlo 
#La forma más basica es guardarlo en la memoria de la app 
app.secret_key = 'mysecretkey'

#Ruta para la pagina principal
#(APP.route: nos permitira crear nuestras rutas)

@app.route('/')
def index():
    objCursor.execute('SELECT * FROM usuarios')
    data = objCursor.fetchall()
    print(data)
    return render_template('login.html', usuarios = data)

@app.route('/info_vacunas')
def vacunas():
    objCursor.execute('SELECT * FROM vacunas')
    data = objCursor.fetchall()
    print(data)
    return render_template('info_vacunas.html', vacunas = data)

@app.route('/info_personas')
def personas():
    objCursor.execute('SELECT * FROM personas')
    data = objCursor.fetchall()
    print(data)
    return render_template('info_personas.html', personas = data)

#cada vez que hacemos llamamos alguna de esas rutas, haran operaciones como agregar, editar, eliminar
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    if request.method == 'POST':
        dni      = request.form['dni'] #recibe el dato del formulario y lo guarda en una variable
        clave    = request.form['clave'] 
        objCursor.execute('INSERT INTO usuarios (dni, clave) VALUES (%s, %s)', (dni, clave))
        obj.commit()
        flash('Usuario agregado correctamente')

        return redirect(url_for('index'))#redirecciona hacia la pagina principal 

@app.route('/editar/<id>')
def editar(id):
    objCursor.execute('SELECT * FROM usuarios WHERE id = {0}'.format(id))
    data = objCursor.fetchall()
    return render_template('editar_usuarios.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        dni    = request.form['dni']
        clave  = request.form['clave']
        objCursor.execute('''
            UPDATE usuarios SET dni = %s, clave = %s WHERE id = %s''', (dni, clave, id))
        obj.commit()
        flash('Usuario actualizado')
        return redirect(url_for('index'))

@app.route('/eliminar/<id>')
#<string:id>: cada vez que reciba una ruta de 'eliminar' debe de tener un numero para poder hacer una operacion
def eliminar_usuario(id):
    objCursor.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
    obj.commit()
    flash('Contacto removido')
    return redirect(url_for(index))

#validacion para comprobar que estamos arrancando como un archivo de ejecucion y no un modulo
#si el archivo que va a ejecutar es el principal(main.py) entonces va a ejecutar el port=300
if __name__ == '__main__':
    app.run(port=3000, debug=True)
