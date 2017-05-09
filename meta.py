import settings
def read_meta_data(file_name):
	# global tables 	# i want to modify it
	f=open(file_name)  # read mode is default in python no need to specify explicitly

	# read()  method return's string whereas readlines() returns list of string

	lines = f.readlines()
	i=0

	# strip() to remove carriage , extra space etc

	while i <(len(lines)):
		content=[]
		if lines[i].strip()=='<begin_table>':
			i+=1
			while lines[i].strip()!='<end_table>':
				content.append(lines[i])
				i+=1
			i+=1
		key=content[0].strip()
		value=[]
		for item in content:
			value.append(item.strip())

		settings.tables[key]=value
		# tables['table1']=['table1', 'A', 'B', 'C']
