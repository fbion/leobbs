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
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "recooper.pl";

$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$thisprog = "userrating.cgi";
$query = new LBCGI;
$inforum = $query->param("oldforum");
$intopic = $query->param("oldtopic");
$inpostno = $query->param("oldpostno");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($inforum !~ /^[0-9]+$/ || $intopic !~ /^[0-9]+$/ || $inpostno !~ /^[0-9]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inmembername = $query->param ("inmembername");
$inpassword = $query->param ("password");
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$inmembername = $query->cookie("amembernamecookie") if ($inmembername eq "");
$inpassword = $query->cookie("apasswordcookie") if ($inpassword eq "");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "����")
{
	&error("�û�ͶƱ&û�и�ע���û���������ͶƱǰû�е�¼��");
}
else
{
	&getmember($inmembername,"no");
	&error("�û�ͶƱ&û�и�ע���û���") if ($userregistered eq "no");
	&error("�û�ͶƱ&����Ĺ���Ա���룡") if ($inpassword ne $password);
}

$editmembername = $query->param("membername");
$editmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

$action = $query->param("action");

&error("��̳ͶƱ&���ⲻ���ڣ�") unless (-e "${lbdir}forum$inforum/$intopic.pl");

$action = "login" if ($action ne "logmein" && $action ne "process");
&getoneforum($inforum);

&title;

$output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> �����������Զ��û�����ͶƱ�����ٻ��������ǵ���������֣��������Խ�ֹ���Ƿ��ԣ�</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> �� <a href="forums.cgi?forum=$inforum">$forumname</a> �� ���û�ͶƱ<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>~;

if ($action eq "login")
{
	$output .= qq~
<form action=$thisprog method=POST>
<input type=hidden name=action value="logmein">
<input type=hidden name=oldforum value="$inforum">
<input type=hidden name=oldtopic value="$intopic">
<input type=hidden name=oldpostno value="$inpostno">
<input type=hidden name=membername value="$editmembername">
<tr><td bgcolor=$titlecolor $catbackpic colSpan=2 align=center><font color=$fontcolormisc><b>�����ȵ�¼Ȼ��� $editmembername ����ͶƱ(����̳���Ͱ�������)</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colSpan=2 align=center><input type=submit name=submit value="��¼ͶƱ"></td></form></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

elsif ($action eq "logmein")
{
        $inmembmod = "no" if ($membercode eq "amo");
        $mymembercode = $membercode;
	&error("�û�ͶƱ&�����������Ա�����ڱ���ͶƱ") unless ($membercode eq "ad" || $membercode eq "smo" || $inmembmod eq "yes");
	&error("�û�ͶƱ&���ܶ��Լ�ͶƱ") if ($inmembername eq $editmembername);
	&getmember($editmembername);
	&error("�û�ͶƱ&û�и�ע���û�") if ($userregistered eq "no");
	&error("�û�ͶƱ&̳�����ܱ�ͶƱ") if ($membercode eq "ad");
	&error("�û�ͶƱ&ֻ��̳�����ܸ�������ͶƱ��") if (($membercode eq "smo" || $membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo") && $mymembercode ne "ad");

	my $threadtomake = "${lbdir}forum$inforum/$intopic.thd.cgi";
	$inpostno--;
	if (-e $threadtomake)
	{
		open(FILE, $threadtomake);
		my @threads = <FILE>;
		close(FILE);
		if ($inpostno < @threads && $inpostno >= 0)
		{
			(my $membername, $topictitle, my $postipaddresstemp, my $showemoticons, my $showsignature, my $postdate, my $post, my $posticon) = split(/\t/, $threads[$inpostno]);
			&error("�û�ͶƱ&�����Ӳ�����$editmembername����") if (lc($membername) ne  lc($editmembername));
		} else { &error("�û�ͶƱ&��Ӧ�����Ӳ����ڣ�!"); }
	}
	else { &error("�û�ͶƱ&��Ӧ�����Ӳ����ڣ�"); }
	$inpostno++;
	
	$rating = 0 if ($rating eq "");
	if ($jifen eq "") {
		require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
		$jifen = $numberofposts * $ttojf + $numberofreplys * $rtojf - $postdel * $deltojf;
  }
	$rating = -6 if ($rating < -6);
	$rating = $maxweiwang if ($rating > $maxweiwang);

	if ($rating == $maxweiwang) {$pwout = qq~<input type=radio name=pw value="warn" >�����û�(������ 1)~;}
	elsif ($rating == -5) {$pwout = qq~<input type=radio name=pw value="praise" >�����û�(������ 1)����<input type=radio name=pw value="warn">��ֹ�û�����(������Ϊ -6)����<input type=radio name=pw value="worstm">���δ��û�����(������Ϊ -6)~;}
	elsif ($rating == -6) {$pwout = qq~<input type=radio name=pw value="praise" >�ָ��û�(�����ָ��� -5)~;}
	else {$pwout = qq~<input type=radio name=pw value="praise" >�����û�(������ 1)����<input type=radio name=pw value="warn">�����û�(������ 1)����<input type=radio name=pw value="reset">����(����Ϊ 0)����<input type=radio name=pw value="worst">��ֹ����(������Ϊ -6)����<input type=radio name=pw value="worstm">���δ��û�����(������Ϊ -6)~;}
                $max1jf = 50 if ($max1jf eq "");

	$output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>$editmembername Ŀǰ��������: $rating��ӵ�еĻ���Ϊ: $jifen</b></font></td></tr>
<tr><td bgcolor=$miscbackone align=center>
<form action=$thisprog method=POST>
<input type=hidden name=action value=process>
<input type=hidden name=membername value="$editmembername">
<input type=hidden name=oldforum value="$inforum">
<input type=hidden name=oldtopic value="$intopic">
<input type=hidden name=oldpostno value="$inpostno">
<b>* �� �� �� �� *</b><BR>
<input type=radio name=pw value="jfzj" checked> ����/�ͷ���̳���� <input type=text name=numschange size=3 maxsize=3> �� (��������� -$max1jf �� $max1jf ֮��)<BR><BR>
<b>* �� �� �� �� *</b><BR>
$pwout
<BR><BR><BR>
</td></tr>
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc>ͶƱԭ��:<br><textarea size=20 name=reason cols=40 rows=5></textarea></td></tr>
<tr><td bgcolor=$miscbackone align=center>ʹ����̳����Ϣ֪ͨ�û�: <input type=radio name=msgnotify value="yes" checked>�ǡ���<input type=radio name=msgnotify value="no">��</td>~;
	$output .= qq~<tr><td bgcolor=$miscbackone align=center>ʹ���ʼ�֪ͨ�û�: <input type=radio name=notify value="yes">�ǡ���<input type=radio name=notify value="no" checked>��</td>~ if ($emailfunctions eq "on");
	$output .= qq~
<tr><td bgcolor=$miscbacktwo align=center><input type=submit value="ȷ��" name=submit></td></form></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

elsif ($action eq "process")
{
        $inmembmod = "no" if ($membercode eq "amo");
        $mymembercode = $membercode;
	&error("�û�ͶƱ&�����������Ա�����ڱ���ͶƱ") unless ($membercode eq "ad" || $membercode eq "smo" || $inmembmod eq "yes");
	&error("�û�ͶƱ&���ܶ��Լ�ͶƱ") if ($inmembername eq $editmembername);
	&getmember($editmembername);
	&error("�û�ͶƱ&û�и�ע���û�") if ($userregistered eq "no");
	&error("�û�ͶƱ&̳�����ܱ�ͶƱ") if ($membercode eq "ad");
	&error("�û�ͶƱ&ֻ��̳�����ܸ�������ͶƱ��") if (($membercode eq "smo" || $membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo") && $mymembercode ne "ad");
	my $thistime = time;

	my $pw = $query->param("pw");
	my $reason = $query->param("reason");
	my $notify = $query->param("notify");
	my $msgnotify = $query->param("msgnotify");
	&error("�û�ͶƱ&ͶƱ����˵�����ɣ�") if ($reason eq "");
	$reason = &cleaninput($reason);
	$reason =~ s/\|//isg;

	my $oldrating = $rating;
	if ($pw eq "praise")
	{
		$pwmail = $pwmailing = "��������";
		$rating++;
		$ratingname = "������ $oldrating ������ $rating";
	}
	elsif ($pw eq "warn")
	{
		$pwmail = $pwmailing = "��������";
		$rating--;
		$ratingname = "������ $oldrating ������ $rating";
	}
	elsif ($pw eq "reset")
	{
		$pwmail = "��������Ϊ 0";
		$pwmailing = "��������";
		$rating = 0;
		$ratingname = "������ $oldrating ������ $rating";
	}
	elsif ($pw eq "worst" || $pw eq "worstm")
	{
		$pwmail = "�������������";
		$pwmailing = "��������";
		$rating = -6;
		$ratingname = "������ $oldrating ������ $rating";
	}
        elsif ($pw eq 'jfzj') {
		$numschange = $query->param("numschange");
                $max1jf = 50 if ($max1jf eq "");
		&error("�û�ͶƱ&���ͻ��һ��߻��������������") unless ($numschange =~ /^[0-9\-]+$/);
		&error("�û�ͶƱ&һ�ν��ͻ����������ó��� $max1jf �֣���") if (abs($numschange) > $max1jf);
		$oldrating = "���� $jifen";
		$jiangcheng = $numschange >= 0 ?  "����" : "�ͷ�";
		$pwmail = "$jiangcheng���� $numschange��";
		$pwmailing = "$jiangcheng����";
		$jifen += $numschange;
		$numschange = abs($numschange);
		$ratingname = "$jiangcheng���� $numschange";
	}

	$rating = 0 if ($rating eq "");
	$rating = -6 if ($rating < -6);
	$rating = $maxweiwang if ($rating > $maxweiwang);
	$newmembercode = $rating == -6 ? "banned" : ($membercode eq "banned" || $membercode eq "masked") ? "me" : $membercode;
	$newmembercode = "masked" if ($pw eq "worstm");


	my $threadtomake = "${lbdir}forum$inforum/$intopic.thd.cgi";
	$inpostno--;
	if (-e $threadtomake)
	{
		&winlock($threadtomake) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		open(FILE, $threadtomake);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my @threads = <FILE>;
		close(FILE);
		if ($inpostno < @threads && $inpostno >= 0)
		{
			(my $membername, $topictitle, my $postipaddresstemp, my $showemoticons, my $showsignature, my $postdate, my $post, my $posticon) = split(/\t/, $threads[$inpostno]);
			&error("�û�ͶƱ&�����Ӳ�����$editmembername����") if (lc($membername) ne  lc($editmembername));
			$post = "[ADMINOPE=$inmembername|$editmembername|$ratingname|$reason|$thistime]$post";
			$threads[$inpostno] = "$membername\t$topictitle\t$postipaddresstemp\t$showemoticons\t$showsignature\t$postdate\t$post\t$posticon";
			open(FILE, ">$threadtomake");
			flock(FILE, 2) if ($OS_USED eq "Unix");
			foreach (@threads)
			{
				chomp;
				next if ($_ eq "");
				print FILE "$_\n";
			}
			close(FILE);
		} else { &winunlock($threadtomake) if ($OS_USED eq "Nt" || $OS_USED eq "Unix"); &error("�û�ͶƱ&��Ӧ�����Ӳ�����!��"); }
		&winunlock($threadtomake) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	}
	else { &error("�û�ͶƱ&��Ӧ�����Ӳ����ڣ�"); }

	my $memfilename = $editmembername;
	$memfilename =~ s/ /\_/sg;
	$memfilename =~ tr/A-Z/a-z/;
	my $namenumber = &getnamenumber($memfilename);
	&checkmemfile($memfilename,$namenumber);
	if ($membername ne "" && $password ne "")
	{
		my $filetomake = "$lbdir$memdir/$namenumber/$memfilename.cgi";
		$filetomake = &stripMETA($filetomake);
		&winlock($filetomake) if ($OS_USED eq "Nt");
		if (open(FILE0, "+<$filetomake"))
		{
	    		seek(FILE0,0,0);
			flock(FILE0, 2) if ($OS_USED eq "Unix");
			print FILE0 "$membername\t$password\t$membertitle\t$newmembercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5";
			close(FILE0);
		}
		&winunlock($filetomake) if ($OS_USED eq "Nt");
		my $filetomake = "$lbdir$memdir/old/$memfilename.cgi";
		$filetomake = &stripMETA($filetomake);
		if (open(FILE0, ">$filetomake"))
		{
			print FILE0 "$membername\t$password\t$membertitle\t$newmembercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5";
			close(FILE0);
		}
	}
        unlink ("${lbdir}cache/meminfo/$memfilename.pl");
	unlink ("${lbdir}cache/myinfo/$memfilename.pl");

	if ($rating == -6)
	{
		my $filetoopen = "${lbdir}data/banemaillist.cgi";
		open(FILE, ">>$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "$emailaddress\t";
		close(FILE);
		$filetoopen = "${lbdir}data/baniplist.cgi";
		open(FILE, ">>$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "$ipaddress\t";
		close(FILE);
	}
	else
	{
		my $filetoopen = "${lbdir}data/banemaillist.cgi";
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		$emaildata = <FILE>;
		close(FILE);
		chomp($emaildata);
		@emaildata = split(/\t/, $emaildata);
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@emaildata)
		{
			next if ($_ eq "");
			print FILE "$_\t" if ($emailaddress ne $_);
		}
		close(FILE);
		&winunlock($filetoopen) if ($OS_USED eq "Nt");

		$filetoopen = "${lbdir}data/baniplist.cgi";
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		$ipdata = <FILE>;
		close(FILE);
		chomp($ipdata);
		@ipdata = split(/\t/, $ipdata);
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@ipdata)
		{
			next if ($_ eq "");
			print FILE "$_\t" if ($ipaddress ne $_);
		}
		close(FILE);
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
	}

	$trueipaddress = $ENV{"HTTP_CLIENT_IP"};
	$trueipaddress = $ENV{"HTTP_X_FORWARDED_FOR"} if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
	$trueipaddress = "no" if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
	
	$filetomake = "${lbdir}data/userratinglog.cgi";
	open(FILE0, ">>$filetomake");
	print FILE0 "$editmembername\t$inmembername\t$ratingname\t$thistime\t$inforum\t$intopic\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t$reason\t\n";
	close(FILE0);
	
	&addadminlog("���û� $editmembername ������ $ratingname�����ɣ�$reason", $intopic);

	if ($notify eq "yes" && $emailfunctions eq "on") {
		eval("use MAILPROG qw(sendmail);");
		my $membertitleout = $newmembercode eq "banned" ? "����ֹ" : "��ͨ��Ա";
		my $subject = "���Ѿ��� $inmembername $pwmail !";
		my $message = "<br>$homename<br>";
		$message .= "<a href=$boardurl/leobbs.cgi target=_blank>$boardurl/leobbs.cgi</a><br>";
		$message .= "<a href=$boardurl/topic.cgi?forum=$inforum&topic=$intopic target=_blank>$boardurl/topic.cgi?forum=$inforum&topic=$intopic</a><br><br><br>";
		$message .= "���Ѿ��� $inmembername $pwmail !<br><br><br>";
		$message .= "���ݣ�$ratingname<br>";
		$message .= "�����ڵ�״̬��: $membertitleout<br>";
		$message .= "�㱻 $pwmailing ��ԭ����:<br>";
		$message .= "$reason<br><br>";
		$message .= "��������Ϊ�д�, �뷢�Ÿ�<br>";
		$message .= "̳��: $adminemail_in ����ԭ��<br>";
		&sendmail($adminemail_out, $adminemail_out, $emailaddress, $subject, $message);
	}
	if ($msgnotify eq "yes") {
	    $topictitle =~ s/^����������//;
	    &shortmessage($inmembername, $editmembername, "���Ѿ���$pwmail!", "�������Ѿ��� $inmembername $pwmailing! �����ݣ�$ratingname��<br>������ص�������: \[url=topic.cgi?forum=$inforum&topic=$intopic\]���˽���\[\/url\]������ԭ����: $reason��");
	}
	$output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>$editmembername �Ѿ��ɹ���$pwmail</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�������:<br><ul>
<li><a href=topic.cgi?forum=$inforum&topic=$intopic>���ص�ǰ���� </a>$pages
<li><a href=forums.cgi?forum=$inforum>���ص�ǰ��̳</a>
<li><a href=leobbs.cgi>������̳��ҳ</a>
</ul></td></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&output("$boardname - �û�ͶƱ",\$output);
exit;

sub shortmessage #���û�������Ϣ�����ò����������ˡ���ȡ�ˡ����⡢���ݣ�
{
	my ($sendername, $receivemember, $topic, $content) = @_;
	$currenttime = time;
	my $filetomake = "$lbdir$msgdir/in/$receivemember\_msg.cgi";
	$filetomake = &stripMETA($filetomake);
	&winlock($filetomake) if ($OS_USED eq "Nt");
	if (open(FILE, $filetomake))
	{
		flock(FILE, 1) if ($OS_USED eq "Unix");
		@filedata = <FILE>;
		close(FILE);
	}
	open(FILE, ">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE "����������$sendername\tno\t$currenttime\t$topic\t$content\n";
	foreach (@filedata)
	{
		chomp;
		print FILE "$_\n";
	}
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
	undef @filedata;
	return;
}
