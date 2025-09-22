from Imports import *

import Deviation1CManager
import ProcessDetectorManager

def run():
    Deviation1CManager.run()

def runProcessDetectionManager():
    ProcessDetectorManager.startProgram()
def runDeviationCanDetect():
    ProcessDetectorManager.RunDeviationDetection(True)
def runDeviationCantDetect():
    ProcessDetectorManager.RunDeviationDetection(False)

def runButtonController():
    ProcessDetectorManager.buttonController()

def runBuzzerController():
    ProcessDetectorManager.buzzerController()

def stopProcess1():
    ProcessDetectorManager.stopProcess1Button()
def stopProcess2():
    ProcessDetectorManager.stopProcess2Button()
def stopProcess3():
    ProcessDetectorManager.stopProcess3Button()
def stopProcess4():
    ProcessDetectorManager.stopProcess4Button()
def stopProcess5():
    ProcessDetectorManager.stopProcess5Button()
def stopProcess6():
    ProcessDetectorManager.stopProcess6Button()
def stopDeviation():
    ProcessDetectorManager.stopDeviationButton()

def refreshJobOrder():
    ProcessDetectorManager.refreshJobOrder()