training = {
    setup : function(template_name) {
        if (window.location.search == "?edit") {
            edit.setup();
            return;
        }

        if (template_name) {
            if (! window[template_name]) {
                alert("Invalid setup name " + template_name);
                return;
            }
            template_work.innerHTML = window[template_name].innerHTML;
        } else
            template_work.innerHTML = write_tutorial.innerHTML;

        training.screen_number = -1;
        var elements = document.getElementsByName('screen');
        for (var i = 0; i < elements.length; i++) {
            elements[i].id = 'screen' + i;
        };
        training.screen();
        if (navigator.platform != 'Win32' || navigator.vendor != 'Google Inc.')
            alert('Only tested with Chrome on Microsoft Windows. Unknown if this works on your browser.');
    },

    fail : function(el) {
        el.style.backgroundColor = 'pink';
        el.style.textDecoration = 'line-through'
        if (window.anim_fail != undefined)
            anim_fail();
    },

    success : function(el) {
        training.screen();  // next screen
        if (window.anim_success != undefined)
            anim_success();
    },

    screen : function( ) {
        setup = null;   // clear previous setup script

        training.screen_number += 1;
        screen_area.innerHTML = window['screen' + training.screen_number].innerHTML;

        var include = window['screen' + training.screen_number].getAttribute('include');
        if (include)      // Include another template
            screen_area.appendChild(window[include].content.cloneNode(true));

        var video_list = document.getElementsByTagName('video');
        for (var i=0; i<video_list.length; i++) {
            if (video_list[i].innerHTML == "") {
                video_list[i].innerHTML = '<source type="video/mp4" src="' + video_list[i].getAttribute('name') +
                     '"/>Your browser does not support MP4 video\'s, Please use a web browser that supports MP4.';
                video_list[i].loop = true;
                video_list[i].autoplay = true;
                video_list[i].height = '180';
                video_list[i].muted = true;
                video_list[i].controls = true;
                video_list[i].style.display = "block";
                video_list[i].style.margin = "auto";
            }
        }

        // replace answer tags with buttons tags
        var tags = document.getElementsByTagName('answer');
        var firstTag = true;
        while(tags.length > 0) {
            var tag = '<button class="answer" onclick="training.';
            if (firstTag) {
                tag = "<br/>" + tag;
                firstTag = false;
            }
            if (tags[0].getAttribute('correct') == "")   // correct attribute specified
                tag += 'success(this)';
            else
                tag += 'fail(this)';

            tag += ';">' + tags[0].innerText + '</button> ';
            tags[0].outerHTML = tag;  // replace the answer tag
        }

        // replace the question tag with reel HTML
        tags = document.getElementsByTagName('question');
        if (tags.length) {
            tags[0].outerHTML =
                '<div style="display: block; margin: auto;">'
                + '<div id="question" style="background-color: white; text-align: center; display: inline-block;">'
                + tags[0].innerHTML + '</div></div>';
            if (window.anim_screen != undefined)
                question.style.maxWidth = "5in";
        }

        if (setup)
            setup();   // call user's setup script
    }
}

edit = {

    setup: function() {
        window.onpointerdown = edit.down;
        window.ondragstart = edit.disableDrag;
        menu_area.innerHTML =
            '<select id="object" onchange="edit.objectSelected(event)" style="background-color: white;">'
            +   '<option id="resetObjectSelect" value="">select an object to modify</option>'
            + '</select>'
            + '<select onchange="edit.newObject(event)" style="background-color: white;">'
            +   '<option value="" id="resetNewObject">Add a new object</option>'
            +   '<option value="charliebrown.webp">Charlie brown</option>'
            +   '<option value="snoopy.webp">Snoopy</option>'
            +   '<option value="popeye.webp">Popeye</option>'
            +   '<option value="wall.webp">wall</option>'
            + '</select>'
        screen_area.innerHTML =
            '<div id="anim_screen" style="position: fixed; left: 0px; bottom: 0px; width: 15in; text-align: center;">'
            + '</div><script id="anim_script"></script>';
    },

    disableDrag: function(e) {
        e.preventDefault();  // Stop browser's built in drag facility
        return false;
    },

    down: function(e) {
        if (e.target.style.position == 'absolute' && e.target.nodeName == 'IMG') {
            edit.target = e.target;
            if ((e.target.x + e.target.width - e.clientX) < 30) {
                edit.function = 'grow';
                edit.offsetX = e.clientX - e.target.width;
            } else {
                edit.function = 'move'
                edit.offsetX = parseInt(e.clientX - e.target.x);
                edit.offsetY = parseInt(e.clientY - e.target.y);
            }
            window.onpointermove = edit.move;
            window.onpointerup = edit.up;
            window.onpointercancel = edit.up;
        }
    },

    up: function(e) {
        window.onpointermove = null;
        window.onpointerup = null;
        window.onpointercancel = null;
    },

    move: function(e) {
        if (edit.function == 'grow') {
            edit.target.width = e.clientX - edit.offsetX;
            if (edit.target.width < 50)
                edit.target.width = 50;
        } else {
            edit.target.style.left = (e.clientX - edit.offsetX) + 'px';
            edit.target.style.top = (e.clientY - edit.offsetY) + 'px';
        }
    },

    newAnimation: function(e) {
        var name = prompt("Name of new animation","cancel");
        if (name == "cancel")
            return;  // cancel new animation request

        if (localStorage.getItem(name)) {
            alert(name + " already exists - use edit");
            return;
        }

        // close previous edit session
        if (edit.name)
            localStorage.setItem(edit.name, anim_screen.outerHTML);

        edit.editName = name;
    },

    newObject: function(e) {
        do {
            var id = prompt("Unique name to identify this object","none");
        } while (id == "none");
        var work = anim_screen.insertBefore(document.createElement("image"),null);
        work.outerHTML = '<img id="' + id + '" src="' + e.srcElement.value
            + '" width="100" style="position: absolute; bottom: 0px;" />';
        resetNewObject.selected = true;
    },

    objectSelected: function(e) {
        if (edit.selectedObject != undefined)
            edit.selectedObject.style.zIndex = edit.savedZIndex;
        edit.selectedObject = window[e.srcElement.value];
        edit.savedZIndex = edit.selectedObject.style.zIndex;
        edit.selectedObject.style.zIndex = 9999;
        edit.savedBorder = edit.selectedObject.style.border;
        edit.selectedObject.style.border = 3;
        resetObjectSelect.selected = true;
    }
}