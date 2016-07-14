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


'''
    CREATES THE SOCKET USED TO TALK TO THE SERVER
'''
HOST = "127.0.0.1"
PORT = 10007

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

main()
