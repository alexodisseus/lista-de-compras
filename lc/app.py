import admin
#import shareholder
#import quote
#import report
#import closure
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
#report.configure(app)
#closure.configure(app)
Bootstrap(app)
people.configure(app)
admin.configure(app)
db.configure(app)