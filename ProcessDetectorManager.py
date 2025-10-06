#%%
from Imports import *
import JobOrderManagerVer2 as JOManager
import WrongMaterialDetector
import Deviation1CManager
import VariableManager as varMan
import DateAndTimeManager
import CsvWriter
import Sql

process_1_csv = None
process_2_csv = None
process_3_csv = None
process_4_csv = None
process_5_csv = None
process_6_csv = None
compiledPiMachine = None

isProcess1MaterialWrong = False
isProcess2MaterialWrong = False
isProcess3MaterialWrong = False
isProcess4MaterialWrong = False
isProcess5MaterialWrong = False
isProcess6MaterialWrong = False

isDeviation = False

def read_proc_1_csv():
    global process_1_csv

    # pd.set_option("display.max_columns", None)
    # pd.set_option("display.max_rows", None)

    # process_1_csv = pd.read_csv(
    #     rf"\\192.168.2.10\csv\csv\VT1\log000_1.csv", encoding="latin1"
    # )

    Sql.SqlConnection()

    process_1_csv = Sql.SelectAllDataFromTable("process1_data")

    Sql.CloseConnection()

def read_proc_2_csv():
    global process_2_csv

    # pd.set_option("display.max_columns", None)
    # pd.set_option("display.max_rows", None)

    # process_2_csv = pd.read_csv(
    #     rf"\\192.168.2.10\csv\csv\VT2\log000_2.csv", encoding="latin1"
    # )

    Sql.SqlConnection()

    process_2_csv = Sql.SelectAllDataFromTable("process2_data")

    Sql.CloseConnection()

def read_proc_3_csv():
    global process_3_csv

    # pd.set_option("display.max_columns", None)
    # pd.set_option("display.max_rows", None)

    # process_3_csv = pd.read_csv(
    #     rf"\\192.168.2.10\csv\csv\VT3\log000_3.csv", encoding="latin1"
    # )

    Sql.SqlConnection()

    process_3_csv = Sql.SelectAllDataFromTable("process3_data")

    Sql.CloseConnection()

def read_proc_4_csv():
    global process_4_csv

    # pd.set_option("display.max_columns", None)
    # pd.set_option("display.max_rows", None)

    # process_4_csv = pd.read_csv(
    #     rf"\\192.168.2.10\csv\csv\VT4\log000_4.csv", encoding="latin1"
    # )

    Sql.SqlConnection()

    process_4_csv = Sql.SelectAllDataFromTable("process4_data")

    Sql.CloseConnection()

def read_proc_5_csv():
    global process_5_csv

    # pd.set_option("display.max_columns", None)
    # pd.set_option("display.max_rows", None)

    # process_5_csv = pd.read_csv(
    #     rf"\\192.168.2.10\csv\csv\VT5\log000_5.csv", encoding="latin1"
    # )

    Sql.SqlConnection()

    process_5_csv = Sql.SelectAllDataFromTable("process5_data")

    Sql.CloseConnection()

def read_proc_6_csv():
    global process_6_csv

    # pd.set_option("display.max_columns", None)
    # pd.set_option("display.max_rows", None)

    # process_6_csv = pd.read_csv(
    #     rf"\\192.168.2.10\csv\csv\VT6\log000_6.csv", encoding="latin1"
    # )

    Sql.SqlConnection()

    process_6_csv = Sql.SelectAllDataFromTable("process6_data")

    Sql.CloseConnection()

def readCompiledPiMachine():
    global df
    global rowCountOrig

    df = None

    Sql.SqlConnection()

    df = Sql.SelectAllDataFromTable("inspection_machine_data")

    

    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)

    # # --- Load data ---
    # file_path = r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv" #pi machine
    # # file_path = r"C:\Users\prod.fcline1\OneDrive - HIBLOW PHILIPPINES INC\CompiledPIMachine.csv" # ONE DRIVE PATH
    # # file_path = r"C:\Users\ai.pc\OneDrive\Desktop\CompiledPIMachine.csv"   # DESKTOP FALSE TESTING

    # df = pd.read_csv(file_path, encoding='latin1')
    df = df[(~df["MODEL_CODE"].isin(['60CAT0203M']))]
    df = df[(~df["MODEL_CODE"].isin(["60CAT0202P"]))]
    df = df[(~df["MODEL_CODE"].isin(["60CAT0203P"]))]
    df = df[(~df["MODEL_CODE"].isin(["60FC00000P"]))]
    df = df[(~df["MODEL_CODE"].isin(["60FC00902P"]))]
    df = df[(~df["MODEL_CODE"].isin(["60FC00903P"]))]
    df = df[(~df["MODEL_CODE"].isin(["60FC00905P"]))]
    df = df[(~df["MODEL_CODE"].isin(["60FCXP001P"]))]
    df = df[(~df["MODEL_CODE"].isin(["30FCXP001P"]))]
    df = df[(~df["PASS_NG"].isin([0]))]

    df['S_N'] = df['S_N'].astype(str)
    df['MODEL_CODE'] = df['MODEL_CODE'].astype(str)
    df = df[df['S_N'].str.len() >= 8]
    df = df[~df['MODEL_CODE'].str.contains('M')]  

    rowCountOrig = df.shape[0]

    Sql.CloseConnection()

def gettingPreviousData(modelCode):
    global df

    global voltageMiddlePrevAverage
    global wattageMiddlePrevAverage
    global amperageMiddlePrevAverage
    global closedPressureMiddlePrevAverage

    global voltageDev
    global wattageDev
    global amperageDev
    global closedPressureDev

    global previousData
    global dateTodayData

    df = df[(df["MODEL_CODE"].isin([modelCode]))] 
    
    DateAndTimeManager.GetDateToday()

    dateTodayData = df[(df["DATE"].astype(str).isin([DateAndTimeManager.dateTodayDashFormat]))]
    previousData = df[(~df["DATE"].astype(str).isin([DateAndTimeManager.dateTodayDashFormat]))]

    voltageMiddlePrevAverage = previousData["VOLTAGE_Middle_V"].tail(200).values.mean()
    wattageMiddlePrevAverage = previousData["WATTAGE_Middle_W"].tail(200).values.mean()
    amperageMiddlePrevAverage = previousData["AMPERAGE_Middle_A"].tail(200).values.mean()
    closedPressureMiddlePrevAverage = previousData["CLOSED_PRESSURE_Middle_kPa"].tail(200).values.mean()

    voltageDev = statistics.pstdev(previousData["VOLTAGE_Middle_V"].tail(200).values)
    wattageDev = statistics.pstdev(previousData["WATTAGE_Middle_W"].tail(200).values)
    amperageDev = statistics.pstdev(previousData["AMPERAGE_Middle_A"].tail(200).values)
    closedPressureDev = statistics.pstdev(previousData["CLOSED_PRESSURE_Middle_kPa"].tail(200).values)

# readCompiledPiMachine()
# gettingPreviousData("60CAT0213P")
#%%
    
def calculatingDeviation(modelCode):
    global currentDataSerialNumber
    global currentDataDate
    global currentDataTime
    global currentDataModel

    global voltageMiddleCurrentValue
    global wattageMiddleCurrentValue
    global amperageMiddleCurrentValue
    global closedPressureMiddleCurrentValue

    global voltageDevUcl, voltageDevLcl
    global wattageDevUcl, wattageDevLcl
    global amperageDevUcl, amperageDevLcl
    global closedPressureDevUcl, closedPressureDevLcl

    currentData = df.tail(1)
    currentDataSerialNumber = currentData["S_N"].values[0]
    currentDataDate = currentData["DATE"].values[0]
    currentDataTime = currentData["TIME"].values[0]
    currentDataModel = currentData["MODEL_CODE"].values[0]

    voltageMiddleCurrentValue = currentData["VOLTAGE_Middle_V"].values[0]
    wattageMiddleCurrentValue = currentData["WATTAGE_Middle_W"].values[0]
    amperageMiddleCurrentValue = currentData["AMPERAGE_Middle_A"].values[0]
    closedPressureMiddleCurrentValue = currentData["CLOSED_PRESSURE_Middle_kPa"].values[0]

    voltageDevUcl = voltageMiddlePrevAverage * (1.00 + (varMan.voltageTolerance / 100))
    voltageDevLcl = voltageMiddlePrevAverage * (1.00 - (varMan.voltageTolerance / 100))

    wattageDevUcl = wattageMiddlePrevAverage * (1.00 + (varMan.voltageTolerance / 100))
    wattageDevLcl = wattageMiddlePrevAverage * (1.00 - (varMan.voltageTolerance / 100))

    amperageDevUcl = amperageMiddlePrevAverage * (1.00 + (varMan.voltageTolerance / 100))
    amperageDevLcl = amperageMiddlePrevAverage * (1.00 - (varMan.voltageTolerance / 100))

    closedPressureDevUcl = closedPressureMiddlePrevAverage * (1.00 + (varMan.voltageTolerance / 100))
    closedPressureDevLcl = closedPressureMiddlePrevAverage * (1.00 - (varMan.voltageTolerance / 100))

def CheckingForDeviation():
    global isDeviation

    voltageMidStats = ""
    wattageMidStats = ""
    amperageMidStats = ""
    closedPressureMidStats = ""

    if voltageMiddleCurrentValue > voltageDevUcl or voltageMiddleCurrentValue < voltageDevLcl:
        print(f"Voltage Deviation Detected {voltageDevUcl} > {voltageMiddleCurrentValue} < {voltageDevLcl}")
        print(f"Serial Number: {currentDataSerialNumber}")
        isDeviation = True
    else:
        print(f"No Voltage Deviation Detected {voltageDevUcl} > {voltageMiddleCurrentValue} < {voltageDevLcl}")
        print(f"Serial Number: {currentDataSerialNumber}")
        
    if wattageMiddleCurrentValue > wattageDevUcl or wattageMiddleCurrentValue < wattageDevLcl:
        print(f"Wattage Deviation Detected {wattageDevUcl} > {wattageMiddleCurrentValue} < {wattageDevLcl}")
        print(f"Serial Number: {currentDataSerialNumber}")
        isDeviation = True
    else:
        print(f"No Wattage Deviation Detected {wattageDevUcl} > {wattageMiddleCurrentValue} < {wattageDevLcl}")
        print(f"Serial Number: {currentDataSerialNumber}")

    if amperageMiddleCurrentValue > amperageDevUcl or amperageMiddleCurrentValue < amperageDevLcl:
        print(f"Amperage Deviation Detected {amperageDevUcl} > {amperageMiddleCurrentValue} < {amperageDevLcl}")
        print(f"Serial Number: {currentDataSerialNumber}")
        isDeviation = True
    else:
        print(f"No Amperage Deviation Detected {amperageDevUcl} > {amperageMiddleCurrentValue} < {amperageDevLcl}")
        print(f"Serial Number: {currentDataSerialNumber}")

    if closedPressureMiddleCurrentValue > closedPressureDevUcl or closedPressureMiddleCurrentValue < closedPressureDevLcl:
        print(f"Closed Pressure Deviation Detected {closedPressureDevUcl} > {closedPressureMiddleCurrentValue} < {closedPressureDevLcl}")
        print(f"Serial Number: {currentDataSerialNumber}")
        isDeviation = True
    else:
        print(f"No Closed Pressure Deviation Detected {closedPressureDevUcl} > {closedPressureMiddleCurrentValue} < {closedPressureDevLcl}")
        print(f"Serial Number: {currentDataSerialNumber}")

    df = {
        "DATE": [currentDataDate],
        "TIME": [currentDataTime],
        "MODEL_CODE": [currentDataModel],
        "S/N": [currentDataSerialNumber],
        "TOLERANCE": [varMan.voltageTolerance],
        "VOLTAGE_MIDDLE": f"{voltageDevUcl} > {voltageMiddleCurrentValue} < {voltageDevLcl}",
        "WATTAGE_MIDDLE": f"{wattageDevUcl} > {wattageMiddleCurrentValue} < {wattageDevLcl}",
        "AMPERAGE_MIDDLE": f"{amperageDevUcl} > {amperageMiddleCurrentValue} < {amperageDevLcl}",
        "CLOSED_PRESSURE": f"{closedPressureDevUcl} > {closedPressureMiddleCurrentValue} < {closedPressureDevLcl}"
    }
    df = pd.DataFrame(df)
    CsvWriter.WriteCsv(df)

def createVoltagePlotFigure(modelCode):
    varMan.voltageFig, ax = plt.subplots(figsize=(6,2.5))

    # Plot your data
    ax.plot(dateTodayData["VOLTAGE_Middle_V"].values, marker='o', linestyle='-', color='blue', label="Voltage Points")
    ax.axhline(voltageMiddlePrevAverage, color='green', linestyle='--', label="Mean")
    ax.axhline(voltageDevUcl, color='red', linestyle='--', label=f"UCL ({varMan.voltageTolerance}%)")
    ax.axhline(voltageDevLcl, color='red', linestyle='--', label=f"LCL (-{varMan.voltageTolerance}%)")

    if modelCode == "60CAT0213P":
        ax.axhline(11.7, color='blue', linestyle='-', label="USL")

    ax.set_title("VOLTAGE MIDDLE")
    ax.set_ylabel("Measured Value")
    ax.legend()




    # plt.plot(dateTodayData["VOLTAGE Middle (V)"].values, marker='o', linestyle='-', color='blue', label="Data Points")
    # plt.axhline(voltageMiddlePrevAverage, color='green', linestyle='--', label="Mean")
    # plt.axhline(voltageDevUcl, color='red', linestyle='--', label="UCL (3%)")
    # plt.axhline(voltageDevLcl, color='red', linestyle='--', label="LCL (-3%)")
    # if modelCode == "60CAT0213P":
    #     plt.axhline(11.7, color='blue', linestyle='-', label="USL")
    # plt.title("VOLTAGE MIDDLE")
    # plt.ylabel("Measured Value")
    # plt.legend()
    # plt.show()

def createWattagePlotFigure(modelCode):
    varMan.wattageFig, ax = plt.subplots(figsize=(6,2.5))

    # Plot your data
    ax.plot(dateTodayData["WATTAGE_Middle_W"].values, marker='o', linestyle='-', color='blue', label="Wattage Points")
    ax.axhline(wattageMiddlePrevAverage, color='green', linestyle='--', label="Mean")
    ax.axhline(wattageDevUcl, color='red', linestyle='--', label=f"UCL ({varMan.voltageTolerance}%)")
    ax.axhline(wattageDevLcl, color='red', linestyle='--', label=f"LCL (-{varMan.voltageTolerance}%)")

    if modelCode == "60CAT0213P":
        ax.axhline(27.1, color='blue', linestyle='-', label="USL")

    ax.set_title("WATTAGE MIDDLE")
    ax.set_ylabel("Measured Value")
    ax.legend()

def createAmperagePlotFigure(modelCode):
    varMan.amperageFig, ax = plt.subplots(figsize=(6,2.5))

    # Plot your data
    ax.plot(dateTodayData["AMPERAGE_Middle_A"].values, marker='o', linestyle='-', color='blue', label="Amperage Points")
    ax.axhline(amperageMiddlePrevAverage, color='green', linestyle='--', label="Mean")
    ax.axhline(amperageDevUcl, color='red', linestyle='--', label=f"UCL ({varMan.voltageTolerance}%)")
    ax.axhline(amperageDevLcl, color='red', linestyle='--', label=f"LCL (-{varMan.voltageTolerance}%)")

    if modelCode == "60CAT0213P":
        ax.axhline(3.7, color='blue', linestyle='-', label="USL")

    ax.set_title("AMPERAGE MIDDLE")
    ax.set_ylabel("Measured Value")
    ax.legend()

def createClosedPressurePlotFigure(modelCode):
    varMan.closedPressureFig, ax = plt.subplots(figsize=(6,2.5))

    # Plot your data
    ax.plot(dateTodayData["CLOSED_PRESSURE_Middle_kPa"].values, marker='o', linestyle='-', color='blue', label="Closed Pressure Points")
    ax.axhline(closedPressureMiddlePrevAverage, color='green', linestyle='--', label="Mean")
    ax.axhline(closedPressureDevUcl, color='red', linestyle='--', label=f"UCL ({varMan.voltageTolerance}%)")
    ax.axhline(closedPressureDevLcl, color='red', linestyle='--', label=f"LCL (-{varMan.voltageTolerance}%)")

    if modelCode == "60CAT0213P":
        ax.axhline(27.8, color='blue', linestyle='-', label="USL")
        ax.axhline(33.2, color='blue', linestyle='-', label="LSL")

    ax.set_title("CLOSED PRESSURE MIDDLE")
    ax.set_ylabel("Measured Value")
    ax.legend()

def RunDeviationDetection(canDetect):
    readCompiledPiMachine()
    gettingPreviousData(df["MODEL_CODE"].tail(1).values[0])
    calculatingDeviation(df["MODEL_CODE"].tail(1).values[0])
    if canDetect:
        CheckingForDeviation()
    createVoltagePlotFigure(df["MODEL_CODE"].tail(1).values[0])
    createWattagePlotFigure(df["MODEL_CODE"].tail(1).values[0])
    createAmperagePlotFigure(df["MODEL_CODE"].tail(1).values[0])
    createClosedPressurePlotFigure(df["MODEL_CODE"].tail(1).values[0])
    WrongMaterialDetector.createVoltageFigure()

# RunDeviationDetection()
    
#%%


def buttonController():
    global isProcess1MaterialWrong
    global isProcess2MaterialWrong
    global isProcess3MaterialWrong
    global isProcess4MaterialWrong
    global isProcess5MaterialWrong
    global isProcess6MaterialWrong
    
    global isDeviation

    while True:
        if isProcess1MaterialWrong:
            WrongMaterialDetector.proc_1_stop_btn.config(bg="red")
        if isProcess2MaterialWrong:
            WrongMaterialDetector.proc_2_stop_btn.config(bg="red")
        if isProcess3MaterialWrong:
            WrongMaterialDetector.proc_3_stop_btn.config(bg="red")
        if isProcess4MaterialWrong:
            WrongMaterialDetector.proc_4_stop_btn.config(bg="red")
        if isProcess5MaterialWrong:
            WrongMaterialDetector.proc_5_stop_btn.config(bg="red")
        if isProcess6MaterialWrong:
            WrongMaterialDetector.proc_6_stop_btn.config(bg="red")
        if isDeviation:
            varMan.deviation_stop_btn.config(bg="red")

        time.sleep(0.5)

def buzzerController():
    global isProcess1MaterialWrong
    global isProcess2MaterialWrong
    global isProcess3MaterialWrong
    global isProcess4MaterialWrong
    global isProcess5MaterialWrong
    global isProcess6MaterialWrong

    global isDeviation

    while True:
        if isProcess1MaterialWrong or isProcess2MaterialWrong or isProcess3MaterialWrong or isProcess4MaterialWrong or isProcess5MaterialWrong or isProcess6MaterialWrong or isDeviation:
            WrongMaterialDetector.ser.write(b'H')
        else:
            WrongMaterialDetector.ser.write(b'L')

        time.sleep(0.5)

def stopProcess1Button():
    global isProcess1MaterialWrong

    WrongMaterialDetector.proc_1_stop_btn.config(bg="orange")
    isProcess1MaterialWrong = False

def stopProcess2Button():
    global isProcess2MaterialWrong

    WrongMaterialDetector.proc_2_stop_btn.config(bg="orange")
    isProcess2MaterialWrong = False

def stopProcess3Button():
    global isProcess3MaterialWrong

    WrongMaterialDetector.proc_3_stop_btn.config(bg="orange")
    isProcess3MaterialWrong = False
def stopProcess4Button():
    global isProcess4MaterialWrong

    WrongMaterialDetector.proc_4_stop_btn.config(bg="orange")
    isProcess4MaterialWrong = False

def stopProcess5Button():
    global isProcess5MaterialWrong

    WrongMaterialDetector.proc_5_stop_btn.config(bg="orange")
    isProcess5MaterialWrong = False

def stopProcess6Button():
    global isProcess6MaterialWrong

    WrongMaterialDetector.proc_6_stop_btn.config(bg="orange")
    isProcess6MaterialWrong = False

def stopDeviationButton():
    global isDeviation

    varMan.deviation_stop_btn.config(bg="orange")
    isDeviation = False

def refreshJobOrder():
    JOManager.check_job_orders()
    JOManager.find_materials()

def startProgram():
    global process_1_csv
    global process_2_csv
    global process_3_csv
    global process_4_csv
    global process_5_csv
    global process_6_csv

    global temp_df_vt_1
    global temp_df_vt_2
    global temp_df_vt_3
    global temp_df_vt_4
    global temp_df_vt_5
    global temp_df_vt_6

    global isProcess1MaterialWrong
    global isProcess2MaterialWrong
    global isProcess3MaterialWrong
    global isProcess4MaterialWrong
    global isProcess5MaterialWrong
    global isProcess6MaterialWrong

    # global process1CountOrig
    # global process2CountOrig
    # global process3CountOrig
    # global process4CountOrig
    # global process5CountOrig
    # global process6CountOrig

    # global inspectionMachineCountOrig

    try:
        Sql.SqlConnection()

        process1CountOrig = len(Sql.SelectAllDataFromTable("process1_data"))
        process2CountOrig = len(Sql.SelectAllDataFromTable("process2_data"))
        process3CountOrig = len(Sql.SelectAllDataFromTable("process3_data"))
        process4CountOrig = len(Sql.SelectAllDataFromTable("process4_data"))
        process5CountOrig = len(Sql.SelectAllDataFromTable("process5_data"))
        process6CountOrig = len(Sql.SelectAllDataFromTable("process6_data"))

        inspectionMachineCountOrig = len(Sql.SelectAllDataFromTable("inspection_machine_data"))

        Sql.CloseConnection()

        print(f"Procces1 Count Orig {process1CountOrig}")
        print(f"Procces2 Count Orig {process2CountOrig}")
        print(f"Procces3 Count Orig {process3CountOrig}")
        print(f"Procces4 Count Orig {process4CountOrig}")
        print(f"Procces5 Count Orig {process5CountOrig}")
        print(f"Procces6 Count Orig {process6CountOrig}")

    except:
        WrongMaterialDetector.ShowErrorBox()

    refreshJobOrder()
    
    while True:
        while True:
            try: 
                Sql.SqlConnection()

                process1CountCurrent = len(Sql.SelectAllDataFromTable("process1_data"))
                process2CountCurrent = len(Sql.SelectAllDataFromTable("process2_data"))
                process3CountCurrent = len(Sql.SelectAllDataFromTable("process3_data"))
                process4CountCurrent = len(Sql.SelectAllDataFromTable("process4_data"))
                process5CountCurrent = len(Sql.SelectAllDataFromTable("process5_data"))
                process6CountCurrent = len(Sql.SelectAllDataFromTable("process6_data"))

                inspectionMachineCountCurrent = len(Sql.SelectAllDataFromTable("inspection_machine_data"))

                Sql.CloseConnection()

                print(f"Procces1 Count Current {process1CountCurrent}")
                print(f"Procces2 Count Current {process2CountCurrent}")
                print(f"Procces3 Count Current {process3CountCurrent}")
                print(f"Procces4 Count Current {process4CountCurrent}")
                print(f"Procces5 Count Current {process5CountCurrent}")
                print(f"Procces6 Count Current {process6CountCurrent}")

                break

            except:
                pass

        #Process 1
        if process1CountCurrent != process1CountOrig:
            print("Process 1 Changes Detected")
            
            refreshJobOrder()

            while True:
                try:
                    read_proc_1_csv()
                    break
                except:
                    pass


            temp_df_vt_1 = process_1_csv.tail(1)

            if (temp_df_vt_1["Process_1_Model_Code"].values == "60CAT0212P"
                or temp_df_vt_1["Process_1_Model_Code"].values == "60CAT0203P"
                or temp_df_vt_1["Process_1_Model_Code"].values == "60CAT0213P"
                or temp_df_vt_1["Process_1_Model_Code"].values == "60CAT0203P"
                or temp_df_vt_1["Process_1_Model_Code"].values == "60CAT0902P"
                or temp_df_vt_1["Process_1_Model_Code"].values == "60CAT0903P"
                or temp_df_vt_1["Process_1_Model_Code"].values == "60CAT0905P"
                or temp_df_vt_1["Process_1_Model_Code"].values == "60CAT0000P"
                ):
                
                CheckMaterial("1" ,"Em2p", temp_df_vt_1["Process_1_Em2p"].values)
                CheckMaterial("1" ,"Em3p", temp_df_vt_1["Process_1_Em3p"].values)
                CheckMaterial("1" ,"Harness", temp_df_vt_1["Process_1_Harness"].values)
                CheckMaterial("1" ,"Frame", temp_df_vt_1["Process_1_Frame"].values)
                CheckMaterial("1" ,"Bushing", temp_df_vt_1["Process_1_Bushing"].values)

            process1CountOrig = process1CountCurrent
        #________________________________________________________________________________
        
        #Process 2
        if process2CountCurrent != process2CountOrig:
            print("Process 2 Changes Detected")
            
            refreshJobOrder()

            while True:
                try:
                    read_proc_2_csv()
                    break
                except:
                    pass
        
            temp_df_vt_2 = process_2_csv.tail(1)

            if (temp_df_vt_2["Process_2_Model_Code"].values == "60CAT0212P"
                or temp_df_vt_2["Process_2_Model_Code"].values == "60CAT0202P"
                or temp_df_vt_2["Process_2_Model_Code"].values == "60CAT0213P"
                or temp_df_vt_2["Process_2_Model_Code"].values == "60CAT0203P"
                ):

                CheckMaterial("2" ,"M4x40_Screw", temp_df_vt_2["Process_2_M4x40_Screw"].values)
                CheckMaterial("2" ,"Rod_Blk", temp_df_vt_2["Process_2_Rod_Blk"].values)
                CheckMaterial("2" ,"Df_Blk", temp_df_vt_2["Process_2_Df_Blk"].values)
                CheckMaterial("2" ,"Df_Ring", temp_df_vt_2["Process_2_Df_Ring"].values)
                CheckMaterial("2" ,"Washer", temp_df_vt_2["Process_2_Washer"].values)
                CheckMaterial("2" ,"Lock_Nut", temp_df_vt_2["Process_2_Lock_Nut"].values)

            if (temp_df_vt_2["Process_2_Model_Code"].values == "60FC00902P"
                or temp_df_vt_2["Process_2_Model_Code"].values == "60FC00903P"
                or temp_df_vt_2["Process_2_Model_Code"].values == "60FC00905P"
                or temp_df_vt_2["Process_2_Model_Code"].values == "60FC00000P"
                ):

                CheckMaterial("2" ,"M4x40_Screw", temp_df_vt_2["Process_2_M4x40_Screw"].values)
                CheckMaterial("2" ,"Rod_Blk", temp_df_vt_2["Process_2_Rod_Blk"].values)
                CheckMaterial("2" ,"Df_Blk", temp_df_vt_2["Process_2_Df_Blk"].values)
                CheckMaterial("2" ,"Washer", temp_df_vt_2["Process_2_Washer"].values)
                CheckMaterial("2" ,"Lock_Nut", temp_df_vt_2["Process_2_Lock_Nut"].values)

            process2CountOrig = process2CountCurrent
        #_________________________________________________________________________

        #Process 3
        if process3CountCurrent != process3CountOrig:
            print("Process 3 Changes Detected")
            
            refreshJobOrder()

            while True:
                try:
                    read_proc_3_csv()
                    break
                except:
                    pass

            temp_df_vt_3 = process_3_csv.tail(1)

            if (temp_df_vt_3["Process_3_Model_Code"].values == "60CAT0213P"
                or temp_df_vt_3["Process_3_Model_Code"].values == "60CAT0203P"
                ):

                CheckMaterial("3" ,"Frame_Gasket", temp_df_vt_3["Process_3_Frame_Gasket"].values)
                CheckMaterial("3" ,"Casing_Block", temp_df_vt_3["Process_3_Casing_Block"].values)
                CheckMaterial("3" ,"Casing_Gasket", temp_df_vt_3["Process_3_Casing_Gasket"].values)
                CheckMaterial("3" ,"M4x16_Screw_1", temp_df_vt_3["Process_3_M4x16_Screw_1"].values)
                CheckMaterial("3" ,"M4x16_Screw_2", temp_df_vt_3["Process_3_M4x16_Screw_2"].values)
                CheckMaterial("3" ,"Ball_Cushion", temp_df_vt_3["Process_3_Ball_Cushion"].values)
                CheckMaterial("3" ,"Partition_Board", temp_df_vt_3["Process_3_Partition_Board"].values)
                CheckMaterial("3" ,"Built_In_Tube_1", temp_df_vt_3["Process_3_Built_In_Tube_1"].values)
                CheckMaterial("3" ,"Built_In_Tube_2", temp_df_vt_3["Process_3_Built_In_Tube_2"].values)
                CheckMaterial("3" ,"Frame_Cover", temp_df_vt_3["Process_3_Frame_Cover"].values)
            
            if (temp_df_vt_3["Process_3_Model_Code"].values == "60CAT0212P"
                or temp_df_vt_3["Process_3_Model_Code"].values == "60CAT0202P"
                ):

                CheckMaterial("3" ,"Frame_Gasket", temp_df_vt_3["Process_3_Frame_Gasket"].values)
                CheckMaterial("3" ,"Casing_Block", temp_df_vt_3["Process_3_Casing_Block"].values)
                CheckMaterial("3" ,"Casing_Gasket", temp_df_vt_3["Process_3_Casing_Gasket"].values)
                CheckMaterial("3" ,"M4x16_Screw_1", temp_df_vt_3["Process_3_M4x16_Screw_1"].values)
                CheckMaterial("3" ,"M4x16_Screw_2", temp_df_vt_3["Process_3_M4x16_Screw_2"].values)
                CheckMaterial("3" ,"Ball_Cushion", temp_df_vt_3["Process_3_Ball_Cushion"].values)
                CheckMaterial("3" ,"Frame_Cover", temp_df_vt_3["Process_3_Frame_Cover"].values)

            if (temp_df_vt_3["Process_3_Model_Code"].values == "60FC00902P"
                or temp_df_vt_3["Process_3_Model_Code"].values == "60FC00903P"
                or temp_df_vt_3["Process_3_Model_Code"].values == "60FC00905P"
                or temp_df_vt_3["Process_3_Model_Code"].values == "60FC00000P"
                ):

                CheckMaterial("3" ,"Frame_Cover", temp_df_vt_3["Process_3_Frame_Cover"].values)
                CheckMaterial("3" ,"Head_Cover", temp_df_vt_3["Process_3_Head_Cover"].values)
                CheckMaterial("3" ,"Casing_Packing", temp_df_vt_3["Process_3_Casing_Packing"].values)
                CheckMaterial("3" ,"M4x12_Screw", temp_df_vt_3["Process_3_M4x12_Screw"].values)
                CheckMaterial("3" ,"Csb_L", temp_df_vt_3["Process_3_Csb_L"].values)
                CheckMaterial("3" ,"Csb_R", temp_df_vt_3["Process_3_Csb_R"].values)
                CheckMaterial("3" ,"Head_Packing", temp_df_vt_3["Process_3_Head_Packing"].values)

            process3CountOrig = process3CountCurrent
        #________________________________________________________________________________________

        #Process 4
        if process4CountCurrent != process4CountOrig:
            print("Process 4 Changes Detected")
            
            refreshJobOrder()

            while True:
                try:
                    read_proc_4_csv()
                    break
                except:
                    pass
            
            temp_df_vt_4 = process_4_csv.tail(1)

            if (temp_df_vt_4["Process_4_Model_Code"].values == "60CAT0212P"
                or temp_df_vt_4["Process_4_Model_Code"].values == "60CAT0202P"
                ):

                CheckMaterial("4" ,"Tank", temp_df_vt_4["Process_4_Tank"].values)
                CheckMaterial("4" ,"Upper_Housing", temp_df_vt_4["Process_4_Upper_Housing"].values)
                CheckMaterial("4" ,"Cord_Hook", temp_df_vt_4["Process_4_Cord_Hook"].values)
                CheckMaterial("4" ,"M4x16_Screw", temp_df_vt_4["Process_4_M4x16_Screw"].values)
                CheckMaterial("4" ,"Tank_Gasket", temp_df_vt_4["Process_4_Tank_Gasket"].values)
                CheckMaterial("4" ,"Tank_Cover", temp_df_vt_4["Process_4_Tank_Cover"].values)
                CheckMaterial("4" ,"Housing_Gasket", temp_df_vt_4["Process_4_Housing_Gasket"].values)
                CheckMaterial("4" ,"M4x40_Screw", temp_df_vt_4["Process_4_M4x40_Screw"].values)

            if (temp_df_vt_4["Process_4_Model_Code"].values == "60CAT0213P"   
                or temp_df_vt_4["Process_4_Model_Code"].values == "60CAT0203P"
                ):

                CheckMaterial("4" ,"Tank", temp_df_vt_4["Process_4_Tank"].values)
                CheckMaterial("4" ,"Upper_Housing", temp_df_vt_4["Process_4_Upper_Housing"].values)
                CheckMaterial("4" ,"Cord_Hook", temp_df_vt_4["Process_4_Cord_Hook"].values)
                CheckMaterial("4" ,"M4x16_Screw", temp_df_vt_4["Process_4_M4x16_Screw"].values)
                CheckMaterial("4" ,"PartitionGasket", temp_df_vt_4["Process_4_PartitionGasket"].values)
                CheckMaterial("4" ,"M4x12_Screw", temp_df_vt_4["Process_4_M4x12_Screw"].values)
                CheckMaterial("4" ,"Housing_Gasket", temp_df_vt_4["Process_4_Housing_Gasket"].values)
                CheckMaterial("4" ,"M4x40_Screw", temp_df_vt_4["Process_4_M4x40_Screw"].values)

            if (temp_df_vt_4["Process_4_Model_Code"].values == "60FC00902P"
                or temp_df_vt_4["Process_4_Model_Code"].values == "60FC00903P"
                or temp_df_vt_4["Process_4_Model_Code"].values == "60FC00905P"
                or temp_df_vt_4["Process_4_Model_Code"].values == "60FC00000P"
                ):

                CheckMaterial("4" ,"M4x12_Screw", temp_df_vt_4["Process_4_M4x12_Screw"].values)
                CheckMaterial("4" ,"Muffler", temp_df_vt_4["Process_4_Muffler"].values)
                CheckMaterial("4" ,"Muffler_Gasket", temp_df_vt_4["Process_4_Muffler_Gasket"].values)
                CheckMaterial("4" ,"VCR", temp_df_vt_4["Process_4_VCR"].values)

            process4CountOrig = process4CountCurrent
        #____________________________________________________________________________________

        #Process 5
        if process5CountCurrent != process5CountOrig:
            print("Process 5 Changes Detected")
            
            refreshJobOrder()

            while True:
                try:
                    read_proc_5_csv()
                    break
                except:
                    pass
            
            temp_df_vt_5 = process_5_csv.tail(1)

            if (temp_df_vt_5["Process_5_Model_Code"].values == "60CAT0212P"
                or temp_df_vt_5["Process_5_Model_Code"].values == "60CAT0203P"
                or temp_df_vt_5["Process_5_Model_Code"].values == "60CAT0213P"
                or temp_df_vt_5["Process_5_Model_Code"].values == "60CAT0203P"
                or temp_df_vt_5["Process_5_Model_Code"].values == "60CAT0902P"
                or temp_df_vt_5["Process_5_Model_Code"].values == "60CAT0903P"
                or temp_df_vt_5["Process_5_Model_Code"].values == "60CAT0905P"
                or temp_df_vt_5["Process_5_Model_Code"].values == "60CAT0000P"
                ):

                CheckMaterial("5" ,"Rating_Label", temp_df_vt_5["Process_5_Rating_Label"].values)

            process5CountOrig = process5CountCurrent
        #_____________________________________________________________________________       

        #Process 6
        if process6CountCurrent != process6CountOrig:
            print("Process 6 Changes Detected")
            
            refreshJobOrder()

            while True:
                try:
                    read_proc_6_csv()
                    break
                except:
                    pass

            temp_df_vt_6 = process_6_csv.tail(1)

            if (temp_df_vt_6["Process_6_Model_Code"].values == "60CAT0212P"
                or temp_df_vt_6["Process_6_Model_Code"].values == "60CAT0203P"
                or temp_df_vt_6["Process_6_Model_Code"].values == "60CAT0213P"
                or temp_df_vt_6["Process_6_Model_Code"].values == "60CAT0203P"
                or temp_df_vt_6["Process_6_Model_Code"].values == "60CAT0902P"
                or temp_df_vt_6["Process_6_Model_Code"].values == "60CAT0903P"
                or temp_df_vt_6["Process_6_Model_Code"].values == "60CAT0905P"
                or temp_df_vt_6["Process_6_Model_Code"].values == "60CAT0000P"
                ):

                CheckMaterial("6" ,"Vinyl", temp_df_vt_6["Process_6_Vinyl"].values)

            process6CountOrig = process6CountCurrent

        #Deviation
        if inspectionMachineCountCurrent != inspectionMachineCountOrig:
            print("Inspection Machine Changes Detected")
            inspectionMachineCountOrig = inspectionMachineCountCurrent
            
            RunDeviationDetection(True)

            inspectionMachineCountOrig = inspectionMachineCountCurrent

        UpdateLoading()
        
        time.sleep(1)

def CheckMaterial(process, material, code):
    global temp_df_vt_1
    global temp_df_vt_2
    global temp_df_vt_3
    global temp_df_vt_4
    global temp_df_vt_5
    global temp_df_vt_6

    global isProcess1MaterialWrong
    global isProcess2MaterialWrong
    global isProcess3MaterialWrong
    global isProcess4MaterialWrong
    global isProcess5MaterialWrong
    global isProcess6MaterialWrong

    if process == "1":
        for a in JOManager.job_order_materials:
            same_value = 0
            if temp_df_vt_1[f"Process_1_{material}"].values[0] == a:
                same_value += 1
                WrongMaterialDetector.InsertInMaterialLogWindow(1, f"Process 1 Correct {material} : {code}")
                print(f"Process 1 Correct {material}")
                break
        if same_value == 0:
            WrongMaterialDetector.InsertInMaterialLogWindow(0, f"Process 1 Incorrect {material} : {code}")
            isProcess1MaterialWrong = True
            print(f"Process 1 Incorrect {material}")

    if process == "2":
        for a in JOManager.job_order_materials:
            same_value = 0
            if temp_df_vt_2[f"Process_2_{material}"].values[0] == a:
                same_value += 1
                WrongMaterialDetector.InsertInMaterialLogWindow(1, f"Process 2 Correct {material} : {code}")
                print(f"Process 2 Correct {material}")
                break
        if same_value == 0:
            WrongMaterialDetector.InsertInMaterialLogWindow(0, f"Process 2 Incorrect {material} : {code}")
            isProcess2MaterialWrong = True
            print(f"Process 2 Incorrect {material}")
    if process == "3":
        for a in JOManager.job_order_materials:
            same_value = 0
            if temp_df_vt_3[f"Process_3_{material}"].values[0] == a:
                same_value += 1
                WrongMaterialDetector.InsertInMaterialLogWindow(1, f"Process 3 Correct {material} : {code}")
                print(f"Process 3 Correct {material}")
                break
        if same_value == 0:
            WrongMaterialDetector.InsertInMaterialLogWindow(0, f"Process 3 Incorrect {material} : {code}")
            isProcess3MaterialWrong = True
            print(f"Process 3 Incorrect {material}")
    if process == "4":
        for a in JOManager.job_order_materials:
            same_value = 0
            if temp_df_vt_4[f"Process_4_{material}"].values[0] == a:
                same_value += 1
                WrongMaterialDetector.InsertInMaterialLogWindow(1, f"Process 4 Correct {material} : {code}")
                print(f"Process 4 Correct {material}")
                break
        if same_value == 0:
            WrongMaterialDetector.InsertInMaterialLogWindow(0, f"Process 4 Incorrect {material} : {code}")
            isProcess4MaterialWrong = True
            print(f"Process 4 Incorrect {material}")
    if process == "5":
        for a in JOManager.job_order_materials:
            same_value = 0
            if temp_df_vt_5[f"Process_5_{material}"].values[0] == a:
                same_value += 1
                WrongMaterialDetector.InsertInMaterialLogWindow(1, f"Process 5 Correct {material} : {code}")
                print(f"Process 5 Correct {material}")
                break
        if same_value == 0:
            WrongMaterialDetector.InsertInMaterialLogWindow(0, f"Process 5 Incorrect {material} : {code}")
            isProcess5MaterialWrong = True
            print(f"Process 5 Incorrect {material}")
    if process == "6":
        for a in JOManager.job_order_materials:
            same_value = 0
            if temp_df_vt_6[f"Process_6_{material}"].values[0] == a:
                same_value += 1
                WrongMaterialDetector.InsertInMaterialLogWindow(1, f"Process 6 Correct {material} : {code}")
                print(f"Process 6 Correct {material}")
                break
        if same_value == 0:
            WrongMaterialDetector.InsertInMaterialLogWindow(0, f"Process 6 Incorrect {material} : {code}")
            isProcess6MaterialWrong = True
            print(f"Process 6 Incorrect {material}")

def UpdateLoading():
    if WrongMaterialDetector.proc_1_err_msg_txt == "Loading...":
        WrongMaterialDetector.proc_1_err_msg_txt = "Loading"
        WrongMaterialDetector.proc_1_err_msg.config(text=WrongMaterialDetector.proc_1_err_msg_txt)
    else:
        WrongMaterialDetector.proc_1_err_msg_txt += "."
        WrongMaterialDetector.proc_1_err_msg.config(text=WrongMaterialDetector.proc_1_err_msg_txt)

    if WrongMaterialDetector.proc_2_err_msg_txt == "Loading...":
        WrongMaterialDetector.proc_2_err_msg_txt = "Loading"
        WrongMaterialDetector.proc_2_err_msg.config(text=WrongMaterialDetector.proc_2_err_msg_txt)
    else:
        WrongMaterialDetector.proc_2_err_msg_txt += "."
        WrongMaterialDetector.proc_2_err_msg.config(text=WrongMaterialDetector.proc_2_err_msg_txt)

    if WrongMaterialDetector.proc_3_err_msg_txt == "Loading...":
        WrongMaterialDetector.proc_3_err_msg_txt = "Loading"
        WrongMaterialDetector.proc_3_err_msg.config(text=WrongMaterialDetector.proc_3_err_msg_txt)
    else:
        WrongMaterialDetector.proc_3_err_msg_txt += "."
        WrongMaterialDetector.proc_3_err_msg.config(text=WrongMaterialDetector.proc_3_err_msg_txt)

    if WrongMaterialDetector.proc_4_err_msg_txt == "Loading...":
        WrongMaterialDetector.proc_4_err_msg_txt = "Loading"
        WrongMaterialDetector.proc_4_err_msg.config(text=WrongMaterialDetector.proc_4_err_msg_txt)
    else:
        WrongMaterialDetector.proc_4_err_msg_txt += "."
        WrongMaterialDetector.proc_4_err_msg.config(text=WrongMaterialDetector.proc_4_err_msg_txt)

    if WrongMaterialDetector.proc_5_err_msg_txt == "Loading...":
        WrongMaterialDetector.proc_5_err_msg_txt = "Loading"
        WrongMaterialDetector.proc_5_err_msg.config(text=WrongMaterialDetector.proc_5_err_msg_txt)
    else:
        WrongMaterialDetector.proc_5_err_msg_txt += "."
        WrongMaterialDetector.proc_5_err_msg.config(text=WrongMaterialDetector.proc_5_err_msg_txt)

    if WrongMaterialDetector.proc_6_err_msg_txt == "Loading...":
        WrongMaterialDetector.proc_6_err_msg_txt = "Loading"
        WrongMaterialDetector.proc_6_err_msg.config(text=WrongMaterialDetector.proc_6_err_msg_txt)
    else:
        WrongMaterialDetector.proc_6_err_msg_txt += "."
        WrongMaterialDetector.proc_6_err_msg.config(text=WrongMaterialDetector.proc_6_err_msg_txt)

    Deviation1CManager.UpdateLoading()


# RunDeviationDetection()

#%%