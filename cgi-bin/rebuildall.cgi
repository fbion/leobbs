#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

BEGIN {
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use LBCGI;
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
require "rebuildlist.pl";
$|++;

$thisprog = "rebuildall.cgi";

$query = new LBCGI;

$nextforum     = $query -> param('nextforum');
$action        = $query -> param("action");
$action        = &cleaninput("$action");
$nextforum     = 0 if ($nextforum eq "");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;

if ($action eq "process") {
    &getmember("$inmembername","no");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
        $filetoopen = "$lbdir" . "data/allforums.cgi";
        open(FILE, "$filetoopen");
        @allforums = <FILE>;
        close(FILE);
        $size=@allforums;

        ($forumid, $no) = split(/\t/,$allforums[$nextforum]);
        if ($forumid ne "") {
	    my $info = rebuildLIST(-Forum=>"$forumid");
            ($threadcount,$topiccount) = split (/\|/,$info);
            $threadcount = 0 if ($threadcount<0);
            $topiccount  = 0 if ($topiccount <0);

            open(FILE, "${lbdir}boarddata/listno$forumid.cgi");
            $topicid = <FILE>;
            close(FILE);
            chomp $topicid;
	    my $rr = &readthreadpl($forumid,$topicid);
	    (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp) = split (/\t/,$rr);
	    if (-e "${lbdir}boarddata/foruminfo$forumid.cgi") {
                open(FILE, "+<${lbdir}boarddata/foruminfo$forumid.cgi");
                ($no, $threads, $posts, $todayforumpost, $no) = split(/\t/,<FILE>);
                $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
	        $lastposter = $startedby if ($lastposter eq "");
	        seek(FILE,0,0);
                print FILE "$lastforumpostdate\t$threadcount\t$topiccount\t$todayforumpost\t$lastposter\t\n";
                close(FILE);
            } else {
                open(FILE, ">${lbdir}boarddata/foruminfo$forumid.cgi");
                print FILE "$lastforumpostdate\t$threadcount\t$topiccount\t$todayforumpost\t$lastposter\t\n";
                close(FILE);
            }
	    $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	    if ($todayforumpost eq "") { $todayforumpost = "0|" };
	    open(FILE, ">${lbdir}boarddata/forumposts$forumid.pl");
	    print FILE "\$threads = $threadcount;\n\$posts = $topiccount;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);
	}
	$nextforum++;
	if ($nextforum > $size){
            print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / �ָ�-���¼���������̳</b></td></tr>
		<tr><td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>�ָ�-���¼���������̳�Ѿ����!</b></td></tr>
	    );
    opendir (CATDIR, "${lbdir}cache");
    @dirdata = readdir(CATDIR);
    closedir (CATDIR);
    @dirdata = grep(/forumcache/,@dirdata);
    foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }

	} else {
	    print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / �ָ�-���¼���������̳</b></td></tr>
		<tr><td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>�ָ�-���¼���������̳</b></td></tr>
		<td bgcolor=#ffffff valign=middle align=left colspan=2>
		<font color=black><b><br><br><br>������...<br>
		������:$threadcount<br>
		�ظ���:$topiccount<BR></b><BR><BR>
		<a href=$thisprog?action=process&nextforum=$nextforum>��������û���Զ�ת�룬����������</a><BR>
		</td></tr>
		<meta http-equiv="refresh" content="2; url=$thisprog?action=process&nextforum=$nextforum">
	    );
	}
    }
    else {
	&adminlogin;
    }
}
else {
    &getmember("$inmembername","no");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
	print qq(
	<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
	<b>��ӭ������̳�������� / �ָ�-���¼���������̳</b></td></tr><tr>
	<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
	<font color=#333333><b>�ָ�-���¼���������̳</b></td></tr>
	<form action="$thisprog" method="post">
	<input type=hidden name="action" value="process">
	<tr><td bgcolor=#FFFFFF valign=middle colspan=2>
	<font color=#000000><b>��ע��:</b><br>�˹��̽��ķѴ��� CPU ʱ���ϵͳ��Դ�������򲻵��ѣ���Ҫ���ñ����ܣ�</td></tr>
	<tr><td bgcolor=#EEEEEE valign=middle align=center colspan=2>
	<input type=submit name=submit value=�ύ></td></form></tr></table></td></tr></table>
	);
    }
    else {
	&adminlogin;
    }
}
print qq~</td></tr></table></body></html>~;
exit;
