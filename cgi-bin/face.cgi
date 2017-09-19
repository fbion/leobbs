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
$LBCGI::POST_MAX=800000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "data/cityinfo.cgi";
require "face/config.pl";
require "facelib.pl";
$|++;
$thisprog = "face.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
}

&ipbanned; #��ɱһЩ ip

$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));

if ($inmembername eq "" || $inmembername eq "����" ) {
    &error("���ܽ��� $plugname &��Ŀǰ������Ƿÿͣ����ȵ�½!");
    exit;
} else {
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie  = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie  = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
}

&error("��ʱ�ر�&$plugnameά���У����Ժ���ʣ�������ǹ���Ա������� <a href=setface.cgi>��̨����</a> ������") if ($close_plug eq 'close');

&error("��ͨ����&��������Ա�Ϊ���ܣ����ܽ��뱾ϵͳ����<a href=profile.cgi?action=modify>���޸���ĸ�������</a>��") if(($sex eq 'no')||($sex eq ''));

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

&title;

$tempmembername = $membername;
$tempmembername =~ s/ /\_/g;
$tempmembername =~ tr/A-Z/a-z/;

$equiplayer = $query->cookie("tempequip");

&readface("$tempmembername",0);

if ($currequip eq '')
{
    # ��� Cookie ��ֵΪ�գ�����Ӧ�Ա�ĳ�ʼֵ���ݸ� $equiplayer
    $equiplayer = $sex eq 'f' ? $fairsex : $mansex if ($equiplayer eq '');
    $equipcookie = cookie(-name => "tempequip", -value => "$equiplayer", -path => "$cookiepath/", -expires => "-1m");
    print header(-cookie=>[$equipcookie], -charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
}
else
{
    $output .= qq~<SCRIPT LANGUAGE="JavaScript">document.cookie = "tempequip=" + "$currequip" +"; path=$cookiepath/";</SCRIPT>~ if ($equiplayer eq '');
    print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
}

$tempmembername = $membername;
$tempmembername =~ s/ /\_/g;
$tempmembername =~ tr/A-Z/a-z/;

$admin_user =~ s/ /\_/g;
$admin_user =~ tr/A-Z/a-z/;

$adminbar = qq~ <img src=$imagesurl/images/fg.gif width=1 height=10> [<a href=setface.cgi>��̨����</a>]~ if (($membercode eq "ad")||($admin_user eq $tempmembername));
$mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
$output .= qq~
<!--3FACE V4.0 Powered By CPower-->
<BODY>
<script>
function openCart() 
{
   var url="buyface.cgi?action=bag"
   var cart;
   cart =window.open(url,"Cart","menubar=no,toolbar=no,location=no,directories=no,status=no,width=530,height=400,scrollbars=yes");
   cart.focus();
}
</script>
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> �����������Թ���װ�������͡����ú͹��������������</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> �� <a href=face.cgi>$plugname</a>$adminbar<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=2 cellspacing=1 border=0 width=100%>
<tr><td colspan="2" align=center bgcolor=$titlecolor $catbackpic>
<table width=100% border=0 cellspacing=0 cellpadding=5>
<tr><td align=left>��Ŀǰ���ֽ�Ϊ��$mymoney1 $moneyname</td><td align=right><B><a href="$thisprog?action=mylog&id=1">ϵͳ��¼</a> | <a href="$thisprog?action=perset">��������</a> | <a href="$thisprog?action=mybureau">�ҵ��¹�</a> | <a href="$thisprog?action=splist">��Ʒ</a> | <a href="javascript:openCart()">�����</a></B>&nbsp;</td>
</tr></table></td></tr><tr bgcolor=$miscbackone><td width=150 valign=top>
<DIV id=Show style='padding:0;position:relative;top:0;left:0;width:140;height:226'></div>~;
$output .= qq~<DIV align=center id=rein><a href=$thisprog?action=init>�ָ�ԭʼ״̬</a></DIV>~ if($filenobeling ne '1');
$output .= qq~
<SCRIPT>
<!--
function Fitting(face,id)
{
   var showArray = face.split('-');
   var s="";
   for (var i=0; i<=25; i++)
   {
	if(showArray[i] != '0')
	    s+="<IMG id=s"+i+" src=$imagesurl/face/"+i+"/"+showArray[i]+".gif style='padding:0;position:absolute;top:0;left:0;width:140;height:226;z-index:"+i+";'>";
   }
   s += "<IMG src=$imagesurl/face/blank.gif style='padding:0;position:absolute;top:0;left:0;width:140;height:226;z-index:50;'>";
   id.innerHTML=s;
}

function Buy(par1,par2,par3,par4)
{
addItemQuantity(par1,par2,par3,par4);
}
-->
</SCRIPT>
<SCRIPT language="javaScript" type="text/javascript" SRC="$imagesurl/face/js/buy.js"></SCRIPT>
<SCRIPT language="javaScript" type="text/javascript" SRC="$imagesurl/face/js/3face.js"></SCRIPT>
</td><td valign=top width=*>~;

$action = $query -> param('action');

my %Mode = ('splist'=> \&splist,'mylog'=> \&mylog,'mybureau'=> \&mybureau,'init'=> \&init_face,'cleanall'=> \&cleanall_face,'perset'=> \&perset,'bag'=> \&bag);

if ($Mode{$action})
{$Mode{$action} -> () ;}
else
{&facehelp;}

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	&whosonline("$membername\t$plugname\tnone\t�鿴��������Ʒ\t");
    }

$output .= qq~</td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;

sub init_face
{   # �ָ�ԭʼ״̬
    $output .= qq~<SCRIPT LANGUAGE="JavaScript">document.cookie = "tempequip=" + "$currequip" +"; path=$cookiepath/";</SCRIPT><meta http-equiv="refresh" content="0; url=$thisprog">~;
}

sub cleanall_face
{   # �������
	$nametocheck = $membername;
	my $nametochecktemp = $membername;
	$nametocheck =~ s/ /\_/g;
	$nametocheck =~ tr/A-Z/a-z/;
        $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
	my $namenumber = &getnamenumber($nametocheck);
	&checkmemfile($nametocheck,$namenumber);
        my $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi";
	if (-e $filetoopen) {
	    &winlock($filetoopen) if ($OS_USED eq "Nt");
	    open(FILE6,"+<$filetoopen");
	    flock (FILE6, 2) if ($OS_USED eq "Unix");
            my $filedata = <FILE6>;
	    chomp($filedata);
	    (my $membername, my $password, my $membertitle, my $membercode, my $numberofposts, my $emailaddress, my $showemail, my $ipaddress, my $homepage, my $oicqnumber, my $icqnumber ,my $location ,my $interests, my $joineddate, my $lastpostdate, my $signature, my $timedifference, my $privateforums, my $useravatar, my $userflag,my  $userxz, my $usersx, my $personalavatar, my $personalwidth, my $personalheight, my $rating, my $lastgone, my $visitno,my  $useradd04,my  $useradd02, my $mymoney, my $postdel, my $sex, my $education, my $marry, my $work, my $born, my $chatlevel,my  $chattime, my $jhmp,my $jhcount,my $ebankdata,my $onlinetime,my $userquestion,my $awards,my $jifen,my $userface, my $soccerdata, my $useradd5) = split(/\t/,$filedata);
	    $userface = "";
            $lastgone = time;
	    if (($membername ne "")&&($password ne "")) {
	      seek(FILE6,0,0);
	      print FILE6 "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
	      close(FILE6);
	      if (open(FILE6,">${lbdir}$memdir/old/$nametocheck.cgi")) {
	          print FILE6 "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
	          close(FILE6);
	      }
	    } else {
                close(FILE6);
	    }
	    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	}
    $output .= qq~<script>document.cookie = "tempequip=" + "" +"; path=$cookiepath/";</script><meta http-equiv="refresh" content="0; url=$thisprog">~;
}


sub facehelp
{
    my $filetoopen = "$lbdir" . "face/face.dat";
    open (FILE, "$filetoopen");
    my @helpdata = <FILE>;
    close (FILE);

    $output .= qq~<table cellspacing=1 cellpadding=5 width=100% bgcolor=$tablebordercolor border=0 align="center">
<tr align=center bgcolor=$miscbackone><td><B>��ӭ��ʹ���װ�������̳����ϵͳ��</B></td></tr>
<tr bgcolor=$miscbacktwo><td valign=top>@helpdata</td></tr></table>~;
}

sub perset	# ��������
{
    if($allequip eq '')
    {
	$output .=qq~<font color=red size=3><b>�ǳ���Ǹ�����������������ݲ����ڣ��빺����Ӧ����Ʒ��</b></font>~;
	return;
    }
    my $setok = $query -> param('setok');

    if($setok ne "y")
    {
	$tempoutput = "<input type=radio name=loadface value=\"y\"> ����������Ϊ��̳ͷ��<input type=radio name=loadface value=\"n\"> ��̳��ͨ����(�鿴��������ʱ����ʾ)";
	$tempoutput =~ s/value=\"$loadface\"/value=\"$loadface\" checked/;

	$output .= qq~
	<table cellspacing=1 cellpadding=5 width=90% bgcolor=$tablebordercolor border=0 align="center">
	<form action="$thisprog" method="post" name="FORM">
	<input type=hidden name="action" value="perset">
	<input type=hidden name="setok" value="y">
	<tr align=middle bgcolor=$miscbackone><td colspan="2">ϵ ͳ Ĭ �� �� ��</td></tr>
	<tr align=left bgcolor=$forumcolortwo><td width=40%>��ͬװ�����������</td><td>$samnum ��</td></tr>
	<tr align=left bgcolor=$forumcolortwo><td>ϵͳ�����¼����</td><td>$lognum ��</td></tr>
	<tr align=middle bgcolor=$miscbackone><td colspan="2">�� �� �� ��</td></tr>
	<tr align=left bgcolor=$forumcolortwo><td>��������ʹ�÷�ʽ</td><td>$tempoutput</td></tr>
	<tr align=middle bgcolor=$forumcolortwo><td colspan="2">[<a href="face.cgi?action=cleanall" onclick="if (confirm('ȷ��Ҫ���������������������')) return ture; else return false; ">����ҵ�����������������</a>(������Ա�Ļ�������������ϣ��˲������ɻָ�)]</td></tr>
	<tr align=middle bgcolor=$miscbacktwo><td colspan="2"><input type=submit value="�� Ҫ �� ��"> <input type=reset value=�ء���></td></tr>
	</form>
	</table>~;
	return;
    }
    else
    {
	my $newloadface = $query -> param('loadface');
	$newloadface    = &cleanarea("$newloadface");

 	if($newloadface eq $loadface)
	{
	    $output .= qq~<meta http-equiv="refresh" content="0; url=$thisprog?action=perset">~;
	    return;
	}
 	&error("��������&��ѡ���Ƿ�Ҫ������������") if($newloadface eq "");

	&upplugdata("$tempmembername","$currequip|$allequip|$newloadface","");
	$tempmembername1 = $tempmembername;
	$tempmembername1 =~ s/ /\_/g;
	$tempmembername1 =~ tr/A-Z/a-z/;
        unlink ("${lbdir}cache/myinfo/$tempmembername1.pl");
        unlink ("${lbdir}cache/meminfo/$tempmembername1.pl");

	$output .= qq~<script>alert("�������ø��ĳɹ���");</script><meta http-equiv="refresh" content="0; url=$thisprog?action=perset">~;
	return;
    }
}

sub splist
{
    $output .= qq~
<SCRIPT language="javaScript" src="$imagesurl/face/js/search.js"></SCRIPT>
<SCRIPT language="javaScript" src="$imagesurl/face/js/catemenu.js" id='VIEW'></SCRIPT>
<body onmousemove="_HideMenu()">
<div id=_menuDiv style='Z-INDEX: 1; VISIBILITY: hidden; WIDTH: 1px; POSITION: absolute; HEIGHT: 1px; BACKGROUND-COLOR: $miscbackone'></div>
<table cellspacing=1 cellpadding=5 width=100% bgcolor=$tablebordercolor border=0>
<tr bgcolor=$miscbacktwo align=left><td><script>displayMenu();</script></td></tr>
<tr bgcolor=$miscbackone align=left><td align=center>
<div id=_Search>
<form name=SEARFORM action="javascript:Search()" method="post">
<select name="type_search" onchange=seletype()>
<option value="">ѡ����������
<option value="0">���۸�<option value="1">�������Ա�<option value="2">������</select>��
<span id=typeinfo><input type=text size=16 name="search_key"></span>��<input type=submit value="��ʼ����" onClick="return checksear();">
</div>
</td>
</form>
</tr>

<tr align=middle bgcolor=$forumcolortwo>
<td align=center valign=top>
<div id=DispInfo>��ҳ�����ʹ��JavaScript���룬��������ʱ�������⣬����������������ã�<BR><font color=red>�����ȡĳ��������ʾû����Ʒ�Ļ��������µ�һ�����Ϳ����ˡ�</font></div>
</td></tr>
<form action="javascript:Page_Jump()" method=POST name="Jump">
<tr bgcolor=$miscbacktwo><td align=center><font color=$menufontcolor>
<div id=DispPage>��ǰ�޼�¼</div>
</td></tr>
</form>
</table>
<script>
// ��Ȩ���У���Ԫ����
var SearchArray;	// ��������
var SaveArray;		// ����ԭ������
var SID;		// ��ǰ��Ʒ����

function killErrors()
{
  return true;
}
window.onerror = killErrors;

function DispSubMenu1(ID)
{
    SID = ID;
    VIEW.src = "$imagesurl/face/js/"+SID+".js";	// ��ȡ��Ӧ��Ʒ����JS�ļ�
}

function DispSubMenu(ID)
{
    SID = ID;
    SPNUM1 = SPNUM = 0;
    VIEW.src = "$imagesurl/face/js/"+SID+".js";	// ��ȡ��Ӧ��Ʒ����JS�ļ�
    if(SPNUM1 == SPNUM)
    {
	VIEW.src = "$imagesurl/face/js/"+SID+".js";	// �ڶ��ζ�ȡ
	alert("���ڵ�����Ӧ����Ʒ��Ϣ����ȷ������...");
	VIEW.src = "$imagesurl/face/js/"+SID+".js";	// �ڶ��ζ�ȡ
    }
    SPInfo(0);					// ��ʾ��Ӧ�����
    SearchArray = new Array();			// ��ʱ��������
    SaveArray   = SPINFO;			// ����ԭ��������
}

function Page_Jump()
{
     SPInfo(document.Jump.N_Page.value);
}

function SPInfo(Page)	// (ҳ��)
{
    var OutPage = "<table border=0 cellPadding=0 cellSpacing=0 width=100% align=center>";
    var ii = 0;

    var TempPnum = SPNUM / $show_pagen;
    var PageNum = Math.ceil(TempPnum);		// ���ҳ��

    if(Page > PageNum)
    {	alert("�����ҳ��������Ч��Χ��1 - "+PageNum+" ҳ��");return;}

    if((Page == '')||(Page < 1))
	Page = 1;

    if (!PageNum)
    	PageInfo = "��ǰû�м�¼";
    if (PageNum == 1)
    	PageInfo = "��ǰ��¼ֻ�� <B>1</B> ҳ";
    else
    {
	var jj;
	PageInfo = "�ܹ� <b>" + PageNum + "</b> ҳ��<b>"+SPNUM+"</b> ����Ʒ��[";
	jj = Page - 6;
	if(jj > 0)
	    PageInfo += " <span style='cursor:hand' onClick=SPInfo(" + jj + ") title='�� " + jj + " ҳ'>��</span>";
	jj++;

	for(t=0;t<5;t++)
	{
	    if(jj > 0)
		PageInfo += " <span style='cursor:hand' onClick=SPInfo(" + jj + ")>" + jj + "</span>";
	    jj++;
	}

	PageInfo += " <font color=#990000><B>" + jj + "</B></font>";
	jj++;
	if(jj <= PageNum)
	    PageInfo += " <span style='cursor:hand' onClick=SPInfo(" + jj + ")>" + jj + "</span>";
	jj++;

	for(t=0;t<5;t++)
	{
	    if(jj < PageNum)
	        PageInfo += " <span style='cursor:hand' onClick=SPInfo(" + jj + ")>" + jj + "</span>";
	    jj++;
 	}

	if(jj <= PageNum)
	    PageInfo += " <span style='cursor:hand' onClick=SPInfo(" + jj + ") title='�� " + jj + " ҳ'>��</span>";
	PageInfo += " ]";
    }

    for(j= SPNUM - Page * $show_pagen  + $show_pagen - 1; j >= SPNUM - Page * $show_pagen && j >= 0;j--)
    {
	var SP_Info = SPINFO[j].split('|');
	if(SP_Info[2] == '0')
	     SPMoney = '<font color=red>���</font>'
	else
	     SPMoney = SP_Info[2]

	if(SP_Info[3] == 'm')
	{    SPSEX = '��';}
	else if(SP_Info[3] == 'f')
	{    SPSEX = 'Ů';}
	else
	{    SPSEX = '��Ů';}

	if (ii==0)
	   OutPage = OutPage + "<tr>";

	OutPage += "<TD width=$c_width>";
	OutPage += "<TABLE border=0 cellPadding=2 cellSpacing=2 width=100%>";
	OutPage += "<TR>";
	OutPage += "<TD bgcolor=$forumcolorone height=84 rowSpan=4 width=84>";

	if(SID.charAt(0) == 't')
	    OutPage += "<img src=$imagesurl/face/"+AID+"/"+SP_Info[5]+".gif alt=����������Դ� width=84 height=84 border=0 onClick=javascript:CHECKEQ('"+AID+"','" + SP_Info[4] + "','" +SP_Info[3]+ "','$sex','"+MINFO[j]+"') style='cursor:hand'></TD>";
	else
	   OutPage += "<img src=$imagesurl/face/"+SID+"/"+SP_Info[5]+".gif alt=����������Դ� width=84 height=84 border=0 onClick=javascript:CHECK('"+SID+"','"+SP_Info[4]+"','"+SP_Info[3]+"','$sex') style='cursor:hand'></TD>";

	OutPage += "<TD bgColor=$forumcolorone>" + SP_Info[1] + "</TD></TR>";
	OutPage += "<TR><TD bgColor=$forumcolorone>�����ۣ�" + SPMoney + "</TD></TR>";
	OutPage += "<TR><TD bgColor=$forumcolorone>�ʡ��ã�" + SPSEX + "</TD></TR>";

	OutPage += "<TR><TD bgColor=$forumcolorone><a href=javascript:CHECK('"+SID+"','" + SP_Info[4] + "','" + SP_Info[3] + "','$sex')>�Դ�</a>��";
	OutPage += "<a href=javascript:Buy('" + SP_Info[1] +"',"+SID+",'" + SP_Info[0] + "',"+ SP_Info[2] + ")>����</a>";

	OutPage += "</TD></TR></TABLE>";
	OutPage += "</TD><TD width=10>&nbsp;</TD>";

	if (ii==($row_num-1))
	    OutPage += "</tr>";
	if (ii<($row_num-1))
	{ii++;} else {ii=0;}
    }

    OutPage = OutPage + "</tr></TABLE>";
    DispInfo.innerHTML = OutPage;
    DispPage.innerHTML = PageInfo + " ���� <input type='text' name='N_Page' size='3' maxlength='3'>  <input type=submit name=Submit value='ȷ��'>";
}
</script>~;
    return;
}


sub mybureau
{
    if($allequip eq '')
    {
	$output .=qq~<font color=red size=3><b>�����¹�û���κ���Ʒ��</b></font>~;
	return;
    }
    for($i=1;$i<26;$i++)
    {
	@tempsp=split(/\_/,@buy_sp[$i]);
	next if(@tempsp eq "");
	for($j=0;$j<@tempsp;$j++)
	{
	    ($info1,$info2)=split(/\,/,@tempsp[$j]);	# ��ƷID���Ƿ�װ��
###
	    $/="";
	    my $filetoopen = "$lbdir" . "face/wpdata/$i.pl";
	    open(FILE,"$filetoopen");
	    my $sort=<FILE>;
	    close(FILE);
	    $/="\n";
	    my $info3 = 1;
	    $info3 = 0 if($sort !~ /$info1\t(.*)/);	# �Ҳ���ָ������ƷID

	    my ($sp_name,$sp_money,$x,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$sp_suit,$sp_suitid)=split(/\t/,$1);
###
	    $ladesign = $info2 eq 'Y' ? 1 : 0 ;
	    $outinfo .=qq~'$sp_name|$info3|$sp_fitherd|$sp_graphic|$sp_sxgraphic||$j|$sp_money|',~;
	    $outinfo1 .=qq~'$ladesign',~;
	    $outinfo2 .=qq~'$i',~;
	    $outinfo3 .=qq~'$info1',~;
	}
    }

    chop($outinfo);
    chop($outinfo1);
    chop($outinfo2);
    chop($outinfo3);

    $output .=qq~
<script>
document.cookie = "tempequip=" + "$currequip" +"; path=$cookiepath/";
Fitting("$currequip",Show);

var AllArray = new Array($outinfo);
var LadeSign = new Array($outinfo1);
var SortArray = new Array($outinfo2);
var SPIDArray = new Array($outinfo3);

function Lade(ID)	
{
    var TEMP = AllArray[ID].split('|');	

    if (TEMP[1] == '0')
    {
	alert("����Ʒ�Ѿ������ڣ��붪����");
	return;
    }

    if ((TEMP[2] != '$sex') && (TEMP[2] != 't'))
    {
	alert("�Բ����Ա𲻷������޷��Դ���");
	return;
    }

    var SPGIF = TEMP[3].split('.gif');	

	for(i=0;i<AllArray.length;i++)	
	{
    	    var TEMPS = AllArray[i].split('|');
	    if((TEMPS[5] != '')||(SortArray[i] == SortArray[ID]))
	    {
		if(LadeSign[i] != 0)
		{
		    var TwoGIF = TEMPS[3].split('.gif');
			    LadeSign[i] = 0;
		    if(SPGIF[0] == TwoGIF[0])
		       CHECK(SortArray[i],TwoGIF[0],TEMPS[2],'$sex');
		}
 	    }
	}
        CHECK(SortArray[ID],SPGIF[0],TEMP[2],'$sex');

    LadeSign[ID] = 1;
    DispInfo(1);
    DispInfo(0);
}

function UnLade(ID)	
{
    var TEMP = AllArray[ID].split('|');	
    var SPGIF = TEMP[3].split('.gif');	
    CHECK(SortArray[ID],SPGIF[0],TEMP[2],'$sex');
    LadeSign[ID] = 0;
    DispInfo(0);
    DispInfo(1);
}

function SAVE()		
{
var exp = new Date();exp.setTime(exp.getTime() + 1*60*60*1000);
document.cookie = "_SortArray=" + SortArray + "; expires=" + exp.toGMTString() +"; path=$cookiepath/";
document.cookie = "_SPIDArray=" + SPIDArray + "; expires=" + exp.toGMTString() +"; path=$cookiepath/";
document.cookie = "_StateArray=" + LadeSign + "; expires=" + exp.toGMTString() +"; path=$cookiepath/";
var Win=window.open("buyface.cgi?action=save","BUY",'width=1,height=1,resizable=0,scrollbars=0,menubar=0,status=0');
}

function DELSP(Sort,NUM)
{
    if(!confirm("���Ƿ�ȷ�϶�����"))return false;
    var Win=window.open("buyface.cgi?action=delsp&class="+Sort+"&id="+NUM,"BUY",'width=10,height=10,resizable=0,scrollbars=0,menubar=0,status=0');
}

function DispInfo(Sign)
{
    var Info = "<table border=0 cellPadding=3 cellSpacing=0 width=84 bgcolor=$tablebordercolor align=left>";
    var jj=0;

    for(i=0;i<AllArray.length;i++)
    {
	if(Sign == LadeSign[i])
	{
	    var UTemp = AllArray[i].split('|');	

	    if(UTemp[2] == 'f')
		SPSEX = 'Ů'
	    else if(UTemp[2] == 'm')
	        SPSEX = '��'
	    else
	        SPSEX = 'ͨ��'

	    if(jj == 0)
	        Info += "<tr>";
	    Info += "<td width=84 bgColor=$miscbackone>";

	    if(Sign == 1)
		Info += "<img src=$imagesurl/face/"+SortArray[i]+"/"+UTemp[4]+" width=84 height=84 border=0 onClick=UnLade("+i+"); style='cursor:hand' title='��Ʒ���ƣ�"+UTemp[0]+"\\n�����Ա�"+SPSEX+"'></td>";
	    else
		Info += "<img src=$imagesurl/face/"+SortArray[i]+"/"+UTemp[4]+" width=84 height=84 border=0 onClick=Lade("+i+"); style='cursor:hand' title='��Ʒ���ƣ�"+UTemp[0]+"\\n�����Ա�"+SPSEX+"'><BR><BR>��<span onClick=buyface("+SortArray[i]+","+UTemp[6]+",'zeng'); style='cursor:hand'>����</span>��<span onClick=DELSP("+SortArray[i]+","+UTemp[6]+"); style='cursor:hand'>����</span></td>";


	    if(jj == 5)
	        Info += "</tr>";
	    if(jj < 5)
	        jj++;
	    else
	        jj = 0;
	}
    }
    k = 6 - jj;
    Info += "<td colspan="+k+" bgColor=$miscbackone></td></tr></table>";
    if(Sign == 1)
	LoadArea.innerHTML = Info;
    else
	ULoadArea.innerHTML = Info;
}
</script>

<table width=100% border=0 cellspacing=1 cellpadding=3 bgcolor=$tablebordercolor>
<tr><td bgcolor=$miscbacktwo height=20><font color=$titlefont size=2><B>��ǰ�����Ʒ</B> | <span onClick=SAVE(); style='cursor:hand'>���浱ǰ����</span></font></td></tr>
</table>
<table width=100% border=0 cellspacing=0 cellpadding=0>
<tr><td>
<div id=LoadArea><script>DispInfo(1);</script></div>
</td></tr>
</table>
<table width=100% border=0 cellspacing=1 cellpadding=3 bgcolor=$tablebordercolor>
<tr><td bgcolor=$miscbacktwo height=20><font color=$titlefont size=2><B>δ�����Ʒ</B></font></td></tr>
</table>
<table width=100% border=0 cellspacing=0 cellpadding=0>
<tr><td>
<div id=ULoadArea><script>DispInfo(0);</script></div>
</td></tr>
</table>~;
}

sub mylog
{
    my $logid = $query -> param('id');

    $output .= qq~
<table cellspacing=1 cellpadding=3 width=98% bgcolor=$tablebordercolor border=0 align=center>
<tr align=center><td colspan=6 bgcolor=$miscbacktwo><b><a href=$thisprog?action=mylog&id=1>�����¼</a> <a href=$thisprog?action=mylog&id=2>���ͼ�¼</a> <a href=$thisprog?action=mylog&id=3>������¼</a></b></td></tr></table>~;

    my $filetoopen = "$lbdir" . "face/log/$tempmembername.pl";
    return if (!( -e "$filetoopen")); # ���������

    open(FILE,"$filetoopen");
    my @mylog=<FILE>;
    close(FILE);

    $output .= qq~<table cellspacing=1 cellpadding=3 width=98% bgcolor=$tablebordercolor border=0 align=center>~;

    if($logid eq '1')
    {
	foreach (@mylog) 
	{
	    ($log_id,$sp_name,$sp_num,$sp_money,$log_time,$other_1,$other_2)=split(/\t/,$_);
	    if($log_id eq '1')	# ����ҵ���¼����
	    {
		$loghead = "�����¼";
		$logcon .= qq~<tr align=center bgcolor=$miscbackone><td>$log_time</td><td>$sp_name</td><td>$sp_num</td><td>$sp_money</td><td>&nbsp;</td><td>&nbsp;</td></tr>~;
	    }
	}
    }
    if($logid eq '2')
    {
	foreach (@mylog) 
	{
	    ($log_id,$sp_name,$sp_num,$sp_money,$log_time,$other_1,$other_2)=split(/\t/,$_);
	    if($log_id eq '2')	# ����ҵ���¼����
	    {
		$loghead = "���ͼ�¼";
		$zengname = "���͸�";
		$zengly = "��������";
		$logcon .= qq~<tr align=center bgcolor=$miscbackone><td>$log_time</td><td>$sp_name</td><td>$sp_num</td><td>$sp_money</td><td>$other_1</td><td>$other_2</td></tr>~;
	    }
	}
    }
    if($logid eq '3')
    {
	foreach (@mylog) 
	{
	    ($log_id,$sp_name,$sp_num,$sp_money,$log_time,$other_1,$other_2)=split(/\t/,$_);
	    if($log_id eq '3')	# ����ҵ���¼����
	    {
		$loghead = "������¼";
		$zengname = "������";
		$zengly = "����������";
		$logcon .= qq~<tr align=center bgcolor=$miscbackone><td>$log_time</td><td>$sp_name</td><td>$sp_num</td><td>$sp_money</td><td>$other_1</td><td>$other_2</td></tr>~;
	    }
	}
    }
    if($logid ne '')
    {
	$output .=qq~
	<tr align=center><td colspan=6 bgcolor=$miscbackone><font color=$titlefontcolor>$loghead</font></td></tr>
	<tr align=center bgcolor=$miscbacktwo><td>����ʱ��</td><td>$loghead��Ʒ</td><td>����</td><td>�۸�</td><td>$zengname</td><td>$zengly</td></tr>$logcon~;
    }
    $output .=qq~</table>~;
}

&output("$plugname",\$output);
