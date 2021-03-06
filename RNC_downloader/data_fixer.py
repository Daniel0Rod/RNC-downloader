import os,database_gen as dgen
from zipfile import ZipFile

# this script formats the file entrance for an output one.

#usable
def unzipper(zipfile):
	"""
	unzips a file 
	returns the content of the zipfile
	"""
	try:
		list_files = []
		single_file = ""
		with ZipFile(zipfile) as zipf:
			for element in zipf.namelist():
				list_files.append(zipf.extract(element))
				single_file = zipf.extract(element)

			if len(list_files) <= 1:
				return single_file
			return list_files 

	except Exception as ex:
		raise ex

		
#usable
def file_formater(file):
	"""
	decodes data and inserted the result in a csv file
	"""
	try:
		if isinstance(file,list):
			for element in file:
				file_formater(element)

		source_info = open("%s" % file,"br").readlines()
		formated_file = open("%s/result.csv" % os.getcwd(),"a+")
		for element in source_info:
			decoded_element = element.decode(encoding = "latin-1")
			if "|" in decoded_element:
				formated_file.write(decoded_element.replace("|",","))
		else:
			return formated_file.name
			pass
	
	except UnicodeDecodeError as unierror:
		raise unierror

	except Exception as ex:
		raise ex


def inserter(file):
	"""
	inserts the data from the file into the table and deletes the file afterwards
	
	"""
	try:
		db = dgen.DbManager("rnc_db","root","Dontwasteourtime99%")
		connection_result = db.connect()
		if connection_result:
			table = db.generate_table()
			if table:
				print(file)
				db.automated_data_loader(file)
				os.system("rm -f %s" % file)
				return "Success"
	except Exception as e:
		return "Failure", e



# this code ain't working...
#it needs more debugging.
def file_formater_and_poster(file):
	"""
	decodes de info from the input file and inserts the data into the database.
	"""
	
	try:
		db = dgen.DbManager("rnc_db","root","Dontwasteourtime99%")
		connection_result = db.connect()
		if connection_result:
			table = db.generate_table()
			if table:
				if isinstance(file,list):
					for element in file:
						file_formater_and_poster(element)
				source_info = open("%s" % file,"br").readlines()
				#formated_file = open("%s/result.csv" % os.getcwd(),"a+")
				for element in source_info:
					decoded_element = element.decode(encoding = "latin-1")
					while "|" in decoded_element:
						decoded_element = decoded_element.replace("|",",")
					inserting_values_into_table = db.query_inserter("rnc_info",decoded_element)
					if inserting_values_into_table[0] is False:
						raise AttributeError("there's an error with your input. which is %s" % inserting_values_into_table[1])
					#if "|" in decoded_element:
					#	formated_file.write(decoded_element.replace("|",","))
				else:
					return True,"Success"
					pass
	
	except UnicodeDecodeError as unierror:
		raise unierror

	except Exception as ex:
		raise ex
	


if __name__ == '__main__':
	print(inserter(file_formater(unzipper("%s/DGII_RNC.zip" % os.getcwd())))) #Testing output in the CLI

	pass
