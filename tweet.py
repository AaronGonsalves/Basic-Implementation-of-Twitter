from google.appengine.ext import ndb

class Tweet(ndb.Model):
	text = ndb.StringProperty()
	time = ndb.DateTimeProperty(auto_now_add=True)
	blobkey = ndb.BlobKeyProperty()

