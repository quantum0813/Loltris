---
layout: layout
title: Download
permalink: /download/
---

<!-- Misc. JS functions -->
<script type="text/javascript">
function getOSName() {
    if (navigator.platform.indexOf("Win")!=-1) {
        return "Windows";
    } else if (navigator.platform.indexOf("Mac")!=-1) {
        return "MacOS";
    } else if (navigator.platform.indexOf("Linux")!=-1) {
        return "Linux";
    } else if (navigator.platform.indexOf("BSD")!=-1) {
        return "BSD";
    }
}

function getDLLink(os_name) {
    switch(os_name) {
        case "Windows":
            return "{{ site.baseurl }}/assets/Software-Packages/Loltris_Win32.zip";
        case "Linux":
            return "{{ site.baseurl }}/assets/Software-Packages/Loltris_Linux32.tar.bz2";
        default:
            return null;
    }
}

function imageExists(url) {
   var img = new Image();
   img.src = url;
   return img.height != 0;
}

function getImageLink(os_name) {
    return "{{ site.baseurl }}/assets/images/platforms/" + os_name + ".png";
}
</script>

<!-- Give the user an appropriate link depending on the users platform -->
<script text="text/javascript">
var os_name = getOSName();
var dl_link = getDLLink(os_name);
if (! dl_link) {
    document.write("Loltris has not been packaged for your platform, if Python/Pygame runs on your platform you can download the ");
    document.write('<a href="{{ site.github_page }}>source</a> and set it up yourself. Be warned that this code is not stable."');
} else {
    document.write("<p>Download binary for " + os_name + " <a href='" + dl_link + "'>here</a></p>");
    document.write("<img src='" + getImageLink(os_name) + "'>");
    document.write("<p>If you would rather have the latest features, download the source <a href='{{ site.github_page }}'>here</a>. But be warned, ");
    document.write("this code is not stable. Therefore it is highly recommended that you download the binary instead.</p>");
}
</script>

<!-- If javascript is disabled, we just give the user all the links -->
<div id="download_list" class="noscript">
    <p>
    <ul>
        <li>Windows (32-bit)
        <ul>
            <li><a href="/Loltris/assets/Software-Packages/Loltris_Win32.zip">Download</a></li>
        </ul>
        </li>
        <li>Linux (32-bit)
        <ul>
            <li><a href="/Loltris/assets/Software-Packages/Loltris_Linux32.tar.bz2">Download</a></li>
        </ul>
        </li>
        <li>Experimental Source+Data (multi-platform, if you know how to set it up)
        <ul>
            <li><a href="https://github.com/UndeadMastodon/Loltris">Download</a></li>
        </ul>
        </li>
    </ul>
    </p>
</div>

<!-- Create the hidden list of downloads (can be enabled by clicking a button) -->
<script text="text/javascript">
// Write the noscript HTML to the document, but hide it
var text = document.getElementById("download_list").innerHTML;
document.write("<div id='hidden_download_list' class='hidden'>" + text + "</div>");

function showDownloadList() {
    // Show the list, while hiding the button
    document.getElementById("hidden_download_list").className = "visible";
    document.getElementById("show_downloads_button").className = "hidden";
}

document.write("<p><input id='show_downloads_button' type='button' value='Show all downloads' onclick='showDownloadList();'></p>");
</script>

<script text="text/javascript">
// If javascript is enabled, this will run. This piece of code hides the contents of
// all elements that are part of the noscript class. Chrome/Chromium does not interpret
// text inside <noscript> tags as markup, this is a workaround.
var elems = document.getElementsByClassName("noscript");
for(var i = 0; i < elems.length; i++) {
    elems[i].className = "hidden";
}
</script>
