import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
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

tweetlist=[]

class SearchTweet(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		searchtweet = self.request.GET.get('searchtweet')
		totaldatabase = MyUserDatabase.query().fetch()
		global tweetlist
		tweetlist = []
		for user in totaldatabase:
			for tw in user.tweets:
				if(searchtweet in (tw.text)):
					temp=[]
					temp.append(tw)
					temp.append(user.username)
					tweetlist.append(temp)
		tweetlist.sort(key=lambda x: x[0].time, reverse=True)

		template_values={
			'tweetlist' : tweetlist,
			'tweet' : searchtweet
		}

		template = JINJA_ENVIRONMENT.get_template('searchtweet.html')
		self.response.write(template.render(template_values))

	def post(self):
		if(self.request.get('button')=='Home'):
			self.redirect('/')
		elif(self.request.get('button')=='Search Again'):
			tweet = self.request.get('searchtweet')
			self.redirect('/searchtweet?searchtweet='+tweet)
		elif(self.request.get('button')=='Download'):
			collection = ndb.Key('BlobCollection',1).get()
			index = int(self.request.get('index'))
			blobkey = tweetlist[index][0].blobkey
			collection.downloadblob = blobkey
			# imageurl = images.get_serving_url(blobkey, secure_url=True)
			collection.put()
			self.redirect('/download')
