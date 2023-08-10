import socket
import threading
import secrets
from tkinter import E
import el_gamal
import RSA

HOST = '192.168.210.1'

PORT = 1234 
LISTENER_LIMIT = 5
active_clients = [] 
    

def chooseMethod():
    lst = ["DES","ELGAMAL","RSA"]
    print("---------Welcome to our secure chat")
    print("1- DES (Data encryption standard)")
    print("2- ElGamal encryption system")
    print("3- RSA (Rivest–Shamir–Adleman)")
    num = input("Choose the encryption system: ")
    print(lst[int(num)-1] + " mode has been started")
    return num

def getMethod():
    return flagmethod
   

def listen_for_messages(client, username,key,elgamapublickey,rsa_string):

    while 1:

        message = client.recv(2048).decode('utf-8')
        print("RECV : ",message)
        if message != '':
           
            final_msg = username + '~' + message + '~' + key + "~" +flagmethod+"~"+elgamapublickey+"~"+rsa_string
            send_messages_to_all(final_msg)
            print("rsaaaaaaa:   ",final_msg)

        else:
            print(f"The message send from client {username} is empty")



def send_message_to_client(client, message):

    client.sendall(message.encode())
    print("SEND : ", message.encode() )

def send_messages_to_all(message):
    
    for user in active_clients:
        
        send_message_to_client(user[1], message)


def client_handler(client,key):
   
    while 1:

        username = client.recv(2048).decode('utf-8')
        print("RECV : ",username)
        if username != '':
            active_clients.append((username, client,key))
        
            key = secrets.token_hex(8).upper()
       
            n,E,D=RSA.calc() 
            print("public and private key paramters: ")
            print("n: ",n)
            print("E: ",E)
            print("D: ",D)
            print("")
            print("")
            
            rsa_string=""

            rsa_string+=str(n)
            rsa_string+=","            
            rsa_string+=str(E)
            rsa_string+=","
            rsa_string+=str(D)
            rsa_string+=","

            


            string_ints = [str(x) for x in ElgamalKey]
            elgamalpublickey = ",".join(string_ints)
            print("elgamal public key",elgamalpublickey)





            
            prompt_message = "SERVER~" + f"{username} added to the chat~" + key + "~" +flagmethod +"~" + elgamalpublickey +"~"+rsa_string 
            send_messages_to_all(prompt_message)
            
            print("Sessison key successfully generated for " + f"{username } ==>",key)

            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, key,elgamalpublickey,rsa_string, )).start()


def main():
    global ElgamalKey
    ElgamalKey = el_gamal.generate_public_key()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    global flagmethod
    flagmethod = chooseMethod()
    
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")
    
    
   
    server.listen(LISTENER_LIMIT)

   
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        key = ""
        threading.Thread(target=client_handler, args=(client,key, )).start()


if __name__ == '__main__':
    main()