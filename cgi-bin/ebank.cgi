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
require "data/mpic.cgi";
require "data/cityinfo.cgi";
require "data/ebankinfo.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "ebank.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
#&ipbanned;
if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else
{
	$boardurltemp =$boardurl;
	$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
	$cookiepath = $boardurltemp;
	$cookiepath =~ s/\/$//;
}

$inmembername = $query->cookie("amembernamecookie") if (!$inmembername);
$inpassword = $query->cookie("apasswordcookie") if (!$inpassword);
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "����" ) #�����¼���ܷ�������
{
	&error("��ͨ����&�����ڵ�����Ƿÿͣ������½�Ժ���ܷ������У�");
}

else
{
	&getmember($inmembername);
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
	&error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
}

$cleanmembername = $inmembername;
$cleanmembername =~ s/ /\_/sg;
$cleanmembername =~ tr/A-Z/a-z/;
$currenttime = time;

#��������û�ͬʱ�ύ�������������ɵĸ�ծ��������
$ebanklockfile = $lbdir . "lock/" . $cleanmembername . "_ebank.lck";
if (-e $ebanklockfile)
{
	&myerror("���д���&�벻Ҫͬʱ�����н��ж�ʽ��ף�") if ($currenttime < (stat($ebanklockfile))[9] + 3);
}
open(LOCKCALFILE, ">$ebanklockfile");
print LOCKCALFILE "1;";
close(LOCKCALFILE);
#END��ˢ

#�û���Ǯ
$myallmoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

#����Ϊ�˻�״̬����ֵ��δ������1��������-1���˻����ᣩ�������ʱ�䣬�������ʱ�䣬�����Ѻ����ֵ��������ν���ʱ�䣬Ԥ������������Ա��Ժ󿪷��¹��ܱ��綨�ڴ��û��Ƿ����Լ��Ĵ��
($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
unless ($mystatus eq "1" || $mystatus eq "-1" || $ebankdata eq "")
{
	($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = "";
}
if ($mystatus)
{
	$mysavedays = &getbetween($mysavetime, $currenttime);
	$mysaveaccrual = int($mysaves * $banksaverate * $mysavedays);
	if ($myloan)
	{
		$myloandays = &getbetween($myloantime, $currenttime) + 1;
		if ($myloandays > $bankloanmaxdays)
		{#����������
			&dooutloan($cleanmembername);
			$myallmoney -= $myloan;
			$rating -= $myloanrating;
			$myloan = 0;
		}
		else
		{
			$myloanaccrual = int($myloan * $bankloanrate * $myloandays);
		}
	}
}		

#�Զ����ᷢ�Ա������û��������û��������еķ��˰������Ȩ����:D��
$mystatus = -1 if (($membercode eq "banned" || $membercode eq "masked") && $mystatus == 1);

#�����ڴ���
if (-e $lbdir . "ebankdata/allloan.cgi")
{
	&winlock($lbdir . "ebankdata/allloan.cgi") if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	open(FILE, $lbdir . "ebankdata/allloan.cgi");
	flock(FILE, 1) if ($OS_USED eq "Unix");
	@allloan = <FILE>;
	close(FILE);
	foreach (@allloan)
	{
		chomp;
		($loaner, $loantime) = split(/,/, $_);
		if (&getbetween($loantime, $currenttime) >= $bankloanmaxdays)
		{
			shift(@allloan);
			push(@outloan, $loaner);
		}
		else
		{
			last;
		}
	}
	if (@outloan)
	{
		open(FILE, ">" . $lbdir . "ebankdata/allloan.cgi");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@allloan)
		{
			chomp;
			print FILE $_ . "\n" if ($_);
		}
		close(FILE);
	}
	&winunlock($lbdir . "ebankdata/allloan.cgi") if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	foreach (@outloan)
	{
		&dooutloan($_);
	}
}
#End���ڴ���

&title;
$action = $query->param('action');
my %Mode = (
	'changepass' => \&changepass,	#�޸�ȡ������
	'open' => \&open,     #����
	'logoff' => \&logoff, #����
	'get' => \&get,       #ȡ��
	'save' => \&save,     #���
	'btrans' => \&btrans, #ת��
	'post' => \&post,     #���
	'loan' => \&loan,     #����
	'repay' => \&repay    #����
	);

if ($Mode{$action})
{
	$Mode{$action} -> ();
}
else
{
	&display;             #Ӫҵ��
}

unlink($ebanklockfile); #�������

print header(-cookie=>[$onlineviewcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&output($pagetitle,\$output);
exit;

sub display #Ӫҵ��
{
	my $onlineview = $query->cookie("onlineview");
	$onlineview = 0 if ($onlineview eq "");
	$onlineview = $onlineview == 1 ? 0 : 1 if ($action eq "onlineview");
	$onlineviewcookie = cookie(-name => "onlineview", -value => "$onlineview", -path => "$cookiepath/", -expires => "+30d");
	my $onlinetitle = $onlineview == 1 ? "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>�ر���ϸ�б�</font></a>]" : "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>��ʾ��ϸ�б�</font></a>]";

	#ȡ���ܴ����Ϣ
	my $allusers = 0;
	my $allsaves = 0;
	if (-e $lbdir . "ebankdata/allsaves.cgi")
	{
		open(FILE, $lbdir . "ebankdata/allsaves.cgi");
		my $allinfo = <FILE>;
		close(FILE);
		chomp($allinfo);
		($allusers, $allsaves) = split(/,/, $allinfo);
	}

	#ȡ��������Ϣ
	my @maxusers;
	my @maxsaves;
	if (-e $lbdir . "ebankdata/order.cgi")
	{
		open(FILE, $lbdir . "ebankdata/order.cgi");
		my @orders = <FILE>;
		close(FILE);
		for ($i = 0; $i < @orders && $i < $bankmaxdisplay; $i++)
		{
			chomp($orders[$i]);
			($maxusers[$i], $maxsaves[$i]) = split(/\t/, $orders[$i]);
		}
	}

	my $banksave100rate = $banksaverate * 100;
	my $bankloan100rate = $bankloanrate * 100;
	my $banktrans100rate = $banktransrate * 100;
	my $bankpost100rate = $bankpostrate * 100;

	my $helpurl = &helpfiles("����");
	$helpurl = qq~$helpurl<img src="$imagesurl/images/$skin/help_b.gif" border=0></span>~;

	my $freshtime = $query->cookie("freshtime");
	if ($freshtime ne "")
	{
		my $autofreshtime = $freshtime * 60 - 1;
		$autofreshtime = 60 if ($autofreshtime < 60);
		my $refreshnow = qq~<meta http-equiv="refresh" content="$autofreshtime;">~;
	}

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	unless(-e "$filetoopens.lck")
	{
		$screenmode = $query->cookie("screenmode");
		$screenmode = 8 if ($screenmode eq "");
		&whosonline("$inmembername\t$bankname\t$bankname\t����Ӫҵ����");
		$membertongji =~ s/������̳/$bankname/o;
		undef $memberoutput if ($onlineview != 1);
	}
	else
	{
		$memberoutput = "";
		$membertongji = " <b>���ڷ�������æ����������Ӫҵ����������������ʱ���ṩ��ʾ��</b>";
		$onlinetitle = "";
	}

	$output .= qq~$refreshnow
	<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=$navfontcolor><a href=leobbs.cgi>$boardname</a> �� $bankname</td><td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center><font face=$font color=$fontcolormisc><b>��ӭ����$banknameӪҵ����</b></font></td></tr>
<tr>
	<td bgcolor=$forumcolorone width=92%><font color=$titlefontcolor>$membertongji�� $onlinetitle</td>
	<td bgcolor=$forumcolorone width=8% align=center><a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 width=40 height=12></a></td>
</tr>~;
	$output .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><table cellPadding=1 cellSpacing=0 border=0>$memberoutput</table><script language="JavaScript"> function O9(id) {if(id != "") window.open("profile.cgi?action=show&member=" + id);}</script></td></tr>~ if ($onlineview == 1 && $memberoutput);
	my $waitress = int(&myrand(10)) + 1;
	$waitress = "$imagesurl/ebank/mm$waitress.gif";
	if ($bankgetpass ne "")
	{
		$promptpassword = qq~prompt("���������ȡ������:", "")~;
		$promptchange = "�޸ĸ���ȡ������";
	}
	else
	{
		$promptpassword = '1';
		$promptchange = "��������ȡ������";
	}
	$output .= qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT><br>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 border=0 width=100%>
<tr><td bgcolor=$forumcolortwo valign=middle colspan=2 align=center $catbackpic><font face=$font color=$fontcolormisc>
<script language="JavaScript" src="$imagesurl/ebank/fader.js"></script>
<script language="JavaScript" type="text/javascript">
prefix="";
arNews = ["$bankmessage", "", "<b><font color=#99ccff>���ʽ��׶ ��� <i>$bankmindeal</i> $moneyname����� <i>$bankmaxdeal</i> $moneyname��24Сʱ����״����� $bankmaxdaydo</font></b>", "", "<b><font color=#885200>��ǰ��������ʣ� <i>$banksave100rate</i>%����ǰ���������ʣ� <i>$bankloan100rate</i>%����������ޣ� <i>$bankloanmaxdays</i> ������</font></b>", "", "<b><font color=green>ת���������ʣ� <i>$banktrans100rate</i>%������������ʣ� <i>$bankpost100rate</i>%��(��� <i>$bankmindeal</i> $moneyname)</font></b>", ""];
</script>
<span id="elFader" style="position:relative;visibility:hidden; height:16" ></span></font>
</td></tr>
<tr>
	<td bgcolor=$miscbacktwo width=260 rowspan=4 valign=top>
		<table><tr><td><font face=$font color=$fontcolormisc><br>�������г��� <font color=#990000>$bankmanager</font><br><br>���ͻ������� $allusers<br><br>������ܶ<br>�� <font color=#000099><i>$allsaves</i></font> $moneyname<br></td><td width=40% align=center><img src=$waitress width=90 height=90 alt="�������ڸ�������ĵ���ӪҵԱMM:)" OnClick="DoKiss()"></td></tr>
		<tr><td colspan=2><br>����ǰʱ�䣺 <span id=showtime></span></td></tr>
<script language="JavaScript" src="$imagesurl/ebank/ebank.js">
</script>
<script language="JavaScript"><!--
displaytime();
function PromptGetPass(formname)
{
	var input = eval(formname + ".getpass");
	if (mypass = $promptpassword)
	{
		input.value = mypass;
		return true;
	}
	else
		return false;
}
function PromptLogOff()
{
	if (confirm('�⽫�������еĴ����ۼ���Ϣ�ӵ�����ֽ��ϣ�\\n������ڱ����д�������Ȼ����Ժ����������\\n�Ƿ����Ҫ������'))
		if (mypass = $promptpassword)
			location.href = "$thisprog?action=logoff&getpass=" + mypass;
}
function PromptChangePass()
{
	if (mypass = $promptpassword)
		if (newpass = prompt("�������µ�ȡ������:", ""))
			if (newpass2 = prompt("���ٴ������µ�ȡ������:", ""))
				if (newpass != newpass2) alert("��������������벻һ�£�");
				else location.href = "$thisprog?action=changepass&getpass=" + mypass + "&newpass=" + newpass;
}
--></script>~;

	if ($mystatus)
	{
		$output .= qq~<tr><td align=center colspan=2><br><table border=1 cellPadding=10 cellSpacing=3><tr><td style="line-height: 140%"><font color=#000066>���˲���״��</font>��������<a href=# OnClick="PromptChangePass()"><font color=blue>$promptchange</font></a><br>~;
		if ($mystatus == 1)
		{
			$output .= qq~<font color=green>�˻�״̬����������������ʹ��</font><br>~;
		}
		else
		{
			$output .= qq~<font color=red>�˻�״̬��������������ʱ����</font><br>~;
		}
		$output .= qq~��ǰ�ֽ𡡡���������<i>$myallmoney</i> $moneyname<br>~;
		$output .= qq~���ڴ�����������<i>$mysaves</i> $moneyname<br>�ۼ�ʱ�����Ϣ������<i>$mysavedays</i> �칲 <i>$mysaveaccrual</i> $moneyname<br>~;
		$output .= qq~<font color=#ff99cc>��ǰ�������������<i>$myloan</i> $moneyname</font><br><font color=#ff99cc>�ۼ�ʱ�����Ϣ������<i>$myloandays</i> �칲 <i>$myloanaccrual</i> $moneyname</font><br>~ if ($myloan);
		$output .= qq~</td></tr></table><br></td></tr>~;
	}
	$output .= qq~<tr><td colspan=2 align=center><a href=setbank.cgi><font color=blue>�������й�������</font></a></td></tr>~ if (($membercode eq "ad" && $bankadminallow ne "manager") || ($membercode eq "smo" && $bankadminallow eq "all") || ",$bankmanager," =~ /,$inmembername,/i);
	$output .= qq~<tr><td colspan=2><hr width=250></td></tr><tr><td colspan=2 align=center><font color=#7700ff>$bankname�ܳ��ͻ�<br><br></font></td></tr><tr><td bgcolor=$titlecolor align=center>�� �� �� ��</td><td bgcolor=$titlecolor align=center>�� ǰ �� ��</td></tr>~;

	for ($i = 1; $i <= @maxusers; $i++)
	{
		$output .= qq~<tr><td bgcolor=$miscbackone>��$i. <a href=profile.cgi?action=show&member=~ . uri_escape($maxusers[$i - 1]) . qq~ target=_blank>$maxusers[$i - 1]</a></td><td bgcolor=$miscbackone>&nbsp;<i>$maxsaves[$i - 1]</i></td></tr>~;
	}
	$output .= qq~<tr><td colspan=2 align=center><br><br></td></tr></table></td>~;

	if ($bankopen ne "on")
	{
		$output .= qq~
	<td bgcolor=$miscbackone align=center><font color=red size=4><b>�����̵��У���ʱͣҵ�����Ժ���ʣ�</b></font></td>
</tr>~;
	}

	else
	{
		unless ($mystatus)
		{
			$output .= qq~
	<td bgcolor=$miscbackone align=center><font size=4>�㵱ǰӵ�� <i>$myallmoney</i> $moneyname�ֽ�<br>����������Ҫ <i>$bankmindeal</i> $moneyname�ֽ������ɡ�<br><br>����Ҫ<a href=$thisprog?action=open><font color=#0000ff><b>����</b></font></a>�����ʹ�ñ��еĸ���ҵ��</font></td>
</tr>~;
		}

		elsif ($mystatus == -1)
		{
			if ($membercode eq "banned" || $membercode eq "masked")
			{
				$output .= qq~
	<td bgcolor=$miscbackone align=center><font size=4>�����㱻��ֹ���ԣ���������˺ű������Զ����ᡣ</font></td>
</tr>~;
			}
			else
			{
				$output .= qq~
	<td bgcolor=$miscbackone align=center><font size=4>������Υ����ĳЩ�涨���зǷ����ڻ��<br>����˺ű��г���ʱ���ᣬ�뾡��������ϵ��</font></td>
</tr>~;
			}
		}

		else
		{
			$output .= qq~
	<td bgcolor=$miscbackone valign=top>��<img src="$imagesurl/ebank/bank.gif" width=16><font color=#99ccff>���ڴ���</font><img src="$imagesurl/ebank/bank.gif" width=16>�����Ź�̨�� ����̨ͬʱ����������<a href=# OnClick="PromptLogOff()"><font color=#cc0000><b>����</b></font></a><hr><br>
	<form name=save action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="save">�� ��Ҫ�����ֽ�:��<input type=text size=10 name=savemoney> $moneyname����<input name=submit type=submit value=�桡�� style="background:#99ccff">��<input name=reset type=reset value=�ء��� style="background:#cccccc"></form>
	<form name=get action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="get"><input type=hidden name=getpass>�� ��Ҫȡ�����:��<input type=text size=10 name=getmoney> $moneyname����<input name=submit type=submit value=ȡ���� style="background:#99ccff" OnClick="return PromptGetPass('get')">��<input name=reset type=reset value=�ء��� style="background:#cccccc"></form>
	</td>
</tr>
<tr>
	<td bgcolor=$miscbacktwo valign=top>��<img src="$imagesurl/ebank/bank.gif" width=16><font color=green>ת�ʻ��</font><img src="$imagesurl/ebank/bank.gif" width=16>�����Ź�̨�� ����̨ͬʱ����������<a href=# OnClick="PromptLogOff()"><font color=#cc0000><b>����</b></font></a><hr><br>~;

			if ($rating < $banktransneed && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" )
			{
				$output .= qq~�� �г��趨��ֻ�������ﵽ $banktransneed ���ϵĻ�Ա�Ͱ�������ʹ��ת�ʺͻ��ܣ�<br><br>~;
			}
			else
			{#�����б�����
				&getmyfriendlist;
				my $friendlist1 = qq~<select name=friends OnChange="btransfriend();"><option>�ҵĺ���</option>~;
				my $friendlist2 = qq~<select name=friends OnChange="postfriend();"><option>�ҵĺ���</option>~;
				foreach (@myfriendlist)
				{
					$friendlist1 .= qq~<option value="$_">$_</option>~;
					$friendlist2 .= qq~<option value="$_">$_</option>~;
				}
				$friendlist1 .= qq~</select>~;
				$friendlist2 .= qq~</select>~;

				$output .= qq~
	<form name=btrans action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="btrans"><input type=hidden name=getpass>�� ��Ҫת��:��<input type=text size=10 name=btransmoney> $moneyname������<input type=text size=12 name=btransuser>��$friendlist1<br>�� ת�˸���:��<input type=text size=30 maxsize=50 name=btransmessage>����<input name=submit type=submit value=ת���� style="background:green" OnClick="return PromptGetPass('btrans')">��<input name=reset type=reset value=�ء��� style="background:#cccccc"></form>
	<form name=post action=$thisprog method=POST OnSubmit="submit.disabled=true; reset.disabled=true;"><input type=hidden name=action value="post"><input type=hidden name=getpass>�� ��Ҫ���:��<input type=text size=10 name=postmoney> $moneyname������<input type=text size=12 name=postuser>��$friendlist2<br>�� ����:��<input type=text size=30 maxsize=50 name=postmessage>����<input name=submit type=submit value=�㡡�� style="background:green" OnClick="return PromptGetPass('post')">��<input name=reset type=reset value=�ء��� style="background:#cccccc"></form>~;
			}

			$output .= qq~</td>
</tr>
<tr>~;
			if ($myloan)
			{
				$output .= qq~
	<td bgcolor=$miscbackone valign=top>��<img src="$imagesurl/ebank/bank.gif" width=16><font color=#ff7777>�����Ŵ�</font><img src="$imagesurl/ebank/bank.gif" width=16>�����Ź�̨<hr><br>
	�� ������Ĵ�����<a href=$thisprog?action=repay><font color=#ff99cc>�������</font></a>��<br><br>
	</td>
</tr>~;
			}
			else
			{
				$output .= qq~<td bgcolor=$miscbackone valign=top>��<img src="$imagesurl/ebank/bank.gif" width=16><font color=red>�����Ŵ�</font><img src="$imagesurl/ebank/bank.gif" width=16>�����Ź�̨<hr><br>~;

				if ($bankallowloan eq "yes")
				{
					if ($rating > 0)
					{
						$output .= qq~<form name=loan action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="loan">�� ��Ҫ��Ѻ�� <select size=1 name=loanrate>~;
						for ($i = 1; $i <= $rating; $i++)
						{
							$output .= qq~<option value=$i>$i</option>~;
						}
						$output .= qq~</select>��������������:��<input type=text size=10 name=loanmoney> $moneyname����<input type=text size=1 style="width: 1px; height: 1px"><input name=submit type=submit value=������ style="background:#ff7777"><br>�� ( ÿ��������������Ѻ $bankrateloan $moneyname )</form>~;
					}
					else
					{
						$output .= qq~�� ��û������������Ѻ���޷����<br><br>~;
					}
				}
				else
				{
					$output .= qq~�� �г��Ѿ�ͣ���˴������<br><br>~;
				}
				$output .= qq~</td></tr>~;
			}

			$output .= qq~<tr><td bgcolor=$miscbacktwo valign=top>��<img src="$imagesurl/ebank/bank.gif" width=16><font color=#000066>������Ŀ</font><img src="$imagesurl/ebank/bank.gif" width=16>������������������н��׼�¼��<hr>~;
			$output .= qq~<table border=1 width=100% bordercolor=#cccccc><tr><td align=center width=30%>����ʱ��</td><td align=center width=30%>�¼�</td><td align=center width=20%>���($moneyname)</td><td align=center width=20%>���($moneyname)</td></tr>~;
			if (-e $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi")
			{
				open(FILE, $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi");
				my @mylogs = <FILE>;
				close(FILE);
				foreach (@mylogs)
				{
					chomp;
					my ($banktime, $bankaction, $banknums, $banksavenum) = split(/\t/, $_);
					$banktime = &dateformat($banktime + $timezone * 3600 + $timedifferencevalue * 3600);
					$output .= qq~<tr><td align=center>$banktime</td><td align=center>$bankaction</td><td align=center>$banknums</td><td align=center>$banksavenum</td></tr>~;
				}
			}
			$output .= qq~</table></td></tr>~;
		}
	}

	$output .= qq~
</table></td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
	$pagetitle = "$boardname - $banknameӪҵ����";

	return;
}

sub changepass #�޸�ȡ������
{
	my $getpass = $query->param('getpass');
	my $newpass = $query->param('newpass');
	&myerror("���д���&��û�ڱ����п�������������ȡ�����룿") unless ($mystatus);
	&myerror("���д���&������ľɵ�ȡ���������") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
	&myerror("���д���&��������µ�ȡ������Ϊ�գ�") if ($newpass eq "");
	&myerror("���д���&��������µ�ȡ�����뺬�в����ʵķǷ��ַ���") if ($newpass =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]/is);
	&myerror("���д���&��������µ�ȡ������̫����") if (length($newpass) > 16);
	&updateuserinfo($cleanmembername, 0, 0, "nochange", 0, "nochange", 0, "nochange", 0, "no", $newpass);
	&printjump("�趨ȡ������ɹ�");
	return;
}

sub open #����
{
	&myerror("���д���&�����̵㣬��ʱͣҵ���޷�������") unless ($bankopen eq "on");
	&myerror("���д���&���Ѿ��ڱ����п������ˣ�") if ($mystatus);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("���д���&����24Сʱ�ڵĽ��״����Ѿ���������������ֵ $bankmaxdaydo��")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("���д���&����ֽ𲻹��������Ҫ��") if ($myallmoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\t�����п���") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, -$bankmindeal, 1, $bankmindeal, $currenttime, 0, "", 0, "yes");
	&updateallsave(1, $bankmindeal);

	&logpriviate("����", $bankmindeal, $bankmindeal);
	&logaction($inmembername, "�����ɹ������� $bankmindeal $moneyname��");

	&order($cleanmembername, $bankmindeal);
	&printjump("�����ɹ�");
	return;
}

sub logoff #����
{
	my $getpass = $query->param('getpass');
	&myerror("���д���&�����̵㣬��ʱͣҵ���޷�������") unless ($bankopen eq "on");
	&myerror("���д���&��û�ڱ����п���������ô������") unless ($mystatus);
	&myerror("���д���&����ʻ�����ʱ���ᣬ�����г���ϵ��") if ($mystatus == -1);
	&myerror("���д���&�������ȡ���������") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("���д���&����24Сʱ�ڵĽ��״����Ѿ���������������ֵ $bankmaxdaydo��")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("���д���&������ȳ����ڱ����еĴ�������������") if ($myloan);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\t����������") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, $mysaves + $mysaveaccrual, "", -$mysaves, "", 0, "", 0, "yes");
	&updateallsave(-1, -$mysaves);

	my $filetodel = $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi";
	unlink($filetodel);

	&logaction($inmembername, "�����ɹ���ȡ�ߴ�� $mysaves $moneyname��������Ϣ $mysaveaccrual $moneyname��");

	&order($cleanmembername, 0);
	&printjump("�����ɹ�");
	return;
}

sub get #ȡ��
{
	my $getmoney = $query->param('getmoney');
	my $getpass = $query->param('getpass');
	&myerror("���д���&�����̵㣬��ʱͣҵ���޷�ȡ�") unless ($bankopen eq "on");
	&myerror("���д���&��û�ڱ����п���������ôȡ�") unless ($mystatus);
	&myerror("���д���&����ʻ�����ʱ���ᣬ�����г���ϵ��") if ($mystatus == -1);
	&myerror("���д���&�������ȡ���������") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("���д���&����24Сʱ�ڵĽ��״����Ѿ���������������ֵ $bankmaxdaydo��")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("���д���&ȡ����������������飡") if ($getmoney =~ /[^0-9]/ or $getmoney eq "");
	&myerror("���д���&��û����ô�������ȡ�����������������Ļ�ͷ�������ٴ��� $bankmindeal $moneyname��") if ($getmoney > $mysaves + $mysaveaccrual - $bankmindeal);
	&myerror("���д���&ȡ�������������󵥱ʽ��׶� $bankmaxdeal $moneyname") if ($getmoney > $bankmaxdeal);
	&myerror("���д���&ȡ������С�ڱ�����С���ʽ��׶� $bankmindeal $moneyname") if ($getmoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\t������ȡ��") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, $getmoney, "nochange", $mysaveaccrual - $getmoney, $currenttime, 0, "nochange", 0, "yes");
	&updateallsave(0, $mysaveaccrual - $getmoney);

	&logpriviate("��Ϣ", $mysaveaccrual, $mysaves + $mysaveaccrual) if ($mysaveaccrual != 0);
	&logpriviate("ȡ��", -$getmoney, $mysaves + $mysaveaccrual - $getmoney);
	&logaction($inmembername, "<font color=#99ccff>ȡ����� $getmoney $moneyname��ͬʱ������Ϣ $mysaveaccrual $moneyname��</font>");

	&order($cleanmembername, $mysaves + $mysaveaccrual - $getmoney);
	&printjump("ȡ��ɹ�");
	return;
}

sub save #���
{
	my $savemoney = $query->param('savemoney');
	&myerror("���д���&�����̵㣬��ʱͣҵ���޷���") unless ($bankopen eq "on");
	&myerror("���д���&��û�ڱ����п���������ô��") unless ($mystatus);
	&myerror("���д���&����ʻ�����ʱ���ᣬ�����г���ϵ��") if ($mystatus == -1);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("���д���&����24Сʱ�ڵĽ��״����Ѿ���������������ֵ $bankmaxdaydo��")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("���д���&�����������������飡") if ($savemoney =~ /[^0-9]/ or $savemoney eq "");
	&myerror("���д���&��û����ô���ֽ���Դ棡") if ($savemoney > $myallmoney);
	&myerror("���д���&��������������󵥱ʽ��׶� $bankmaxdeal $moneyname") if ($savemoney > $bankmaxdeal);
	&myerror("���д���&�������С�ڱ�����С���ʽ��׶� $bankmindeal $moneyname") if ($savemoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\t�����д��") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, -$savemoney, "nochange", $mysaveaccrual + $savemoney, $currenttime, 0, "nochange", 0, "yes");
	&updateallsave(0, $mysaveaccrual + $savemoney);

	&logpriviate("��Ϣ", $mysaveaccrual, $mysaves + $mysaveaccrual) if ($mysaveaccrual != 0);
	&logpriviate("����", $savemoney, $mysaves + $mysaveaccrual + $savemoney);
	&logaction($inmembername, "<font color=#99ccff>������ $savemoney $moneyname��ͬʱ������Ϣ $mysaveaccrual $moneyname��</font>");

	&order($cleanmembername, $mysaves + $mysaveaccrual + $savemoney);
	&printjump("���ɹ�");
	return;
}

sub btrans #ת��
{
	my $btransuser = $query->param('btransuser');
	my $btransmoney = $query->param('btransmoney');
	my $btransmessage = $query->param('btransmessage');
	my $getpass = $query->param('getpass');
	$btransuser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
	&myerror("���д���&�����̵㣬��ʱͣҵ���޷�ת�ʣ�") unless ($bankopen eq "on");
	&myerror("���д���&��û�ڱ����п���������ôת�ʣ�") unless ($mystatus);
	&myerror("���д���&����ʻ�����ʱ���ᣬ�����г���ϵ��") if ($mystatus == -1);
	&myerror("���д���&�������ȡ���������") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("���д���&����24Сʱ�ڵĽ��״����Ѿ���������������ֵ $bankmaxdaydo��")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("���д���&ת�˸���̫���ˣ�") if (length($btransmessage) > 50);
	&myerror("���д���&������öȣ������������ߣ��޷�ʹ��ת��ҵ��") if ($rating < $banktransneed && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo");
	&myerror("���д���&ת����������������飡") if ($btransmoney =~ /[^0-9]/ or $btransmoney eq "");
	my $banktranscharge = int($banktransrate * $btransmoney + 0.5); #��������:)
	$banktranscharge = $bankmindeal if ($banktranscharge < $bankmindeal);
	&myerror("���д���&��û����ô��������ת�ʺ�֧��ת�ʷ��ã��������������Ļ�ͷ�������ٴ��� $bankmindeal $moneyname��") if ($btransmoney + $banktranscharge > $mysaves + $mysaveaccrual - $bankmindeal);
	&myerror("���д���&ת�������������󵥱ʽ��׶� $bankmaxdeal $moneyname") if ($btransmoney > $bankmaxdeal);
	&myerror("���д���&ת������С�ڱ�����С���ʽ��׶� $bankmindeal $moneyname") if ($btransmoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\t������ת��") unless(-e "$filetoopens.lck");

	$btransuser =~ s/ /\_/sg;
	$btransuser =~ tr/A-Z/a-z/;
	&myerror("���д���&�Լ����Լ�תʲô�ʣ�") if ($btransuser eq $cleanmembername);
	$btransmessage = &unHTML($btransmessage);

	&getmember($btransuser);
	&myerror("���д���&ת�ʶ����û������ڣ�") if ($userregistered eq "no");
	my ($tmystatus, $tmysaves, $tmysavetime, $tmyloan, $tmyloantime, $tmyloanrating, $tbankadd1, $tbankadd2, $tbankadd3, $tbankadd4, $tbankadd5) = split(/,/, $ebankdata);
	&myerror("���д���&ת�ʶ����û���û���ڱ��п���������Կ���ʹ�û��ҵ��") if ($tmystatus eq "");
	&myerror("���д���&�Է��˻��Ѿ������ᣬ�޷�������") if ($tmystatus == -1 || $membercode eq "banned" || $membercode eq "masked");
	my $tmysavedays = &getbetween($tmysavetime, $currenttime);
	my $tmysaveaccrual = int($tmysaves * $banksaverate * $tmysavedays);

	&updateuserinfo($cleanmembername, 0, 0, "nochange", $mysaveaccrual - $btransmoney - $banktranscharge, $currenttime, 0, "nochange", 0, "yes");
	&updateuserinfo($btransuser, 0, 0, "nochange", $tmysaveaccrual + $btransmoney, $currenttime, 0, "nochange", 0, "no");
	&updateallsave(0, $mysaveaccrual + $tmysaveaccrual - $banktranscharge);	

	&bankmessage($btransuser, "ת��֪ͨ", "����$inmembername �����ڱ��е��ʻ���ת���� $btransmoney $moneyname�������Ѿ����ʣ�����գ�<br>����ת�˸��ԣ�<font color=green>$btransmessage</font>��");

	&logpriviate("��Ϣ", $mysaveaccrual, $mysaves + $mysaveaccrual) if ($mysaveaccrual != 0);
	&logpriviate("ת��������", -$banktranscharge, $mysaves + $mysaveaccrual - $banktranscharge);
	&logpriviate("ת����$btransuser", -$btransmoney, $mysaves + $mysaveaccrual - $banktranscharge - $btransmoney);
	&order($cleanmembername, $mysaves + $mysaveaccrual - $banktranscharge - $btransmoney, $btransuser, $tmysaves + $tmysaveaccrual + $btransmoney);

	$cleanmembername = $btransuser;
	&logpriviate("��Ϣ", $tmysaveaccrual, $tmysaves + $tmysaveaccrual) if ($tmysaveaccrual != 0);
	&logpriviate("��$inmembernameת��", $btransmoney, $tmysaves + $tmysaveaccrual + $btransmoney);

	&logaction($inmembername, "<font color=green>ת����� $btransmoney $moneyname�� $btransuser������������ $banktranscharge $moneyname��ͬʱ����ת����������Ϣ $mysaveaccrual $moneyname��ת�뷽������Ϣ $tmysaveaccrual $moneyname��ת�˸��ԣ�$btransmessage</font>");
	&printjump("ת�ʳɹ�");
	return;
}

sub post
{
	my $postuser = $query->param('postuser');
	my $postmoney = $query->param('postmoney');
	my $postmessage = $query->param('postmessage');
	my $getpass = $query->param('getpass');
	$postuser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
	&myerror("���д���&�����̵㣬��ʱͣҵ���޷���") unless ($bankopen eq "on");
	&myerror("���д���&��û�ڱ����п���������ô��") unless ($mystatus);
	&myerror("���д���&����ʻ�����ʱ���ᣬ�����г���ϵ��") if ($mystatus == -1);
	&myerror("���д���&�������ȡ���������") if ($bankgetpass ne "" && $bankgetpass ne $getpass);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("���д���&����24Сʱ�ڵĽ��״����Ѿ���������������ֵ $bankmaxdaydo��")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("���д���&����̫���ˣ�") if (length($postmessage) > 50);
	&myerror("���д���&������öȣ������������ߣ��޷�ʹ�û��ҵ��") if ($rating < $banktransneed && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo");
	&myerror("���д���&�����������������飡") if ($postmoney =~ /[^0-9]/ or $postmoney eq "");
	my $bankpostcharge = int($bankpostrate * $postmoney + 0.5); #��������:)
	$bankpostcharge = $bankmindeal if ($bankpostcharge < $bankmindeal);
	&myerror("���д���&��û����ô������������֧�������ã��������������Ļ�ͷ�������ٴ��� $bankmindeal $moneyname��") if ($postmoney + $bankpostcharge > $mysaves + $mysaveaccrual - $bankmindeal);
	&myerror("���д���&��������������󵥱ʽ��׶� $bankmaxdeal $moneyname") if ($postmoney > $bankmaxdeal);
	&myerror("���д���&�������С�ڱ�����С���ʽ��׶� $bankmindeal $moneyname") if ($postmoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\t�����л��") unless(-e "$filetoopens.lck");

	$postuser =~ s/ /\_/sg;
	$postuser =~ tr/A-Z/a-z/;
	&myerror("���д���&�Լ����Լ����ʲô�") if ($postuser eq $cleanmembername);
	$postmessage = &unHTML($postmessage);

	&getmember($postuser);
	&myerror("���д���&�������û������ڣ�") if ($userregistered eq "no");

	&updateuserinfo($cleanmembername, 0, 0, "nochange", $mysaveaccrual - $postmoney - $bankpostcharge, $currenttime, 0, "nochange", 0, "yes");
	&updateuserinfo($postuser, 0, $postmoney, "nochange", 0, "nochange", 0, "nochange", 0, "no");
	&updateallsave(0, $mysaveaccrual - $postmoney - $bankpostcharge);	

	&bankmessage($postuser, "��", "����$inmembername �ӱ��и������� $postmoney $moneyname�ֽ������Ѿ���λ������գ�<br>�������ԣ�<font color=green>$postmessage</font>��");

	&logpriviate("��Ϣ", $mysaveaccrual, $mysaves + $mysaveaccrual) if ($mysaveaccrual != 0);
	&logpriviate("���������", -$bankpostcharge, $mysaves + $mysaveaccrual - $bankpostcharge);
	&logpriviate("�����$postuser", -$postmoney, $mysaves + $mysaveaccrual - $bankpostcharge - $postmoney);
	&logaction($inmembername, "<font color=green>���û� $postuser �����$postmoney $moneyname������������ $bankpostcharge $moneyname��ͬʱ������Ϣ $mysaveaccrual $moneyname�����ԣ�$postmessage</font>");

	&order($cleanmembername, $mysaves + $mysaveaccrual - $bankpostcharge - $postmoney);
	&printjump("���ɹ�");
	return;
}

sub loan #����
{
	my $loanrate = $query->param('loanrate');
	my $loanmoney = $query->param('loanmoney');
	&myerror("���д���&�����̵㣬��ʱͣҵ���޷����") unless ($bankopen eq "on");
	&myerror("���д���&��û�ڱ����п���������ô���") unless ($mystatus);
	&myerror("���д���&����ʻ�����ʱ���ᣬ�����г���ϵ��") if ($mystatus == -1);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("���д���&����24Сʱ�ڵĽ��״����Ѿ���������������ֵ $bankmaxdaydo��")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("���д���&��������Ѿ����г�ͣ�ã�") if ($bankallowloan ne "yes");
	&myerror("���д���&�㵱ǰ���д���û�л��壬�������µĴ��") if ($myloan);
	&myerror("���д���&��Ѻ�����������") if ($loanrate =~ /[^0-9]/ or $loanrate eq "");
	&myerror("���д���&��Ѻ�����������") if ($loanrate == 0);
	&myerror("���д���&��û����ô����������������Ѻ��") if ($loanrate > $rating);
	&myerror("���д���&�������������") if ($loanmoney =~ /[^0-9]/ or $loanmoney eq "");
	&myerror("���д���&������Ѻ����ֵ����������������") if ($loanmoney > $bankrateloan * $loanrate);
	&myerror("���д���&�������������󵥱ʽ��׶� $bankmaxdeal $moneyname") if ($loanmoney > $bankmaxdeal);
	&myerror("���д���&������С�ڱ�����С���ʽ��׶� $bankmindeal $moneyname") if ($loanmoney < $bankmindeal);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\t�����д���") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, $loanmoney, "nochange", 0, "nochange", $loanmoney, $currenttime, $loanrate, "yes");
	my $filetomake = $lbdir . "ebankdata/allloan.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, ">>$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE "$cleanmembername,$currenttime\n";
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");

	&bankmessage($cleanmembername, "����֪ͨ", "�������ڱ��е�Ѻ�� $loanrate ���������� $loanmoney $moneyname�����ڴ����Ѿ����ŵ�����ֽ����ڴӽ��쿪ʼ�� $bankloanmaxdays �����ڼ�ʱ�黹�����������ϵͳ���Զ�ǿ���ջش���ҿ۳����Ѻ��������");

	&logpriviate("����", $loanmoney, $mysaves);
	&logaction($inmembername, "<font color=#ff7777>�����е�Ѻ�� $loanrate ������������ $loanmoney $moneyname����ѷ��������ֽ�</font>");
	&printjump("����ɹ�");
	return;
}

sub repay
{
	&myerror("���д���&�����̵㣬��ʱͣҵ���޷��������") unless ($bankopen eq "on");
	&myerror("���д���&��û�ڱ����п���������ʲô���") unless ($mystatus);
	&myerror("���д���&����ʻ�����ʱ���ᣬ�����г���ϵ��") if ($mystatus == -1);
	@mybankdotimes = split(/\|/, $mybankdotime);
	&myerror("���д���&����24Сʱ�ڵĽ��״����Ѿ���������������ֵ $bankmaxdaydo��")if (@mybankdotimes >= $bankmaxdaydo && $currenttime - pop(@mybankdotimes) <= 86400 && $membercode ne "ad");
	&myerror("���д���&��û�д�����,��ɶ��") unless ($myloan);
	&myerror("���д���&����ֽ𲻹��������") if ($myallmoney < $myloan + $myloanaccrual);

	my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\t$bankname\tnone\t�����л���") unless(-e "$filetoopens.lck");

	&updateuserinfo($cleanmembername, 0, -($myloan + $myloanaccrual), "nochange", 0, "nochange", -$myloan, "", -$myloanrating, "no");

	my $filetoopen = $lbdir . "ebankdata/allloan.cgi";
	if (-e $filetoopen)
	{
		&winlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my @filedata = <FILE>;
		close(FILE);
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@filedata)
		{
			chomp;
			print FILE $_ . "\n" unless ($_ =~ /^$cleanmembername,/i);
		}
		close(FILE);
		&winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	}

	&logpriviate("����", $myloan + $myloanaccrual, $mysaves);
	&logaction($inmembername, "<font color=#ff7777>�����г����� $myloan $moneyname���֧����Ϣ $myloanaccrual $moneyname��</font>");
	&printjump("�����ɹ�");
	return;	
}

#####����Ϊ���ú�����

sub order #�����������
{
	my ($adduser1, $addsave1, $adduser2, $addsave2) = @_;
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
	$ordersaves{$adduser1} = $addsave1 if ($adduser1 ne "");
	$ordersaves{$adduser2} = $addsave2 if ($adduser2 ne "");
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

sub getbetween #ȡ������ʱ��֮���������������ò�������ʼʱ�䣬����ʱ�䣩
{
	my ($begintime, $endtime) = @_;
	my ($tmpsecond, $tmpminute, $tmphour, $tmpday, $tmpmonth, $tmpyear, $tmpwday, $tmpyday, $tmpisdst) = localtime($begintime + $timezone * 3600);
	$begintime -= ($tmphour * 3600 + $tmpminute * 60 + $tmpsecond);
	my $betweendays = int(($endtime - $begintime) / 86400);
	return $betweendays;
}

sub getmyfriendlist #ȡ���û������б�
{
	my $filetoopen = $lbdir . "memfriend/" . $cleanmembername . ".cgi";
	if (-e $filetoopen)
	{
		open(FILE, $filetoopen);
		@myfriendlist = <FILE>;
		close(FILE);
	}

	chomp(@myfriendlist);
	foreach (@myfriendlist)
	{
		s/^����������//sg;
	}
	return;
}

sub bankmessage #���û������ж���Ϣ�����ò�������ȡ�ˡ����⡢���ݣ�
{
	my ($receivemember, $topic, $content) = @_;
	my @filedata;
	my $filetomake = $lbdir . $msgdir . "/in/" . $receivemember . "_msg.cgi";
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

sub logaction #��¼������־�����ò�����������Ա����־���ݣ�
{
	my ($actionmember, $actionretail) = @_;

	my $filetomake = $lbdir . "ebankdata/alllogs.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
	open(FILE, ">>$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE "$actionmember\t$currenttime\t$actionretail\n";
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt");
	return;
}

sub logpriviate #������˴��ۣ����ò��������׶���������ͷ���ڽ��ࣩ
{
	my ($bankaction, $banknums, $banksavenum) = @_;

	my $filetomake = $lbdir . "ebankdata/log/" . $cleanmembername . ".cgi";
	my @mylogs;
	&winlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	if (-e $filetomake)
	{
		open(FILE, $filetomake);

		flock(FILE, 1) if ($OS_USED eq "Unix");
		@mylogs = <FILE>;
		close(FILE);
		while (@mylogs >= $banklogpriviate)
		{
			pop(@mylogs) ;
		}
	}
	@mylogs = ("$currenttime\t$bankaction\t$banknums\t$banksavenum", @mylogs);

	open(FILE, ">$filetomake");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach (@mylogs)
	{
		chomp;
		print FILE $_ . "\n";
	}
	close(FILE);
	&winunlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
	return;
}

sub dooutloan #�����û��Ĺ��ڴ�����ò������û�����
{
	my $loaner = shift;

	my $namenumber = &getnamenumber($loaner);
	&checkmemfile($loaner,$namenumber);
	my $filetoopen = "$lbdir$memdir/$namenumber/$loaner.cgi";
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

		if ($mystatus && $myloan)
		{
			$mesloan = $myloan;
			$mesloantime = $myloantime;
			$mesloanrating = $myloanrating;
			$mymoney -= $myloan;
			$rating -= $myloanrating;
			$myloan = 0;
			$myloantime = "";
			$myloanrating = 0;
		}

		$rating = -5 if ($rating < -5);
		$rating = $maxweiwang if ($rating > $maxweiwang);
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

	if ($mesloan)
	{
		$mesloantime = &shortdate($mesloantime);
		&logaction("<font color=red>�����Զ��������</font>", "<font color=red>$loaner �� $mesloantime ��Ѻ $mesloanrating ��������� $mesloan $moneyname���ڣ��ѿ۳���Ѻ����������ǿ��׷�ش��</font>");
		&bankmessage($loaner, "�������ڲ���֪ͨ", "�������� $mesloantime �ڱ��е�Ѻ $mesloanrating ����������� $mesloan $moneyname��������δ���������Ѱ�����̳���з��۳����Ѻ������ֵ��<br>����ͬʱ��Ĳ�������Ҳ��ǿ��׷�أ��Դ��¼�����������ź���<br><br>");
	}
	return;
}

sub printjump #��ʾLB�����תҳ�棨���ò�����ҳ�����⣩
{
	my $content = shift;

	$output .= qq~
	<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=$navfontcolor><a href=leobbs.cgi>$boardname</a> �� <a href=ebank.cgi>$bankname</a> �� $content</td><td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellPadding=6 cellSpacing=1 border=0 width=100%>
	<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>��лѡ�����ǵ����ʷ�����ղ������еĽ����Ѿ���Ч��</b></font></td></tr>
	<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������û���Զ����أ�������������ӣ���
		<ul><li><a href=$thisprog>��������Ӫҵ����</a>  $pagestoshow</ul>
	</td></tr>
</table></td></tr>
</table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	$pagetitle = "$boardname - ������$content";
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

sub updateuserinfo #�����û���Ϣ
{
	my ($nametocheck, $crating, $cmoney, $bankstats, $csaves, $savetime, $cloan, $loantime, $cloanrating, $allowcount, $newgetpass) = @_;
	#�û����������仯������Ǯ�仯�������µ������˻�״̬(���仯����"nochange")�����仯�������µĴ��ʱ��(���仯����"nochange")������仯�������µĴ���ʱ��(���仯����"nochange")�������Ѻֵ�仯�����Ƿ�������н��״���������Ϊ"yes", ������Ϊ"no"��
	my $namenumber = &getnamenumber($nametocheck);
	&checkmemfile($nametocheck,$namenumber);

	my $filetoopen = "$lbdir$memdir/$namenumber/$nametocheck.cgi";
	if (-e $filetoopen)
	{
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		open(FILE, "+<$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		my $filedata = <FILE>;
		chomp($filedata);
		my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
		my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);

		if ($allowcount eq "yes")
		{
			my @mybankdotimes = split(/\|/, $mybankdotime);
			@mybankdotimes = ($currenttime, @mybankdotimes);
			$mybankdotime = "";
			for (my $i = 0; $i < $bankmaxdaydo; $i++)
			{
				last if ($i == @mybankdotimes);
				$mybankdotime .= $mybankdotimes[$i] . "|";
			}
			chop($mybankdotime);
		}

		$rating += $crating;
		$mymoney += $cmoney;
		$mystatus = $bankstats if ($bankstats ne "nochange");
		$mysaves = 0 unless($mysaves);
		$mysaves += $csaves;
		$mysavetime = $savetime if ($savetime ne "nochange");
		$myloan = 0 unless($myloan);
		$myloan += $cloan;
		$myloantime = $loantime if ($loantime ne "nochange");
		$myloanrating = 0 unless($myloanrating);
		$myloanrating += $cloanrating;
		$bankgetpass = $newgetpass if ($newgetpass ne "");

		$ebankdata = "$mystatus,$mysaves,$mysavetime,$myloan,$myloantime,$myloanrating,$mybankdotime,$bankgetpass,$bankadd2,$bankadd3,$bankadd4,$bankadd5";

		if (($membername ne "") && ($password ne ""))
		{
			seek(FILE,0,0);
#			$lastgone = $currenttime;
			print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
			close(FILE);
			
		      if (open(FILE,">$lbdir$memdir/old/$nametocheck.cgi")) {
#			$lastgone = $currenttime;
			print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
			close(FILE);
		      }
		} else {
		    close(FILE);
		}
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
		unlink ("${lbdir}cache/myinfo/$nametocheck.pl");
		unlink ("${lbdir}cache/meminfo/$nametocheck.pl");
	}
	return;
}

sub myerror
{
	my $errorinfo = shift;
	unlink($ebanklockfile);
	&error($errorinfo);
	return;
}
