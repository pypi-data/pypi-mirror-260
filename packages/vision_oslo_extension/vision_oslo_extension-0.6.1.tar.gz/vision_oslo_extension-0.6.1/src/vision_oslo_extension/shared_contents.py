#
# -*- coding: utf-8  -*-
#=================================================================
# Created by: Jieming Ye
# Created on: Feb 2024
# Last Modified: Feb 2024
#=================================================================
"""
Pre-requisite: 
N/A
Used Input:
Various
Expected Output:
Various
Description:
This script defines two shared classes of default values to be shared among various scripts.
This script also defines a SharedMethods class containing common functions to be used for various scripts such as checking the existence of files, time manipulation, etc. 

"""
#=================================================================
# VERSION CONTROL
# V1.0 (Jieming Ye) - Initial Version
#=================================================================
# Set Information Variable
# N/A
#=================================================================


#import tkinter as tk
import os
import shutil
import importlib.resources
import csv
import time

class SharedVariables:
    # this class will store all shared varibles
    sim_variable = None
    main_option = None
    
    # varible to be updated following version upgrade:
    # Replace 'your_package_name' with the actual name of your package
    package_name = 'vision_oslo_extension'
    support_name = 'support'

    tiploc_name = 'tiploc_library.csv'
    
class Local_Shared:
    # this class will store all local shared varibles
    option_select = None
    time_start = None
    time_end = None
    text_input = None
    low_threshold = None
    high_threshold = None
    time_step = None

class SharedMethods:
    # copy files from source folder to active entry
    def copy_example_files(filename):
        distribution = importlib.resources.files(SharedVariables.package_name)
        # Get the path to the package
        #package_path = distribution.location + "\\" + SharedVariables.package_name
        package_path = os.path.join(str(distribution), SharedVariables.support_name)

        # Get the absolute path of the file in the package location
        file_in_package = os.path.join(package_path, filename)
        current_path = os.getcwd() # get current path

        check_file = os.path.join(current_path, filename)

        if os.path.exists(check_file):
            print(f"File '{filename}' already exists in the current working directory. Skipping copy...")
        else:
            # Copy the file to the current working directory
            shutil.copy(file_in_package,current_path)
            print(f"File '{filename}' copied to the current working directory. Config as required...")

    #check existin file
    def check_existing_file(filename):
        print("Checking File {}...".format(filename))
        current_path = os.getcwd() # get current path
        # print(current)
        file_path = os.path.join(current_path,filename) # join the file path
        # print(file_path)
        if not os.path.isfile(file_path): # if the oof file does not exist
            print("ERROR: Required file {} does not exist. Checking required...".format(filename))
            return False
        return True

    # check the folder and file for summary
    def folder_file_check(subfolder,filename):
        print("Checking File {} in {}...".format(filename,subfolder))
        current_path = os.getcwd() # get current path

        # Create the complete folder path
        folder_path = os.path.join(current_path, subfolder)
        
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print("ERROR: Required folder {} does not exist. Exiting...".format(subfolder))
            return False
        
        # file path
        file_path = os.path.join(folder_path,filename) # join the file path
        # print(file_path)
        if not os.path.isfile(file_path):
            print("ERROR: Required file {} does not exist at {}. Exiting...".format(filename,subfolder))
            return False
        return True

    # check oof file
    def check_oofresult_file(simname):
        # if getattr(sys, 'frozen', False):
        # # PyInstaller creates a temp folder and stores path in _MEIPASS
        #     application_path = sys._MEIPASS
        # else:
        #     # Regular Python execution
        #     application_path = os.path.dirname(os.path.abspath(__file__))

        resultfile = simname + ".oof"
        if not SharedMethods.check_existing_file(resultfile):
            return False

        return True

    # osop running       
    def osop_running(cmdline):
        # package_name = 'vision_oslo_extension'
        # Get the distribution object for your package
        distribution = importlib.resources.files(SharedVariables.package_name)
        # Get the path to the package
        package_path = str(distribution)

        with open("batch_run.bat","w") as fba:
            fba.writelines("@echo off\n")
            fba.writelines("set PATH=%PATH%;" + package_path + "\n")
            fba.writelines("@echo on\n")
            fba.writelines(cmdline)
        os.system("batch_run.bat")

    # rename files
    def file_rename(old_name,new_name):
        try:
            os.rename(old_name,new_name)
            print("File {} successfully created. Processing Continue...".format(new_name))
        except FileExistsError:
            os.remove(new_name)
            os.rename(old_name,new_name)
            print("File {} successfully replaced. Processing Continue...".format(new_name))
        except FileNotFoundError:
            print("\nFile {} FAILED as the OSOP extraction fail. Check Input...".format(new_name))

    # module to check 7 digit user input time
    def time_input_process(time_string,option_back):
        #option_back = 1: return string
        #option_back = 2: return seconds

        if not len(time_string) == 7:
            print("Invalid data input. Press reenter the 7 digit time.")
            return False

        seconds_int = 0        
        day = int(time_string[:1])
        hour = int(time_string[1:3])
        minute = int(time_string[3:5])
        second = int(time_string[5:7])

        if not 0 <= day <= 9:
            print("Invalid Day input. Press reenter the 7 digit time.")
            return False
                
        if 0 <= hour <= 24:
            seconds_int += hour*60*60
        else:
            print("Invalid Hour input. Press reenter the 7 digit time.")
            return False
                
        if 0 <= minute <= 60:
            seconds_int += minute*60
        else:
            print("Invalid Minute input. Press reenter the 7 digit time.")
            return False
                
        if 0 <= second <= 60:
            seconds_int += second
        else:
            print("Invalid Second input. Press reenter the 7 digit time.")
            return False

        if option_back == 1:
            return time_string
        else:
            return seconds_int

    # check the propoer life file of the model
    def check_lst_file(simname):
        cmdline = "osop " + simname
        filename = simname + ".osop.lst"
        opcname = simname + ".opc"

        with open(opcname,"w") as fopc:
            fopc.writelines("LIST INPUT FILE\n")
    
        # Create batch file for list command and run the batch file
        # and define the lst file name to process the information
        # generate List file
        if not os.path.isfile(filename):
            SharedMethods.osop_running(cmdline)
        lst_file_size = os.path.getsize(filename)
        
        if lst_file_size < 10000: # a random size (bytes) to check if lst should be redone (10000 bytes = 10 kb)
            SharedMethods.osop_running(cmdline)
    
    # module to read the text file input    
    def file_read_import(filename,simname):
        
        if not os.path.isfile(filename): # if the file exist
            input("Required input file {} does not exist. Please select another option.".format(filename))

        # reading the train list file
        text_input = []
        with open(filename) as fbrlist:
            for index, line in enumerate(fbrlist):
                text_input.append(line[:50].strip())

        return text_input
    
    # write to text file (not used)
    def file_write(header,creatname,listname):
        with open(creatname, 'w') as fw:
            fw.write(header)
            for items in listname:
                string_line = map(str,items) # string all item
                result_line = ",".join(string_line) # join item removing brackets/quotes
                fw.write("%s\n" % result_line) # print out
    
    # module to convert 7 digits time to time format 
    def time_convert(time_string):
        
        #time_string = input()          
        day = int(time_string[:1])
        hour = int(time_string[1:3])
        minute = int(time_string[3:5])
        second = int(time_string[5:7])

        if not day == 0:
            day = day # to be updated to process info at a later stage
        time = str(hour) + ":" + str(minute) + ":" + str(second)        
        #debug purpose
        #print(seconds_int)
        # Return the second integer number as same used in the list file           
        return time

    # read tiploc information
    def get_tiploc_library():
        tiploc = {} # create a empty tiploc
        
        filename = SharedVariables.tiploc_name
        distribution = importlib.resources.files(SharedVariables.package_name)
        package_path = os.path.join(str(distribution), SharedVariables.support_name)

        # Get the absolute path of the file in the package location
        filepath = os.path.join(package_path, filename)

        last_modified_timestamp = os.path.getmtime(filepath)
        # Convert timestamp to a readable format
        last_time = time.strftime('%Y-%m-%d', time.localtime(last_modified_timestamp))

        print("\nTIPLOC Libray Last Update: {}".format(last_time))
        print("Please contact support if a TIPLOC library update is needed!")

        with open(filepath,'r') as file:
            csv_reader = csv.reader(file)
            # next(csv_reader)  # Skip the first row
            for row in csv_reader:
                key = row[0]
                value = row[1]
                tiploc[key] = value
        
        return tiploc

    # defin the running in thread mechanism    
    def common_thread_run(import_option, sim_name, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step):
        if import_option == "cif_prepare.py":
            from vision_oslo_extension import cif_prepare as fc
        elif import_option == "model_check.py":
            from vision_oslo_extension import model_check as fc
        elif import_option == "oslo_extraction.py":
            from vision_oslo_extension import oslo_extraction as fc
        elif import_option == "post_processing.py":
            from vision_oslo_extension import post_processing as fc
        elif import_option == "average_load.py":
            from vision_oslo_extension import average_load as fc
        elif import_option == "protection_if.py":
            from vision_oslo_extension import protection_if as fc
        elif import_option == "grid_connection.py":
            from vision_oslo_extension import grid_connection as fc
        elif import_option == "ole_processing.py":
            from vision_oslo_extension import ole_processing as fc
        elif import_option == "batch_processing.py":
            from vision_oslo_extension import batch_processing as fc
        elif import_option == "dc_summary.py":
            from vision_oslo_extension import dc_summary as fc
        
        try:    
            continue_process = fc.main(sim_name, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step)
            if not continue_process:
                # Do something if the process should not continue
                print('\033[1;31m') # color control warning message red
                print("ERROR: Process terminated unexpectly. Please Check Error History Above or Contact Support. You can continue use other options...")
                print('\033[1;0m') # color control warning message reset
            else:
                # Do something if the process should continue
                print('\033[1;32m') # color control warning message red
                print("Action Succesfully Completed. Check monitor history above and result files in your folder.")
                print('\033[1;0m') # color control warning message reset
        
        except Exception as e:
            print(f"Error in {import_option}:", e)
