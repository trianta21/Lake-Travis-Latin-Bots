from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import random
import tkinter
from tkinter import *
from PIL import ImageTk, Image

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

def login():
    global logged_in
    #driver.get('https://laketravis.schoology.com/group/2278353920')
    #driver.get('https://laketravis.schoology.com/group/2278336525')
    driver.get('https://laketravis.schoology.com/group/2278334531')
    username = username_entry.get()
    password = password_entry.get()
    logged_in = False
    try:
        user_box = driver.find_element(By.NAME, 'mail')
        pass_box = driver.find_element(By.NAME, 'pass')
        user_box.send_keys(username)
        pass_box.send_keys(password)
        login_button = driver.find_element(By.NAME, 'op')
        login_button.click()
        window.update()
        time.sleep(0.5)
    except NoSuchElementException:
        print('already logged in')
        logged_in = True
    try:
        login_failed = driver.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/div/table/tbody/tr/td[2]/div')
        print('incorrect login')
        tm_stop_btn['state'] = DISABLED
        tm_start_btn['state'] = NORMAL
        failed_login_message.place(x=6, y=570)
        window.update()
    except NoSuchElementException:
        failed_login_message.place_forget()
        print('logging in')
        logged_in = True
    time.sleep(1)
    if logged_in:
        latin_app_button = driver.find_element(By.ID, 'app-run-364888653')
        latin_app_button.click()
        window.update()
        time.sleep(2)
        driver.get('https://lthslatin.org')

def latin_cheat():
    word = driver.find_element(By.ID, 'timedMorph_form').text
    print('XXX word is: ' + word + ' XXX')
    gram = driver.find_element(By.ID, 'timedMorph_stimulus').text
    print('XXX grammar is: ' + gram + ' XXX')
    word_list = []
    word_count = 0
    answer_array_found_index = -1
    for answer_list in TIMED_MORPH_ANSWERS_ARRAY:
        answer_array_found_index = answer_array_found_index + 1
        if word in answer_list:
            word_count = word_count + 1
            word_list = answer_list
            break
        window.update()
    if update_mode:
        if word_count == 0:
            answer_array_found_index = answer_array_found_index + 1
            word_list = add_new_wordlist(word)
    true_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[3]/div/div/form/div[1]/label')
    false_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[3]/div/div/form/div[2]/label')
    time.sleep(0.2)
    if gram in word_list:
        true_button.click()
        tf_input = True
    else:
        hit_false = True
        for att in word_list:
            att_list = att.split('+')
            if gram in att_list:
                true_button.click()
                tf_input = True
                hit_false = False
            window.update()
        if hit_false:
            false_button.click()
            tf_input = False
    time.sleep(1)

    if update_mode:
        try:
            erroris = driver.find_element(By.XPATH, 'html/body/div[6]/div[6]/h3/span/em')
            update_wordlist(word_list, gram, tf_input, answer_array_found_index)
        except NoSuchElementException:
            print('correct')

def add_new_wordlist(word):
    word_list = [word, '1st person', 'singular', 'present', 'indicative', 'active', 'nominative', 'masculine',
                 'positive', 'participle', 'adverb', 'relative', 'dactyl']
    TIMED_MORPH_ANSWERS_ARRAY.append(word_list)
    print('timed morph answers array with appended new word list: ')
    print(TIMED_MORPH_ANSWERS_ARRAY)
    return word_list

def update_wordlist(word_list, gram, tf_input, fault_index):
    updated_wl = word_list
    print('UPDATING WORD: ' + word_list[0])
    print('WORD AT FAULT INDEX: ' + TIMED_MORPH_ANSWERS_ARRAY[fault_index][0])
    print('UPDATING GRAM: ' + gram)
    print('tf input is: : ' + str(tf_input))
    gram_type_index = -1
    gram_index = -1
    for t in grammar_array:
        for g in t:
            if g == gram:
                gram_type_index = grammar_array.index(t)
                gram_index = grammar_array[gram_type_index].index(g)
                break
            window.update()
    print('GRAMMAR TYPE INDEX: ' + str(gram_type_index))
    print('GRAMMAR INDEX: ' + str(gram_index))
    if tf_input:
        if gram_index == len(grammar_array[gram_type_index]) - 1:
            gram_index = -1
        updated_wl[gram_type_index + 1] = grammar_array[gram_type_index][gram_index + 1]
        TIMED_MORPH_ANSWERS_ARRAY[fault_index] = updated_wl
        print(updated_wl)
    window.update()
    if not tf_input:
        multigrams_list = updated_wl[gram_type_index + 1].split('+')
        print('000000000000 MGRAMS LIST: ')
        print(multigrams_list)
        if grammar_array[gram_type_index].index(gram) < grammar_array[gram_type_index].index(multigrams_list[-1]):
            updated_wl[gram_type_index + 1] = updated_wl[gram_type_index + 1] + '+' + gram
        else:
            updated_wl[gram_type_index + 1] = gram
        print('Guaranteed W Gram: ' + gram)
        TIMED_MORPH_ANSWERS_ARRAY[fault_index] = updated_wl
        print(updated_wl)

def startup_time_morph():
    tm_start_btn['state'] = DISABLED
    tm_stop_btn['state'] = NORMAL
    print('STARTED UP')
    global go
    global go_counter
    global get_streak
    global reading_answers_file
    global reading_name
    global force_stop
    get_streak = tm_streak_entry.get()
    go = True
    force_stop = False
    window.update()
    print('year: '+year.get())
    if year.get() == '1':
        reading_answers_file = 'Reading Answers/THE ARK_answers.csv'
    elif year.get() == '2':
        reading_answers_file = 'Reading Answers/HERCULES CONSULTS THE ORACLE_answers.csv'
    elif year.get() == '3':
        reading_answers_file = 'Reading Answers/EIGHTH LABOR~ THE MAN-EATING HORSES OF DIOMEDES_answers.csv'
    elif year.get() == '4':
        reading_answers_file = 'Reading Answers/AENEID 1.1-1.11_answers.csv'
    print(reading_answers_file)
    reading_name = reading_answers_file[reading_answers_file.index('/')+1:reading_answers_file.index('_')]
    reading_name = reading_name.replace('~', ':')
    print(reading_name)
    login()
    time.sleep(1)
    if logged_in:
        with open(reading_answers_file, newline='', encoding='utf8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                print(row)
                if row:
                    print(row[0])
                TIMED_MORPH_ANSWERS_ARRAY.append(row)
            print(TIMED_MORPH_ANSWERS_ARRAY)
        time_morph_loop()
        go_counter = 0

def stop_time_morph():
    tm_stop_btn['state'] = DISABLED
    tm_start_btn['state'] = NORMAL
    print('STOPPED')
    global force_stop
    force_stop = True
    window.update()

def toggle_update_mode():
    global update_mode
    if update_mode:
        update_mode_switch.config(image=switch_off)
        update_mode = False
        print('update mode is: ')
        print(update_mode)
    else:
        update_mode_switch.config(image=switch_on)
        update_mode = True
        print('update mode is: ')
        print(update_mode)

def time_morph_loop():
    global go
    global go_counter
    challenges_dropdown = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/ul[3]/li[4]/h6')
    challenges_dropdown.click()
    window.update()
    time.sleep(.3)
    timedmorph_button = driver.find_element(By.NAME, 'timed_morphology')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    timedmorph_button.click()
    window.update()
    time.sleep(2)
    crowns_streak_element_text = driver.find_element(By.XPATH, '/html/body/div[6]/div[5]/div/ol/li[2]/a').text
    crowns_streak = int(crowns_streak_element_text[crowns_streak_element_text.index(': ') + 2:crowns_streak_element_text.index(': ') + 5])
    readings_selector = Select(driver.find_element(By.ID, 'whatreading'))
    readings_selector.select_by_visible_text(reading_name)
    window.update()
    time.sleep(2)
    while go:
        latin_cheat()
        time.sleep(random.uniform(1.0, 1.5))
        streak = int(driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/p[1]/strong').text)+1
        go_counter = go_counter + 1
        print('GO COUNTER: ' + str(go_counter))
        print('STREAK: ' + str(streak))
        window.update()
        try:
            if force_stop or streak == int(get_streak):
                if update_mode:
                    with open(reading_answers_file, 'w', newline='', encoding='utf8') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerows(TIMED_MORPH_ANSWERS_ARRAY)
                go = False
                tm_stop_btn['state'] = DISABLED
                tm_start_btn['state'] = NORMAL
                TIMED_MORPH_ANSWERS_ARRAY.clear()
            if streak > crowns_streak:
                go = False
                tm_stop_btn['state'] = DISABLED
                tm_start_btn['state'] = NORMAL
                TIMED_MORPH_ANSWERS_ARRAY.clear()
                beating_mr_crowns()
            window.update()
        except ValueError:
            print('You must enter an Integer into the Streak Box')

grammar_array = [['1st person', '2nd person', '3rd person'], ['singular', 'plural'], ['present', 'imperfect', 'future', 'perfect', 'pluperfect', 'future perfect'], ['indicative', 'subjunctive', 'imperative'], ['active', 'passive', 'deponent', 'not deponent', 'semi-deponent'], ['nominative', 'genitive', 'dative', 'accusative', 'ablative'], ['masculine', 'feminine', 'neuter'], ['positive', 'comparative', 'superlative'], ['participle', 'infinitive', 'gerund'], ['adverb', 'noun', 'pronoun', 'conjunction', 'adjective', 'preposition w/ abl.', 'preposition w/ acc.'], ['relative', 'demonstrative', 'interrogative', 'indefinite', 'pronominal', 'reflexive', 'possessive', 'cardinal', 'ordinal', 'intensive', 'personal pronoun'], ['dactyl', 'spondee', 'iamb', 'trochee', 'choriamb']]
TIMED_MORPH_ANSWERS_ARRAY = []
go = False
go_counter = 0
get_streak = '-1'
logged_in = False
force_stop = False
update_mode = True
reading_answers_file = ''
reading_name = ''

window = Tk()
window.title('Latin Hack-inator B)')
window.geometry('640x640+50+50')
window.resizable(0, 0)
window.configure(bg='black')
sillyd = Image.open('Images/Silly_Duck.png')
gui_sillyd = ImageTk.PhotoImage(sillyd)
sillyd_label = Label(window, image=gui_sillyd, bg='black')
tm_start_btn = Button(window, text='Initiate', command=startup_time_morph)
tm_stop_btn = Button(window, text='Terminate', command=stop_time_morph, state=DISABLED)
tm_streak_entry = Entry(window, width=6, bg='white')
username_entry = Entry(window, width=20, bg='white')
password_entry = Entry(window, width=20, bg='white')
failed_login_message = Label(text='Incorrect Username or Password', bg='black', fg='red', font=('LMRoman5', '7', 'italic'))
switch_on = ImageTk.PhotoImage(Image.open('Images/ON SWITCH.png'))
switch_off = ImageTk.PhotoImage(Image.open('Images/OFF SWITCH.png'))
update_mode_switch = Button(window, image=switch_on, bd=0, highlightthickness=0, command=toggle_update_mode)
update_mode_switch_text = Label(window, text='Update Mode', bg='black', fg='white', font=('LMRoman5', '12'))
year = StringVar()
year_choices = ['1', '2', '3', '4']
year.set(year_choices[3])
latin_year_dropdown = OptionMenu(window, year, *year_choices)
latin_year_dropdown_text = Label(window, text='Year of Latin:', bg='black', fg='white', font=('LMRoman5', '12'))
canvas = Canvas(window, width=640, height=640, bg='black')
crown = Image.open('Images/silly_crown.png')
gui_crown = ImageTk.PhotoImage(crown)

def homescreen():
    sillyd_label.place(x=-2, y=0)
    tm_streak_entry.place(x=283, y=365)
    tm_start_btn.place(x=280, y=390)
    tm_stop_btn.place(x=272, y=420)
    username_entry.place(x=10, y=590)
    password_entry.place(x=10, y=610)
    update_mode_switch.place(x=500, y=550)
    update_mode_switch_text.place(x=515, y=530)
    latin_year_dropdown.place(x=575, y=15)
    latin_year_dropdown_text.place(x=470, y=18)

def beating_mr_crowns():
    sillyd_label.place_forget()
    tm_stop_btn.place_forget()
    tm_start_btn.place_forget()
    tkinter.font.Font()
    crown_message = Label(window, text='The (2nd Place) crown is MINE now Mr. Crowns >:)', bg='black', fg='red', font=('LMRoman5', '18', 'italic'))
    canvas.pack()
    y = 0
    duck_on_can = canvas.create_image(0, y, anchor=NW, image=gui_sillyd)
    window.update()
    while y < 300:
        canvas.moveto(duck_on_can, 0, y)
        y = y+10
        time.sleep(.07)
        window.update()
    time.sleep(2)
    y = -160
    crown_on_can = canvas.create_image(110, y, anchor=NW, image=gui_crown)
    window.update()
    while y < 230:
        canvas.moveto(crown_on_can, 110, y)
        y = y+10
        time.sleep(.07)
        window.update()
    crown_message.place(x=40, y=100)
    time.sleep(20)
    sys.exit()

homescreen()
window.mainloop()