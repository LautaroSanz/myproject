# routes/marcas.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.product import Marca
from utils.db import db

marcas = Blueprint('marcas', __name__)

def check_marca(nombre):
    if not isinstance(nombre, str) or not nombre.strip():
        flash('El nombre de la marca debe ser un string no vacío')
        return False
    return True

@marcas.route('/', methods=['GET'])
def ver_marcas():
    marcas = Marca.query.all()
    return render_template('marcas.html', marcas=marcas)

@marcas.route('/add-marca', methods=['GET', 'POST'])
def add_marca():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if check_marca(nombre):
            nueva_marca = Marca(nombre=nombre, cant_art=0)
            db.session.add(nueva_marca)
            db.session.commit()
            flash('Marca agregada con éxito')
            return redirect(url_for('marcas.ver_marcas'))
    return render_template('add_marca.html')

@marcas.route('/edit-marca/<int:id>', methods=['GET', 'POST'])
def edit_marca(id):
    marca = Marca.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        if check_marca(nombre):
            marca.nombre = nombre
            db.session.commit()
            flash('Marca actualizada con éxito')
            return redirect(url_for('marcas.ver_marcas'))
    return render_template('edit_marca.html', marca=marca)

@marcas.route('/delete-marca/<int:id>', methods=['GET'])
def delete_marca(id):
    marca = Marca.query.get_or_404(id)
    db.session.delete(marca)
    db.session.commit()
    flash('Marca eliminada con éxito')
    return redirect(url_for('marcas.ver_marcas'))
