from utils.utils import path_dict

import sys
import os
import argparse

sys.path.append(os.getcwd())

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str)
parser.add_argument("save_path", type=str, default="./save")

args = parser.parse_args()

if not os.path.isdir(args.save_path):
  os.mkdir(args.save_path)
  
ep_path = path_dict(args.path)

for key in ep_path:
  #save_folder
  folder = args.save_path + '/' +key
  if not os.path.isdir(folder):
    os.mkdir(folder)
  
  #new directory
  for ep in ep_path[key]:
    file_name = re.sub('.xlsx', '.pickle', ep.split('/')[-1])
    tmp_name = re.sub('.xlsx', 'tmp.pickle', ep.split('/')[-1])
    
    #already exists
    if file_name in os.listdir(folder): pass
    
    else:
      lines = pd.read_excel(ep)[0]
      names = defaultdict(list)

      #update if there is tmp pickle
      if tmp_name in os.listdir(folder):
        with open(folder +'/' + tmp_name, 'rb') as f:
          tmp = pickle.load(f)
      
        lines = pd.read_excel(ep)[0][int(tmp['end'][-1])+1:] #pages update
        names = tmp #pickle update
        print('The tmp file exists: ', names)

      #read lines and get the indice of mentions
      for n, line in enumerate(lines):
        print('Line: ', [(n,t) for n, t in enumerate(line.split(' '))])
        names['end'].append(n)
        
        while True: #In one line
          if len(names.keys()) > 0:
            print(names.keys())

          name = input('Mention? ') # will be used as id of the cluster

          if len(name) != 0:   
            index = input('Start, End or just a number').split(',')
            try:
              if name == 'stop':
                raise
              names[name].append((n, int(index[0]), int(index[-1])))
            
            except:
              names['end'] = names['end'][:-1]
              with open(folder + '/' + tmp_name, 'wb') as f:
                pickle.dump(names, f, pickle.HIGHEST_PROTOCOL)
              raise
          
          #escape while
          else: break
        
        #clear
        os.system('cls')
      
      # After finishing one episode
      with open(folder + '/' + file_name, 'wb') as f: #save 
        pickle.dump(names, f, pickle.HIGHEST_PROTOCOL)
      
      if os.path.isdir(folder + '/' + tmp_name): #erase
        os.remove(folder + '/' + tmp_name)
      
      stop = input('stop? press something')
      if len(stop) != 0: raise
        
        
