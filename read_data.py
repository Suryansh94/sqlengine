import csv
import settings
def read():
	for name in settings.tables:
		file_name=str(name)+'.csv'
		f=open(file_name)
		reader=csv.reader(f)
		got_data=list(reader)
		settings.data[name]=got_data
