#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    $links = &HTML("$links");
    $output .= qq~
<img src=$imagesurl/images/none.gif height=5><br>
<SCRIPT>valigntop()</SCRIPT>
<table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellspacing=1 cellpadding=6 width=100%>
<tr><td bgcolor=$titlecolor colspan=7 $catbackpic><font color=$titlefontcolor><B>-=> ��ҳ����</td></tr>
<tr><td bgcolor=$forumcolortwo colspan=7 width=*><font color=$titlefontcolor>
<font color=$forumfontcolor>$links</td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
1;
