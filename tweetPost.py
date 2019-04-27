import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import os
from myuser import MyUser
from myuser import MyUserDatabase
from tweet import Tweet
from google.appengine.api import images

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

class TweetPost(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		myuser = ndb.Key('MyUser',users.get_current_user().user_id()).get()
		database = ndb.Key('MyUserDatabase',myuser.username).get()
		collection = ndb.Key('BlobCollection',1).get()

		file_uploaded = len(collection.blobs)>0

		# if(self.request.get('button')=='Download'):
		# 	index = int(self.request.get('index'))
		# 	blobkey = database.tweets[index].blobkey
		# 	collection.downloadblob = blobkey
		# 	collection.put()
		# 	self.redirect('/download')

		template_values = {
			'database' : database,
			'upload_url' : blobstore.create_upload_url('/upload'),
			'file_uploaded' : file_uploaded
		}

		template = JINJA_ENVIRONMENT.get_template('tweetPost.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'

		myuser = ndb.Key('MyUser',users.get_current_user().user_id()).get()
		database = ndb.Key('MyUserDatabase',myuser.username).get()
		collection = ndb.Key('BlobCollection',1).get()
		string = self.request.get('users_tweet')
		# imageurl = ''
		tweet_post_flag = len(string)>280 or (len(string)<=0 and len(collection.blobs)==0)

		if(self.request.get('button')=='Back'):
			collection.blobs=[]
			collection.put()
			self.redirect('/')
		elif(self.request.get('button')=='Delete'):
			del database.tweets[int(self.request.get('index'))]
			database.put()
			collection.blobs=[]
			collection.put()
			self.redirect('/tweetPost')
		elif(self.request.get('button')=='Edit'):
			collection.blobs=[]
			collection.put()
			self.redirect('/edittweet?index='+str(int(self.request.get('index'))))
		elif(self.request.get('button')=='Post'):
			if(not tweet_post_flag):
				blobkey=None
				if(len(collection.blobs)>0):
					blobkey=collection.blobs[0]
					# imageurl = images.get_serving_url(blobkey, secure_url=True)
				collection.blobs=[]
				collection.put()
				new_tweet = Tweet(text=string,blobkey=blobkey)
				database.tweets.insert(0,new_tweet)
				database.put()
				self.redirect('/tweetPost')

		template_values={
			'string' : string,
			'database' : database
			# 'tweet_url' : imageurl
		}

		template = JINJA_ENVIRONMENT.get_template('tweetPost.html')
		self.response.write(template.render(template_values))
