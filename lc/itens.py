from flask import Flask
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import model
import requests


itens = Blueprint('itens', __name__, url_prefix='/itens')


@itens.route('/', methods=['GET'])
def index():
    return render_template('itens/index.html')  


@itens.route('/cadastrar', methods=['GET', 'POST'])
def create():
    product_name = request.args.get('name', '')
    product_image = request.args.get('image', '')
    product_description = request.args.get('description', '')
    product_quantity = request.args.get('quantity', '')

    if request.method == 'POST':
        # Aqui você pode processar o cadastro do item
        # Exemplo: salvar no banco de dados
        flash('Item cadastrado com sucesso!')
        return redirect(url_for('itens.index'))

    return render_template('itens/create.html', 
                           product_name=product_name, 
                           product_image=product_image, 
                           product_description=product_description, 
                           product_quantity=product_quantity)




@itens.route('/consulta', methods=['GET', 'POST'])
def search():
    product_info = None
    if request.method == 'POST':
        ean_code = request.form['ean_code']
        product_info = get_product_info(ean_code)
        print(product_info)  # Imprimindo as informações no terminal
    return render_template('itens/search.html', product_info=product_info)




def get_product_info(ean_code: str):
    response = requests.get(f'https://world.openfoodfacts.org/api/v0/product/{ean_code}.json')
    if response.status_code == 200:
        product = response.json().get('product', {})
        
        return {
            'name': product.get('product_name', 'N/A'),
            'image_url': product.get('image_url', ''),
            'quantity': product.get('quantity', 'N/A'),
            'description': product.get('description', 'N/A'),
            'has_image': bool(product.get('image_url'))  # Verifica se há imagem
        }
    return {}






def configure(app):
    app.register_blueprint(itens)

