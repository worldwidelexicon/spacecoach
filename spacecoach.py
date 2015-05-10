#
# Spacecoach parametric model
# Brian S McConnell <bsmcconnell@gmail.com>, www.spacecoach.org
#
# This Python program models mission costs as a function of delta V, specific impulse,
# and a number of other factors. You can use this to estimate operating costs and test various
# assumptions about engine performance, the impact of in situ resource utilization, and
# cost savings due to leaving part of the hull at the destination.
#
# USAGE:
#
# s = spacecoach()
# data = s.data
# costs = s.costs
# highcharts_data = s.highcharts
#
# NOTE you can override the default values if you want. On initialization, the class will
# generate data that can be plotted graphically. Each series graphs the propellant ratio (to dry hull)
# as a function of delta V for specific impulse ranging from 1000s to 5000s (you can expand the range
# if you want). For each Isp value, it also graphs the propellant ratio for inbound ISRU, versus all
# water supplied from Earth, to show the impact of partial ISRU on mission costs.
#

import math
import os
import string

class spacecoach():
    def __init__(self, mass = 40000, low_isp = 1000, high_isp = 5000, low_dv = 1000, high_dv = 30000, interval = 5000, leo_cost=1700.0,
                 water_cost = 1700.0, num_missions=10, crew_cost=105000000, fabrication_cost = 200000000):
        self.dry_mass = mass
        self.low_isp = low_isp
        self.high_isp = high_isp
        self.low_dv = low_dv
        self.high_dv = high_dv
        self.leo_cost = leo_cost
        self.water_cost = water_cost
        self.eml2_dv = 7000
        self.data = None
        self.costs = None
        self.highcharts = None
        self.num_missions = num_missions
        self.crew_cost = crew_cost
        self.fabrication_cost = fabrication_cost
        self.missions = [
            {'name':'NEO', 'dv':3000},
            {'name':'cislunar', 'dv':5000},
            {'name':'mars ISRU inbound', 'dv':7500},
            {'name':'ceres ISRU inbound', 'dv':12500},
            {'name':'mars', 'dv':15000},
            {'name':'venus', 'dv':20000},
            {'name':'ceres', 'dv':25000}]
        self.data = self.generate_data(low_isp = low_isp, high_isp = high_isp, low_dv = low_dv,
                                        high_dv = high_dv, interval = interval)
        self.generate_html()
        
    def generate_data(self, low_isp = 1000, high_isp = 5000, low_dv = 1000, high_dv = 30000, interval = 500):
        data = list()
        for m in self.missions:
            dv = m['dv']
            isp = low_isp
            values = list()
            while isp <= high_isp:
                mr = math.pow(2.718, (dv / (9.81 * isp)))
                pr = mr - 1.0
                per_kg = self.leo_cost * math.pow(2.718, (self.eml2_dv / (9.81 * isp)))
                per_kg_water = per_kg * (self.water_cost / self.leo_cost)
                ship = (self.fabrication_cost + (self.dry_mass * per_kg)) / self.num_missions
                propellant = (self.dry_mass * pr) * per_kg_water
                crew = self.crew_cost
                total = ship + propellant + crew
                values.append(dict(
                    isp = isp,
                    mr = mr,
                    pr = pr,
                    per_kg = per_kg,
                    per_kg_water = per_kg_water,
                    ship = ship,
                    propellant = propellant,
                    crew = crew,
                    total = total,
                ))
                isp += 100
            data.append(dict(
                dv = dv,
                name = m['name'],
                values = values,
            ))
        return data
    
    def generate_html(self):
        chart_data = u''
        row = 1
        for rows in self.data:
            chart_data += '{'
            chart_data += 'name: "' + rows['name'] + ' ' + str(rows['dv']) + ' m/s", '
            chart_data += 'data: ['
            col = 1
            values = rows['values']
            for cols in values:
                chart_data += '[' + str(cols['isp']) + ',' + str(cols['total']) + ']'
                if col < len(values):
                    chart_data += ','
                col += 1
            chart_data += ']}'
            if row < len(self.data):
                chart_data += '\n,'
            row += 1
        subtitle = str(self.dry_mass) + ' kg dry hull, ' + str(self.num_missions) + ' mission lifetime, $' + str(int(self.leo_cost)) + '/kg equip/crew to LEO, $' + str(int(self.water_cost)) + '/kg water to LEO, $' + str(self.fabrication_cost) + ' ship fabrication cost'
        data = dict(
            subtitle = subtitle,
            series_data = chart_data,
        )
        self.template_data = data
        
        #f = open('graph.html', 'w')
        #f.write(html)
        #f.close()
        
        #for mission in self.data:
        #    name = mission['name']
        #    r = open('area_template.html','r')
        #    html = r.read()
        #    r.close()
        #    
        #    chart_data = ''
        #    
        #    chart_data += '{'
        #    values = mission['values']
        #    
        #    chart_data += 'name: \'Ship Fabrication & Delivery\', '
        #    chart_data += 'data: ['
        #    
        #    col = 1
        #    for cols in values:
        #        chart_data += str(cols['ship'])
        #        if col < len(values):
        #            chart_data += ','
        #        else:
        #            chart_data += ']}'
        #        col += 1
        #    
        #    chart_data += ','
        #    
        #    chart_data += '{name: \'Crew & CRV Launch\', '
        #    chart_data += 'data: ['
        #    
        #    col = 1
        #    for cols in values:
        #        chart_data += str(cols['crew'])
        #        if col < len(values):
        #            chart_data += ','
        #        else:
        #            chart_data += ']}'
        #        col += 1
        #
        #    chart_data += ','
        #    
        #    chart_data += '{name: \'Water & Water Equivalent Material\', '
        #    chart_data += 'data: ['
        #    
        #    col = 1
        #    for cols in values:
        #        chart_data += str(cols['propellant'])
        #        if col < len(values):
        #            chart_data += ','
        #        else:
        #            chart_data += ']}'
        #        col += 1
        #
        #    html = string.replace(html, '{{ data }}', chart_data)
        #    
        #    x_axis = '['
        #    col = 1
        #    for cols in values:
        #        x_axis += str(cols['isp'])
        #        if col < len(values):
        #            x_axis += ','
        #        else:
        #            x_axis += ']'
        #        col += 1
        #        
        #    html = string.replace(html, '{{ categories }}', x_axis)
        #    
        #    html = string.replace(html, '{{ subtitle }}', 'EML2 : ' + string.capitalize(mission['name']) + ' ' + str(mission['dv']) + ' m/s delta-v')
        #    
        #    filename = string.replace(name,' ','_')
        #    
        #    f = open(filename + '.html', 'w')
        #    f.write(html)
        #    f.close()
