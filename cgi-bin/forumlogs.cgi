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
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
$LBCGI::POST_MAX=200000;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "forumlogs.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

&ipbanned;

$inforum = $query->param("forum");
&error("����̳&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($inforum !~ /^[0-9]+$/);
require "data/style${inforum}.cgi" if (-e "${lbdir}data/style${inforum}.cgi");

$inmembername = $query->param("membername");
$inpassword = $query->param("password");
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$inmembername = $query->cookie("amembernamecookie") unless ($inmembername);
$inpassword = $query->cookie("apasswordcookie") unless ($inpassword);
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if (!$inmembername || $inmembername eq "����")
{
	$inmembername = "����";
}
else
{
	&getmember($inmembername, "no");
	&error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
	&error("��ͨ����&�������û���������������µ�¼��") if ($inpassword ne $password);
}
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if (($viewadminlog ne "")&&($viewadminlog ne "0")) {
    if (($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")){
        if (($membercode eq "masked")||($membercode eq "banned")) {&error("������־&������־����ֻ������ͨ��Աʹ��"); }
        if (($viewadminlog eq 1)&&($inmembername eq "����")) {&error("������־&������־����ֻ����ע���Աʹ�ã���ע�ᣡ"); }
        if ($viewadminlog eq 2) {if ($membercode !~ /^rz/) {&error("������־&������־����ֻ������֤��Ա�����ϼ���ʹ�ã�");}}
        if ($viewadminlog eq 3) {&error("������־&������־����ֻ������������ϼ���ʹ�ã�");}
    }
}

$action = $query->param('action');
if ($action eq 'delete' && $membercode eq 'ad')
{
	my $logtime = time;
	my $trueipaddress = $ENV{"HTTP_CLIENT_IP"};
	$trueipaddress = $ENV{"HTTP_X_FORWARDED_FOR"} if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
	$trueipaddress = "no" if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);

	my $filetomake = "${lbdir}boarddata/adminlog$inforum.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(FILE, $filetomake);
	$readdisktimes++;
	flock(FILE, 1) if ($OS_USED eq "Unix");
	my @alllogs = <FILE>;
	close(FILE);
	push(@alllogs, "$inmembername\t$logtime\t\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t��հ�����־\n");
	my $start = $#alllogs - 50;
	$start = 0 if ($start < 0);
	my $alllog = join('', @alllogs[$start .. $#alllogs]);

	open(FILE, ">$filetomake");
	$writedisktimes++;
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE $alllog;
	close(FILE);
	&winunlock($filetomake) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

        print "<script language='javascript'>document.location = '$thisprog?forum=$inforum'</script>";
	exit;
}

&getoneforum($inforum);
$testentry = $query->cookie("forumsallowed$inforum");
$allowed = $allowedentry{$inforum} eq "yes" || ($testentry eq $forumpass && $testentry ne "") || $membercode eq "ad" || $membercode eq "smo" || $inmembmod eq "yes" ? "yes" : "no";
&error("������̳&�Բ�����û��Ȩ�޽����˽����̳��") if ($privateforum eq "yes" && $allowed ne "yes");
&error("������̳&��һ���Ա������������̳��") if ($startnewthreads eq "cert" && (($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode !~ /^rz/) || $inmembername eq "����") && $userincert eq "no");
&error("������̳&�����̳��û��Ȩ�޽�����̳��") if ($yxz ne '' && $yxz!~/,$membercode,/);
if ($allowusers ne ''){
    &error('������̳&�㲻����������̳��') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}
if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &error("������̳&�㲻����������̳���������Ϊ $rating��������ֻ̳���������ڵ��� $enterminweiwang �Ĳ��ܽ��룡") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0 ) {
	require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
	$mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	&error("������̳&�㲻����������̳����Ľ�ǮΪ $mymoney1��������ֻ̳�н�Ǯ���ڵ��� $enterminmony �Ĳ��ܽ��룡") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
	&error("������̳&�㲻����������̳����Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $enterminjf �Ĳ��ܽ��룡") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

my $filetoopens = "${lbdir}data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
unless (-e "${filetoopens}.lck")
{
	if ($privateforum ne "yes")
	{
		&whosonline("$inmembername\t$forumname\tboth\t�鿴������־");
	}
	else
	{
		&whosonline("$inmembername\t$forumname(��)\tboth\t�鿴������־");
	}
}

$type = $query->param("type");
$type = &stripMETA($type);
$key = $query->param("key");
$key = &stripMETA($key);
&mischeader("�鿴������־");

$filetoopen = "${lbdir}/boarddata/adminlog$inforum.cgi";
&winlock($filetoopen) if ($OS_USED eq "Nt");
open(FILE, $filetoopen);
$readdisktimes++;
flock(FILE, 1) if ($OS_USED eq "Unix");
@alllogs = <FILE>;
close(FILE);
&winunlock($filetoopen) if ($OS_USED eq "Nt");
@alllogs = $type eq "name" ? grep(/^$key\t/i, @alllogs) : grep(/$key[^\t]*$/i, @alllogs) if ($key ne "");
$allitems = @alllogs;
&splitpage("forum=$inforum&type=$type&key=$key");
$adminoption = qq~��<a href=$thisprog?action=delete&forum=$inforum onClick="return confirm('�Ƿ����Ҫ��ձ���İ�����־�����50��������������')"><img src=$imagesurl/images/del.gif border=0 title="��ձ���İ�����־"></a>~ if ($membercode eq 'ad');

$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr style="color: $titlefontcolor; font-weight: bold; background-color: $titlecolor" align=center><td width=80 bgcolor=$titlecolor $catbackpic>������</td><td bgcolor=$titlecolor $catbackpic>����ʱ��</td><td bgcolor=$titlecolor $catbackpic>��������</td><td bgcolor=$titlecolor $catbackpic>�������</td><td width=100 bgcolor=$titlecolor $catbackpic>���� IP</td></tr>~;

$addtimes = $timedifferencevalue * 3600 + $timezone * 3600;
for ($i = $startnum; $i >= $endnum; $i--)
{
	my $thislog = $alllogs[$i];
	chomp($thislog);
	my ($logname, $logtime, $logtopic, $logip, $logproxy, $log) = split(/\t/, $thislog);

	my $encodename = &uri_escape($logname);
	$logname = "<a href=profile.cgi?action=show&member=$encodename target=_blank>$logname</a>";
	$logtime = &dateformatshort($logtime + $addtimes);
	$logtopic = $logtopic eq "" ? "������" : &gettopic($logtopic);
	if ($membercode eq "ad") {
	    if ($logproxy ne "no") { $logproxy = qq~<BR><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$logproxy',420,320)" title="LB WHOIS��Ϣ">$logproxy</span>~; } else { $logproxy = ""; }
	    $logip = qq~<span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$logip',420,320)" title="LB WHOIS��Ϣ">$logip</span>$logproxy~;
	} else {  $logip = "����"; }
	$output .= "\n<tr bgColor=$forumcolortwo align=center><td>$logname</td><td>$logtime</td><td>$log</td><td>$logtopic</td><td>$logip</td></tr>";
}

$select = qq~<select name=type><option value="name">��������</option><option value="log">����������</option></select>~;
$select =~ s/value=\"$type\"/value=\"$type\" selected/o;
$output .= qq~
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth align=center><form action=$thisprog>
<tr><td height=4><input type=hidden name=forum value="$inforum"></td></tr>
<tr><td>$pages$adminoption</td><td align=right>$select <input name=key type=text size=16 value="$key"> <input type=submit value="�� ��"></td></tr>
</table></form>~;

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&output("$boardname - ������־�鿴",\$output);
exit;

sub gettopic
{
	my $intopic = shift;
	if (open(FILE, "${lbdir}forum$inforum/$intopic.pl"))
	{
		$readdisktimes++;
		my $line = <FILE>;
		close(FILE);
		chomp($line);
		(undef, my $title, undef) = split(/\t/, $line);
		$title =~ s/^����������//;
		$title = "δ֪" if ($title eq "");
		return "<a href=topic.cgi?forum=$inforum&topic=$intopic target=_blank>$title</a>";
	}
	else
	{
		return "�ѱ�ɾ��";
	}
}

sub splitpage
{#��÷�ҳ
	my $addstring = shift;
	my $instart = $query->param("start");
	$instart = 0 if ($instart !~ /^[0-9]+$/);

	my $temppages = $allitems / 40;
	my $numberofpages = int($temppages);
	$numberofpages++ if ($numberofpages != $temppages);

	if ($numberofpages > 1)
	{
		$startnum = $allitems - $instart - 1;
		$endnum = $startnum - 39;
		$endnum = 0 if ($endnum < 0);

		my $currentpage = int($instart / 40) + 1;
		my $endstart = ($numberofpages - 1) * 40;
		my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<a href=$thisprog?start=0&$addstring title="�� ҳ" ><font face=webdings>9</font></a>~;
		my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<a href=$thisprog?start=$endstart&$addstring title="β ҳ" ><font face=webdings>:</font></a>~;

		my $uppage = $currentpage - 1;
		my $nextpage = $currentpage + 1;
		my $upstart = $instart - 40;
		my $nextstart = $instart + 40;
		my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<a href=$thisprog?start=$upstart&$addstring title="��$uppageҳ"><font face=webdings>7</font></a>~;
		my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<a href=$thisprog?start=$nextstart&$addstring title="��$nextpageҳ"><font face=webdings>8</font></a>~;

		my $tempstep = $currentpage / 7;
		my $currentstep = int($tempstep);
		$currentstep++ if ($currentstep != $tempstep);
		my $upsteppage = ($currentstep - 1) * 7;
		my $nextsteppage = $currentstep * 7 + 1;
		my $upstepstart = ($upsteppage - 1) * 40;
		my $nextstepstart = ($nextsteppage - 1) * 40;
		my $showupstep = $upsteppage < 1 ? "" : qq~<a href=$thisprog?start=$upstepstart&$addstring class=hb title="��$upsteppageҳ">��</a> ~;
		my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<a href=$thisprog?start=$nextstepstart&$addstring class=hb title="��$nextsteppageҳ">��</a> ~;

		$pages = "";
		my $currentstart = $upstepstart + 40;
		for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++)
		{
			last if ($i > $numberofpages);
			$pages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<a href=$thisprog?start=$currentstart&$addstring class=hb>$i</a> ~;
			$currentstart += 40;
		}
		$pages = "<font color=$menufontcolor><b>�� <font color=$fonthighlight>$numberofpages</font> ҳ</b> $beginpage $showup \[ $showupstep$pages$shownextstep\] $shownext $endpage</font>";
	}
	else
	{
		$startnum = $allitems - 1;
		$endnum = 0;
		$pages = "<font color=$menufontcolor>ֻ��һҳ</font>";
	}
	return;
}