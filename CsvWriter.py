#%%
from Imports import *



#Write Csv File
def WriteCsv(excelData):
    if os.path.exists(f"JoReference.csv"):
        print("Overiting The Existing File")
        #Read Existed
        existedExcel = pd.read_csv(f"JoReference.csv")
        df = pd.concat([existedExcel, pd.DataFrame(excelData, index=[0])], axis = 0, ignore_index = True)
        df.to_csv(f"JoReference.csv", index = False)
    else:
        print("Creating New File")
        # Create Excel File
        df = pd.concat([excelData], axis = 0, ignore_index = True)
        df.to_csv(f"JoReference.csv", index = False)
        
# %%
