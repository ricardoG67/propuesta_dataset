from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import numpy as np

app = Flask(__name__)
cnx = mysql.connector.connect(host='localhost', user='root', password='', database='propuesta_dataset')
app.secret_key = 'mysecretkey'

'''
Imagenes
1.- ID
2.- url
3.- clicks
4.- impresiones (cantidad de veces que se mostro)
5.- CTR (clicks/impresiones)
'''

@app.route('/')
def home():

    numeros = (random_generator())
    
    numeros = tuple([int(x) for x in numeros])

    cnx = mysql.connector.connect(host='localhost', user='root', password='', database='propuesta_dataset')
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM imagenes where id IN (%s,%s,%s,%s,%s,%s)', (numeros[0],numeros[1],numeros[2],numeros[3],numeros[4],numeros[5]))
    data = cursor.fetchall()
    cnx.commit()

    incrementar_impresiones(numeros)

    return render_template('index.html', data=data)

@app.route('/seleccionado/<string:id>')
def seleccionado(id):
    incrementar_click(id)
    return redirect(url_for('home'))


############
#FUNCIONES
############
def random_generator():
    id = max_id()
    while(True):
        numbers = np.random.randint(1, id, 6)
        numbers = np.unique(numbers)
        if len(numbers) == 6:
            return numbers

def max_id():
    cnx = mysql.connector.connect(host='localhost', user='root', password='', database='propuesta_dataset')
    cursor = cnx.cursor()
    cursor.execute('SELECT MAX(id) FROM imagenes')
    data = cursor.fetchone()
    cnx.commit()
    return data

def incrementar_impresiones(numeros):
    cnx = mysql.connector.connect(host='localhost', user='root', password='', database='propuesta_dataset')
    cursor = cnx.cursor()
    cursor.execute('UPDATE imagenes SET impresiones = impresiones + 1 where id IN (%s,%s,%s,%s,%s,%s)', (numeros[0],numeros[1],numeros[2],numeros[3],numeros[4],numeros[5]))
    cnx.commit()
    update_ctr(numeros)

def incrementar_click(id):
    cnx = mysql.connector.connect(host='localhost', user='root', password='', database='propuesta_dataset')
    cursor = cnx.cursor()
    cursor.execute('UPDATE imagenes SET clicks = clicks + 1 where id = %s', (id,))
    cnx.commit()

def update_ctr(numeros):
    numeros = [float(x) for x in numeros]

    cnx = mysql.connector.connect(host='localhost', user='root', password='', database='propuesta_dataset')
    cursor = cnx.cursor()
    cursor.execute('UPDATE imagenes SET CTR = clicks/impresiones where id IN (%s,%s,%s,%s,%s,%s)', (numeros[0],numeros[1],numeros[2],numeros[3],numeros[4],numeros[5]))
    cnx.commit()

#NO FUNCIONA LO DE UPDATE_CTR POR LO QUE SE HARÁ MANUAL
'''
UPDATE imagenes
SET CTR = clicks / impresiones
WHERE impresiones > 0;
'''

if __name__ == '__main__':
    app.run(debug=True)