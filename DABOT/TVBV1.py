from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import random
import re
import tkinter
from tkinter import *
from PIL import ImageTk, Image

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

def login():
    global logged_in
    if group_color.get() == 'Green':
        driver.get('https://laketravis.schoology.com/group/2278334531')
    elif group_color.get() == 'Purple':
        driver.get('https://laketravis.schoology.com/group/2278353920')
    elif group_color.get() == 'Blue':
        driver.get('https://laketravis.schoology.com/group/2278336525')
    elif group_color.get() == 'Orange':
        driver.get('https://laketravis.schoology.com/group/2278336525')
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
    raw_word_text = driver.find_element(By.ID, 'timedVocab_lemma').text
    words = re.split(', |\\n', raw_word_text)
    temp_parts_list = []
    for parts in words:
        if parts.find('.') != -1 or parts.find('-') != -1:
            temp_parts_list.append(parts)
    for i in temp_parts_list:
        words.remove(i)
    definition = driver.find_element(By.ID, 'timedVocab_def').text
    word_list = []
    word_count = 0
    answer_array_found_index = -1
    permit = True

    abort = False
    for word_defs in TIMED_VOCAB_ANSWERS_ARRAY:
        def_found = True
        answer_array_found_index += 1
        for word in words:
            if word not in word_defs:
                def_found = False
                break
        if def_found:
            word_list = word_defs
            break
    """
    for answer_list in TIMED_VOCAB_ANSWERS_ARRAY:
        temp_array = answer_list
        if permit:
            answer_array_found_index = answer_array_found_index + 1
        for x in temp_array:
            entry = x
            for single_word in words:
                if single_word == entry and permit:
                    word_count = word_count + 1
            window.update()
        if word_count >= len(words) - 1 and permit:
            word_list = answer_list
            permit = False
    """
    if word_list == []:
        answer_array_found_index = answer_array_found_index + 1
        word_list = add_new_wordlist(words)
    true_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[3]/div/div/form/div[1]/label')
    false_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[3]/div/div/form/div[2]/label')
    time.sleep(0.2)
    if definition in word_list:
        true_button.click()
        tf_input = True
    else:
        false_button.click()
        tf_input = False
    time.sleep(2)

    try:
        correct_answer_string = ''
        try:
            correct_answer_string = driver.find_element(By.XPATH, '/html/body/div[6]/div[6]/h3/span[1]/em[1]/strong').text
        except:
            correct_answer_string = driver.find_element(By.XPATH, '/html/body/div[6]/div[6]/h3/span[1]/em/strong').text
        correct_answers = correct_answer_string.split(', ')
        update_wordlist(word_list, answer_array_found_index, correct_answers)
    except NoSuchElementException:
        pass
    # print(TIMED_VOCAB_ANSWERS_ARRAY)

def add_new_wordlist(words):
    word_list = words
    TIMED_VOCAB_ANSWERS_ARRAY.append(word_list)
    return word_list

def update_wordlist(word_list, fault_index, correct_answers):
    updated_wl = word_list
    for all_def in correct_answers:
        try:
            if updated_wl.index(all_def) != -1:
                break
        except:
            updated_wl.append(all_def)
    TIMED_VOCAB_ANSWERS_ARRAY[fault_index] = updated_wl

def startup_time_vocab():
    tm_start_btn['state'] = DISABLED
    tm_stop_btn['state'] = NORMAL
    print('STARTED UP')
    global go
    global go_counter
    global get_streak
    global timedvocab_answers_file
    global force_stop
    get_streak = tm_streak_entry.get()
    go = True
    force_stop = False
    window.update()
    timedvocab_answers_file = 'Timed Vocab Bot/timedvocab_answers.csv'
    login()
    time.sleep(1)
    if logged_in:
        with open(timedvocab_answers_file, newline='', encoding='utf8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                TIMED_VOCAB_ANSWERS_ARRAY.append(row)
        time_vocab_loop()
        go_counter = 0

def stop_time_vocab():
    tm_stop_btn['state'] = DISABLED
    tm_start_btn['state'] = NORMAL
    print('STOPPED')
    global force_stop
    force_stop = True
    window.update()

def time_vocab_loop():
    global go
    global go_counter
    global TIMED_VOCAB_ANSWERS_ARRAY
    challenges_dropdown = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/ul[3]/li[4]/h6')
    challenges_dropdown.click()
    window.update()
    time.sleep(.3)
    timedvocab_button = driver.find_element(By.NAME, 'timed_vocab')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    timedvocab_button.click()
    window.update()
    time.sleep(2)
    while go:
        latin_cheat()
        time.sleep(random.uniform(.1, .5))
        streak = int(driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/p[1]/strong').text) + 1
        go_counter = go_counter + 1
        print('GO COUNTER: ' + str(go_counter))
        window.update()
        try:
            if force_stop or streak == int(get_streak):
                dup_free_list = []
                for i in TIMED_VOCAB_ANSWERS_ARRAY:
                    if i not in dup_free_list:
                        dup_free_list.append(i)
                TIMED_VOCAB_ANSWERS_ARRAY = dup_free_list[:]
                with open(timedvocab_answers_file, 'w', newline='', encoding='utf8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(TIMED_VOCAB_ANSWERS_ARRAY)
                go = False
                tm_stop_btn['state'] = DISABLED
                tm_start_btn['state'] = NORMAL
                TIMED_VOCAB_ANSWERS_ARRAY.clear()
            window.update()
        except ValueError:
            print('You must enter an Integer into the Streak Box')

TIMED_VOCAB_ANSWERS_ARRAY = []
go = False
go_counter = 0
get_streak = '-1'
logged_in = False
force_stop = False
timedvocab_answers_file = ''

window = Tk()
window.title('Agguire cry-inator V1')
window.geometry('640x640+50+50')
window.resizable(0, 0)
window.configure(bg='white')
sillyd = Image.open('Images/Cry.png')
gui_sillyd = ImageTk.PhotoImage(sillyd)
sillyd_label = Label(window, image=gui_sillyd, bg='white')
tm_start_btn = Button(window, text='Initiate', command=startup_time_vocab)
tm_stop_btn = Button(window, text='Terminate', command=stop_time_vocab, state=DISABLED)
tm_streak_entry = Entry(window, width=6, bg='white')
username_entry = Entry(window, width=20, bg='white')
password_entry = Entry(window, width=20, bg='white')
failed_login_message = Label(text='Incorrect Username or Password', bg='red', fg='black', font=('LMRoman5', '7', 'italic'))
group_color = StringVar()
group_color_choices = ['Green', 'Purple', 'Blue', 'Orange']
group_color.set(group_color_choices[0])
latin_group_color_dropdown = OptionMenu(window, group_color, *group_color_choices)
latin_group_color_dropdown_text = Label(window, text='Group Color: ', bg='white', fg='black', font=('LMRoman5', '12'))
canvas = Canvas(window, width=640, height=640, bg='grey')

def homescreen():
    sillyd_label.place(x=-2, y=0)
    tm_streak_entry.place(x=283, y=365)
    tm_start_btn.place(x=280, y=390)
    tm_stop_btn.place(x=272, y=420)
    username_entry.place(x=10, y=590)
    password_entry.place(x=10, y=610)
    latin_group_color_dropdown.place(x=555, y=15)
    latin_group_color_dropdown_text.place(x=450, y=18)

homescreen()
window.mainloop()