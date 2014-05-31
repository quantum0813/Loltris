---
layout: layout
title: Download
permalink: /download/
---

<!-- JS functions -->
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

<script text="text/javascript">
var os_name = getOSName();
var dl_link = getDLLink(os_name);
if (! dl_link) {
    document.write("Loltris has not been packaged for your platform, if Python/Pygame runs on your platform you can download the ");
    document.write('<a href="{{ site.github_page }}>source</a> and set it up yourself. Be warned that this code is not stable."');
} else {
    document.write("Download binary for " + os_name + " <a href='" + dl_link + "'>here</a><br>");
    document.write("<img src='" + getImageLink(os_name) + "'>");
    document.write("<br>If you would rather have the latest features, download the source <a href='{{ site.github_page }}'>here</a>. But be warned, ");
    document.write("this code is not stable. Therefore it is highly recommended that you download the binary instead.");
}
</script>

<!-- If javascript is disabled, we just give the user all the links -->
<noscript>
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
</noscript>
