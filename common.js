document.shared = {} // shared variables to eliminate need for global variables

// Each menu item needs ONCLICK= 
function setupMenu() {
    var menus = document.getElementsByClassName("menu");
    for (var i=0; i<menus.length; i++) {
        var menuList = menus[i].getElementsByTagName("li");
        for (var j=0; j<menuList.length; j++) 
            if (menuList[j].childElementCount == 0)
                menuList[j].onclick = loadPageData;
    }
}

// screen size has changed - modify document to fix page correctly
function setupDisplay() {
    var width = window.innerWidth;  // returns px increments
    var maxWidth = 96 * 8.5;  // pixels in 8.5 inches

    if (width > maxWidth) { // screen is larger than needed
        // center the display and reduce size for readability
        document.getElementById('pageArea').style.left = ((width - maxWidth) / 2) + 'px';
        document.getElementById('pageArea').style.width = maxWidth + 'px';
        document.getElementById('pageArea').style.position = 'fixed';

        // make page data area use a scroll bar if needed and fix header at top
        document.getElementById('pageData').style.height
            = (window.innerHeight - document.getElementById('pageData').offsetTop - 10) + 'px';

        // hide photo and make contact info look better 
        document.getElementById('hdrPhoto').style.visibility = '';
        document.getElementById('hdrPhoto').style.height = '';
        document.getElementById('hdrInfo').style.float = 'right';

    } else { // smaller screen sizes
        // make display scrollable
        document.getElementById('pageArea').style.left = '';
        document.getElementById('pageArea').style.width = '';
        document.getElementById('pageArea').style.position = '';

        // remove scroll bar for non-header area and make header scrollable
        document.getElementById('pageData').style.height = '';

        // hide photo and make contact info look better 
        document.getElementById('hdrPhoto').style.visibility = 'hidden';
        document.getElementById('hdrPhoto').style.height = '0px';
        document.getElementById('hdrInfo').style.float = 'left';
    }
}

// New page requested
function loadPageData() {
    if (this.onclick == null) {  // called from setup() - initial page setup
        if (window.location.href.indexOf('page=') < 0) 
            currentPage = 'Home.html';
        else
            currentPage = window.location.href.substr(
                window.location.href.indexOf('page=')+5) + '.html';
    } else
        currentPage = this.innerText.trim().replace(/[^a-zA-Z0-9]/g, '_') + '.html';
    currentPage += '?_=' + new Date().getTime(); // ignore caches
    currentPage = currentPage.toLowerCase();

    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = processPageData;

    document.getElementById('pageData').innerHTML = 'Loading page: ' + currentPage;
    xhttp.open('GET', currentPage, true);
    xhttp.send();
}

// all elements with class="code" are considered code snippets.
// This function modifies these elements so they are easier to
// read and use.
function processPageData() {

    document.getElementById('pageData').innerHTML = '<h1>web page ' + currentPage
        + ' is being downloaded - readystate: ' + this.readyState 
        + ' status: ' + this.status + '</h1>';
    if (this.readyState != 4) 
        return;
    if ((this.status == 0 && this.response == '') ||
        this.status != 200) {
        document.getElementById('pageData').innerHTML =
        '<h1>This site is still under construction. Sorry for any inconvenience.</h1>'
        +   '<h1>Failed to load: web page '
        + currentPage
        + ' readystate: ' + this.readyState 
        + ' status: ' + this.status + '</h1>';
        return;
    }

    // modify the code elements
    var codeElements = this.responseText.split('<code');
    var pageData = "<br/>" + codeElements.shift();  // first entry cannot be <code>
    while (codeElements.length) {

        var work = codeElements[0].indexOf('>')+1;
        pageData += '\n<p><div class="codeTable"' 
            + codeElements[0].substr(0, work)  // Change code to table element
            + '<table><thead></thead><tbody><tr>\n<td>'; // code table definition
        
        var lines = codeElements[0].substr(work).split('</code>');
        if (lines.length == 1) {
            lines = (lines[0] + '<code' + codeElements[1]).split('</code>');
            if (lines.length == 1) {
                lines.push('***** missing </code> ******\n');
            }    
            codeElements.shift();  // remove line already processed
        }
        codeElements.shift();  // remove line already processed

        var codeEnd = lines.pop(); // terminated by last </code> 
        
        lines = lines.join('</code>')   // </code> is part of the code snippet
            .replace(/&/g, '&amp;')   // display &
            .replace(/>/g, '&gt;')    // display >
            .replace(/</g, '&lt;')    // display <
            .split('\n');             // For <pre> we need to process each line

        // remove first and last lines if blank
        if (lines[0].trimLeft() == '')
            lines.shift();
        if (lines[lines.length - 1].trimLeft() == '')
            lines.pop();

        // left justify code snippets using first line as justification start position
        // as <tr><td>???</td></tr>.
        var leadingSpaceCount = lines[0].length - lines[0].trimLeft().length;    
        for (var j = 0; j < lines.length; j++) {
            if (lines[j].substr(0, leadingSpaceCount).trimLeft() == '')
                pageData += lines[j].substr(leadingSpaceCount);
            else
                pageData += lines[j].trimLeft();  // not empty, just clear all leading space
            pageData += '\n';
        }

        pageData += '</td></tr></tbody></table></div></p>\n' // close this code snippet
            + codeEnd;     // text after </code>
    }

    document.getElementById('pageData').innerHTML = pageData;

    // Check each code element for _title attribute (my special attribute)
    // and use it for the title of this code snippet
    var codeElements = document.getElementsByClassName('codeTable');
    for (var i=0; i<codeElements.length; i++) {
        if (codeElements[i].hasAttribute('_title')) 
            codeElements[i].getElementsByTagName('thead')[0].innerHTML 
                = '<th>'+ codeElements[i].getAttribute('_title') + '</th>';
    }
}

let speakMsg = new SpeechSynthesisUtterance();

function findVoice(voice) {
	console.log('process', voice.name);
	return /.*Aria.*English.*United States.*/.test(voice.name);
}

function speakButton() {
	let buttonText = document.getElementById('speakButton').innerText;
	if (buttonText == 'Pause') {
		document.getElementById('speakButton').innerText = 'Pausing';
		window.speechSynthesis.pause();
	}
	else if (buttonText == 'Resume') {
		document.getElementById('speakButton').innerText = 'Resuming';
		window.speechSynthesis.resume();
	}
	else if (buttonText == 'Read text aloud') {
		document.getElementById('speakButton').innerText = 'Starting speech';
		if (speakMsg.text == '') {
			speakMsg.text = document.getElementsByClassName("WordSection1")[0].innerText;
			speakMsg.onend = (event) => {
				document.getElementById('speakButton').innerText = 'Read text aloud';
			}
			speakMsg.onpause = (event) => {
				document.getElementById('speakButton').innerText = 'Resume';
			}
			speakMsg.onresume = (event) => {
				document.getElementById('speakButton').innerText = 'Pause';
			}
			speakMsg.onstart = (event) => {
				document.getElementById('speakButton').innerText = 'Pause';
			}
			speakMsg.voice = window.speechSynthesis.getVoices().find(findVoice);
		}
		window.speechSynthesis.speak(speakMsg);
	}	
}
