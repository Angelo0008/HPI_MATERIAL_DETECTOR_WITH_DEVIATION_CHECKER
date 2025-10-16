# %%
from Imports import *
import JobOrderManagerVer2 as JOManager
import serial
# import Deviation1CManager
import ExecutableManager
import VariableManager as varMan



# %%
Engine = ""
prog_run = True
is_debug = False

# Process 1
process_1_csv = ""

proc_1_Mtrl_1_code = ""
proc_1_Mtrl_2_code = ""
proc_1_Mtrl_3_code = ""
proc_1_Mtrl_4_code = ""
proc_1_Mtrl_5_code = ""


proc_1_txt = ""
proc_1_stop_btn = ""
proc_1_err_msg = ""
proc_1_err_msg_txt = "Loading"
proc_1_is_wrong_itm = False
is_read_proc1_csv = False
# Add time tolerance error flag
proc_1_time_out_of_tolerance = False


# Process 2
proc_2_csv = ""

proc_2_Mtrl_1_code = ""
proc_2_Mtrl_2_code = ""
proc_2_Mtrl_3_code = ""
proc_2_Mtrl_4_code = ""
proc_2_Mtrl_5_code = ""


proc_2_txt = ""
proc_2_stop_btn = ""
proc_2_err_msg = ""
proc_2_err_msg_txt = "Loading"
proc_2_is_wrong_itm = False
is_read_proc2_csv = False
# Add time tolerance error flag
proc_2_time_out_of_tolerance = False


# Process 3
proc_3_csv = ""

proc_3_Mtrl_1_code = ""
proc_3_Mtrl_2_code = ""
proc_3_Mtrl_3_code = ""
proc_3_Mtrl_4_code = ""
proc_3_Mtrl_5_code = ""


proc_3_txt = ""
proc_3_stop_btn = ""
proc_3_err_msg = ""
proc_3_err_msg_txt = "Loading"
proc_3_is_wrong_itm = False
is_read_proc3_csv = False
# Add time tolerance error flag
proc_3_time_out_of_tolerance = False


# Process 4
proc_4_csv = ""

proc_4_Mtrl_1_code = ""
proc_4_Mtrl_2_code = ""
proc_4_Mtrl_3_code = ""
proc_4_Mtrl_4_code = ""
proc_4_Mtrl_5_code = ""


proc_4_txt = ""
proc_4_stop_btn = ""
proc_4_err_msg = ""
proc_4_err_msg_txt = "Loading"
proc_4_is_wrong_itm = False
is_read_proc4_csv = False
# Add time tolerance error flag
proc_4_time_out_of_tolerance = False


# Process 5
proc_5_csv = ""

proc_5_Mtrl_1_code = ""
proc_5_Mtrl_2_code = ""
proc_5_Mtrl_3_code = ""
proc_5_Mtrl_4_code = ""
proc_5_Mtrl_5_code = ""


proc_5_txt = ""
proc_5_stop_btn = ""
proc_5_err_msg = ""
proc_5_err_msg_txt = "Loading"
proc_5_is_wrong_itm = False
is_read_proc5_csv = False
# Add time tolerance error flag
proc_5_time_out_of_tolerance = False


# Process 6
proc_6_csv = ""

proc_6_Mtrl_1_code = ""
proc_6_Mtrl_2_code = ""
proc_6_Mtrl_3_code = ""
proc_6_Mtrl_4_code = ""
proc_6_Mtrl_5_code = ""


proc_6_txt = ""
proc_6_stop_btn = ""
proc_6_err_msg = ""
proc_6_err_msg_txt = "Loading"
proc_6_is_wrong_itm = False
is_read_proc6_csv = False
# Add time tolerance error flag
proc_6_time_out_of_tolerance = False

is_speaking = False

is_proc_1_by_pass = False
is_proc_2_by_pass = False
is_proc_3_by_pass = False
is_proc_4_by_pass = False
is_proc_5_by_pass = False
is_proc_6_by_pass = False

sound_title = ""

log_count = 0

ser = None

def arduinoConnection():
    global ser
    global comPort

    comPort = 2
    while True:
        try:
            ser = serial.Serial(f'COM{comPort}', 9600)
            print(f"Com Port Connection: {comPort}")
            break
        except:
            pass
            comPort += 1

def disable_deviation():
    varMan.deviation_err_msg_text = "Loading..."
    varMan.deviation_err_msg.config(text=varMan.deviation_err_msg_text, fg="black")

    varMan.deviation_txt.config(text="DeviationChecker", fg="black")

    varMan.deviation_stop_btn.config(bg="orange")
    varMan.isDeviationDetected = False

# %%
def stop_prog():
    global prog_run
    global proc_1_is_wrong_itm
    global proc_2_is_wrong_itm
    global proc_3_is_wrong_itm
    global proc_4_is_wrong_itm
    global proc_5_is_wrong_itm
    global proc_6_is_wrong_itm

    prog_run = False
    proc_1_is_wrong_itm = False
    proc_2_is_wrong_itm = False
    proc_3_is_wrong_itm = False
    proc_4_is_wrong_itm = False
    proc_5_is_wrong_itm = False
    proc_6_is_wrong_itm = False

    root.destroy()
        
def InsertInMaterialLogWindow(state, message):
    varMan.materialLogWindow.configure(state ='normal')

    # Inserting Text which is read only
    if state == 0:
        varMan.materialLogWindow.insert(tk.INSERT, f"{message}\n", "red")
    elif state == 1:
        varMan.materialLogWindow.insert(tk.INSERT, f"{message}\n")

    varMan.materialLogWindow.configure(state ='disabled')

def ClearMaterialLogWindow():
    varMan.materialLogWindow.configure(state='normal')
    varMan.materialLogWindow.delete('1.0', tk.END)
    varMan.materialLogWindow.configure(state='disabled')

def InsertInLogWindow(message):
    varMan.deviation_time_text.configure(state ='normal')
    # Inserting Text which is read only
    varMan.deviation_time_text.insert(tk.INSERT, f"{message}\n")
    varMan.deviation_time_text.configure(state ='disabled')

def ClearLogWindow():
    varMan.deviation_time_text.configure(state='normal')
    varMan.deviation_time_text.delete('1.0', tk.END)
    varMan.deviation_time_text.configure(state='disabled')

def open_new_window():
    global jobOrderMaterialsText
    global new_win

    try:
        new_win.destroy()
    except:
        pass

    materials = ""

    new_win = tk.Toplevel(root)  # Create a new top-level window
    new_win.title(f"JO Num. {JOManager.read_job_order} JO Date: {JOManager.jobOrderDate} JO Time: {JOManager.jobOrderTime}")
    new_win.geometry("550x400")

    frame = tk.Frame(new_win)
    frame.pack(fill="both", expand=True)

    # Scrollbar
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    # Text widget (instead of Label)
    text_widget = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set, font=("Arial", 12))
    text_widget.pack(fill="both", expand=True)

    # Connect scrollbar to text widget
    scrollbar.config(command=text_widget.yview)

    ExecutableManager.refreshJobOrder()

    for a in JOManager.job_order_materials:
        materials += f"{a}\n"

    text_widget.insert("1.0", materials)
    text_widget.config(state="disabled")  # make it read-only

def backWindow():
    global frame1, frame2

    frame1.pack()
    frame2.pack_forget()

def nextWindow():
    global frame1, frame2

    frame1.pack_forget()
    frame2.pack()

def createVoltageFigure():
    global frame2

    canvas = FigureCanvasTkAgg(varMan.voltageFig, master=frame2)
    canvas.draw()
    canvas.get_tk_widget().grid(row=5, column=0, ipadx=5)

    canvas2 = FigureCanvasTkAgg(varMan.wattageFig, master=frame2)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=5, column=1, ipadx=5)

    canvas3 = FigureCanvasTkAgg(varMan.amperageFig, master=frame2)
    canvas3.draw()
    canvas3.get_tk_widget().grid(row=6, column=0, ipadx=5)

    canvas4 = FigureCanvasTkAgg(varMan.closedPressureFig, master=frame2)
    canvas4.draw()
    canvas4.get_tk_widget().grid(row=6, column=1, ipadx=5)

def addVoltageTolerance():
    varMan.voltageTolerance += 1
    voltageToleranceText.config(text=f"{varMan.voltageTolerance}%")

    thread = threading.Thread(target=ExecutableManager.runDeviationCantDetect) # carl
    thread.start()

def subtractVoltageTolerance():
    varMan.voltageTolerance -= 1
    voltageToleranceText.config(text=f"{varMan.voltageTolerance}%")
    ExecutableManager.runDeviationCantDetect()

    thread = threading.Thread(target=ExecutableManager.runDeviationCantDetect) # carl
    thread.start()

def ShowErrorBox():
    showerror(title='Error Status', message='Unable To Read Csv Files Press Ok To Exit')
    stop_prog()

# %%
from ctypes import windll
import tkinter as tk

def showGUI():
    global Engine, prog_run, is_debug, root
    global process_1_csv, proc_1_Mtrl_1_code, proc_1_Mtrl_2_code, proc_1_Mtrl_3_code, proc_1_Mtrl_4_code, proc_1_Mtrl_5_code, proc_1_time_text
    global proc_1_txt, proc_1_stop_btn, proc_1_err_msg, proc_1_err_msg_txt, proc_1_is_wrong_itm, is_read_proc1_csv, proc_1_time_out_of_tolerance
    global proc_2_csv, proc_2_Mtrl_1_code, proc_2_Mtrl_2_code, proc_2_Mtrl_3_code, proc_2_Mtrl_4_code, proc_2_Mtrl_5_code, proc_2_time_text
    global proc_2_txt, proc_2_stop_btn, proc_2_err_msg, proc_2_err_msg_txt, proc_2_is_wrong_itm, is_read_proc2_csv, proc_2_time_out_of_tolerance
    global proc_3_csv, proc_3_Mtrl_1_code, proc_3_Mtrl_2_code, proc_3_Mtrl_3_code, proc_3_Mtrl_4_code, proc_3_Mtrl_5_code, proc_3_time_text
    global proc_3_txt, proc_3_stop_btn, proc_3_err_msg, proc_3_err_msg_txt, proc_3_is_wrong_itm, is_read_proc3_csv, proc_3_time_out_of_tolerance
    global proc_4_csv, proc_4_Mtrl_1_code, proc_4_Mtrl_2_code, proc_4_Mtrl_3_code, proc_4_Mtrl_4_code, proc_4_Mtrl_5_code, proc_4_time_text
    global proc_4_txt, proc_4_stop_btn, proc_4_err_msg, proc_4_err_msg_txt, proc_4_is_wrong_itm, is_read_proc4_csv, proc_4_time_out_of_tolerance
    global proc_5_csv, proc_5_Mtrl_1_code, proc_5_Mtrl_2_code, proc_5_Mtrl_3_code, proc_5_Mtrl_4_code, proc_5_Mtrl_5_code, proc_5_time_text
    global proc_5_txt, proc_5_stop_btn, proc_5_err_msg, proc_5_err_msg_txt, proc_5_is_wrong_itm, is_read_proc5_csv, proc_5_time_out_of_tolerance
    global proc_6_csv, proc_6_Mtrl_1_code, proc_6_Mtrl_2_code, proc_6_Mtrl_3_code, proc_6_Mtrl_4_code, proc_6_Mtrl_5_code, proc_6_time_text
    global proc_6_txt, proc_6_stop_btn, proc_6_err_msg, proc_6_err_msg_txt, proc_6_is_wrong_itm, is_read_proc6_csv, proc_6_time_out_of_tolerance
    global comText
    global is_speaking, is_proc_1_by_pass, is_proc_2_by_pass, is_proc_3_by_pass, is_proc_4_by_pass, is_proc_5_by_pass, is_proc_6_by_pass
    global sound_title, log_count, ser
    global frame1, frame2
    global voltageToleranceText
    
    # Fixing Blur/This line ensures the GUI doesn't appear blurry on high-DPI displays by enabling DPI awareness.
    windll.shcore.SetProcessDpiAwareness(1)



    # Creates the main window titled "Wrong Material Detector".
    # Sets its size and position.
    root = tk.Tk()
    root.title("HPI - QCS")
    root.geometry("2000x850+50+50")
    # root.resizable(False, False)

    frame1 = tk.Frame(root)
    frame1.pack()

    frame2 = tk.Frame(root)
    frame2.pack_forget()

    # Distributes space across three columns evenly.
    frame1.columnconfigure(0, weight=1)
    frame1.columnconfigure(1, weight=1)
    frame1.columnconfigure(2, weight=1)
    frame1.columnconfigure(3, weight=1)

    # Distributes space across three columns evenly.
    frame2.columnconfigure(0, weight=1)
    frame2.columnconfigure(1, weight=1)
    frame2.columnconfigure(2, weight=1)
    frame2.columnconfigure(3, weight=1)

    # place a label on the root window
    comText = tk.Label(frame1, text=f"Com Port: {comPort}", font=("Arial", 12, "bold"), fg="green")
    comText.grid(column=0, row=0)

    showJobOrderMaterialsButton = tk.Button(
        frame1,
        text="MATERIALS",
        font=("Arial", 10),
        command=open_new_window,
        width=10,
        height=1,
    )
    showJobOrderMaterialsButton.grid(column=1, row=0, ipadx=5, ipady=5) # Button to stop process 1
    showJobOrderMaterialsButton.config(bg="lightgreen", fg="black") # Button color and text

    # PROCESS 1
    proc_1_txt = tk.Label(frame1, text="Process 1", font=("Arial", 12, "bold"))
    proc_1_txt.grid(column=0, row=1)
    proc_1_stop_btn = tk.Button(
        frame1,
        text="STOP",
        font=("Arial", 12),
        command=ExecutableManager.stopProcess1,
        width=15,
        height=1,
    )
    proc_1_stop_btn.grid(column=0, row=2, ipadx=5, ipady=5) # Button to stop process 1
    proc_1_stop_btn.config(bg="orange", fg="black") # Button color and text
    proc_1_err_msg = tk.Label(frame1, text=proc_1_err_msg_txt, font=("Arial", 12))
    proc_1_err_msg.grid(column=0, row=3)
    
    #----------------------------------------------------------DISPLAY STOP BUTTON
    # PROCESS 2
    proc_2_txt = tk.Label(frame1, text="Process 2", font=("Arial", 12, "bold"))
    proc_2_txt.grid(column=1, row=1)
    proc_2_stop_btn = tk.Button(
        frame1,
        text="STOP",
        font=("Arial", 12),
        command=ExecutableManager.stopProcess2,
        width=15,
        height=1,
    )
    proc_2_stop_btn.grid(column=1, row=2, ipadx=5, ipady=5)
    proc_2_stop_btn.config(bg="orange", fg="black")
    proc_2_err_msg = tk.Label(frame1, text=proc_2_err_msg_txt, font=("Arial", 12))
    proc_2_err_msg.grid(column=1, row=3)
    #----------------------------------------------------------
    # proc_2_time_text = tk.Text(root, height=3, width=40, font=("Arial", 10))
    # proc_2_time_text.grid(column=1, row=4)
    # proc_2_time_text.config(state="disabled")

    # PROCESS 3
    proc_3_txt = tk.Label(frame1, text="Process 3", font=("Arial", 12, "bold"))
    proc_3_txt.grid(column=0, row=5, pady=(40, 0))
    proc_3_stop_btn = tk.Button(
        frame1,
        text="STOP",
        font=("Arial", 12),
        command=ExecutableManager.stopProcess3,
        width=15,
        height=1,
    )
    proc_3_stop_btn.grid(column=0, row=6, ipadx=5, ipady=5)
    proc_3_stop_btn.config(bg="orange", fg="black")
    proc_3_err_msg = tk.Label(frame1, text=proc_3_err_msg_txt, font=("Arial", 12))
    proc_3_err_msg.grid(column=0, row=7)

    # PROCESS 4
    proc_4_txt = tk.Label(frame1, text="Process 4", font=("Arial", 12, "bold"))
    proc_4_txt.grid(column=1, row=5, pady=(40, 0))
    proc_4_stop_btn = tk.Button(
        frame1,
        text="STOP",
        font=("Arial", 12),
        command=ExecutableManager.stopProcess4,
        width=15,
        height=1,
    )
    proc_4_stop_btn.grid(column=1, row=6, ipadx=5, ipady=5)
    proc_4_stop_btn.config(bg="orange", fg="black")
    proc_4_err_msg = tk.Label(frame1, text=proc_4_err_msg_txt, font=("Arial", 12))
    proc_4_err_msg.grid(column=1, row=7)

    # PROCESS 5
    proc_5_txt = tk.Label(frame1, text="Process 5", font=("Arial", 12, "bold"))
    proc_5_txt.grid(column=0, row=8, pady=(40, 0))
    proc_5_stop_btn = tk.Button(
        frame1,
        text="STOP",
        font=("Arial", 12),
        command=ExecutableManager.stopProcess5,
        width=15,
        height=1,
    )
    proc_5_stop_btn.grid(column=0, row=9, ipadx=5, ipady=5)
    proc_5_stop_btn.config(bg="orange", fg="black")
    proc_5_err_msg = tk.Label(frame1, text=proc_5_err_msg_txt, font=("Arial", 12))
    proc_5_err_msg.grid(column=0, row=10)
    

    # PROCESS 6
    proc_6_txt = tk.Label(frame1, text="Process 6", font=("Arial", 12, "bold"))
    proc_6_txt.grid(column=1, row=8, pady=(40, 0))
    proc_6_stop_btn = tk.Button(
        frame1,
        text="STOP",
        font=("Arial", 12),
        command=ExecutableManager.stopProcess6,
        width=15,
        height=1,
    )
    proc_6_stop_btn.grid(column=1, row=9, ipadx=5, ipady=5)
    proc_6_stop_btn.config(bg="orange", fg="black")
    proc_6_err_msg = tk.Label(frame1, text=proc_6_err_msg_txt, font=("Arial", 12))
    proc_6_err_msg.grid(column=1, row=10)

    

    # LOG BOX
    varMan.materialLogWindow = tk.Text(frame1, height=10, width=80, font=("Arial", 14))
    varMan.materialLogWindow.grid(column=0, row=11, columnspan=3)
    varMan.materialLogWindow.config(state="disabled")
    varMan.materialLogWindow.tag_configure("red", foreground="red")

    materialLogWindowClearButton = tk.Button(
        frame1,
        text="CLEAR",
        font=("Arial", 10),
        command=ClearMaterialLogWindow,
        width=10,
        height=1,
    )
    materialLogWindowClearButton.grid(column=0, row=12, ipadx=5, ipady=5) # Button to stop process 1
    materialLogWindowClearButton.config(bg="gray", fg="black") # Button color and text

    nextWindowButton = tk.Button(
        frame1,
        text="NEXT",
        font=("Arial", 10),
        command=nextWindow,
        width=10,
        height=1,
    )
    nextWindowButton.grid(column=3, row=0, ipadx=5, ipady=5)
    nextWindowButton.config(bg="lightgreen", fg="black")

    #FRAME 2_____________________________________________________________________________________

    nextWindowButton = tk.Button(
        frame2,
        text="BACK",
        font=("Arial", 10),
        command=backWindow,
        width=10,
        height=1,
    )
    nextWindowButton.grid(column=0, row=0, ipadx=5, ipady=5)
    nextWindowButton.config(bg="lightgreen", fg="black")

    # TEXT (DeviationChecker)
    varMan.deviation_txt = tk.Label(frame2, text="DeviationChecker", font=("Arial", 12, "bold"))
    varMan.deviation_txt.grid(column=0, row=1)

    # STOP BUTTON
    varMan.deviation_stop_btn = tk.Button(
        frame2,
        text="STOP",
        font=("Arial", 12),
        command=ExecutableManager.stopDeviation,
        width=15,
        height=1,
    )
    varMan.deviation_stop_btn.grid(column=0, row=2, ipadx=5, ipady=5)
    varMan.deviation_stop_btn.config(bg="orange", fg="black")

    # LOADING MESSAGE
    varMan.deviation_err_msg = tk.Label(frame2, text=varMan.deviation_err_msg_text, font=("Arial", 12))
    varMan.deviation_err_msg.grid(column=0, row=3)



    # - BUTTON
    minusButton = tk.Button(
        frame2,
        text="-",
        font=("Arial", 12),
        command=subtractVoltageTolerance,
        width=2,
        height=1,
    )
    minusButton.grid(column=0, row=4, padx=(0, 70))
    minusButton.config(bg="orange", fg="black")

    # TEXT (DeviationChecker)
    voltageToleranceText = tk.Label(frame2, text=f"{varMan.voltageTolerance}%", font=("Arial", 12, "bold"))
    voltageToleranceText.grid(column=0, row=4)
    
    # + BUTTON
    plusButton = tk.Button(
        frame2,
        text="+",
        font=("Arial", 12),
        command=addVoltageTolerance,
        width=2,
        height=1,
    )
    plusButton.grid(column=0, row=4, padx=(70, 0))
    plusButton.config(bg="orange", fg="black")


    #  !------------------------------------THREADS SECTION------------------------------------!
    ExecutableManager.runDeviationCantDetect()

    processDetector = threading.Thread(target=ExecutableManager.runProcessDetectionManager) # carl
    processDetector.start()   # 

    buttonController = threading.Thread(target=ExecutableManager.runButtonController) # carl
    buttonController.start()   # 

    buzzerController = threading.Thread(target=ExecutableManager.runBuzzerController) # carl
    buzzerController.start()   # 


    #  !------------------------------------THREADS SECTION------------------------------------!

    root.protocol("WM_DELETE_WINDOW", stop_prog)
    root.mainloop()
