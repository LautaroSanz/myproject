from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.product import Productos
from app import db  

products = Blueprint('products', __name__)

@products.route('/')
def home():
    productos= Productos.query.all()
    return render_template("index.html",productos=productos)

@products.route('/add_products', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        precio = request.form['precio']
        

        if not isinstance(nombre, str):
            flash('El nombre debe ser un string')
            return redirect(url_for('products.add_product'))
        
        if not isinstance(marca, str):
            flash('La marca debe ser un string')
            return redirect(url_for('products.add_product'))
        
        try:
            precio = float(precio)
        except ValueError:
            flash('El precio debe ser un flotante')
            return redirect(url_for('products.home'))
     
     
        new_product = Productos(nombre=nombre, marca=marca, precio=precio)
        db.session.add(new_product)
        db.session.commit()
        flash('Product Added')
        return redirect(url_for('products.home'))

@products.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Productos.query.get_or_404(id)  
    if request.method == 'POST':
        product.nombre = request.form['nombre']
        product.marca = request.form['marca']
        product.precio = request.form['precio']
        db.session.commit()
        flash('Product Updated')
        return redirect(url_for('products.home'))  
    return render_template('edit-product.html', product=product)


@products.route('/delete/<int:id>', methods=['GET'])
def delete_product(id):
    product = Productos.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product Removed Succesfully')
    return redirect(url_for('products.home'))  
