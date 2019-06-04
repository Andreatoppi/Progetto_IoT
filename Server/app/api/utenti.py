# -*- encoding: utf8 -*-
from flask_restful import Resource, reqparse

from app.flask_app import api
from app.models import Utenti, Accessi
import datetime
import time
import numpy as np
import statistics, os
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect

parser = reqparse.RequestParser()
parser.add_argument('codice', type=str, required=True, location='json')
parser.add_argument('nome', type=str, required=True, location='json')
parser.add_argument('cognome', type=str, required=True, location='json')
parser.add_argument('autorizzazione', type=str, location='json')


class UtenteGetApi(Resource):
    def get(self, codice):
        utenti = Utenti.query(Utenti.codice==codice).fetch(1)
        if not utenti:
            return {'message': 'The resource does not exist.'}, 404
        utente = utenti[0]
        return {'message': 'Resource retrieved correctly.',
                'data': {
                        'codice': utente.codice,
                        'nome': utente.nome,
                        'cognome': utente.cognome,
                        'autorizzazione': utente.autorizzazione
                        }
                }

api.add_resource(UtenteGetApi, '/api/v0.1/utente/<string:codice>')

class AccessoApi(Resource):
    def post(self,codice):
        # if not request.json or 'codice' not in request.json:
        #     abort(400)

        # #prendo il numero della tessera
        # codice = request.json['codice']

        utenti = Utenti.query(Utenti.codice==codice).fetch(1)
        if not utenti:
            return {'message': 'CODICE SCONOSCIUTO'}
        utente = utenti[0]

        accessi = Accessi.query().fetch()
        if len(accessi) > 3:
            media, varianza = training()
        else:
            media = 0
            varianza = 1

        if utente.autorizzazione=='True':
            prob = registra_acceso(utente, media, varianza)
            return {'nome': utente.nome,
                    'cognome': utente.cognome,
                    'message' : 'ACCESSO CONSENTITO',
                    'media' : media,
                    'varianza' : varianza,
                    'prob' : prob
                    }
        prob = registra_acceso(utente, media, varianza)
        return {'nome': utente.nome,
                'cognome': utente.cognome,
                'message' : 'ACCESSO NEGATO',
                'media' : media,
                'varianza' : varianza,
                'prob' : prob
                }

api.add_resource(AccessoApi, '/api/v0.1/accesso/<string:codice>')

def registra_acceso(utente, media, varianza):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(time.time())
    fascia_orario = int(datetime.datetime.fromtimestamp(ts).strftime('%H'))

    anomalia, prob = verificaAnomalia(fascia_orario, media, varianza)

    accesso = Accessi(codice=utente.codice,
                    nome=utente.nome,
                    cognome=utente.cognome,
                    autorizzazione=utente.autorizzazione,
                    timestamp=st,
                    datatemp=fascia_orario,
                    anomalia=anomalia)
    accesso.put()
    return prob

#variabili per la gaussiana
soglia = 0.2

#definisco la gaussiana
def gaussian(x, mu, sig):
    if sig == 0:
        return 1
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def average(list):
    return sum(list)/float(len(list))

def training():

    vettore_accessi = []
    # rimpie vettore degli orari
    accessi = Accessi.query().order(Accessi.datatemp).fetch(projection=[Accessi.datatemp])
    for accesso in accessi:
        vettore_accessi.append(accesso.datatemp)

    mean_access = average(vettore_accessi)
    sig_access = statistics.stdev(vettore_accessi)

    return  mean_access, sig_access

def verificaAnomalia(fascia_orario, media, dev):
    #verifica se c'è anomalia

    prob = gaussian(fascia_orario, media, dev)

    if prob > soglia:
        return False, prob
    else:
        return True, prob