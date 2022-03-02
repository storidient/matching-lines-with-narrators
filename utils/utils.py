import re
import os

def path_dict(path):
  ep_path = dict()

  for folder in os.listdir(path):
    folder_path = path + '/' + folder
    file_list = os.listdir(folder_path)
    file_list = sorted(file_list, key = lambda x : int(re.sub('[^0-9]', '', x)))
    ep_path[folder] = [folder_path + '/' + file for file in file_list]
  
  return ep_path
