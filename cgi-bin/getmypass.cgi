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
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "getmypass.cgi";
$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}

$inmembername  = $query -> param("username");
$inpassword    = $query -> param("password");
$inmembername =~ s/\_/ /isg;

$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
&error("�޸�����&����У������벻Ҫ�����޸ģ�") if (($inmembername eq "")||($inpassword eq ""));

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "����") {
    $inmembername = "����";
    $userregistered = "no";
    &error("�޸�����&�����û�������Ϊ�գ�");
}
else {
    &getmember("$inmembername","no");
    &error("�޸�����&���󣬴��û������ڣ�") if ($userregistered eq "no");
}

opendir (DIRS, "${lbdir}$msgdir");
my @files = readdir(DIRS);
closedir (DIRS);
@files = grep(/\.cgi$/i, @files);
foreach (@files) {unlink ("${lbdir}$msgdir/$_") if ((-M "${lbdir}$msgdir/$_") > 1);}

$inmembernamefile = $inmembername;
$inmembernamefile =~ s/ /\_/g;
$inmembernamefile =~ tr/A-Z/a-z/;

if (-e "${lbdir}$msgdir/$inmembernamefile.cgi") {
    open(FILE, "${lbdir}$msgdir/$inmembernamefile.cgi");
    $x = <FILE>;
    close(FILE);
    chomp $x;
} else {
    &error("�޸�����&��ʱ��������ȡ�����������һ��������޸����빤����");
}

if ($password ne "") {
    $password = "$x$password";
    eval {$mypassword = md5_hex($password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$mypassword = md5_hex($password);');}
}

&error("�޸�����&��������У������벻Ҫ�����޸ģ�") if ($mypassword ne $inpassword);
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&mischeader("ȡ������");
$action        = $query -> param('action');
$output .= qq~<p><SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
~;

if ($action eq "login") {
    $password1 = $query -> param('password1');
    $password2 = $query -> param('password2');
    if ($password1 ne $password2) { &error("ȡ������&�Բ����������������̳���벻��ͬ��"); }
    if($password1 =~ /[^a-zA-Z0-9]/)     { &error("ȡ������&��̳����ֻ�����Сд��ĸ�����ֵ���ϣ���"); }
    if($password1 =~ /^lEO/)     { &error("ȡ������&��̳���벻������ lEO ��ͷ�����������"); }
    if(length($password1)<8)      { &error("ȡ������&��̳����̫���ˣ����������̳������� 8 λ���ϣ�"); }

    if ($password1 ne "") {
        eval {$password1 = md5_hex($password1);};
        if ($@) {eval('use Digest::MD5 qw(md5_hex);$password1 = md5_hex($password1);');}
        $password1 = "lEO$password1";
    }
    
    if (($inmembername ne "")&&($password1 ne "")) {
    	my $namenumber = &getnamenumber($inmembernamefile);
	&checkmemfile($inmembernamefile,$namenumber);
	$filetomake = "$lbdir" . "$memdir/$namenumber/$inmembernamefile.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE3,"+<$filetomake");
        flock(FILE3, 2) if ($OS_USED eq "Unix");
        my $filedata = <FILE3>;
	chomp($filedata);
	($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber ,$location ,$interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount,$ebankdata,$onlinetime,$userquestion,$awards,$jifen,$userface,$soccerdata,$useradd5) = split(/\t/,$filedata);
	seek(FILE3,0,0);
	print FILE3 "$membername\t$password1\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
	close(FILE3);
	if (open(FILE, ">${lbdir}$memdir/old/$inmembernamefile.cgi")) {
	    print FILE "$membername\t$password1\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
	    close(FILE);
	}
	&winunlock($filetomake) if ($OS_USED eq "Nt");
    }
    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>$inmembername�������������Ѿ���Ч��</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
���������<ul><li><a href="loginout.cgi">���˵�¼��̳</a>
</ul></tr></td></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
~;
    unlink ("${lbdir}$msgdir/$inmembernamefile.cgi");
}
else {
    $output .= qq~<tr>
<td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center>
<form action="$thisprog" name="login" method="post" onSubmit="submitonce(this)">
<input type=hidden name="action" value="login">
<input type=hidden name="username" value="$inmembername">
<input type=hidden name="password" value="$inpassword">
<font face="$font" color=$fontcolormisc><b>$inmembername����������Ѿ�ͨ��ȷ�ϣ�����������������</b></font></td></tr>
<tr><td width=40% bgcolor=$miscbackone><font color=$fontcolormisc><b>��̳���룺 (����8λ)</b><br>��������̳���룬���ִ�Сд<br>ֻ��ʹ�ô�Сд��ĸ�����ֵ����</font></td><td width=60% bgcolor=$miscbackone><input type=password name="password1">&nbsp;* ���������д</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��̳���룺 (����8λ)</b><br>����һ�飬�Ա�ȷ����</font></td><td bgcolor=$miscbackone><input type=password name="password2">&nbsp;* ���������д</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit value="ȷ ��" name=submit></td></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR><BR>
~;
}
&output("$boardname - ȡ������",\$output);
exit;
