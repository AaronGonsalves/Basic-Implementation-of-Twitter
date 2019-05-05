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

class Edit(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		user = users.get_current_user()
		myuser = ndb.Key('MyUser',user.user_id()).get();
		database = None

		firstTime = myuser.username == None
		if(not firstTime):
			database=ndb.Key('MyUserDatabase',myuser.username).get()

		template_values = {
			'firstTime' : firstTime,
			'database' : database,
			'myuser' : myuser
		}

		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'

		user = users.get_current_user()
		myuser = ndb.Key('MyUser',user.user_id()).get()
		firstTime = myuser.username == None
		database=None
		if(not firstTime):
			database=ndb.Key('MyUserDatabase',myuser.username).get()
		warning_text=''
		warning = False

		if(firstTime):
			if self.request.get('button') == 'Update' :

				username = self.request.get('users_username').lower()
				name = self.request.get('users_name').lower()
				profile = self.request.get('users_profile').lower()

				query = MyUser.query(MyUser.username==username).fetch()
				warning=True
				if(username==' none ' or username=='' or username==None):
					warning_text='Enter a valid username'
				elif(query!=[] and query!=None):
					warning_text='This username is already taken'
				elif(name==' none ' or name=='' or name==None):
					warning_text='Please enter a valid name'
				elif(profile==' none ' or profile=='' or profile==None):
					warning_text='Please enter a valid profile'
				elif(len(profile)>280):
					warning_text='Max limit of profile is 280 characters'
				else:
					warning=False
					myuser.username = username
					new_database = MyUserDatabase(id=username,username=username,profile=profile,name=name)
					myuser.put()
					new_database.put()
					self.redirect('/')

			elif self.request.get('button') == 'Cancel' :
				warning = True;
				warning_text='Please enter your details as it\'s your first time'

		else:
			if(self.request.get('button') == 'Update') :
				database = ndb.Key('MyUserDatabase',myuser.username).get()
				database.profile = self.request.get('users_profile')
				database.name = self.request.get('users_name')
				database.put()
				self.redirect('/')
			elif(self.request.get('button') == 'Cancel'):
				self.redirect('/')

		template_values={
			'firstTime' : firstTime,
			'database' : database,
			'myuser' : myuser,
			'warning' : warning,
			'warning_text' : warning_text,
			'none' : ''
		}

		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(template_values))
