import http.client

def httpMetodiAb(ip, porta, path):
	try:
		connection = http.client.HTTPConnection(ip, porta)
		connection.request('OPTIONS', path)
		response = connection.getresponse()
		allow_header = response.getheader('allow')
		if allow_header:
			methods = allow_header.split(',')
			print("I metodi abilitati sono:")
			for method in methods:
				print(method.strip())
		else:
			print("Intestazione 'allow' non presente nella risposta.")
			methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
			print("I metodi abilitati non sono specificati dall'intestazione. Si procederà con una serie di richieste per determinare i metodi supportati.")
			for method in methods:
				connection = http.client.HTTPConnection(ip, porta)
				connection.request(method, path)
				response = connection.getresponse()
				if response.status == 200:
					print(f"Il metodo {method} è supportato")
				elif response.status == 405:
					print(f"Il metodo {method} non è supportato")
		connection.close()
		
	except ConnectionRefusedError as e:
		print("Connessione fallita:")
		print(e)


if __name__ == "__main__":

	ip = input("Inserire IP/ip del target: ")
	porta = input("Inserire la porta del target (default: 80): ")
	path = input("Inserire un path da scansionare: (default: /) ")
	if path == "":
		path="/"

	if porta == "":
		porta = 80
	httpMetodiAb(ip, porta, path)
		

