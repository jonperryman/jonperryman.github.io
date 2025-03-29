console.log("script file enter");
const mf = {

    open_scrollable_div: function(template_name) {
        scrollable_div.style.display = "block";
        document.body.style.overflowY = "hidden";
        scrollable_div.innerHTML = close_x.innerHTML + template_name.innerHTML;
    },

    close_scrollable_div: function () {
        scrollable_div.style.display = "none";
        document.body.style.overflowY = "auto";
    },
    
    display_toc: function () {
        toc_content.style.display = 'block';
    },
	
    hide_toc: function () {
        toc_content.style.display = 'none';
    }
}
console.log("script file leave");