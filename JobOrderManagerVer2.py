# %%
from Imports import *

read_job_order = None
job_order_materials = None
jobOrderDate = None
jobOrderTime = None

def check_job_orders():
    global read_job_order
    global jobOrderDate
    global jobOrderTime

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    data_frames = pd.read_csv(fr"\\192.168.2.10\csv\csv\JobOrder\log000_JobOrder.csv", encoding='latin1')

    data_frames = data_frames.tail(1)

    read_job_order = data_frames["Job Order Number"].values[0].replace("\t", "").replace(" ", "").replace("-", "")
    jobOrderDate = data_frames["DATE"].values[0]
    jobOrderTime = data_frames["TIME"].values[0]

def find_materials():
    global job_order_materials
    global read_job_order
    global jobOrderDf

    current_year = datetime.datetime.now().year

    
    folder_name_current_with_dollar = f"{current_year}$"
    folder_name_current_without_dollar = f"{current_year}"

    
    file_path_current_with_dollar = fr'\\192.168.2.19\production\{folder_name_current_with_dollar}\1. Document for Production Admin\8. JOB ORDER MATERIAL LIST\{read_job_order}.xlsx'

    
    if os.path.exists(file_path_current_with_dollar):
        try:
            job_order_materials = pd.read_excel(file_path_current_with_dollar)
            jobOrderDf = pd.read_excel(file_path_current_with_dollar)
            if "Material" in job_order_materials.columns:
                job_order_materials = job_order_materials["Material"]
            else:
                print(f"'Material' column not found in the file: {file_path_current_with_dollar}")
        except Exception as e:
            print(f"Error reading file in current year with dollar sign: {e}")
    else:
        
        file_path_current_without_dollar = fr'\\192.168.2.19\production\{folder_name_current_without_dollar}\1. Document for Production Admin\8. JOB ORDER MATERIAL LIST\{read_job_order}.xlsx'
        if os.path.exists(file_path_current_without_dollar):
            try:
                job_order_materials = pd.read_excel(file_path_current_without_dollar)
                jobOrderDf = pd.read_excel(file_path_current_without_dollar)
                if "Material" in job_order_materials.columns:
                    job_order_materials = job_order_materials["Material"]
                else:
                    print(f"'Material' column not found in the file: {file_path_current_without_dollar}")
            except Exception as e:
                print(f"Error reading file in current year without dollar sign: {e}")
        else:
            
            previous_year = current_year - 1
            folder_name_prev_with_dollar = f"{previous_year}$"
            folder_name_prev_without_dollar = f"{previous_year}"

            
            file_path_prev_with_dollar = fr'\\192.168.2.19\{folder_name_prev_with_dollar}\1. Document for Production Admin\8. JOB ORDER MATERIAL LIST\{read_job_order}.xlsx'
            if os.path.exists(file_path_prev_with_dollar):
                try:
                    job_order_materials = pd.read_excel(file_path_prev_with_dollar)
                    jobOrderDf = pd.read_excel(file_path_prev_with_dollar)
                    if "Material" in job_order_materials.columns:
                        job_order_materials = job_order_materials["Material"]
                    else:
                        print(f"'Material' column not found in the file: {file_path_prev_with_dollar}")
                except Exception as e:
                    print(f"Error reading file in previous year with dollar sign: {e}")
            else:
                
                file_path_prev_without_dollar = fr'\\192.168.2.19\{folder_name_prev_without_dollar}\1. Document for Production Admin\8. JOB ORDER MATERIAL LIST\{read_job_order}.xlsx'
                if os.path.exists(file_path_prev_without_dollar):
                    try:
                        job_order_materials = pd.read_excel(file_path_prev_without_dollar)
                        jobOrderDf = pd.read_excel(file_path_prev_without_dollar)
                        if "Material" in job_order_materials.columns:
                            job_order_materials = job_order_materials["Material"]
                        else:
                            print(f"'Material' column not found in the file: {file_path_prev_without_dollar}")
                    except Exception as e:
                        print(f"Error reading file in previous year without dollar sign: {e}")
                else:
                    print(f"File not found: {file_path_current_with_dollar}, {file_path_current_without_dollar}, {file_path_prev_with_dollar}, and {file_path_prev_without_dollar}")

# check_job_orders()
# find_materials()

#EM2P
# expectedData = jobOrderDf[jobOrderDf['Material Description'].str.lower().str.contains("2p", na=False)]
# expectedData

# expectedData = jobOrderDf[jobOrderDf['Material Description'].str.lower().str.contains("3p", na=False)]
# expectedData

# expectedData = jobOrderDf[jobOrderDf['Material Description'].str.lower().str.contains("harness", na=False)]
# expectedData

# expectedData = jobOrderDf[jobOrderDf['Material Description'].str.lower().str.contains("frame", na=False)]
# expectedData = expectedData[expectedData['Material'].str.lower().str.contains("fm", na=False)]
# expectedData

# expectedData = jobOrderDf[jobOrderDf['Material Description'].str.lower().str.contains("bushing", na=False)]
# expectedData = expectedData["Material"].values

# for a in expectedData:
#     print(a)

# expectedData = jobOrderDf[jobOrderDf['Material Description'].str.lower().str.contains("vinyl", na=False)]
# expectedData = expectedData[expectedData['Material'].str.lower().str.contains("csb", na=False)]
# expectedData = expectedData["Material"].values
#%%