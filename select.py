import settings
import sqlparse
import string

def get_result(query):
	# That 'u' is part of the external representation of the string, meaning it's a Unicode string as opposed to a byte string.
	# It's not in the string, it's part of the type.
	query=query.replace(',',' ')
	query=query.replace(';',' ')
	tokens=query.split()
	# print query
	# res = sqlparse.split(query)
	# res = sqlparse.format(query, reindent=True, keyword_case='upper',strip_comments =True)
	# res=' '.join(res.split('\n'))
	# print res
	# stmt=res[0]
	# print stmt.tokens
	# print str(stmt.tokens[-1])
	contents={} # to get selected tables names,column names and conditions
	i=0
	keywords=['SELECT','FROM','WHERE']
	while i<len(tokens):
		word=tokens[i].strip()
		if word in keywords:
			i=i+1
			vals=[]
			while i<len(tokens) and tokens[i].strip() not in keywords:
				if len(tokens[i].strip())==0:
					i=i+1
				else:
					vals.append(str(tokens[i].strip()))
					i=i+1
			contents[word]=vals

	# print "select"
	# print contents['SELECT'],contents['FROM'],contents['WHERE']

	if 'FROM' not in contents.keys() or len(contents['SELECT'])==0 or len(contents['FROM'])==0:
		print 'Error'
		return

	for i in contents['FROM']:
		if i not in settings.tables.keys():
			print 'Invalid table name'
			return
	for item in contents['SELECT']:
		table_name=contents['FROM'][0]
		if item !='*' and item not in settings.tables[table_name]:
			print 'Invalid column name'
			return

	if len(contents['FROM'])==1:
		# single table
		table_name=contents['FROM'][0]
		result=settings.data[table_name]
		if 'WHERE' not in contents.keys():
			# one table involve
			if len(contents['SELECT'])==1:
				# It can be single column , aggregate function or *
				value=contents['SELECT'][0].strip()
				print value

				if '(' in value :
					# max() , min() , avg()
					# aggregate function
					func=value.split('(')[0]
					# print func
					attribute=value.split('(')[1].split(')')[0]
					# print attribute
					# print result
					index_of_attribute = settings.tables[table_name].index(attribute)
					# print index_of_attribute
					if func=='max' or func=='MAX':
						max_attribute=int(-1e9)
						for row in result:
							max_attribute=max(max_attribute,int(row[index_of_attribute-1]))
						print max_attribute
					if func=='min' or func=='MIN':
						min_attribute=int(1e9)
						for row in result:
							print row[index_of_attribute-1]
							min_attribute=min(min_attribute,int(row[index_of_attribute-1]))
						print min_attribute
					if func == 'sum' or func=='SUM':
						sum_attribute=int(0)
						for row in result:
							sum_attribute+=int(row[index_of_attribute-1])
						print sum_attribute
					if func=='avg' or func=='AVG':
						average=int(0)
						sum_attribute=int(0)
						cnt=len(result)
						for row in result:
							sum_attribute+=int(row[index_of_attribute-1])
						average=sum_attribute/cnt;
						print average
					if func=='distinct' or func=='DISTINCT':
						ans=[]
						for row in result:
							item=row[index_of_attribute-1]
							if item not in ans:
								ans.append(item)
						for item in ans:
							print item
				elif '*' in value :
					# star
					for i in range(len(settings.tables[table_name])-1):
						print settings.tables[table_name][i+1]," ",
					print '\n'
					for row in result:
						for item in row:
							print item,
						print '\n'
				else :
					# single column
					attribute_name=contents['SELECT'][0]
					index_of_attribute=settings.tables[table_name].index(attribute_name)-1
					for row in result:
						print row[index_of_attribute]

			else:
				# multiple columns in select statement
				columns=len(contents['SELECT'])
				index_of_attribute=[]
				for i in range(len(contents['SELECT'])):
					index_of_attribute.append(settings.tables[table_name].index(contents['SELECT'][i])-1)

				for i in index_of_attribute:
					print settings.tables[table_name][i+1],
				print '\n'
				for row in result:
					for i in index_of_attribute:
						print row[i],
					print '\n'


				# multiple aggregate functions


		else:
			# where present
			condition_list=contents['WHERE']
			updated_data=[]
			if 'AND' in condition_list:
			# more than one condition
				cond1=contents['WHERE'][0]
				operator=contents['WHERE'][1]
				cond2=contents['WHERE'][2]
				#temp1 has the results of applying cond1 on data
				temp1=[]

				if '>=' in cond1:
					C=cond1.split('>=')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=settings.data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])>=value:
							temp1.append(row)


				elif '<=' in cond1:
					C=cond1.split('<=')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=settings.data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])<=value:
							temp1.append(row)

				elif '<' in cond1:
					C=cond1.split('<')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=settings.data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])<value:
							temp1.append(row)

				elif '>' in cond1:
					C=cond1.split('>')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=settings.data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])>value:
							temp1.append(row)

				elif '=' in cond1:
					C=cond1.split('=')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=settings.data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])==value:
							temp1.append(row)


				#temp2 has the results of applying cond2 on data
				temp2=[]

				if '>=' in cond2:
					C=cond2.split('>=')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=settings.data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])>=value:
							temp2.append(row)


				elif '<=' in cond2:
					C=cond2.split('<=')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=settings.data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])<=value:
							temp2.append(row)

				elif '<' in cond2:
					C=cond2.split('<')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=settings.data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])<value:
							temp2.append(row)

				elif '>' in cond2:
					C=cond2.split('>')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=settings.data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])>value:
							temp2.append(row)

				elif '=' in cond2:
					C=cond2.split('=')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=settings.data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])==value:
							temp2.append(row)
				#final data is list of lists with all columns
				#kept global so that after condition is applied, project can be done only once
				updated_data=[]


				#now based on the condition get the finalData
				if operator=='AND':
					current_data=settings.data[table_name]

					for item in current_data:
						if item in temp1 and item in temp2:
							updated_data.append(item)

				elif operator=='OR':
					current_data=settings.data[table_name]

					for item in current_data:
						if item in temp1 or item in temp2:
							updated_data.append(item)

			else:
				cond=condition_list[0]
				if '>=' in cond:
					C=cond.split('>=')
					var=C[0].strip()
					value=int(C[1].strip())
					print var,value
					current_data=settings.data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:

						if int(row[attrIndex-1])>=int(value):
							updated_data.append(row)


				elif '<=' in cond:
					C=cond.split('<=')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])<=value:
							updated_data.append(row)

				elif '<' in cond:
					C=cond.split('<')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])<value:
							updated_data.append(row)

				elif '>' in cond:
					C=cond.split('>')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])>value:
							updated_data.append(row)

				elif '=' in cond:
					C=cond.split('=')
					var=C[0].strip()
					value=int(C[1].strip())

					current_data=data[table_name]
					#get the index of attribute
					attrIndex=settings.tables[table_name].index(var)-1
					for row in current_data:
						if int(row[attrIndex])==value:
							updated_data.append(row)

			# update result and do same process
			result=updated_data

			if len(contents['SELECT'])==1:
				# It can be single column , aggregate function or *
				value=contents['SELECT'][0].strip()
				print value

				if '(' in value :
					# max() , min() , avg()
					# aggregate function
					func=value.split('(')[0]
					# print func
					attribute=value.split('(')[1].split(')')[0]
					# print attribute
					# print result
					index_of_attribute = settings.tables[table_name].index(attribute)
					# print index_of_attribute
					if func=='max' or func=='MAX':
						max_attribute=int(-1e9)
						for row in result:
							max_attribute=max(max_attribute,int(row[index_of_attribute-1]))
						print max_attribute
					if func=='min' or func=='MIN':
						min_attribute=int(1e9)
						for row in result:
							print row[index_of_attribute-1]
							min_attribute=min(min_attribute,int(row[index_of_attribute-1]))
						print min_attribute
					if func == 'sum' or func=='SUM':
						sum_attribute=int(0)
						for row in result:
							sum_attribute+=int(row[index_of_attribute-1])
						print sum_attribute
					if func=='avg' or func=='AVG':
						average=int(0)
						sum_attribute=int(0)
						cnt=len(result)
						for row in result:
							sum_attribute+=int(row[index_of_attribute-1])
						average=sum_attribute/cnt;
						print average
					if func=='distinct' or func=='DISTINCT':
						ans=[]
						for row in result:
							item=row[index_of_attribute-1]
							if item not in ans:
								ans.append(item)
						for item in ans:
							print item
				elif '*' in value :
					# star
					for i in range(len(settings.tables[table_name])-1):
						print settings.tables[table_name][i+1]," ",
					print '\n'
					for row in result:
						for item in row:
							print item,
						print '\n'
				else :
					# single column
					attribute_name=contents['SELECT'][0]
					print attribute_name,table_name
					index_of_attribute=settings.tables[table_name].index(attribute_name)-1
					print index_of_attribute
					for row in result:
						print row[index_of_attribute]

			else:
				# multiple columns in select statement
				columns=len(contents['SELECT'])
				index_of_attribute=[]
				for i in range(len(contents['SELECT'])):
					index_of_attribute.append(settings.tables[table_name].index(contents['SELECT'][i])-1)

				for i in index_of_attribute:
					print settings.tables[table_name][i+1],
				print '\n'
				for row in result:
					for i in index_of_attribute:
						print row[i],
					print '\n'


				# multiple aggregate function
	else:
		cross_product=[]
		#attributes in the global list
		attrList=[]

		tableList=contents['FROM']
		for i in settings.tables[tableList[0]]:
			attrList.append(i)

		table1=settings.data[tableList[0]]

		i=1
		while(i<len(tableList)):

			if len(settings.data[tableList[i]])!=0:
				for j in settings.tables[tableList[i]]:
					attrList.append(j)
				table2=settings.data[tableList[i]]

				temp=[]
				for row1 in table1:
					for row2 in table2:
						temp.append(row1+row2)
				table1=temp
				i=i+1
			else:
				i=i+1

		for item in settings.tables:
			attrList.remove(item)
		cross_product=table1
		# multiple tables
		table_name=contents['FROM'][0]
		result=cross_product

		if 'WHERE' not in contents.keys():
			# one table involve
			if len(contents['SELECT'])==1:
				# It can be single column , aggregate function or *
				value=contents['SELECT'][0].strip()
				if '(' in value :
					# max() , min() , avg()
					# aggregate function
					func=value.split('(')[0]
					# print func
					attribute=value.split('(')[1].split(')')[0]
					# print attribute
					# print result
					index_of_attribute = attrList.index(attribute)
					# print index_of_attribute
					if func=='max' or func=='MAX':
						max_attribute=int(-1e9)
						for row in result:
							max_attribute=max(max_attribute,int(row[index_of_attribute]))
						print max_attribute
					if func=='min' or func=='MIN':
						min_attribute=int(1e9)
						for row in result:
							print row[index_of_attribute-1]
							min_attribute=min(min_attribute,int(row[index_of_attribute]))
						print min_attribute
					if func == 'sum' or func=='SUM':
						sum_attribute=int(0)
						for row in result:
							sum_attribute+=int(row[index_of_attribute])
						print sum_attribute
					if func=='avg' or func=='AVG':
						average=int(0)
						sum_attribute=int(0)
						cnt=len(result)
						for row in result:
							sum_attribute+=int(row[index_of_attribute])
						average=sum_attribute/cnt;
						print average
					if func=='distinct' or func=='DISTINCT':
						ans=[]
						for row in result:
							item=row[index_of_attribute]
							if item not in ans:
								ans.append(item)
						for item in ans:
							print item
				elif '*' in value :
					# star
					for item in attrList:
						print item+' ',
					print ''
					result=cross_product
					for row in result:
						for i in row:
							print str(i)+' ',
						print ''
				else :
					# single column
					attribute_name=contents['SELECT'][0]
					index_of_attribute=attrList.index(attribute_name)
					for row in result:
						print row[index_of_attribute]

			else:
				# multiple columns in select statement
				attribute_indexes=[]
				for i in contents['SELECT']:
					attribute_indexes.append(attrList.index(i))
				result=cross_product
				for row in result:
					for i in attribute_indexes:
						print row[i]+' ',
					print ''
				# multiple aggregate functions
