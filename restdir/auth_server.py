
import socket, sys, argparse

class Server():
    def run(self, args): # [token,puerto,direcdión,ruta]
        HOST = args[2]  
        PORT = args[1]

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.listen()
        
        try:
         s.bind((HOST, PORT))
        except socket.error as msg:
         print('# Bind failed. ')
         sys.exit()

        



if __name__ == "__main__":
    if len(sys.argv) > 4:
        print("Error, muchos argumentos ?")
        sys.exit()
        
    args = list()
    token = #generar token random
    puerto = 3002
    direccion = "0.0.0.0"
    ruta = #currrent dir
    
    parser = argparse.ArgumentParser(description="Restdir arguments")
    parser.add_argument("-a", "--admin", action='store', const=token, type=str)
    parser.add_argument("-p", "--port",  action='store', const=puerto, type=int)
    parser.add_argument("-l", "--listening", action='store', const=direccion, type=str)
    parser.add_argument("-d", "--db",  action='store', const=ruta, type=str)
    
    args = parser.parse_args()
    
    Server.run(args)

    