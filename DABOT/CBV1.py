from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import csv
import time
import sys
import tkinter
import tkinter.font
from tkinter import *
from PIL import ImageTk, Image
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

s = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, service=s)

def login():
    driver.get('https://laketravis.schoology.com/course/5128046083/materials')
    # username = 'S11077'
    username = input('Username: ')
    password = input('Password: ')
    try:
        user_box = driver.find_element(By.NAME, 'mail')
        pass_box = driver.find_element(By.NAME, 'pass')
        user_box.send_keys(username)
        pass_box.send_keys(password)
        login_button = driver.find_element(By.NAME, 'op')
        login_button.click()
        time.sleep(0.5)
        try:
            login_failed = driver.find_element(By.CLASS_NAME, 'messages error')
            print('incorrect login')
        except NoSuchElementException:
            print('logging in')
    except NoSuchElementException:
        print('already logged in')
    time.sleep(1)
    latin_app_button = driver.find_element(By.ID, 'app-run-364888653')
    latin_app_button.click()
    time.sleep(2)
    driver.get('https://lthslatin.org')

def ciple_cheeze():
    global x
    login()
    challenges_dropdown = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/ul[3]/li[4]/h6/a')
    challenges_dropdown.click()
    time.sleep(.3)
    ciples_button = driver.find_element(By.NAME, 'party')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    ciples_button.click()
    link = "https://latinlexicon.org/word_study_tool.php"
    driver.execute_script("window.open('{}');".format(link))
    time.sleep(1)
    tabs = driver.window_handles
    driver.switch_to.window(tabs[0])
    wait = True
    while wait:
        try:
            header_text = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/h1').text
            wait = False
        except NoSuchElementException:
            print('waiting')
            time.sleep(2)
    level = int((header_text[-2:-1]))
    get_words(level)
    print(noun_list)
    print(participle_list)
    driver.switch_to.window(tabs[1])
    answers = []
    for w in range(0, 5):
        driver.get("https://latinlexicon.org/word_study_tool.php")
        word_input_box = driver.find_element(By.XPATH, '/html/body/form/div/label/textarea')
        search = driver.find_element(By.NAME, 'iSubmit')
        word_input_box.send_keys(noun_list[w] + ' ' + participle_list[w])
        search.click()
        time.sleep(1)
        print(noun_list[w] + ':')
        gcn_lists = (get_gcn_lists())
        participle_tab = driver.find_element(By.XPATH, '/html/body/div[2]/div[4]/div/div[2]')
        participle_tab.click()
        time.sleep(1)
        paradigm_link = get_paradigm()
        driver.get(paradigm_link)
        answers.extend(get_answers(gcn_lists))
    print(answers)
    driver.switch_to.window(tabs[0])
    solve(answers)

noun_list = []
participle_list = []

def get_words(level):
    if level <= 5:
        for x in range(1, 22, 5):
            try:
                participle = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div/div['+str(x)+']/h6').text
                participle_list.append(participle)
            except NoSuchElementException:
                print('no principle parts')
    for row in range(1, 6):
        for b in range(1, 5):
            box = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div[' + str(row * 4 + b) + ']/div/input')
            text = box.get_attribute('value')
            if ' ' in text:
                noun = text[0:text.index(' ')]
                participle = text[text.index(' ')+1:]
            else:
                noun = text
            if noun not in noun_list:
                noun_list.append(noun)
            if participle not in participle_list and len(participle_list) < 5:
                participle_list.append(participle)

def get_gcn_lists():
    gram_box = 0
    entry_error = 0
    gender_case_number_list = []
    search_cards = driver.find_elements(By.CLASS_NAME, 'search_card')
    for search_card in search_cards:
        search_card_text = search_card.text
        try:
            if driver.find_element(By.XPATH,'/html/body/div[3]/div[' + str(2 + gram_box * 6 + entry_error) + ']').get_attribute('class') == 'entry_error':
                entry_error += 1
        except NoSuchElementException:
            'no entry error'
        if 'noun' in search_card_text:
            r = 1
            while True:
                try:
                    lex_gram_text = driver.find_element(By.XPATH,'/html/body/div[3]/div[' + str(2 + gram_box*6 + entry_error) + ']/div[' + str(r) + ']').text.split(' ')
                    print(lex_gram_text)
                    gender_case_number_list.append(lex_gram_text)
                except NoSuchElementException:
                    print('out of gcn texts\n')
                    break
                r += 1
        else:
            gram_box += 1
    return gender_case_number_list

def get_paradigm():
    gram_box = 0
    entry_error = 0
    paradigm_links = driver.find_elements(By.XPATH, '//*[@id="paradigm_container"]/label/a')
    search_cards = driver.find_elements(By.CLASS_NAME, 'search_card')
    for search_card in search_cards:
        search_card_text = search_card.text
        try:
            if driver.find_element(By.XPATH, '/html/body/div[3]/div[' + str(2 + gram_box * 6 + entry_error) + ']').get_attribute('class') == 'entry_error':
                entry_error += 1
        except NoSuchElementException:
            'no entry error'
        if 'verb' in search_card_text:
            print('paradigm link: ' + paradigm_links[gram_box].text)
            paradigm_link = paradigm_links[gram_box].get_attribute('href')
            break
        else:
            gram_box += 1
    return paradigm_link

def get_answers(gcn):
    gcn_lists = gcn
    row_answers = []
    for div in range(4, 8):
        possible_forms = []
        for lst in gcn_lists:
            try:
                possible_form = driver.find_element(By.XPATH, '/html/body/div[3]/div[' + str(div) + ']/table[' + str(genders.index(lst[0]) + 1) + ']/tbody/tr[' + str(cases.index(lst[1]) + 2) + ']/td[' + str(numbers.index(lst[2]) + 2) + ']').text
            except NoSuchElementException:
                print('missing in latin lexicon')
                break
            if ' ' in possible_form:
                shortened_form_c = possible_form[0:possible_form.index(',')]
                shortened_form_s1 = possible_form[possible_form.index(' ') + 1:]
                shortened_form_s2 = shortened_form_s1[0:shortened_form_s1.index(' ')]
                possible_form = shortened_form_c
                possible_form2 = shortened_form_s2
                if possible_form2 not in possible_forms and len(possible_form) > 0:
                    possible_forms.append(possible_form2)
            if possible_form not in possible_forms and len(possible_form) > 0:
                possible_forms.append(possible_form)
                if 'i' in possible_form:
                    possible_forms.append(possible_form.replace('i', 'j'))
        if len(possible_forms) > 0:
            row_answers.append(possible_forms)
    return row_answers

def solve(ansr_list):
    submit_button = driver.find_element(By.ID, 'inffeedback')
    submit_button.click()
    time.sleep(0.5)
    for z in range(0,10):
        for row in range(1, 6):
            for box in range(1, 5):

                entry_box = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div[' + str(row * 4 + box) + ']/div/input')
                print('data color: ')
                print(entry_box.get_attribute('data-color'))
                if entry_box.get_attribute('data-color') == 'seagreen':
                    print('CORRECT')
                elif entry_box.get_attribute('data-color') == 'red':
                    print('it was wrong')
                    value = entry_box.get_attribute('value')
                    if ' ' in value:
                        noun = value[0:value.index(' ')]
                    else:
                        noun = value
                    try:
                        part_form = ansr_list[(row - 1) * 4 + (box - 1)].pop(0)
                        print(part_form)
                        part_form = part_form.replace('ē', 'e')
                        part_form = part_form.replace('ō', 'o')
                        part_form = part_form.replace('ī', 'i')
                        part_form = part_form.replace('ā', 'a')
                        part_form = part_form.replace('ū', 'u')
                    except IndexError:
                        print('lalala')
                    if len(part_form) > 0:
                        for bs in range(0, 40):
                            entry_box.send_keys(Keys.BACKSPACE)
                        entry_box.send_keys(noun + ' ')
                        entry_box.send_keys(part_form)
            submit_button.click()
            if driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/h3').text == 'Level Up!':
                print('#1 Victory Royale')
                sys.exit()
        time.sleep(0.5)

genders = ['masculine', 'feminine', 'neuter']
cases = ['nominative', 'genitive', 'dative', 'accusative', 'ablative', 'vocative']
numbers = ['singular', 'plural']

ciple_cheeze()