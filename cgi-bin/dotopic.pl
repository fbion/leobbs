#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

if (-e "${lbdir}boarddata/jinghua$inforum.cgi") {
    open(FILE, "${lbdir}boarddata/jinghua$inforum.cgi");
    my @jhdatas = <FILE>;
    close(FILE);
    $jhdata = join("\_",@jhdatas);
    $jhdata = "\_$jhdata\_";
    $jhdata =~ s/\W//isg;
} 

if (($category=~/childforum-[0-9]+/)&&($indexforum ne "no")) {
    $tempforumno=$category;
    $tempforumno=~s/childforum-//;
    $filetoopen = "${lbdir}forum$tempforumno/foruminfo.cgi";
    open(FILE, "$filetoopen");
    my $forums = <FILE>;
    close(FILE);
    (undef, undef, undef, $tempforumname, undef) = split(/\t/,$forums);
    $addlink  = qq~ �� <a href=forums.cgi?forum=$tempforumno>$tempforumname</a>~;
}
$forumdescription = &HTML("$forumdescription");
$forumdescription =~ s/<BR>//isg;
$forumdescription =~ s/<P>//isg;

if ($indexforum ne "no") {
    $tempoutput = qq~<table width=\$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> $forumdescription</td></tr></table><table width=\$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=\$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr height=25><td bgcolor=\$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=\$navfontcolor><a href=leobbs.cgi>$boardname</a>$addlink �� <a href=forums.cgi?forum=$inforum>$forumname</a> [<a href=forums.cgi?forum=$inforum&show=\$inshow>����</a>] �� �����topictitletempshow��jhimage</td><td bgcolor=\$navbackground align=right valign=bottom>\$uservisitdata</td></tr></table></td></tr></table>~;
} else {
    $tempoutput = qq~<table width=\$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> $forumdescription</td></tr></table><table width=\$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=\$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr height=25><td bgcolor=\$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=\$navfontcolor><a href=forums.cgi?forum=$inforum>$forumname</a> [<a href=forums.cgi?forum=$inforum&show=\$inshow>����</a>] �� �����topictitletempshow��jhimage</td><td bgcolor=\$navbackground align=right valign=bottom>\$uservisitdata</td></tr></table></td></tr></table>~;
}
if (open(FILE,"${lbdir}data/notshowsignature.cgi")){ 
    $notshowsignaturemember = <FILE>; 
    close(FILE); 
} 
$notshowsignaturemember=~s/^\t//; 
$notshowsignaturemember=~s/\t$//; 
$notshowsignaturemember="\t$notshowsignaturemember\t";

if (!(-e "${lbdir}cache/forumstopic$inforum.pl")) {
    open (FILE, ">${lbdir}cache/forumstopic$inforum.pl");
    print FILE qq~\$notshowsignaturemember=qq($notshowsignaturemember);\n~;
    $tempoutput =~ s/\\/\\\\/isg;
    $tempoutput =~ s/~/\\\~/isg;
    $tempoutput =~ s/\$/\\\$/isg;
    $tempoutput =~ s/\@/\\\@/isg;
    $tempoutput =~ s/\\\$/\$/isg;
    print FILE qq(\$tempoutput =qq~$tempoutput~;\n);
    $tempoutput =~ s/\$/\\\$/isg;
    $tempoutput =~ s/\\\~/~/isg;
    $tempoutput =~ s/\\\$/\$/isg;
    $tempoutput =~ s/\\\@/\@/isg;
    $tempoutput =~ s/\\\\/\\/isg;
    print FILE qq~\$jhdata=qq($jhdata);\n~;
    print FILE "1;\n";
    close(FILE);
}

$tempoutput =~ s/\$inshow/$inshow/isg;
$tempoutput  =~ s/\$uservisitdata/$uservisitdata/isg;
$tempoutput  =~ s/\$tablewidth/$tablewidth/isg;
$tempoutput  =~ s/\$navborder/$navborder/isg;
$tempoutput  =~ s/\$navbackground/$navbackground/isg;
$tempoutput  =~ s/\$navfontcolor/$navfontcolor/isg;
$jhdata = "" if ($usejhpoint ne "yes");

1;
