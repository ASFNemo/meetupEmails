import socket
import argparse
import os
import time
import urlparse
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import  sleep
import random
from random import randint


groups_visited = {}
groups_to_visit = []
group_request_sent = 0

def main():

    browser = webdriver.Firefox()
    browser.get("https://secure.meetup.com/login/")

    time.sleep(3)

    login(browser)


def login(browser):
    globals()
    argparser = argparse.ArgumentParser()
    argparser.add_argument("username", help="meetup username")
    argparser.add_argument("password", help="meetup password")
    arguments = argparser.parse_args()

    print "about to enter username and password"

    enter_email = browser.find_element_by_xpath("//*[@id=\"email\"]")
    enter_email.send_keys(arguments.username)
    enter_password =  browser.find_element_by_xpath("//*[@id=\"password\"]")
    enter_password.send_keys(arguments.password)

    enter_password.submit()

    print "login should be complete"


def get_groups(browser):

    '''
        get_groups() scrapes the links of all the groups on that page and puts sorts them. those that have been seen
        previously are disgarded, otherwise they are added to our list.
    :param browser:  the page we will be scraping
    :return:
    '''

    page_source = BeautifulSoup(browser.page_source, "html.parser")

    links = []

    for link in page_source.find_all('a'):
        if 'groupCard--photo' in str(page_source.get('class')):
            group_url = page_source.get('href')
            if group_url not in links:
                links.append(group_url)

    for link in links:
        if link not in groups_visited:
            groups_to_visit.append(group_url)
            groups_visited[group_url] = 1


def visit_group(browser):
    if groups_to_visit:
        visit = random.choice(groups_to_visit)
        browser.get(visit)

    random_int = randint(0,99)

    if random_int > 83 or random_int == 44:
        join_group(browser, visit)
        groups_to_visit.remove(visit)


def join_group(browser, link):
    join = link + 'join/'
    browser.get(join)

    if browser.current_url is join:
        browser.get("http://www.meetup.com")
    elif browser.current_urld is (link + "quick_join/"):
        answer_join_questions(browser)
        browser.get("http://www.meetup.com")


def answer_join_questions(browser):
    '''
    check aprox what the question is asking and give generic answer
    :param browser: the page we are on
    :return:
    '''

    page_source = BeautifulSoup(browser.page_source, "html.parser")

    for question in page_source.find_all('label'):
        answer = response(question.text)
        # work out how to make sure that the next tag is a textarea
        textarea = question.find_next_siblings('textarea')
        textarea_id = textarea.get('id')
        input_box = browser.find_element_by_id(textarea_id)
        input_box.send_keys(answer)

    join = browser.find_element_by_type('intro_questions_button').click
    join.click()


def response(question):

    '''
    this will create all manner of responses to a wide veriety of questions that may be asked by a group when joining
    :param question:
    :return:
    '''

    question = question.lower()
    words = question.split(" ")

    # ADD MORE ANSWERS AS DIFFERENT QUESTIONS ARE FOUND
    if (('where' or "how" or "who") and ('hear' or 'find')) in words:
        final_response = 'a freind of mine told me about it'
    elif ("name" and ('your' or "real")) in words:
        final_response = "James Crownston"
    elif (("town" or "city" or 'area') and ("live" or 'where' or 'home')) in words:
        final_response = "New York but I travel around the world more then I am at home due to my job"
    else:
        final_response = "Honestly, I am in a slight rush right now. I will come back and answer properly later. Sorry"

    return final_response


'''
    CREATES THE SOCKET USED TO TALK TO THE SERVER
'''
HOST = "127.0.0.1"
PORT = 10007

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

main()
