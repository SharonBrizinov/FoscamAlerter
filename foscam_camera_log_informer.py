#!/usr/bin/python

'''
Foscam Log Informer
Pyhton 2.7

By: Sharon Brizinov
'''

# Imports
import httplib
import time
import smtplib
from datetime import datetime

# Camera stuff
USERNAME = "USERNAME" # Generic Username
PASSWORD = "PASSWORD" # Generic Password

# Configuration
IP_HOME_PREFIX = "192.168.1."
DATE_STRUCT = r"%a, %Y-%m-%d %H:%M:%S"
LOG_URL = "/get_log.cgi?user=%s&pwd=%s"
DEFULT_TIMOUT = 2
SLEEP_TIME_SEC = 10 * 60 # 10 Minutes

# Full log file path
FILE_LOG_PATH = r"foscam.log"

# LOG PARSER
LIST_ITEMS_REMOVE = [r"var log_text='", r"';"]
SPLIT_ELEMENTS = "   "

# Regular logins
INDEX_DATE = 0
INDEX_USERNAME = 1
INDEX_COMMAND = 1
INDEX_IP_ADDR = 2
INDEX_INFO = 3

# Special commands
STR_LOGIN = "login"
STR_MOTION_DETECTED = "motion detect"


# Mail stuff
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 465  #Or 587

EMAIL_FROM = "EMAIL_FROM@gmail.com"
EMAIL_FROM_PASS = "PASSWORD"
EMAIL_FROM_NICKNAME = "NICKNAME"
EMAIL_TO = "EMAIL_TO@gmail.com"
EMAIL_SUBJECT = "Camera #%s Alert"
EMAIL_SUBJECT_GENERIC = "Camera Notification Alerts"
EMAIL_BODY = "ALERT!\n%s"

# Cameras
CAMERA_LIST_TUPPLES = [("192.168.1.11", 81, USERNAME, PASSWORD),
                        ("192.168.1.21", 82, USERNAME, PASSWORD),
                        ("192.168.1.31", 83, USERNAME, PASSWORD)]

'''
Get whole http page
'''
def get_http_page(host, port = 80, timout = 10, path="/"):
    """ 
    This function retreives webpages
    """
    ret = ""
    try:
        conn = httplib.HTTPConnection(host, port)#, timeout = timout)
        conn.request("GET", path)
        ret = conn.getresponse().read()
    except:
        pass
    return ret

def get_ip_str_in_home(ip, prefix_home):
    if ip.startswith(prefix_home):
        return ip + " (HOME)"
    else:
        return ip


def write_to_log(data_to_write, is_title = False, should_print = False):
    with open(FILE_LOG_PATH, "a") as f:
        if is_title:
            f.write("\n--------\n")

        # Write to log
        f.write(data_to_write + "\n")
        
        # Print to screen
        if should_print:
            print data_to_write

        if is_title:
            f.write("--------\n")


'''
Single loging item representation
'''
class LoginItem():
    def __init__(self, date, command, username, ip_addr, info, camID):

        # Get real date
        if isinstance(date, (str, unicode)):
            self.date = datetime.fromtimestamp( time.mktime( time.strptime(date, DATE_STRUCT) ) )            
        else:
            self.date = date

        self.command = command
        self.username = username
        self.ip_addr = ip_addr
        self.info = info
        self.camID = camID

    def __repr__(self):
        # If we have command, and it is not login, print the command
        if self.command != None and self.command != "" and self.command != STR_LOGIN:
            return str(self.date) + ", CAM#" + str(self.camID) + ": " + self.command
        # Login
        else:
            return str(self.date) + ", CAM#" + str(self.camID) + ": " + self.username + " has connected from IP <" + get_ip_str_in_home(self.ip_addr,IP_HOME_PREFIX) + "> | " + self.info
'''
Handles the whole log page
'''
class WebpageLog():
    def __init__(self, host, port, log_url, username, password, camID):
        self.host = host
        self.port = port
        self.log_url = log_url
        self.username = username
        self.password = password
        self.camID = camID
        self.date_last_check = None

    def get_url_filled(self):
        '''
        Get full url filled with params
        '''
        return self.log_url % (self.username, self.password)

    def get_http_page_cleaned(self, list_items_to_remove = []):
        '''
        Remove unwanted items form result page
        '''
        page = get_http_page(self.host, self.port, timout = DEFULT_TIMOUT, path = self.get_url_filled())

        'Remove unwanted strings'
        for str_remove in list_items_to_remove: 
            page = page.replace(str_remove, r"")
        
        return page

    def get_log_list(self):
        '''
        Get page log as a list
        '''
        page = self.get_http_page_cleaned(LIST_ITEMS_REMOVE)
        return filter(None, page.split(r"\n"))

    def get_logins_list(self):
        '''
        Get all logins as list of 'login items'
        '''
        # Get all log as list of raw strings
        logins_list_before_parse = self.get_log_list()
        # List with real login items
        login_items_list = []

        for loggin in logins_list_before_parse:

            # Stripping leading spaces and tabs.
            # Also make sure we have something to work with
            loggin = loggin.lstrip()
            
            if loggin == '' or loggin == None:
                continue

            # split for taking each element seperatly, clean it and finaly filter empty items
            loggin_single_list = loggin.split(SPLIT_ELEMENTS)
            loggin_single_list = map(lambda x: x.lstrip(), loggin_single_list)
            loggin_single_list = filter(None, loggin_single_list)
            
            # Special command
            if len(loggin_single_list) == 2:
                login_item = LoginItem(loggin_single_list[INDEX_DATE],
                                loggin_single_list[INDEX_COMMAND],
                                None,
                                None,
                                None,
                                self.camID)
            
            # Ugly fix: Sometime there is no user 
            if len(loggin_single_list) == 3:
                loggin_single_list.insert(INDEX_USERNAME, "???")
            
            if len(loggin_single_list) == 4:
                # Adding items to list
                login_item = LoginItem(loggin_single_list[INDEX_DATE],
                                    STR_LOGIN,
                                loggin_single_list[INDEX_USERNAME],
                                loggin_single_list[INDEX_IP_ADDR],
                                loggin_single_list[INDEX_INFO],
                                self.camID)

            login_items_list.append(login_item)

        return login_items_list

    def update_last_check(self, current_date_check):
        if self.date_last_check == None or self.date_last_check < current_date_check:
            self.date_last_check = current_date_check





def send_email(body, camID = -1):
    '''
    Send mail - GMAIL
    '''
    # Sending mail
    try:
        gmail_user = EMAIL_FROM
        gmail_pwd = EMAIL_FROM_PASS
        FROM = EMAIL_FROM_NICKNAME
        TO = [EMAIL_TO] #must be a list

        # Generic alert (system's up/down) vs. regular alert (camera X was accessed)
        if camID == -1:
            SUBJECT = EMAIL_SUBJECT_GENERIC
        else:
            SUBJECT = EMAIL_SUBJECT % str(camID)

        TEXT = EMAIL_BODY % body

        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        # Send
        server = smtplib.SMTP_SSL(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.login(gmail_user, gmail_pwd)
        server.ehlo()
        #server.starttls()                
        server.sendmail(FROM, TO, message)
        #server.quit()
        server.close()

    except Exception, e:
        print "Could not send mail beaucse: <%s>" % str(e)
        pass

def main():
    '''
    Main funciton
    '''
    
    # Starting...
    started_str = "Started at %s" % datetime.fromtimestamp(time.time())
    write_to_log(started_str, True, True)
    send_email(started_str)

    # Add all cameras
    cameras_list = []
    for i in xrange(len(CAMERA_LIST_TUPPLES)):
        cameras_list.append(WebpageLog(CAMERA_LIST_TUPPLES[i][0], CAMERA_LIST_TUPPLES[i][1], LOG_URL, CAMERA_LIST_TUPPLES[i][2], CAMERA_LIST_TUPPLES[i][3], i+1))

    # First add all login items to a big dated sorted list
    login_list = []
    for camera_log in cameras_list:
        login_list += camera_log.get_logins_list()
        if len(login_list) > 0:
            camera_log.update_last_check(login_list[-1].date)
    login_list.sort(key=lambda elem: elem.date)

    # Write to log
    for login in login_list:
        write_to_log(str(login))

    # Watch DOG
    try:
        while(True):

            # For each camera log, look for all log items and search for new ones....
            for camera_log in cameras_list:
                for login in camera_log.get_logins_list():

                    # Check for each login line -->
                    # if the date is greater the current greatest date
                    if login.date > camera_log.date_last_check:

                        # Write to log and print to screen
                        write_to_log(str(login), False, True)

                        # Sending mail
                        send_email(str(login), login.camID)

                        # Add to list
                        login_list.append(login)

                        # Update last checked date for current camera log
                        camera_log.update_last_check(login.date)

            # Sleep...
            time.sleep(SLEEP_TIME_SEC)

    except (KeyboardInterrupt, SystemExit):
        print "Keyboard interupt !"

    # Shutting down...
    shutdown_str = "Closed at %s" % datetime.fromtimestamp(time.time())
    write_to_log(shutdown_str, True, True)
    send_email(shutdown_str)
    
if __name__== "__main__":
    main()