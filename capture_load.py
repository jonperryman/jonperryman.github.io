#! /usr/bin/python3
import sys
import os
import mysql.connector
import glob

table = "world"

mydb = mysql.connector.connect(
    host="localhost",
    user="testuser",
    database="covid",
    passwd="testuserPassword"
    )

mycursor = mydb.cursor()

def getfiles():
    a = 1

def loaddata(filename):
    def sqlcmd(sqldata):
        mycursor.execute(sqldata)
        myresult = mycursor.fetchall()
        return(myresult)
    
    f = open(filename,"r")
    lines = f.readlines()
    f.close()
    lines.pop(0)     # ignore title line

    table = filename.split("/")[-1][5:].split("_")[0].lower()
    for line in lines:
        fields = line.split(",")
        sql = ""
        for field in fields:
            field = field.strip()
            if field == "":
                sql += ",0"
            elif field == "NaN" or field == "N/A":
                sql += ",-999999"
            elif field.isnumeric():
                sql += ',' + field
            else:
                sql += ',"' + field + '"'
        sql = "INSERT INTO `"+table+"` values(" + sql[1:] + ");"
        mycursor.execute(sql)
        if mycursor._affected_rows != 1:
            raise Exception("Insert failed with " + mycursor.affected_rows + " rows")
    mydb.commit()
    os.rename(filename,filename+".loaded")

# load data to the tables
files = glob.glob("/home/jon/Downloads/covid*.csv")
for file in files:
    loaddata(file)

