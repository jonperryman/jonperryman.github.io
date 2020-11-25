#! /usr/bin/python3
import mysql.connector


table = "FBIarrests"

race_table = {'Black' : 'Black',
    'Hispanic' : 'Hispanic',
    'White' : 'White'}

mydb = mysql.connector.connect(
    host="localhost",
    user="stduser",
    database="police_shootings",
    passwd="pwdStduser"
    )

mycursor = mydb.cursor()

def main():
    if table == "FBIarrests":
        FBIarrests() 
        exit()
    elif table == "allDeaths":
        allDeaths() 
        exit()
    elif table == "fbi":
        print("<h2>fbi report</h2>")
        sql = """
            SELECT *  
                FROM police_shootings. fbi_arrests
                limit 1000
            """
        race_table = {'B' : 'Black',
            'H' : 'Hispanic',
            'W' : 'White'}
    elif False:
        print("<h2>Unarmed or attacking deaths by race and year</h2>")
        sql = """
            SELECT race, substring(date,1,4), count(DISTINCT(`name`))  
                FROM police_shootings. washingtonPost
                where (armed like 'un%' or armed = '') and threat_level != 'attack'
                group by race, substring(date,1,4)
                limit 1000
            """
        race_table = {'B' : 'Black',
            'H' : 'Hispanic',
            'W' : 'White'}
    elif False:
        print("<h2>Unarmed not attacking deaths by race and year</h2>")
        sql = """
            SELECT race, substring(date,1,4), count(DISTINCT(`name`))  
                FROM police_shootings. mappingPoliceViolence
                where (unarmed = 'unarmed' or unarmed like 'un%' or unarmed = '') 
                    and alleged_threat_level != 'attack'
                    and substr(date,1,4) >= 2015
                group by race, substring(date,1,4)
                limit 1000
            """
    elif False:
        print("<h2>All deaths by race and year</h2>")
        sql = """
            SELECT race, substring(date,1,4), count(DISTINCT(name))  
                FROM police_shootings. mappingPoliceViolence
                where substr(date,1,4) >= 2015
                group by race, substring(date,1,4)
                limit 1000
            """


    print("<p class='hilite'>"+sql+"</p>\n")

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    if table == "fbi":
        fbi(myresult)
        exit()

    genericTable(myresult)

def FBIarrests():

    sql = ("select offence,total1,total2,black,white,hispanic from `fbi_arrests`")
    print("<p class='hilite'>"+sql+"</p>\n")

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    for row in myresult:
        work = int(row[1].replace(',',''))-int(row[2].replace(',',''))
        print(row[0], 
        int(row[1].replace(',',''))-int(row[2].replace(',','')),
        int(row[1].replace(',',''))-int(row[2].replace(',',''))+int(row[3].replace(',','')),
        row[3], row[4], row[5])

def allDeaths():
    displayAllDeaths("race", "1=1") 
    displayAllDeaths("'unarmed', race, 'men'", "gender='male' and (unarmed not like 'un%' or alleged_threat_level='attack')") 
    displayAllDeaths("'armed', race, 'men'", "gender='male' and unarmed like 'un%' and alleged_threat_level!='attack'") 

def displayAllDeaths(fields, where):

    sql = ("select '<div id=""', lower(race), '""> #', " + fields + 
        " ,'per million &nbsp; (actual', round(count(distinct(name))/5), ')</div>'" + 
        " from `mappingPoliceViolence.org` where date>=2015 and date<=2019 and (" +
        where + ") group by race;")
    print("<p class='hilite'>"+sql+"</p>\n")

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    for row in myresult:
        line = ""
        for column in row:
            line += " " + str(column)
        print(line)

def genericTable(myresult):

    tab = {}
    tabsum = {}
    race = 'xxxx'

    for x in myresult:

        if x[0] != race:
            race = x[0]
            race_text = race_table.get(race, "Other")
            if race_text not in tab:
                tab[race_text] = {}
        try:
            tab[race_text][x[1]] += x[2]
        except:
            tab[race_text][x[1]] = x[2]

        try:
            tabsum[x[1]] += x[2]
        except KeyError:
            tabsum[x[1]] = x[2]

    tabsum = sorted(tabsum.items())
    tab = sorted(tab.items())

    data = "<table><tr><td> </td>"
    for year in tabsum:
        data += "<td style='text-align: center;'>" + year[0] + "</td>"
    data += "<td>total</td></tr>\n"

    for race in tab:
        sum = 0
        data += "<tr><td> "+race[0]+" </td>"
        for year in tabsum: 
            occurance = race[1].get(year[0], 0)
            data += "<td> " + str(occurance) + " <br/> " + \
            str(round(occurance / year[1] * 100)) + "% </td>"
            sum += occurance
        data += "<td> " + str(sum) + " </tr>\n "

    sum = 0
    data += "<tr><td>Total</td>"
    for year in tabsum:
        data += "<td> " + str(year[1]) + " <br/> 100% </td>"
        sum += year[1]
    data += "<td> " + str(sum) + " </td></tr>\n</table>"

    print(data)

    return()

def fbi(myresult):

    for x in myresult:

        offense = x[0]
        other = int(x[3].replace(',','')) + int(x[4].replace(',','')) + int(x[5].replace(',',''))
        white = int(x[1].replace(',',''))
        black = int(x[2].replace(',',''))
        hispanic = int(x[6].replace(',',''))
        total = other + white + black + hispanic

        print( '<div class="arrests" offense="' + offense + '"', 
            'black="'+str(black)+'"', 
            'white="'+str(white)+'"', 
            'hispanic="'+str(hispanic)+'"', 
            'other="'+str(other)+'">',
            '</div>\n'
        ) 

    return()

main()
exit()



"""ALTER TABLE `fatalencounters`
add uid varchar(100) , add name varchar(100) , add age varchar(100) , add gender varchar(100) , add race varchar(100) , add race_with_imputations varchar(100) , add imputation_probability varchar(100) , add URL_of_image_of_deceased varchar(255) , add date varchar(100) , add address varchar(255) , add city varchar(100) , add Full_Address varchar(255) , add zip varchar(100) , add county varchar(100) , add unnamed1 varchar(100) , add agency_responsible varchar(100) , add Cause varchar(100) , add brief_description varchar(5000) , add Dispositions_Exclusions varchar(1000) , add Link_documentation varchar(255) , add mental_illness varchar(100) , add Video varchar(255) , add Date_and_Description varchar(1000) , add Unique_ID_formula varchar(100) , add year varchar(100)

add year varchar(100) , add county varchar(100) , add race_or_ethnicity varchar(100) , add all_deaths varchar(100) , add arrest_related_deaths varchar(100) , add in_custody_deaths varchar(100) , add population varchar(100) , add all_deaths_per_100000 varchar(100) , add arrest_related_deaths_per_100000 varchar(100) , add in_custody_deaths_per_100000 varchar(100)

add county varchar(100) , add reporting_agency varchar(100) , add agency_full_name varchar(100) , add ncic_number_county varchar(100) , add ncic_number_city varchar(100) , add ncic_number_agency varchar(100) , add date_of_birth_mm varchar(100) , add date_of_birth_dd varchar(100) , add date_of_birth_yyyy varchar(100) , add race varchar(100) , add gender varchar(100) , add custody_status varchar(100) , add custody_offense varchar(100) , add date_of_death_yyyy varchar(100) , add date_of_death_mm varchar(100) , add date_of_death_dd varchar(100) , add custodial_responsibility_at_time_of_death varchar(100) , add location_where_cause_of_death_occurred varchar(100) , add facility_death_occured varchar(100) , add manner_of_death varchar(100) , add means_of_death varchar(100)

name varchar(100) , add age varchar(100) , add gender varchar(100) , add ace varchar(100) , add URL_image_victim varchar(100) , add Date varchar(100) , add Address_Incident varchar(100) , add City varchar(100) , add State varchar(100) , add Zip varchar(100) , add County varchar(100) , add Agency varchar(100) , add Cause varchar(100) , add description varchar(100) , add Official_disposition varchar(100) , add Criminal_Charges varchar(100) , add url_news_article_or_photo_of_official_document varchar(100) , add mental_illness varchar(100) , add Unarmed varchar(100) , add Alleged_Weapon varchar(100) , add Alleged_Threat_Level varchar(100) , add Fleeing varchar(100) , add Body_Camera varchar(100) , add WaPo_ID_If_in_WaPo_database varchar(100) , add Off_Duty_Killing varchar(100) , add Geography varchar(100) , add ID int
"""