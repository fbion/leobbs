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
require "data/cityinfo.cgi";
require "data/mpic.cgi";
require "bbs.lib.pl";

opendir (DIRS, "$lbdir");
my @files = readdir(DIRS);
closedir (DIRS);
@files = grep(/^\w+?$/i, @files);
my @ftpdir = grep(/^ftpdata/i, @files);
$ftpdir = $ftpdir[0];

require "$ftpdir/conf.cgi";

$|++;
$thisprog = "ftp.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

&ipbanned;


if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else
{
	my $boardurltemp = $boardurl;
	$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
	$cookiepath = $boardurltemp;
	$cookiepath =~ s/\/$//;
}

$inmembername = $query->cookie("amembernamecookie") unless ($inmembername);
$inpassword = $query->cookie("apasswordcookie") unless ($inpassword);
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t]//isg;
$cleanmembername = $inmembername;
$cleanmembername =~ s/ /\_/sg;
$cleanmembername =~ tr/A-Z/a-z/;
$ftplockfile = "${lbdir}lock/$cleanmembername\_ftpiii.lck";
$currenttime = time;
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "����")
{#����û����
	&error("��ͨ����&�ÿͲ��ܲ鿴FTP ����,���ȵ�¼��");
}
else
{
	&getmember($inmembername, 'no');
	&error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
	&error("��ͨ����&�������û���������������µ�¼��") if ($inpassword ne $password);
	&error("Ȩ�޴���&���������»���Ե��Ñ���������� FTP ���ˣ�") if ($membercode eq "banned" || $membercode eq "masked");

	#��������û�ͬʱ�ύ�������������ɵĸ�ծ���������
	if (-e $ftplockfile)
	{
		&myerror("ˢ�´���&�벻Ҫˢ��FTP����̫�죡") if ($currenttime < (stat($ftplockfile))[9] + 3);
	}
	open(LOCKCALFILE, ">$ftplockfile");
	close(LOCKCALFILE);

	$myallmoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
}

if (($membercode ne "ad")&&($plugstats eq "close")) {
    unlink($ftplockfile);
    &error("��ͨ����&FTP �����Ѿ�������Ա��ʱ�رգ�");
}

$action = $query->param("action");
my %Mode = (
	"view"	=> \&view,	#�鿴ĳ��FTP�ĵ�¼����
	"poll"	=> \&poll,	#��ĳ��FTP���
	"add"	=> \&add,	#���һ��FTP��¼����
	"addok"	=> \&addok,
	"edit"	=> \&edit,	#�༭һ��FTP��¼����
	"editok"=> \&editok,
	"info"	=> \&info,	#��ѯFTP�Ĺ����¼
	"delete"=> \&delete,	#ɾ��һ��FTP��¼����
	"up"	=> \&up,	#����FTP�������е�λ��
	"repair"=> \&repair,	#�ؽ���������
	"config"=> \&config	#���ó�������
);

if ($Mode{$action})
{
	$Mode{$action}->();
}
else
{
	&list;
}

unlink($ftplockfile);
print header(-cookie=>[$onlineviewcookie], -charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output("$boardname - FTP ����",\$output);
exit;

sub list
{
	my $onlineview = $query->cookie("onlineview");
	$onlineview = 0 if ($onlineview eq "");
	$onlineview = $onlineview == 1 ? 0 : 1 if ($action eq "onlineview");
	$onlineviewcookie = cookie(-name=>"onlineview", -value=>"$onlineview", -path=>"$cookiepath/", -expires=>"+30d");
	my $onlinetitle = $onlineview == 1 ? "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>�ر���ϸ�б�</font></a>]" : "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>��ʾ��ϸ�б�</font></a>]";

	#д���û�����״̬����������б�
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	unless (-e "$filetoopens.lck")
	{
		$screenmode = $query->cookie("screenmode");
		$screenmode = 8 if ($screenmode eq "");
		&whosonline("$inmembername\tFTP ����\tFTP ����\t�鿴 FTP �����б�");
		$membertongji =~ s/������̳/FTP ����/o;
		undef $memberoutput if ($onlineview != 1);
	}
	else
	{
		$memberoutput = "";
		$membertongji = " <b>���ڷ�������æ������ FTP ���˵�����������ʱ���ṩ��ʾ��</b>";
		$onlinetitle = "";
	}

	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(LIST, $listtoupdate);
	flock(LIST, 1) if ($OS_USED eq "Unix");
	my @ftpinfos = <LIST>;
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#ͷ�����������ͳ��
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT><table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr>
	<td bgcolor=$titlecolor width=92% $catbackpic><font color=$titlefontcolor>$membertongji�� $onlinetitle</td>
	<td bgcolor=$titlecolor width=8% align=center $catbackpic><a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 width=40 height=12></a></td>
</tr>~;
	$output .= qq~\n<tr><td colspan=2 bgcolor=$forumcolorone $otherbackpic><table cellPadding=1 cellSpacing=0>$memberoutput</table><script language="JavaScript"> function O9(id) {if(id != "") window.open("profile.cgi?action=show&member=" + id);}</script></td></tr>~ if ($onlineview == 1 && $memberoutput);
	$output .= qq~
</table></td></tr></table><SCRIPT>valignend()</SCRIPT><p>
<script language="JavaScript">
function Closed()
{
	alert("��� FTP Ŀǰ����ʱ�ر��ˣ�");
	return false;
}
function LeastRate()
{
	alert("�������ֵ���񲻹���� FTP �Ĳ鿴Ҫ��");
	return false;
}
function LeastMoney(myallmoney)
{
	alert("����������Һ��񲻹���ֻ�� " + myallmoney + " $moneyname��������� FTP �ĵ�¼����Ŷ��\\n������������д��Ļ��Ͻ�ȥȡǮ������ֻ���ֽ�:)");
	return false;
}
function MaxUser()
{
	alert("�鿴��� FTP ��¼���ϵ������Ѿ��ﵽ���޶���������");
	return false;
}
function ViewNEW(money, myallmoney)
{
	if (confirm("�������һ�β鿴��� FTP���������� " + myallmoney + " $moneyname�������ҡ�\\n�����¼������Ҫ������ " + money + " $moneyname�������ң��Ƿ������"))
		return true;
	else
		return false;
}
function ViewOLD()
{
	if (confirm("����ǰ�������� FTP �����ϣ��ٴβ鿴���軨Ǯ:) �Ƿ������"))
		return true;
	else
		return false;
}
function AdminView()
{
	if (confirm("������� FTP �Ĺ�����Ա���鿴���ϲ������ƣ��Ƿ������"))
		return true;
	else
		return false;	
}
</script>~;
	$output .= "\n<table width=$tablewidth align=center><tr><td>����<a href=$thisprog?action=add><font color=$fonthighlight><b>�����µ� FTP ����</b></font></a></td></tr></table>" if ($membercode eq "ad" || ",$saleusers," =~ /,$inmembername,/i);
	$output .= qq~
	<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr style="color: $titlefontcolor; font-weight: bold; background-color: $titlecolor" align=center><td $catbackpic>FTP ���� (�������)</td><td $catbackpic>״̬</td><td $catbackpic>����</td><td $catbackpic>����Ա</td><td $catbackpic>��ǰ�ۼ�</td><td $catbackpic>����Ҫ��</td><td $catbackpic>��������</td><td $catbackpic>�÷�</td></tr>~;

	foreach (@ftpinfos)
	{
		undef @ftpviews; undef $adminoption;
		chomp;
		my ($ftpid, $ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $_);
		my $viewfile = "$lbdir$ftpdir/view$ftpid.cgi";
		if (-e $viewfile)
		{
			open(VIEW, $viewfile);
			@ftpviews = <VIEW>;
			close(VIEW);
		}
		my @view = grep(/^$cleanmembername\t/, @ftpviews);
		my $viewnum = @ftpviews;
		$ftpmoney -= $ftpreduce * int(($currenttime - $ftptime) / 86400);
		$ftpmoney = 1 if ($ftpmoney < 1);

		if ($ftpstatus eq "close")
		{
			$prompt = "Closed()";
		}
		elsif (lc($inmembername) eq lc($ftpadmin) || $membercode eq "ad")
		{
			$prompt = "AdminView()";
		}
		elsif ($rating < $ftprate)
		{
			$prompt = "LeastRate()";
		}
		elsif (@view >= 1)
		{
			$prompt = "ViewOLD()";
		}
		elsif ($viewnum >= $ftpmaxuser && $ftpmaxuser ne "")
		{
			$prompt = "MaxUser()";
		}
		elsif ($myallmoney < $ftpmoney)
		{
			$prompt = "LeastMoney($myallmoney)";
		}
		else
		{
			$prompt = "ViewNEW($ftpmoney, $myallmoney)";
		}

		if (lc($inmembername) eq lc($ftpadmin) || $membercode eq "ad")
		{
			$adminoption = qq~<a href=$thisprog?action=edit&id=$ftpid><font color=$titlecolor>��</font></a> <font color=$titlecolor>|</font> <a href=$thisprog?action=delete&id=$ftpid OnClick="return confirm('�⽫����ɾ����� FTP �������ϣ����ֻ��һʱ�ж�ʹ�ã�������ֻ������ʱ�رա��Ƿ������');"><font color=$titlecolor>ɾ</font></a> <font color=$titlecolor>|</font> <a href=$thisprog?action=info&id=$ftpid><font color=$titlecolor>��¼</font></a>~;
		}
		$adminoption .= qq~ <font color=$titlecolor>|</font> <a href=$thisprog?action=up&id=$ftpid OnClick="return confirm('�⽫����� FTP ���������˵����λ�ã��Ƿ������');"><font color=$titlecolor>��</font></a>~ if ($membercode eq "ad");

		$ftpintro =~ s/<br>/\n/isg;
		$ftpname = "<font color=$fonthighlight><b>$ftpname</b></font>" if ($ftptype ne "priviate");
		$ftpname = qq~<a href=$thisprog?action=view&id=$ftpid OnClick="return $prompt;" title="$ftpintro">$ftpname</a>~;
		$ftpstatus = $ftpstatus eq "close" ? "�ر�" : "����";
		$ftptype = $ftptype eq "priviate" ? "����" : "����";
		my $encodeftpadmin = uri_escape($ftpadmin);
		$ftpadmin = "<a href=profile.cgi?action=show&member=$encodeftpadmin target=_blank>$ftpadmin</a>";
		$ftpmaxuser = $ftpmaxuser eq "" ? qq~<span title="��ǰ��������: $viewnum\n�������������: ����">$viewnum / MAX</span>~ : qq~<span title="��ǰ��������: $viewnum\n�������������: $ftpmaxuser">$viewnum / $ftpmaxuser</span>~;
		$pollscore = $polluser > 0 ? sprintf("%4.2f", $pollscore / $polluser) : "��";
		$output .= "\n<tr bgColor=$forumcolortwo align=center><td>$ftpname<div align=right>$adminoption</div></td><td>$ftpstatus</td><td>$ftptype</td><td>$ftpadmin</td><td><i>$ftpmoney</i> $moneyname</td><td>$ftprate</td><td>$ftpmaxuser</td><td>$pollscore</td></tr>";
	}

	$output .= qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT><table cellPadding=0 cellSpacing=0 width=$tablewidth><tr><td align=right width=100% style="line-height: 150%">&copy; <b>�������: <a href=http://www.94cool.net target=_blank><font color=5599ff>94Cool</font><font color=ff9955>.net</font></a></b> <a href=mailto:Jim_White\@etang.com>BigJim</a> </td></tr></table>~;

	if ($membercode eq "ad")
	{#̳�����Կ�������ѡ��
		$plugopenorclose = qq~<select name="plugstats"><option value="open">��������</option><option value="close">��ʱ�ر�</option></select>~;
		$plugopenorclose =~ s/value=\"$plugstats\"/value=\"$plugstats\" selected/;
		$output .= qq~<p>
<script language="JavaScript">
function AddSALE()
{
	if (name = prompt("������Ҫ��ӵ�������� FTP ����� ID��", ""))
	{
		if (CONFIG.saleusers.innerText) CONFIG.saleusers.innerText += "," + name;
		else CONFIG.saleusers.innerText = name;
	}
}
function DeleteSALE()
{
	if (name = prompt("������Ҫȥ����������� FTP ����� ID��", ""))
	{
		CONFIG.saleusers.innerText = eval("CONFIG.saleusers.innerText.replace(/," + name + "/ig" + ",'')");
		CONFIG.saleusers.innerText = eval("CONFIG.saleusers.innerText.replace(/" + name + ",/ig" + ",'')");
		CONFIG.saleusers.innerText = eval("CONFIG.saleusers.innerText.replace(/" + name + "/ig" + ",'')");
	}
}
function ShowConfig()
{
	if (configtable.style.display == "none")
	{
		configtable.style.display = "";
		showtext.innerHTML = "���� FTP ��������";
	}
	else
	{
		configtable.style.display = "none";
		showtext.innerHTML = "��ʾ FTP ��������";
	}
}
</script>
<SCRIPT>valigntop()</SCRIPT>
<table cellSpacing=0 cellPadding=0 width=$tablewidth bgColor=$tablebordercolor align=center><tr><td><table cellSpacing=1 cellPadding=6 width=100%>
<tr><td bgColor=$titlecolor $catbackpic><font color=$titlefontcolor>��<b>����ѡ��</b>����<input type=checkbox OnClick="ShowConfig()"> <span id=showtext>��ʾ FTP ��������</span></font>��������<a href=$thisprog?action=repair OnClick="return confirm('������ҳ����Ϣ��ʧ��ʱ�򣬿���ʹ�ô˹��ָܻ����Ƿ������')"><font color=$fonthighlight><b>�޸���������</b></font></a></td></tr>
<tr><td bgColor=$forumcolorone align=center><table id=configtable cellSpacing=15 style="display:none"><form name=CONFIG action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="config"><tr><td align=center><textarea name=saleusers rows=3 cols=40 readonly=true>$saleusers</textarea><br>��̳����������������Ա��<input type=button value="�� ��" OnClick="AddSALE()">��<input type=button value="ɾ ��" OnClick="DeleteSALE()"></td><td><br>����FTP ���˲��״̬: $plugopenorclose<br>�������� FTP ����Ա���: <input name=percent type=text size=3 value="$percent"> %<br><br>��������<input type=submit name=submit value="������">��<input type=reset value="�ء���"></td><form></tr></table></td></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
	}
	return;
}

sub view
{
	my $ftpid = $query->param("id");
	&myerror("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("��ͨ����&��Ҫ�鿴�� FTP �������ڣ�") unless (-e $infofile);

	#д���û�����״̬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ����\tnone\t�鿴 FTP �����¼����") unless(-e "$filetoopens.lck");

	open (INFO, $infofile);
	flock(INFO, 1) if ($OS_USED eq "Unix");
	my $ftpinfo = <INFO>;
	close(INFO);
	chomp($ftpinfo);
	my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, $ftpaddress, $ftpport, $ftpuser, $ftppass, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);

	&myerror("�鿴����&��� FTP �Ѿ���ʱ�رգ�") if ($ftpstatus eq "close");
	&myerror("�鿴����&������������鿴��� FTP �����Ҫ��") if ($rating < $ftprate && lc($inmembername) ne lc($ftpadmin) && $membercode ne "ad");

	my $viewfile = "$lbdir$ftpdir/view$ftpid.cgi";
	if (-e $viewfile)
	{
		open(VIEW, $viewfile);
		flock(VIEW, 1) if ($OS_USED eq "Unix");
		@ftpviews = <VIEW>;
		close(VIEW);
	}
	my @view = grep(/^$cleanmembername\t/, @ftpviews);
	if (@view < 1 && lc($inmembername) ne lc($ftpadmin) && $membercode ne "ad")
	{
		&myerror("�鿴����&�鿴��� FTP ��¼���ϵ������Ѿ��ﵽ���޶���������") if (@ftpviews >= $ftpmaxuser && $ftpmaxuser ne "");
		$ftpmoney -= $ftpreduce * int(($currenttime - $ftptime) / 86400);
		$ftpmoney = 1 if ($ftpmoney < 1);
		&myerror("�鿴����&�����̳�����ֽ𲻹�֧���鿴��� FTP �����¼��������Ҫ�Ļ��ѣ�") if ($myallmoney < $ftpmoney);

		#�����û���Ǯ�Ͳ鿴��¼
		use testinfo qw(ipwhere);
		my $fromwhere = &ipwhere($trueipaddress);
		&updateusermoney($inmembername, -$ftpmoney);
		&winlock($viewfile) if ($OS_USED eq "Nt");
		open(VIEW, ">>$viewfile");
		flock(VIEW, 2) if ($OS_USED eq "Unix");
		print VIEW "$cleanmembername\t$trueipaddress\t$currenttime\t$fromwhere\n";
		close(VIEW);
		&winunlock($viewfile) if ($OS_USED eq "Nt");
		&updateusermoney($ftpadmin, $ftpmoney * $percent / 100) if ($ftptype eq "priviate");
	}

	if ($ftpuser =~ /\*$/)
	{#ʹ��Serv-U�Ķ����˻���ʽ
		eval("use Digest::MD5 qw(md5_hex);");
		if ($@ eq "")
		{#MD5ģ�鹤������
			$ftpuser =~ s/\*$//o;
			$ftpuser .= $cleanmembername;
			$ftppass = md5_hex("$ftppass$ftpuser");
		}
	}
	$pollscore = $polluser > 0 ? sprintf("%4.2f", $pollscore / $polluser) . " ��" : "��";

	#���ҳ��
	&ftpheader;
	$output .= qq~
	<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr style="color: $fonthighlight; font-weight: bold; background-color: $titlecolor" align=center><td colSpan=2>$ftpname �ľ����¼����</td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" width=20% align=center>�����ַ:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$boardname</font>$ftpaddress<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>����˿�:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$boardname</font>$ftpport<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>��½�û�:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$boardname</font>$ftpuser<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>��½����:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$boardname</font>$ftppass<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>���˵��:��</td><td bgColor=$miscbacktwo><form action=$thisprog method=POST><input name=action type=hidden value="poll"><input name=id type=hidden value="$ftpid"><table width=100%><tr><td width=12></td><td>$ftpintro</td><td align=right>��ǰ����: $pollscore<br><br><select name=score><option value=1>1</option><option value=2>2</option><option value=3>3</option><option value=4>4</option><option value=5>5</option><option value=6 selected>6</option><option value=7>7</option><option value=8>8</option><option value=9>9</option><option value=10>10</option></select> <input type=submit value="����"></td></tr></table></td></tr></form>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
	return;
}

sub poll
{
	my $ftpid = $query->param("id");
	&myerror("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("��ͨ����&��Ҫ���ֵ� FTP �������ڣ�") unless (-e $infofile);
	my $score = $query->param("score");
	&myerror("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") unless ($score =~/^[0-9]+$/ && $score > 0 && $score <= 10);

	#д���û�����״̬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ����\tnone\t�� FTP ��������") unless(-e "$filetoopens.lck");

	#�����û����ֲ���ʱ��
	my $pollfile = "$lbdir$ftpdir/poll$ftpid.cgi";
	&winlock($pollfile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	if (-e $pollfile)
	{
		open(POLL, $pollfile);
		flock(POLL, 1) if ($OS_USED eq "Unix");
		@pollusers = <POLL>;
		close(POLL);
	}
	foreach (@pollusers)
	{
		chomp;
		my ($pollname, $lasttime) = split(/\t/, $_);
		$polltime{$pollname} = $lasttime;
	}
	if ($currenttime - $polltime{$cleanmembername} < 86400)
	{
		&winunlock($pollfile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		&myerror("���ִ���&�������24Сʱ���Ѿ������������������ˣ�");
	}
	$polltime{$cleanmembername} = $currenttime;
	open(POLL, ">$pollfile");
	flock(POLL, 2) if ($OS_USED eq "Unix");
	while (($pollname, $lasttime) = each(%polltime))
	{
		print POLL "$pollname\t$lasttime\n";
	}
	close(POLL);
	&winunlock($pollfile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#���·���������
	&winlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open (INFO, $infofile);
	flock(INFO, 1) if ($OS_USED eq "Unix");
	my $ftpinfo = <INFO>;
	close(INFO);
	chomp($ftpinfo);
	my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, $ftpaddress, $ftpport, $ftpuser, $ftppass, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);
	$polluser++;
	$pollscore += $score;
	open(INFO, ">$infofile");
	flock(INFO, 2) if ($OS_USED eq "Unix");
	print INFO "$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftpaddress\t$ftpport\t$ftpuser\t$ftppass\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore";
	close(INFO);
	&winunlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#���������ļ�
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	$filetoopens = &lockfilename($listtoupdate);
	unless(-e "$filetoopens.lck")
	{#������æ�������������
		&winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		open(LIST, $listtoupdate);
		flock(LIST, 1) if ($OS_USED eq "Unix");
		my @ftpinfos = <LIST>;
		close(LIST);
		open(LIST, ">$listtoupdate");
		flock(LIST, 2) if ($OS_USED eq "Unix");
		foreach (@ftpinfos)
		{
			chomp;
			my ($id, undef) = split(/\t/, $_);
			print LIST $id == $ftpid ? "$ftpid\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n" : "$_\n";
		}
		close(LIST);
		&winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	}

	#�����ת����ҳ��
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�� FTP �������ֳɹ���</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������û���Զ����أ�������������ӣ�<ul><li><a href=$thisprog>���� FTP ����ҳ��</a><li><a href=$thisprog?action=view&id=$ftpid>���� FTP ��¼����</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub add
{
	&myerror("Ȩ�޴���&��û��Ȩ������ FTP ����") unless ($membercode eq "ad" || ",$saleusers," =~ /,$inmembername,/i);

	#д���û�����״̬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ����\tnone\t���� FTP") unless(-e "$filetoopens.lck");

	&ftpheader;
	my $statusoption = qq~<input name=ftpstatus type=radio value="open" checked> �������š���<input name=ftpstatus type=radio value="close"> ��ʱ�ر�~;
	my $typeoption = qq~<select name=ftptype><option value="public">��̳����</option><option value="priviate">���˷���</option></select>~;
	my $rateoption = "";
	for (0 .. $maxweiwang)
	{
		$rateoption .= qq~<option value="$_">$_</option>~;
	}
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="addok">
<tr><td bgcolor=$miscbackone align=center><table width=80%>
<tr><td><b>FTP ״̬(*): ����</b>$statusoption</td></tr>
<tr><td><b>FTP ����(*): ����</b><input name=ftpname type=text size=60></td></tr>
<tr><td><b>FTP ����(*): ����</b>$typeoption����<i>ѡ����˷������ͣ��������˿��Եõ��� FTP ����� $percent% ��Ϊ���͡�</i></td></tr>
<tr><td><b>FTP ��ַ(*): ����</b><input name=ftpaddress type=text size=24></td></tr>
<tr><td><b>FTP �˿�(*): ����</b><input name=ftpport type=text size=8 value="21" OnFocus="this.select()"></td></tr>
<tr><td><b>��¼�û�����(*): </b><input name=ftpuser type=text size=36></td></tr>
<tr><td><b>��¼����(*): ����</b><input name=ftppass type=text size=36></td></tr>
<tr><td>����<i>ע�⣺�����Ҫʹ�� Serv-U �Ķ����ʻ����ܣ��뽫��¼�û�������û���ǰ׺ +��*������ʽ�����硰leobbs_*���������û���BigJim������õ��û������ǡ�leobbs_bigjim������¼������ Serv-U ������趨����������ʹ�õ�Key��Serv-U û�а�װ����������ʹ�ã�Serv-U ��������ص�ַΪ <a href=http://www.94cool.net/download/Serv-U.rar>http://www.94cool.net/download/Serv-U.rar</a>��</i></td></tr>
<tr><td><b>�鿴��Ҫ����(*): </b><select name=ftprate>$rateoption</select></td></tr>
<tr><td><b>��ʼ�ۼ�(*): ����</b><input name=ftpmoney type=text size=18></td></tr>
<tr><td><b>ÿ24Сʱ����:����</b><input name=ftpreduce type=text size=15>����<i>����Ҫ�����ա�</i></td></tr>
<tr><td><b>����������:����</b><input name=ftpmaxuser type=text size=8>����<i>�ﵽ�����Ժ�FTP ���Զ�ֹͣ���ۣ�����������������ա�</i></td></tr>
<tr><td><b>FTP �������:����</b><textarea name=ftpintro rows=5 cols=60></textarea></td></tr>
<tr><td align=center><br><input type=submit name=submit value="��������"></td></tr>
</table></td></tr></form>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
	return;
}

sub addok
{
	&myerror("Ȩ�޴���&��û��Ȩ������ FTP ����") unless ($membercode eq "ad" || ",$saleusers," =~ /,$inmembername,/i);

	for ("ftpstatus", "ftpname", "ftptype", "ftpaddress", "ftpport", "ftpuser", "ftppass", "ftprate", "ftpmoney", "ftpreduce", "ftpmaxuser", "ftpintro")
	{
		${$_} = &cleaninput($query->param($_));
	}
	#������
	$ftpstatus = "open" unless ($ftpstatus eq "close");
	&myerror("�������&��û������ FTP �����ƣ�") if ($ftpname eq "");
	$ftptype = "public" unless ($ftptype eq "priviate");
	&myerror("�������&��û������ FTP �ĵ�ַ��") if ($ftpaddress eq "");
	$ftpport = 21 unless ($ftpport =~ /^[0-9]+$/);
	&myerror("�������&��û������ FTP ���û�����") if ($ftpuser eq "");
	&myerror("�������&��û������ FTP �����룡") if ($ftppass eq "");
	$ftprate = 0 unless ($ftprate =~ /^[0-9]+$/);
	$ftpmoney = 1 unless ($ftpmoney =~ /^[0-9]+$/);
	$ftpreduce = "" unless ($ftpreduce =~ /^[0-9]+$/);
	$ftpmaxuser = "" unless ($ftpmaxuser =~ /^[0-9]+$/);

	#д���û�����״̬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ����\tnone\t���� FTP") unless(-e "$filetoopens.lck");

	#ȡ����FTP��ID
	my $numfiletoupdate = "$lbdir$ftpdir/lastnum.cgi";
	if (open(NUMFILE, $numfiletoupdate))
	{
		$lastnumber = <NUMFILE>;
		close(NUMFILE);
		chomp($lastnumber);
	}
	do
	{
		$lastnumber++;
	} while (-e "$lbdir$ftpdir/info$lastnumber.cgi");
	open(NUMFILE, ">$numfiletoupdate");
	flock(NUMFILE, 2) if ($OS_USED eq "Unix");
	print NUMFILE $lastnumber;
	close(NUMFILE);

	#д���������ļ�
	open(INFO, ">$lbdir$ftpdir/info$lastnumber.cgi");
	print INFO "$ftpstatus\t$ftpname\t$ftptype\t$inmembername\t$currenttime\t$ftpaddress\t$ftpport\t$ftpuser\t$ftppass\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t0\t0";
	close(INFO);

	#���������ļ�
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt");
	open(LIST, ">>$listtoupdate");
	flock(LIST, 2) if ($OS_USED eq "Unix");
	print LIST "$lastnumber\t$ftpstatus\t$ftpname\t$ftptype\t$inmembername\t$currenttime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t0\t0\t0\n";
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt");

	#�����ת����ҳ��
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>������� FTP �ɹ���</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������û���Զ����أ�������������ӣ�<ul><li><a href=$thisprog>���� FTP ����ҳ��</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub edit
{
	my $ftpid = $query->param("id");
	&myerror("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("��ͨ����&��Ҫ�༭�� FTP �������ڣ�") unless (-e $infofile);

	#д���û�����״̬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ����\tnone\t�༭ FTP ����") unless(-e "$filetoopens.lck");

	#����ɵ�����
	open (INFO, $infofile);
	flock(INFO, 1) if ($OS_USED eq "Unix");
	my $ftpinfo = <INFO>;
	close(INFO);
	chomp($ftpinfo);
	my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, undef, $ftpaddress, $ftpport, $ftpuser, $ftppass, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, undef) = split(/\t/, $ftpinfo);
	&myerror("Ȩ�޴���&��û��Ȩ���༭��� FTP��") unless ($membercode eq "ad" || lc($inmembername) eq lc($ftpadmin));

	&ftpheader;
	my $statusoption = qq~<input name=ftpstatus type=radio value="open"> �������š���<input name=ftpstatus type=radio value="close"> ��ʱ�ر�~;
	$statusoption =~ s/value=\"$ftpstatus\"/value=\"$ftpstatus\" checked/o;
	my $typeoption = qq~<select name=ftptype><option value="public">��̳����</option><option value="priviate">���˷���</option></select>~;
	$typeoption =~ s/value=\"$ftptype\"/value=\"$ftptype\" selected/o;
	my $rateoption = "";
	for (0 .. $maxweiwang)
	{
		$rateoption .= qq~<option value="$_">$_</option>~;
	}
	$rateoption =~ s/value=\"$ftprate\"/value=\"$ftprate\" selected/o;
	$ftpintro =~ s/<br>/\n/isg;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="editok"><input type=hidden name=id value="$ftpid">
<tr><td bgcolor=$miscbackone align=center><table width=80%>
<tr><td><b>FTP ״̬(*): ����</b>$statusoption</td></tr>
<tr><td><b>FTP ����(*): ����</b><input name=ftpname type=text size=60 value="$ftpname"></td></tr>
<tr><td><b>FTP ����(*): ����</b>$typeoption����<i>ѡ����˷������ͣ��������˿��Եõ��� FTP ����� $percent% ��Ϊ���͡�</i></td></tr>
<tr><td><b>FTP ��ַ(*): ����</b><input name=ftpaddress type=text size=24 value="$ftpaddress"></td></tr>
<tr><td><b>FTP �˿�(*): ����</b><input name=ftpport type=text size=8 value="$ftpport" OnFocus="this.select()" value="$ftpport"></td></tr>
<tr><td><b>��¼�û�����(*): </b><input name=ftpuser type=text size=36 value="$ftpuser"></td></tr>
<tr><td><b>��¼����(*): ����</b><input name=ftppass type=text size=36 value="$ftppass"></td></tr>
<tr><td>����<i>ע�⣺�����Ҫʹ�� Serv-U �Ķ����ʻ����ܣ��뽫��¼�û�������û���ǰ׺ +��*������ʽ�����硰dlmovie_*���������û���BigJim������õ��û������ǡ�dlmovie_bigjim������¼������ Serv-U ������趨����������ʹ�õ�Key��Serv-U û�а�װ����������ʹ�ã�Serv-U ��������ص�ַΪ <a href=http://www.94cool.net/download/Serv-U.rar>http://www.94cool.net/download/Serv-U.rar</a>��</i></td></tr>
<tr><td><b>�鿴��Ҫ����(*): </b><select name=ftprate>$rateoption</select></td></tr>
<tr><td><b>��ʼ�ۼ�(*): ����</b><input name=ftpmoney type=text size=18 value="$ftpmoney"></td></tr>
<tr><td><b>ÿ24Сʱ����:����</b><input name=ftpreduce type=text size=15 value="$ftpreduce">����<i>����Ҫ�����ա�</i></td></tr>
<tr><td><b>����������:����</b><input name=ftpmaxuser type=text size=8 value="$ftpmaxuser">����<i>�ﵽ�����Ժ�FTP ���Զ�ֹͣ���ۣ�����������������ա�</i></td></tr>
<tr><td><b>FTP �������:����</b><textarea name=ftpintro rows=5 cols=60>$ftpintro</textarea></td></tr>
<tr><td><b>������в鿴��¼:</b>����<input name=ftpclear type=checkbox value="yes"> <i>ѡ������Ժ�FTP �Ĳ鿴��Ա�����ᱻ��գ������˾������»�����̳���ҹ����µĵ�¼���ϡ�</i></td></tr>
<tr><td align=center><br><input type=submit name=submit value="��������"></td></tr>
</table></td></tr></form>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
	return;
}

sub editok
{
	my $ftpid = $query->param("id");
	&myerror("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("��ͨ����&��Ҫ�༭�� FTP �������ڣ�") unless (-e $infofile);

	for ("ftpstatus", "ftpname", "ftptype", "ftpaddress", "ftpport", "ftpuser", "ftppass", "ftprate", "ftpmoney", "ftpreduce", "ftpmaxuser", "ftpintro", "ftpclear")
	{
		${$_} = &cleaninput($query->param($_));
	}
	#������
	$ftpstatus = "open" unless ($ftpstatus eq "close");
	&myerror("�������&��û������ FTP �����ƣ�") if ($ftpname eq "");
	$ftptype = "public" unless ($ftptype eq "priviate");
	&myerror("�������&��û������ FTP �ĵ�ַ��") if ($ftpaddress eq "");
	$ftpport = 21 unless ($ftpport =~ /^[0-9]+$/);
	&myerror("�������&��û������ FTP ���û�����") if ($ftpuser eq "");
	&myerror("�������&��û������ FTP �����룡") if ($ftppass eq "");
	$ftprate = 0 unless ($ftprate =~ /^[0-9]+$/);
	$ftpmoney = 1 unless ($ftpmoney =~ /^[0-9]+$/);
	$ftpreduce = "" unless ($ftpreduce =~ /^[0-9]+$/);
	$ftpmaxuser = "" unless ($ftpmaxuser =~ /^[0-9]+$/);

	#д���û�����״̬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ����\tnone\t�༭ FTP ����") unless(-e "$filetoopens.lck");

	&winlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open (INFO, $infofile);
	flock(INFO, 1) if ($OS_USED eq "Unix");
	my $ftpinfo = <INFO>;
	close(INFO);
	chomp($ftpinfo);
	my (undef, undef, undef, $ftpadmin, $ftptime, undef, undef, undef, undef, undef, undef, undef, undef, undef, $polluser, $pollscore) = split(/\t/, $ftpinfo);
	unless ($membercode eq "ad" || lc($inmembername) eq lc($ftpadmin))
	{
		&winunlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		&myerror("Ȩ�޴���&��û��Ȩ���༭��� FTP��");
	}

	#��ղ鿴��¼
	if ($ftpclear eq "yes")
	{
		unlink("$lbdir$ftpdir/view$ftpid.cgi");
		$ftptime = $currenttime;
	}

	#���������ļ�
	open(INFO, ">$infofile");
	flock(INFO, 2) if ($OS_USED eq "Unix");
	print INFO "$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftpaddress\t$ftpport\t$ftpuser\t$ftppass\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore";
	close(INFO);
	&winunlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#���������ļ�
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(LIST, $listtoupdate);
	flock(LIST, 1) if ($OS_USED eq "Unix");
	my @ftpinfos = <LIST>;
	close(LIST);
	open(LIST, ">$listtoupdate");
	flock(LIST, 2) if ($OS_USED eq "Unix");
	foreach (@ftpinfos)
	{
		chomp;
		my ($id, undef) = split(/\t/, $_);
		print LIST $id == $ftpid ? "$ftpid\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n" : "$_\n";
	}
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#�����ת����ҳ��
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�༭��� FTP ���ϳɹ���</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������û���Զ����أ�������������ӣ�<ul><li><a href=$thisprog>���� FTP ����ҳ��</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub info
{
	use testinfo qw(ipwhere);

	my $ftpid = $query->param("id");
	&myerror("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("��ͨ����&��Ҫ��ѯ�� FTP �������ڣ�") unless (-e $infofile);

	#д���û�����״̬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ����\tnone\t��ѯ FTP �����¼") unless(-e "$filetoopens.lck");

	#�ж��û�Ȩ��
	if ($membercode ne "ad")
	{
		open (INFO, $infofile);
		flock(INFO, 1) if ($OS_USED eq "Unix");
		my $ftpinfo = <INFO>;
		close(INFO);
		chomp($ftpinfo);
		my (undef, undef, undef, $ftpadmin, undef) = split(/\t/, $ftpinfo);
		&myerror("Ȩ�޴���&��û��Ȩ����ѯ��� FTP �Ĺ����¼��") unless (lc($inmembername) eq lc($ftpadmin));
	}

	#��ȡ�鿴��¼
	my $viewfile = "$lbdir$ftpdir/view$ftpid.cgi";
	if (-e $viewfile)
	{
		open(VIEW, $viewfile);
		flock(VIEW, 1) if ($OS_USED eq "Unix");
		@ftpusers = <VIEW>;
		close(VIEW);
	}

	#��ָ��IP��������
	my $key = $query->param("key");
	$key = "" unless ($key =~ /^[0-9\.]+$/);
	$key =~ s/^\.//sg;
	$key =~ s/\.$//sg;
	if ($key ne "")
	{
		@ips = split(/\./, $key);
		if (@ips < 4)
		{
			@ftpusers = grep(/\t$key\./, @ftpusers);
		}
		else
		{
			@ftpusers = grep(/\t$key/, @ftpusers);
		}
	}
	$allitems = @ftpusers;
	&splitpage("action=info&id=$ftpid&key=$key"); #��ҳ

	#���ҳ��
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr style="color: $titlefontcolor; font-weight: bold; background-color: $titlecolor" align=center><td $catbackpic>�鿴��</td><td $catbackpic>����IP</td><td $catbackpic>��Դ����</td><td $catbackpic>����ʱ��</td></tr>~;
	my $timeadd = ($timezone + $timedifferencevalue) * 3600;
	for ($i = $startnum; $i >= $endnum; $i--)
	{
		my $userinfo = $ftpusers[$i];
		chomp($userinfo);
		my ($username, $userip, $usertime, $userwhere) = split(/\t/, $userinfo);
		my $encodename = uri_escape($username);
		$userwhere = &ipwhere($userip) if ($userwhere eq "");
		my $usertime = &dateformatshort($usertime);
		$output .= qq~\n<tr align=center bgColor=$forumcolorone><td><a href=profile.cgi?action=show&member=$encodename target=_blank>$username</a></td><td>$userip</td><td>$userwhere</td><td>$usertime</td></tr>~;
	}
	$output .= qq~
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth align=center>
<form action=$thisprog><input name=action type=hidden value="info"><input name=id type=hidden value="$ftpid"><tr><td>$pages</td>
<td align=right>���ղ鿴��IP����(֧�ְ�A��B��C���ַ����) <input name=key type=text size=16> <input type=submit value="�� ��"></td></tr>
</table></form>~;
	return;
}

sub delete
{
	my $ftpid = $query->param("id");
	&myerror("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("��ͨ����&��Ҫɾ���� FTP �������ڣ�") unless (-e $infofile);

	#д���û�����״̬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ����\tnone\tɾ�� FTP ����") unless(-e "$filetoopens.lck");

	#�ж��û�Ȩ��
	if ($membercode ne "ad")
	{
		open (INFO, $infofile);
		flock(INFO, 1) if ($OS_USED eq "Unix");
		my $ftpinfo = <INFO>;
		close(INFO);
		chomp($ftpinfo);
		my (undef, undef, undef, $ftpadmin, undef) = split(/\t/, $ftpinfo);
		&myerror("Ȩ�޴���&��û��Ȩ��ɾ����� FTP��") unless (lc($inmembername) eq lc($ftpadmin));
	}

	#ɾ�������ļ�
	unlink("$lbdir$ftpdir/info$ftpid.cgi");
	unlink("$lbdir$ftpdir/view$ftpid.cgi");
	unlink("$lbdir$ftpdir/poll$ftpid.cgi");

	#���������ļ�
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(LIST, $listtoupdate);
	flock(LIST, 1) if ($OS_USED eq "Unix");
	my @ftpinfos = <LIST>;
	close(LIST);
	open(LIST, ">$listtoupdate");
	flock(LIST, 2) if ($OS_USED eq "Unix");
	foreach (@ftpinfos)
	{
		chomp;
		my ($id, undef) = split(/\t/, $_);
		print LIST "$_\n" unless ($id == $ftpid);
	}
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#�����ת����ҳ��
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>ɾ�� FTP ���ϳɹ���</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������û���Զ����أ�������������ӣ�<ul><li><a href=$thisprog>���� FTP ����ҳ��</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub up
{
	&myerror("Ȩ�޴���&����Ȩ���� FTP λ�ã�") unless ($membercode eq "ad");
	my $ftpid = $query->param("id");
	&myerror("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("��ͨ����&��Ҫ������ FTP �������ڣ�") unless (-e $infofile);

	#д���û�����״̬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ����\tnone\t���� FTP λ��") unless(-e "$filetoopens.lck");

	#����ɵ�����
	open (INFO, $infofile);
	flock(INFO, 1) if ($OS_USED eq "Unix");
	my $ftpinfo = <INFO>;
	close(INFO);
	chomp($ftpinfo);
	my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, undef, undef, undef, undef, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);

	#���������ļ�
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(LIST, $listtoupdate);
	flock(LIST, 1) if ($OS_USED eq "Unix");
	my @ftpinfos = <LIST>;
	close(LIST);
	open(LIST, ">$listtoupdate");
	flock(LIST, 2) if ($OS_USED eq "Unix");
	print LIST "$ftpid\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n";
	foreach (@ftpinfos)
	{
		chomp;
		my ($id, undef) = split(/\t/, $_);
		print LIST "$_\n" unless ($id == $ftpid);
	}
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#�����ת����ҳ��
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>���� FTP λ�óɹ���</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������û���Զ����أ�������������ӣ�<ul><li><a href=$thisprog>���� FTP ����ҳ��</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub repair
{
	&myerror("Ȩ�޴���&����Ȩ���� FTP ���˹���") unless ($membercode eq "ad");

	#д���û�����״̬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ����\tnone\t�޸� FTP ����") unless(-e "$filetoopens.lck");

	#��ȡ���������ļ�ID������
	opendir(DIR, "$lbdir$ftpdir");
	my @infofiles = readdir(DIR);
	closedir(DIR);
	@infofiles = grep(/^info[0-9]+\.cgi$/i, @infofiles);
	foreach (@infofiles)
	{
		s/^info//is;
		s/\.cgi$//is;
	}
	@infofiles = sort numerically @infofiles;

	#���´������ļ��ж���
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt");
	open(LIST, ">$listtoupdate");
	flock(LIST, 2) if ($OS_USED eq "Unix");
	foreach (@infofiles)
	{
		open (INFO, "$lbdir$ftpdir/info$_.cgi");
		flock(INFO, 1) if ($OS_USED eq "Unix");
		my $ftpinfo = <INFO>;
		close(INFO);
		chomp($ftpinfo);
		my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, undef, undef, undef, undef, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);
		print LIST "$_\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n";
	}
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt");

	#�����ת����ҳ��
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�ؽ� FTP ����������ɣ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������û���Զ����أ�������������ӣ�<ul><li><a href=$thisprog>���� FTP ����ҳ��</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub config
{
	&myerror("Ȩ�޴���&����Ȩ���� FTP ���˹���") unless ($membercode eq "ad");

	#д���û�����״̬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ����\tnone\t�趨 FTP ����") unless(-e "$filetoopens.lck");

	my $newsaleusers = $query->param("saleusers");
	my $newpercent = $query->param("percent");
	my $newplugstats = $query->param("plugstats");
	$newpercent = 10 if ($newpercent eq "");
	$newplugstats = "open" if ($newplugstats eq "");
	if (($newpercent ne "")||($newsaleusers ne "")||($newplugstats ne "")) {
	    my $configtomake = "$lbdir$ftpdir/conf.cgi";
	    &winlock($configtomake) if ($OS_USED eq "Nt");
	    open(CONFIG, ">$configtomake");
	    flock(CONFIG, 2) if ($OS_USED eq "Unix");
	    print CONFIG qq~\$plugstats = "$newplugstats";\n\$saleusers = "$newsaleusers";\n\$percent = $newpercent;\n1;~;
	    close(CONFIG);
	    &winunlock($configtomake) if ($OS_USED eq "Nt");
	}

	#�����ת����ҳ��
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�޸� FTP ����������ɣ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������û���Զ����أ�������������ӣ�<ul><li><a href=$thisprog>���� FTP ����ҳ��</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;	
}

sub ftpheader
{#���ͷ��������
	my $boardgraphic = $boardlogo =~ /\.swf$/i ? qq~<param name=play value=true><param name=loop value=true><param name=quality value=high><embed src=$imagesurl/myimages/$boardlogo quality=high width=$fgwidth height=$fgheight pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application/x-shockwave-flash"></embed>~ : "<img src=$imagesurl/myimages/$boardlogo border=0>";

	my $jump;
	if ($action eq "view")
	{
		$jump = qq~�鿴 FTP �����¼����~;
	}
	elsif ($action eq "poll")
	{
		$jump = qq~�� FTP ��������~;
	}
	elsif ($action eq "add")
	{
		$jump = qq~������� FTP~;
	}
	elsif ($action eq "addok")
	{
		$jump = qq~������� FTP �ɹ�~;
	}
	elsif ($action eq "edit")
	{
		$jump = qq~�༭��� FTP ����~;
	}
	elsif ($action eq "editok")
	{
		$jump = qq~�༭��� FTP ���ϳɹ�~;
	}
	elsif ($action eq "info")
	{
		$jump = qq~�鿴 FTP �����¼~;
	}
	elsif ($action eq "delete")
	{
		$jump = qq~ɾ�� FTP ���ϳɹ�~;
	}
	elsif ($action eq "up")
	{
		$jump = qq~���� FTP λ�óɹ�~;
	}
	elsif ($action eq "repair")
	{
		$jump = qq~�ؽ� FTP �����������~;
	}
	elsif ($action eq "config")
	{
		$jump = qq~�޸� FTP �����������~;
	}
	else
	{
		$jump = qq~�鿴 FTP ����~;
	}

	&title;
	$output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> �����������Բ鿴��վ FTP ���˵��б���ϸ��Ϣ</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> �� <a href=$thisprog>FTP ����</a> �� $jump<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
~;
	return;
}

sub updateusermoney
{#�����û���Ǯ
	my ($nametochange, $cmoney) = @_;
	$nametochange =~ s/ /\_/sg;
	$nametochange =~ tr/A-Z/a-z/;
	my $namenumber = &getnamenumber($nametochange);
	&checkmemfile($nametochange,$namenumber);
	my $memfiletoupdate = "$lbdir$memdir/$namenumber/$nametochange.cgi";
	$memfiletoupdate = &stripMETA($memfiletoupdate);
	if (-e $memfiletoupdate)
	{
		&winlock($memfiletoupdate) if ($OS_USED eq "Nt");
		open(FILE, $memfiletoupdate);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my $filedata = <FILE>;
		close(FILE);
		chomp($filedata);
		my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $soccerdata,$useradd5) = split(/\t/, $filedata);
		$mymoney += int($cmoney);
		if ($membername ne "" && $password ne "")
		{
			open(FILE, ">$memfiletoupdate");
			flock(FILE, 2) if ($OS_USED eq "Unix");
			print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$soccerdata\t$useradd5";
			close(FILE);
		}
		&winunlock($memfiletoupdate) if ($OS_USED eq "Nt");
	}
	return;
}

sub splitpage
{#��÷�ҳ
	my $addstring = shift;
	my $instart = $query->param("start");
	$instart = 0 if ($instart !~ /^[0-9]+$/);

	my $temppages = $allitems / 20;
	my $numberofpages = int($temppages);
	$numberofpages++ if ($numberofpages != $temppages);

	if ($numberofpages > 1)
	{
		$startnum = $allitems - $instart - 1;
		$endnum = $startnum - 19;
		$endnum = 0 if ($endnum < 0);

		my $currentpage = int($instart / 20) + 1;
		my $endstart = ($numberofpages - 1) * 20;
		my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<a href=$thisprog?start=0&$addstring title="�� ҳ" ><font face=webdings>9</font></a>~;
		my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<a href=$thisprog?start=$endstart&$addstring title="β ҳ" ><font face=webdings>:</font></a>~;

		my $uppage = $currentpage - 1;
		my $nextpage = $currentpage + 1;
		my $upstart = $instart - 20;
		my $nextstart = $instart + 20;
		my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<a href=$thisprog?start=$upstart&$addstring title="��$uppageҳ"><font face=webdings>7</font></a>~;
		my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<a href=$thisprog?start=$nextstart&$addstring title="��$nextpageҳ"><font face=webdings>8</font></a>~;

		my $tempstep = $currentpage / 7;
		my $currentstep = int($tempstep);
		$currentstep++ if ($currentstep != $tempstep);
		my $upsteppage = ($currentstep - 1) * 7;
		my $nextsteppage = $currentstep * 7 + 1;
		my $upstepstart = ($upsteppage - 1) * 20;
		my $nextstepstart = ($nextsteppage - 1) * 20;
		my $showupstep = $upsteppage < 1 ? "" : qq~<a href=$thisprog?start=$upstepstart&$addstring class=hb title="��$upsteppageҳ">��</a> ~;
		my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<a href=$thisprog?start=$nextstepstart&$addstring class=hb title="��$nextsteppageҳ">��</a> ~;

		$pages = "";
		my $currentstart = $upstepstart + 20;
		for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++)
		{
			last if ($i > $numberofpages);
			$pages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<a href=$thisprog?start=$currentstart&$addstring class=hb>$i</a> ~;
			$currentstart += 20;
		}
		$pages = "<font color=$menufontcolor><b>�� <font color=$fonthighlight>$numberofpages</font> ҳ</b> $beginpage $showup \[ $showupstep$pages$shownextstep\] $shownext $endpage</font><br>";
	}
	else
	{
		$startnum = $allitems - 1;
		$endnum = 0;
		$pages = "<font color=$menufontcolor>ֻ��һҳ</font><br>";
	}
	return;
}

sub myerror
{
	my $errorinfo = shift;
	unlink($ftplockfile);
	&error($errorinfo);
	return;
}