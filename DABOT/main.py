# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

driver = webdriver.Chrome()


def login():
    # logs into schoology and latin app
    driver.get('https://laketravis.schoology.com/course/5128046083/materials')
    username = 'S106476'
    password = '21042004AVT'
    try:
        user_box = driver.find_element(By.NAME, 'mail')
        pass_box = driver.find_element(By.NAME, 'pass')
        user_box.send_keys(username)
        pass_box.send_keys(password)
        login_button = driver.find_element(By.NAME, 'op')
        login_button.click()
        window.update()
    except NoSuchElementException:
        print('already logged in')
    time.sleep(1)
    latin_app_button = driver.find_element(By.ID, 'app-run-364888653')
    latin_app_button.click()
    window.update()
    time.sleep(2)
    # opens latin app and opens time morphology
    driver.get('https://lthslatin.org')
    challenges_dropdown = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/ul[3]/li[4]/h6/a')
    challenges_dropdown.click()
    window.update()
    time.sleep(.3)
    timedmorph_button = driver.find_element(By.NAME, 'timed_morphology')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    timedmorph_button.click()
    window.update()
    time.sleep(2)
    # opens correct reading
    readings_selector = Select(driver.find_element(By.ID, 'whatreading'))
    readings_selector.select_by_visible_text('HERCULES CONSULTS THE ORACLE')
    window.update()
    time.sleep(2)


def latin_hackinate():
    word = driver.find_element(By.ID, 'timedMorph_form').text
    print('XXX word is: '+word+' XXX')
    gram = driver.find_element(By.ID, 'timedMorph_stimulus').text
    print('XXX grammar is: '+gram+' XXX')
    word_list = []
    # looks for word in the answers array to extract the answer list
    word_count = 0
    answer_array_found_index = -1
    for answer_list in TIMED_MORPH_ANSWERS_ARRAY:
        answer_array_found_index = answer_array_found_index + 1
        # print('DO THESE INDEXES MATCH')
        # print(TIMED_MORPH_ANSWERS_ARRAY.index(answer_list))
        # print(answer_array_found_index)
        if word in answer_list:
            word_count = word_count + 1
            word_list = answer_list
            break
        window.update()
    if word_count == 0:
        answer_array_found_index = answer_array_found_index + 1
        word_list = add_new_wordlist(word)
    # move these
    true_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[3]/div/div/form/div[1]/label')
    false_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[3]/div/div/form/div[2]/label')
    if gram in word_list:
        true_button.click()
        tf_input = True
    else:
        hit_false = True
        for att in word_list:
            # using att list instead of just att should prevent false positive noun-pronoun error
            att_list = att.split('+')
            if gram in att_list:
                true_button.click()
                tf_input = True
                hit_false = False
            window.update()
        if hit_false:
            false_button.click()
            tf_input = False
    time.sleep(.4)
    try:
        # possibly make it look for the "is" instead of the correction word
        # correction = driver.find_element(By.XPATH, '/html/body/div[6]/div[6]/h3/span/strong[2]').text
        erroris = driver.find_element(By.XPATH, 'html/body/div[6]/div[6]/h3/span/em')
        #
        # if correction == gram:
        #     print('correction: '+correction)
        #     print('word list before calling update is: ' + str(word_list))
        update_wordlist(word_list, gram, tf_input, answer_array_found_index)
        # else:
        #     print('NVM')
    except NoSuchElementException:
        print('correct')


def add_new_wordlist(word):
    # make these actual grammar values
    word_list = [word, '1st person', 'singular', 'present', 'indicative', 'active', 'nominative', 'masculine',
                 'positive', 'participle', 'adverb', 'relative', 'dactyl']
    TIMED_MORPH_ANSWERS_ARRAY.append(word_list)
    print('timed morph answers array with appended new word list: ')
    print(TIMED_MORPH_ANSWERS_ARRAY)
    return word_list


def update_wordlist(word_list, gram, tf_input, fault_index):
    updated_wl = word_list
    print('UPDATING WORD: ' + word_list[0])
    print('WORD AT FAULT INDEX: '+TIMED_MORPH_ANSWERS_ARRAY[fault_index][0])
    print('UPDATING GRAM: ' + gram)
    print('tf input is: : '+str(tf_input))
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

    # Input True and got it wrong - change grammar
    if tf_input:
        # brings list back to first element if last element is reached
        if gram_index == len(grammar_array[gram_type_index]) - 1:
            gram_index = -1
        updated_wl[gram_type_index+1] = grammar_array[gram_type_index][gram_index+1]
        TIMED_MORPH_ANSWERS_ARRAY[fault_index] = updated_wl
        print(updated_wl)
    window.update()
    # Input False and got it wrong - Guaranteed W THIS ONE WORKS/UPDATES PROPERLY
    if not tf_input:
        mgrams_list = updated_wl[gram_type_index+1].split('+')
        print('000000000000 MGRAMS LIST: ')
        print(mgrams_list)
        if grammar_array[gram_type_index].index(gram) < grammar_array[gram_type_index].index(mgrams_list[-1]):
            updated_wl[gram_type_index + 1] = updated_wl[gram_type_index + 1]+'+'+gram
        else:
            updated_wl[gram_type_index+1] = gram
        print('Guaranteed W Gram: '+gram)
        TIMED_MORPH_ANSWERS_ARRAY[fault_index] = updated_wl
        print(updated_wl)


grammar_array = [['1st person', '2nd person', '3rd person'],
                 ['singular', 'plural'],
                 ['present', 'imperfect', 'future', 'perfect', 'pluperfect', 'future perfect'],
                 ['indicative', 'subjunctive', 'imperative'],
                 ['active', 'passive', 'deponent', 'not deponent', 'semi-deponent'],
                 ['nominative', 'genitive', 'dative', 'accusative', 'ablative'],
                 ['masculine', 'feminine', 'neuter'],
                 ['positive', 'comparative', 'superlative'],
                 ['participle', 'infinitive', 'gerund'],
                 ['adverb', 'noun', 'pronoun', 'conjunction', 'adjective', 'preposition w/ abl.', 'preposition w/ acc.'],
                 ['relative', 'demonstrative', 'interrogative', 'indefinite', 'reflexive', 'cardinal', 'ordinal',
                  'intensive',
                  'pronominal', 'possessive'],
                 ['dactyl', 'spondee', 'iamb', 'trochee', 'choriamb']]

TIMED_MORPH_ANSWERS_ARRAY = []

#
#
#
#
# Run ------------------------------------------------------------------------------------------------------------------

go = False
go_counter = 0
input_tot = '0'


def startup():
    start_btn['state'] = DISABLED
    stop_btn['state'] = NORMAL
    print('STARTED UP')
    global go
    global go_counter
    global input_tot
    input_tot = entry.get()
    go = True
    window.update()
    login()
    time.sleep(1)
    # Takes all values from csv file and puts them in 2d array (TIMED_MORPH_ANSWERS_ARRAY)
    with open('timedmorphAnswers.csv', newline='', encoding='utf8') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            print(row)
            if row:
                print(row[0])
            TIMED_MORPH_ANSWERS_ARRAY.append(row)
        print(TIMED_MORPH_ANSWERS_ARRAY)
    cheat_loop()
    go_counter = 0


def stop():
    stop_btn['state'] = DISABLED
    start_btn['state'] = NORMAL
    print('STOPPED')
    global go_counter
    go_counter = int(input_tot)-1
    window.update()


def cheat_loop():
    global go
    global go_counter
    while go:
        latin_hackinate()
        go_counter = go_counter + 1
        print('GO COUNTER: '+str(go_counter))
        window.update()
        time.sleep(1.5)
        if go_counter == int(input_tot):
            with open('timedmorphAnswers.csv', 'w', newline='', encoding='utf8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(TIMED_MORPH_ANSWERS_ARRAY)
            go = False
            TIMED_MORPH_ANSWERS_ARRAY.clear()
            print('Empty answers array: ')
            print(TIMED_MORPH_ANSWERS_ARRAY)
        window.update()


# Makes GUI
window = Tk()
window.title('Latin Hack-inator')
window.geometry('320x320')
image1 = Image.open('Silly_Duck.png')
gui_image = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(image=gui_image)
label1.image = gui_image
label1.place(x=0, y=0)
entry = Entry(window, width=6, bg="white")
start_btn = Button(window, text='Initiate', command=startup)
start_btn.place(x=140, y=200)
stop_btn = Button(window, text='Terminate', command=stop, state=DISABLED)
stop_btn.place(x=132, y=230)
entry.place(x=143, y=170)
print('Input tot: '+input_tot)
window.mainloop()
