#
# -*- coding: utf-8  -*-
#=================================================================
# Created by: Jieming Ye
# Created on: Feb 2024
# Last Modified: Feb 2024
#=================================================================
"""
Pre-requisite: 

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
#=================================================================
# Set Information Variable
# N/A
#=================================================================

import pandas as pd

from vision_oslo_extension.shared_contents import SharedMethods


def main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):

    #User Interface - Welcome message:
    print("Common Interface File (CIF) Processor")
    print("")
    print("Copyright: Engineering Services 2024")
    print("")

    filename = text_input
    if not SharedMethods.check_existing_file(filename):
        return False

    # user input selection
    # 1: Output to readable format.
    # 2: Filter out Diesel Services
    # 3: Filter out services by TIPLOC
    # 

    option = option_select

    if option not in ["1","2","3"]:
        print("ERROR: Error in cif_prepare.py. Consult Support....")
        return False
    
    if option == "1":
        readable_format(filename)

    if option == "2":
        cif_remove_process(filename)

                   
    return True

# Action on the CIF based on the Header selection
def cif_data_action(line,header_record,train_info,timetable_info,change_info,TIPLOC_lookup,train_id):
    if header_record == "HD":
        #print(line.rstrip()) # remove training space
        return

    if header_record == "TI": # TIPLOC insert record
        return
    
    if header_record == "TA":  # TIPLOC amend record
        return

    if header_record == "TD": # TIPLOC delete record
        return
    
    if header_record == "AA": # Assocated records
        return
    
    if header_record == "BS": #  Basic schedule record
        
        info1 = (line[2:3].strip() or None)   # Transaction Type
        info2 = (line[3:9].strip() or None)   # Train UID
        info3 = (line[9:15].strip() or None)   # Dates run from
        info4 = (line[15:21].strip() or None)   # Dates run to
        info5 = (line[21:22].strip() or None)   # Monday
        info6 = (line[22:23].strip() or None)   # Tuesday
        info7 = (line[23:24].strip() or None)   # Wednesday
        info8 = (line[24:25].strip() or None)   # Thursday
        info9 = (line[25:26].strip() or None)   # Friday
        info10 = (line[26:27].strip() or None)   # Saturday
        info11 = (line[27:28].strip() or None)   # Sunday
        info12 = (line[28:29].strip() or None)   # Bank Holiday
        info13 = (line[29:30].strip() or None)   # Train Status
        info14 = (line[30:32].strip() or None)   # Train Category
        info15 = (line[32:36].strip() or None)   # Train Identity
        info16 = (line[36:40].strip() or None)   # Headcode
        info17 = (line[40:41].strip() or None)   # Course Indicator
        info18 = (line[41:49].strip() or None)   # Train service code
        info19 = (line[49:50].strip() or None)   # Business Sector
        info20 = (line[50:53].strip() or None)   # Power Type
        info21 = (line[53:57].strip() or None)   # Timing Load
        info22 = (line[57:60].strip() or None)   # Speed
        info23 = (line[60:66].strip() or None)   # Operating Chars
        info24 = (line[66:67].strip() or None)   # Train Class
        info25 = (line[67:68].strip() or None)   # Sleepers
        info26 = (line[68:69].strip() or None)   # Reservations
        info27 = (line[69:70].strip() or None)   # Connect Indicator
        info28 = (line[70:74].strip() or None)   # Catering Code
        info29 = (line[74:78].strip() or None)   # Service Branding
        info30 = (line[78:79].strip() or None)   # Spare
        info31 = (line[79:80].strip() or None)   # STP Indicator
        train_info.append([train_id,info1,info2,info3,info4,info5,info6,info7,info8, \
                           info9,info10,info11,info12,info13,info14,info15,info16,info17,info18, \
                           info19,info20,info21,info22,info23,info24,info25,info26,info27,info28, \
                           info29,info30,info31])
        #print(train_info[train_id-1])
        
        return
    
    if header_record == "BX":
        info1 = (line[6:11].strip() or None)  # UIC code
        info2 = (line[11:13].strip() or None)  # ATOC Code
        info3 = (line[13:14].strip() or None)  # Applicable Tiemtable Code
        info4 = (line[14:22].strip() or None)  # Retail Service ID
        train_info[train_id-1] += [info1,info2,info3,info4,0,0,0]
        #print(train_info[train_id-1])
        
        return
    
    if header_record == "LO":
        info1 = (line[2:9].strip() or None)  # TIPLOC Location        
        train_info[train_id-1][37] = TIPLOC_lookup.get(info1,info1) # origin
        
        hour = line[10:12].strip()
        minute = line[12:14].strip()
        if line[14:15].strip() == "H":
            sec = "30"
        else:
            sec = "00"

        info2 = None  # Arrival Time
        info3 = hour+":"+minute+":"+sec  # Scheduled depature time
        info4 = info3 # Time
        info5 = (line[19:22].strip() or None) # Platform
        info6 = (line[22:25].strip() or None) # Line
        info7 = None # Path
        info8 = (line[29:41].strip() or None)  # Activity
        info9 = (line[25:27].strip() or None)  # Engineering Allowance
        info10 = (line[27:29].strip() or None)  # Pathing Allowance
        info11 = (line[41:43].strip() or None)  # Performance Allowance

        timetable_info.append([train_id,info1,TIPLOC_lookup.get(info1,info1),info2, \
                               info3,info4,info5,info6,info7,info8,info9,info10,info11])
        return
    
    if header_record == "LI":
        
        info1 = (line[2:9].strip() or None)  # TIPLOC Location

        if line[15:19].strip() == "":
            info2 = None  # Arrival Time
            
            hour = line[20:22].strip()
            minute = line[22:24].strip()
            if line[24:25].strip() == "H":
                sec = "30"
            else:
                sec = "00"
            info3 = hour+":"+minute+":"+sec  # Scheduled Passing Time
        else:   
            hour = line[10:12].strip()
            minute = line[12:14].strip()
            if line[14:15].strip() == "H":
                sec = "30"
            else:
                sec = "00"
            info2 = hour+":"+minute+":"+sec  # Scheduled Arrival Time

            hour = line[15:17].strip()
            minute = line[17:19].strip()
            if line[19:20].strip() == "H":
                sec = "30"
            else:
                sec = "00"
            info3 = hour+":"+minute+":"+sec  # Scheduled Depature Time
                 
        info4 = info3 # Time
        info5 = (line[33:36].strip() or None)  # Platform
        info6 = (line[36:39].strip() or None)  # Line
        info7 = (line[39:42].strip() or None)  # Path
        info8 = (line[42:54].strip() or None)  # Activity
        info9 = (line[54:56].strip() or None)  # Engineering Allowance
        info10 = (line[56:58].strip() or None)  # Pathing Allowance
        info11 = (line[58:60].strip() or None)  # Performance Allowance

        timetable_info.append([train_id,info1,TIPLOC_lookup.get(info1,info1),info2, \
                               info3,info4,info5,info6,info7,info8,info9,info10,info11])
        return
    
    if header_record == "CR":
        change_no = train_info[train_id-1][36] + 1
        info1 = (line[2:9].strip() or None)   # Location
        info2 = (line[10:12].strip() or None)   # Train Category
        info3 = (line[12:16].strip() or None)   # Train Identity
        info4 = (line[16:20].strip() or None)   # Headcode
        info5 = (line[20:21].strip() or None)   # Course Indicator 
        info6 = (line[21:29].strip() or None)   # Train service code
        info7 = (line[29:30].strip() or None)   # Business Sector
        info8 = (line[30:33].strip() or None)   # Power Type
        info9 = (line[33:37].strip() or None)   # Timing Load
        info10 = (line[37:40].strip() or None)   # Speed
        info11 = (line[40:46].strip() or None)   # Operating Chars
        info12 = (line[46:47].strip() or None)   # Train Class
        info13 = (line[47:48].strip() or None)   # Sleepers
        info14 = (line[48:49].strip() or None)   # Reservations
        info15 = (line[49:50].strip() or None)   # Connect Indicator
        info16 = (line[50:54].strip() or None)   # Catering Code
        info17 = (line[54:58].strip() or None)   # Service Branding
        info18 = (line[58:62].strip() or None)   # Traction Class
        info19 = (line[62:67].strip() or None)   # UIC Code
        info20 = (line[67:75].strip() or None)   # Retailer Service ID
        change_info.append([train_id,info1,TIPLOC_lookup.get(info1,info1),info2,info3,info4, \
                            info5,info6,info7,info8,info9,info10,info11,info12,info13,info14, \
                            info15,info16,info17,info18,info19,info20])
        
        train_info[train_id-1][36] = change_no
        train_info[train_id-1] += [TIPLOC_lookup.get(info1,info1),info8]
        return
    
    if header_record == "LT":
        info1 = (line[2:9].strip() or None)  # TIPLOC Location
        train_info[train_id-1][38] = TIPLOC_lookup.get(info1,info1) # Destination

        hour = line[10:12].strip()
        minute = line[12:14].strip()
        if line[14:15].strip() == "H":
            sec = "30"
        else:
            sec = "00"

        info2 = hour+":"+minute+":"+sec  # Scheduled Arrival Time
        info3 = None  # Scheduled depature time
        info4 = info2 # Time
        info5 = (line[19:22].strip() or None) # Platform
        info6 = None # Line
        info7 = (line[22:25].strip() or None) # Path
        info8 = (line[25:37].strip() or None) # Activiey
        info9 = None # Engineering Allowance
        info10 = None # Pathing Allowance
        info11 = None # Peformance Allowance

        timetable_info.append([train_id,info1,TIPLOC_lookup.get(info1,info1),info2, \
                               info3,info4,info5,info6,info7,info8,info9,info10,info11])
        return
    
    if header_record == "ZZ":
        print("CIF file reading completed")
        return
    
    
    if header_record == "":
        return

# output data in excel
def readable_format(filename):
    #define essential variables
    header_record = ""   # Line ID
    train_id = 0   # Train ID

    # define essential list to be updated
    train_info = [] # train basic information
    timetable_info = []
    change_info = []

    TIPLOC_lookup = SharedMethods.get_tiploc_library()

    # open text file to get the total line information (best way i can think of)
    # although it require reading the file twice
    print("Analysing CIF file....")
    with open(filename) as fp:
        total_line = sum(1 for line in enumerate(fp))

    print("Extracting information from CIF file....")
    print("")
    # open CIF file
    with open(filename) as fp:

        for index, line in enumerate(fp):
            # Get Header Info
            header_record = line[:2].strip()    # Get the Header Code
            if header_record == "BS":
                train_id = train_id + 1

            # excute action
            cif_data_action(line,header_record,train_info,timetable_info,change_info,TIPLOC_lookup,train_id)

            # print processing information
            if index  % (round(0.01*total_line)) == 0:
                finish_mark = int(index / (round(0.01*total_line))*1)
                print("{} % completed.".format(finish_mark))

    # Find the maximum length of the nested lists
    max_length = max(len(x) for x in train_info)

    columns = ['Train_ID','Type','UID','Date_Runs_from','Date_Runs_to', \
               'Mon','Tue','Wed','Thr','Fri','Sat','Sun','BH','Status', \
               'Category','Identity','Headcode','Course_Indicator','Service_Code', \
               'Business_Sector','Power_Type','Timing_Load','Speed','Operating_Code', \
               'Seating_Class','Sleepers','Resevations','Connection','Catering_Code', \
               'Service_Branding','Spare','STP_Indicator','UIC_Code','ATOC_Code', \
               'Applicable_Code','Retail_Service_ID','Info_Change','Origin','Destination']
    add = max_length - len(columns)
    for i in range(1, int(add/2)+1):
        columns.append(f'Location{i}')
        columns.append(f'Power_Type{i}')
    
    # Convert nested list to DataFrame
    df_sum = pd.DataFrame(train_info, columns=columns)

    columns = ['Train_ID','TIPLOC','Location', \
               'Category','Identity','Headcode','Course_Indicator','Service_Code', \
               'Business_Sector','Power_Type','Timing_Load','Speed','Operating_Code', \
               'Seating_Class','Sleepers','Resevations','Connection','Catering_Code', \
               'Service_Branding','Traction_Class','UIC_Code','Retail_Service_ID']
    
    df_change = pd.DataFrame(change_info, columns=columns)

    columns = ['Train_ID','TIPLOC','Location','Arrival Time','Depature/Passing Time', \
               'Time(A/D)','Platform','Line','Path','Activity','Engineering Allowance', \
               'Pathing Allowance','Performance Allowance'] 
    df_timetable = pd.DataFrame(timetable_info, columns=columns)

    # checking CIF information
    df_list = information_list(df_sum,df_timetable,TIPLOC_lookup)

    # Write DataFrame to Excel
    # write data to excel / overwrite the existing one

    print("Saving train summary information to csv...")
    csv_file = filename + '_CIF_Summary.csv'
    # Write DataFrame to CSV
    df_list.to_csv(csv_file, index=False)

    print("Saving train summary information to csv...")
    csv_file = filename + '_CIF_Detail.csv'
    # Write DataFrame to CSV
    df_sum.to_csv(csv_file, index=False)

    print("Saving train changeEnroute information to csv...")
    csv_file = filename + '_CIF_ChangeEnRoute.csv'
    # Write DataFrame to CSV
    df_change.to_csv(csv_file, index=False)
    
    print("Saving train timetable information to csv...")
    csv_file = filename + '_CIF_Timetable.csv'
    # Write DataFrame to CSV
    df_timetable.to_csv(csv_file, index=False)

    return True

# generate unique list
def information_list(df_sum,df_timetable,TIPLOC_lookup):
    # get teh unique list
    tiploc_list = sorted(df_timetable['TIPLOC'].unique())
    # Create a dictionary to store the location information
    loc_list = []
    for tiploc in tiploc_list:
        loc_list.append(TIPLOC_lookup.get(tiploc, tiploc))
    toc_list = sorted(df_sum['ATOC_Code'].unique())
    dep_list = sorted(df_sum['Origin'].unique())
    des_list = sorted(df_sum['Destination'].unique())

    # Determine the length of the longest list
    max_length = max(len(tiploc_list), len(loc_list), len(toc_list), len(dep_list), len(des_list))

    # Create a dictionary to store the lists
    data = {
        'TIPLOC_all': tiploc_list + [None] * (max_length - len(tiploc_list)),
        'Location_all': loc_list + [None] * (max_length - len(loc_list)),
        'ATOC_Code_all': toc_list + [None] * (max_length - len(toc_list)),
        'Origin_all': dep_list + [None] * (max_length - len(dep_list)),
        'Destination_all': des_list + [None] * (max_length - len(des_list))
    }

    # Create a new DataFrame from the dictionary
    new_df = pd.DataFrame(data)

    return new_df

    # excel_file = filename + '_CIF_Detail.xlsx'
    # with pd.ExcelWriter(excel_file, engine='openpyxl', mode='w') as writer:
    #     print("Saving train summary information to excel...(This takes time...)")
    #     df_sum = df_sum.astype(str)
    #     df_sum.to_excel(writer, sheet_name="Summary", index=False)
    #     print("Saving train change information to excel...")
    #     df_change = df_change.astype(str)
    #     df_change.to_excel(writer, sheet_name="ChangeInfo", index=False)

    #     print("Excel Saving.....(This takes time if your timetable is big)")

    # with pd.ExcelWriter(excel_file, engine='openpyxl', mode='w') as writer:
    #     print("Saving train timetable information to excel...")
    #     df_timetable = df_timetable.astype(str)
    #     df_timetable.to_excel(writer, sheet_name="Timetable", index=False)

    #     print("Excel Saving.....(This takes a while if your timetable is big)")
    
# remove diesel services   
def cif_remove_process(filename):
    
    # find the new file name
    i = 1
    while True:
        filename_new = f'{filename}_{i}_.cif'
        if not SharedMethods.check_existing_file(filename_new):
            print("Ignore the ERROR message above as it is allowed.")
            break
        else:
            i = i + 1  
    
    # open text file to get the total line information (best way i can think of)
    # although it require reading the file twice
    print("Analysing CIF file....")
    with open(filename) as fp:
        total_line = sum(1 for line in enumerate(fp))

    print("Selecting information from CIF file....")
    print("")
    # open CIF file
    train_id = 0
    flag = False
    flagCR = False
    flagselect = True
    lines_to_read = []
    with open(filename, 'r') as fp, open(filename_new, 'w') as fp2:

        for index, line in enumerate(fp):
            header_record = line[:2].strip()    # Get the Header Code
            
            if header_record == "HD": # write down first line
                fp2.write(line)

            if header_record == "BS":
                flag = True
                cif_remove_diesel(fp2,lines_to_read,flagselect,flagCR) # process last train
                         
                power = line[50:53].strip()   # Power Type 
                if power in ["D","DEM","DMU","ED"]: # refresh the flag for new train
                    flagselect = False
                else:
                    flagselect = True
                
                flagCR = False # refresh the flag for new train

                lines_to_read = []
                train_id = train_id + 1
            
            if header_record == "CR": # if there is information change en route.
                flagCR = True
            
            if flag == True:
                lines_to_read.append(line)

            # print processing information
            if index  % (round(0.01*total_line)) == 0:
                finish_mark = int(index / (round(0.01*total_line))*1)
                print("{} % completed.".format(finish_mark))

    return

# each train jounery decision - Remove of Diesel services: Split Train when there is a mode change enroute
def cif_remove_diesel(fp2,lines_to_read,flagselect,flagCR):

    if lines_to_read == []:
        return
    
    if flagCR == False: # if there is no change en route
        if flagselect == False: # if it starts with Diesel
            return
        else: # if it starts with electric
            for line in lines_to_read:
                fp2.write(line)
    
    else: # if there is a change en route
        new_lines = []
        mode = False # mode now, False if Diesel
        mode_change = False # power mode change at CR record
        preCR = False # if the previous line is CR record
        header = lines_to_read[0][:30] # first 30 charater: properties of trains
        add = None # addtional BX information
        crline = None # CR Line Info

        for line in lines_to_read:
            header_record = line[:2].strip()
            
            if header_record == "BS":
                if flagselect == True: # if it starts with electric
                    mode = True
                    new_lines.append(line)
                continue

            if header_record == "BX":
                add = line
                if mode == True:
                    new_lines.append(line)
                continue

            if header_record == "LO":
                if mode == True:
                    new_lines.append(line)
                continue

            if header_record == "LI":
                if preCR == False: # if the reprevious line is not CR
                    if mode == True: # if is is still electric
                        new_lines.append(line)
                else:
                    if mode == True: # if it is electric
                        if mode_change == True: # and also if it changes from d to e
                            # start a new train
                            templine = header + crline + '\n'
                            new_lines.append(templine)
                            if add is not None:
                                new_lines.append(add)
                            templine = "LO" + line[2:19] + "          TB                                                 \n"
                            new_lines.append(templine)
                            # reset flag
                            mode_change = False
                            preCR= False
                    else: # if it is disel now
                        if mode_change == True: # and also if it changes from e to d
                            # finish the line
                            templine = "LT" + line[2:19] + "      TF                                                     \n"
                            new_lines.append(templine)
                            # reset flag
                            mode_change = False
                            preCR= False
                continue

            if header_record == "CR":
                preCR = True
                power = line[30:33].strip()
                if power in ["D","DEM","DMU","ED"]:
                    if mode == True: # if the previous is e and now d
                        mode_change = True
                        crline = line[10:60]
                    mode = False
                else:
                    if mode == False: # if the previous is d and now e
                        mode_change = True
                        crline = line[10:60]
                    mode = True
                continue
        
        # write to file
        for line in new_lines:
            fp2.write(line)                
    return

# programme running
if __name__ == "__main__":
    # Add your debugging code here
    simname = "StraightLine1"  # Provide a simulation name or adjust as needed
    main_option = "1"  # Adjust as needed
    time_start = "0070000"  # Adjust as needed
    time_end = "0080000"  # Adjust as needed
    option_select = "2"  # Adjust as needed
    text_input = "DEC19 file.cif"  # Adjust as needed
    low_v = None  # Adjust as needed
    high_v = None  # Adjust as needed
    time_step = None  # Adjust as needed

    # Call your main function with the provided parameters
    main(simname, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step)

