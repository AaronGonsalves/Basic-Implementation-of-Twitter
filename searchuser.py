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

class SearchUser(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		searchname = self.request.GET.get('searchname').lower()

		search = MyUserDatabase.query()

		totallist=search.fetch()
		searchlist=[]
		for user in totallist:
			if(user.username.startswith(searchname)):
				searchlist.append(user.username)

		template_values={
			'searchlist' : searchlist,
			'searchname' : searchname
		}

		template = JINJA_ENVIRONMENT.get_template('searchuser.html')
		self.response.write(template.render(template_values))

	def post(self):
		if(self.request.get('button')=='Home'):
			self.redirect('/')
		elif(self.request.get('button')=='Search Again'):
			name = self.request.get('searchname')
			self.redirect('/searchuser?searchname='+name)
