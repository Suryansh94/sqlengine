
# from __future__ import braces
import sys
import os
import sqlparse
import meta
import settings
import read_data
import select
# query= sqlparse.format(command,keyword_case="upper")

settings.init()
meta.read_meta_data('metadata.txt')
read_data.read()
cmd=sys.argv[1]
query= sqlparse.format(cmd,keyword_case="upper")

# print query
# res= sqlparse.parse(query)
# print res[0]

# query=query.replace(',',' ').replace(';','')
# print query
# check if its select query
if query.split()[0]=='SELECT':
	select.get_result(query)
else:
	print "Please input valid string"
