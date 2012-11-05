__author__ = 'miracledelivery'

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os, re
html_template =  os.path.join(os.path.dirname(__file__), 'templates/sql_tools.html' )
SELECT_RE = (r"\s*?(?P<select>SELECT.*?)"
             r"\s*?(?P<from>FROM.*?)"
             r"\s*?(?P<join>JOIN.*?)?"
             r"\s*?(?P<where>WHERE.*?)?"
             r"\s*?(?P<groupby>GROUP\sBY.*?)?"
             r"\s*?(?P<orderby>ORDER\sBY.*?)?$")

def process_group(raw_sql, line_width, kawaii):
    if raw_sql:
        words = raw_sql.split()
        group = 0
        sql_lines = ['']
        for word in words:
            sql_line = sql_lines[group]
            if len(sql_line) + len(word) < line_width-1:
                sql_lines[group] += word
                sql_lines[group] += ' '
            else:
                sql_lines.append(word + ' ')
                group += 1

        sql_lines[0] = '"' + sql_lines[0] + '"'

        converted_sql = sql_lines[0] + '\n'
        for sql_line in sql_lines[1:]:
            converted_sql += '+ "' + sql_line + '"\n'
        return converted_sql

def sql_converter(raw_sql, line_width=60, kawaii=False):
    select_pattern = re.compile(SELECT_RE, re.IGNORECASE | re.DOTALL)
    results = select_pattern.match(raw_sql)
    if results:
        converted_sql = []
        for result in filter(lambda a: a!=None, results.groups()):
            converted_sql.append(process_group(result, line_width, kawaii))
        return '+ '.join(converted_sql)

class MainHandler(webapp.RequestHandler):
    def render(self, **values):
        self.response.out.write(template.render(html_template, values))

    def get(self):
        self.render()

    def post(self):
        raw_sql = self.request.get("sql_strings")
        pretty_sql = sql_converter(raw_sql).upper()
        self.render(pretty_sql=pretty_sql, raw_sql=raw_sql)


#print sql_converter('select * from nds.nds_link where link_id = 12345 and seq_num = 1 and tile_num = 10 and nndb_id is not null order by link_id')

app = webapp.WSGIApplication([('/', MainHandler)], debug=True)