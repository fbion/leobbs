#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

if ($indexforum ne "no") {
    if ($category=~/childforum-[0-9]+/) {
	$tempforumno=$category;
	$tempforumno=~s/childforum-//;
	open(FILE, "${lbdir}forum$tempforumno/foruminfo.cgi");
	$forums = <FILE>;
	close(FILE);
	(undef, undef, undef, $tempforumname, undef) = split(/\t/,$forums);
	$addlink  = qq~ �� <a href=forums.cgi?forum=$tempforumno>$tempforumname</a>~;
    }
    $forumdescription = &HTML("$forumdescription");
    $forumdescription =~ s/<BR>//isg;
    $forumdescription =~ s/<P>//isg;
    $titleoutput = qq~<table width=\$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> $forumdescription</td></tr></table><table width=\$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=\$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr height=25><td bgcolor=\$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=\$navfontcolor><a href=leobbs.cgi>$boardname</a>$addlink �� <a href=forums.cgi?forum=$inforum>$forumname</a> �� �����̳����</td><td bgcolor=\$navbackground align=right valign=bottom>\$uservisitdata</td></tr></table></td></tr></table>~;
}
if (!(-e "${lbdir}cache/forumshead$inforum.pl")) {
    $titleoutput =~ s/\\/\\\\/isg;
    $titleoutput =~ s/~/\\\~/isg;
    $titleoutput =~ s/\$/\\\$/isg;
    $titleoutput =~ s/\@/\\\@/isg;
    $titleoutput =~ s/\\\$/\$/isg;
    open (FILE, ">${lbdir}cache/forumshead$inforum.pl");
    print FILE qq(\$titleoutput = qq~$titleoutput~;\n);
    print FILE "1;\n";
    close (FILE);
    $titleoutput =~ s/\$/\\\$/isg;
    $titleoutput =~ s/\\\~/~/isg;
    $titleoutput =~ s/\\\$/\$/isg;
    $titleoutput =~ s/\\\@/\@/isg;
    $titleoutput =~ s/\\\\/\\/isg;
}
$titleoutput  =~ s/\$uservisitdata/$uservisitdata/isg;
$titleoutput  =~ s/\$tablewidth/$tablewidth/isg;
$titleoutput  =~ s/\$navborder/$navborder/isg;
$titleoutput  =~ s/\$navbackground/$navbackground/isg;
$titleoutput  =~ s/\$navfontcolor/$navfontcolor/isg;
1;
