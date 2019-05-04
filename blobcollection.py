from google.appengine.ext import ndb

class BlobCollection(ndb.Model):
	blobs = ndb.BlobKeyProperty(repeated=True)
	# downloadblob = ndb.BlobKeyProperty();
