#%%
from Imports import *
import JobOrderManagerVer2 as JOManager
import WrongMaterialDetector
import Deviation1CManager
import VariableManager as varMan
import DateAndTimeManager

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

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    process_1_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT1\log000_1.csv", encoding="latin1"
    )
def read_proc_2_csv():
    global process_2_csv

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    process_2_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT2\log000_2.csv", encoding="latin1"
    )

def read_proc_3_csv():
    global process_3_csv

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    process_3_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT3\log000_3.csv", encoding="latin1"
    )

def read_proc_4_csv():
    global process_4_csv

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    process_4_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT4\log000_4.csv", encoding="latin1"
    )

def read_proc_5_csv():
    global process_5_csv

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    process_5_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT5\log000_5.csv", encoding="latin1"
    )

def read_proc_6_csv():
    global process_6_csv

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    process_6_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT6\log000_6.csv", encoding="latin1"
    )

def readCompiledPiMachine():
    global df
    global rowCountOrig

    df = None

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # --- Load data ---
    file_path = r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv" #pi machine
    # file_path = r"C:\Users\prod.fcline1\OneDrive - HIBLOW PHILIPPINES INC\CompiledPIMachine.csv" # ONE DRIVE PATH
    # file_path = r"C:\Users\ai.pc\OneDrive\Desktop\CompiledPIMachine.csv"   # DESKTOP FALSE TESTING

    df = pd.read_csv(file_path, encoding='latin1')
    df = df[(~df["MODEL CODE"].isin(['60CAT0203M']))]
    df = df[(~df["MODEL CODE"].isin(["60CAT0202P"]))]
    df = df[(~df["MODEL CODE"].isin(["60CAT0203P"]))]
    df = df[(~df["MODEL CODE"].isin(["60FC00000P"]))]
    df = df[(~df["MODEL CODE"].isin(["60FC00902P"]))]
    df = df[(~df["MODEL CODE"].isin(["60FC00903P"]))]
    df = df[(~df["MODEL CODE"].isin(["60FC00905P"]))]
    df = df[(~df["MODEL CODE"].isin(["60FCXP001P"]))]
    df = df[(~df["MODEL CODE"].isin(["30FCXP001P"]))]
    df = df[(~df["PASS/NG"].isin([0]))]

    df['S/N'] = df['S/N'].astype(str)
    df['MODEL CODE'] = df['MODEL CODE'].astype(str)
    df = df[df['S/N'].str.len() >= 8]
    df = df[~df['MODEL CODE'].str.contains('M')]  

    rowCountOrig = df.shape[0]

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

    df = df[(df["MODEL CODE"].isin([modelCode]))] 
    
    DateAndTimeManager.GetDateToday()

    dateTodayData = df[(df["DATE"].isin([DateAndTimeManager.dateToday]))]
    previousData = df[(~df["DATE"].isin([DateAndTimeManager.dateToday]))]

    voltageMiddlePrevAverage = previousData["VOLTAGE Middle (V)"].tail(200).values.mean()
    wattageMiddlePrevAverage = previousData["WATTAGE Middle (W)"].tail(200).values.mean()
    amperageMiddlePrevAverage = previousData["AMPERAGE Middle (A)"].tail(200).values.mean()
    closedPressureMiddlePrevAverage = previousData["CLOSED PRESSURE Middle (kPa)"].tail(200).values.mean()

    voltageDev = statistics.pstdev(previousData["VOLTAGE Middle (V)"].tail(200).values)
    wattageDev = statistics.pstdev(previousData["WATTAGE Middle (W)"].tail(200).values)
    amperageDev = statistics.pstdev(previousData["AMPERAGE Middle (A)"].tail(200).values)
    closedPressureDev = statistics.pstdev(previousData["CLOSED PRESSURE Middle (kPa)"].tail(200).values)
    
def calculatingDeviation(modelCode):
    global currentDataSerialNumber

    global voltageMiddleCurrentValue
    global wattageMiddleCurrentValue
    global amperageMiddleCurrentValue
    global closedPressureMiddleCurrentValue

    global voltageDevUcl, voltageDevLcl
    global wattageDevUcl, wattageDevLcl
    global amperageDevUcl, amperageDevLcl
    global closedPressureDevUcl, closedPressureDevLcl

    currentData = df.tail(1)
    currentDataSerialNumber = currentData["S/N"].values[0]

    voltageMiddleCurrentValue = currentData["VOLTAGE Middle (V)"].values[0]
    wattageMiddleCurrentValue = currentData["WATTAGE Middle (W)"].values[0]
    amperageMiddleCurrentValue = currentData["AMPERAGE Middle (A)"].values[0]
    closedPressureMiddleCurrentValue = currentData["CLOSED PRESSURE Middle (kPa)"].values[0]

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

def createVoltagePlotFigure(modelCode):
    varMan.voltageFig, ax = plt.subplots(figsize=(6,2.5))

    # Plot your data
    ax.plot(dateTodayData["VOLTAGE Middle (V)"].values, marker='o', linestyle='-', color='blue', label="Voltage Points")
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
    ax.plot(dateTodayData["WATTAGE Middle (W)"].values, marker='o', linestyle='-', color='blue', label="Wattage Points")
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
    ax.plot(dateTodayData["AMPERAGE Middle (A)"].values, marker='o', linestyle='-', color='blue', label="Amperage Points")
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
    ax.plot(dateTodayData["CLOSED PRESSURE Middle (kPa)"].values, marker='o', linestyle='-', color='blue', label="Closed Pressure Points")
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
    gettingPreviousData(df["MODEL CODE"].tail(1).values[0])
    calculatingDeviation(df["MODEL CODE"].tail(1).values[0])
    if canDetect:
        CheckingForDeviation()
    createVoltagePlotFigure(df["MODEL CODE"].tail(1).values[0])
    createWattagePlotFigure(df["MODEL CODE"].tail(1).values[0])
    createAmperagePlotFigure(df["MODEL CODE"].tail(1).values[0])
    createClosedPressurePlotFigure(df["MODEL CODE"].tail(1).values[0])
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

    try:
        process1_org_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT1\log000_1.csv")
        process2_org_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT2\log000_2.csv")
        process3_org_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT3\log000_3.csv")
        process4_org_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT4\log000_4.csv")
        process5_org_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT5\log000_5.csv")
        process6_org_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT6\log000_6.csv")

        compiledPiFileOrig = os.path.getmtime(r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv")
    except:
        WrongMaterialDetector.ShowErrorBox()

    refreshJobOrder()
    
    while True:
        while True:
            try: 
                process1_curr_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT1\log000_1.csv")
                process2_curr_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT2\log000_2.csv")
                process3_curr_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT3\log000_3.csv")
                process4_curr_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT4\log000_4.csv")
                process5_curr_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT5\log000_5.csv")
                process6_curr_file = os.path.getmtime(r"\\192.168.2.10\csv\csv\VT6\log000_6.csv")

                compiledPiFileCurrent = os.path.getmtime(r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv")

                break

            except:
                pass

        #Process 1
        if process1_curr_file != process1_org_file:
            print("Process 1 Changes Detected")
            refreshJobOrder()

            while True:
                try:
                    read_proc_1_csv()
                    break
                except:
                    pass


            temp_df_vt_1 = process_1_csv.tail(1)

            if (temp_df_vt_1["Process 1 Model Code"].values == "60CAT0212P"
                or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0203P"
                or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0213P"
                or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0203P"
                or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0902P"
                or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0903P"
                or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0905P"
                or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0000P"
                ):
                
                CheckMaterial("1" ,"Em2p", temp_df_vt_1["Process 1 Em2p"].values)
                CheckMaterial("1" ,"Em3p", temp_df_vt_1["Process 1 Em3p"].values)
                CheckMaterial("1" ,"Harness", temp_df_vt_1["Process 1 Harness"].values)
                CheckMaterial("1" ,"Frame", temp_df_vt_1["Process 1 Frame"].values)
                CheckMaterial("1" ,"Bushing", temp_df_vt_1["Process 1 Bushing"].values)

            process1_org_file = process1_curr_file
        #________________________________________________________________________________
        
        #Process 2
        if process2_curr_file != process2_org_file:
            print("Process 2 Changes Detected")
            refreshJobOrder()

            while True:
                try:
                    read_proc_2_csv()
                    break
                except:
                    pass
        
            temp_df_vt_2 = process_2_csv.tail(1)

            if (temp_df_vt_2["Process 2 Model Code"].values == "60CAT0212P"
                or temp_df_vt_2["Process 2 Model Code"].values == "60CAT0202P"
                or temp_df_vt_2["Process 2 Model Code"].values == "60CAT0213P"
                or temp_df_vt_2["Process 2 Model Code"].values == "60CAT0203P"
                ):

                CheckMaterial("2" ,"M4x40 Screw", temp_df_vt_2["Process 2 M4x40 Screw"].values)
                CheckMaterial("2" ,"Rod Blk", temp_df_vt_2["Process 2 Rod Blk"].values)
                CheckMaterial("2" ,"Df Blk", temp_df_vt_2["Process 2 Df Blk"].values)
                CheckMaterial("2" ,"Df Ring", temp_df_vt_2["Process 2 Df Ring"].values)
                CheckMaterial("2" ,"Washer", temp_df_vt_2["Process 2 Washer"].values)
                CheckMaterial("2" ,"Lock Nut", temp_df_vt_2["Process 2 Lock Nut"].values)

            if (temp_df_vt_2["Process 2 Model Code"].values == "60FC00902P"
                or temp_df_vt_2["Process 2 Model Code"].values == "60FC00903P"
                or temp_df_vt_2["Process 2 Model Code"].values == "60FC00905P"
                or temp_df_vt_2["Process 2 Model Code"].values == "60FC00000P"
                ):

                CheckMaterial("2" ,"M4x40 Screw", temp_df_vt_2["Process 2 M4x40 Screw"].values)
                CheckMaterial("2" ,"Rod Blk", temp_df_vt_2["Process 2 Rod Blk"].values)
                CheckMaterial("2" ,"Df Blk", temp_df_vt_2["Process 2 Df Blk"].values)
                CheckMaterial("2" ,"Washer", temp_df_vt_2["Process 2 Washer"].values)
                CheckMaterial("2" ,"Lock Nut", temp_df_vt_2["Process 2 Lock Nut"].values)

            process2_org_file = process2_curr_file
        #_________________________________________________________________________

        #Process 3
        if process3_curr_file != process3_org_file:
            print("Process 3 Changes Detected")
            refreshJobOrder()

            while True:
                try:
                    read_proc_3_csv()
                    break
                except:
                    pass

            temp_df_vt_3 = process_3_csv.tail(1)

            if (temp_df_vt_3["Process 3 Model Code"].values == "60CAT0213P"
                or temp_df_vt_3["Process 3 Model Code"].values == "60CAT0203P"
                ):

                CheckMaterial("3" ,"Frame Gasket", temp_df_vt_3["Process 3 Frame Gasket"].values)
                CheckMaterial("3" ,"Casing Block", temp_df_vt_3["Process 3 Casing Block"].values)
                CheckMaterial("3" ,"Casing Gasket", temp_df_vt_3["Process 3 Casing Gasket"].values)
                CheckMaterial("3" ,"M4x16 Screw 1", temp_df_vt_3["Process 3 M4x16 Screw 1"].values)
                CheckMaterial("3" ,"M4x16 Screw 2", temp_df_vt_3["Process 3 M4x16 Screw 2"].values)
                CheckMaterial("3" ,"Ball Cushion", temp_df_vt_3["Process 3 Ball Cushion"].values)
                CheckMaterial("3" ,"Partition Board", temp_df_vt_3["Process 3 Partition Board"].values)
                CheckMaterial("3" ,"Built In Tube 1", temp_df_vt_3["Process 3 Built In Tube 1"].values)
                CheckMaterial("3" ,"Built In Tube 2", temp_df_vt_3["Process 3 Built In Tube 2"].values)
                CheckMaterial("3" ,"Frame Cover", temp_df_vt_3["Process 3 Frame Cover"].values)
            
            if (temp_df_vt_3["Process 3 Model Code"].values == "60CAT0212P"
                or temp_df_vt_3["Process 3 Model Code"].values == "60CAT0202P"
                ):

                CheckMaterial("3" ,"Frame Gasket", temp_df_vt_3["Process 3 Frame Gasket"].values)
                CheckMaterial("3" ,"Casing Block", temp_df_vt_3["Process 3 Casing Block"].values)
                CheckMaterial("3" ,"Casing Gasket", temp_df_vt_3["Process 3 Casing Gasket"].values)
                CheckMaterial("3" ,"M4x16 Screw 1", temp_df_vt_3["Process 3 M4x16 Screw 1"].values)
                CheckMaterial("3" ,"M4x16 Screw 2", temp_df_vt_3["Process 3 M4x16 Screw 2"].values)
                CheckMaterial("3" ,"Ball Cushion", temp_df_vt_3["Process 3 Ball Cushion"].values)
                CheckMaterial("3" ,"Frame Cover", temp_df_vt_3["Process 3 Frame Cover"].values)

            if (temp_df_vt_3["Process 3 Model Code"].values == "60FC00902P"
                or temp_df_vt_3["Process 3 Model Code"].values == "60FC00903P"
                or temp_df_vt_3["Process 3 Model Code"].values == "60FC00905P"
                or temp_df_vt_3["Process 3 Model Code"].values == "60FC00000P"
                ):

                CheckMaterial("3" ,"Frame Cover", temp_df_vt_3["Process 3 Frame Cover"].values)
                CheckMaterial("3" ,"Head Cover", temp_df_vt_3["Process 3 Head Cover"].values)
                CheckMaterial("3" ,"Casing Packing", temp_df_vt_3["Process 3 Casing Packing"].values)
                CheckMaterial("3" ,"M4x12 Screw", temp_df_vt_3["Process 3 M4x12 Screw"].values)
                CheckMaterial("3" ,"Csb L", temp_df_vt_3["Process 3 Csb L"].values)
                CheckMaterial("3" ,"Csb R", temp_df_vt_3["Process 3 Csb R"].values)
                CheckMaterial("3" ,"Head Packing", temp_df_vt_3["Process 3 Head Packing"].values)

            process3_org_file = process3_curr_file
        #________________________________________________________________________________________

        #Process 4
        if process4_curr_file != process4_org_file:
            print("Process 4 Changes Detected")
            refreshJobOrder()

            while True:
                try:
                    read_proc_4_csv()
                    break
                except:
                    pass
            
            temp_df_vt_4 = process_4_csv.tail(1)

            if (temp_df_vt_4["Process 4 Model Code"].values == "60CAT0212P"
                or temp_df_vt_4["Process 4 Model Code"].values == "60CAT0202P"
                ):

                CheckMaterial("4" ,"Tank", temp_df_vt_4["Process 4 Tank"].values)
                CheckMaterial("4" ,"Upper Housing", temp_df_vt_4["Process 4 Upper Housing"].values)
                CheckMaterial("4" ,"Cord Hook", temp_df_vt_4["Process 4 Cord Hook"].values)
                CheckMaterial("4" ,"M4x16 Screw", temp_df_vt_4["Process 4 M4x16 Screw"].values)
                CheckMaterial("4" ,"Tank Gasket", temp_df_vt_4["Process 4 Tank Gasket"].values)
                CheckMaterial("4" ,"Tank Cover", temp_df_vt_4["Process 4 Tank Cover"].values)
                CheckMaterial("4" ,"Housing Gasket", temp_df_vt_4["Process 4 Housing Gasket"].values)
                CheckMaterial("4" ,"M4x40 Screw", temp_df_vt_4["Process 4 M4x40 Screw"].values)

            if (temp_df_vt_4["Process 4 Model Code"].values == "60CAT0213P"   
                or temp_df_vt_4["Process 4 Model Code"].values == "60CAT0203P"
                ):

                CheckMaterial("4" ,"Tank", temp_df_vt_4["Process 4 Tank"].values)
                CheckMaterial("4" ,"Upper Housing", temp_df_vt_4["Process 4 Upper Housing"].values)
                CheckMaterial("4" ,"Cord Hook", temp_df_vt_4["Process 4 Cord Hook"].values)
                CheckMaterial("4" ,"M4x16 Screw", temp_df_vt_4["Process 4 M4x16 Screw"].values)
                CheckMaterial("4" ,"PartitionGasket", temp_df_vt_4["Process 4 PartitionGasket"].values)
                CheckMaterial("4" ,"M4x12 Screw", temp_df_vt_4["Process 4 M4x12 Screw"].values)
                CheckMaterial("4" ,"Housing Gasket", temp_df_vt_4["Process 4 Housing Gasket"].values)
                CheckMaterial("4" ,"M4x40 Screw", temp_df_vt_4["Process 4 M4x40 Screw"].values)

            if (temp_df_vt_4["Process 4 Model Code"].values == "60FC00902P"
                or temp_df_vt_4["Process 4 Model Code"].values == "60FC00903P"
                or temp_df_vt_4["Process 4 Model Code"].values == "60FC00905P"
                or temp_df_vt_4["Process 4 Model Code"].values == "60FC00000P"
                ):

                CheckMaterial("4" ,"M4x12 Screw", temp_df_vt_4["Process 4 M4x12 Screw"].values)
                CheckMaterial("4" ,"Muffler", temp_df_vt_4["Process 4 Muffler"].values)
                CheckMaterial("4" ,"Muffler Gasket", temp_df_vt_4["Process 4 Muffler Gasket"].values)
                CheckMaterial("4" ,"VCR", temp_df_vt_4["Process 4 VCR"].values)

            process4_org_file = process4_curr_file
        #____________________________________________________________________________________

        #Process 5
        if process5_curr_file != process5_org_file:
            print("Process 5 Changes Detected")
            refreshJobOrder()

            while True:
                try:
                    read_proc_5_csv()
                    break
                except:
                    pass
            
            temp_df_vt_5 = process_5_csv.tail(1)

            if (temp_df_vt_5["Process 5 Model Code"].values == "60CAT0212P"
                or temp_df_vt_5["Process 5 Model Code"].values == "60CAT0203P"
                or temp_df_vt_5["Process 5 Model Code"].values == "60CAT0213P"
                or temp_df_vt_5["Process 5 Model Code"].values == "60CAT0203P"
                or temp_df_vt_5["Process 5 Model Code"].values == "60CAT0902P"
                or temp_df_vt_5["Process 5 Model Code"].values == "60CAT0903P"
                or temp_df_vt_5["Process 5 Model Code"].values == "60CAT0905P"
                or temp_df_vt_5["Process 5 Model Code"].values == "60CAT0000P"
                ):

                CheckMaterial("5" ,"Rating Label", temp_df_vt_5["Process 5 Rating Label"].values)

            process5_org_file = process5_curr_file
        #_____________________________________________________________________________       

        #Process 6
        if process6_curr_file != process6_org_file:
            print("Process 6 Changes Detected")
            refreshJobOrder()

            while True:
                try:
                    read_proc_6_csv()
                    break
                except:
                    pass

            temp_df_vt_6 = process_6_csv.tail(1)

            if (temp_df_vt_6["Process 6 Model Code"].values == "60CAT0212P"
                or temp_df_vt_6["Process 6 Model Code"].values == "60CAT0203P"
                or temp_df_vt_6["Process 6 Model Code"].values == "60CAT0213P"
                or temp_df_vt_6["Process 6 Model Code"].values == "60CAT0203P"
                or temp_df_vt_6["Process 6 Model Code"].values == "60CAT0902P"
                or temp_df_vt_6["Process 6 Model Code"].values == "60CAT0903P"
                or temp_df_vt_6["Process 6 Model Code"].values == "60CAT0905P"
                or temp_df_vt_6["Process 6 Model Code"].values == "60CAT0000P"
                ):

                CheckMaterial("6" ,"Vinyl", temp_df_vt_6["Process 6 Vinyl"].values)

            process6_org_file = process6_curr_file

        #Deviation
        if compiledPiFileCurrent != compiledPiFileOrig:
            print("Inspection Machine Changes Detected")
            RunDeviationDetection(True)

            compiledPiFileOrig = compiledPiFileCurrent

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
            if temp_df_vt_1[f"Process 1 {material}"].values[0] == a:
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
            if temp_df_vt_2[f"Process 2 {material}"].values[0] == a:
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
            if temp_df_vt_3[f"Process 3 {material}"].values[0] == a:
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
            if temp_df_vt_4[f"Process 4 {material}"].values[0] == a:
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
            if temp_df_vt_5[f"Process 5 {material}"].values[0] == a:
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
            if temp_df_vt_6[f"Process 6 {material}"].values[0] == a:
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