import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from myuser import MyUser
from myuser import MyUserDatabase

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

class ViewFollow(webapp2.RequestHandler):
	def get(self):
		view = self.request.get('view')
		myuser = ndb.Key('MyUser',users.get_current_user().user_id()).get()
		database = ndb.Key('MyUserDatabase',myuser.username).get()
		viewlist=[]
		displaytext=''
		if(view=='Followers'):
			viewlist=database.followers
			displaytext= 'You\'re being followed by'
			if(viewlist==[]):
				displaytext= 'You\'re not being followed by anyone'
		else:
			viewlist=database.following
			displaytext = 'You\'re following'
			if(viewlist==[]):
				displaytext= 'You\'re not following anyone'

		template_values={
			'viewlist' : viewlist,
			'displaytext' : displaytext,
			'view' : view
		}

		template = JINJA_ENVIRONMENT.get_template('viewfollow.html')
		self.response.write(template.render(template_values))

	def post(self):
		if(self.request.get('button')=='Back'):
			self.redirect('/')

