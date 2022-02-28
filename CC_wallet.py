#importing the regex module
import re,os
from difflib import get_close_matches
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from PIL import Image
import shutil


# dictionaries to keep for analysis
crypto_address_patterns = {}
crypto_address_patterns["bitcoin"] = "([13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-z0-9]{38,60})"
crypto_address_patterns["etherium"] = "0x[a-fA-F0-9]{40}"
crypto_address_patterns["dogecoin"] = "D[5-9A-HJ-NP-U]{1}[1-9a-km-zA-HJ-NP-Z]{32}"
crypto_address_patterns["monero"] = "4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}"
crypto_address_patterns["dash"] = "X[1-9A-HJ-NP-Za-km-z]{33}"
crypto_address_patterns["Adeptio"] = "[A][a-km-zA-HJ-NP-Z1-9]{24,33}"
crypto_address_patterns["Amitycoin"] ="amit[1-9A-Za-z^OIl]{94}"
crypto_address_patterns["Beam"] ="([0-9a-f]{1,80})"
crypto_address_patterns["BitDaric"] ="[R][a-km-zA-HJ-NP-Z1-9]{25,34}"
crypto_address_patterns["BLK-BURNT"] ="(?:[0-9a-z]{2}?){1,%d}+"
crypto_address_patterns["CRowdCLassic"] ="[C][a-zA-Z0-9]{33}"
crypto_address_patterns["CloakCoin"] ="[B|C][a-km-zA-HJ-NP-Z1-9]{33}|^smY[a-km-zA-HJ-NP-Z1-9]{99}"
crypto_address_patterns["Counterparty"] ="[1][a-zA-Z0-9]{33}"
crypto_address_patterns["Credits"] ="[C][a-km-zA-HJ-NP-Z1-9]{25,34}"
crypto_address_patterns["Croat"] ="C[1-9A-HJ-NP-Za-km-z]{94}"
crypto_address_patterns["DSTRA"] ="[D][a-km-zA-HJ-NP-Z1-9]{33}"
crypto_address_patterns[""] =""
crypto_address_patterns[""] =""
crypto_address_patterns[""] =""
crypto_address_patterns[""] =""
crypto_address_patterns[""] =""
crypto_address_patterns[""] =""
crypto_address_patterns[""] =""
crypto_address_patterns[""] =""
cryptocoin_flag = "g"

#crypto_addresses_found[cryptocurrency_name][address]=[list_of_filepaths]
crypto_addresses_found = {}	

word_counts = {}
#file_type_catelog[file_type_extension]=[filepath] 
file_type_catelog = {}
#word_matched_image_files[file_type_extension][keyword] = [filepath]
word_matched_image_files = {}
#other_image_files[file_type_extension][keyword] = [filepath]
other_image_files = {}
#word_matched_filenames[file_type_extension][keyword] = [filepath]
word_matched_filenames = {}
#word_matched_files[nw]=[filepath]
word_matched_files = {} 	
word_substitutions = {}

#predefined variables
directory = ""
result_directory = ""
result_dir = ""
file_type_list_dir = ""
filename_word_match_list_dir = ""
wordsearch_file_list_dir = ""
word_matched_image_list_dir = ""
other_image_list_dir = ""
crypto_addresses_dir = ""


# important predefined lists
image_file_types = [".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp",".png",".gif",".apng",".avif",".svg",".webp",".bmp",".ico", ".cur",".tif", ".tiff"]
keywords = [
    "cryptaddress",
    "cryptocurrency",
    "address",
    "detector",
	"symbol",
	"mota",
	"btc"
  ]

def modify_keywords():
	action = 0
	while action!=4:
		if len(keywords)>0:
			print("These are the keywords to search:")
				for i in keywords:
					print(i)
		else:
			print("No keywords listed to search")
		action = int(input("Want to '1'->clear,'2'->add,'3'->remove'4'->Done?"))
		if action == 1:
			keywords.clear()
			print("cleared")
		elif action == 2:
			keywords.append(input("Enter keyword:"))
		elif action == 3:
			keywords.remove(input("Enter Keyword to Remove:"))
	return
		

def select_directory(title_txt):
	dir = filedialog.askdirectory(title=title_txt)
	return dir

def select_directories():
	directory = select_directory("Enter target directory:")
	result_directory = select_directory("Enter result folder destination:")

def create_new_dir(parent_dir,name):
	new_dir = os.path.join(parent_dir,name)
	try:
		os.mkdir(new_dir,mode=755)
	except OSError as e:
		if e.errno == errno.EEXIST:
			print(new_dir)
			print('Directory already exists')
		else:
			raise
	return new_dir

def define_directories():
	result_dir = create_new_dir(result_directory,'results')
	file_type_list_dir = create_new_dir(result_dir,'file_type_lists')
	filename_word_match_list_dir = create_new_dir(result_dir','filename_word_match_lists')
	wordsearch_file_list_dir = create_new_dir(result_dir,'wordsearch_file_lists')
	word_matched_image_list_dir = create_new_dir(result_dir,'word_matched_image_lists')
	other_image_list_dir = create_new_dir(result_dir,'other_image_lists')
	crypto_addresses_dir = create_new_dir(result_dir,'crypto_addresses') 

def new_project():
	select_directories()
	define_directories()
	modify_keywords()
	wordsearch_directory(directory,list_of_words)
	search_crypto_addresses()
	cc_directory_files()

# def pull_existing_project():
	# #DOES NOT WORK YET --- NEED TO WORK ON PULLING DICTIONARIES
	# select_directories()
	# define_directories()
	# pull_dict_values_from_results()

	
def search_crypto_addresses():
	print("Starting to search for Cryptocurrency Addresses...")
	for k in file_type_catelog.keys():
		# go thru imagery filename dictionary to check for matching
		if k not in image_file_types:
			for filepath in file_type_catelog[k]:
				for c in crypto_address_patterns.keys():
					matches = pattern_search_file(filepath,crypto_address_patterns[c])
					if len(matches)>0:
						if c not in crypto_addresses_found.keys():
							crypto_addresses_found[c] = {}
						for m in matches:
							if m in crypto_addresses_found[c].keys():
								crypto_addresses_found[c][m].append(filepath)
							else:
								crypto_addresses_found[c][m] = [filepath]
						
	print("Cryptocurrency Address Search Complete.")
	print("---------------------------------------")
	for k in crypto_addresses_found.keys():
		print('    %-7s %d' %(k,len(crypto_addresses_found[k])))
		cryptocurrency_dir = create_new_dir(crypto_addresses_dir,k)
		for kk in crypto_addresses_found[k].keys():
			print('        %' %(kk))
			save_dict_values_by_keys(crypto_addresses_found[k],cryptocurrency_dir)
	print('results are saved.')
	return

def replace_crypto_addresses():
	for k in crypto_addresses_found.keys():
		print('    %-7s %d' %(k,len(crypto_addresses_found[k])))
		for kk in crypto_addresses_found[k].keys():
			print('        %' %(kk))
			replace_q = input("Want to replace this?").lower()
			if replace_q.startswith("y"):
				new_crypto_address = ""
				check_answer = "no"
				while check_answer.startswith("n"):
					new_crypto_address = input("Enter New Address:")
					print("New Address: %" %new_crypto_address)
					check_answer = input("Is that Correct?").lower()
				print("Replacing...")
				for filepath in crypto_addresses_found[k][kk]:
					print(filepath)
					replace_pattern_in_file(filepath, kk, new_crypto_address, flags=cryptocoin_flag)
				

def pattern_search_file(filename, pattern):
	matches = []
	with open(filename) as df:
		data = df.read()
		matches = re.findall(pattern, filetext)
	return matches

def find_image_filepath():
	file = None
	filepath = None
	file = filedialog.askopenfile(mode='r', filetypes=[('Image Files', image_file_types)])
	if file:
		filepath = os.path.abspath(file.name)
	return filepath

def open_image(filepath):
	# open method used to open different extension image file
	im = Image.open(filepath) 
	# show image
	im.show()

def replace_images(dictionary):
	for k in dictionary.keys():
		print(k + " file type")
		for original_filepath in dictionary[k]:
			ask_again = True
			while ask_again:
				print("Original Image:")
				print(original_filepath)
				open_image(original_filepath)
				replace_q = input("Want to replace this?").lower()
				if replace_q.startswith("y"):
					new_image_filepath = find_image_filepath()
					if new_image_filepath:
						print("Replace With")
						print(new_image_filepath)
						open_image(new_image_filepath)
						confirm_q = input("Replace with this?").lower()
						if confirm_q.startswith("y"):
							shutil.move(new_image_filepath,original_filepath)
							print("done")
							ask_again = False
						else:
							print("Let's try again...")
				else:
					ask_again = False
	print("Those are all the images")
	return
			

#defining the replace method
def replace_pattern_in_file(filePath, text, subs, flags=0):
    with open(file_path, "r+") as file:
        #read the file contents
        file_contents = file.read()
        text_pattern = re.compile(re.escape(text), flags)
        file_contents = text_pattern.sub(subs, file_contents)
        file.seek(0)
        file.truncate()
        file.write(file_contents)

def replace_pattern_in_string(original_str,text, subs, flags=0):
	text_pattern = re.compile(re.escape(text), flags)
    new_string = text_pattern.sub(subs, original_str)
	return new_string


def match_filenames(file_list, list_of_words):
	returning_dictionary = {}
	for x in list_of_words:
		li = [y for y in get_close_matches(file_list) if x in y]
		if len(li)>0:
			returning_dictionary[x] = li 		
	return returning_dictionary

def wordsearch_dict_filename_lists():
	# create nested dictionary
	for k in file_type_catelog.keys():
		# go thru imagery filename dictionary to check for matching
		if k in image_file_types:
			matched_dict = match_filenames(file_type_catelog[k],list_of_words)
			if len(matched_dict)>0:
				word_matched_image_files[k] = matched_dict
			else:
				other_image_files[k] = matched_dict
		# if not image file, catelog other files
		else:
			matched_dict = match_filenames(file_type_catelog[k],list_of_words)
			if len(matched_dict)>0:
				word_matched_filenames[k] = matched_dict
				
	return

		
def wordsearch_file(filename,list_of_words):	
	with open(filename) as df:
		data = df.read()
		sp = data.split()
		for x in list_of_words:
			li = [y for y in get_close_matches(x,sp,cutoff=0.5) if x in y]
				word_counts[nw] = counts.get(nw, 0) + 1
			#check if filename for new word (nw) is recorded,add if not
			for nw in li:
				if nw in word_matched_files.keys():
					if filename not in word_matched_files[nw]:
						word_matched_files[nw].append(filepath)	
						
	return
	
def catelog_files(directory):
	print('Cateloging Files...')
	for root, dirs, files in os.walk(directory):
		for filename in files:
			filepath = os.path.join(path,filename)
			# catelog file types
			extension = filename.split(".")[-1]
			if extension not in file_type_catelog.keys():
				file_type_catelog[extension] = []
			file_type_catelog[extension].append(filepath) 
	print("Files Cateloged:")
	for k in file_type_catelog.keys():
		print('    %-7s %d' %(k,len(file_type_catelog[k])))
	return

def get_dic_from_saved_files(dictionary,saved_dir):
	with os.scandir(saved_dir) as i:
		for entry in i:
			if entry.is_file():
				dictionary[entry.name.replace(".txt","")]=

def pull_dict_values_from_results():
	get_dic_from_saved_files(file_type_catelog,file_type_list_dir)
	get_dic_from_saved_files(word_matched_image_files,word_matched_image_list_dir)
	get_dic_from_saved_files(other_image_files,other_image_list_dir)
	get_dic_from_saved_files(word_matched_filenames,filename_word_match_list_dir)
	get_dic_from_saved_files(word_matched_files,wordsearch_file_list_dir)

def save_dict_values_by_keys(dictionary,destination_dir):
	for k in dictionary.keys():
		txtfile = open(os.path.join(destination_dir,k + '.txt'),'w')
		for e in dictionary[k]:
			txtfile.write(e + "\n")
		txtfile.close()

def search_files_word_matches():
	for k in file_type_catelog.keys():
		# go thru filename dictionary to check for matching words inside files
		if k not in image_file_types:
			for f in file_type_catelog[k]:
				wordsearch_file(filename,list_of_words)
	return

def wordsearch_directory(directory,list_of_words):
	catelog_files(directory,list_of_words)
	save_dict_values_by_keys(file_type_catelog,file_type_list_dir)
	print("File type lists are saved")
	print("Filename Word Search in Progress..")
	wordsearch_dict_filename_lists()
	print("Filename Word Search Complete.")
	print("Saving List of Image Filenames with mached words..")
	#-----------------------------------------------------
	#dictionary[file_type_extension][keyword] = [filepath]
	# create sub folder for each file type
	# filepaths with keyword as name
	for k in word_matched_image_files.keys():
		file_type_dir = create_new_dir(word_matched_image_list_dir,k)
		save_dict_values_by_keys(word_matched_image_files[k],file_type_dir)
	print("Image Filename Match lists saved")
	print("Saving List of Other Image Filenames..")
	for k in other_image_files.keys():
		file_type_dir = create_new_dir(other_image_list_dir,k)
		save_dict_values_by_keys(other_image_files[k],file_type_dir)
	print("Other Image Filename lists saved")
	print("Saving List of other Matched Filenames..")
	for k in word_matched_filenames.keys():
		file_type_dir = create_new_dir(filename_word_match_list_dir,k)
		save_dict_values_by_keys(word_matched_filenames[k],file_type_dir)
	print("Other Matched Filename lists saved")
	#-----------------------------------------------------
	print("----------------------------------")
	print("Now searching files for matches...")
	search_files_word_matches()
	print("Results:")
	for k in word_counts.keys():
		print('    %-7s %d' %(k,len(word_counts[k])))
	print("----------------------------------")
	print("Saving List of Files that had Matched Words..")
	save_dict_values_by_keys(word_matched_files,wordsearch_file_list_dir)
	print("Word Search File Lists saved")

def sub_matched_words_in_files():
	for k in word_matched_files.keys():
		sub_q = input("Replace " + k + "?").lower()
		if sub_q.startswith('y'):
			sub = input("Replace with:")
			print("Starting to replace " + k + " with " + sub)
			word_substitutions[k]=sub
			for f in word_matched_files[k]:
				print("->" + f)
				replace_pattern_in_file(f, k, sub, flags=0)
	print("Those are all the matches")
	return

def rename_matched_filenames():
	for k in word_matched_filenames.keys():
		if k in word_substitutions.keys():
			print("Previously replaced " + k + " with " + word_substitutions[k]")
			
			sub_q = input("Replace " + k + "?").lower()
			if sub_q.startswith('y'):
				use_previous_sub_q = input("Use " + word_substitutions[k] + " ?").lower()
				if use_previous_sub_q.startswith('y'):
					sub = word_substitutions[k]
				else:
					sub = input("Replace with:")
				print("Starting to replace " + k + " with " + sub)
				for filename in word_matched_filenames[k]:
					new_filename = replace_pattern_in_string(filename,k, sub, flags=0)
					os.rename(filename,new_filename)
	print("renaming files complete.")

def cc_directory_files():
	
	sub_words_q = input('Want to substitute words found in files?').lower()
	if sub_words_q.startswith('y'):
		sub_matched_words_in_files()
	replace_word_matched_images_q = input("Want to replace word matched images?").lower()
	if replace_word_matched_images_q.startswith('y'):
		replace_images(word_matched_image_files)
	replace_other_images_q = input("Want to replace other images?").lower()
	if replace_other_images_q.startswith('y'):
		replace_images(other_image_files)
	rename_matched_filenames_q = input('Want to rename word matched filenames?').lower()
	if rename_matched_filenames_q.startswith('y'):
		rename_matched_filenames()
	replace_crypto_addresses_q = input("Want to replace cryptocurrency addresses?").lower()
	if replace_crypto_addresses_q.startswith('y'):
		replace_crypto_addresses()
	
	
	

----------------------------------------------------------------------------
# mystring="walk walked walking talk talking talks talked fly flying"
# list_of_words=["walk","talk","fly"]

# word_counts = {}

# from nltk.stem.snowball import EnglishStemmer
# stemmer = EnglishStemmer()



# for target in list_of_words:
    # word_counts[target] = 0

    # for word in mystring.split(' '):

        # # Stem the word and compare it to the stem of the target
        # stem = stemmer.stem(word)        
        # if stem == stemmer.stem(target):
            # word_counts[target] += 1

# print word_counts
# Output:

# {'fly': 2, 'talk': 4, 'walk': 3}
# -----------------------------------------------------------------
# file_path="review.txt"
# text="boundation"
# subs="foundation"
# #calling the replace method
# replace(file_path, text, subs)
# -------------------------------------------------------------------------

# def checkKey(dict, key):
      
    # if key in dict.keys():
        # print("Present, ", end =" ")
        # print("value =", dict[key])
    # else:
        # print("Not present")
		
		
		

# from collections import defaultdict
  
# Details = defaultdict(list)
# Details["Country"].append("India")
