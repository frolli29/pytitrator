"fenêtre de calibration du pH mètre"

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from graphic.windows.phmeter_calib_win import Ui_calibration_window

from subsystems.pHmeter import *
from datetime import datetime

class PhMeterCalibWindow(QDialog, Ui_calibration_window):
    def __init__(self, ihm, parent=None):
        super(PhMeterCalibWindow,self).__init__(parent)
        #self.cal_window=QDialog()
        #self.setupUi(self.cal_window)
        self.setupUi(self)
        self.ihm=ihm

        #connexions
        
        # self.buttonBox.accepted.connect(self.validateCal) #lorsqu'on clique sur valider, la calibration est enregsitrée
        # self.buttonBox.accepted.connect(self.ihm.phmeter.onCalibrationChange)        
        # self.buttonBox.accepted.connect(self.ihm.controlPanel.refreshCalibrationText)        
        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject) 
        self.buttonBox.clicked.connect(self.on_button_clicked)

        if self.ihm.phmeter.state=='open':
            self.ihm.timer_display.timeout.connect(self.setOnDirectVoltage) #voltage current update

        #connexions 
        self.button_ph4.clicked.connect(lambda : self.saveAndShowVoltage(self.U_ph4))
        self.button_ph7.clicked.connect(lambda : self.saveAndShowVoltage(self.U_ph7))
        self.button_ph10.clicked.connect(lambda : self.saveAndShowVoltage(self.U_ph10))

        self.U4=0
        self.U7=0
        self.U10=0
        self.used_pH_buffers=set()
    
    def on_button_clicked(self, button):
        if self.buttonBox.standardButton(button) == QDialogButtonBox.Apply:
            self.validateCal()
            self.ihm.phmeter.onCalibrationChange()
            self.ihm.controlPanel.refreshCalibrationText()
            self.accept()
            self.reject()
            
            # self.buttonBox.accepted.connect(self.validateCal) #lorsqu'on clique sur valider, la calibration est enregsitrée
            # self.buttonBox.accepted.connect(self.ihm.phmeter.onCalibrationChange)        
            # self.buttonBox.accepted.connect(self.ihm.controlPanel.refreshCalibrationText)        
            # self.buttonBox.accepted.connect(self.accept)
            # self.buttonBox.rejected.connect(self.reject)


    """def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(440, 290)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 220, 231, 51))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        #print("passage!")

        self.direct_voltage_mV = QtWidgets.QLCDNumber(Dialog)
        self.direct_voltage_mV.setGeometry(QtCore.QRect(210, 80, 211, 131))
        self.direct_voltage_mV.setObjectName("direct_voltage_mV")
        self.direct_voltage_mV.setNumDigits(6)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(260, 40, 131, 41))
        self.label.setObjectName("label")
        self.lcdNumber_pH4 = QtWidgets.QLCDNumber(Dialog)
        self.lcdNumber_pH4.setGeometry(QtCore.QRect(30, 50, 71, 51))
        self.lcdNumber_pH4.setObjectName("lcdNumber_pH4")
        self.lcdNumber_pH4.setNumDigits(6)
        self.lcdNumber_pH7 = QtWidgets.QLCDNumber(Dialog)
        self.lcdNumber_pH7.setGeometry(QtCore.QRect(30, 130, 71, 51))
        self.lcdNumber_pH7.setObjectName("lcdNumber_pH7")
        self.lcdNumber_pH7.setNumDigits(6)
        self.lcdNumber_pH10 = QtWidgets.QLCDNumber(Dialog)
        self.lcdNumber_pH10.setGeometry(QtCore.QRect(30, 210, 71, 51))
        self.lcdNumber_pH10.setObjectName("lcdNumber_pH10")
        self.lcdNumber_pH10.setNumDigits(6)
        self.pushButton_pH4 = QtWidgets.QPushButton(Dialog, clicked = lambda: self.saveAndShowVoltage(self.lcdNumber_pH4))
        self.pushButton_pH4.setGeometry(QtCore.QRect(130, 50, 51, 51))
        self.pushButton_pH4.setObjectName("pushButton_pH4")
        self.pushButton_pH7 = QtWidgets.QPushButton(Dialog, clicked = lambda: self.saveAndShowVoltage(self.lcdNumber_pH7))
        self.pushButton_pH7.setGeometry(QtCore.QRect(130, 130, 51, 51))
        self.pushButton_pH7.setObjectName("pushButton_pH7")
        self.pushButton_pH10 = QtWidgets.QPushButton(Dialog, clicked = lambda: self.saveAndShowVoltage(self.lcdNumber_pH10))
        self.pushButton_pH10.setGeometry(QtCore.QRect(130, 210, 51, 51))
        self.pushButton_pH10.setObjectName("pushButton_pH10")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 10, 151, 31))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)"""
        
        #self.buttonBox.clicked.connect(self.motherWindow.setOnDirectPH) 
        #pour retrouver le pH en direct quand on revient sur le control pannel 
        
        
        
        #rajouter une fonction à la fermeture de la fenetre pour desactiver les actions sur le timer

        #affichage de la tension déjà affichée sur le panneau de contrôle
        #if self.phmeter.getIsOpen():
            #U=self.phmeter.U_pH.getVoltage()  #valeur actuelle de tension
            #self.direct_voltage_mV.display(U)
    
    # def retranslateUi(self, Dialog):
    #     _translate = QtCore.QCoreApplication.translate
    #     Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
    #     self.label.setText(_translate("Dialog", "tension (mV) en direct"))
    #     self.pushButton_pH10.setText(_translate("Dialog", "pH10"))
    #     self.pushButton_pH7.setText(_translate("Dialog", "pH7"))
    #     self.pushButton_pH4.setText(_translate("Dialog", "pH4"))
    #     self.label_2.setText(_translate("Dialog", "Tensions enregistrées"))

    def setOnDirectVoltage(self): #, ch, voltage):
        self.lcdNumber.display(1000*self.ihm.phmeter.currentVoltage)

    def saveAndShowVoltage(self, screen): #sreen est un objet QLCDNumber
        U=self.ihm.phmeter.currentVoltage
        print("save voltage")
        if screen==self.U_ph4:
            self.U4=U
            self.used_pH_buffers.add(4)
        if screen==self.U_ph7:
            self.U7=U
            self.used_pH_buffers.add(7)
        if screen==self.U_ph10:
            self.U10=U
            self.used_pH_buffers.add(10)
        print("voltage=",U)
        screen.display(U)

    def validateCal(self): #pH_buffers est un tuple contenant les valeurs de pH des tampons
        print("validate cal")
        pH_buffers=sorted(list(self.used_pH_buffers))
        self.used_pH_buffers = pH_buffers
        #print("pH buffers : ",type(pH_buffers),pH_buffers)
        dt = datetime.now()
        if pH_buffers == [4]:
            u_cal = [self.U4]
        elif pH_buffers == [7]:
            u_cal = [self.U7]
        elif pH_buffers == [4,7]:
            u_cal = [self.U4, self.U7]
            print("calib 2 pts")
        elif pH_buffers == [4,7,10]:
            u_cal = [self.U4, self.U7, self.U10]
            print("calib 3 pts")
        else:
            print("This type of calibration is not suppported")
        (a,b)=PHMeter.computeCalCoefs(self.ihm.phmeter,u_cal,pH_buffers) #calcul des coefficients de calib
        PHMeter.saveCalData(self.ihm.phmeter, dt.strftime("%m/%d/%Y %H:%M:%S"), pH_buffers, u_cal, (a,b)) #enregistrer dans le fichier


if __name__ == "__main__":
    
    #spectro
    od = OceanDirectAPI()
    device_count = od.find_usb_devices() # 1 si appareils détectés
    device_ids = od.get_device_ids()
    #device_count = len(device_ids)
    id=device_ids[0]
    spectro = od.open_device(id) #crée une instance de la classe Spectrometer
    adv = Spectrometer.Advanced(spectro)
    spectro_unit=AbsorbanceMeasure(od,spectro)

    #pHmètre
    U_pH = VoltageInput()
    ph_meter = PHMeter(U_pH)

    #Interface
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    cp = ControlPannel(ph_meter,spectro_unit)
    ui = PhMeterCalibWindow(ph_meter, cp)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
