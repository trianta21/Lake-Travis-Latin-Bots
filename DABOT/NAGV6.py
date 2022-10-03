import tkinter
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
from PIL import ImageTk, Image

driver = webdriver.Chrome()

dat = [[["F","a","S","NOM"],["F","ae","P","NOM"],["F","ae","S","GEN"], ["F","ārum","P","GEN"],["F","ae","S","DAT"],["F","īs","P","DAT"],["F","am","S","ACC"],["F","ās","P","ACC"],["F","ā","S","ABL"],["F","īs","P","ABL"]],[["M","us","S","NOM"],["M","ī","P","NOM"],["M","ī","S","GEN"], ["M","ōrum","P","GEN"],["M","ō","S","DAT"],["M","īs","P","DAT"],["M","um","S","ACC"],["M","ōs","P","ACC"],["M","ō","S","ABL"],["M","īs","P","ABL"]],[["N","um","S","NOM"],["N","a","P","NOM"],["N","ī","S","GEN"], ["N","ōrum","P","GEN"],["N","ō","S","DAT"],["N","īs","P","DAT"],["N","um","S","ACC"],["N","a","P","ACC"],["N","ō","S","ABL"],["N","īs","P","ABL"]],[["M","","S","NOM"],["M","ēs","P","NOM"],["M","is","S","GEN"], ["M","um","P","GEN"],["M","ī","S","DAT"],["M","ibus","P","DAT"],["M","em","S","ACC"],["M","ēs","P","ACC"],["M","e","S","ABL"],["M","ibus","P","ABL"]],[["N","","S","NOM"],["N","a","P","NOM"],["N","is","S","GEN"], ["N","um","P","GEN"],["N","ī","S","DAT"],["N","ibus","P","DAT"],["N","","S","ACC"],["N","a","P","ACC"],["N","e","S","ABL"],["N","ibus","P","ABL"]],[["M","is","S","NOM"],["M","ēs","P","NOM"],["M","is","S","GEN"], ["M","ium","P","GEN"],["M","ī","S","DAT"],["M","ibus","P","DAT"],["M","em","S","ACC"],["M","ēs","P","ACC"],["M","e","S","ABL"],["M","ibus","P","ABL"]],[["N","e","S","NOM"],["N","ia","P","NOM"],["N","is","S","GEN"], ["N","ium","P","GEN"],["N","ī","S","DAT"],["N","ibus","P","DAT"],["N","e","S","ACC"],["N","ia","P","ACC"],["N","ī","S","ABL"],["N","ibus","P","ABL"]],[["M","us","S","NOM"],["M","ūs","P","NOM"],["M","ūs","S","GEN"], ["M","uum","P","GEN"],["M","uī","S","DAT"],["M","ibus","P","DAT"],["M","um","S","ACC"],["M","ūs","P","ACC"],["M","ū","S","ABL"],["M","ibus","P","ABL"]],[["N","ū","S","NOM"],["N","ua","P","NOM"],["N","ūs","S","GEN"], ["N","uum","P","GEN"],["N","ū","S","DAT"],["N","ibus","P","DAT"],["N","N","ū","S","ACC"],["N","ua","P","ACC"],["N","ū","S","ABL"],["N","ibus","P","ABL"]],[["F","ēs","S","NOM"],["F","ēs","P","NOM"],["F","eī","S","GEN"], ["F","ērum","P","GEN"],["F","eī","S","DAT"],["F","ēbus","P","DAT"],["F","em","S","ACC"],["F","ēs","P","ACC"],["F","ē","S","ABL"],["F","ēbus","P","ABL"]],[["M","ēs","S","NOM"],["M","ēs","P","NOM"],["M","ēī","S","GEN"], ["M","ērum","P","GEN"],["M","ēī","S","DAT"],["M","ēbus","P","DAT"],["M","em","S","ACC"],["M","ēs","P","ACC"],["M","ē","S","ABL"],["M","ēbus","P","ABL"]]]

def ranFunc (e):
	return len(e)

def endSor(word):
	dig4 = word[len(word)-4:]
	endlis = []
	for x in range(len(dat)):
   		for y in range(len(dat[x])):
   			if dat[x][y][1] in dig4:
   				endlis.append(dat[x][y][1])
	endlis.sort(reverse=True, key=ranFunc)
	return endlis[0]

def login():
	driver.get('https://laketravis.schoology.com/course/5128046083/materials')
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
	challenges_dropdown = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/ul[3]/li[4]/h6/a')
	challenges_dropdown.click()
	window.update()
	time.sleep(.3)
	nounadj_button = driver.find_element(By.NAME, 'agreement')
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	nounadj_button.click()
	window.update()
	time.sleep(2)

def core(num):
	words = driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/form/ol/li[{0}]/h3".format(num)).text
	f = words[0:words.find(" ")]
	s = words[words.find(" ")+1:]
	fend = endSor(f)
	send = endSor(s)
	fprop = []
	sprop = []
	for x in range(len(dat)):
		for y in range(len(dat[x])):
			if dat[x][y][1] == fend:
				fprop.append(dat[x][y])
			if dat[x][y][1] == send:
				sprop.append(dat[x][y])
	for x in range(len(fprop)):
		for y in range(len(sprop)):
			if (fprop[x][0]==sprop[y][0])&(fprop[x][2]==sprop[y][2])&(fprop[x][3]==sprop[y][3]):
				return("1")
	return("2")

def latin_do():
	for x in range(1, 11):
		target = driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/form/ol/li[{0}]/div/div/div[{1}]/label".format(x, core(x)))
		target.click()
		time.sleep(.5)
		target.location_once_scrolled_into_view
		time.sleep(.5)
	driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/h1/a[1]").click()
	time.sleep(1)

def perform():
	start_btn['state'] = DISABLED
	stop_btn['state'] = NORMAL
	num_attempt = entry.get()
	window.update()
	login()
	time.sleep(3)
	for y in range(0, int(num_attempt)):
		latin_do()
		time.sleep(1)
		driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/h1/a[2]").click()
		time.sleep(2)
		driver.execute_script("window.scrollTo(0,0);")
		time.sleep(1)

def stop():
	start_btn['state'] = NORMAL
	stop_btn['state'] = DISABLED

window = Tk()
window.title('Better than Kate bot V6')
window.geometry('340x225')
image1 = Image.open('Silly_Dog.png')
gui_image = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(image=gui_image)
label1.image = gui_image
label1.place(x=0, y=0)
entry = Entry(window, width=6, bg="white")
entry1 = Entry(window, width = 12, bg="white")
entry2 = Entry(window, width = 12, bg="white")
start_btn = Button(window, text='Initiate', command=perform)
start_btn.place(x=150, y=140)
stop_btn = Button(window, text='Terminate', command=stop, state=DISABLED)
stop_btn.place(x=142, y=170)
entry.place(x=153, y=110)
entry1.place(x=5, y = 5)
entry2.place(x = 5, y = 25)
window.mainloop()