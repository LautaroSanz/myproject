from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from models.product import Productos,Marca
from app import db

products = Blueprint('products', __name__)

@products.route('/get_marcas', methods=['GET'])
def get_marcas():
    query = request.args.get('q', '')
    marcas = Marca.query.filter(Marca.nombre.ilike(f'%{query}%')).all()
    return jsonify([{'nombre': marca.nombre} for marca in marcas])




def check(nombre, marca, precio):
    if not isinstance(nombre, str) or not nombre.strip():
        flash('El nombre debe ser un string no vacío')
        return False

    if not isinstance(marca, str) or not marca.strip():
        flash('La marca debe ser un string no vacío')
        return False

    try:
        precio = float(precio)
        if precio <= 0:
            flash('El precio debe ser un número positivo')
            return False
    except ValueError:
        flash('El precio debe ser un número válido')
        return False

    return True


@products.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = 'administrador'
        if request.form.get('password') == password:
            return redirect(url_for('products.home'))
        else:
            return render_template("login.html", error='Contraseña incorrecta')
    return render_template("login.html")

@products.route('/home')
def home():
    productos = Productos.query.all()
    return render_template("index.html", productos=productos)


@products.route('/add_products', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        precio = request.form['precio']

        # Verificar si la marca existe en la base de datos
        marca_existe = Marca.query.filter_by(nombre=marca).first()
        if not marca_existe:
            flash('La marca seleccionada no existe')
            return redirect(url_for('products.add_product'))

        if check(nombre, marca, precio):
            new_product = Productos(nombre=nombre, marca=marca, precio=float(precio))
            db.session.add(new_product)
            db.session.commit()
            flash('Producto agregado con éxito')
            return redirect(url_for('products.home'))
        else:
            # Obtener la lista de marcas para el template
            marcas = Marca.query.all()
            return render_template('index.html', nombre=nombre, marca=marca, precio=precio, marcas=marcas)

    # Obtener la lista de marcas para el template
    marcas = Marca.query.all()
    return render_template('index.html', marcas=marcas)

@products.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Productos.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        precio = request.form['precio']

        marca_existe = Marca.query.filter_by(nombre=marca).first()
        if not marca_existe:
            flash('La marca seleccionada no existe')
            return redirect(url_for('products.home'))


        if check(nombre, marca, precio):
            product.nombre = nombre
            product.marca = marca
            product.precio = float(precio)
            db.session.commit()
            flash('Producto actualizado con éxito')
            return redirect(url_for('products.home'))
        else:
            return render_template('edit-product.html', product=product, nombre=nombre, marca=marca, precio=precio)

    return render_template('edit-product.html', product=product)

@products.route('/delete/<int:id>', methods=['GET'])
def delete_product(id):
    product = Productos.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado con éxito')
    return redirect(url_for('products.home'))
