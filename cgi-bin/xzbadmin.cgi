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
require "code.cgi";
require "bbs.lib.pl";
require "postjs.cgi";
$|++;
$thisprog	= "xzbadmin.cgi";
$query		= new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

if (int($hownews) < 50)
{	#����Ԥ��ֵ
	$hownews = 100;
}
#ȡ������
for ('forum','membername','password','action','inpost','message','xzbid','checked') {
    next unless defined $_;
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$inforum		= $forum;
if (($inforum eq "")||($inforum !~ /^[0-9]+$/))
{	#��֤����̳���
	&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��");
}
if (-e "${lbdir}data/style${inforum}.cgi")
{	#��ȡר�����
	require "${lbdir}data/style${inforum}.cgi";
}
$inmembername	= $membername;			#ת������
$inpassword	= $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$currenttime	= time;
$inmembername	= &stripMETA($inmembername);

#���˷��
$inselectstyle	= $query->cookie("selectstyle");	#��ȡ����
$inselectstyle   = $skinselected if ($inselectstyle eq "");
if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./))
{	#���˷����ȷ
	&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��");	#�������ҳ
}
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi"))
{	#��ָ�����˷��
	require "${lbdir}data/skin/${inselectstyle}.cgi";	#��ȡ���˷��
}
#��Ա�ʺ�
if ($inmembername eq "")
{	#û�ṩ��Ա����
	$inmembername	= $query->cookie("amembernamecookie");	#�� COOKIE ��ȡ
}
if ($inpassword eq "")
{	#û�ṩ����
	$inpassword		= $query->cookie("apasswordcookie");	#�� COOKIE ��ȡ
}
$inmembername	=~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;	#�ִ�����
$inpassword		=~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

#����ʺ�
if (($inmembername eq "")||($inmembername eq "����"))
{	#����
	&error("��ͨ����&ֻ�޻�Ա���룡");	#��ֹ����
}
else
{	#��Ա
	&getmember("$inmembername","no");	#��ȡ�ʺ�����
	if ($userregistered eq "no")
	{	#δע���ʺ�
		&error("��ͨ����&���û����������ڣ�");				#��ֹ����
	}
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
}
$addtimes		= ($timedifferencevalue + $timezone)*3600;	#ʱ��
#��̳״̬
&doonoff;  #��̳�������

&error("������̳&�����̳��û��Ȩ�޽�����̳��") if ($yxz ne '' && $yxz!~/,$membercode,/);
    if ($allowusers ne '') {
	&error('������̳&�㲻����������̳��') if (",$allowusers," !~ /\Q,$inmembername,\E/i);
    }

#��ȡ����̳����
my $forumdata	= "${lbdir}forum${inforum}/foruminfo.cgi";
if (-e $forumdata)
{	#�ҵ��÷���̳����
	&getoneforum("$inforum");							#��ȡ����
}
else
{	#�Ҳ�������
	&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��");	#�������ҳ
}
#��֤Ȩ��
if (($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes"))
{	#��Ȩ�޵��ˣ�̳�����ܰ������������е�
	&error("ɾ��С�ֱ�&��ûȨ��ɾ����");					#�������ҳ
}
#˵������
$helpurl		= &helpfiles("�Ķ����");
$helpurl		= qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;
#ָ��ģʽ
my %Mode = (
	'delete'		=> \&deletexzb,		#ɾ��
	'deleteover'	=> \&deleteoverxzb,	#ɾ�� 2
	'edit'			=> \&editxzb,		#�༭
);
#�����ͷ
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
#��֤ģʽ
if (defined $Mode{$action})
{	#�и�ģʽ
	$Mode{$action}->();		#ִ��ģʽ
}
else
{	#û�и�ģʽ
	&toppage;				#ִ��Ԥ��ģʽ -> ��ҳ
}
#���ҳ��
&output("$forumname - С�ֱ�����",\$output);
#�������
exit;
#ģʽ����
sub toppage
{	#ģʽ -> ��ҳ
	#���ҳ��ͷ
	&mischeader("С�ֱ�����");
	#��ȡ����
	my @xzbdata = ();								#��ʼ��
	open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");	#�����ļ�
	while (my $line = <FILE>)
	{	#ÿ�ζ�ȡһ������ loop 1
		chomp $line;			#ȥ�����з�
		push(@xzbdata,$line);	#�Ž���� ARRAY
	}#loop 1 end
	close(FILE);									#�ر��ļ�

	#ҳ�����
	$output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post" id="1">
<input type="hidden" name="action" value="delete">
<input type="hidden" name="forum" value="$inforum">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="7%" $catbackpic align="center">
		</td>
		<td bgcolor="$titlecolor" width="*" $catbackpic align="center">
			<font color="$titlefontcolor"><b>����</b></font>
		</td>
		<td bgcolor="$titlecolor" width="10%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>������</b></font>
		</td>
		<td bgcolor="$titlecolor" width="20%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>����ʱ��</b></font>
		</td>
		<td bgcolor="$titlecolor" width="15%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>�����ֽ���</b></font>
		</td>
		<td bgcolor="$titlecolor" width="3%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>ѡ</b></font>
		</td>
	</tr>~;
	#�������
	my $i = 0;	#���
	foreach my $line(@xzbdata)
	{	#��Ȧ�������� loop 1
		#   û��   , ����   , ������  , ���� , ����ʱ��
		my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);		#�ָ�����
		#����ɫ
		if ($i%2 == 0) {
			$postbackcolor = $postcolorone;
		} else {
			$postbackcolor = $postcolortwo;
		}
		my $admini		= qq~<div align="right"><font color="$titlecolor">|<a href="$thisprog?action=edit&forum=$inforum&xzbid=$posttime"><font color="$titlecolor">�༭</font></a>|<a href="$thisprog?action=delete&forum=$inforum&xzbid=$posttime"><font color="$titlecolor">ɾ��</font></a>|</font></div>~;		#��������
		my $postdate		= &dateformat($posttime+$addtimes);						#����ʱ��
		my $msgbytes	= length($msg);												#�ֽ���
		my $startedby	= uri_escape($postid);		#��Ա��
		$iuu = $i + 1;
		$output .= qq~
	<tr>
		<td bgcolor="$postbackcolor" width="7%" align="center">
			<font color="$postfontcolorone">No.<i>$iuu</i></font>
		</td>
		<td bgcolor="$postbackcolor" width="*" align="left">
			&nbsp;&nbsp;<font color="$postfontcolorone">$title</font>$admini
		</td>
		<td bgcolor="$postbackcolor" width="10%" align="center">
			<font color="$postfontcolorone"><span style=cursor:hand onClick=javascript:O9('$startedby')>$postid</span></font>
		</td>
		<td bgcolor="$postbackcolor" width="20%" align="center">
			<font color="$postfontcolorone">$postdate</font>
		</td>
		<td bgcolor="$postbackcolor" width="15%" align="center">
			<font color="$postfontcolorone"><i>$msgbytes</i> byte(s)</font>
		</td>
		<td bgcolor="$postbackcolor" width="3%" align="center">
			<input type="checkbox" name="xzbid" value="$posttime">
		</td>
	</tr>~;
		$i++;																		#��ŵ���
	}#loop 1 end
	#ҳ�����
	$output .= qq~
	</table>
	</td>
</tr>
</table><SCRIPT>valignend()</SCRIPT>
<table cellpadding="0" cellspacing="2" width="$tablewidth" align="center" border="0">
<tr>
	<td align="right" width="75%">
		<input type="submit" value="ɾ��ѡ��">
	</td>
</form id="1 end">
<form action="$thisprog" method="post" id="2">
<input type="hidden" name="action" value="deleteover">
<input type="hidden" name="forum" value="$inforum">
	<td align="right">
		<input type="submit" value="ɾ����������Сʱ��С�ֱ�">
	</td>
</tr>
</form id="2 end">
</table><BR>~;
}
sub editxzb
{	#ģʽ -> �༭
	#���ҳ��ͷ
	&mischeader("�༭С�ֱ�");
	#��ѰҪ�༭��С�ֱ�
	my $findresult	= -1;	#��ʼ��
	my @xzbdata		= ();
	my $xzbno		= 0;
	open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");	#�����ļ�
	while (my $line = <FILE>)
	{	#ÿ�ζ�ȡһ������ loop 1
		chomp $line;															#ȥ�����з�
		my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);	#�ָ�����
		if ($posttime eq $xzbid)
		{	#�������
			$findresult = $xzbno;		#������Ѱ���
		}
		elsif ($findresult == -1)
		{	#���ǵ�ʱ��
			$xzbno++;				#��ŵ���
		}
		push(@xzbdata,$line);													#�Ž����� ARRAY
	}#loop 1 end
	close(FILE);
	if ($findresult == -1)
	{	#�Ҳ���
		&error("�༭С�ֱ�&�Ҳ���Ŀ��С�ֱ���");										#�������ҳ
	}
	if ($checked ne 'yes')
	{	#δ����ȷ��
		#Ŀǰ����
		#   û��   , ����   , ������  , ���� , ����ʱ��
		my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$xzbdata[$xzbno]);	#�ָ�����
	    $msg =~ s/\<p\>/\n\n/ig;															#�ִ�����
	    $msg =~ s/\<br\>/\n/ig;
		my $startedby	=  uri_escape($postid);				#��Ա��
		#ҳ�����
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post" id="1">
<input type="hidden" name="action" value="edit">
<input type="hidden" name="checked" value="yes">
<input type="hidden" name="forum" value="$inforum">
<input type="hidden" name="xzbid" value="$posttime">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center" colspan="2">
			<font color="$titlefontcolor"><b>�༭��ѡС�ֱ�</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolortwo" alin="center" colspan="2">
			<table cellpadding="0" cellspacing="0" width="100%" bgcolor="$tablebordercolor" align="center" border="0">
			<tr>
				<td>
					<table cellpadding="3" cellspacing="1" border="0" width="100%">
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
					<tr>
						<td bgcolor=$miscbackone valign=top>
							<font color="$fontcolormisc"><b>С�ֱ�������</b></font>
						</td>
						<td bgcolor="$miscbackone">
							<font color="$postfontcolorone"><u><span style=cursor:hand onClick=javascript:O9('$startedby')>$postid</span></u></font>
						</td>
					</tr>
					<tr>
						<td bgcolor=$miscbackone valign=top>
							<font color="$fontcolormisc"><b>С�ֱ�����</b> (��� 80 ��)</font>
						</td>
						<td bgcolor="$miscbackone">
							<input type="text" maxlength="80" name=inpost onkeydown=ctlent() value="$title" size=80>
						</td>
					</tr>
					<tr>
						<td bgcolor=$miscbacktwo valign=top>
							<font color="$fontcolormisc"><b>С�ֱ�����</b> (��� $hownews ��)<p>
							�ڴ���̳�У�
							<li>HTML ��ǩ: <b>������</b>
							<li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS ��ǩ</a>: <b>����</b></font>
						</td>
						<td bgcolor=$miscbacktwo valign=top>
							<TEXTAREA cols=58 name=message rows=6 wrap=soft onkeydown=ctlent()>$msg</TEXTAREA>
						</td>
					</tr>
					</table>
				</td>
			</tr>
			</table>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="right" width="51%">
			<input type="submit" value="�ύ�༭">&nbsp;
		</td>
</form id="1">
<form action="$thisprog" method="get" id="2">
<input type="hidden" name="forum" value="$inforum">
		<td bgcolor="$postcolorone" align="left">
			&nbsp;<input type="submit" value="������ҳ��">
		</td>
</form id="2">
	</tr>
	</table>
	</td>
</tr>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
	else
	{	#�ѽ���ȷ��
		#��C̎��
		if ($inpost eq "")
		{
			&error("�༭С�ֱ�&����������⣡");									#�������ҳ
		}
		elsif (length($inpost) > 82)
		{
			&error("�༭С�ֱ�&���������");										#�������ҳ
		}
		elsif (length($message) > $hownews)
		{
			&error("�༭С�ֱ�&���ݹ�����");										#�������ҳ
		}
		#�༭����
		my $newfile	= '';									#��ʼ���ļ�
		foreach my $line (@xzbdata)
		{	#ÿ�ζ�ȡһ������ loop 1
			chomp $line;			#ȥ�����з�
			my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);		#�ָ�����
			if($posttime eq $xzbid)
			{	#�༭Ŀ��
				$line = "����������\t$inpost\t$inmembername\t$message\t$posttime\t";	#����
			}
			$newfile .= $line."\n";														#�������ļ���
		}#loop 1 end
		open(FILE,'>'."${lbdir}boarddata/xzb$inforum.cgi");	#����ֻд�ļ�
		print FILE $newfile;								#д�����ļ�����
		close(FILE);										#�ر��ļ�
		#ҳ�����
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="get">
<input type="hidden" name="forum" value="$inforum">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>�Ѿ��༭��С�ֱ�����</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="center">
			<input type="submit" value="������ҳ��">
		</td>
	</tr>
	</table>
	</td>
</tr>
</form>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
}
sub deletexzb
{	#ģʽ -> ɾ��
	#���ҳ��ͷ
	&mischeader("ɾ��С�ֱ�");
	#��ȡ��ѡ����
	my @noarray		= ();	#��ʼ��
	my %nohash		= ();
	my $xzbidcount	= 0;
	my $novalue		= '';	# HIDDEN ��������
	if ($xzbid ne "")
	{	#�ж����һ�� ID
		@noarray = $query->param('xzbid');	#���� ID
		foreach my $xzbid(@noarray)
		{	#�������� ID loop 1
			$novalue .= '<input type="hidden" name="xzbid" value="'.$xzbid.'">'."\n";	#������λ
			$nohash{$xzbid} = $xzbid;													#���� HASH
			$xzbidcount++;																#��Ŀ����
		}#loop 1 end 
		chomp $novalue;						#ȥ�����ỻ��
	}
	if ($xzbidcount == 0)
	{	#ûѡ�κ�С�ֱ�
		&error("ɾ��С�ֱ�&û��ѡ�κ�С�ֱ���");			#�������ҳ
	}

	if ($checked ne 'yes')
	{	#δ����ȷ��
		#ҳ�����
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post" id="1">
<input type="hidden" name="action" value="delete">
<input type="hidden" name="checked" value="yes">
<input type="hidden" name="forum" value="$inforum">
$novalue
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center" colspan="2">
			<font color="$titlefontcolor"><b>ȷ��ɾ����ѡ�� $xzbidcount ��С�ֱ���</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="right" width="51%">
			<input type="submit" value="ȷ��ɾ��">&nbsp;
		</td>
</form id="1">
<form action="$thisprog" method="get" id="2">
<input type="hidden" name="forum" value="$inforum">
		<td bgcolor="$postcolorone" align="left">
			&nbsp;<input type="submit" value="������ҳ��">
		</td>
</form id="2">
	</tr>
	</table>
	</td>
</tr>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
	else
	{	#�ѽ���ȷ��
		#ɾ������
		my $newfile	= '';									#��ʼ���ļ�
		my $delbyte	= '';									#ɾ�����ֽ�
		open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");		#�����ļ�
		while (my $line = <FILE>)
		{	#ÿ�ζ�ȡһ������ loop 1
			chomp $line;			#ȥ�����з�
			my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);		#�ָ�����
			if(($line eq "") || (defined $nohash{$posttime}))
			{	#�հ��л�ɾ��Ŀ¼
				$delbyte += length($line);	#����ɾ�����ֽ�
				next;						#����
			}
			$newfile .= $line."\n";														#�������ļ���
		}#loop 1 end
		close(FILE);										#�ر��ļ�
		open(FILE,'>'."${lbdir}boarddata/xzb$inforum.cgi");	#����ֻд�ļ�
		print FILE $newfile;								#д�����ļ�����
		close(FILE);										#�ر��ļ�
		#ҳ�����
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="get">
<input type="hidden" name="forum" value="$inforum">
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>��ѡ�� $xzbidcount ��С�ֱ��ѱ�ɾ��</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolortwo" align="center">
			�ܹ�ɾ�� $delbyte  byte(s)
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="center">
			<input type="submit" value="������ҳ��">
		</td>
	</tr>
	</table>
	</td>
</tr>
</form>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
}
sub deleteoverxzb
{	#ģʽ -> ɾ�� 2
	#���ҳ��ͷ
	&mischeader("ɾ��С�ֱ�");
	#��ȡ��ʱ����
	my @delxzbid	= ();	#��ʼ��
	if($checked ne 'yes')
	{	#δ����ȷ��
		open(FILE,"${lbdir}boarddata/xzb$inforum.cgi");	#�����ļ�
		while (my $line = <FILE>)
		{	#ÿ�ζ�ȡһ������ loop 1
			chomp $line;															#ȥ�����з�
			my ($nouse , $title , $postid , $msg , $posttime) = split(/\t/,$line);	#�ָ�����
			if ($currenttime-$posttime > 3600*48)
			{	#��������Сʱ
				push(@delxzbid,$posttime);		#�ŵ���ɾ ID
			}
		}#loop 1 end
		close(FILE);									#�ر��ļ�
	}
	else
	{	#�ѽ���ȷ��
		@delxzbid = $query->param('xzbid');				#��ɾ ID
	}
	if (@delxzbid == 0)
	{	#û�κ�С�ֱ���Ҫɾ
		&error("ɾ��С�ֱ�&û��С�ֱ���Ҫɾ����");			#�������ҳ
	}
	#��ȡ��ѡ����
	my %nohash		= ();
	my $xzbidcount	= 0;
	my $novalue		= '';	# HIDDEN ��������
	foreach my $xzbid(@delxzbid)
	{	#�������� ID loop 1
		unless ($currenttime-$posttime > 3600*48)
		{	#�ټ��ʱ�䣬��ͨ��
			next;		#����
		}
		$novalue .= '<input type="hidden" name="xzbid" value="'.$xzbid.'">'."\n";	#������λ
		$nohash{$xzbid} = $xzbid;													#���� HASH
		$xzbidcount++;																#��Ŀ����
	}#loop 1 end 
	chomp $novalue;						#ȥ�����ỻ��
	
	if ($checked ne 'yes')
	{	#δ����ȷ��
		#ҳ�����
		$output .= qq~<P><SCRIPT>valigntop()</SCRIPT>
<table cellpadding="0" cellspacing="0" width="$tablewidth" bgcolor="$tablebordercolor" align="center" border="0">
<form action="$thisprog" method="post">
<input type="hidden" name="action" value="delete">
<input type="hidden" name="checked" value="yes">
<input type="hidden" name="forum" value="$inforum">
$novalue
<tr>
	<td>
	<table cellpadding="3" cellspacing="1" width="100%" border="0">
	<tr>
		<td bgcolor="$titlecolor" width="100%" $catbackpic align="center">
			<font color="$titlefontcolor"><b>ȷ��ɾ����ѡ�� $xzbidcount ��С�ֱ���</b></font>
		</td>
	</tr>
	<tr>
		<td bgcolor="$postcolorone" align="center">
			<input type="submit" value="ȷ��ɾ��">
		</td>
	</tr>
	</table>
	</td>
</tr>
</form>
</table><SCRIPT>valignend()</SCRIPT>~;
	}
}