from google.appengine.ext import ndb

class Utenti(ndb.Model):
    codice = ndb.StringProperty(required=True, indexed=True)
    nome = ndb.StringProperty(required=True)
    cognome = ndb.StringProperty(required=True)
    autorizzazione = ndb.StringProperty()

class Accessi(ndb.Model):
    codice = ndb.StringProperty(required=True)
    nome = ndb.StringProperty(required=True)
    cognome = ndb.StringProperty(required=True)
    autorizzazione = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(required=True, indexed=True)
    datatemp = ndb.IntegerProperty(required=True)
    anomalia = ndb.BooleanProperty(required=True)