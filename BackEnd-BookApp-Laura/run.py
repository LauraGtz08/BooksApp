from flask import Flask, request, render_template
from flask.json.tag import JSONTag
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import json

#-----------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5432/db_books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)

#-----------------------------------------------------------------------------------------------------------------------

class Usuarios(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.password = password

#-----------------------------------------------------------------------------------------------------------------------

class Editorial(db.Model):
    __tablename__ = "editorial"
    id_editorial = db.Column(db.Integer, primary_key=True)
    nombre_editorial = db.Column(db.String(80))

    def __init__(self, nombre_editorial):
        self.nombre_editorial = nombre_editorial

#-----------------------------------------------------------------------------------------------------------------------

class Genero(db.Model):
    __tablename__ = "genero"
    id_genero = db.Column(db.Integer, primary_key=True)
    nombre_genero = db.Column(db.String(80))

    def __init__(self, nombre_genero):
        self.nombre_genero = nombre_genero

#-----------------------------------------------------------------------------------------------------------------------

class Autor(db.Model):
    __tablename__ = "autor"
    id_autor = db.Column(db.Integer, primary_key=True)
    nombre_autor = db.Column(db.String(120))
    fechanac = db.Column(db.Date)
    nacionalidad = db.Column(db.String(80))
    

    def __init__(self, nombre_autor, fechanac, nacionalidad):
        self.nombre_autor = nombre_autor
        self.fechanac = fechanac
        self.nacionalidad = nacionalidad

#-----------------------------------------------------------------------------------------------------------------------
       
class Libro(db.Model):
    __tablename__ = "libro"
    id_libro = db.Column(db.Integer, primary_key=True)
    titulo_libro = db.Column(db.String(255))
    fecha_publicacion = db.Column(db.Date)
    numero_paginas = db.Column(db.Integer)
    formato = db.Column(db.String(30))
    id_editorial = db.Column(db.Integer, db.ForeignKey("editorial.id_editorial", ondelete = 'CASCADE'))
    id_genero = db.Column(db.Integer, db.ForeignKey("genero.id_genero", ondelete = 'CASCADE'))
    id_autor = db.Column(db.Integer, db.ForeignKey("autor.id_autor", ondelete = 'CASCADE'))

    def __init__(self, titulo_libro, fecha_publicacion, numero_paginas, formato, id_editorial, id_genero, id_autor):
        self.titulo_libro = titulo_libro
        self.fecha_publicacion = fecha_publicacion
        self.numero_paginas = numero_paginas
        self.formato = formato
        self.id_editorial = id_editorial
        self.id_genero = id_genero
        self.id_autor = id_autor

#-----------------------------------------------------------------------------------------------------------------------

class Favorito(db.Model):
    __tablename__ = "favorito"
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete = 'CASCADE'), primary_key=True)
    id_libro = db.Column(db.Integer, db.ForeignKey("libro.id_libro", ondelete = 'CASCADE'), primary_key=True)

    def __init__(self, id_usuario, id_libro):
        self.id_usuario = id_usuario
        self.id_libro = id_libro

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()
    email = request_data["email"]
    password = request_data["password"]
    print(email)
    print(password)
    #email = request.form["email"]
    #password = request.form["password"]
    consulta_usuario = Usuarios.query.filter_by(email=email).first()
    consulta_usuario.password
    if(consulta_usuario.password == password):
        return "INICIO DE SESION EXITOSA"
    else:
        return "FAIL"
    #bcrypt.check_password_hash(consulta_usuario.password, password)
    
#-----------------------------------------------------------------------------------------------------------------------

@app.route("/registrarUsuario", methods=["POST"])
def registrarUsuario():
    request_data = request.get_json()
    email = request_data["email"]
    password = request_data["password"]
    print(email)
    print(password)
    #email = request.form["email"]
    #password = request.form["password"]
    #password_cifrado = bcrypt.generate_password_hash(password).decode('utf-8')
    #print(password_cifrado)
    usuario_nuevo = Usuarios(email=email, password=password)
    db.session.add(usuario_nuevo)
    db.session.commit()

    return "USUARIO REGISTRADO"

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/consultarSelect")
def consultarSelect():
    consultar_editorial = Editorial.query.all()
    consultar_genero = Genero.query.all()
    consultar_autor = Autor.query.all()
    dict_editorial = {}
    dict_genero = {}
    dict_autor = {}
    dict_all = {}

    for i, data in enumerate(consultar_editorial):
        dict_editorial[i] = {
            'id': data.id_editorial,
            'nombre': data.nombre_editorial
        }

    for i, data in enumerate(consultar_genero):
        dict_genero[i] = {
            'id': data.id_genero,
            'nombre': data.nombre_genero
        }

    for i, data in enumerate(consultar_autor):
        dict_autor[i] = {
            'id': data.id_autor,
            'nombre': data.nombre_autor
        }

    dict_all['editoriales'] = dict_editorial
    dict_all['generos'] = dict_genero
    dict_all['autores'] = dict_autor

    print(consultar_genero)
    print(dict_genero)

    json_file = json.dumps(dict_all, ensure_ascii = False)
    return json_file

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/registrarEditorial", methods=["POST"])
def registrarEditorial():
    request_data = request.get_json()
    nombre_editorial = request_data["nombreEditorial"]
    print(nombre_editorial)
    new_editorial = Editorial(nombre_editorial=nombre_editorial)
    db.session.add(new_editorial)
    db.session.commit()

    return "EDITORIAL REGISTRADA"

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/registrarGenero", methods=["POST"])
def registrarGenero():
    request_data = request.get_json()
    nombre_genero = request_data["nombreGenero"]
    print(nombre_genero)
    new_genero = Genero(nombre_genero=nombre_genero)
    db.session.add(new_genero)
    db.session.commit()

    return "GENERO REGISTRADO"

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/registrarAutor", methods=["POST"])
def registrarAutor():
    request_data = request.get_json()
    nombre_autor = request_data["nombreAutor"]
    fechanac = request_data["fechanacAutor"]
    nacionalidad = request_data["nacionalidadAutor"]
    print(nombre_autor)
    print(fechanac)
    print(nacionalidad)
    new_autor = Autor(nombre_autor=nombre_autor, fechanac=fechanac, nacionalidad=nacionalidad)
    db.session.add(new_autor)
    db.session.commit()

    return "AUTOR REGISTRADO"

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/registrarLibro", methods=["POST"])
def registrarLibro():
    request_data = request.get_json()
    titulo_libro = request_data["tituloLibro"]
    fecha_publicacion = request_data["fechapubLibro"]
    numero_paginas = request_data["nopagLibro"]
    formato = request_data["formatoLibro"]
    id_editorial = request_data["editorial"]
    id_genero = request_data["genero"]
    id_autor = request_data["autor"]
    new_libro = Libro(titulo_libro=titulo_libro, fecha_publicacion=fecha_publicacion, 
    numero_paginas=numero_paginas, formato=formato, id_editorial=id_editorial, id_genero=id_genero, id_autor=id_autor)
    db.session.add(new_libro)
    db.session.commit()

    return "LIBRO REGISTRADO"

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/consultarSelectFavorito")
def consultarSelectFavorito():
    consultar_usuario = Usuarios.query.all()
    consultar_libro = Libro.query.all()
    dict_usuario = {}
    dict_libro = {}
    dict_all = {}


    for i, data in enumerate(consultar_usuario):
        dict_usuario[i] = {
            'id': data.id,
            'email': data.email
        }

    for i, data in enumerate(consultar_libro):
        dict_libro[i] = {
            'id_libro': data.id_libro,
            'titulo_libro': data.titulo_libro
        }

    dict_all['usuarios'] = dict_usuario
    dict_all['libros'] = dict_libro


    print(consultar_libro)
    print(dict_libro)
    print(consultar_usuario)
    print(dict_usuario)

    json_file = json.dumps(dict_all, ensure_ascii = False)
    return json_file

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/registrarFavorito", methods=["POST"])
def registrarFavorito():
    request_data = request.get_json()
    id_usuario = request_data["usuario"]
    id_libro = request_data["libro"]
    new_favorito = Favorito(id_usuario=id_usuario, id_libro=id_libro)
    db.session.add(new_favorito)
    db.session.commit()

    return "FAVORITO REGISTRADO"

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/menu")
def menu():
    libros = Libro.query.join(Genero, Libro.id_genero == Genero.id_genero).join(Autor, 
    Libro.id_autor == Autor.id_autor).join(Editorial, Libro.
    id_editorial == Editorial.id_editorial).add_columns(Libro.titulo_libro, Autor.nombre_autor, 
    Autor.nacionalidad, Libro.fecha_publicacion, Genero.nombre_genero, 
    Editorial.nombre_editorial, Libro.numero_paginas, Libro.formato, Libro.id_libro)
    print(libros)
    dict_libros = {}

    for i, data in enumerate(libros):
        dict_libros[i] = {
            'id_libro': data.id_libro,
            'titulo_libro': data.titulo_libro,
            'fecha_publicacion': data.fecha_publicacion,
            'numero_paginas': data.numero_paginas,
            'formato': data.formato,
            'nombre_editorial': data.nombre_editorial,
            'nombre_genero': data.nombre_genero,
            'nombre_autor': data.nombre_autor
        }

    json_file = json.dumps(dict_libros, ensure_ascii = False, default=str)
    return json_file

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/TablaFavoritos")
def TablaFavoritos():

    favoritos = Favorito.query.join(Libro, Favorito.id_libro == Libro.id_libro).join(Usuarios, 
    Favorito.id_usuario == Usuarios.id).add_columns(Usuarios.email, Libro.titulo_libro)
    print(favoritos)
    dict_favoritos = {}

    for i, data in enumerate(favoritos):
        dict_favoritos[i] = {
            'titulo_libro': data.titulo_libro,
            'email': data.email
        }

    json_file = json.dumps(dict_favoritos, ensure_ascii = False, default=str)
    return json_file

## MODIFICAR Y ELIMINAR

# @app.route("/eliminarAutor")
# def eliminarAutor(id):
#     Autor.query.filter_by(nombre_autor=id).delete()
#     db.session.comit()
#     return redirect("/verautor")


# @app.route("/editarAutor/<id>")
# def editarAutor():
#     buscar_autor = Autor.query.filter_by(nombre_autor=id).first()
#     return render_template("modificarAutor.html", buscar_autor=buscar_autor)

# @app.route("/modificarAutor", methods=['POST'])
# def modificarAutor():

#-----------------------------------------------------------------------------------------------------------------------
@app.route("/eliminarAutor/<id>")
def eliminarAutor(id):
    print(id)
    autor_delete = db.session.query(Autor).filter(Autor.id_autor == id).first()
    db.session.delete(autor_delete)
    db.session.commit()
    return "AUTOR ELIMINADO"

#-----------------------------------------------------------------------------------------------------------------------
@app.route("/eliminarGenero/<id>")
def eliminarGenero(id):
    print(id)
    genero_delete = db.session.query(Genero).filter(Genero.id_genero == id).first()
    db.session.delete(genero_delete)
    db.session.commit()
    return "EDITORIAL ELIMINADA"

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/eliminarEditorial/<id>")
def eliminarEditorial(id):
    print(id)
    editorial_delete = db.session.query(Editorial).filter(Editorial.id_editorial == id).first()
    db.session.delete(editorial_delete)
    db.session.commit()
    return "EDITORIAL ELIMINADA"

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/eliminarLibro/<id>", methods=["DELETE"])
def eliminarLibro(id):
    libro_delete = db.session.query(Libro).filter(Libro.id_libro == id).first()
    db.session.delete(libro_delete)
    db.session.commit()
    return "LIBRO ELIMINADO"


#-----------------------------------------------------------------------------------------------------------------------   

@app.route("/editarLibro", methods=["PATCH"])
def editarLibro():
    request_data = request.get_json()
    consulta_libro = Libro.query.filter_by(id_libro=request_data['libro']).first()
    print(consulta_libro)
    print(consulta_libro.titulo_libro)
    print(consulta_libro.numero_paginas)

    new_titulo_libro = request_data["tituloLibro"]
    new_fecha_publicacion = request_data["fechapubLibro"]
    new_numero_paginas = request_data["nopagLibro"]
    new_formato = request_data["formatoLibro"]
    new_id_editorial = request_data["editorial"]
    new_id_genero = request_data["genero"]
    new_id_autor = request_data["autor"]
   
    consulta_libro.titulo_libro = new_titulo_libro
    consulta_libro.fecha_publicacion = new_fecha_publicacion
    consulta_libro.numero_paginas = new_numero_paginas
    consulta_libro.formato = new_formato
    consulta_libro.id_editorial = new_id_editorial 
    consulta_libro.id_genero = new_id_genero
    consulta_libro.id_autor = new_id_autor
    db.session.commit()


    return "LIBRO ACTUALIZADO"

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/obtenerLibro/<id>")
def obtenerLibro(id):
    consultar_libro = Libro.query.filter_by(id_libro=id).first()
    dict_libro = {}

    
    dict_libro = {
        'id_libro': consultar_libro.id_libro,
        'titulo_libro': consultar_libro.titulo_libro,
        'fecha_publicacion': consultar_libro.fecha_publicacion,
        'numero_paginas': consultar_libro.numero_paginas,
        'formato': consultar_libro.formato,
        'id_editorial': consultar_libro.id_editorial,
        'id_genero': consultar_libro.id_genero,
        'id_autor': consultar_libro.id_autor
    }
        


    json_file = json.dumps(dict_libro, ensure_ascii = False, default=str)
    print(json_file)
    return json_file



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)