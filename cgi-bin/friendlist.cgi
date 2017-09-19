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
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

my $query = new LBCGI;
$thisprog = "friendlist.cgi";

my $action = $query->param('action');
my $deluser = $query->param('deluser');
my $adduser = $query->param('adduser');
my $inmembername = $query->param('membername');
my $inpassword = $query->param('password');
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$adduser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\;\\\{\}\'\:\"\,\.\/\<\>\?]//isg;
$deluser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\;\\\{\}\'\:\"\,\.\/\<\>\?]//isg;

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie");   }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
    $userregistered = "no";
    errorbl("���¼����ʹ�ñ����ܣ�");
} else {
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($inpassword ne "" && $userregistered eq "no");
    &error("��ͨ����&�������û���������������µ�¼��") if ($inpassword ne $password && $userregistered ne "no");
    &action;
}

sub action {
if ($action eq "adduser") { &adduser($adduser); }
elsif ($action eq "deluser") { &deluser($deluser); }
else { &list; }
}

sub adduser {
errorbl("�Լ�����Լ�Ϊ������ʲô��") if ($adduser eq $inmembername);
&getmember($adduser,"no");
if ($userregistered ne "no") {

$memberfiletitle = $inmembername;
$memberfiletitle =~ s/ /_/g;
$memberfiletitle =~ tr/A-Z/a-z/;

$deluser =~ s/\+/ /;

$filetomake = "$lbdir" . "memfriend/${memberfiletitle}.cgi";
if (-e $filetomake) {
	open(FILE, "$filetomake");
	@currentlist = <FILE>;
	close (FILE);
}

unless (grep(/^����������$adduser$/, @currentlist)) {
push (@currentlist, $adduser);
}

if (open(FILE, ">$filetomake")) {
flock(FILE, 2) if ($OS_USED eq "Unix");
foreach $user (@currentlist) {
	chomp($user);
	$user =~ s/^����������//isg;
	print FILE "����������$user\n";
}
close(FILE);
}

&list;
} else {
errorbl("û�и�ע���û���");
}
} ### end adduser

sub deluser {

$memberfiletitle = $inmembername;
$memberfiletitle =~ s/ /_/g;
$memberfiletitle =~ tr/A-Z/a-z/;

$deluser =~ s/\+/ /;

$filetomake = "$lbdir" . "memfriend/${memberfiletitle}.cgi";
if (-e $filetomake) {
	open(FILE, "$filetomake");
	@currentlist = <FILE>;
	close (FILE);
} else {
	errorbl("��ĺ����б�Ϊ�գ�");
}

if (open(FILE, ">$filetomake")) {
flock(FILE, 2) if ($OS_USED eq "Unix");
foreach $user (@currentlist) {
	chomp($user);
	$user =~ s/^����������//isg;
	unless ($user eq $deluser) {
	print FILE "����������$user\n";
	}
}
close(FILE);
}

&list;

} ### end deluser

sub list {

$output .= qq~<html>
<head>
<script type="text/javascript">
function openScript(url, width, height) {
        var Win = window.open(url,"openwindow",'width=' + width + ',height=' + height + ',resizable=1,scrollbars=yes,menubar=yes,status=yes' );
}
</script>
<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline 	}
		A:link 	  {	text-decoration: none;}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
		TD	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT	{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT	{	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		DIV	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}

</style>
<title>$inmembername - �����б�</title>
</head>
<body bgcolor="#D1D9E2"  alink="#333333" vlink="#333333" link="#333333" >
<center>$inmembername �ĺ����б�</center><br>
<table width=97% align=center cellspacing=0 cellpadding=1 bgcolor=#333333>
		<tr><td>
<table width=100% cellspacing=0 cellpadding=4>
~;

$memberfiletitle = $inmembername;
$memberfiletitle =~ s/ /_/g;
$memberfiletitle =~ tr/A-Z/a-z/;

$filetomake = "$lbdir" . "memfriend/${memberfiletitle}.cgi";
if (-e $filetomake) {
	open(FILE, "$filetomake");
	@currentlist = <FILE>;
	close (FILE);
}



$colspant = "7";
$colspans = "5";

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    &whosonline("$inmembername\t�����б�\tnone\t�鿴�����б�\t");
}

$output .= qq~
<tr>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>����</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>����Ϣ</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>Email</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>ICQ</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>OICQ</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>��ҳ</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>ɾ��?</b></center></font></td>
</tr>
~;
$pmnamenumber = 0;
foreach $user (@currentlist) {
    chomp $user;
	$user =~ s/^����������//isg;
#    &getmember($user);
    &getmember("$user","no");
    $memname = $membername;
    $memname =~ s/ /+/;
    $pmname = $membername;
    $pmname =~ s/ /_/;
    $duser = $user;
    $duser =~ s/ /+/;
$pmnamenumber++;
    if ($userregistered ne "no") {

	$homepage =~ s/http\:\/\///sg;

	if ($homepage) { $homepage = qq~<a href="http://$homepage" target="_blank"><img src="$imagesurl/images/homepage.gif" border=0></a>~; } else { $homepage = "N/A"; }
	$emailaddress = &encodeemail($emailaddress);
	if ($showemail eq "no"||$emailstatus eq "no"||$emailaddress eq ""||$showemail eq "msn"){
	    $emailaddress = "δ����" if ($$emailaddress eq "");
	    $emailaddress = "����" if ($emailstatus eq "no");
	    $emailaddress = "����" if ($showemail eq "no");
	    $emailaddress = "<a href=mailto:$emailaddress><img border=0 src=$imagesurl/images/msn.gif></a>" if ($showemail eq "msn");
	}
	else {$emailaddress = "<a href=mailto:$emailaddress><img border=0 src=$imagesurl/images/email.gif></a>" }

	if ($icqnumber) { $icqnumber = qq~<a href="javascript:openScript('misc.cgi?action=icq&UIN=$icqnumber',450,300)"><img src=$imagesurl/images/icq.gif border=0></a>~; } else { $icqnumber = "N/A"; }
	if ($oicqnumber) { $oicqnumber = qq~<a href="javascript:openScript('http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$oicqnumber',450,200)"><img src="$imagesurl/images/oicq.gif" border=0></a>~; } else { $oicqnumber = "N/A"; }

    my $membernametemp = "\_$membername\_";
    if ($onlineuserlist =~ /$membernametemp/i) { $onlineinfo = "���û�Ŀǰ����";$onlinepic="online1.gif"; } else { $onlineinfo = "���û�Ŀǰ������";$onlinepic="offline1.gif"; }
    if (($mymembercode eq "ad")&&($onlineuserlisthidden =~ /$membernametemp/i)) { $onlineinfo = "���û�Ŀǰ��������״̬";$onlinepic="onlinehidden.gif"; }
    $online = qq~<IMG SRC=$imagesurl/images/$onlinepic width=15 alt=$onlineinfo align=absmiddle>~;

	$output .=qq~
	<tr>
	<td bgcolor=$miscbackone>$online <a href="profile.cgi?action=show&member=~ . uri_escape($pmname) . qq~" target=_blank>$user</a></td>
	<td bgcolor=$miscbackone><center><a href=# onClick="javascript:openScript('messanger.cgi?action=new&touser=~ . uri_escape($pmname) . qq~',600,400)"><img src="$imagesurl/images/message.gif" border=0></a></center></td>
	<td bgcolor=$miscbackone><center>$emailaddress</center></td>
	<td bgcolor=$miscbackone><center>$icqnumber</center></td>
	<td bgcolor=$miscbackone><center>$oicqnumber</center></td>
	<td bgcolor=$miscbackone><center>$homepage</center></td>
	<td bgcolor=$miscbackone><center><form action=friendlist.cgi method=post name=pm$pmnamenumber><input type=hidden name=action value=deluser><input type=hidden name=deluser value=$duser><a href="javascript:document.pm$pmnamenumber.submit()">ɾ��</a></center></td></form></tr>
	~;
    }
    else {
	$output .=qq~
	<tr>
	<td bgcolor=$miscbackone>$user (δע��)</td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone><center><form action=friendlist.cgi method=post name=pm$pmnamenumber><input type=hidden name=action value=deluser><input type=hidden name=deluser value=$duser><a href="javascript:document.pm$pmnamenumber.submit()">ɾ��</a></center></td></form></tr>
	~;

    }
}

$output .= qq~
<tr>
<form action=friendlist.cgi method=post name=adduser><input type=hidden name=action value=adduser><td bgcolor=$miscbackone><font  color=black >��������:</td><td colspan=$colspans bgcolor=$miscbackone><input type=text size=20 name=adduser></td><td bgcolor=$miscbackone><center><a href="javascript:document.adduser.submit()">����</a></center></td></form>
<tr><td bgcolor=$miscbackone colspan=$colspant><center><font  color=black >������Ҫ�����ӵĺ����������������ȷ�ϲ�����<br><br><a href=javascript:top.close();>[�رմ���]</a></center></td></tr>
</table></td></tr>
	    </table>
</body>
</html>
~;

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print "$output";
} ### end of list

sub errorbl {
$errormsg = shift;
$output = qq~
<html>
<head>
<title>$inmembername - �����б� >> ����</title>
<meta http-equiv="refresh" content="30;URL=friendlist.cgi">
<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline 	}
		A:link 	  {	text-decoration: none;}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
		TD	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT	{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT	{	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		DIV	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	{	FONT-FAMILY: ����; FONT-SIZE: 9pt	}

</style>
</head>
<body bgcolor="#D1D9E2"  alink="#333333" vlink="#333333" link="#333333">
<br>
<center>�����б����</center><br><br>
<font color=red>
<center>
<b>$errormsg</b>
</center>
</font>
<br><br>
<center><font color=$fontcolormisc> << <a href="javascript:history.go(-1)">������һҳ</a></center>

</body>
</html>
~;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print "$output";
exit;
}
