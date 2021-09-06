'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision C, 09/05/2021

Verified working on: Python 2.7 and 3 for Windows 8.1 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

import os, sys, platform
import time, datetime
import inspect #To enable 'TellWhichFileWereIn'
import threading
from copy import deepcopy

###############
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
###############

###############
if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3
###############

###############
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input
############### #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

########################################################
#https://docs.python.org/3/library/smtplib.html
import smtplib #for sending emails
#print(smtplib.__file__) #Print location of module

#https://docs.python.org/3/library/base64.html
import base64 #for sending emails with attachments
#print(base64.__file__) #Print location of module

#import email
#print(email.__file__) #Print location of module
#print(email.__all__) #print all functions within the module

#https://docs.python.org/3/library/email.html
from email.mime.text import MIMEText #for sending emails with attachments
from email.mime.image import MIMEImage #for sending emails with attachments
from email.mime.multipart import MIMEMultipart #for sending emails with attachments
from email.mime.base import MIMEBase #for sending emails with attachments

###############
if sys.version_info[0] < 3:
    from email import Encoders as encoders #for sending emails with attachments
else:
    from email import encoders as encoders #for sending emails with attachments
###############

#import shutil #Only needed if we're copying and/or zipping files
########################################################

import select
import re
import collections
import random
from random import randint
import atexit #This line keeps the console window open so that we can see error messages from a program crash before the console window is closed.
import traceback

class EmailAndSMS_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame
    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict):

        print("#################### EmailAndSMS_ReubenPython2and3Class __init__ starting. ####################")

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = -1
        self.EnableInternal_MyPrint_Flag = 0
        self.GUI_ready_to_be_updated_flag = 0

        ##########################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("The OS platform is: " + self.my_platform)
        ##########################################

        ##########################################
        ##########################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            ##########################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))
            ##########################################

            ##########################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
                self.RootIsOwnedExternallyFlag = 1
            else:
                self.root = None
                self.RootIsOwnedExternallyFlag = 0

            print("RootIsOwnedExternallyFlag = " + str(self.RootIsOwnedExternallyFlag))
            ##########################################

            ##########################################
            if "GUI_RootAfterCallbackInterval_Milliseconds" in self.GUIparametersDict:
                self.GUI_RootAfterCallbackInterval_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_RootAfterCallbackInterval_Milliseconds", self.GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds"], 0.0, 1000.0))
            else:
                self.GUI_RootAfterCallbackInterval_Milliseconds = 30

            print("GUI_RootAfterCallbackInterval_Milliseconds = " + str(self.GUI_RootAfterCallbackInterval_Milliseconds))
            ##########################################

            ##########################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            ##########################################

            ##########################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            ##########################################

            ##########################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("NumberOfPrintLines = " + str(self.NumberOfPrintLines))
            ##########################################

            ##########################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            ##########################################

            ##########################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("GUI_ROW = " + str(self.GUI_ROW))
            ##########################################

            ##########################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("GUI_COLUMN = " + str(self.GUI_COLUMN))
            ##########################################

            ##########################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("GUI_PADX = " + str(self.GUI_PADX))
            ##########################################

            ##########################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("GUI_PADY = " + str(self.GUI_PADY))
            ##########################################

            ##########################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 0.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 0

            print("GUI_ROWSPAN = " + str(self.GUI_ROWSPAN))
            ##########################################

            ##########################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 0

            print("GUI_COLUMNSPAN = " + str(self.GUI_COLUMNSPAN))
            ##########################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("No GUIparametersDict present, setting USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))

        print("GUIparametersDict = " + str(self.GUIparametersDict))
        ##########################################
        ##########################################

        ########################################## IMPORTANT THAT THESE VARIABLES ARE DECLARED/INITIALIZED HERE BEFORE WE TRY TO USE EMAIL/PHONE PARSING FUNCTIONS WITH MYPRINTS
        ##########################################
        self.EmailAddressEntry_DefaultText = "Enter email address"
        self.PhoneNumberEntry_DefaultText = "Enter phone number for SMS texting"

        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        if "EmailSenderAccountUsername" in setup_dict:
            self.EmailSenderAccountUsername = setup_dict["EmailSenderAccountUsername"]
        else:
            self.EmailSenderAccountUsername = "default"

        print("EmailSenderAccountUsername = " + str(self.EmailSenderAccountUsername))
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        if "EmailSenderAccountPassword" in setup_dict:
            self.EmailSenderAccountPassword = setup_dict["EmailSenderAccountPassword"]
        else:
            self.EmailSenderAccountPassword = "default"

        print("EmailSenderAccountPassword = " + str(self.EmailSenderAccountPassword))
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        if "EmailAddress_RecipientList" in setup_dict:
            self.EmailAddress_RecipientList = list()

            EmailAddress_RecipientList_temp = setup_dict["EmailAddress_RecipientList"]

            ##############
            if self.IsInputList(EmailAddress_RecipientList_temp) == 0:
                EmailAddress_RecipientList_temp = list([EmailAddress_RecipientList_temp])
            ##############
            
            ##############
            for EmailAddress in EmailAddress_RecipientList_temp:

                SuccessFlag = self.EmailAddress_AddressErrorCheckerAndRecipientListAppending(str(EmailAddress), 1) #, 1 means to add to the list

                if SuccessFlag == 0:
                    print("EmailAndSMS_ReubenPython2and3Class __init__ error: 'EmailAddress_RecipientList' contains errors.")
                    return
            ##############

        else:
            print("EmailAndSMS_ReubenPython2and3Class __init__ error: setup_dict must contain 'EmailAddress_RecipientList'.")
            return

        print("EmailAddress_RecipientList = " + str(self.EmailAddress_RecipientList))
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        if "PhoneNumber_RecipientList" in setup_dict:
            self.PhoneNumber_RecipientList = list()

            PhoneNumber_RecipientList_temp = setup_dict["PhoneNumber_RecipientList"]

            ##############
            if self.IsInputList(PhoneNumber_RecipientList_temp) == 0:
                PhoneNumber_RecipientList_temp = list([PhoneNumber_RecipientList_temp])
            ##############
            
            ##############
            for PhoneNumber in PhoneNumber_RecipientList_temp:

                SuccessFlag = self.PhoneNumber_NumberErrorCheckerAndRecipientListAppending(str(PhoneNumber), 1) #, 1 means to add to the list

                if SuccessFlag == 0:
                    print("EmailAndSMS_ReubenPython2and3Class __init__ error: 'PhoneNumber_RecipientList' contains errors.")
                    return
            ##############

        else:
            print("EmailAndSMS_ReubenPython2and3Class __init__ error: setup_dict must contain 'PhoneNumber_RecipientList'.")
            return

        print("PhoneNumber_RecipientList = " + str(self.PhoneNumber_RecipientList))
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        if "TxThread_TimeToSleepEachLoop" in setup_dict:
            if self.my_platform == "pi": #Must have at least 0.001 sleep in each loop, or the RaspPi will seize-up!
                self.TxThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("TxThread_TimeToSleepEachLoop", setup_dict["TxThread_TimeToSleepEachLoop"], 0.001, 100000)
            else:
                self.TxThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("TxThread_TimeToSleepEachLoop", setup_dict["TxThread_TimeToSleepEachLoop"], 0.000, 100000)

        else:
            self.TxThread_TimeToSleepEachLoop = 0.030

        print("TxThread_TimeToSleepEachLoop: " + str(self.TxThread_TimeToSleepEachLoop))
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        if "TxMessage_Queue_MaxSize" in setup_dict:
            self.TxMessage_Queue_MaxSize = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("TxMessage_Queue_MaxSize", setup_dict["TxMessage_Queue_MaxSize"], 0.000, 100000))

        else:
            self.TxMessage_Queue_MaxSize = 100

        print("TxMessage_Queue_MaxSize: " + str(self.TxMessage_Queue_MaxSize))
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        if "TestFilesFolderFullPath" in setup_dict:
            self.TestFilesFolderFullPath = str(setup_dict["TestFilesFolderFullPath"])

            '''
            if self.TestFilesFolderFullPath.find("\\") != -1:
                print("EmailAndSMS_ReubenPython2and3Class __init__ error: 'TestFilesFolderFullPath' must not contain '\\' backward-slashes.")
                return

            if self.TestFilesFolderFullPath.find("//") != -1:
                print("EmailAndSMS_ReubenPython2and3Class __init__ error: 'TestFilesFolderFullPath' must not contain '//' double-forward-slashes")
                return

            if self.TestFilesFolderFullPath.find("/") == -1:
                print("EmailAndSMS_ReubenPython2and3Class __init__ error: 'TestFilesFolderFullPath' must be FULL path (should include single-forward-slashes).")
                return
            '''

        else:
            self.TestFilesFolderFullPath = os.getcwd()

        print("TestFilesFolderFullPath = " + str(self.TestFilesFolderFullPath))
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        self.TestEmailNeedsToBeSentFlag = 0
        self.TestSMSNeedsToBeSentFlag = 0
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        self.LoopCounter_CalculatedFromTxThread = 0
        self.CurrentTime_CalculatedFromTxThread = -11111.0
        self.LastTime_CalculatedFromTxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromTxThread = -1
        self.DataStreamingDeltaT_CalculatedFromTxThread = -1
        self.Starting_CalculatedFromTxThread = self.getPreciseSecondsTimeStampString()
        self.TxThread_still_running_flag = 1

        self.EmailToTxQueue = Queue.Queue()
        self.SMStoTxQueue = Queue.Queue()

        self.MostRecentTxMessageDict = dict([("TxMessageCounter", self.LoopCounter_CalculatedFromTxThread),
                                             ("TxMessageTimeSeconds", self.CurrentTime_CalculatedFromTxThread),
                                             ("MessageType", "NULL"),
                                             ("MessageContentsDict", dict())])
        ##########################################
        ##########################################

        print("#################### EmailAndSMS_ReubenPython2and3Class __init__ ended input-parameter parsing and variable initialization. ####################")

        ##########################################
        ##########################################
        self.TxThread_ThreadingObject = threading.Thread(target=self.TxThread, args=())
        self.TxThread_ThreadingObject.start()
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        if self.USE_GUI_FLAG == 1:
            self.StartGUI(self.root)
        ##########################################
        ##########################################

        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __del__(self):
        dummy_var = 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getTimeStampString(self):

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('date-%m-%d-%Y---time-%H-%M-%S')

        return st
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, input, print_result_flag = 0):

        result = isinstance(input, list)

        if print_result_flag == 1:
            print("IsInputList: " + str(result))

        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers=4, number_of_decimal_places=3):
        #print("ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput input: " + str(input))

        if type(input) == "str":
            return "-1111111111"

        IsListFlag = self.IsInputList(input)

        if IsListFlag == 0:
            float_number_list = [input]
        else:
            float_number_list = list(input)

        float_number_list_as_strings = []
        for element in float_number_list:
            try:
                element = float(element)
                prefix_string = "{:." + str(number_of_decimal_places) + "f}"
                element_as_string = prefix_string.format(element)
                float_number_list_as_strings.append(element_as_string)
            except:
                print(self.TellWhichFileWereIn() + ": ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput ERROR: " + str(element) + " cannot be turned into a float")
                return "-1111111111"

        StringToReturn = ""
        if IsListFlag == 0:
            StringToReturn = float_number_list_as_strings[0].zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
        else:
            StringToReturn = "["
            for index, StringElement in enumerate(float_number_list_as_strings):
                if float_number_list[index] >= 0:
                    StringElement = "+" + StringElement  # So that our strings always have either + or - signs to maintain the same string length

                StringElement = StringElement.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place

                if index != len(float_number_list_as_strings) - 1:
                    StringToReturn = StringToReturn + StringElement + ", "
                else:
                    StringToReturn = StringToReturn + StringElement + "]"

        return StringToReturn
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentTxMessageDict(self):
        return self.MostRecentTxMessageDict
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def AddEmailToBeSentToAllRecipients(self, EmailToSendDict):

        ####################################################
        if "Subject" not in EmailToSendDict:
            self.MyPrint_WithoutLogFile("SendEmail ERROR: AddEmailToBeSentToAllRecipients, EmailToSendDict must include the key 'Subject'.")
            return 0

        ###### THERE IS NOT REQUIREMENT FOR A 'TO' KEY BECAUSE WE KNOW WE'RE SENDING IT TO EVERYONE ON THE RECIPIENT LIST

        if "Text" not in EmailToSendDict:
            self.MyPrint_WithoutLogFile("SendEmail ERROR: AddEmailToBeSentToAllRecipients, EmailToSendDict must include the key 'Text'.")
            return 0
        ####################################################

        ####################################################
        if self.EmailToTxQueue.qsize() < self.TxMessage_Queue_MaxSize:
            self.EmailToTxQueue.put(EmailToSendDict)
            return 1
        ####################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def AddSMStoBeSentToAllRecipients(self, SMStoSendDict):

        ####################################################
        if "Subject" not in SMStoSendDict:
            self.MyPrint_WithoutLogFile("SendSMS_ToEntireRecipientList ERROR: SMSToSendDict must include the key 'Subject'.")
            return 0

        ###### THERE IS NOT REQUIREMENT FOR A 'TO' KEY BECAUSE WE KNOW WE'RE SENDING IT TO EVERYONE ON THE RECIPIENT LIST

        if "Text" not in SMStoSendDict:
            self.MyPrint_WithoutLogFile("SendSMS_ToEntireRecipientList ERROR: SMSToSendDict must include the key 'Text'.")
            return 0
        ####################################################

        ####################################################
        if self.SMStoTxQueue.qsize() < self.TxMessage_Queue_MaxSize:
            self.SMStoTxQueue.put(SMStoSendDict)
            return 1
        ####################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CalculatedFromTxThread(self):

        try:

            self.DataStreamingDeltaT_CalculatedFromTxThread = self.CurrentTime_CalculatedFromTxThread - self.LastTime_CalculatedFromTxThread

            ##########################
            if self.DataStreamingDeltaT_CalculatedFromTxThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromTxThread = 1.0/self.DataStreamingDeltaT_CalculatedFromTxThread
            ##########################

            self.LastTime_CalculatedFromTxThread = self.CurrentTime_CalculatedFromTxThread

            self.LoopCounter_CalculatedFromTxThread = self.LoopCounter_CalculatedFromTxThread + 1

        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("UpdateFrequencyCalculation_CalculatedFromTxThread ERROR, exceptions: %s" % exceptions)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SendEmail(self, EmailToSendDict):

        ####################################################
        if "Subject" not in EmailToSendDict:
            self.MyPrint_WithoutLogFile("SendEmail ERROR: EmailToSendDict must include the key 'Subject'.")
            return 0

        if "To" not in EmailToSendDict:
            self.MyPrint_WithoutLogFile("SendEmail ERROR: EmailToSendDict must include the key 'To'.")
            return 0
        else:
            if self.EmailAddress_AddressErrorCheckerAndRecipientListAppending(EmailToSendDict["To"], 0) == 0: # ",0" means we're not adding it to our recipient list
                return 0

        if "Text" not in EmailToSendDict:
            self.MyPrint_WithoutLogFile("SendEmail ERROR: EmailToSendDict must include the key 'Text'.")
            return 0
        ####################################################

        ####################################################
        try:
            #print("SendEmail, sending email to " + EmailToSendDict["To"])

            EmailMessage = MIMEMultipart()
            EmailMessage['Subject'] = EmailToSendDict["Subject"]
            EmailMessage['From'] = self.EmailSenderAccountUsername
            EmailMessage['To'] = EmailToSendDict["To"]

            EmailMessage.attach(MIMEText(EmailToSendDict["Text"]))
        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("SendEmail Error: Failed to create the standard email, exceptions: %s" % exceptions)
            return 0
        ####################################################

        #################################################### Attach the TxtFile
        if "TxtFileToAttachFullFilePath" in EmailToSendDict:

            try:
                txt_file = open(EmailToSendDict["TxtFileToAttachFullFilePath"], "r")
                txt_attachment = MIMEText(txt_file.read())

                TxtFileLastSlashIndex = EmailToSendDict["TxtFileToAttachFullFilePath"].rfind("/")
                TxtFilenameWithExtension_NoPath = EmailToSendDict["TxtFileToAttachFullFilePath"][TxtFileLastSlashIndex + 1:]
                #print("TxtFilenameWithExtension_NoPath: " + str(TxtFilenameWithExtension_NoPath))
                txt_attachment.add_header('Content-Disposition', 'attachment', filename=TxtFilenameWithExtension_NoPath)
                
            except:
                exceptions = sys.exc_info()[0]
                self.MyPrint_WithoutLogFile("SendEmail Error: Failed to open TxtFile " + EmailToSendDict["TxtFileToAttachFullFilePath"] + " and convert to MIMEText, exceptions: %s" % exceptions)
                return 0

            try:
                EmailMessage.attach(txt_attachment)
                self.MyPrint_WithoutLogFile("Attached TxtFile " + EmailToSendDict["TxtFileToAttachFullFilePath"])

            except:
                exceptions = sys.exc_info()[0]
                self.MyPrint_WithoutLogFile("SendEmail Error: Failed to attach TxtFile " + EmailToSendDict["TxtFileToAttachFullFilePath"] + " to the email, exceptions: %s" % exceptions)
                return 0
        ####################################################

        #################################################### Attach the Excel/Binary file
        if "ExcelOrBinaryFileToAttachFullFilePath" in EmailToSendDict:
            try:
                excel_binary_attachment = MIMEBase('application', 'octet-stream')
                excel_binary_attachment.set_payload(open(EmailToSendDict["ExcelOrBinaryFileToAttachFullFilePath"], 'rb').read())

                excel_binary_attachment_encoded = excel_binary_attachment
                encoders.encode_base64(excel_binary_attachment_encoded)

                ExcelBinaryFileLastSlashIndex = EmailToSendDict["ExcelOrBinaryFileToAttachFullFilePath"].rfind("/")
                ExcelBinaryFilenameWithExtension_NoPath = EmailToSendDict["ExcelOrBinaryFileToAttachFullFilePath"][ExcelBinaryFileLastSlashIndex + 1:]
                #print("ExcelBinaryFilenameWithExtension_NoPath: " + str(ExcelBinaryFilenameWithExtension_NoPath))
                excel_binary_attachment_encoded.add_header('Content-Disposition', 'attachment', filename=ExcelBinaryFilenameWithExtension_NoPath)
                
            except:
                exceptions = sys.exc_info()[0]
                self.MyPrint_WithoutLogFile("SendEmail Error: Failed to open ExcelBinaryFile " + EmailToSendDict["ExcelOrBinaryFileToAttachFullFilePath"] + " and convert to MIMEBase/encode_base64, exceptions: %s" % exceptions)
                return 0

            try:
                EmailMessage.attach(excel_binary_attachment_encoded)
                self.MyPrint_WithoutLogFile("Attached ExcelBinaryFile " + EmailToSendDict["ExcelOrBinaryFileToAttachFullFilePath"])

            except:
                exceptions = sys.exc_info()[0]
                self.MyPrint_WithoutLogFile("SendEmail Error: Failed to attach ExcelBinaryFile " + EmailToSendDict["ExcelOrBinaryFileToAttachFullFilePath"] + " to the email, exceptions: %s" % exceptions)
                return 0
        ####################################################

        #################################################### Attach the image
        if "ImageFileToAttachFullFilePath" in EmailToSendDict:

            try:
                image_data = open(EmailToSendDict["ImageFileToAttachFullFilePath"], 'rb').read()
                
                ImageFileLastSlashIndex = EmailToSendDict["ImageFileToAttachFullFilePath"].rfind("/")
                ImageFilenameWithExtension_NoPath = EmailToSendDict["ImageFileToAttachFullFilePath"][ImageFileLastSlashIndex + 1:]
                #print("ImageFilenameWithExtension_NoPath: " + str(ImageFilenameWithExtension_NoPath))
                image = MIMEImage(image_data, name=ImageFilenameWithExtension_NoPath)
            except:
                exceptions = sys.exc_info()[0]
                self.MyPrint_WithoutLogFile("SendEmail Error: Failed to open image " + EmailToSendDict["ImageFileToAttachFullFilePath"] + " and convert to MIMEimage, exceptions: %s" % exceptions)
                return 0

            try:
                EmailMessage.attach(image)
                self.MyPrint_WithoutLogFile("Attached image " + EmailToSendDict["ImageFileToAttachFullFilePath"])
            except:
                exceptions = sys.exc_info()[0]
                self.MyPrint_WithoutLogFile("SendEmail Error: Failed to attach image " + EmailToSendDict["ImageFileToAttachFullFilePath"] + " to the email, exceptions: %s" % exceptions)
                return 0
        ####################################################

        ####################################################
        try:
            SMTPobject = smtplib.SMTP("smtp.gmail.com", 587)
            SMTPobject.ehlo()
            SMTPobject.starttls()
            SMTPobject.ehlo()
            SMTPobject.login(self.EmailSenderAccountUsername, self.EmailSenderAccountPassword)
            SMTPobject.sendmail(self.EmailSenderAccountUsername, EmailToSendDict["To"], EmailMessage.as_string())
            SMTPobject.quit()
            SMTPobject.close()

            self.MyPrint_WithoutLogFile("Successfully sent email to " + EmailToSendDict["To"])
            return 1
        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("SendEmail Error: Failed to send email to " + EmailToSendDict["To"] + ", exceptions: %s" % exceptions)
            return 0
        ####################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SendEmail_ToEntireRecipientList(self, EmailToSendToAllRecipientsDict):

        ####################################################
        if "Subject" not in EmailToSendToAllRecipientsDict:
            self.MyPrint_WithoutLogFile("SendEmail_ToEntireRecipientList ERROR: EmailToSendDict must include the key 'Subject'.")
            return 0

        #THERE IS NOT REQUIREMENT FOR A 'TO' KEY BECAUSE WE KNOW WE'RE SENDING IT TO EVERYONE ON THE RECIPIENT LIST

        if "Text" not in EmailToSendToAllRecipientsDict:
            self.MyPrint_WithoutLogFile("SendEmail_ToEntireRecipientList ERROR: EmailToSendDict must include the key 'Text'.")
            return 0
        ####################################################

        EmailSuccessFlagDict = dict()
        for EmailAddress in self.EmailAddress_RecipientList:

            EmailToSendTo1addressDict = deepcopy(EmailToSendToAllRecipientsDict)

            EmailToSendTo1addressDict.pop('To', None) #delete a key regardless of whether it is in the dictionary
            EmailToSendTo1addressDict["To"] = EmailAddress

            EmailSuccessFlag = self.__SendEmail(EmailToSendTo1addressDict)
            EmailSuccessFlagDict[EmailAddress] = EmailSuccessFlag

        self.MyPrint_WithoutLogFile("SendEmail_ToEntireRecipientList, EmailSuccessFlagDict: " + str(EmailSuccessFlagDict))

        for Key in EmailSuccessFlagDict:
            if EmailSuccessFlagDict[Key] == 0:
                return 0

        return 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SendSMS_ToEntireRecipientList(self, SMStoSendToAllRecipientsDict):

        ####################################################
        if "Subject" not in SMStoSendToAllRecipientsDict:
            self.MyPrint_WithoutLogFile("SendSMS_ToEntireRecipientList ERROR: SMSToSendDict must include the key 'Subject'.")
            return 0

        ###### THERE IS NOT REQUIREMENT FOR A 'TO' KEY BECAUSE WE KNOW WE'RE SENDING IT TO EVERYONE ON THE RECIPIENT LIST

        if "Text" not in SMStoSendToAllRecipientsDict:
            self.MyPrint_WithoutLogFile("SendSMS_ToEntireRecipientList ERROR: SMSToSendDict must include the key 'Text'.")
            return 0
        ####################################################

        SMSsuccessFlagDict = dict()
        for PhoneNumber in self.PhoneNumber_RecipientList:

            SMStoSendTo1addressDict = deepcopy(SMStoSendToAllRecipientsDict)
            SMStoSendTo1addressDict.pop('To', None) #delete a key regardless of whether it is in the dictionary
            SMStoSendTo1addressDict["To"] = PhoneNumber

            SMSsuccessFlag = self.__SendSMS(SMStoSendTo1addressDict)
            SMSsuccessFlagDict[PhoneNumber]= SMSsuccessFlag

        self.MyPrint_WithoutLogFile("SendSMS_ToEntireRecipientList, SMSsuccessFlagDict: " + str(SMSsuccessFlagDict))

        for Key in SMSsuccessFlagDict:
            if SMSsuccessFlagDict[Key] == 0:
                return 0

        return 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SendSMS(self, SMStoSendDict):

        ####################################################
        if "Subject" not in SMStoSendDict:
            self.MyPrint_WithoutLogFile("SendSMS ERROR: SMStoSendDict must include the key 'Subject'.")
            return 0

        if "To" not in SMStoSendDict:
            self.MyPrint_WithoutLogFile("SendSMS ERROR: SMStoSendDict must include the key 'To'.")
            return 0
        else:
            if self.PhoneNumber_NumberErrorCheckerAndRecipientListAppending(SMStoSendDict["To"], 0) == 0: # ",0" means we're not adding it to our recipient list
                return 0

        if "Text" not in SMStoSendDict:
            self.MyPrint_WithoutLogFile("SendSMS ERROR: SMStoSendDict must include the key 'Text'.")
            return 0
        ####################################################

        SMSsuccessFlagList = []
        PhoneServiceProviderAppendix_list = ["@mms.att.net", "@tmomail.net", "@vtext.com", "@vzwpix.com", "@page.nextel.com"] #Sometimes verizon uses vtext, sometimes vzwpix
        for PhoneServiceProviderAppendix in PhoneServiceProviderAppendix_list:

            SMStoSendDict_For1provider = deepcopy(SMStoSendDict)
            SMStoSendDict_For1provider.pop('To', None) #delete a key regardless of whether it is in the dictionary
            SMStoSendDict_For1provider["To"] = SMStoSendDict["To"] + PhoneServiceProviderAppendix

            EmailSuccessFlag = self.__SendEmail(SMStoSendDict_For1provider)
            SMSsuccessFlagList.append(EmailSuccessFlag)

        if 1 in SMSsuccessFlagList: #Since we're intentioning sending the message to EVERY POSSIBLE CARRIER, we'll inherently have a bunch of failures. We only need 1 success.
            self.MyPrint_WithoutLogFile("Successfully sent SMS.")
            return 1
        else:
            self.MyPrint_WithoutLogFile("Failed to send SMS.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################
    def TxThread(self):  #unicorn

        print("Started the TxThread thread for EmailAndSMS_ReubenPython2and3Class object.")
        self.TxThread_still_running_flag = 1

        #############################################################################################################################################
        #############################################################################################################################################
        #############################################################################################################################################
        #############################################################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:


            try:
                ##################################################################################################################
                ##################################################################################################################
                ##################################################################################################################

                ###############################################
                ############################################### unicorn
                if self.TestEmailNeedsToBeSentFlag == 1:
                    self.EmailToTxQueue.put(dict([("Subject", "You are a recipient of the EmailAndSMS_ReubenPython2and3Class."),
                                                 ("Text", "Hello from the EmailAndSMS_ReubenPython2and3Class!"),
                                                 ("TxtFileToAttachFullFilePath", self.TestFilesFolderFullPath + "/TestTxtFile.txt"),
                                                 ("ExcelOrBinaryFileToAttachFullFilePath", self.TestFilesFolderFullPath + "/TestExcelFile.xlsx"),
                                                 ("ImageFileToAttachFullFilePath", self.TestFilesFolderFullPath + "/TestImage.jpg")]))

                    self.TestEmailNeedsToBeSentFlag = 0
                ###############################################
                ###############################################

                ###############################################
                ###############################################
                if self.TestSMSNeedsToBeSentFlag == 1:
                    self.SMStoTxQueue.put(dict([("Subject", "You are a recipient of the EmailAndSMS_ReubenPython2and3Class."),
                                                 ("Text", "Hello from the EmailAndSMS_ReubenPython2and3Class!")]))

                    self.TestSMSNeedsToBeSentFlag = 0
                ###############################################
                ###############################################

                ################################################################################################################
                ################################################################################################################
                if self.EmailToTxQueue.qsize() > 0:
                    EmailToTx_LocalCopy_Dict = self.EmailToTxQueue.get()

                    self.CurrentTime_CalculatedFromTxThread = self.getPreciseSecondsTimeStampString() - self.Starting_CalculatedFromTxThread
                    self.UpdateFrequencyCalculation_CalculatedFromTxThread()  # ONLY UPDATE IF WE HAD NEW DATA

                    self.MostRecentTxMessageDict = dict([("TxMessageCounter", self.LoopCounter_CalculatedFromTxThread),
                                                        ("TxMessageTimeSeconds", self.CurrentTime_CalculatedFromTxThread),
                                                        ("MessageType", "Email"),
                                                        ("MessageContentsDict", deepcopy(EmailToTx_LocalCopy_Dict))])

                    self.__SendEmail_ToEntireRecipientList(EmailToTx_LocalCopy_Dict) #This function can ONLY be called internally
                ################################################################################################################
                ################################################################################################################

                ################################################################################################################
                ################################################################################################################
                if self.SMStoTxQueue.qsize() > 0:
                    SMStoTx_LocalCopy_Dict = self.SMStoTxQueue.get()

                    self.CurrentTime_CalculatedFromTxThread = self.getPreciseSecondsTimeStampString() - self.Starting_CalculatedFromTxThread
                    self.UpdateFrequencyCalculation_CalculatedFromTxThread()  # ONLY UPDATE IF WE HAD NEW DATA

                    self.MostRecentTxMessageDict = dict([("TxMessageCounter", self.LoopCounter_CalculatedFromTxThread),
                                                        ("TxMessageTimeSeconds", self.CurrentTime_CalculatedFromTxThread),
                                                        ("MessageType", "SMS"),
                                                        ("MessageContentsDict", deepcopy(SMStoTx_LocalCopy_Dict))])

                    self.__SendSMS_ToEntireRecipientList(SMStoTx_LocalCopy_Dict) #This function can ONLY be called internally
                ################################################################################################################
                ################################################################################################################

                ################################################################################################################
                ################################################################################################################
                if self.TxThread_TimeToSleepEachLoop > 0.0:
                    time.sleep(self.TxThread_TimeToSleepEachLoop)
                ################################################################################################################
                ################################################################################################################

                ##################################################################################################################
                ##################################################################################################################
                ##################################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("EmailAndSMS_ReubenPython2and3Class TxThread: Exceptions: %s" % exceptions)

        #############################################################################################################################################
        #############################################################################################################################################
        #############################################################################################################################################
        #############################################################################################################################################

        print("Finished the TxThread for EmailAndSMS_ReubenPython2and3Class object.")
        self.TxThread_still_running_flag = 0

    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for EmailAndSMS_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent=None):

        GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=(GuiParent,))
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent=None):

        print("Starting the GUI_Thread for EmailAndSMS_ReubenPython2and3Class object.")

        ########################
        if parent == None:  #This class object owns root and must handle it properly
            self.root = Tk()
            self.parent = self.root

            ################################################### SET THE DEFAULT FONT FOR ALL WIDGETS CREATED AFTTER/BELOW THIS CALL
            default_font = tkFont.nametofont("TkDefaultFont")
            default_font.configure(size=8)
            self.root.option_add("*Font", default_font)
            ###################################################

        else:
            self.root = parent
            self.parent = parent
        ########################

        ########################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN)
        ########################

        ###########################################################
        SendTestEmailButton = Button(self.myFrame, text='Send Test Email', state="normal", width=15, command=lambda i=1: self.SendTestEmailButtonResponse())
        SendTestEmailButton.grid(row=0, column=0, padx=1, pady=1)
        ###########################################################

        ###########################################################
        self.EmailAddressEntry_TextInput = [StringVar()]
        self.EmailAddressEntry_TextInput[0].set(self.EmailAddressEntry_DefaultText)

        self.EmailAddressEntry = Entry(self.myFrame, state="normal", width=40,  textvariable=self.EmailAddressEntry_TextInput[0], justify='center')
        self.EmailAddressEntry.grid(row=0, column=1, padx=10, pady=0)

        self.EmailAddressEntry.bind('<Return>', lambda event, name = "<Return>": self.EmailAddressEntry_Response(event, name))
        self.EmailAddressEntry.bind('<Button-1>', lambda event, name = "<Button-1>": self.EmailAddressEntry_Response(event, name))
        self.EmailAddressEntry.bind('<Button-2>', lambda event, name = "<Button-2>": self.EmailAddressEntry_Response(event, name))
        self.EmailAddressEntry.bind('<Button-3>', lambda event, name = "<Button-3>": self.EmailAddressEntry_Response(event, name))
        self.EmailAddressEntry.bind('<Leave>', lambda event, name = "<Leave>": self.EmailAddressEntry_Response(event, name))
        ###########################################################

        ###########################################################
        SendTestSMSButton = Button(self.myFrame, text='Send Test SMS', state="normal", width=15, command=lambda i=1: self.SendTestSMSButtonResponse())
        SendTestSMSButton.grid(row=1, column=0, padx=1, pady=1)
        ###########################################################

        ###########################################################
        self.PhoneNumberEntry_TextInput = [StringVar()]
        self.PhoneNumberEntry_TextInput[0].set(self.PhoneNumberEntry_DefaultText)

        self.PhoneNumberEntry = Entry(self.myFrame, state="normal", width=40,  textvariable=self.PhoneNumberEntry_TextInput[0], justify='center')
        self.PhoneNumberEntry.grid(row=1, column=1, padx=10, pady=0)

        self.PhoneNumberEntry.bind('<Return>', lambda event, name = "<Return>": self.PhoneNumberEntry_Response(event, name))
        self.PhoneNumberEntry.bind('<Button-1>', lambda event, name = "<Button-1>": self.PhoneNumberEntry_Response(event, name))
        self.PhoneNumberEntry.bind('<Button-2>', lambda event, name = "<Button-2>": self.PhoneNumberEntry_Response(event, name))
        self.PhoneNumberEntry.bind('<Button-3>', lambda event, name = "<Button-3>": self.PhoneNumberEntry_Response(event, name))
        self.PhoneNumberEntry.bind('<Leave>', lambda event, name = "<Leave>": self.PhoneNumberEntry_Response(event, name))
        ###########################################################

        ###########################################################
        self.RecipientList_label = Label(self.myFrame, text="RecipientList_label", width=40)
        self.RecipientList_label.grid(row=0, column=2, padx=1, pady=1, columnspan=1, rowspan=2)
        ###########################################################

        ###########################################################
        self.DebugInfo_label = Label(self.myFrame, text="DebugInfo_label", width=40)
        self.DebugInfo_label.grid(row=0, column=3, padx=1, pady=1, columnspan=1, rowspan=1)
        ###########################################################

        ########################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=100)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=1, pady=1, columnspan=4, rowspan=10)
        ########################

        ########################
        if self.RootIsOwnedExternallyFlag == 0: #This class object owns root and must handle it properly
            self.root.protocol("WM_DELETE_WINDOW", self.ExitProgram_Callback)

            self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds, self.GUI_update_clock)
            self.GUI_ready_to_be_updated_flag = 1
            self.root.mainloop()
        else:
            self.GUI_ready_to_be_updated_flag = 1
        ########################

        ########################
        if self.RootIsOwnedExternallyFlag == 0: #This class object owns root and must handle it properly
            self.root.quit()  # Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
            self.root.destroy()  # Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
        ########################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EmailAddressEntry_Response(self, event = None, name = "default"):

        if name == "<Button-1>" or name == "<Button-2>" or name == "<Button-3>":
            self.EmailAddressEntry_TextInput[0].set("")

        elif name == "<Leave>" and self.EmailAddressEntry_TextInput[0].get() == "": #If we click into the box and then click out without typing
            self.EmailAddressEntry_TextInput[0].set(self.EmailAddressEntry_DefaultText)
            self.myFrame.focus_set() #Gets the keyboard icon out of the widget

        elif name != "<Leave>":
            EmailAddressEntryInputToParse = self.EmailAddressEntry_TextInput[0].get()
            self.myFrame.focus_set() #Gets the keyboard icon out of the widget

            if self.EmailAddress_AddressErrorCheckerAndRecipientListAppending(EmailAddressEntryInputToParse, 1) == 0: #Failed
                self.EmailAddressEntry_TextInput[0].set(self.EmailAddressEntry_DefaultText)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EmailAddress_AddressErrorCheckerAndRecipientListAppending(self, EmailAddressToCheck, AddInputToRecipientListFlag = 0):

        EmailAddressToCheck = str(EmailAddressToCheck)

        if EmailAddressToCheck.find("@") == -1:
            self.MyPrint_WithoutLogFile("EmailAddress_AddressErrorCheckerAndRecipientListAppending ERROR: Email address must contain '@'")
            return 0

        if EmailAddressToCheck not in self.EmailAddress_RecipientList and AddInputToRecipientListFlag == 1:
            self.EmailAddress_RecipientList.append(EmailAddressToCheck)
            #self.MyPrint_WithoutLogFile("self.EmailAddress_RecipientList: " + str(self.EmailAddress_RecipientList))

        return 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PhoneNumberEntry_Response(self, event = None, name = "default"):

        if name == "<Button-1>" or name == "<Button-2>" or name == "<Button-3>":
            self.PhoneNumberEntry_TextInput[0].set("")

        elif name == "<Leave>" and self.PhoneNumberEntry_TextInput[0].get() == "": #If we click into the box and then click out without typing
            self.PhoneNumberEntry_TextInput[0].set(self.PhoneNumberEntry_DefaultText)
            self.myFrame.focus_set() #Gets the keyboard icon out of the widget

        elif name != "<Leave>":
            PhoneNumberEntryInputToParse = self.PhoneNumberEntry_TextInput[0].get()
            self.myFrame.focus_set() #Gets the keyboard icon out of the widget

            if self.PhoneNumber_NumberErrorCheckerAndRecipientListAppending(PhoneNumberEntryInputToParse, 1) == 0: #Failed
                self.PhoneNumberEntry_TextInput[0].set(self.PhoneNumberEntry_DefaultText)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################.
    ##########################################################################################################
    def PhoneNumber_NumberErrorCheckerAndRecipientListAppending(self, PhoneNumberToCheck, AddInputToRecipientListFlag = 0):

        try:
            PhoneNumberToCheck_int = int(PhoneNumberToCheck) #Succeeds if only numbers are present, BUT WE WON'T PASS THIS INTO PhoneNumberToCheck_str BECAUSE LEADING 0'S ARE DELETED.
            PhoneNumberToCheck_str = str(PhoneNumberToCheck)

            #self.MyPrint_WithoutLogFile("PhoneNumberToCheck: " + PhoneNumberToCheck_str + ", Length = " + str(len(PhoneNumberToCheck_str)))

            if len(PhoneNumberToCheck_str) != 10:
                self.MyPrint_WithoutLogFile("PhoneNumber_NumberErrorCheckerAndRecipientListAppending ERROR: Phone number must have length = 10.")
                return 0

            if PhoneNumberToCheck_str not in self.PhoneNumber_RecipientList and AddInputToRecipientListFlag == 1:
                self.PhoneNumber_RecipientList.append(PhoneNumberToCheck_str)
                #self.MyPrint_WithoutLogFile("self.PhoneNumber_RecipientList: " + str(self.PhoneNumber_RecipientList))

            return 1

        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("PhoneNumber_NumberErrorCheckerAndRecipientListAppending, Exceptions: %s" % exceptions)
            return 0
    ##########################################################################################################
    ##########################################################################################################

    #######################################################################################################################
    def SendTestEmailButtonResponse(self):

        self.TestEmailNeedsToBeSentFlag = 1

    #######################################################################################################################

    #######################################################################################################################
    def SendTestSMSButtonResponse(self):

        self.TestSMSNeedsToBeSentFlag = 1

    #######################################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                RecipientList_label_TextToDisplay = "Email Recipient List:"

                for EmailAddress in self.EmailAddress_RecipientList:
                    RecipientList_label_TextToDisplay = RecipientList_label_TextToDisplay + "\n" + EmailAddress

                RecipientList_label_TextToDisplay = RecipientList_label_TextToDisplay + "\nSMS Recipient List:"

                for PhoneNumber in self.PhoneNumber_RecipientList:
                    RecipientList_label_TextToDisplay = RecipientList_label_TextToDisplay + "\n" + PhoneNumber

                self.RecipientList_label["text"] =  RecipientList_label_TextToDisplay
                #######################################################

                #######################################################
                self.DebugInfo_label["text"] = "TxMessageCounter: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.MostRecentTxMessageDict["TxMessageCounter"], 0, 3)  + \
                                            "\nTxMessageTimeSeconds: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.MostRecentTxMessageDict["TxMessageTimeSeconds"], 0, 3) + \
                                            "\nTx Freq: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromTxThread, 0, 3) + \
                                            "\nEmailToTxQueue Length: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EmailToTxQueue.qsize(), 0, 3) + \
                                            "\nSMStoTxQueue Length: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.SMStoTxQueue.qsize(), 0, 3)
                #######################################################

                #######################################################
                self.PrintToGui_Label.config(text = self.PrintToGui_Label_TextInput_Str)
                #######################################################

            #######################################################
            #######################################################
            if self.RootIsOwnedExternallyFlag == 0:  # This class object owns root and must handle it properly
                self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds, self.GUI_update_clock)
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################
