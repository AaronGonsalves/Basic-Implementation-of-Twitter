import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from myuser import MyUser
from myuser import MyUserDatabase
from tweet import Tweet

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

index=-1

class EditTweet(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		global index
		index = int(self.request.GET.get('index'))
		myuser = ndb.Key('MyUser',users.get_current_user().user_id()).get()
		database = ndb.Key('MyUserDatabase',myuser.username).get()
		text = database.tweets[index].text

		template_values={
			'text' : text
		}
		template = JINJA_ENVIRONMENT.get_template('edittweet.html')
		self.response.write(template.render(template_values))

	def post(self):
		myuser = ndb.Key('MyUser',users.get_current_user().user_id()).get()
		database = ndb.Key('MyUserDatabase',myuser.username).get()

		if(self.request.get('button')=='Submit'):
			new_text = self.request.get('text')
			database.tweets[index].text=new_text
			database.put()
			self.redirect('/tweetPost')
		elif(self.request.get('button')=='Cancel'):
			self.redirect('/tweetPost')
		elif(self.request.get('button')=='Delete'):
			del database.tweets[index]
			database.put()
			self.redirect('/tweetPost')

		




