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


def reader_main():

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("email", help="gmail email")
    argument_parser.add_argument("password", help="gmail password")
    arguments = argument_parser.parse_args()

    browser = webdriver.Firefox()
    go_to_page(browser, "https://accounts.google.com/ServiceLogin?service=mail&continue=https:"
                        + "//mail.google.com/mail/#identifier")

    enter_email(browser, arguments.email)
    enter_password(browser, arguments.password)

    if browser.current_url is not "https://mail.google.com/mail/#inbox":
        go_to_page(browser, "https://mail.google.com/mail/#inbox")


def go_to_page(browser, url):
    browser.get(url)

    time.sleep(3)


def enter_email(browser, email):

    email_enter = browser.find_element_by_xpath("//*[@id=\"Email\"]")
    email_enter.send_keys(email)
    email_enter.submit()

    time.sleep(3)


def enter_password(browser, password):

    password_enter = browser.find_element_by_xpath("//*[@id=\"Passwd\"]")
    password_enter.send_keys(password)
    password_enter.submit()

    time.sleep(3)


reader_main()
