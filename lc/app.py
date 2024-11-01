import admin
#import shareholder
#import quote
import itens
import lists
import people
from flask_bootstrap import Bootstrap
import model

from flask import Flask


db = model


app = Flask(__name__)
app.config['TITLE'] = "Listas de compras"
app.secret_key = b'guerra aos senhores'


#shareholder.configure(app)
#quote.configure(app)
Bootstrap(app)
itens.configure(app)
lists.configure(app)
people.configure(app)
admin.configure(app)
db.configure(app)