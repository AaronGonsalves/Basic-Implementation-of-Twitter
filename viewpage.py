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

username=''
prevsearch=''
tweet_or_user = ''

class ViewPage(webapp2.RequestHandler):
	def get(self):
		global username
		global prevsearch
		global tweet_or_user
		username = self.request.GET.get('username')
		prevsearch = self.request.GET.get('prevsearch')
		tweet_or_user = self.request.GET.get('tou')

		database = ndb.Key('MyUserDatabase',username).get()
		tweetlist=[]
		count=0
		for x in database.tweets:
			if(count<50):
				tweetlist.append(x)
				count=count+1

		currusername = ndb.Key('MyUser',users.get_current_user().user_id()).get().username
		curruser = ndb.Key('MyUserDatabase',currusername).get()

		follow = False
		for x in curruser.following:
			if(x==username):
				follow=True
				break

		follow_text=''
		if(currusername==username):
			follow_text='Home'
		elif(follow):
			follow_text='Unfollow'
		else:
			follow_text='Follow'

		empty = tweetlist==[]
		display = currusername!=username

		template_values={
			'user' : database,
			'tweetlist' : tweetlist,
			'follow_text' : follow_text,
			'display_follow' : display,
			'empty' : empty
		}

		template = JINJA_ENVIRONMENT.get_template('viewpage.html')
		self.response.write(template.render(template_values))

	def post(self):
		if(self.request.get('button')=='Home'):
			self.redirect('/')
		elif(self.request.get('button')=='Back'):
			if(tweet_or_user=='tweet'):
				self.redirect('/searchtweet?searchtweet='+prevsearch)
			else:
				self.redirect('/searchuser?searchname='+prevsearch)
		elif(self.request.get('button')=='Download'):
			database = ndb.Key('MyUserDatabase',username).get()
			collection = ndb.Key('BlobCollection',1).get()
			index = int(self.request.get('index'))
			blobkey = database.tweets[index].blobkey
			collection.downloadblob = blobkey
			collection.put()
			self.redirect('/download')
		else:
			database = ndb.Key('MyUserDatabase',username).get()
			currusername = ndb.Key('MyUser',users.get_current_user().user_id()).get().username
			curruserdatabase = ndb.Key('MyUserDatabase',currusername).get()

			if(self.request.get('button')=='Follow'):
				curruserdatabase.following.append(username)
				database.followers.append(currusername)
			elif(self.request.get('button')=='Unfollow'):
				curruserdatabase.following.remove(username)
				database.followers.remove(currusername)

			curruserdatabase.put()
			database.put()
			self.redirect('/')
