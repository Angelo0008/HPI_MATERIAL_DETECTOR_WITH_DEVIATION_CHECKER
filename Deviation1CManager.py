#%%

#   RUNNING 
# DOES NOT READ THE PASS TWICE DUE TO THE NG IS ACTIVATED


# RUN THESE TO JUPITER
# ReadFiles()
# EmptyColumnCreator()
# PopulateContent()



import pandas as pd
import time
import os
from datetime import datetime

# Tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
import threading
import VariableManager as varMan

import WrongMaterialDetector
import EventLogging

# Global variables to track processed rows
processed_sn = set()
current_sn = None
rowCountOrig = 0
rowCountCurrent = 0

def ReadFiles():
    global df
    global processed_sn
    global current_sn
    global rowCountOrig

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # --- Load data ---
    file_path = r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv" #pi machine

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
    # df = df[(~df["PASS/NG"].isin([0]))]

    # NO NEED TO EDIT (CONSTANT)
    # --- CLEANING before loop ---
    df['S/N'] = df['S/N'].astype(str)
    df['MODEL CODE'] = df['MODEL CODE'].astype(str)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.dropna(subset=['DATE'])
    df = df[df['S/N'].str.len() >= 8]
    df = df[~df['MODEL CODE'].str.contains('M')]

    # --- Add the READER column --- #NEW
    df["READER"] = 0                #NEW
                                                                       
    # Reset processed S/N set when reading new file
    processed_sn = set()                 #new
    current_sn = None                    #new

    rowCountOrig = df.shape[0]

def automaticStopper():
    time.sleep(2)
    WrongMaterialDetector.disable_deviation()

def EmptyColumnCreator():
    global compiledFrame

    # --- Blank frame ---
    emptyColumn = [
        "DATE", 
        "TIME", 
        "MODEL CODE", 
        "S/N", 
        "PASS/NG",

        "VOLTAGE MAX (V)", 
        "V_MAX PASS", 
        "AVE V_MAX PASS",                   
        "DEV V_MAX PASS",

        "WATTAGE MAX (W)",
        "WATTAGE MAX PASS",
        "AVE WATTAGE MAX (W)",                  
        "DEV WATTAGE MAX (W)",

        "CLOSED PRESSURE_MAX (kPa)",
        "CLOSED PRESSURE_MAX PASS",
        "AVE CLOSED PRESSURE_MAX (kPa)",        
        "DEV CLOSED PRESSURE_MAX (kPa)", 

        "VOLTAGE Middle (V)",
        "VOLTAGE Middle PASS",                  
        "AVE VOLTAGE Middle (V)",
        "DEV VOLTAGE Middle (V)",

        "WATTAGE Middle (W)",
        "WATTAGE Middle (W) PASS",              
        "AVE WATTAGE Middle (W)",
        "DEV WATTAGE Middle (W)",

        "AMPERAGE Middle (A)",
        "AMPERAGE Middle (A) PASS",             
        "AVE AMPERAGE Middle (A)",
        "DEV AMPERAGE Middle (A)",

        "CLOSED PRESSURE Middle (kPa)",
        "CLOSED PRESSURE Middle (kPa) PASS",    
        "AVE CLOSED PRESSURE Middle (kPa)",
        "DEV CLOSED PRESSURE Middle (kPa)",

        "VOLTAGE MIN (V)",
        "VOLTAGE MIN (V) PASS",                 
        "AVE VOLTAGE MIN (V)",
        "DEV VOLTAGE MIN (V)",

        "WATTAGE MIN (W)",
        "WATTAGE MIN (W) PASS",                 
        "AVE WATTAGE MIN (W)",
        "DEV WATTAGE MIN (W)",

        "CLOSED PRESSURE MIN (kPa)",
        "CLOSED PRESSURE MIN (kPa) PASS",       
        "AVE CLOSED PRESSURE MIN (kPa)",
        "DEV CLOSED PRESSURE MIN (kPa)"
    ]
    compiledFrame = pd.DataFrame(columns=emptyColumn)

def PopulateContent():
    global model_summary
    global compiledFrame
    global current_sn

    dataList = []

    # S/N that are already in compiledFrame                         #NEW2
    existing_sn = set(compiledFrame["S/N"].astype(str).values)      #NEW2

    # --- Custom loop FIRST (to populate compiledFrame) ---
    for a in range(len(df)):
        tempdf = df.iloc[[a]]

        # Only read rows that have not been read yet    #NEW
        # if tempdf["READER"].values[0] == 1:             #NEW
        #     continue                                    #NEW

        model_code = tempdf["MODEL CODE"].values[0]
        current_sn = tempdf["S/N"].values[0]

        # # Skip if this S/N was already processed
        # if current_sn in processed_sn:
        #     continue

        # Skip if this S/N was already processed in this pass or already in compiledFrame   #NEW2
        if current_sn in processed_sn or str(current_sn) in existing_sn:    #NEW2
            continue    #NEW2

        processed_sn.add(current_sn)

        dataFrame = {
            "DATE": tempdf["DATE"].values[0],
            "TIME": tempdf["TIME"].values[0],
            "MODEL CODE": model_code,
            "S/N": current_sn,
            "PASS/NG": tempdf["PASS/NG"].values[0],
            "VOLTAGE MAX (V)": tempdf["VOLTAGE MAX (V)"].values[0],
            "WATTAGE MAX (W)": tempdf["WATTAGE MAX (W)"].values[0],
            "CLOSED PRESSURE_MAX (kPa)": tempdf["CLOSED PRESSURE_MAX (kPa)"].values[0],
            "VOLTAGE Middle (V)": tempdf["VOLTAGE Middle (V)"].values[0],
            "WATTAGE Middle (W)": tempdf["WATTAGE Middle (W)"].values[0],
            "AMPERAGE Middle (A)": tempdf["AMPERAGE Middle (A)"].values[0],
            "CLOSED PRESSURE Middle (kPa)": tempdf["CLOSED PRESSURE Middle (kPa)"].values[0],
            "VOLTAGE MIN (V)": tempdf["VOLTAGE MIN (V)"].values[0],
            "WATTAGE MIN (W)": tempdf["WATTAGE MIN (W)"].values[0],
            "CLOSED PRESSURE MIN (kPa)": tempdf["CLOSED PRESSURE MIN (kPa)"].values[0]
        }

        if tempdf["PASS/NG"].values[0] == 1:
            dataFrame["V_MAX PASS"] = tempdf["VOLTAGE MAX (V)"].values[0]
            dataFrame["WATTAGE MAX PASS"] = tempdf["WATTAGE MAX (W)"].values[0]
            dataFrame["CLOSED PRESSURE_MAX PASS"] = tempdf["CLOSED PRESSURE_MAX (kPa)"].values[0]
            dataFrame["VOLTAGE Middle PASS"] = tempdf["VOLTAGE Middle (V)"].values[0]
            dataFrame["WATTAGE Middle (W) PASS"] = tempdf["WATTAGE Middle (W)"].values[0]
            dataFrame["AMPERAGE Middle (A) PASS"] = tempdf["AMPERAGE Middle (A)"].values[0]
            dataFrame["CLOSED PRESSURE Middle (kPa) PASS"] = tempdf["CLOSED PRESSURE Middle (kPa)"].values[0]
            dataFrame["VOLTAGE MIN (V) PASS"] = tempdf["VOLTAGE MIN (V)"].values[0]
            dataFrame["WATTAGE MIN (W) PASS"] = tempdf["WATTAGE MIN (W)"].values[0]
            dataFrame["CLOSED PRESSURE MIN (kPa) PASS"] = tempdf["CLOSED PRESSURE MIN (kPa)"].values[0]
        # else:
        #     # Set all PASS columns to 0 when PASS/NG is 0
        #     dataFrame["V_MAX PASS"] = 0
        #     dataFrame["WATTAGE MAX PASS"] = 0
        #     dataFrame["CLOSED PRESSURE_MAX PASS"] = 0
        #     dataFrame["VOLTAGE Middle PASS"] = 0
        #     dataFrame["WATTAGE Middle (W) PASS"] = 0
        #     dataFrame["AMPERAGE Middle (A) PASS"] = 0
        #     dataFrame["CLOSED PRESSURE Middle (kPa) PASS"] = 0
        #     dataFrame["VOLTAGE MIN (V) PASS"] = 0
        #     dataFrame["WATTAGE MIN (W) PASS"] = 0
        #     dataFrame["CLOSED PRESSURE MIN (kPa) PASS"] = 0
            
        dataList.append(dataFrame)
        # Mark this S/N as processed and set READER=1 in the original df    #NEW
        # processed_sn.add(current_sn)  # Mark this S/N as processed          
        # df.loc[df["S/N"] == current_sn, "READER"] = 1                       #NEW

    dataFrame = pd.DataFrame(dataList)
    compiledFrame = pd.concat([compiledFrame, dataFrame], ignore_index=True)

    # --- COMPUTE model_summary AFTER compiledFrame exists --- (REVISED)
    today = pd.to_datetime(datetime.now().date())
    results = []

    for model, group in compiledFrame.groupby('MODEL CODE'):
        past_data = group[group['DATE'].dt.date < today.date()]
        if past_data.empty:
            print(f" Skipping {model}: No past data")
            continue

        past_data = past_data.sort_values('DATE', ascending=False)
        accumulated_rows = pd.DataFrame()
        count = 0

        for date in past_data['DATE'].dt.date.unique():
            daily_rows = past_data[past_data['DATE'].dt.date == date]
            valid_rows = daily_rows[daily_rows["PASS/NG"] == 1]
            accumulated_rows = pd.concat([accumulated_rows, valid_rows])
            count += len(valid_rows)
            if count >= 200:
                latest_valid_date = date
                break

        if count < 200:
            print(f" Skipping {model}: Not enough valid PASS/NG rows")
            continue

        pass_avg = accumulated_rows["V_MAX PASS"].mean()
        wattage_avg = accumulated_rows["WATTAGE MAX PASS"].mean()
        closedPressure_avg = accumulated_rows["CLOSED PRESSURE_MAX PASS"].mean()
        voltageMiddle_avg = accumulated_rows["VOLTAGE Middle PASS"].mean()
        wattageMiddle_avg = accumulated_rows["WATTAGE Middle (W) PASS"].mean()
        amperageMiddle_avg = accumulated_rows["AMPERAGE Middle (A) PASS"].mean()
        closePressureMiddle_avg = accumulated_rows["CLOSED PRESSURE Middle (kPa) PASS"].mean()
        voltageMin_avg = accumulated_rows["VOLTAGE MIN (V) PASS"].mean()
        wattageMin_avg = accumulated_rows["WATTAGE MIN (W) PASS"].mean()
        closePressureMin_avg = accumulated_rows["CLOSED PRESSURE MIN (kPa) PASS"].mean()

        results.append({
            'MODEL CODE': model,
            'LATEST DATE': latest_valid_date,
            'V-MAX PASS AVG': pass_avg,
            'WATTAGE MAX AVG': wattage_avg,
            'CLOSED PRESSURE_MAX AVG': closedPressure_avg,
            'VOLTAGE Middle AVG': voltageMiddle_avg,
            'WATTAGE Middle AVG': wattageMiddle_avg,
            'AMPERAGE Middle AVG': amperageMiddle_avg,
            'CLOSED PRESSURE Middle AVG': closePressureMiddle_avg,
            'VOLTAGE MIN (V) AVG': voltageMin_avg,
            'WATTAGE MIN AVG': wattageMin_avg,
            'CLOSED PRESSURE MIN AVG': closePressureMin_avg
        })

    model_summary = pd.DataFrame(results)
    pass_avg_map = model_summary.set_index("MODEL CODE")["V-MAX PASS AVG"].to_dict()
    wattage_avg_map = model_summary.set_index("MODEL CODE")["WATTAGE MAX AVG"].to_dict()
    closedPressure_avg_map = model_summary.set_index("MODEL CODE")['CLOSED PRESSURE_MAX AVG'].to_dict()
    voltageMiddle_avg_map = model_summary.set_index("MODEL CODE")["VOLTAGE Middle AVG"].to_dict()
    wattageMiddle_avg = model_summary.set_index("MODEL CODE")["WATTAGE Middle AVG"].to_dict()
    amperageMiddle_avg = model_summary.set_index("MODEL CODE")["AMPERAGE Middle AVG"].to_dict()
    closePressureMiddle_avg = model_summary.set_index("MODEL CODE")["CLOSED PRESSURE Middle AVG"].to_dict()
    voltageMin_avg = model_summary.set_index("MODEL CODE")["VOLTAGE MIN (V) AVG"].to_dict()
    wattageMin_avg = model_summary.set_index("MODEL CODE")["WATTAGE MIN AVG"].to_dict()
    closePressureMin_avg = model_summary.set_index("MODEL CODE")["CLOSED PRESSURE MIN AVG"].to_dict()

    # --- Inject AVERAGE DISPLAY ---
    compiledFrame["AVE V_MAX PASS"] = compiledFrame["MODEL CODE"].map(pass_avg_map)
    compiledFrame["AVE WATTAGE MAX (W)"] = compiledFrame["MODEL CODE"].map(wattage_avg_map)
    compiledFrame["AVE CLOSED PRESSURE_MAX (kPa)"] = compiledFrame["MODEL CODE"].map(closedPressure_avg_map)
    compiledFrame["AVE VOLTAGE Middle (V)"] = compiledFrame["MODEL CODE"].map(voltageMiddle_avg_map)
    compiledFrame["AVE WATTAGE Middle (W)"] = compiledFrame["MODEL CODE"].map(wattageMiddle_avg)
    compiledFrame["AVE AMPERAGE Middle (A)"] = compiledFrame["MODEL CODE"].map(amperageMiddle_avg)
    compiledFrame["AVE CLOSED PRESSURE Middle (kPa)"] = compiledFrame["MODEL CODE"].map(closePressureMiddle_avg)
    compiledFrame["AVE VOLTAGE MIN (V)"] = compiledFrame["MODEL CODE"].map(voltageMin_avg)
    compiledFrame["AVE WATTAGE MIN (W)"] = compiledFrame["MODEL CODE"].map(wattageMin_avg)
    compiledFrame["AVE CLOSED PRESSURE MIN (kPa)"] = compiledFrame["MODEL CODE"].map(closePressureMin_avg)

    # --- Compute DEV DISPLAY ---
    compiledFrame["DEV V_MAX PASS"] = (compiledFrame["AVE V_MAX PASS"] - compiledFrame["V_MAX PASS"]) / compiledFrame["AVE V_MAX PASS"]
    compiledFrame["DEV WATTAGE MAX (W)"] = (compiledFrame["AVE WATTAGE MAX (W)"] - compiledFrame["WATTAGE MAX PASS"]) / compiledFrame["AVE WATTAGE MAX (W)"]
    compiledFrame["DEV CLOSED PRESSURE_MAX (kPa)"] = (compiledFrame["AVE CLOSED PRESSURE_MAX (kPa)"] - compiledFrame["CLOSED PRESSURE_MAX PASS"]) / compiledFrame["AVE CLOSED PRESSURE_MAX (kPa)"].astype(float)
    compiledFrame["DEV VOLTAGE Middle (V)"] = (compiledFrame["AVE VOLTAGE Middle (V)"] - compiledFrame["VOLTAGE Middle PASS"]) / compiledFrame["AVE VOLTAGE Middle (V)"]
    compiledFrame["DEV WATTAGE Middle (W)"] = (compiledFrame["AVE WATTAGE Middle (W)"] - compiledFrame["WATTAGE Middle (W) PASS"]) / compiledFrame["AVE WATTAGE Middle (W)"]
    compiledFrame["DEV AMPERAGE Middle (A)"] = (compiledFrame["AVE AMPERAGE Middle (A)"] - compiledFrame["AMPERAGE Middle (A) PASS"]) / compiledFrame["AVE AMPERAGE Middle (A)"]
    compiledFrame["DEV CLOSED PRESSURE Middle (kPa)"] = (compiledFrame["AVE CLOSED PRESSURE Middle (kPa)"] - compiledFrame["CLOSED PRESSURE Middle (kPa) PASS"]) / compiledFrame["AVE CLOSED PRESSURE Middle (kPa)"]
    compiledFrame["DEV VOLTAGE MIN (V)"] = (compiledFrame["AVE VOLTAGE MIN (V)"] - compiledFrame["VOLTAGE MIN (V) PASS"]) / compiledFrame["AVE VOLTAGE MIN (V)"]
    compiledFrame["DEV WATTAGE MIN (W)"] = (compiledFrame["AVE WATTAGE MIN (W)"] - compiledFrame["WATTAGE MIN (W) PASS"]) / compiledFrame["AVE WATTAGE MIN (W)"]
    compiledFrame["DEV CLOSED PRESSURE MIN (kPa)"] = (compiledFrame["AVE CLOSED PRESSURE MIN (kPa)"] - compiledFrame["CLOSED PRESSURE MIN (kPa) PASS"]) / compiledFrame["AVE CLOSED PRESSURE MIN (kPa)"]

def DeviationChecker():
    global current_sn
    
    # Skip if no current S/N or if we've already processed this S/N
    if current_sn is None or current_sn not in compiledFrame["S/N"].values:
        return

    # Get the row for the current S/N
    current_row = compiledFrame[compiledFrame["S/N"] == current_sn].iloc[-1]
    sn_value = current_row["S/N"]

    #1
    value = current_row["DEV V_MAX PASS"]
    print(f"1 DEV V_MAX PASS VALUES - S/N {sn_value}: {value:.3f}")
    if value > 0.05 or value < -0.05:
        print("DEV V_MAX PASS DEVIATION DETECTED")
        varMan.isDeviationDetected = True
        WrongMaterialDetector.InsertInLogWindow(f"1    S/N {sn_value} - V_MAX DEVIATION DETECTED:                                               {value:.3f}")
        EventLogging.logEvent(f"DEV V_MAX DEVIATION DETECTED - S/N {sn_value}: {value:.3f}")  # NOTEPAD

        autoStopper = threading.Thread(target=automaticStopper)
        autoStopper.start()
    else:
        print(f"DEV V_MAX PASS DEVIATION GOOD - S/N {sn_value}: {value:.3f}")

    #2
    value = current_row["DEV WATTAGE MAX (W)"]
    print(f"DEV WATTAGE MAX (W) VALUES - S/N {sn_value}: {value:.3f}")
    if value > 0.05 or value < -0.05:
        print(" DEV WATTAGE MAX (W) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
        WrongMaterialDetector.InsertInLogWindow(f"2    S/N {sn_value} - WATTAGE MAX DEVIATION DETECTED:                                {value:.3f}")
        EventLogging.logEvent(f"DEV WATTAGE MAX DEVIATION DETECTED - S/N {sn_value}: {value:.3f}")  # NOTEPAD

        autoStopper = threading.Thread(target=automaticStopper)
        autoStopper.start()
    else:
        print(f"DEV WATTAGE MAX (W) DEVIATION GOOD - S/N {sn_value}: {value:.3f}")

    #3
    value = current_row["DEV CLOSED PRESSURE_MAX (kPa)"]
    print(f"DEV CLOSED PRESSURE_MAX (kPa) VALUES - S/N {sn_value}: {value:.3f}")
    if value > 0.05 or value < -0.05:
        print("DEV CLOSED PRESSURE_MAX (kPa) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
        WrongMaterialDetector.InsertInLogWindow(f"3    S/N {sn_value} - CLOSED PRESSURE MAX DEVIATION DETECTED:             {value:.3f}")
        EventLogging.logEvent(f"DEV CLOSED PRESSURE MAX DEVIATION DETECTED - S/N {sn_value}: {value:.3f}")  # NOTEPAD

        autoStopper = threading.Thread(target=automaticStopper)
        autoStopper.start()
    else:
        print(f"DEV CLOSED PRESSURE_MAX (kPa) DEVIATION GOOD - S/N {sn_value}: {value:.3f}")

    #4
    value = current_row["DEV VOLTAGE Middle (V)"]
    print(f"DEV VOLTAGE Middle (V) VALUES - S/N {sn_value}: {value:.3f}")
    if value > 0.05 or value < -0.05:
        print("DEV VOLTAGE Middle (V) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
        WrongMaterialDetector.InsertInLogWindow(f"4    S/N {sn_value} - VOLTAGE MIDDLE DEVIATION DETECTED:                          {value:.3f}")
        EventLogging.logEvent(f"DEV VOLTAGE MIDDLE DEVIATION DETECTED - S/N {sn_value}: {value:.3f}")  # NOTEPAD

        autoStopper = threading.Thread(target=automaticStopper)
        autoStopper.start()
    else:
        print(f"DEV VOLTAGE Middle (V) DEVIATION GOOD - S/N {sn_value}: {value:.3f}")

    #5
    value = current_row["DEV WATTAGE Middle (W)"]
    print(f"DEV WATTAGE Middle (W) VALUES - S/N {sn_value}: {value:.3f}")
    if value > 0.05 or value < -0.05:
        print("DEV WATTAGE Middle (W) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
        WrongMaterialDetector.InsertInLogWindow(f"5    S/N {sn_value} - WATTAGE MIDDLE DEVIATION DETECTED:                         {value:.3f}")
        EventLogging.logEvent(f"DEV WATTAGE MIDDLE DEVIATION DETECTED - S/N {sn_value}: {value:.3f}")

        autoStopper = threading.Thread(target=automaticStopper)
        autoStopper.start()
    else:
        print(f"DEV WATTAGE Middle (W) DEVIATION GOOD - S/N {sn_value}: {value:.3f}")

    #6
    value = current_row["DEV AMPERAGE Middle (A)"]
    print(f"DEV AMPERAGE Middle (A) VALUES - S/N {sn_value}: {value:.3f}")
    if value > 0.05 or value < -0.05:
        print("DEV AMPERAGE Middle (A) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
        WrongMaterialDetector.InsertInLogWindow(f"6    S/N {sn_value} - AMPERAGE MIDDLE DEVIATION DETECTED:                       {value:.3f}")
        EventLogging.logEvent(f"DEV AMPERAGE MIDDLE DEVIATION DETECTED - S/N {sn_value}: {value:.3f}")  # NOTEPAD

        autoStopper = threading.Thread(target=automaticStopper)
        autoStopper.start()
    else:
        print(f"DEV AMPERAGE Middle (A) DEVIATION GOOD - S/N {sn_value}: {value:.3f}")

    #7
    value = current_row["DEV CLOSED PRESSURE Middle (kPa)"]
    print(f"DEV CLOSED PRESSURE Middle (kPa) VALUES - S/N {sn_value}: {value:.3f}")
    if value > 0.05 or value < -0.05:
        print("DEV CLOSED PRESSURE Middle (kPa) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
        WrongMaterialDetector.InsertInLogWindow(f"7    S/N {sn_value} - CLOSED PRESSURE MIDDLE DEVIATION DETECTED:       {value:.3f}")
        EventLogging.logEvent(f"DEV CLOSED PRESSURE MIDDLE DEVIATION DETECTED - S/N {sn_value}: {value:.3f}")  # NOTEPAD

        autoStopper = threading.Thread(target=automaticStopper)
        autoStopper.start()
    else:
        print(f"DEV CLOSED PRESSURE Middle (kPa) DEVIATION GOOD - S/N {sn_value}: {value:.3f}")

    #8
    value = current_row["DEV VOLTAGE MIN (V)"]
    print(f"DEV VOLTAGE MIN (V) VALUES - S/N {sn_value}: {value:.3f}")
    if value > 0.05 or value < -0.05:
        print("DEV VOLTAGE MIN (V) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
        WrongMaterialDetector.InsertInLogWindow(f"8    S/N {sn_value} - VOLTAGE MIN DEVIATION DETECTED:                                  {value:.3f}")
        EventLogging.logEvent(f"8  DEV VOLTAGE MIN DEVIATION DETECTED - S/N {sn_value}: {value:.3f}")  # NOTEPAD

        autoStopper = threading.Thread(target=automaticStopper)
        autoStopper.start()
    else:
        print(f"DEV VOLTAGE MIN (V) DEVIATION GOOD - S/N {sn_value}: {value:.3f}")

    #9
    value = current_row["DEV WATTAGE MIN (W)"]
    print(f"DEV WATTAGE MIN (W) VALUES - S/N {sn_value}: {value:.3f}")
    if value > 0.05 or value < -0.05:
        print("DEV WATTAGE MIN (W) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
        WrongMaterialDetector.InsertInLogWindow(f"9    S/N {sn_value} - WATTAGE MIN DEVIATION DETECTED:                                 {value:.3f}")
        EventLogging.logEvent(f"9  DEV WATTAGE MIN DEVIATION DETECTED - S/N {sn_value}: {value:.3f}")  # NOTEPAD

        autoStopper = threading.Thread(target=automaticStopper)
        autoStopper.start()
    else:
        print(f"DEV WATTAGE MIN (W) DEVIATION GOOD - S/N {sn_value}: {value:.3f}")

    #10
    value = current_row["DEV CLOSED PRESSURE MIN (kPa)"]
    print(f"10 DEV CLOSED PRESSURE MIN (kPa) VALUES - S/N {sn_value}: {value:.3f}")
    if value > 0.05 or value < -0.05:
        print("DEV CLOSED PRESSURE MIN (kPa) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
        WrongMaterialDetector.InsertInLogWindow(f"10  S/N {sn_value} - CLOSED PRESSURE MIN DEVIATION DETECTED:              {value:.3f}")
        EventLogging.logEvent(f"10 DEV CLOSED PRESSURE MIN DEVIATION DETECTED - S/N {sn_value}: {value:.3f}")

        autoStopper = threading.Thread(target=automaticStopper)
        autoStopper.start()
    else:
        print(f"10 DEV CLOSED PRESSURE MIN (kPa) DEVIATION GOOD - S/N {sn_value}: {value:.3f}")

    if varMan.isDeviationDetected:
        print("⚠️ DEVIATION DETECTED")
        
        varMan.deviation_err_msg_text =  "⚠️ DEVIATION DETECTED"
        varMan.deviation_err_msg.config(text=varMan.deviation_err_msg_text)
        varMan.deviation_stop_btn.config(bg="red")
    else:
        print("✅ NO DEVIATION DETECTED")

def UpdateLoading():
    if varMan.deviation_err_msg_text == "Loading...":
        varMan.deviation_err_msg_text = "Loading"
        varMan.deviation_err_msg.config(text=varMan.deviation_err_msg_text, font=("Arial", 12))

    else:
        varMan.deviation_err_msg_text += "."
        varMan.deviation_err_msg.config(text=varMan.deviation_err_msg_text, font=("Arial", 12))


def startProgram():
    ReadFiles()
    EmptyColumnCreator()
    PopulateContent()
    DeviationChecker()

def run():
    global rowCountOrig
    global rowCountCurrent

    #Reading Original File
    compiledPiFileOrig =os.path.getmtime(r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv") #pi machine
    # compiledPiFileOrig = os.path.getmtime(r'C:\Users\prod.fcline1\OneDrive - HIBLOW PHILIPPINES INC\CompiledPIMachine.csv') # ONE DRIVE PATH
    # compiledPiFileOrig = os.path.getmtime(r"C:\Users\ai.pc\OneDrive\Desktop\CompiledPIMachine.csv") # DESKTOP FALSE TESTING

    while True:
        if not varMan.isDeviationDetected:
            #Reading Original File
            compiledPiFileCurrent = os.path.getmtime(r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv") #pi machine
            # compiledPiFileCurrent = os.path.getmtime(r'C:\Users\prod.fcline1\OneDrive - HIBLOW PHILIPPINES INC\CompiledPIMachine.csv') # ONE DRIVE PATH 
            # compiledPiFileCurrent = os.path.getmtime(r"C:\Users\ai.pc\OneDrive\Desktop\CompiledPIMachine.csv") # DESKTOP FALSE TESTING                               
        
            if compiledPiFileCurrent != compiledPiFileOrig:
                print("FILE CHANGES DETECTED")

                #Run Program
                # print("🚀 Running model analysis...")
                ReadFiles()
                if rowCountCurrent != rowCountOrig:
                    EmptyColumnCreator()
                    PopulateContent()
                    DeviationChecker()

                compiledPiFileOrig = compiledPiFileCurrent

                rowCountCurrent = rowCountOrig
                
            

            print("WAITING FOR CHANGES IN CSV FILE")
            time.sleep(1)


# %%
