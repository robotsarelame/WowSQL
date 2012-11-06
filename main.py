__author__ = 'miracledelivery'

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os, re

# ----------------------------------------------------------------------------------------------------> global variables
HTML_TEMPLATE =  os.path.join(os.path.dirname(__file__), 'templates/sql_tools.html' )

# regular expression for matching basic SELECT queries
SELECT_RE = (r"""
                \s*?                               # spaces/tabs/new lines before the SELECT statement are valid
                                                   # --> first group in detail:
                (?P<select>                        # initialize named group with the 'select' name
                SELECT                             # matches 'SELECT' (actual RegExp is called with re.IGNORECASE key)
                .*?)                               # matches any characters (lazy) before next match occurs
                                                   # --> end of first group
                \s*?(?P<from>FROM\s.*?)            # 'from' and following chars
                \s*?(?P<join>                      # 'join' group
                (?:INNER\s*?|                      # unnamed group initialization with JOIN modifiers
                LEFT\s*?(?:OUTER\s*?)?|            # 'LEFT' with optional 'OUTER' modifier
                RIGHT\s*?(?:OUTER\s*?)?|
                FULL\s*?(?:OUTER\s*?)?|
                CROSS\s*?)?                        # the whole unnamed group is optional (the '?' after group)
                JOIN\s.*?)?                        # end of 'JOIN' group. The very important here is
                                                   #   that JOIN and following groups are optional
                \s*?(?P<where>WHERE\s.*?)?         # 'WHERE' group
                \s*?(?P<groupby>GROUP\s*?BY\s.*?)?
                \s*?(?P<orderby>ORDER\s*?BY\s.*?)?
                $                                  # match to the end
                """)

# precompiled pattern, it's better to have one precompiled for better perfomance
SELECT_PATTERN = re.compile(SELECT_RE, re.IGNORECASE | re.DOTALL | re.VERBOSE)

# ----------------------------------------------------------------------------------------------------> global functions
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
    results = SELECT_PATTERN.match(raw_sql)
    if results:
        converted_sql = []
        for result in filter(lambda a: a is not None, results.groups()):
            converted_sql.append(process_group(result, line_width, kawaii))
        return '+ '.join(converted_sql)

# ------------------------------------------------------------------------------------------------------> global classes
class MainHandler(webapp.RequestHandler):
    def render(self, **values):
        self.response.out.write(template.render(HTML_TEMPLATE, values))

    def get(self):
        self.render()

    def post(self):
        raw_sql = self.request.get("sql_strings")
        pretty_sql = sql_converter(raw_sql)
        if pretty_sql:
            self.render(pretty_sql=pretty_sql.upper(), raw_sql=raw_sql)
        else:
            self.render(pretty_sql='DUMB!', raw_sql=raw_sql)

#print sql_converter('select * from nds.nds_link where link_id = 12345 and seq_num = 1 and tile_num = 10 and nndb_id is not null order by link_id')

app = webapp.WSGIApplication([('/', MainHandler)], debug=True)