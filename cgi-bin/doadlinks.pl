#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    $adlinks = &HTML("$adlinks");
    $adlinks =~ s/\$imagesurl/$imagesurl/isg;
    $adlinks =~ s/\$tablebordercolor/$tablebordercolor/isg;
    $adlinks =~ s/\$forumcolorone/$forumcolorone/isg;
    $adlinks =~ s/\$forumcolortwo/$forumcolortwo/isg;
    $adlinks =~ s/\[br\]/\n/isg;
    $adlinks = "<table cellpadding=0 cellspacing=0 width=$tablewidth align=center><tr><td>$adlinks</td></tr></table>";
1;
