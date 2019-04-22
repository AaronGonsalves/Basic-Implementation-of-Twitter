from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload = self.get_uploads()[0]
		collection = ndb.Key('BlobCollection', 1).get()
		collection.blobs.append(upload.key())
		collection.put()
		self.redirect('/tweetPost')
