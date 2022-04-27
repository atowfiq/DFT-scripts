import matplotlib.pyplot as plt
import numpy as np

import os
import os.path
import subprocess
from shutil import copyfile, move
from os.path import isfile, join, basename, exists
import copy
import matplotlib.pyplot as plt
import mysql.connector
from random import shuffle
import numpy as np

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='fedbfull')
cursor = cnx.cursor()


cursor.execute ("select * from bandstructure")
# fetch all of the rows from the query
data = cursor.fetchall ()
# print the rows
for row in data:
    bands = row[2].split(", ")
# close the cursor object
    x= np.array(bands)
    plt.plot(x)
plt.show()
cursor.close ()
# close the connection
cnx.close ()
