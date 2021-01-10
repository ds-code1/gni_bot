#encoding: UTF-8
import os
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

user = sys.argv[1]
password = sys.argv[2]
gni_user = sys.argv[3]
gni_password = sys.argv[4]
head = sys.argv[5]
acount_number = sys.argv[6]
do_you_wanna_wait = sys.argv[7]

option = Options()
option.headless = True
firefox_binary = FirefoxBinary('/usr/lib/firefox/firefox')

#config functions
def init_bot():
	print('initializing')
	if (head == '--headless'):
		firefox = webdriver.Firefox(options=option,firefox_binary=firefox_binary)
		return firefox
	elif (head == '--head'):
		firefox = webdriver.Firefox(firefox_binary=firefox_binary)
		return firefox
	print('initialized')

def change_ip():
	os.system('sudo anonsurf change')
	os.system('curl http://ipecho.net/plain; echo')

#essential functions
def confirm_wait():
	if (do_you_wanna_wait == "--ok"):
		input('can i continue?')
	else:
		pass

def return_page():
	print('closing page and return to gni')
	firefox.close()
	firefox.switch_to.window(firefox.window_handles[0])

def acount_select():
	sleep(5)

#login functions
def login_gni(firefox):
	print('login in: gni')
	firefox.get('https://www.ganharnoinsta.com/painel/')
	email = firefox.find_element_by_name("email")
	senha = firefox.find_element_by_name("senha")
	email.send_keys(gni_user)
	sleep(2)
	senha.send_keys(gni_password)
	sleep(1)
	senha.send_keys(Keys.ENTER)
	confirm_wait()

	print('logged')

def insta_login(firefox):
	print('login in: instagram')
	firefox.get('https://www.instagram.com/')
	sleep(4)
	permissions_detect()
	firefox.find_element_by_name('username').send_keys(user)
	firefox.find_element_by_name('password').send_keys(password)
	firefox.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button').send_keys(Keys.ENTER)
	sleep(15)
	print('logged')


#actions executables
def follow():
	try:
		obj_1 = firefox.find_element_by_xpath('//span/span[1]/button')
		obj_1.click()

		status_code = block_ip_detect()
		return status_code

	except:
		try:
			obj_2 = firefox.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/div[2]/button')
			obj_2.click()

			status_code = block_ip_detect()
			return status_code

		except:
			obj = firefox.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button')
			obj.click()

			status_code = block_ip_detect()
			return status_code

def like():
	obj_1 = firefox.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button')
	obj_1.click()

	status_code = block_ip_detect()
	return status_code


#actions config
def confirm_action():
	print('confirming actions')
	confirmar = firefox.find_element_by_id('btn-confirmar')
	confirmar.click()
	print('actions confirmed')

def access_actions():
	try:
		acessar = firefox.find_element_by_link_text('Acessar Perfil')
		acessar.click()
		return "perfil"
	except:
		acessar = firefox.find_element_by_link_text('Acessar Publicação')
		acessar.click()
		return "publication"

def initialize_actions(firefox):
	print('initializing actions')
	firefox.get("https://www.ganharnoinsta.com/painel/?pagina=sistema")  
	
	sleep(6)

	acount_select()

	button = firefox.find_element_by_id("btn_iniciar")
	button.click()
	print('actions initialized')

#detectors
def empy_list_detect():
	try:
		acessar = firefox.find_element_by_link_text('Acessar Perfil')
		return "ok"
	except:
		try:
			acessar = firefox.find_element_by_link_text('Acessar Publicação')
			return "ok"
		except:
			return "not found"

def block_ip_detect():
	try:
		firefox.find_element_by_css_selector('button.aOOlW:nth-child(2)')

		print('ip block detected!')
		return "forbiden"
	except:
		return "ok"

def permissions_detect():
	try:
		obj_1 = firefox.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]')
		obj_1.click()
	except:
		pass

#init bot
firefox = init_bot()

#loop functions
def init_sequence(firefox):
	insta_login(firefox)
	login_gni(firefox)
	sleep(7)
	initialize_actions(firefox)

def windown_count():
	try:
		firefox.switch_to.window(firefox.window_handles[-1])
		firefox.switch_to.window(firefox.window_handles[0])
		return 2
	except:
		return 1

def rescue_loop(firefox):
	firefox.switch_to.window(firefox.window_handles[0])
	firefox.close()
	firefox.switch_to.window(firefox.window_handles[-1])

	firefox.get('https://www.ganharnoinsta.com/painel/?pagina=sistema')
	sleep(3)
	initialize_actions(firefox)
	sleep(2)
	loop_sequence(firefox)

def loop_sequence(firefox):	
	while True:
		sleep(2)
		status_code = empy_list_detect()
		if (status_code == "ok"):
			type_of_action = access_actions()
			sleep(7)

			if (type_of_action == 'perfil'):
				firefox.switch_to.window(firefox.window_handles[-1])
				status_code = follow()
				sleep(9)
				return_page()
				confirm_action()
				loop_sequence(firefox)
			elif (type_of_action == 'publication'):
				firefox.switch_to_window(firefox.window_handles[-1])
				status_code = like()
				if (status_code == "ok"):
					sleep(9)
					return_page()
					confirm_action()
					loop_sequence(firefox)
				else:
					change_ip()
					firefox.quit()

					firefox = init_bot()
					init_sequence(firefox)
					sleep(2)
					try:
						loop_sequence(firefox)
					except:
						rescue_loop(firefox)

		else:
			button_search = firefox.find_element_by_xpath('//*[@id="refresh"]')
			button_search.click()
			sleep(5)
			loop_sequence(firefox)

init_sequence(firefox)
sleep(3)
try:
	loop_sequence(firefox)
except:
	rescue_loop(firefox)