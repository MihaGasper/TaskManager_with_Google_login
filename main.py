#!/usr/bin/env python
import os
import jinja2
import webapp2
from google.appengine.api import users
from models import Inputs


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):

        user = users.get_current_user()

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            params = {"logiran": logiran, "logout_url": logout_url, "user": user}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "login_url": login_url, "user": user}

        self.render_template("hello.html", params=params)


class RezultatHandler(BaseHandler):
    def post(self):
        input1 = self.request.get("input1")
        input2 = self.request.get("input2")
        input3 = self.request.get("input3")

        inputs = Inputs(input1=input1, input2=input2, input3=input3)

        inputs.put()


        self.render_template("rezultat.html")

class SeznamHandler(BaseHandler):
    def get(self):
        seznam = Inputs.query(Inputs.izbrisan == False).fetch()
        params = {"seznam": seznam}
        self.render_template("seznam.html", params=params)


class PosameznoHanedler(BaseHandler):
    def get(self, inputs_id):
        inputs = Inputs.get_by_id(int(inputs_id))
        params = {"inputs": inputs}
        self.render_template("posamezno.html", params=params)


class UrediHandler(BaseHandler):
    def get(self, inputs_id):
        inputs = Inputs.get_by_id(int(inputs_id))
        params = {"inputs": inputs}
        self.render_template("uredi.html", params=params)

    def post(self, inputs_id):
        input1 = self.request.get("input1")
        input2 = self.request.get("input2")
        input3 = self.request.get("input3")

        inputs = Inputs(input1=input1, input2=input2, input3=input3).get_by_id(int(inputs_id))

        inputs.input1 = input1
        inputs.input2 = input2
        inputs.input3 = input3

        inputs.put()

        self.redirect_to("seznam")


class IzbrisiHandler(BaseHandler):
    def get(self, inputs_id):
        inputs = Inputs.get_by_id(int(inputs_id))
        params = {"inputs": inputs}
        self.render_template("izbrisi.html", params=params)

    def post(self, inputs_id):
        inputs = Inputs.get_by_id(int(inputs_id))
        inputs.izbrisan = True
        inputs.put()
        self.redirect_to("seznam")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/seznam', SeznamHandler, name="seznam"),
    webapp2.Route('/inputs/<inputs_id:\d+>', PosameznoHanedler),
    webapp2.Route('/inputs/<inputs_id:\d+>/uredi', UrediHandler),
    webapp2.Route('/inputs/<inputs_id:\d+>/izbrisi', IzbrisiHandler),
], debug=True)
