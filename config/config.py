import os

#Dirs
configDir = os.path.dirname(os.path.abspath(__file__))
root =os.path.abspath(os.path.join(configDir, os.pardir))
resourcesDir =os.path.abspath(os.path.join(root, 'resources'))
externalTools =os.path.abspath(os.path.join(root, 'externalTools'))

#Tools
sqlMap =os.path.abspath(os.path.join(externalTools, 'sqlmap/sqlmap.py'))

#Resources
sqlMapOutPut =os.path.abspath(os.path.join(resourcesDir, 'sqlmap_output.txt'))
wordList =os.path.abspath(os.path.join(resourcesDir, 'wordlist.txt'))