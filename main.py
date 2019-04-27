import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
import os
from myuser import MyUser
from myuser import MyUserDatabase
from edit import Edit
from tweetPost import TweetPost
from searchuser import SearchUser
from searchtweet import SearchTweet
from viewpage import ViewPage
from edittweet import EditTweet
from blobcollection import BlobCollection
from uploadhandler import UploadHandler
from downloadhandler import DownloadHandler
from viewfollow import ViewFollow
from google.appengine.api import images

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-type'] = 'text/html'

		url=''
		url_string=''
		welcome='Welcome back'
		edit_url='/edit'
		user = users.get_current_user()
		myuser = None
		finaltweetlist=[]
		empty=[]
		# global urlimg
		collection_key = ndb.Key('BlobCollection', 1)
		collection = collection_key.get()
		if collection == None:
			collection = BlobCollection(id=1)
			collection.put()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'

			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()

			if myuser!=None:
				database = ndb.Key('MyUserDatabase', myuser.username).get()
				totaltweetlist=[]
				totaltweetlist+= database.tweets

				for x in database.following:
					database_other = ndb.Key('MyUserDatabase',x).get()
					totaltweetlist+= database_other.tweets

				totaltweetlist.sort(key=lambda x: x.time, reverse=True)
				finaltweetlist=[]
				count=0
				for x in totaltweetlist:
					if(count==50):
						break
					else:
						finaltweetlist.append(x)
						count=count+1

				empty = finaltweetlist==[]

				if(self.request.get('button')=='Download'):
					collection = ndb.Key('BlobCollection',1).get()
					index = int(self.request.get('index'))
					blobkey = finaltweetlist[index].blobkey
					# urlimg = images.get_serving_url(blobkey, secure_url=True)
					collection.downloadblob = blobkey
					collection.put()
					self.redirect('/download')

			if myuser==None:
				myuser = MyUser(id=user.user_id(),email_id=user.email())
				myuser.put()
				self.redirect('/edit')
		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'

		template_values = {
			'url' : url,
			'url_string' : url_string,
			'user' : user,
			'welcome' : welcome,
			'edit_url' : edit_url,
			'myuser' : myuser,
			'list' : finaltweetlist,
			'empty' : empty
			# 'urlimg' : urlimg
		}

		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

	def post(self):
		if(self.request.get('button')=='Search User'):
			name = self.request.get('searchname')
			self.redirect('/searchuser?searchname='+name)
		elif(self.request.get('button')=='Search Tweet'):
			tweet = self.request.get('searchtweet')
			self.redirect('/searchtweet?searchtweet='+tweet)

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/edit', Edit),
	('/tweetPost', TweetPost),
	('/searchuser', SearchUser),
	('/searchtweet', SearchTweet),
	('/viewpage', ViewPage),
	('/edittweet', EditTweet),
	('/upload', UploadHandler),
	('/download', DownloadHandler),
	('/viewfollow',ViewFollow)
], debug=True)
