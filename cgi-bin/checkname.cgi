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
require "data/styles.cgi";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "checkname.cgi";

$query = new LBCGI;
$inmembername = $query -> param('name');
$inmembername = &cleaninput($inmembername);
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

$CheckR="";
$bannedmember = "no";
($ipaddress,$trueipaddress) = split(/\=/,&myip);

$filetoopen = "$lbdir" . "data/baniplist.cgi";
open(FILE,"${lbdir}data/baniplist.cgi");
my $bannedips = <FILE>;
close(FILE);
chomp $bannedips;
$bannedips = "\t$bannedips\t";
$bannedips =~ s/\t\t/\t/isg;
my $ipaddresstemp     = "\t$ipaddress\t";
my $trueipaddresstemp = "\t$trueipaddress\t";
$bannedmember = "yes" if (($bannedips =~ /$ipaddresstemp/i)||($bannedips =~ /$trueipaddresstemp/i));

if ($bannedmember eq "yes") { $CheckR = "��ǰ�� IP ������T���óɽ�ֹע�����û��ˣ�����������������T�Ա�����"; }

open(THEFILE,"${lbdir}data/noreglist.cgi");
$userarray = <THEFILE>;
close(THEFILE);
chomp $userarray;
@saveduserarray = split(/\t/,$userarray);
$noreg = "no";
foreach (@saveduserarray) {
    chomp $_;
    if ($inmembername =~ m/$_/isg) {
        $noreg = "yes";
	last;
    }
}
$CheckR="�Ѿ����������߱���ֹע��,�����һ���û�����" if ($noreg eq "yes");

$CheckR="�û��������⣬�������" if (($inmembername =~ /^m-/i)||($inmembername =~ /^s-/i)||($inmembername =~ /tr-/i)||($inmembername =~ /^y-/i)||($inmembername =~ /ע��/i)||($inmembername =~ /guest/i)||($inmembername =~ /qq-/i)||($inmembername =~ /qq/i)||($inmembername =~ /qw/i)||($inmembername =~ /q-/i)||($inmembername =~ /qx-/i)||($inmembername =~ /qw-/i)||($inmembername =~ /qr-/i)||($inmembername =~ /^ȫ��/i)||($inmembername =~ /register/i)||($inmembername =~ /��Ƹ��/i)||($inmembername =~ /����/i)||($inmembername =~ /����ϵͳѶϢ/i)||($inmembername =~ /leobbs/i)||($inmembername =~ /leoboard/i)||($inmembername =~ /�װ�/i)||($inmembername =~ /LB5000/i)||($inmembername =~ /ȫ�������Ա/i)||($inmembername =~ /����Ա/i)||($inmembername =~ /����/i)||($inmembername =~ /����Ϣ�㲥/i)||($inmembername =~ /��ʱ��ȱ/i)||($inmembername =~ /����������/i)||($inmembername =~ /����/i)||($inmembername =~ /̳��/i)||($inmembername =~ /nodisplay/i)||($inmembername =~ /^system/i)||($inmembername =~ /---/i)||($inmembername eq "admin")||($inmembername eq "root")||($inmembername eq "copy")||($inmembername =~ /^sub/)||($inmembername =~ /^exec/)||($inmembername =~ /\@ARGV/i)||($inmembername =~ /^require/)||($inmembername =~ /^rename/i)||($inmembername =~ /^dir/i)||($inmembername =~ /^print/i)||($inmembername =~ /^con/i)||($inmembername =~ /^nul/i)||($inmembername =~ /^aux/i)||($inmembername =~ /^com/i)||($inmembername =~ /^lpt/i)||($inmembername =~ /^open/i));

$CheckR="�û��������⣬�������" if ($inmembername =~ /^q(.+?)-/ig || $inmembername =~ /^q(.+?)q/ig);


$tempinmembername =$inmembername;
$tempinmembername =~ s/ //g;
$tempinmembername =~ s/  //g;
if ($inmembername =~ /^����/) { $CheckR="�е�����Ӵ���벻Ҫ���û����Ŀ�ͷ��ʹ�ÿ���������"; }
if ($inmembername =~ /_/)     { $CheckR="�е�����Ӵ���벻Ҫ���û�����ʹ���»��ߣ�"; }
if ($inmembername =~ /\t/)    { $CheckR="�е�����Ӵ���벻Ҫ���û�����ʹ�������ַ���"; }
if (length($inmembername)>12) { $CheckR="̫���ˣ��벻Ҫ����12���ַ���6�����֣���"; }
if (length($inmembername)<2)  { $CheckR="̫���ˣ��벻Ҫ���2���ַ���1�����֣���"; }

#&getmember("$inmembername");
&getmember("$inmembername","no");
if ($userregistered ne "no") { $CheckR="�Ѿ����û�ʹ�ã���ѡ��һ���µ��û�����"; }

if ($inmembername eq "") { $CheckR = "����Ϊ��"; }
if ($inmembername ne "") { $show   = qq~"<font color="red">$inmembername</font>"~; }
$CheckR = "�Բ�����������û��������⣬�벻Ҫ���û����а���\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]�����ַ���" if ($inmembername =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/);

if ($CheckR eq "") {$CheckR="û�����⣬��������ʹ�á�"; }
print qq~
<html>
<head> 
<title>$boardname</title>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<!--end Java-->
<!--css info(editable)-->
<style>
A:visited{TEXT-DECORATION: none}
A:active{TEXT-DECORATION: none}
A:hover{TEXT-DECORATION: underline overline}
A:link{text-decoration: none;}
.t{LINE-HEIGHT: 1.4}
BODY{FONT-FAMILY: ��ϸ����; FONT-SIZE: 9pt;
SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
SCROLLBAR-SHADOW-COLOR: buttonface;
SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
SCROLLBAR-TRACK-COLOR: #eeeeee;
SCROLLBAR-DARKSHADOW-COLOR: buttonshadow}
TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: ��ϸ����; FONT-SIZE: 9pt} 
INPUT{BORDER-TOP-WIDTH: 1px; PADDING-RIGHT: 1px; PADDING-LEFT: 1px; BORDER-LEFT-WIDTH: 1px; FONT-SIZE: 9pt; BORDER-LEFT-COLOR: #cccccc; BORDER-BOTTOM-WIDTH: 1px; BORDER-BOTTOM-COLOR: #cccccc; PADDING-BOTTOM: 1px; BORDER-TOP-COLOR: #cccccc; PADDING-TOP: 1px; HEIGHT: 18px; BORDER-RIGHT-WIDTH: 1px; BORDER-RIGHT-COLOR: #cccccc}
textarea, select {border-width: 1; border-color: #000000; background-color: #efefef; font-family: ��ϸ����; font-size: 9pt; font-style: bold;}
--> 
</style> 
<!--end css info-->
</head>
<body $lbbody>
<table width=100% align=center cellspacing=0 cellpadding=1  border=0 bgcolor=$titleborder height="100%"><tr><td>
<table width=100% cellspacing=0 cellpadding=4 border=0 height="100%">
<tr><td align="center" bgcolor=$menubackground><font color=$menufontcolor>����ѡ���û���$show$CheckR</font></td></tr></table></td></tr></table>
</body>
</html>
~;
exit;
