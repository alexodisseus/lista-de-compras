import sys
import inspect
from flask import Blueprint, render_template, request, redirect, url_for, flash
from model import create_person, list_person, update_person, delete_person, get_person, Person

people = Blueprint('people', __name__, url_prefix='/')


@people.route('/', methods=['GET'])
def index():
    return render_template('index.html')



@people.route('/people', methods=['GET'])
def list_people():
    filters = request.args.get('filter', '')
    people = list_person(filters)
    return render_template('list_people.html', data=people)

@people.route('/people/new', methods=['GET', 'POST'])
def new_person():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        types = request.form['types']
        create_person(name, password, types)
        flash('Pessoa criada com sucesso!', 'success')
        return redirect(url_for('people.list_people'))  # Correção aqui
    return render_template('person_form.html')

@people.route('/people/edit/<int:id>', methods=['GET', 'POST'])
def edit_person(id):
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        types = request.form['types']
        update_person(id, name, password, types)
        flash('Pessoa atualizada com sucesso!', 'success')
        return redirect(url_for('people.list_people'))  # Correção aqui
    person = None
    
    person = get_person(id)
    return render_template('person_form.html', person=person)

@people.route('/people/delete/<int:id>', methods=['POST'])
def delete_person_route(id):
    delete_person(id)
    flash('Pessoa deletada com sucesso!', 'success')
    return redirect(url_for('people.list_people'))  # Correção aqui



def configure(app):
	app.register_blueprint(people)