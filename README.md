# FoscamAlerter
Foscam's IP Camera WatchDog.

This project aims to help people easily keep tracking of their Foscam camera logins, and to be notified when someone logs in to thier camera. 

  - Keep track of all of your camera's logins.
  - Receive an email when someone logs in.

### Inspiration
[Foscam][df1] is a real player in the IP Camera industry and provides many IP based prodcuts indoor and outdoor. However, most of the products are using basic HTTP which means that all the connections to the camera are badly insecure. 
This means, everytime I login to my camera from outside of my home LAN, I expose myself to a potential hacker who could sniff the communication (e.g: MITM) and steal my camera's credentials. We could use some tricks to encrypte the connection at home using VPN solutions / installing SSH server at home and connect to the camera only from the local network through the SSH server. But it all requires some level of understanding and a lot of free time to deal with. Two things which most of the people are lacking of.
In addition there are a lot of security isseus that were discovered over the years with those cameras (example for some of those [CVEs][df2]).

### Damage control and preventive measures
Assuming you can't secure your camera properly, the solution would be a watch-dog which informs you whenever someone logins to your camera. This way, you'll know in real time of potential intrusion and could prevent the attacker's next step by:
 - Shutting down the camera.
 - Update firmware.
 - Change username & password.
 - Change IP, DNS address, Port.

### Requirements
- Python 2.7
- Foscam Camera, tested with:
    - Foscam FI8910W (11.37.2.X, 2.0.10.X)
    
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


### Log Example

```sh
Sun, 2015-01-13 13:31:35   USER       192.168.1.11      access
Sun, 2015-01-13 13:32:52   USER       192.168.1.11      access
Sun, 2015-01-13 13:34:15   USER       192.168.1.11      access
```


***MIT License***


 [df1]: <http://foscam.us/>
 [df2]: <https://www.cvedetails.com/vulnerability-list/vendor_id-12538/Foscam.html>
