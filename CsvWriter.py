from Imports import *
import DateAndTimeManager
# %%
#Write Csv File
def WriteCsv(excelData):
    # fileDirectory = (r'\\192.168.2.19\ai_team\AI Program\Outputs')
    # os.chdir(fileDirectory)
    # print(os.getcwd())

    if os.path.exists(f"DeviationResults.csv"):
        print("Overiting The Existing File")
        #Read Existed
        existedExcel = pd.read_csv(f"DeviationResults.csv")
        df = pd.concat([existedExcel, pd.DataFrame(excelData, index=[0])], axis = 0, ignore_index = True)
        df.to_csv(f"DeviationResults.csv", index = False)
        df.to_csv(fr"\\192.168.2.19\general\INSPECTION-MACHINE\FC1\DeviationResults.csv", index = False)
    else:
        print("Creating New File")
        #Create Excel File
        df = pd.concat([excelData], axis = 0, ignore_index = True)
        df.to_csv(f"DeviationResults.csv", index = False)
        df.to_csv(fr"\\192.168.2.19\general\INSPECTION-MACHINE\FC1\DeviationResults.csv", index = False)