import tkinter
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import csv
from PIL import ImageTk, Image

driver = webdriver.Chrome()

conj_array = []
principle_parts = []
pov_order = []
english_array = []

def login():
	driver.get('https://laketravis.schoology.com/course/5128046083/materials')
	synopsis_sect = entry0.get()
	synopsis = entry.get()
	try:
		username = entry1.get()
		password = entry2.get()
		user_box = driver.find_element(By.NAME, 'mail')
		pass_box = driver.find_element(By.NAME, 'pass')
		user_box.send_keys(username)
		pass_box.send_keys(password)
		login_button = driver.find_element(By.NAME, 'op')
		login_button.click()
	except NoSuchElementException:
		print('already logged in')
	window.update()
	time.sleep(1)
	latin_app_button = driver.find_element(By.ID, 'app-run-364888653')
	latin_app_button.click()
	window.update()
	time.sleep(2)
	driver.get('https://lthslatin.org')
	synopsis_dropdown = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/ul[3]/li[{0}]/h6/a'.format(synopsis_sect))
	synopsis_dropdown.click()
	window.update()
	time.sleep(.3)
	syn_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/ul[3]/li[{0}]/div/ul/li[{1}]'.format(synopsis_sect, synopsis))
	syn_button.location_once_scrolled_into_view
	time.sleep(.5)
	syn_button.click()
	window.update()
	time.sleep(3)

def determine_conj():
	global conj_array
	conj_array = []
	second_ending = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[1]/ul/li[2]/span').text
	second_ending = second_ending[len(second_ending)-3:]
	current_conj = ''
	if second_ending == 'āre':
		current_conj = 'first'
	elif second_ending == 'ēre':
		current_conj = 'second'
	elif second_ending == 'ere':
		first_ending = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[1]/ul/li[1]/span').text
		if first_ending[len(first_ending)-2:] == 'iō':
			current_conj = 'thirdis'
		else:
			current_conj = 'third'
	else:
		current_conj = 'fourth'
	with open('{0}_conj.csv'.format(current_conj), newline='', encoding='utf8') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			conj_array.append(row)

def pov_fill():
	global pov_order
	pov_order = []
	pov = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[1]/ul/li[5]/span/span').text
	pov_order = [int(pov[0])+1,int(pov[0])+7]
	if pov[4] == 'p':
		for x in range(0,2):
			pov_order[x] += 3

def princ_part():
	global principle_parts
	principle_parts = []
	part_lengths = [len(conj_array[2][0]),len(conj_array[14][2]),len(conj_array[2][3]),len(conj_array[0][2])]
	for x in range(1,5):
		temp_principle = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[1]/ul/li[{0}]/span'.format(x)).text
		principle_parts.append(temp_principle[0:len(temp_principle)-part_lengths[x-1]])

def english_fill():
	global english_array
	english_array = []
	word = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[1]/ul/li[5]/span/em').text
	e_exception = ''
	present = entry_pres.get()
	past = entry_past.get()
	action = entry_action.get()
	with open('english_conj.csv', newline='', encoding='utf8') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			english_array.append(row)
	if present != '':
		for x in range(len(english_array)):
			for y in range(len(english_array[x])):
				phrase = english_array[x][y]
				if phrase[phrase.find('1')+1:] == 'ing':
					english_array[x][y] = phrase.replace('1ing', action)
				elif phrase[phrase.find('1')+1:] == 'ed':
					english_array[x][y] = phrase.replace('1ed', past)
				else:
					english_array[x][y] = phrase.replace('1', present)
	elif word[-1] == 'y':
		for x in range(len(english_array)):
			for y in range(len(english_array[x])):
				phrase = english_array[x][y]
				if phrase[phrase.find('1')+1:] == 'ed':
					english_array[x][y] = phrase.replace('1', word[0:len(word)-1] + 'i')
				else:
					english_array[x][y] = phrase.replace('1', word)
	else:
		if word[-1] == 'e':
			e_exception = 'e'
			word = word[0:len(word)-1]
		for x in range(len(english_array)):
			for y in range(len(english_array[x])):
				phrase = english_array[x][y]
				if phrase.find('1') == len(phrase)-1:
					english_array[x][y] = phrase.replace('1', word + e_exception)
				else:
					english_array[x][y] = phrase.replace('1', word)

def participle_fill():
	driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[1]/div/div/a[2]').click()
	driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/ul/li[2]/a').click()
	time.sleep(1)
	parts_order = [1,3,3,1]
	i = 0
	for x in range(0,2):
		for y in range(0,2):
			driver.find_element(By.XPATH, '/html/body/div[7]/div[1]/div[2]/div/div[{0}]/div[{1}]/h4/a'.format(x+1,y+1)).click()
			lat_input = driver.find_element(By.XPATH, '/html/body/div[7]/div[1]/div[2]/div/div[{0}]/div[{1}]/div/div/div[1]/div/div/input'.format(x+1,y+1))
			driver.execute_script('arguments[0].value = "";', lat_input)
			lat_input.send_keys(principle_parts[parts_order[i]] + conj_array[0][i])
			eng_input = driver.find_element(By.XPATH, '/html/body/div[7]/div[1]/div[2]/div/div[{0}]/div[{1}]/div/div/div[2]/div/div/input'.format(x+1,y+1))
			driver.execute_script('arguments[0].value = "";', eng_input)
			eng_input.send_keys(english_array[0][i])
			driver.find_element(By.XPATH, '/html/body/div[7]/div[1]/div[2]/div/div[{0}]/div[{1}]/h4/a'.format(x+1,y+1)).click()
			i += 1

def infintive_fill():
	driver.find_element(By.XPATH, '/html/body/div[7]/div[1]/div[1]/div/div/a[2]').click()
	driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/div/ul/li[3]/a').click()
	time.sleep(1)
	parts_order = [1,2,3,1,3]
	i = 0
	for x in range(0,3):
		driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div[2]/div/div[1]/div[{0}]/h4/a'.format(x+1)).click()
		lat_input = driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div[2]/div/div[1]/div[{0}]/div/div/div[1]/div/div/input'.format(x+1))
		driver.execute_script('arguments[0].value = "";', lat_input)
		lat_input.send_keys(principle_parts[parts_order[i]] + conj_array[1][i])
		eng_input = driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div[2]/div/div[1]/div[{0}]/div/div/div[2]/div/div/input'.format(x+1))
		driver.execute_script('arguments[0].value = "";', eng_input)
		eng_input.send_keys(english_array[1][i])
		driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div[2]/div/div[1]/div[{0}]/h4/a'.format(x+1)).click()
		i += 1
	for y in range(0,2):
		driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div[2]/div/div[2]/div[{0}]/h4/a'.format(y+1)).click()
		lat_input = driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div[2]/div/div[2]/div[{0}]/div/div/div[1]/div/div/input'.format(y+1))
		driver.execute_script('arguments[0].value = "";', lat_input)
		lat_input.send_keys(principle_parts[parts_order[i]] + conj_array[1][i])
		eng_input = driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div[2]/div/div[2]/div[{0}]/div/div/div[2]/div/div/input'.format(y+1))
		driver.execute_script('arguments[0].value = "";', eng_input)
		eng_input.send_keys(english_array[1][i])
		driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div[2]/div/div[2]/div[{0}]/h4/a'.format(y+1)).click()
		i += 1

def indicative_fill():
	driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div[1]/div/div/a[2]').click()
	driver.find_element(By.XPATH, '/html/body/div[8]/div[2]/div/ul/li[4]/a').click()
	time.sleep(1)
	parts_order = [1,1,1,2,2,2,1,1,1,3,3,3]
	i = 0
	for x in range(0,2):
		for y in range(0,6):
			driver.find_element(By.XPATH, '/html/body/div[9]/div[1]/div[2]/div/div[{0}]/div[{1}]/h4/a'.format(x+1,y+1)).click()
			lat_input = driver.find_element(By.XPATH, '/html/body/div[9]/div[1]/div[2]/div/div[{0}]/div[{1}]/div/div/div[1]/div/div/input'.format(x+1,y+1))
			driver.execute_script('arguments[0].value = "";', lat_input)
			lat_input.send_keys(principle_parts[parts_order[i]] + conj_array[pov_order[0]][i])
			eng_input = driver.find_element(By.XPATH, '/html/body/div[9]/div[1]/div[2]/div/div[{0}]/div[{1}]/div/div/div[2]/div/div/input'.format(x+1,y+1))
			driver.execute_script('arguments[0].value = "";', eng_input)
			eng_input.send_keys(english_array[pov_order[0]][i])
			driver.find_element(By.XPATH, '/html/body/div[9]/div[1]/div[2]/div/div[{0}]/div[{1}]/h4/a'.format(x+1,y+1)).click()
			i += 1

def subjunctive_fill():
	driver.find_element(By.XPATH, '/html/body/div[9]/div[1]/div[1]/div/div/a[2]').click()
	driver.find_element(By.XPATH, '/html/body/div[9]/div[2]/div/ul/li[5]/a').click()
	time.sleep(1)
	parts_order = [1,1,2,2,1,1,3,3]
	i = 0
	for x in range(0,2):
		for y in range(0,4):
			driver.find_element(By.XPATH, '/html/body/div[10]/div[1]/div[2]/div/div[{0}]/div[{1}]/h4/a'.format(x+1,y+1)).click()
			lat_input = driver.find_element(By.XPATH, '/html/body/div[10]/div[1]/div[2]/div/div[{0}]/div[{1}]/div/div/div/input'.format(x+1,y+1))
			driver.execute_script('arguments[0].value = "";', lat_input)
			lat_input.send_keys(principle_parts[parts_order[i]] + conj_array[pov_order[1]][i])
			driver.find_element(By.XPATH, '/html/body/div[10]/div[1]/div[2]/div/div[{0}]/div[{1}]/h4/a'.format(x+1,y+1)).click()
			i += 1

def imperative_fill():
	driver.find_element(By.XPATH, '/html/body/div[10]/div[1]/div[1]/div/div/a[2]').click()
	driver.find_element(By.XPATH, '/html/body/div[10]/div[2]/div/ul/li[6]/a').click()
	time.sleep(1)
	i = 0
	for x in range(0,2):
		driver.find_element(By.XPATH, '/html/body/div[11]/div[1]/div[2]/div/div[{0}]/h4/a'.format(x+1)).click()
		for y in range(0,2):
			lat_input = driver.find_element(By.XPATH, '/html/body/div[11]/div[1]/div[2]/div/div[{0}]/div/div/div[1]/div[{1}]/input'.format(x+1,y+1))
			driver.execute_script('arguments[0].value = "";', lat_input)
			lat_input.send_keys(principle_parts[1] + conj_array[14][i])
			i += 1
		eng_input = driver.find_element(By.XPATH, '/html/body/div[11]/div[1]/div[2]/div/div[{0}]/div/div/div[2]/div/input'.format(x+1))
		driver.execute_script('arguments[0].value = "";', eng_input)
		eng_input.send_keys(english_array[8][x])
		driver.find_element(By.XPATH, '/html/body/div[11]/div[1]/div[2]/div/div[{0}]/h4/a'.format(x+1)).click()

def synopsis_hack():
	start_btn['state'] = DISABLED
	login()
	determine_conj()
	pov_fill()
	english_fill()
	princ_part()
	participle_fill()
	infintive_fill()
	indicative_fill()
	subjunctive_fill()
	imperative_fill()
	stop_btn['state'] = NORMAL

def stop():
	stop_btn['state'] = DISABLED
	entry_pres.delete(0, 'end')
	entry_past.delete(0, 'end')
	entry_action.delete(0, 'end')
	start_btn['state'] = NORMAL

window = Tk()
window.title('Faster Than Crowns Bot V1')
window.geometry('500x256')
image1 = Image.open('Silly_Cheem.png')
gui_image = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(image=gui_image)
label1.image = gui_image
label1.place(x=0, y=0)
label2 = tkinter.Label(text = 'Manual Override("", "ed", "ing")', bg="white")
label2.place(x=5, y=47)
entry0 = Entry(window, width = 6, bg = "white")
entry = Entry(window, width = 6, bg = "white")
entry1 = Entry(window, width = 12, bg = "white")
entry2 = Entry(window, width = 12, bg = "white")
entry_pres = Entry(window, width = 12, bg = "white")
entry_past = Entry(window, width = 12, bg = "white")
entry_action = Entry(window, width = 12, bg = "white")
start_btn = Button(window, text='Initiate', command=synopsis_hack)
stop_btn = Button(window, text='Terminate', command=stop, state=DISABLED)
start_btn.place(x=230, y=195)
stop_btn.place(x=222, y=225)
entry0.place(x=233, y=147)
entry.place(x=233, y=170)
entry1.place(x=5, y=5)
entry2.place(x=5, y=25)
entry_pres.place(x=5, y=71)
entry_past.place(x=5, y=91)
entry_action.place(x=5, y=111)
window.mainloop()