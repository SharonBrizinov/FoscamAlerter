# FoscamAlerter
Foscam's IP Camera WatchDog.

This project aims to help people easily keep tracking of their Foscam camera logins, and to be notified when someone logs in to thier camera. 

  - Keep track of all of your camera's logins.
  - Receive an email when someone logs in.

### Inspiration
[Foscam][df1] is a real player in the IP Camera industry and provides many IP based prodcuts indoor and outdoor. However, most of the products are using basic HTTP connection and all the connections to the camera are badly insecure. 
This means, everytime I login to my camera from outside of my home LAN, I expose myself to a potential hacker who could sniff the communication (e.g: MITM) and steal my camera's credentials. In addition there are a lot of security isseus that were discovered over the years with those cameras (example for some of those [CVEs][df2]).

### Requirements
- Python 2.7
    
### Pre-Running
Edit some of the variables before running.

>Required:
- USERNAME: generic username for all cameras.
- PASSWORD: generic password for all cameras.
- IP_HOME_PREFIX: base form of your LAN IP (192.168.1).
- CAMERA_LIST_TUPPLES: tuples of all of your cameras at home. (IP, PORT, USERNAME, PASSWORD).

>Optional:
- FILE_LOG_PATH: log path.
- EMAIL_FROM: receive email from - username.
- EMAIL_FROM_PASS: receive email from - password.
- EMAIL_TO: your personal email address to be notified at.


### Run

```sh
$ python foscam_camera_log_informer.py
```


***MIT License***


 [df1]: <http://foscam.us/>
 [df2]: <https://www.cvedetails.com/vulnerability-list/vendor_id-12538/Foscam.html>
