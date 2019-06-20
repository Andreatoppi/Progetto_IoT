# -*- encoding: utf8 -*-
import appengine_config
import os
import logging
from flask import Flask, render_template, app, request, url_for, make_response, session, redirect,jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, validators, BooleanField, SelectField
from wtforms.validators import DataRequired
from app.models import Utenti, Accessi
from flask_restful import Resource, reqparse, Api
from flask_wtf.csrf import CSRFProtect
import datetime
import time

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'ciao'

#gestione e validazione delle form
class MyForm(FlaskForm):
    codice = StringField('codice', [validators.DataRequired()])
    nome = StringField('nome', validators=[DataRequired()])
    cognome = StringField('cognome', [validators.DataRequired()])
    autorizzazione = SelectField(u'autorizzazione', choices=[('True','True'), ('False','False')])

api = Api(app)

@app.route('/', methods=['GET'])
def home():
    return app.send_static_file('index.html')

@app.route('/inserisci', methods=['GET'])
def inserisci():
    form = MyForm()
    if form.validate_on_submit():
        codice = request.form['codice']
        nome = request.form['nome']
        cognome = request.form['cognome']
    return render_template('inserimento.html', form=form)

@app.route('/inserisci', methods=['POST'])
def post():
    codice = request.form['codice']
    nome = request.form['nome']
    cognome = request.form['cognome']
    autorizzazione = request.form['autorizzazione']
    utente = Utenti.get_by_id(codice)
    if utente:
        return ('Codice utente gia esistente')
    utente = Utenti(id=codice,
                    codice=codice,
                    nome=nome,
                    cognome=cognome,
                    autorizzazione=autorizzazione)
    utente.put()
    return redirect(url_for('home'))

@app.route('/visualizza', methods=['GET'])
def get_tutti_utenti():

    handlers=[]
    utenti = Utenti.query().fetch()
    for utente in utenti:
         read = read = [(utente.codice), (utente.nome), (utente.cognome), (utente.autorizzazione)]
         handlers.append(read)

    if handlers is not None:
        return render_template('utenti.html', handlers=handlers)

@app.route('/accessi', methods=['GET'])
def get_access():
    accessi = Accessi.query().order(-Accessi.timestamp).fetch()
    output = []
    for accesso in accessi:
        read = [(accesso.codice),
                (accesso.nome),
                (accesso.cognome),
                (accesso.autorizzazione),
                (accesso.timestamp),
                (accesso.datatemp),
                (accesso.anomalia)
        ]
        output.append(read)
    if output:
        return render_template('accessi.html', handlers=output)
    return jsonify({'data': []})

@app.route('/ultimo', methods=['GET'])
def get_ultimo():
    accessi = Accessi.query().order(-Accessi.timestamp).fetch(1)
    output = []
    for accesso in accessi:
        read = {'codice': accesso.codice,
                'nome' : accesso.nome,
                'cognome': accesso.cognome,
                'autorizzazione': accesso.autorizzazione,
                'timestamp' : accesso.timestamp,
                'fascia_orario': accesso.datatemp
        }
        output.append(read)
    if output:
        return jsonify(output)
    return jsonify({'data': []})

@app.route('/anomalie', methods=['GET'])
def get_anomalies():
    accessi = Accessi.query(Accessi.anomalia == True).fetch()
    output = []
    for accesso in accessi:
        read = [(accesso.codice),
                (accesso.nome),
                (accesso.cognome),
                (accesso.autorizzazione),
                (accesso.timestamp),
                (accesso.datatemp),
                (accesso.anomalia)
        ]
        output.append(read)
    if output:
        return render_template('anomalie.html', handlers=output)
    return jsonify({'data': []})

@app.route('/permessi', methods=['GET'])
def cambiaPermessi():
    handlers=[]
    utenti = Utenti.query().fetch()
    for utente in utenti:
         read = [(utente.codice), (utente.nome), (utente.cognome), (utente.autorizzazione)]
         handlers.append(read)
    
    return render_template('permessi.html', handlers=handlers)

@app.route('/permessi/<codice>', methods=['POST'])
def cambiaPermesso(codice):
    utente = Utenti.get_by_id(codice)    
    if not utente:
        return ('Utente non esistente')
    if utente.autorizzazione == 'True':
        utente = Utenti(id=utente.codice,
                        codice=utente.codice,
                        nome=utente.nome,
                        cognome=utente.cognome,
                        autorizzazione='False')
    else:
        utente = Utenti(id=utente.codice,
                        codice=utente.codice,
                        nome=utente.nome,
                        cognome=utente.cognome,
                        autorizzazione='True')
    utente.put()
    return redirect(url_for('cambiaPermessi'))