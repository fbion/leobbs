#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

opendir (DIR, "${lbdir}data/skin"); 
my @dirdata = readdir(DIR);
closedir (DIR);
my @skinselectdata = grep(/\.(cgi)$/i,@dirdata);
map(s/\.cgi$//is, @skinselectdata);
$skincount = @skinselectdata;
my $userskin = qq~<div class="menuitems">&nbsp;<a href="index.cgi?action=change_skin&thisprog=' + url + '&skin=leobbs"><font color=#000000>Ĭ�Ϸ��</font></a>&nbsp;</div>~;
for (my $i=0;$i<$skincount;$i++) {
    eval{ require "${lbdir}data/skin/$skinselectdata[$i].cgi"; };
    next if ($@);
    if ($cssname ne "") { $skinnames = $cssname; } else { $skinnames = $skinselectdata[$i]; }
    $skinselectdata[$i] = uri_escape($skinselectdata[$i]);
    $userskin.= qq~<div class="menuitems">&nbsp;<a href="index.cgi?action=change_skin&thisprog=' + url + '&skin=$skinselectdata[$i]"><font color=#000000>$skinnames</font></a>&nbsp;</div>~ if (lc($skinselectdata[$i]) ne "leobbs");
    $cssname = "";
}
eval{ require "${lbdir}data/skin/leobbs.cgi"; };
$userskins = qq~
<script>
var url = new String (window.document.location);
url = url.replace (/&/g, "%26");
url = url.replace (/\\\\//g, "%2F");
url = url.replace (/:/g, "%3A");
url = url.replace (/\\\\?/g, "%3F");
url = url.replace (/=/g, "%3D");
linkset[3]='$userskin'</script>~;
$skinselect = qq~<img src=\$imagesurl/images/fg.gif width=1> <span style=cursor:hand onMouseover="showmenu(event,linkset[3])" onMouseout="delayhidemenu()">��̳���&nbsp;</span>~;
open(FILE, ">${lbdir}data/skinselect.pl");
print FILE qq(\$userskins = qq~$userskins~;\n);
print FILE qq(\$skinselect = qq~$skinselect~;\n);
print FILE "1;\n";
close(FILE);
1;
