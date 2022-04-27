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


cnx = mysql.connector.connect(user='root', password='inshALLAH%6',
                              host='127.0.0.1',
                              database='fedbfull')#
cursor = cnx.cursor()


def getAllGeneratedIds():
    query = "SELECT distinct database_id,compoundid from bandstructure where source='icsd'"
    cursor.execute(query)
    return [item[0] for item in cursor.fetchall()]


print getAllGeneratedIds()