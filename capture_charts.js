function capture_file(filename, text) {
    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    pom.setAttribute('download', filename);

    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
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

function captureChart(chartTitle, chartData) {
    var work = ["graph-deaths-daily",
                "graph-cases-daily"
                ].indexOf(chartTitle);
    if (work>=0) {
        console.log("process title",chartTitle,"data",chartData);
        chartData.series[0].name;
        chartData.series[0].data;
    } else 
        console.log("ignoring chart", chartTitle)
}

function capture() {    
    var tab = document.getElementsByTagName("script");  // yesterdays covid table
    for (var i=0; i<tab.length; i++) {
        if (tab[i].innerText.length>0) {
            var work = tab[i].innerText.split("Highcharts.chart")
            for (var j=1; j<work.length; j++) {
                var f = new Function('', 'captureChart'+work[j]);
                f();
            } 
        }
    }

    #var filename = "_"+work[0]+work[1]+".csv";

    var thead = tab.tHead.getElementsByTagName('th');
    var popColumn = thead.length-1;
    for (; popColumn>0 && thead[popColumn].innerText!="Population"; popColumn--) {}
    if (popColumn == 0) 
        throw "Population column not found";
    var data = cnvtCSV(date, popColumn, thead);

    var work = data.split("USAState");
    if (work.length == 2) {
        if (work[1] != ", TotalCases, NewCases, TotalDeaths, NewDeaths, TotalRecovered, ActiveCases, Tot Cases/1M pop, Deaths/1M pop, TotalTests, Tests/1M pop, Population, Projections")
            throw("Invalid columns for covidUsa.csv: " + data);
        filename = "covidUsa"+filename;  
    } else {
        work = data.split("CountryOther");
        if (work.length != 2)
            throw("Invalid title: " + data)
        if (work[1] != ", TotalCases, NewCases, TotalDeaths, NewDeaths, TotalRecovered, ActiveCases, SeriousCritical, Tot Cases/1M pop, Deaths/1M pop, TotalTests, Tests/1M pop, Population, Continent") 
            throw("Invalid columns for covidWorld.csv: " + data);
        filename = "covidWorld"+filename;
    }

    var rows = tab.tBodies[0].getElementsByTagName("tr");
    for (var i=1; i<rows.length; i++) {  
        data += "\n" + cnvtCSV(date, popColumn, rows[i].getElementsByTagName("td"));
    } 
    capture_file(filename, data);    
}

capture();