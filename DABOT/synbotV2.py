import tkinter
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
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
	driver.execute_script("window.scrollBy(0, -30)") 
	driver
	time.sleep(.5)
	syn_button.click()
	window.update()
	time.sleep(2)

def determine_conj():
	global conj_array
	conj_array = []
	dr_exception = 0
	second_ending = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[1]/ul/li[2]/span').text
	second_ending = second_ending[len(second_ending)-3:]
	current_conj = ''
	if second_ending == 'āre' or second_ending == 'are':
		current_conj = 'first'
	elif second_ending == 'ēre':
		current_conj = 'second'
	elif second_ending == 'rre':
		current_conj = 'thirdre'
	elif second_ending == 'ere':
		first_ending = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[1]/ul/li[1]/span').text
		if first_ending[len(first_ending)-2:] == 'iō':
			current_conj = 'thirdis'
		else:
			current_conj = 'third'
	else:
		current_conj = 'fourth'
	with open('{0}_conj_no_accent.csv'.format(current_conj), newline='', encoding='utf8') as csv_file:
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
	english_word_tensed = ['','','','']
	h,i,j = 1,0,1
	with open('english_conjv2.csv', newline='', encoding='utf8') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			english_array.append(row)
	tense_array = ['verb','past tense','past participle','gerund or present participle']
	word = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[1]/ul/li[5]/span/em').text + ','
	word = word[:word.find(',')]
	driver.execute_script("window.open('');")
	driver.switch_to.window(driver.window_handles[1])
	driver.get('https://www.google.com/search?q=google+dictionary&sxsrf=AOaemvIxDA9Hzjbq0uB8DnCKG_1DJHlbIQ%3A1636741006178&ei=jq-OYZSLCuqrqtsPvfSCmA4&oq=google+dictionary&gs_lcp=Cgdnd3Mtd2l6EAMyBwgjELADECcyBwgjELADECcyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyEAguEMcBENEDEMgDELADEEMyEAguEMcBENEDEMgDELADEENKBQg4EgExSgQIQRgAUABYAGCvBmgBcAJ4AIABAIgBAJIBAJgBAMgBC8ABAQ&sclient=gws-wiz&ved=0ahUKEwiUioyyt5P0AhXqlWoFHT26AOMQ4dUDCA8&uact=5')
	time.sleep(1)
	driver.find_element(By.XPATH, '/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div[1]/label/input').send_keys(word + Keys.ENTER)
	time.sleep(1)
	while True:
		if driver.find_element(By.XPATH, '/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/span/div/div/div[3]/div/div[4]/div[{0}]/div/div/div/div[1]/i/span'.format(h)).text == 'verb':
			break
		else:
			h += 1
	while i < 4:
		current_tense = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/span/div/div/div[3]/div/div[4]/div[{0}]/div/div/div/div[2]/span[{1}]/span[1]'.format(h,j + i)).text
		try:
			temp = tense_array.index(current_tense)
			english_word_tensed.pop(temp)
			english_word_tensed.insert(temp, driver.find_element(By.XPATH, '/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/span/div/div/div[3]/div/div[4]/div[{0}]/div/div/div/div[2]/span[{1}]/span[2]'.format(h,j + i)).text)
			i += 1
		except:
			j += 1
	for x in range(len(english_array)):
		for y in range(len(english_array[x])):
			phrase = english_array[x][y]
			if phrase[len(phrase)-1:] == 'v':
				english_array[x][y] = phrase.replace('v', english_word_tensed[0])
			elif phrase[len(phrase)-2:] == 'pt':
				english_array[x][y] = phrase.replace('pt', english_word_tensed[1])
			elif phrase[len(phrase)-3:] == 'pap':
				english_array[x][y] = phrase.replace('pap', english_word_tensed[2])
			elif phrase[len(phrase)-3:] == 'gpp':
				english_array[x][y] = phrase.replace('gpp', english_word_tensed[3])
	driver.switch_to.window(driver.window_handles[0])
	time.sleep(1)

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
	start_btn['state'] = NORMAL

window = Tk()
window.title('Faster Than Crowns Bot V1')
window.geometry('500x256')
image1 = Image.open('Silly_Cheem.png')
gui_image = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(image=gui_image)
label1.image = gui_image
label1.place(x=0, y=0)
entry0 = Entry(window, width = 6, bg = "white")
entry = Entry(window, width = 6, bg = "white")
entry1 = Entry(window, width = 12, bg = "white")
entry2 = Entry(window, width = 12, bg = "white")
start_btn = Button(window, text='Initiate', command=synopsis_hack)
stop_btn = Button(window, text='Terminate', command=stop, state=DISABLED)
start_btn.place(x=230, y=195)
stop_btn.place(x=222, y=225)
entry0.place(x=233, y=147)
entry.place(x=233, y=170)
entry1.place(x=5, y=5)
entry2.place(x=5, y=25)
window.mainloop()