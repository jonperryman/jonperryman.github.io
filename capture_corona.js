/* 
    Capture worldometer corona data manually for the previous day.
    
    To run this javascript:    
    1. open the worldometer web page for the corona data you wish collect. 
    2. Open deveveloper tools. 
    3. Select the source tab.
    4. Select "snippets". This may be hidden. Click the ">>" where you see "page source >>".
    5. If this is the first time you run this, then click "new snippet" and 
       give it a name. In the snippet area, paste a copy of this javascript.
    6. Right mouse click on the snippet name and click on "run".
    7. A CSV download file will be created.
    8. For additional locations, change to that location and repeat step 6.
*/

function capture_file(filename, text) {
    var a = document.createElement('a');
    a.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    a.setAttribute('download', filename);

    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        a.dispatchEvent(event);
    }
    else {
        a.click();
    }
}

function cnvtCSV(date, popColumn, data) {
    if (data[10].innerText && !isNaN(data[10].innerText.split(",").join("")))
        var work = (Math.round(1000000 * Number( data[3].innerText.split(",").join("")) / Number( data[popColumn].innerText.split(",").join("")))).toString() + ", "
            + (Math.round(1000000 * Number( data[5].innerText.split(",").join(""))/ Number( data[popColumn].innerText.split(",").join("")))).toString() + ", "
            + date; 
    else
        var work = "-999999, -999999" + ", " + date;

    for (var i=1; i<data.length; i++) { // omit row number
        work += ", " + data[i].innerText.split(",").join("");
    }
    work = work.split("\n").join("").split("\r").join("");
    return work;
}

function capture() {

    var tab = document.getElementsByTagName("table")[1];  // yesterdays covid table
    var work = new Date();
    if (work.getHours() < 17)
        work.setDate(work.getDate()-1);
    else if (work.getHours() < 19)
        throw "Covid database updates from 5 to 7.";

    work = work.toLocaleDateString().split("/")
    var date = work[2]+"-"+work[0]+"-"+work[1];
    var filename = "_"+work[0]+work[1]+".csv";

    var thead = tab.tHead.getElementsByTagName('th');
    var popColumn = thead.length-1;
    for (; popColumn>0 && thead[popColumn].innerText!="Population"; popColumn--) {}
    if (popColumn == 0) 
        throw "Population column not found";
    var data = cnvtCSV(date, popColumn, thead);

    var work = data.split("USAState");
    if (work.length == 2) {
        var work2 = ", TotalCases, NewCases, TotalDeaths, NewDeaths, TotalRecovered, ActiveCases, Tot Cases/1M pop, Deaths/1M pop, TotalTests, Tests/ 1M pop, Population, Projections";
        if (work[1] != work2)
            throw("Invalid columns for covidUsa.csv: \n" + work[1] + "\n" + work2);
        filename = "covidUsa"+filename;  
    } else {
        work = data.split("CountryOther");
        if (work.length != 2)
            throw("Invalid title: " + data)
        var work2 = ", TotalCases, NewCases, TotalDeaths, NewDeaths, TotalRecovered, ActiveCases, SeriousCritical, Tot Cases/1M pop, Deaths/1M pop, TotalTests, Tests/1M pop, Population, Continent";
        if (work[1] != work2) 
            throw("Invalid columns for covidWorld.csv: \n" + work[1] + "\n" + work2);
        filename = "covidWorld"+filename;
    }

    var rows = tab.tBodies[0].getElementsByTagName("tr");
    for (var i=1; i<rows.length; i++) {  
        data += "\n" + cnvtCSV(date, popColumn, rows[i].getElementsByTagName("td"));
    } 
    capture_file(filename, data);    
}

capture();