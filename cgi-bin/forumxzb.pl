#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

$xzb="";
if (-e "${lbdir}boarddata/xzb$inforum.cgi") {
    open (FILEX, "${lbdir}boarddata/xzb$inforum.cgi");
    my @xzbdata = <FILEX>;
    close (FILEX);
    if (-e "${lbdir}boarddata/xzbs$inforum.cgi") {
	open(FILEX,"${lbdir}boarddata/xzbs$inforum.cgi");
	$xzbcount=<FILEX>;
	close(FILEX);
    }
    if ($xzbcount eq "") { $xzbcount= 0; }
    if ($xzbcount>=$#xzbdata) { $xzbcount = 0; } else { $xzbcount++; }
    $xzbdata[$xzbcount] =~ s/^����������\t//isg;
    (my $title, my $postid, my $msg, my $posttime)=split(/\t/,$xzbdata[$xzbcount]);
    open(FILEX,">${lbdir}boarddata/xzbs$inforum.cgi");
    print FILEX $xzbcount;
    close(FILEX);
    if ($title ne "") {
	my $temppostid = $postid;
        $temppostid    =~ s/ /\_/isg;
	$temppostid    =~ tr/A-Z/a-z/;
        my $titletemps = &lbhz($title,35);
        $xzb = qq~&nbsp;С�ֱ�: <img src=$imagesurl/images/icon.gif width=14> <span style=cursor:hand onClick="javascript:openScript('xzb.cgi?action=view&forum=$inforum&id=$xzbcount',420,320)" title="$title"><font color=$fonthighlight>$titletemps</font></span> -- <span style=cursor:hand onClick=javascript:O9('~ . uri_escape($temppostid) . qq~')>$postid</span>~;
	$xzb = qq~<B>[<a href=xzbadmin.cgi?forum=$inforum>����</a>]</b>$xzb~ if (($membercode eq "ad")||($membercode eq "smo")||($inmembmod eq "yes"));
    }
}
1;
