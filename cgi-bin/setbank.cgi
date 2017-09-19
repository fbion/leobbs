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
require "data/ebankinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";

$|++;
$thisprog = "setbank.cgi";
$query = new LBCGI;
#&ipbanned;

$action = $query->param('action');
if ($action eq "login")
{
	$inmembername = $query->param("membername");
	$inpassword = $query->param("password");
	$inpasswordtemp = $inpassword;
	if ($inpassword ne "") {
	    eval {$inpassword = md5_hex($inpassword);};
	    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
	    unless ($@) {$inpassword = "lEO$inpassword";}
	}
	&checkverify;
	my $tempmembername = uri_escape($inmembername);
	print "Set-Cookie: adminname=$tempmembername\n";
	print "Set-Cookie: adminpass=$inpassword\n";
}
else
{
	$inmembername = $query->cookie("adminname");
	$inpassword = $query->cookie("adminpass");
}
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
&getmember($inmembername,"no");
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

if (($membercode eq "ad" || ($membercode eq "smo" && $bankadminallow eq "all") || ",$bankmanager," =~ /,$inmembername,/i) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername)))
{
	my %Mode = (
		'setinfo' => \&setinfo,     #�趨���и���ҵ��ָ��
		'setok' => \&setok,         #�����趨
		'editmem' => \&editmem,     #�༭һ���û��Ĵ����
		'editok' => \&editok,       #����༭ֵ
		'empty' => \&empty,         #������н�����־
		'deletelog' => \&deletelog, #ɾ��ָ����־
		'repair' => \&repair,       #�޸�������ʾ����
		'viewloan' => \&viewloan,   #�鿴�����嵥
		'bonus' => \&bonus,         #����Ա�����
		'bonusok' => \&bonusok
		);

	if ($Mode{$action})
	{
		$Mode{$action} -> ();
	}
	else
	{
		&showlog;
	}
	print $output;
}
 
else
{
	my $ipaddress = $ENV{'REMOTE_ADDR'};
	$trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);
	$trueipaddress = $ENV{'HTTP_CLIENT_IP'};
	$ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);
	&logaction($inmembername, "<b>�� $ipaddress ������ $inpasswordtemp ��¼�г��칫��ʧ�ܡ�</b>") if ($inmembername && $inpassword);	
	&ebankadminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;

sub viewloan
{
	open(FILE, $lbdir . "ebankdata/allloan.cgi");
	my @loaninfo = <FILE>;
	close(FILE);
	
	$output = qq~<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=4><font color=#ffffff><b>��ӭ������̳�������� / �����г��칫��</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=4>��<a href=$thisprog>�� ��</a>  >> �鿴�����嵥��</td>
</tr>
<tr>
	<td bgcolor=#eeeeee align=center width=20%>������</td>
	<td bgcolor=#eeeeee align=center width=40%>��������</td>
	<td bgcolor=#eeeeee align=center width=20%>��������</td>
	<td bgcolor=#eeeeee align=center width=20%>��Ѻ����</td>
</tr>~;

	foreach (@loaninfo)
	{
		chomp;
		my ($loaner, $loantime) = split(/,/, $_);
		my $namenumber = &getnamenumber($loaner);
		&checkmemfile($loaner,$namenumber);
		my $loanfile = "$lbdir$memdir/$namenumber/$loaner.cgi";
		if (-e $loanfile)
		{
			open(FILE, $loanfile);
			my $filedata = <FILE>;
			close(FILE);
		
			my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
			my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
			$loantime = &shortdate($loantime);
		
			$output .= qq~<tr>
	<td bgcolor=#ffffff align=center><a href=profile.cgi?action=show&member=~ . uri_escape($loaner) . qq~ target=_blank>$membername</a></td>
	<td bgcolor=#ffffff align=center>$loantime</td>
	<td bgcolor=#ffffff align=center>$myloan</td>
	<td bgcolor=#ffffff align=center>$myloanrating</td>
</tr>~;
		}
	}
	$output .= "</table>";	

	return;	
}

sub bonusok
{
	my $step = $query->param('step');
	$step = 1 if ($step eq "");
	my $bonusmem = $query->param('bonusmem');

	for ("bonustarget", "bonusday", "bonuspost", "bonusnum", "bonusreason")
	{
		${$_} = &cleaninput($query->param($_));
	}
	&seterror("������󸽼�Ҫ����������") if ($bonusday =~ /[^0-9]/ || $bonuspost =~ /[^0-9]/);
	&seterror("û�������������������������") if ($bonusnum !~ /^[0-9]+$/);
	&seterror("�������뷢��������ɣ�") if ($bonusreason eq "");

	opendir(DIR, "$lbdir$memdir/old");
	my @memberfiles = readdir(DIR);
	close(DIR);
	@memberfiles = grep(/\.cgi$/i, @memberfiles);

	my $currenttime = time;
	for ($i = ($step - 1) * 200; $i < $step * 200 && $i < @memberfiles; $i++)
	{
		&winunlock($lastfile) if (($OS_USED eq "Unix" || $OS_USED eq "Nt") && $lastfile ne "");
		($nametocheck,$no) = split (/\./,$memberfiles[$i]);
		my $namenumber = &getnamenumber($nametocheck);
		&checkmemfile($nametocheck,$namenumber);
		$lastfile = $lbdir . $memdir . "/$namenumber/" . $memberfiles[$i];
		&winlock($lastfile) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");
		open(FILE, $lastfile);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my $filedata = <FILE>;
		close(FILE);
		
		my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
		my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
		my ($numberofposts, $numberofreplys) = split(/\|/, $numberofposts);

		next if ($membercode eq "banned" || $membercode eq "masked");
		next if ($bonustarget ne "all" && $mystatus != 1);
		next if ($bonusday ne "" && $currenttime - $joineddate < $bonusday * 86400);
		next if ($bonuspost ne "" && $numberofposts + $numberofreplys < $bonuspost);

		$mymoney += $bonusnum;
		open(FILE, ">$lastfile");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
		close(FILE);
		&winunlock($lastfile) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");
		$bonusmem++;
	        unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
		unlink ("${lbdir}cache/myinfo/$nametocheck.pl");

		$lastfile = $memberfiles[$i];
		$lastfile =~ s/\.cgi$//isg;
		&bankmessage($lastfile, "<font color=red>���֪ͨ</font>", "����$inmembername ��$bonusreason�����ɣ��������� $bonusnum $moneyname�ĺ��������������ֽ�");
		$lastfile = "";
	}
	&winunlock($lastfile) if (($OS_USED eq "Unix" || $OS_USED eq "Nt") && $lastfile ne "");

	if ($i < @memberfiles - 1)
	{
		#������һ��
		$step++;
		$output = qq~<form name=MAINFORM action=$thisprog?step=$step method=POST>
<input type=hidden name=action value=bonusok>
<input type=hidden name=step value=$step>
<input type=hidden name=bonustarget value="$bonustarget">
<input type=hidden name=bonusmem value="$bonusmem">
<input type=hidden name=bonusday value="$bonusday">
<input type=hidden name=bonuspost value="$bonuspost">
<input type=hidden name=bonusnum value="$bonusnum">
<input type=hidden name=bonusreason value="$bonusreason">
</form>
<script language="JavaScript">
setTimeout("MAINFORM.submit()", 1000);
</script>
�������������û���Զ�ǰ������<a href="javascript: MAINFORM.submit()">�������</a>~;
	}
	else
	{
		$bonustarget = $bonustarget eq "all" ? "����ע���Ա" : "�������пͻ�";
		$bonusday = "ע�� $bonusday ������" if ($bonusday ne "");
		$bonuspost = "���� $bonuspost ƪ����" if ($bonuspost ne "");
		$bonusday = $bonusday ne "" && $bonuspost ne "" ? "$bonusday��$bonuspost��" : $bonusday ne "" || $bonuspost ne "" ? "$bonusday$bonuspost��" : "";
		&logaction($inmembername, "<font color=red>��$bonusreason�����ɸ�$bonusday$bonustarget�����ܹ� $bonusmem �� $bonusnum $moneyname �ĺ����");
		$output = qq~
<table width=100% cellpadding=6 cellspacing=0>
<tr><td bgcolor=#2159C9><font color=#ffffff><b>��ӭ������̳�������� / �װ������г��칫��</b></td></tr>
<tr><td align=center><br><b><font color=red>��$bonusday$bonustarget�ĺ��������ɣ��ܹ�������� $bonusmem ��!</font></b></td></tr>
</table>~;
	}
	return;
}

sub repair
{
	my $step = $query->param('step');
	$step = 1 unless ($step);

	my %ordersaves;
	if ($step == 1)
	{
		&setbankonoff("off");
		unlink($lbdir . "ebankdata/allsaves.cgi");
		unlink($lbdir . "ebankdata/allloan.cgi");
		unlink($lbdir . "ebankdata/order.cgi");
		unlink(&lockfilename($lbdir . "ebankdata/order.cgi") . ".lck");
	}
	else
	{
		#��ȡ����������
		open(FILE, $lbdir . "ebankdata/order.cgi");
		my @orderdata = <FILE>;
		close(FILE);
		foreach (@orderdata)
		{
			chomp;
			my ($tempuser, $tempsave) = split(/\t/, $_);
			$ordersaves{$tempuser} = $tempsave if ($tempuser ne "");
		}
	}
	opendir(DIR, "${lbdir}ebankdata/log");
	my @memberfiles = readdir(DIR);
	close(DIR);
	@memberfiles = grep(/\.cgi$/i, @memberfiles);

	my $stepusers = 0;
	my $stepsaves = 0;
	for ($i = ($step - 1) * 200; $i < $step * 200 && $i < @memberfiles; $i++)
	{
		($nametocheck,$no) = split(/\./,$memberfiles[$i]);
		my $namenumber = &getnamenumber($nametocheck);
		&checkmemfile($nametocheck,$namenumber);
		my $filetoopen = $lbdir . $memdir . "/$namenumber/" . $memberfiles[$i];
		open(FILE, $filetoopen);
		my $filedata = <FILE>;
		close(FILE);
		
		my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
		my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
		
		if ($mystatus)
		{
			$membername =~ s/ /\_/sg;
			$membername =~ tr/A-Z/a-z/;
			$stepusers++;
			$stepsaves += $mysaves;
			$ordersaves{$membername} = $mysaves;
			if ($myloan)
			{
				my $filetomake = $lbdir . "ebankdata/allloan.cgi";
				&winlock($filetomake) if ($OS_USED eq "Nt");
				open(FILE, ">>$filetomake");
				flock(FILE, 2) if ($OS_USED eq "Unix");
				print FILE "$membername,$myloantime\n";
				close(FILE);
				&winunlock($filetomake) if ($OS_USED eq "Nt");
			}
		}
	}
	&updateallsave($stepusers, $stepsaves);
	#����������������������ۺ�
	my @orderusers = sort {$ordersaves{$a}<=>$ordersaves{$b}} keys(%ordersaves);
	open(FILE, ">" . $lbdir . "ebankdata/order.cgi");
	for ($k = 1; $k <= $bankmaxdisplay * 2; $k++)
	{
		$j = @orderusers - $k;
		last if ($j < 0);
		print FILE $orderusers[$j] . "\t" . $ordersaves{$orderusers[$j]} . "\n" if ($ordersaves{$orderusers[$j]});
	}
	close(FILE);

	if ($i < @memberfiles - 1)
	{
		#������һ��
		$step++;
		$output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog?action=repair&step=$step"><br>�������������û���Զ�ǰ������<a href=$thisprog>�������</a>~;
	}
	else
	{
		#�����¼����������
		my $filetomake = $lbdir . "ebankdata/allloan.cgi";
		open(FILE, $filetomake);
		my @loaninfo = <FILE>;
		close(FILE);
		my %loantimes;
		foreach (@loaninfo)
		{
			chomp;
			my ($loaner, $loantime) = split(/,/, $_);
			$loantimes{$loaner} = $loantime if ($loaner ne "");
		}
		
		my @loaners = sort {$loantimes{$a}<=>$loantimes{$b}} keys(%loantimes);
		
		&winlock($filetomake) if ($OS_USED eq "Nt");
		open(FILE, ">$filetomake");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@loaners)
		{
			print FILE $_ . "," . $loantimes{$_} . "\n";
		}
		close(FILE);
		&winunlock($filetomake) if ($OS_USED eq "Nt");

		&setbankonoff("on");
		$output = qq~
<table width=100% cellpadding=6 cellspacing=0>
<tr><td bgcolor=#2159C9><font color=#ffffff><b>��ӭ������̳�������� / �װ������г��칫��</b></td></tr>
<tr><td align=center><br><b>������ʾ�޸����!</b></td></tr>
</table>~;
	}

	return;
}

sub showlog
{
	my $page = $query->param('page');
	$page = 1 unless ($page);
	my $type = $query->param('type');
	$type = "name" unless($type eq "key" || $type eq "time");
	my $key = $query->param('key');

	open(FILE, $lbdir . "ebankdata/alllogs.cgi");
	my @ebanklogs = <FILE>;
	close(FILE);

	if ($key ne "")
	{#ѡ��ָ����¼
		if ($type eq "name")
		{
			$key =~ s/ /\_/sg;
			@ebanklogs = grep(/^$key\t.+\t.+$/i, @ebanklogs);
		}
		elsif ($type eq "time")
		{
			my ($begin, $end);
			for ($begin = 0; $begin < @ebanklogs; $begin++)
			{
				my ($temp1, $temptime, $temp2) = split(/\t/, $ebanklogs[$begin]);
				$temptime = &shortdate($temptime + $timezone * 3600 + $timedifferencevalue * 3600);
				last if ($key eq $temptime);
			}
			for ($end = @ebanklogs - 1; $end >= $begin - 1; $end--)
			{
				my ($temp1, $temptime, $temp2) = split(/\t/, $ebanklogs[$end]);
				$temptime = &shortdate($temptime + $timezone * 3600 + $timedifferencevalue * 3600);
				last if ($key eq $temptime);
			}
			if ($begin > $end)
			{
				undef(@ebanklogs);
			}
			else
			{
				@ebanklogs = @ebanklogs[$begin..$end];
			}
		}
		else
		{
			@ebanklogs = grep(/^.+\t.+\t.*$key.*$/i, @ebanklogs);
		}
	}

	my $allpages = int(@ebanklogs / 25) + 1;
	$page = 1 if ($page < 1);
	$page = $allpages if ($page > $allpages);
	my $showpage = "";
	if ($allpages > 1)
	{
		$showpage .= qq~��¼�� <b>$allpages</b> ҳ ~;
		$i = $page - 1;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();" title="��һҳ"><<</span> ~ if ($i > 0);
		$showpage .= "[ ";
		$i = $page - 3;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">��</span> ~ if ($i > 0);
		$i++;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i > 0);
		$i++;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i > 0);
		$i++;
		$showpage .= qq~<font color=#990000>$i</font> ~;
		$i++;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i <= $allpages);
		$i++;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i <= $allpages);
		$i++;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">��</span> ~ if ($i <= $allpages);
		$showpage .= "] ";
		$i = $page + 1;
		$showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();" title="��һҳ">>></span> ~ if ($i <= $allpages);
		$showpage .= "��ֱ����ת���� <input type=text name=page size=2 value=$page style='text-align: right' OnMouseOver='this.focus();' OnFocus='this.select();'> ҳ <input type=submit value='Go'>";
	}
	else
	{
		$showpage = "��¼ֻ�� <b>1</b> ҳ";
	}

	$output = qq~
<script language="JavaScript">
function goempty()
{
	if (clearday = prompt("������Ҫ��ն�������ǰ����־��", "30"))
		location.href = "$thisprog?action=empty&day=" + clearday;
}
</script>
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=4><font color=#ffffff><b>��ӭ������̳�������� / �װ������г��칫��</b></td>
</tr>
<form name=EDIT action=$thisprog method=POST>
<input type=hidden name=action value="editmem">
<tr>
	<td bgcolor=#cccccc width=20%>��<a href=$thisprog?action=setinfo>�趨����ҵ��</a></td>
	<td bgcolor=#cccccc width=20%><a href=$thisprog?action=repair OnClick="return confirm('�⽫��ʱ�Զ��ر����У�������ɻ��Զ����¿��š�\\nһ��������д˲������Ƿ������');">���¼���ͳ�ƺ�����</a></td>
	<td bgcolor=#cccccc width=20%><a href=$thisprog?action=bonus><font color=red>�����пͻ������</font></a></td>
	<td bgcolor=#cccccc width=45% align=right>���ٱ༭��Ա�ʻ��� <input type=text size=10 name=memid value=�û��� OnMouseOver="this.focus();" OnFocus="this.select();">��<input type=submit value=�༭></td>
</tr>
</form>
<form name=MAINFORM action=$thisprog method=POST>
<tr>
	<td align=left bgcolor=#ffffff>��<a href=$thisprog?action=viewloan><font color=#ff7700>�����嵥</font></a></td> 
	<td align=center colspan=3 bgcolor=#ffffff>$showpage</td>
</tr>
<tr>
	<td bgcolor=#eeeeee>��<b>������־</b></td>
	<td bgcolor=#eeeeee><select name=type><option value="name">����ָ����Ա</option><option value="time">�����ض�����</option><option value="key">������������</option></select></td>
	<td bgcolor=#eeeeee align=right colspan=2><input name=key value="$key" type=text size=20 OnMouseOver="this.focus();" OnFocus="this.select();">��<input type=submit value=����>����<a href="javascript:goempty()">��չ��ڽ��׼�¼</a>��</td>	
</tr>
</form>
<form name=DELETE action=$thisprog method=POST>
<input type=hidden name=action value=deletelog>
<tr>
	<td bgcolor=#ffffff>��<b>Ӫҵ״��</b></td>~;
	if ($key ne "")
	{
		$output .= qq~<td bgcolor=#ffffff colspan=3><table width=98%><td><i><font color=#0000ee>�������������������ڵĸ�ʽ������ 2002/09/29 ��������ʽ��</font></i></td><td align=right><a href="$thisprog">����ȫ����־��ʾ</a></td></table></td>~;
	}
	else
	{
		$output .= qq~<script language="JavaScript">
function CheckAll() {for (var i = 0; i < DELETE.dellogid.length; i++) {DELETE.dellogid[i].checked = true;}}
function FanAll() {for (var i = 0; i < DELETE.dellogid.length; i++) {DELETE.dellogid[i].checked = !DELETE.dellogid[i].checked;}}
</script>
<td bgcolor=#ffffff colspan=3><table width=98%><td><i><font color=#0000ee>�������������������ڵĸ�ʽ������ 2002/09/29 ��������ʽ��</font></i></td><td align=right><input type=button OnClick="CheckAll();" value="ȫѡ"> <input type=button OnClick="FanAll();" value="��ѡ">��<a href="JavaScript:DELETE.submit();" OnClick="return confirm('�⽫ɾ����ѡ���Ľ�����־���Ƿ������');">ɾ��ѡ���ļ�¼</a></td></table></td>~;
	}
	$output .= qq~</tr>~;

	my $lognum = @ebanklogs - ($page - 1) * 25;
	my ($logcustomer, $logtime, $logevent);
	for ($i = $lognum - 1; $i >= $lognum - 25 && $i >= 0; $i--)
	{
		chomp($ebanklogs[$i]);
		($logcustomer, $logtime, $logevent) = split(/\t/, $ebanklogs[$i]);
		$logtime = &dateformatshort($logtime + $timezone * 3600 + $timedifferencevalue * 3600);
		$logcustomer = qq~<a href=profile.cgi?action=show&member=~ . uri_escape($logcustomer) . qq~ target=_blank>$logcustomer</a>~ unless ($logcustomer =~ /�����Զ��������/);
		$output .= qq~<tr>
	<td bgcolor=#ffffff>��$logcustomer</td>
	<td bgcolor=#ffffff>$logtime</td>~;
		if ($key ne "")
		{
			$output .= qq~<td bgcolor=#ffffff colspan=2>$logevent</td>~;
		}
		else
		{
			my $j = $i + 1;
			$output .= qq~<td bgcolor=#ffffff colspan=2><table width=98%><td>$logevent</td><td align=right><input type=checkbox name=dellogid value=$j></td></table></td>~;
		}
		$output .= qq~</tr>~;
	}

	$output .= qq~</form>	
<form action=$thisprog method=POST>
<input type=hidden name=action value="search">
<tr>
	<td bgcolor=#eeeeee>��<b>������־</b></td>
	<td bgcolor=#eeeeee><select name=type><option value="name">����ָ����Ա</option><option value="time">�����ض�����</option><option value="key">������������</option></select></td>
	<td bgcolor=#eeeeee align=right colspan=2><input name=key value="$key" type=text size=20 OnMouseOver="this.focus();" OnFocus="this.select();">��<input type=submit value=����>����<a href="javascript:goempty()">��չ��ڽ��׼�¼</a>��</td>	
</tr>
<tr>
	<td align=left bgcolor=#ffffff>��<a href=$thisprog?action=viewloan><font color=#ff7700>�����嵥</font></a></td> 
	<td align=center colspan=3 bgcolor=#ffffff>$showpage</td>
</tr>
</form>
</table>~;

	$output =~ s/<option value="$type">/<option value="$type" selected>/g;
	return;
}

sub bonus
{
	$output = qq~<form action=$thisprog method=POST><input type=hidden name=action value="bonusok">
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>��ӭ������̳�������� / �����г��칫��</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=2>��<a href=$thisprog>�� ��</a>  >> <font color=red>���ͻ��������</font></td>
</tr>
<tr>
	<td bgcolor=#ffffff width=35%>��������󣺡�</td>
	<td bgcolor=#ffffff>��<input type=radio name=bonustarget value="user" checked>���������пͻ�(���˺ű�����)��<input type=radio name=bonustarget value="all">������ע���Ա(�����Ժ�����)</td>
</tr>
<tr>
	<td bgcolor=#ffffff>�����󸽼�Ҫ�󣺡�</td>
	<td bgcolor=#ffffff>��ע�� <input type=text size=3 name=bonusday> ������ ���ҷ��� <input type=text size=4 name=bonuspost> ���ϡ�(����Ҫ��������)</td>
</tr>
<tr>
	<td bgcolor=#ffffff>����������</td>
	<td bgcolor=#ffffff>��<input type=text size=12 name=bonusnum> $moneyname</td>
</tr>
<tr>
	<td bgcolor=#ffffff>��������ɣ���</td>
	<td bgcolor=#ffffff>��<input type=text size=50 name=bonusreason></td>
</tr>
<tr>
	<td bgcolor=#ffffff align=center><input type=submit value=������></td>
	<td bgcolor=#ffffff align=center><input type=reset value=�ء���></td>
</tr>
</table></form>~;
	return;	
}

sub deletelog
{
	my @dellogid = $query->param('dellogid');
	
	my $delnum = 0;
	my $currenttime = time;
	my $filetoopen = $lbdir . "ebankdata/alllogs.cgi";
	&winlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	flock(FILE, 1) if ($OS_USED eq "Unix");
	open(FILE, $filetoopen);
	my @ebanklogs = <FILE>;
	close(FILE);	
	foreach (@dellogid)
	{
		if ($_ > 0 && $_ <= @ebanklogs)
		{
			$ebanklogs[$_ - 1] = "";
			$delnum++;
		}
	}
	unless ($delnum)
	{
		&winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
		&seterror("��ѡ��Ҫɾ�������м�¼�Ժ��ٲ�����");
	}
	open(FILE, ">$filetoopen");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach (@ebanklogs)
	{
		chomp;
		print FILE $_ . "\n" if ($_);
	}
	print FILE "$inmembername\t$currenttime\t<b>ɾ���� $delnum �����н�����־��</b>\n";
	close(FILE);
	&winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	
	$output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>���ɹ���ɾ���� $delnum �����н�����־��<br>�������������û���Զ����أ���<a href=$thisprog>�������</a>~;
	return;	
}

sub setinfo
{
	my $banksave100rate = $banksaverate * 100;
	my $bankloan100rate = $bankloanrate * 100;
	my $banktrans100rate = $banktransrate * 100;
	my $bankpost100rate = $bankpostrate * 100;

	$output = qq~<form action=$thisprog method=POST><input type=hidden name=action value="setok">
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>��ӭ������̳�������� / �����г��칫��</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=2>��<a href=$thisprog>�� ��</a>  >> �趨����ҵ�������</td>
</tr>
<tr>
	<td bgcolor=#ffffff width=35%>������״̬����</td>
	<td bgcolor=#ffffff>��<input type=radio name=bankopen value="on">���������š�<input type=radio name=bankopen value="off">����ʱ�ر�</td>
</tr>
<tr>
	<td bgcolor=#ffffff>���������ƣ���</td>
	<td bgcolor=#ffffff>��<input type=text size=20 name=bankname value="$bankname"></td>
</tr>
<tr>
	<td bgcolor=#ffffff>���г����ƣ���</td>
	<td bgcolor=#ffffff>��<input type=text size=20 name=bankmanager value="$bankmanager">����Ӣ�Ķ��ż����λ�г�</td>
</tr>
<tr>
	<td bgcolor=#ffffff>�����л�ӭ��ʾ����</td>
	<td bgcolor=#ffffff>��<input type=text size=60 name=bankmessage value="$bankmessage"></td>
</tr>
<tr>
	<td bgcolor=#ffffff>����������ʣ���</td>
	<td bgcolor=#ffffff>��<input type=text size=4 name=banksaverate value="$banksave100rate"> %��<i>Ĭ��Ϊ 0.88%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>��ת�ʻ��������Ҫ����ֵ����</td>
	<td bgcolor=#ffffff>��<input type=text size=6 name=banktransneed value="$banktransneed"></td>
</tr>
<tr>
	<td bgcolor=#ffffff>��ת���������ʣ�</td>
	<td bgcolor=#ffffff>��<input type=text size=6 name=banktransrate value="$banktrans100rate"> %��<i>Ĭ��Ϊ 10%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>������������ʣ�</td>
	<td bgcolor=#ffffff>��<input type=text size=6 name=bankpostrate value="$bankpost100rate"> %��<i>Ĭ��Ϊ 20%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>���Ƿ񿪷Ŵ���ܣ�</td>
	<td bgcolor=#ffffff>��<input type=radio name=bankallowloan value="yes">�����š�����<input type=radio name=bankallowloan value="no">���ر�</td>
</tr>
<tr>
	<td bgcolor=#ffffff>��������������ޣ�</td>
	<td bgcolor=#ffffff>��<input type=text size=2 name=bankloanmaxdays value="$bankloanmaxdays"> �졡<i>Ĭ��Ϊ 7</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>�����������ʣ���</td>
	<td bgcolor=#ffffff>��<input type=text size=4 name=bankloanrate value="$bankloan100rate"> %��<i>Ĭ��Ϊ 1.88%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>��ÿ��������ߵ�Ѻ���������</td>
	<td bgcolor=#ffffff>��<input type=text size=6 name=bankrateloan value="$bankrateloan"> $moneyname</td>
</tr>
<tr>
	<td bgcolor=#ffffff>�����ʽ�������޶��</td>
	<td bgcolor=#ffffff>��<input type size=10 name=bankmaxdeal value="$bankmaxdeal"> $moneyname��<i>Ĭ��Ϊ 500000</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>�����ʽ�������޶��</td>
	<td bgcolor=#ffffff>��<input type size=10 name=bankmindeal value="$bankmindeal"> $moneyname��<i>Ĭ��Ϊ 10</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>����ҳ��ʾ���û�����������</td>
	<td bgcolor=#ffffff>��<input type size=4 name=bankmaxdisplay value="$bankmaxdisplay">��<i>Ĭ��Ϊ 10 �����ܳ��� 20</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>��24Сʱ������״�������</td>
	<td bgcolor=#ffffff>��<input type size=4 name=bankmaxdaydo value="$bankmaxdaydo">��<i>Ĭ��Ϊ 5 �����ܳ��� 10����̳����Ч</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>�����˴�������¼��������</td>
	<td bgcolor=#ffffff>��<input type size=4 name=banklogpriviate value="$banklogpriviate">��<i>Ĭ��Ϊ 6 �����ܳ��� 20</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>������������л�Ա��</td>
	<td bgcolor=#ffffff>��<select name=bankadminallow><option value="allad">����̳�����г�</option><option value="all">�����ܰ�����̳�����г�</option></select></td>
</tr>
<tr>
	<td bgcolor=#ffffff align=center><input type=submit value=�ᡡ��></td>
	<td bgcolor=#ffffff align=center><input type=reset value=�ء���></td>
</tr>
</table></form>~;

	$output =~ s/<input type=radio name=bankopen value="$bankopen">/<input type=radio name=bankopen value="$bankopen" checked>/g;
	$output =~ s/<input type=radio name=bankrateuse value="$bankrateuse">/<input type=radio name=bankrateuse value="$bankrateuse" checked>/g;
	$output =~ s/<input type=radio name=bankallowloan value="$bankallowloan">/<input type=radio name=bankallowloan value="$bankallowloan" checked>/g;
	$output =~ s/<option value="$bankadminallow">/<option value="$bankadminallow" selected>/g;

	return;
}

sub editmem
{
	my $memid = $query->param('memid');
	&seterror("û������༭���ʻ�����") if ($memid eq "");
	&seterror("�ʻ������зǷ��ַ���") if (($memid =~ m/\//) || ($memid =~ m/\\/) || ($memid =~ m/\.\./));
	&getmember($memid, "no");
	&seterror("�û� $memid �����ڣ�") if ($userregistered eq "no");
	($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
	&seterror("�û� $memid û���ڱ��п�����") unless ($mystatus);

	my $loanoutput;
	if ($myloan)
	{
		$loanoutput = qq~�û��ӱ��д��� $myloan $moneyname����<input type=checkbox name=clearloan value="yes">������û��Ĵ����¼��~;
	}
	else
	{
		$loanoutput = qq~�û��ڱ���û�д���~;
	}

	$output = qq~<form action=$thisprog method=POST><input type=hidden name=action value="editok"><input type=hidden name=memid value="$memid">
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>��ӭ������̳�������� / �װ������г��칫��</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=2>��<a href=$thisprog>�� ��</a>  >> �༭ $memid �Ĵ�������ϣ�</td>
</tr>
<tr>
	<td bgcolor=#ffffff width=40%>���û���������</td>
	<td bgcolor=#ffffff>��<input type=text size=15 name=newsavenums value="$mysaves"> $moneyname</td>
</tr>
<tr>
	<td bgcolor=#ffffff>���û����������</td>
	<td bgcolor=#ffffff>��$loanoutput</td>
</tr>
<tr>
	<td bgcolor=#ffffff>���޸�ȡ�����룺��</td>
	<td bgcolor=#ffffff>��<input type=text name=getpass size=15> (�������޸�)</td>
</tr>
<tr>
	<td bgcolor=#ffffff>���û��˻�״̬����</td>
	<td bgcolor=#ffffff>��<input name=accountstats type=radio value="on"> ����ʹ�á���<input name=accountstats value="off" type=radio> ��ʱ����</td>
</tr>
<tr>
	<td bgcolor=#ffffff align=center><input type=submit value=�ޡ���></td>
	<td bgcolor=#ffffff align=center><input type=reset value=�ء���></td>
</tr>
</table></form>~;

	if ($mystatus == 1)
	{
		$output =~ s/value="on"/value="on" checked/g;
	}
	else
	{
		$output =~ s/value="off"/value="on" checked/g;
	}

	return;
}

sub setok
{
	my $newbankopen = $query->param('bankopen');
	my $newbankname = $query->param('bankname');
	my $newbankmanager = $query->param('bankmanager');
	my $newbankmessage = $query->param('bankmessage');
	my $newbanksaverate = $query->param('banksaverate');
	my $newbanktransneed = $query->param('banktransneed');
	my $newbanktransrate = $query->param('banktransrate');
	my $newbankpostrate = $query->param('bankpostrate');
	my $newbankallowloan = $query->param('bankallowloan');
	my $newbankloanmaxdays = $query->param('bankloanmaxdays');
	my $newbankloanrate = $query->param('bankloanrate');
	my $newbankrateloan = $query->param('bankrateloan');
	my $newbankmaxdeal = $query->param('bankmaxdeal');
	my $newbankmindeal = $query->param('bankmindeal');
	my $newbankmaxdisplay = $query->param('bankmaxdisplay');
	my $newbankmaxdaydo = $query->param('bankmaxdaydo');
	my $newbanklogpriviate = $query->param('banklogpriviate');
	my $newbankadminallow = $query->param('bankadminallow');

	$newbankopen = "on" if ($newbankopen ne "off");
	&seterror("��û�������г�������") if ($newbankmanager eq "");
	$newbankmanager = &unHTML($newbankmanager);
	&seterror("��û�������������ƣ�") if ($newbankname eq "");
	$newbankname = &unHTML($newbankname);
	$newbankmessage = &unHTML($newbankmessage);
	&seterror("����������������") if ($newbanksaverate =~ /[^0-9\.]/ or $newbanksaverate eq "");
	&seterror("���������̫�ߣ�") if ($newbanksaverate > 10);
	$newbanksaverate /= 100;
	&seterror("ת�ʻ��������Ҫ����ֵ�������") if ($newbanktransneed =~ /[^0-9]/ or $newbanktransneed eq "");
	&seterror("ת�ʻ����������") if ($newbanktransrate =~ /[^0-9\.]/ or $newbanktransrate eq "");
	$newbanktransrate /= 100;
	&seterror("�������������") if ($newbankpostrate =~ /[^0-9\.]/ or $newbankpostrate eq "");
	$newbankpostrate /= 100;
	$newbankallowloan = "yes" if ($newbankallowloan ne "no");
	&seterror("��������������������") if ($newbankloanmaxdays =~ /[^0-9]/ or $newbankloanmaxdays eq "");
	&seterror("�����������������") if ($newbankloanrate =~ /[^0-9\.]/ or $newbankloanrate eq "");
	$newbankloanrate /= 100;
	&seterror("�������ʱ�����ڴ�����ʣ�") if ($newbankloanrate <= $newbanksaverate);
	&seterror("ÿ��������ߵ�Ѻ���������������") if ($newbankrateloan =~ /[^0-9]/ or $newbankrateloan eq "");
	&seterror("���ʽ�������޶��������") if ($newbankmaxdeal =~ /[^0-9]/ or $newbankmaxdeal eq "");
	&seterror("���ʽ�������޶��������") if ($newbankmindeal =~ /[^0-9]/ or $newbankmindeal eq "");
	&seterror("���ʽ�������޶�Ӧ�ô��ڵ��ʽ�������޶") if ($newbankmaxdeal <= $newbankmindeal);
	&seterror("��ҳ��ʾ���û��������������") if ($newbankmaxdisplay =~ /[^0-9]/ or $newbankmaxdisplay eq "");
	&seterror("��ҳ��ʾ���û����������࣡") if ($newbankmaxdisplay > 20);
	&seterror("24Сʱ������״����������") if ($newbankmaxdaydo =~ /[^0-9]/ or $newbankmaxdaydo eq "");
	&seterror("24Сʱ������״������࣡") if ($newbankmaxdaydo > 10);
	&seterror("���˴�����߼�¼�����������") if ($newbanklogpriviate =~ /[^0-9]/ or $newbanklogpriviate eq "");
	&seterror("���˴�����߼�¼�������࣡") if ($newbanklogpriviate > 20);
	$newbankadminallow = "allad" unless ($newbankadminallow eq "all" or $newbankadminallow eq "manager");

	my $filetomake = $lbdir . "data/ebankinfo.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, ">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE qq~\# EbankMX For LB Plus is Powered By 94Cool.Net BigJim
\$bankopen = "$newbankopen";
\$bankname = "$newbankname";
\$bankmanager = "$newbankmanager";
\$bankmessage = "$newbankmessage";
\$banksaverate = $newbanksaverate;
\$banktransneed = $newbanktransneed;
\$banktransrate = $newbanktransrate;
\$bankpostrate = $newbankpostrate;
\$bankallowloan = "$newbankallowloan";
\$bankloanmaxdays = $newbankloanmaxdays;
\$bankloanrate = $newbankloanrate;
\$bankrateloan = $newbankrateloan;
\$bankmaxdeal = $newbankmaxdeal;
\$bankmindeal = $newbankmindeal;
\$bankmaxdisplay = $newbankmaxdisplay;
\$bankmaxdaydo = $newbankmaxdaydo;
\$banklogpriviate = $newbanklogpriviate;
\$bankadminallow = "$newbankadminallow";
1;~;
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");

	$output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>�������������û���Զ����أ���<a href=$thisprog>�������</a>~;
	return;
}

sub editok
{
	my $memid = $query->param('memid');
	&seterror("û������༭���ʻ�����") if ($memid eq "");
	&seterror("�ʻ������зǷ��ַ���") if (($memid =~ m/\//) || ($memid =~ m/\\/) || ($memid =~ m/\.\./));
	$memid =~ s/ /\_/sg;
	$memid =~ tr/A-Z/a-z/;

	my $newsavenums = $query->param('newsavenums');
	my $clearloan = $query->param('clearloan');
	my $accountstats = $query->param('accountstats');
	my $getpass = $query->param('getpass');
	$getpass =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

	$memid = &stripMETA($memid);
	my $namenumber = &getnamenumber($memid);
	&checkmemfile($memid,$namenumber);
	my $filetoopen = "$lbdir$memdir/$namenumber/$memid.cgi";
	if (-e $filetoopen)
	{
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my $filedata = <FILE>;
		close(FILE);
		chomp($filedata);
		my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
		my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);

		if ($mystatus)
		{
			if ($mysaves != $newsavenums)
			{			
				&logaction($inmembername, "�༭�û� $membername �Ĵ��� $mysaves $moneyname�� $newsavenums $moneyname��");
				&updateallsave(0, $newsavenums - $mysaves);
				$mysaves = $newsavenums;
				&order($memid, $newsavenums);
			}

			if ($myloan && $clearloan eq "yes")
			{		
				&logaction($inmembername, "������û� $membername $myloan $moneyname�Ĵ����¼��");
				$myloan = 0;
				$myloantime = "";
				$myloanrating = 0;
			}

			if ($getpass ne "")
			{
				$bankgetpass = $getpass;
				&logaction($inmembername, "<b>�޸����û� $membername ��ȡ�����롣</b>");
			}

			if ($accountstats eq "on" && $mystatus == -1)
			{
				&bankmessage($memid, "�ⶳ֪ͨ", "����$bankname���˻��Ѿ���$inmembername�ⶳ��");
				&logaction($inmembername, "<font color=green>����˶��û� $membername �ʻ��Ķ��ᡣ</font>");
				$mystatus = 1;
			}
			elsif ($accountstats eq "off" && $mystatus == 1)
			{
				&bankmessage($memid, "����֪ͨ", "����$bankname���˻��Ѿ���$inmembername���ᣬ����������������ϵ��");
				&logaction($inmembername, "<font color=red>��ʱ�������û� $membername ���ʻ���</font>");
				$mystatus = -1;
			}

			$ebankdata = "$mystatus,$mysaves,$mysavetime,$myloan,$myloantime,$myloanrating,$mybankdotime,$bankgetpass,$bankadd2,$bankadd3,$bankadd4,$bankadd5";

			if (($membername ne "") && ($password ne ""))
			{
				if (open(FILE, ">$filetoopen"))
				{
					flock(FILE, 2) if ($OS_USED eq "Unix");
					$lastgone = time;
					print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
					close(FILE);
				}
			}
			&winunlock($filetoopen) if ($OS_USED eq "Nt");
		}
		else
		{
			&winunlock($filetoopen) if ($OS_USED eq "Nt");
			&seterror("�û� $memid û���ڱ��п�����");
		}
	}
	else
	{
		&seterror("�û� $memid �����ڣ�");
	}

	$output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>�������������û���Զ����أ���<a href=$thisprog>�������</a>~;
	return;
}

sub empty
{
	my $clearday = $query->param("day");
	$clearday = 30 if ($clearday !~ /^[0-9]+$/);
	my $currenttime = time;
	my $cleartime = $currenttime - $clearday * 86400;
	my $filetomake = $lbdir . "ebankdata/alllogs.cgi";
	&winlock($filetomake) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");
	open(FILE, $filetomake);
	flock(FILE, 1)  if ($OS_USED eq "Unix");
	my @alllogs = <FILE>;
	close(FILE);
	my $deletenum = 0;
	open(FILE, ">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach (@alllogs)
	{
		chomp;
		my (undef, $logtime, undef) = split(/\t/, $_);
		if ($logtime < $cleartime)
		{
			$deletenum++;
		}
		else
		{
			print FILE "$_\n";
		}
	}
	print FILE "$inmembername\t$currenttime\t<b>����ɾ�������� $clearday ����ǰ�Ĺ��ڽ�����־�� $deletenum ����</b>\n";
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");

	$output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>�������������û���Զ����أ���<a href=$thisprog>�������</a>~;
	return;
}

sub seterror
{
	my $message = $_[0];
	my $output = qq~
<table width=100% cellpadding=6 cellspacing=0>
<tr><td bgcolor=#2159C9><font color=#ffffff><b>��ӭ������̳�������� / ���й���������</b></font></td></tr>
<tr><td bgcolor=#eeeeee><font color=#990000><b>����������</b>$message</font></td></tr>
<tr><td bgcolor=#ffffff>����<a href="javascript:history.go(-1);">������һҳ</a></td></tr>
</table>
</td></tr></table></body></html>~;
	print $output;	
	exit;
}

sub bankmessage #���û������ж���Ϣ�����ò�������ȡ�ˡ����⡢���ݣ�
{
	my ($receivemember, $topic, $content) = @_;

	my @filedata;
	my $filetomake = $lbdir . $msgdir . "/in/" . $receivemember . "_msg.cgi";
	$filetomake = &stripMETA($filetomake);
	my $currenttime = time;
	&winlock($filetomake) if ($OS_USED eq "Nt");
	if (-e $filetomake)
	{
		open(FILE, $filetomake);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		@filedata = <FILE>;
		close(FILE);
	}

	@filedata = ("����������$bankname\tno\t$currenttime\t$topic\t$content<br><br>������лʹ��$bankname�����ʷ���<br><br>\n", @filedata);

	open(FILE, ">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach (@filedata)
	{
		chomp;
		print FILE "$_\n";
	}
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");

	return;
}

sub updateallsave #���ñ仯��������������Ϣ
{
	my ($callusers, $callsaves) = @_;

	my $filetoopen = $lbdir . "ebankdata/allsaves.cgi";
	my $allusers = 0;
	my $allsaves = 0;
	&winlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	if (-e $filetoopen)
	{
		open(FILE, $lbdir . "ebankdata/allsaves.cgi");
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my $allinfo = <FILE>;
		close(FILE);
		chomp($allinfo);
		($allusers, $allsaves) = split(/,/, $allinfo);
	}

	$allusers += $callusers;
	$allsaves += $callsaves;

	if (open(FILE, ">$filetoopen"))
	{
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "$allusers,$allsaves";
		close(FILE);
	}
	&winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));

	return;
}

sub logaction #��¼������־�����ò�����������Ա����־���ݣ�
{
	my ($actionmember, $actionretail) = @_;
	my $currenttime = time;

	my $filetomake = $lbdir . "ebankdata/alllogs.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, ">>$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE "$actionmember\t$currenttime\t$actionretail\n";
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");

	return;
}

sub ebankadminlogin
{
if ($useverify eq 'yes')
{
   if ($verifyusegd ne 'no')
   {
       eval ('use GD;');
       if ($@)
       {
           $verifyusegd = 'no';
       }
   }
   if ($verifyusegd eq 'no')
   {
       $houzhui = 'bmp';
   } else {
       $houzhui = 'png';
   }
   require 'verifynum.cgi';
}

	print qq~
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>��ӭ���������г��칫��</b></font></td>
</tr>
<form action=$thisprog method=POST>
<input type=hidden name=action value="login">
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername" value="$inmembername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
~;
print qq~
<tr>
	<td bgcolor=#ffffff valign=middle width=40% align=right><font color=#555555>�������ұ�ͼƬ������</font></td>
	<td bgcolor=#ffffff valign=middle><input type=hidden name=sessionid value="$sessionid"><input type=text name=verifynum size=4 maxlength=4>����<img src=$imagesurl/verifynum/$sessionid.$houzhui border=0 align=absmiddle></td>
</tr>
~ if ($useverify eq "yes");

print qq~
<tr>
	<td bgcolor=#ffffff valign=middle colspan=2 align=center><input type=submit value="�� ½"></td>
</tr>
</form>
<tr>
	<td bgcolor=#ffffff valign=middle align=left colspan=2><font face=$font color=#555555>
		<blockquote><b>��ע��</b><p><b>ֻ�������г����ܽ����г��칫�ҡ�<br>δ������Ȩ�ĳ��Ե�¼��Ϊ���ᱻ��¼��������־��</b><p>�ڽ����г��칫��ǰ����ȷ�������������� Cookie ѡ�<br> Cookie ֻ������ڵ�ǰ������������С�Ϊ�˰�ȫ���������ر����������Cookie ��ʧЧ�����Զ�ɾ����</blockquote>
	</td>
</tr>
~;
	return;
}

sub order #�����������
{
	my ($adduser, $addsave) = @_;
	my %ordersaves;

	my $filetoopen = $lbdir . "ebankdata/order.cgi";
	my $filetoopens = &lockfilename($filetoopen);
	return if (-e $filetoopens . ".lck");
	&winlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	if (-e $filetoopen)
	{
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		@orderdata = <FILE>;
		close(FILE);
	}
	foreach (@orderdata)
	{
		chomp;
		my ($tempuser, $tempsave) = split(/\t/, $_);
		$ordersaves{$tempuser} = $tempsave if ($tempuser ne "");
	}
	$ordersaves{$adduser} = $addsave if ($adduser ne "");
	my @orderusers = sort {$ordersaves{$a}<=>$ordersaves{$b}} keys(%ordersaves);
	open(FILE, ">$filetoopen");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	for ($i = 1; $i <= $bankmaxdisplay * 2; $i++)
	{
		$j = @orderusers - $i;
		last if ($j < 0);
		print FILE $orderusers[$j] . "\t" . $ordersaves{$orderusers[$j]} . "\n" if ($ordersaves{$orderusers[$j]});
	}
	close(FILE);
	&winunlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));

	return;
}

sub setbankonoff
{
	my $status = shift;

        my $filetomake = $lbdir . "data/ebankinfo.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, $filetomake);
	flock(FILE, 1) if ($OS_USED eq "Unix");
	my @tempinfo = <FILE>;
	close(FILE);
	open(FILE,">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach $tempconfig (@tempinfo)
	{
		chomp($tempconfig);
		$tempconfig = "\$bankopen = \"$status\";" if ($tempconfig =~ /\$bankopen/);
		print FILE $tempconfig . "\n";
	}
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
}

sub checkverify {
	my $verifynum = $query->param('verifynum');
	my $sessionid = $query->param('sessionid');
	$sessionid =~ s/[^0-9a-f]//isg;
	if (length($sessionid) != 32 && $useverify eq "yes")
	{
		$inpassword = "";
		return;
	}
        mkdir ("${lbdir}verifynum", 0777) unless (-e "${lbdir}verifynum");
        mkdir ("${lbdir}verifynum/login", 0777) if (!(-e "${lbdir}verifynum/login"));

	###��ȡ��ʵ�� IP ��ַ
	my $ipaddress = $ENV{'REMOTE_ADDR'};
	my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);
	$trueipaddress = $ENV{'HTTP_CLIENT_IP'};
	$ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);

	###��ȡ��ǰ���̵���֤�����֤�����ʱ�䡢�û�����
	my $filetoopen = "${lbdir}verifynum/$sessionid.cgi";
	open(FILE, $filetoopen);
	my $content = <FILE>;
	close(FILE);
	unlink($filetoopen);
	chomp($content);
	my ($trueverifynum, $verifytime, $savedipaddress) = split(/\t/, $content);
	my $currenttime = time;

	if (($verifynum ne $trueverifynum || $currenttime > $verifytime + 300 || $ipaddress ne $savedipaddress)&&($useverify eq "yes"))
	{#��֤����Чʱ���Ϊ5����
		$inpassword = "";
	}
	else
	{
		unlink("${lbdir}verifynum/$sessionid.cgi");
		unlink("${imagesdir}verifynum/$sessionid.cgi");
		my $memberfilename = $inmembername;
		$memberfilename =~ s/ /_/g;
		$memberfilename =~ tr/A-Z/a-z/;
		$memberfilename = "${lbdir}verifynum/login/$memberfilename.cgi";

		open(FILE, ">$memberfilename");
		print FILE "$currenttime";
		close(FILE);
	}
	return;
}