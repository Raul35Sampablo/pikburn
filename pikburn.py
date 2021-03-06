#!/usr/bin/python
#Importamos las clases de PySide

#revisar https://github.com/shuge/Qt-Python-Binding-Examples/tree/master/common_widgets
# REVISAR https://electrocrea.com/blogs/tutoriales/como-usar-programador-de-pic-k-150

import sys
#para conocer el puerto donde esta conectado
from serial.tools.list_ports import comports
import subprocess

try:
    from PySide import QtCore
    from PySide import QtGui
except ImportError:
    from PyQt4 import QtCore
    from PyQt4 import QtGui




class Demo(QtGui.QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        
        #layout = QVBoxLayout(self)
        

        x, y, w, h = 500, 200, 300, 400
        self.setGeometry(x, y, w, h)


        
        combo = QtGui.QComboBox(self)
        #movemos combo (x,y)
        combo.move(480, 292)
        #seteamos el numero masximo de items que se pueden ver en el combo
        combo.setMaxVisibleItems(5)

        combo.currentIndexChanged.connect(self._cb_currentIndexChanged)
        combo.highlighted.connect(self._cb_highlighted)

        #items = ('', 'PIC16F83', 'PIC16F84', 'PIC16F84A', 'PIC16F87')
        items = ('','PIC12F508', 'PIC12F509', 'PIC12F635', 'PIC12F675', 'PIC12F683', 'PIC16F505', 'PIC16F506', 'PIC16F54', 'PIC16F57', 'PIC16F59', 'PIC16F627',
                 'PIC16LF627A', 'PIC16F627A', 'PIC16F628', 'PIC16LF628A', 'PIC16F628A', 'PIC16F630', 'PIC16F631', 'PIC16F636', 'PIC16F636-1', 'PIC16F639', 'PIC16F648A',
                 'PIC16F676', 'PIC16F677', 'PIC16F677-1', 'PIC16F684', 'PIC16F685', 'PIC16F685-1', 'PIC16F687', 'PIC16F687', 'PIC16F687-1', 'PIC16F688', 'PIC16F689',
                 'PIC16F689-1', 'PIC16F690', 'PIC16F690-1', 'PIC16F716', 'PIC16F72', 'PIC16F73', 'PIC16F74','PIC16F76', 'PIC16F77', 'PIC16F737', 'PIC16F747', 'PIC16F767',
                 'PIC16F777', 'PIC16F83', 'PIC16F84', 'PIC16F84A', 'PIC16F87', 'PIC16F88', 'PIC16F818', 'PIC16F819', 'PIC16F870', 'PIC16F871', 'PIC16F872', 'PIC16F873',
                 'PIC16F873A', 'PIC16LF873A', 'PIC16F874', 'PIC16F874A', 'PIC16F876', 'PIC16F876A', 'PIC16F877', 'PIC16F877A')
        combo.addItems(items)
        
        
# TODAS LAS TEXT EDIT
        #pantalla=QtGui.QTextEdit(self)
        #pantalla.setGeometry(QtCore.QRect(10, 0, 460, 266))
        #pantalla.setObjectName("pantalla")
        #pantalla.setText("Aqui van el archivo HEX \n falta mostrar el numero de linea esta aqui https://stackoverflow.com/questions/40386194/create-text-area-textedit-with-line-number-in-pyqt.")
        #pantalla.setStyleSheet("background-color: black;")        
        #self.pantalla.setStyleSheet("background-color: transparent;")

        self.pantalla=QtGui.QTextEdit(self)
        self.pantalla.setGeometry(QtCore.QRect(10, 0, 460, 266))
        self.pantalla.setObjectName("pantalla")
        self.pantalla.setText("Aqui van el archivo HEX, pero en binario y los numeros en la izquierada tambien son binario \n falta mostrar el numero de linea esta aqui https://stackoverflow.com/questions/40386194/create-text-area-textedit-with-line-number-in-pyqt.")
        self.pantalla.setStyleSheet("background-color: black;")        
        #self.pantalla.setStyleSheet("background-color: transparent;")
        
# TODAS LAS LABELS
        
        #label 
        label1 = QtGui.QLabel(self)
        label1.setText("Chip Selector:")
        label1.move(480, 271)
        
        # label autor y version
        lversion = QtGui.QLabel(self)
        lversion.setText("PikBurn V. Alpha 0.001     Developed by: Ronal Forero")
        lversion.move(10, 430)
        
        #label de la tarje
        #lboard = QtGui.QLabel(self)

        #label de Mensajes de ERORR o EXITO, mesajes filtraos de la terminal
        self.msg = QtGui.QLabel("Dispositivo K150 no conectado",self)
        self.msg.setStyleSheet("QLabel { background-color : black; color : red; }")
        self.msg.move(10, 274)        
        
      
        #label del puerto USB
        self.lusb = QtGui.QLabel("Port:                                                     ",self)
        self.lusb.move(100, 304)
        #self.lusb= QtGui.QLabel("f")
        #lusb.move(0, 271)

        #lusb.move(0,228)
        #lboard = QtGui.QLabel(self)
        #lboard.setText("Chip Selector:")
        #lboard.move(30, 10)  


        
        # Imiagen posicion del PIC en el ZIF
        self.label=QtGui.QLabel(self)
        self.label.setPixmap(QtGui.QPixmap("SOCKETS.png"))
        self.label.move(470, 0)

        #self.bconect= QtGui.QPushButton("Conectar",self)
        #self.bconect.clicked.connect(self.port)
        #self.bconect.move(10, 10)        
            
        #Icono en la ventana
        self.setWindowIcon(QtGui.QIcon('PikBurn3.png'))    
        
        #label 
        #label1 = QtGui.QLabel(self)
        #label1.setText("Chip Selector:")
        #label1.move(480, 271)
        


# TODOS LOS BOTONES

        # boton conectar
        self.bconect= QtGui.QPushButton("Conectar",self)
        self.bconect.clicked.connect(self.port)
        self.bconect.move(10, 300)
        
        # boton Load
        self.bload= QtGui.QPushButton("Load",self)
        self.bload.clicked.connect(self.load_file_hex)
        self.bload.move(10, 340)        
        
        # boton Merge
        self.bmerge= QtGui.QPushButton("Merge",self)
        self.bmerge.clicked.connect(self.port)
        self.bmerge.move(110, 340)
        
        # boton Program
        self.bprogram= QtGui.QPushButton("Program",self)
        self.bprogram.clicked.connect(self.port)
        self.bprogram.move(210, 340)
        
        # boton Verify
        self.bverify= QtGui.QPushButton("Verify",self)
        self.bverify.clicked.connect(self.port)
        self.bverify.move(310, 340)
        
        # boton Refresh
        self.brefresh= QtGui.QPushButton("Refresh",self)
        self.brefresh.clicked.connect(self.load_file_hex)
        self.brefresh.move(10, 390)        
        
        # boton Save
        self.bsave= QtGui.QPushButton("Save",self)
        self.bsave.clicked.connect(self.port)
        self.bsave.move(110, 390)
        
        # boton Read
        self.bread= QtGui.QPushButton("Read",self)
        self.bread.clicked.connect(self.port)
        self.bread.move(210, 390)
        
        # boton Blank
        self.bblank= QtGui.QPushButton("Blank",self)
        self.bblank.clicked.connect(self.port)
        self.bblank.move(310, 390)
        
        
# BARRA DE PROGRESO
        self.bar=QtGui.QProgressBar(self)
        self.bar.move(489, 416)
        
        
        
        
        
    def text_change(self):       
        print("change ok")
    
    def text_click(event):
        print("clicked ok ")
        
# Funcion para conocer la posicion del combobox del selector de pic
    def _cb_currentIndexChanged(self, idx):
        print ('current selected index:', idx)
        #Chequear esto.. porque cada vez que se agreguen pics por encima de los establecidos esots numeros cambian
        # si la posicion es 1 y 2 entre.. esas posiciones las vemos en la terminal por el print
        if idx in (8,16,49,50) :
            #PIC16F84A  PIC16F87 PIC16F628A PIC16F54
            pixmap=QtGui.QPixmap('PIN18.png')
            self.label.setPixmap(pixmap)
        elif idx == 6 :   
            pixmap=QtGui.QPixmap('PIN1413.png')
            self.label.setPixmap(pixmap)
        elif idx == 65 :   
            #PIC16F877A
            pixmap=QtGui.QPixmap('PIN40.png')
            self.label.setPixmap(pixmap)
        #else:#solo se muestra el zirf
            #pixmap=QtGui.QPixmap('SOCKETS.png')
            #self.label.setPixmap(pixmap)
            
            #probamos cambiando color del boton
            self.bconect.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
            



    def _cb_highlighted(self, idx):
        print ('highlighted index:', idx)
        

    def port(self,algo):
            print("Entro al boton")
            #self.setText("Chip :")
            
            
# Funcion para cargar archivos HEX
#loader = QUiLoader()

#file = QFile(":/forms/myform.ui")

#file.open(QFile.ReadOnly)

#myWidget = loader.load(file, self)

#file.close()
            
            
                
    def load_file_hex(self):

        fname = QtGui.QFileDialog.getOpenFileName()
        ruta_load=fname[0]
        print(type(ruta_load))
        ruta_load_str=''.join(ruta_load)
        #leemos el archivo HEX
        leer_file=open(ruta_load,'r')
        texto=leer_file.read()
        leer_file.close()
        #Convertimos hex a binario
        #n_bits=8
        #scale=16
        #texto_bin=bin(int(texto, scale))[2:].zfill(num_of_bits)
        #decimal=int(texto,16)
        #texto_bin=bin(decimal)
        #setiamos en la pantalla
        self.pantalla.setText(texto)  
        #self.pantalla.setText.toPlainText(fname)            
            
            
        
    #Funcion para conocer el puerto y el nombre de manufactura
    def port(self):
        #Aqui vemos la direccion /dev/tty****
        puerto=sorted( x[0] for x in comports() )
        print (puerto)
        puerto= ''.join(puerto)
        print (puerto)
        
        #limpiamos para que no hallan mensajes montadas
        puerto= puerto + "                               "
        print (puerto)
        #Buscamos la ide
        ruta_id=sorted( x[2] for x in comports() )
        #Convertimos de list a string
        ruta_id= ''.join(ruta_id)
        
        #puerto usb
        self.lusb.setText(puerto)


        #Validamos si hay algo conectado
        status_conect=sorted( x[0] for x in comports() )
        if (status_conect == []):
            conexion= int(0)
            puerto= "Dispositivo K150 No conectado"
            board= " "
            self.msg.setText(puerto)                                                                                     
            #name_board = Label(ventana, text =board).place(x=90, y=94)

        else:
            conexion= int(1)
            #Buscamos el numero ID del puerto
            id1=ruta_id.rindex(":")
            id2=id1 + 1
            id3= id1 + 5
            id_puerto=ruta_id[id2:id3]
            #Buscamos el nombre de la empresa manufacturera a partir del ID
            ruta_name_port= subprocess.check_output( "lsusb", stderr=subprocess.STDOUT, shell=True)
            #Convertimos de bytes a string
            ruta_de_port= ruta_name_port.decode("utf-8")
            #Buscamos el ID del puerto
            ruta_name_port1=ruta_de_port.index(id_puerto)
            ruta_name_port2=ruta_name_port1 + 4
            #Extraemos el nombre de manufactura
            name_port=ruta_de_port[ruta_name_port1:ruta_name_port2]
            ruta_name_port2=ruta_name_port1 + 5
            ruta_name_port3=ruta_name_port1 + 60
            name_board=ruta_de_port[ruta_name_port2:ruta_name_port3]
            #Buscamos el salto de linea que esta luego de la linea deseada
            name_board1=name_board.index("Bus")
            #Guardamos en board la posicion cero hasta antes de la palabra Bus
            board= name_board[0:name_board1] + "                                    "
            print(board)
            self.msg.setText("Conexion Exitosa en el puerto:" +" " + puerto) 
            
            

            
            
            #lboard.setText(board)
            #lboard.move(0, 0)   
            #name_board = Label(ventana, text =board).place(x=50, y=94)


        #mensaje_puerto = Label(ventana, text =puerto).place(x=100, y=64)




      







    def show_and_raise(self):
        self.show()
        self.raise_()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)





    demo = Demo()
    # Tamaño de la ventana
    #demo.resize(ancho,alto)
    demo.resize(600,450)
    #NOmbre de la ventana
    demo.setWindowTitle("PikBurn")
    demo.show_and_raise()


    sys.exit(app.exec_())
