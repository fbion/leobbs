#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    $line1 = &HTML($line1);
    $line1 =~ s/\n/<BR>/isg;
    $output .= qq~
    <BR><BR>
    <center><img src="$imagesurl/myimages/$boardlogo" border=0><BR><BR><BR>
    <TABLE cellSpacing=0 cellPadding=0 width=400 height=350><TR><TD><IMG src=$imagesurl/images/top_l.gif></TD><TD background=$imagesurl/images/top_c.gif></TD><TD><IMG src=$imagesurl/images/top_r.gif></TD></TR><TR><TD vAlign=top background=$imagesurl/images/center_l.gif></TD><TD bgcolor=#fffff1 width=100% height=100% valign=top>
    <b><font color=#FF0000>$boardname����ά���У����Ժ��ٷ���...</b></font>
    <BR><BR>$line1<BR><br>
    <TD vAlign=top background=$imagesurl/images/center_r.gif></TD></TR><TR><TD vAlign=top><IMG src=$imagesurl/images/foot_l1.gif ></TD><TD background=$imagesurl/images/foot_c.gif></TD><TD align=right><IMG src=$imagesurl/images/foot_r.gif></TD></TR></TABLE><BR>
    <br><br><br>
~;
    print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
    &output("$boardname����ά���У����Ժ��ٷ���...",\$output);
    exit;
1;
