from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping_list.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    lista_id = db.Column(db.Integer, db.ForeignKey('lista.id'), nullable=True)  # Adicionando a chave estrangeira

class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_lista = db.Column(db.String(100), nullable=False)
    evento = db.Column(db.String(100), nullable=False)
    data_evento = db.Column(db.String(10), nullable=False)
    itens = db.relationship('Item', backref='lista', lazy=True)
    participantes = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listas', methods=['GET'])
def listas():
    todas_listas = Lista.query.all()
    return render_template('listas.html', listas=todas_listas)

@app.route('/listas', methods=['POST'])
def add_lista():
    data = request.get_json()
    nova_lista = Lista(nome_lista=data['nome_lista'], evento=data['evento'], data_evento=data['data_evento'], participantes=data.get('participantes'))
    db.session.add(nova_lista)
    db.session.commit()
    return jsonify({'message': 'Lista adicionada!'}), 201

@app.route('/listas/<int:lista_id>', methods=['GET'])
def get_lista(lista_id):
    lista = Lista.query.get_or_404(lista_id)
    return render_template('itens.html', lista=lista)

@app.route('/listas/<int:lista_id>/items', methods=['POST'])
def add_item_to_lista(lista_id):
    data = request.get_json()
    novo_item = Item(nome=data['nome'], quantidade=data['quantidade'], preco=data['preco'], lista_id=lista_id)
    db.session.add(novo_item)
    db.session.commit()
    return jsonify({'message': 'Item adicionado!'}), 201

@app.route('/listas', methods=['GET'])
def get_listas():
    listas = Lista.query.all()
    return jsonify([{ 'id': lista.id, 'nome_lista': lista.nome_lista, 'evento': lista.evento, 'data_evento': lista.data_evento, 'participantes': lista.participantes } for lista in listas])

if __name__ == '__main__':
    app.run(debug=True)
