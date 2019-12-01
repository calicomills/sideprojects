import string
import datetime
import subprocess
import os
import sys
import paramiko
import shutil
from collections import OrderedDict

path = r"D:\syslog_test"
path_old = r"D:\syslog_test\old_files"
path_new = r"D:\syslog_test\latest_files"

round_name = sys.argv[1]
print sys.argv[1]

class Message:
    def __init__(self):
        print "Initialising..."
    def compare_message(self,old_file,new_file):
          file_out = open(os.path.join(path,"Round_"+round_name + "_messages.log"),'w')
          file1 = open(old_file,'r')
          file2 = open(new_file,'r')
          main_dict = OrderedDict()
          for line in file2.readlines() :
              main_dict.update({line:1})
          for line in file1.readlines() :
              main_dict[line]=2      
          for d in main_dict:
              if main_dict.get(d) == 1 :
                  print main_dict.get(d)
                  file_out.write(d)
    def copy_messages(self,files):        
        if files == "latest":
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect('192.168.1.40', username='root', password='ctp1fb',timeout=30)  
                sftp = ssh.open_sftp()  
                sourcedirpath = path_new
                cmd= 'C:\Program Files (x86)\WINSCP\WinSCP.com' +' /command "open root@192.168.1.40 -hostkey=""ssh-rsa 2048 d5:7c:73:cf:11:e9:4e:40:c3:17:2e:52:d6:93:18:9b""" "get /var/log/messages* '+sourcedirpath+'\\"  "exit"' 
                print cmd
                subprocess.call(cmd)
        if files == "duplicate" :
                new_files = os.listdir(path_new)
                for file in new_files :
                    if "messages" in file:
                        old_file = os.path.join(path_new,file)
                        new_file = os.path.join(path_old,file)
                        
                        shutil.copy(old_file,new_file)
                        print "copying...."
    def createmegatxtfiles(self,path1,path2):
        old_msgs = os.listdir(path1)
        mega_old_path = os.path.join(path_old,"mega_old.txt")
        mega_old_f = open(mega_old_path,"w")
        for old in old_msgs :
            if "messages" in old :
                old_f = os.path.join(path1,old)
                with open(old_f,'r') as file1:
                    for lines in file1.readlines():
                        mega_old_f.write(lines)       
        new_msgs = os.listdir(path2)
        mega_new_path = os.path.join(path_new,"mega_new.txt")
        mega_new_f = open(mega_new_path,"w")
        for new in new_msgs :
            if "messages" in new:
                new_f = os.path.join(path2,new)
                with open(new_f,'r') as file1:
                    for lines in file1.readlines():
                        mega_new_f.write(lines)                   
        return (mega_old_path,mega_new_path)

          
obj = Message()
obj.copy_messages("latest")
mega_oldf,mega_newf = obj.createmegatxtfiles(path_old,path_new)
obj.compare_message(mega_oldf,mega_newf)
obj.copy_messages("duplicate")


             

 