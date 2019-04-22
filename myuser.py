from google.appengine.ext import ndb
from tweet import Tweet

class MyUser(ndb.Model):
	email_id = ndb.StringProperty()
	username = ndb.StringProperty()

class MyUserDatabase(ndb.Model):
	username = ndb.StringProperty()
	name = ndb.StringProperty()
	profile = ndb.StringProperty()
	tweets = ndb.StructuredProperty(Tweet, repeated=True)
	following = ndb.StringProperty(repeated=True)
	followers = ndb.StringProperty(repeated=True)