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

class ViewTimeline(webapp2.RequestHandler):
	def get(self):
		myuser = ndb.Key('MyUser', users.get_current_user().user_id()).get()
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
			collection.downloadblob = blobkey
			collection.put()
			self.redirect('/download')

		template_values={
			'list' : finaltweetlist,
			'empty' : empty
		}

		template = JINJA_ENVIRONMENT.get_template('viewtimeline.html')
		self.response.write(template.render(template_values))

	def post(self):
		if(self.request.get('button')=='Home'):
			self.redirect('/')