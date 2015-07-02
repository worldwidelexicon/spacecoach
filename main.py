import datetime
import json
import math
import os
import string
import types
import urllib
import urllib2
import webapp2
import wsgiref.handlers

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.runtime import apiproxy_errors
from google.appengine.api.labs import taskqueue

from spacecoach import spacecoach

def render(template_name, data):
    path = os.path.join(os.path.dirname(__file__), template_name)
    return template.render(path, data)
    
class EngineData(db.Model):
    email = db.StringProperty(default='')
    test_date = db.StringProperty(default='')
    engine_type = db.StringProperty(default='')
    propellant = db.StringProperty(default='')
    specific_impulse = db.FloatProperty(default=0)
    power = db.FloatProperty(default=0)
    thrust = db.FloatProperty()
    efficiency = db.FloatProperty()
    url = db.StringProperty(default='')
    
class EngineDataHandler(webapp2.RequestHandler):
    def get(self):
        html = """
        <form action=/enginedata method=post>
        <table>
        <tr><td>Secret</td><td><input type=text name=secret></td></tr>
        </table>
        </form>
        """
        self.response.out.write(html)
    def post(self):
        secret = self.request.get('secret')
        email = self.request.get('email')
        test_date = self.request.get('test_date')
        engine_type = self.request.get('engine_type')
        propellant = self.request.get('propellant')
        specific_impulse = float(self.request.get('specific_impulse'))
        power = float(self.request.get('power'))
        thrust = float(self.request.get('thrust'))
        efficiency = float(self.request.get('efficiency'))
        url = self.request.get('url')
        if len(email) > 4 and len(test_date) > 8 and len(engine_type) > 0 and len (propellant) > 0 and secret == 'littlebirdy':
            data = EngineData()
            data.email = email
            data.test_date = test_date
            data.engine_type = engine_type
            data.propellant = propellant
            data.specific_impulse = specific_impulse
            data.power = power
            data.thrust = thrust
            data.efficiency = efficiency
            data.url = url
            data.put()
            # serve data accepted message, display input form again
        else:
            self.error(400)
            # serve invalid data page

class PageServer(webapp2.RequestHandler):
    def get(self):
        dry_mass = self.request.get('dry_mass')
        if len(dry_mass) > 0:
            dry_mass = float(dry_mass)
        else:
            dry_mass = 40000
        water_cost = self.request.get('water_cost')
        if len(water_cost) > 0:
            water_cost = float(water_cost)
        else:
            water_cost = 1700
        water_delivered = self.request.get('water_delivered')
        if len(water_delivered) > 0:
            water_delivered = int(water_delivered)
        else:
            water_delivered = 40000
        leo_cost = self.request.get('leo_cost')
        if len(leo_cost) > 0:
            leo_cost = float(leo_cost)
        else:
            leo_cost = 1700
        crew_cost = self.request.get('crew_cost')
        if len(crew_cost) > 0:
            crew_cost = float(crew_cost)
        else:
            crew_cost = 105000000
        fabrication_cost = self.request.get('fabrication_cost')
        if len(fabrication_cost) > 0:
            fabrication_cost = float(fabrication_cost)
        else:
            fabrication_cost = 200000000
        num_missions = self.request.get('num_missions')
        if len(num_missions) > 0:
            num_missions = int(num_missions)
        else:
            num_missions = 10
        s = spacecoach(num_missions=num_missions,fabrication_cost=fabrication_cost,mass=dry_mass, water_cost=water_cost, crew_cost=crew_cost,
                       leo_cost=leo_cost, water_delivered=water_delivered)
        self.response.out.write(render('graph_template.html', s.template_data))

app = webapp2.WSGIApplication([("/", PageServer)], debug=True)
