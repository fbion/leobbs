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
require "admin.lib.pl";

$|++;
$thisprog = "resetusr.cgi";

$query = new LBCGI;
#&ipbanned;

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
&getmember($inmembername,"no");

$prestep = $query->param('prestep');
$prestep = 300 if ($prestep <= 0 );
&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;
if ($membercode eq "ad" && $inpassword eq $password && lc($inmembername) eq lc($membername))
{
	my $action = $query->param('action');
	if ($action eq "process")
	{
		my @resettype = $query->param('resettype');
		@resettype = map(&cleaninput($_), @resettype);
		my $step = $query->param('step');
		$step =~ s/[^\d]//sg;
		$step ||= 1;

		opendir(DIR, "$lbdir$memdir/old");
		my @memberfiles = readdir(DIR);
		close(DIR);
		@memberfiles = grep(/\.cgi$/i, @memberfiles);

		my $begin = ($step - 1) * $prestep;
		my $end = $step * $prestep - 1;
		$end = $#memberfiles if ($end > $#memberfiles);

		for ($begin .. $end)
		{
			($nametocheck,$no) = split(/\./,$memberfiles[$_]);
			my $namenumber = &getnamenumber($nametocheck);
			&checkmemfile($nametocheck,$namenumber);
		        unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
			unlink ("${lbdir}cache/myinfo/$nametocheck.pl");

			my $filetoopen = "$lbdir$memdir/$namenumber/$memberfiles[$_]";

			open(FILE, $filetoopen);
			my $filedata = <FILE>;
			close(FILE);
			chomp($filedata);

			my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
			($numberofposts, my $numberofreplys) = split(/\|/, $numberofposts);

			foreach my $resetname (@resettype)
			{
				if ($resetname eq "membertitle") { $datainfo = "Member"; } else { $datainfo = ""; }
				eval("\$$resetname = '$datainfo';");
			}

			if ($membername ne "" && $password ne "")
			{
				if (open(FILE, ">$filetoopen"))
				{
					print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5";
					close(FILE);
				}
			}
		}

		if ($end < $#memberfiles)
		{
			$step1=$step*$prestep;
			$step++;

			foreach (@resettype)
			{
				$typedisplay .= qq~<input type=hidden name=resettype value="$_">~;
			}
			print qq~<form name=MAINFORM action=$thisprog method=POST>
<input type=hidden name=action value="process">
<input type=hidden name=step value=$step>
<input type=hidden name=prestep value=$prestep>
$typedisplay
</form>
<script language="JavaScript">
setTimeout("MAINFORM.submit()", 2000);
</script>
<tr><td bgcolor=#2159C9><font color=#ffffff><b>��ӭ������̳�������� / �û���������</b></td></tr>
<tr><td align=center><br>�Ѿ�������$step1���û������ڿ�ʼ����$prestep���û�����������<BR>�����������û���Զ�ǰ������<a href="javascript: MAINFORM.submit()">�������</a>��</td></tr>~;
		}

		else
		{
    opendir (DIRS, "${lbdir}cache/meminfo");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/meminfo/$_");
    }
			print qq~
<tr><td bgcolor=#2159C9><font color=#ffffff><b>��ӭ������̳�������� / �û���������</b></td></tr>
<tr><td align=center><br><b>�û������������!</b></td></tr>~;
		}
	}

	else
	{
		print qq~<form action=$thisprog method=POST onSubmit="return confirm('��ȷ�����Ҫ���������û������ݣ�')">
<input type=hidden name=action value="process">
<input type=hidden name=step value=1>
<tr><td bgColor=#2159C9 colSpan=4><font color=#ffffff><b>��ӭ������̳�������� / �û���������</b></td></tr>
<tr><td bgColor=#ffffff colSpan=4><b>��ѡ��Ҫ���õ��û�����</b></td></tr>
<tr bgColor=#ffffff><td><input type=checkbox name=resettype value="numberofposts"> ��������</td><td><input type=checkbox name=resettype value="numberofreplys"> ��������</td><td><input type=checkbox name=resettype value="postdel"> ��ɾ������</td><td><input type=checkbox name=resettype value="rating"> ����</td></tr>
<tr bgColor=#ffffff><td><input type=checkbox name=resettype value="mymoney"> �����Ǯ</td><td><input type=checkbox name=resettype value="ebankdata"> ��������</td><td><input type=checkbox name=resettype value="jifen"> �������</td><td><input type=checkbox name=resettype value="onlinetime"> ����ʱ��</td></tr>
<tr bgColor=#ffffff><td><input type=checkbox name=resettype value="userface"> ��������</td><td><input type=checkbox name=resettype value="membertitle"> �û�ͷ��</td><td><input type=checkbox name=resettype value="jhmp"> ��������</td><td><input type=checkbox name=resettype value="signature"> �û�ǩ��</td></tr>
<tr bgColor=#ffffff><td colSpan=4> �����û������ֶ��� <input type=text size=12 name=resettype> <i>�߼�ѡ�������д signature ����������û�ǩ��������Ϥ�������գ���Ҫ�����д��</i></td></tr>
<tr bgColor=#ffffff><td colSpan=4> �����û������ֶ��� <input type=text size=12 name=resettype> <i>�߼�ѡ�����Ϥ���û������գ���Ҫ�����д��</i></td></tr>
<tr bgColor=#ffffff><td colSpan=4> �����û������ֶ��� <input type=text size=12 name=resettype> <i>�߼�ѡ�����Ϥ���û������գ���Ҫ�����д��</i></td></tr>
<tr bgColor=#ffffff><td colSpan=4> ÿ�����õ��û��� <input type=text size=4 maxlength=4 name=prestep value=300> Ĭ�ϣ�300��������ְ������������ʵ����������ֵ��</td></tr>
<tr><td bgColor=#ffffff colSpan=4 align=center><input type=submit value="�ء���"></td></tr></form>~;
	}
}

else
{
	&adminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;