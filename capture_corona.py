""" 
    Program to extract corona virus daily new cases and deaths from worldometers.

    Python3 required to run this program.
    You will need to modify os.command() below if you are not running under Linux 
    or not using Chrome web browser. Any web browser should work fine to create 
    the CSV data in the download directory.

    Change variables countries and states to the places you want to see.
"""

countries = [ "france", "italy", "spain", "germany", "mexico", "sweden",
    "finland", "norway", "denmark", "belgium", "brazil", "argentina", "uk", "colombia",
    "poland", "belgium", "iraq"]
states = ["california","texas","new-york","new-jersey","florida","texas",
    "illinois", "ohio", "georgia", "michigan", "wisconsin", "pennsylvania", 
    "arizona", "louisiana", "massachusetts", "south-carolina"]

import requests
import os

def get_corona_data(directory,locations):
    for location in locations:
        print("downloading worldometer data for", location)
        p = requests.get("https://www.worldometers.info/coronavirus/" + directory + "/"+location)
        p = p.content.decode()
        p = p.split("Highcharts.chart(")
        p.pop(0)     # only process chart calls
        for chart in p:
            file.write("\ngetChartData('"+location+"', ")
            file.write(chart.split("</script")[0])

file = open("capture_corona.html","w")
file.write("""
    <html>
    <body>
    <div id='download_progress'>Extracting data for:</div>
    <a id='download' href='data:text/plain;charset=utf-8,' download='capture_corona.csv'></a>

    <script>

    var downloaded_data = '';

    function q(data) { // return quoted string
        return '\\'' + data + '\\'';
    }

    function getChartData(location, description, data) {
        download_progress.innerHTML += '<br/>\\n' + location + ' ' 
            + description + ' title=' + data.title.text;
        if (description == 'graph-cases-daily' || description == 'graph-deaths-daily') {
            if (true) {   // create CSV data
                if (downloaded_data == '') 
                    downloaded_data = '\\'location\\',\\'description\\',\\'title\\',\\'name\\',' 
                        + q(data.xAxis.categories.join('\\', \\'')) + '\\n';     // labels 
                downloaded_data += q(location) + ', '  //  daily
                    + q(description) + ', '
                    + q(data.title.text) + ', '
                    + q(data.series[0].name) + ', ' 
                    + data.series[0].data + '\\n'; 
                downloaded_data += q(location) + ', '  //  3 day running average
                    + q(description) + ', '
                    + q(data.title.text) + ', '
                    + q(data.series[1].name) + ', ' 
                    + data.series[1].data + '\\n'; 
                downloaded_data += q(location) + ', '  //  7 day running average
                    + q(description) + ', '
                    + q(data.title.text) + ', '
                    + q(data.series[2].name) + ', ' 
                    + data.series[2].data + '\\n'; 
                download_progress.innerHTML += ' <span style=\\'background-color: lightgreen;\\'>completed</span>';
            
            } else {  // graphing data instead of creating csv data
                if (downloaded_data == '') 
                    downloaded_data = 'ylabel = [' + q(data.xAxis.categories.join('\\', \\'')) + '];\\n';     // labels 
                downloaded_data += 'graphdata(' + q(location) + ', ' 
                    + q(description) + ', '
                    + q(data.title.text) + ', '
                    + q(data.series[2].name) + ', '    // 7 day running average
                    + '[' + data.series[2].data + ']\\n'
                    + ');\\n\\n'; 
            }

        } else {  // ignore this file
            download_progress.innerHTML += ' <span style=\\'background-color: pink;\\'>Skipped</span>';
        }
    }
    """)

get_corona_data("country", countries)
get_corona_data("usa", states)

file.write("""
    download.href += downloaded_data;
    download.click();
    </script>
    </body>
    </html>""")

file.close()

os.system("google-chrome capture_corona.html")