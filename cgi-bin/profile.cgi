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

#  $ENV{'TMP'}="$LBPATH/lock"; #����㲻���ϴ�ͼƬ����ȥ��ǰ���#
#  $ENV{'TEMP'}="$LBPATH/lock";#����㲻���ϴ�ͼƬ����ȥ��ǰ���#

use LBCGI;
$LBCGI::POST_MAX=1000000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/membertitles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "profile.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

&ipbanned; #��ɱһЩ ip

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}

$addme=$query->param('addme');

if ($arrowavaupload ne "on") { undef $addme; }

$action        = $query -> param('action');
$inmember      = $query -> param('member');
$inmember      =~ s/\///g;
$inmember      =~ s/\.\.//g;
$inmembername  = $query -> param("membername");
$inpassword    = $query -> param("password");
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$oldpassword   = $query -> param("oldpassword");
$action        = &cleaninput("$action");
$inmember      = &cleaninput("$inmember");
$inmembername  = &cleaninput("$inmembername");
$inpassword    = &cleaninput("$inpassword");
$oldpassword   = &cleaninput("$oldpassword");
$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if (($inmembername eq "")&&($action ne "lostpass")&&($action ne "lostpassword")&&($action ne "sendpassword")){
    $inmembername = "����";
    $userregistered = "no";
    if ($dispprofile eq "no") {
        print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("�鿴��Ա����&������Ȩ�鿴��Ա���ϣ�")
    }
} else {
    &getmember("$inmembername","no");
    &error("��ͨ����&�û� $inmembername �ڱ���̳�в����ڣ�") if (($userregistered eq "no")&&($action ne "lostpass")&&($action ne "lostpassword"));
    &error("��ͨ����&��̳�������û���������������µ�¼��") if ($inpassword ne $password && $action eq "show");
}
if ($arrawsignpic eq "on")      { $signpicstates = "����";}      else {$signpicstates = "��ֹ";}
if ($arrawsignflash eq "on")    { $signflashstates = "����";}    else {$signflashstates = "��ֹ";}
if ($arrawsignfontsize eq "on") { $signfontsizestates = "����";} else {$signfontsizestates = "��ֹ";}
if ($arrawsignsound eq "on")    { $signsoundstates = "����";}    else {$signsoundstates = "��ֹ";}

&mischeader("�û�����");

$output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=6 cellspacing=1 width=100%>
~;

my %Mode = (
'show'                 =>    \&showprofile,
'shows'                =>    \&showprofile,
'lostpassword'         =>    \&lostpasswordform,
'lostpass'             =>    \&lostpasswordform,
'sendpassword'         =>    \&sendpassword,
'modify'               =>    \&modify,
'process'              =>    \&savemodify,
);

if($Mode{$action}) {
    $Mode{$action}->();
} else {
    &error("�鿴����&������������ʱ�����");
}

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output($boardname,\$output);
exit;

sub lostpasswordform {
    require "dolostpasswordform.pl";
}

sub sendpassword {
    require "dosendpassword.pl";
}

sub savemodify {
    require "dosavemodify.pl";
}

sub modify {
    require "domodify.pl";
}

sub showprofile {
    $inmember =~ s/\_/ /isg;
    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        &whosonline("$inmembername\t��������\tboth\t�鿴<b>$inmember</b>�ĸ�������\t");
    }
    &getmember("$inmember","no");
    if ("$userregistered" eq "no") { &error("�鿴����&û�д��û�����"); }
    
    if ($jifen >= $mpostmarkmax) { $mtitle =  $mtitlemax;  $membergraphic = $mgraphicmax; }
    elsif ($jifen >= $mpostmark19) { $mtitle =  $mtitle19;  $membergraphic = $mgraphic19; }
    elsif ($jifen >= $mpostmark18) { $mtitle =  $mtitle18;  $membergraphic = $mgraphic18; }
    elsif ($jifen >= $mpostmark17) { $mtitle =  $mtitle17;  $membergraphic = $mgraphic17; }
    elsif ($jifen >= $mpostmark16) { $mtitle =  $mtitle16;  $membergraphic = $mgraphic16; }
    elsif ($jifen >= $mpostmark15) { $mtitle =  $mtitle15;  $membergraphic = $mgraphic15; }
    elsif ($jifen >= $mpostmark14) { $mtitle =  $mtitle14;  $membergraphic = $mgraphic14; }
    elsif ($jifen >= $mpostmark13) { $mtitle =  $mtitle13;  $membergraphic = $mgraphic13; }
    elsif ($jifen >= $mpostmark12) { $mtitle =  $mtitle12;  $membergraphic = $mgraphic12; }
    elsif ($jifen >= $mpostmark11) { $mtitle =  $mtitle11;  $membergraphic = $mgraphic11; }
    elsif ($jifen >= $mpostmark10) { $mtitle =  $mtitle10;  $membergraphic = $mgraphic10; }
    elsif ($jifen >= $mpostmark9)  { $mtitle =  $mtitle9;   $membergraphic = $mgraphic9; }
    elsif ($jifen >= $mpostmark8)  { $mtitle =  $mtitle8;   $membergraphic = $mgraphic8; }
    elsif ($jifen >= $mpostmark7)  { $mtitle =  $mtitle7;   $membergraphic = $mgraphic7; }
    elsif ($jifen >= $mpostmark6)  { $mtitle =  $mtitle6;   $membergraphic = $mgraphic6; }
    elsif ($jifen >= $mpostmark5)  { $mtitle =  $mtitle5;   $membergraphic = $mgraphic5; }
    elsif ($jifen >= $mpostmark4)  { $mtitle =  $mtitle4;   $membergraphic = $mgraphic4; }
    elsif ($jifen >= $mpostmark3)  { $mtitle =  $mtitle3;   $membergraphic = $mgraphic3; }
    elsif ($jifen >= $mpostmark2)  { $mtitle =  $mtitle2;   $membergraphic = $mgraphic2; }
    elsif ($jifen >= $mpostmark1)  { $mtitle =  $mtitle1;   $membergraphic = $mgraphic1; }
    else { $mtitle = $mtitle0; $mgraphic0 ="none.gif" if ($mgraphic0 eq ""); $membergraphic = $mgraphic0; }  #��ʾĬ�ϵȼ�

    $emailaddress = &encodeemail($emailaddress);
    if ($showemail eq "no") { $emailaddress = "����"; }
	elsif ($showemail eq "popo") { $emailaddress = qq~<img src=$imagesurl/images/popo.gif border=0 width=16 align=absmiddle> <a href=mailto:$emailaddress>$emailaddress</a>~; }
	elsif ($showemail eq "msn")  { $emailaddress = qq~<img src=$imagesurl/images/msn.gif border=0 width=16 align=absmiddle> <a href="mailto:$emailaddress">$emailaddress</a>~; }
	else { $emailaddress = qq~<a href="mailto:$emailaddress">$emailaddress</a>~; }

    if (($oicqnumber) && ($oicqnumber =~ /[0-9]/)) { $qqlogo = qq~<a href=http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$oicqnumber target=_blank><img src=$imagesurl/images/oicq.gif alt="�鿴 OICQ:$oicqnumber ������" atta="<img src=http://qqshow-user.tencent.com/$oicqnumber/10/00/>" border=0 width=16 height=16></a>~;} else { $oicqnumber = "û��"; $qqlogo ="";}
    if ($icqnumber eq "") { $icqnumber = "û��"; $icqlogo = ""; } else { $icqlogo = qq~<a href=misc.cgi?action=icq&UIN=$icqnumber target=_blank><img src=$imagesurl/images/icq.gif alt="�� ICQ:$icqnumber ������Ϣ" border=0 width=16 height=16></a>~; }
    if ((($membercode eq "ad")&&($membertitle eq "Member"))||(($membercode eq "ad")&&($membertitle eq "member")))   { $membertitle = "��̳̳��"; }
    if ((($membercode eq "mo")&&($membertitle eq "Member"))||(($membercode eq "mo")&&($membertitle eq "member")))   { $membertitle = "��̳����";}
    if ((($membercode eq "cmo")&&($membertitle eq "Member"))||(($membercode eq "cmo")&&($membertitle eq "member")))  { $membertitle = "����������";}
    if ((($membercode eq "smo")&&($membertitle eq "Member"))||(($membercode eq "smo")&&($membertitle eq "member"))) { $membertitle = "�ܰ���";}
    if ((($membercode eq "amo")&&($membertitle eq "Member"))||(($membercode eq "amo")&&($membertitle eq "member"))) { $membertitle = "��̳������";}

    $mtitle = $motitle  if (($membercode eq "mo")&&($motitle ne ""));
    $mtitle = $adtitle  if (($membercode eq "ad")&&($adtitle ne ""));
    $mtitle = $cmotitle if (($membercode eq "cmo")&&($cmotitle ne ""));
    $mtitle = $smotitle if (($membercode eq "smo")&&($smotitle ne ""));
    $mtitle = $amotitle if (($membercode eq "amo")&&($amotitle ne ""));

    if ($membercode eq "banned") { $membertitle = "��ֹ����"; }
    if ($membertitle eq "member" || $membertitle eq "Member" || $membertitle eq "") { $membertitle = "û��"; }
    if (($homepage eq "http://") || ($homepage eq "")) { $homepage = "û��"; } else { $homepage = qq~<a href="$homepage" target=_blank>$homepage</a>~; }

    $lastgone   = $joineddate if($lastgone eq "");
    $joineddate = &longdate($joineddate + ($timedifferencevalue*3600) + ($timezone*3600));
    $lastgone   = &dateformat($lastgone + ($timedifferencevalue*3600) + ($timezone*3600));

    ($postdate, $posturl, $posttopic) = split(/\%%%/,$lastpostdate);
    $posttopic =~ s/^����������//;

    if ($postdate ne "û�з����") {
        $postdate = &longdate($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
        $lastpostdetails = qq~<a href="$posturl">$posttopic</a> ($postdate)~;
    } else {
	$lastpostdetails = "û�з����";
    }
    
    if ($avatars eq "on") {
	if (($personalavatar)&&($personalwidth)&&($personalheight)) { #�Զ���ͷ�����
	    $personalavatar =~ s/\$imagesurl/${imagesurl}/o;
	    if (($personalavatar =~ /\.swf$/i)&&($flashavatar eq "yes")) {
	        $personalavatar=uri_escape($personalavatar);
		$useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>);
	    } else {
	        $personalavatar=uri_escape($personalavatar);
		$useravatar = qq(<br>&nbsp; <img src=$personalavatar border=0 width=$personalwidth height=$personalheight>);
	    }
	}
        elsif (($useravatar ne "noavatar") && ($useravatar)) {
            $useravatar=uri_escape($useravatar);
	    $useravatar = qq(<br>&nbsp; <img src="$imagesurl/avatars/$useravatar.gif" border=0 $defaultwidth $defaultheight>);
        }
        else {$useravatar="û��"; }
    }
    
    $xnuseravatar = "û��";
    if ($userface ne '') {
        my ($currequip,$x,$loadface)=split(/\|/,$userface);
        $xnuseravatar = qq~<SCRIPT>Face_Info("$currequip","$imagesurl");</SCRIPT>~;
    }

    $interests = "û��" if ($interests eq "");
    $location  = "û��" if ($location eq "");

    if ($signaturehtml) {$signature = $signaturehtml ;} 
        elsif ($signatureorigin)  { if ($idmbcodestate eq 'on') { require "dosignlbcode.pl"; $signature = &signlbcode($signatureorigin); } $signature =~ s/\n/\<BR\>/isg;} 
	else {$signature = "û��";}

    if ($sex eq "f") {
	$sex = "��Ů <img src=$imagesurl/images/fem.gif width=20 alt=��Ů align=absmiddle>";
    }
    elsif ($sex eq "m") {
	$sex = "˧�� <img src=$imagesurl/images/mal.gif width=20 alt=˧�� align=absmiddle>";
    }
    else { $sex = "����"; }

    $numberofreplys = 0 if ($numberofreplys eq "");
    $postdel   = 0 if ($postdel eq "");
    $jhmp    = "��������" if ($jhmp eq "");
    if ($rating !~ /^[0-9\-]+$/) {$rating = 0;}
    if ($rating eq "") {$rating =0;}
    $mymoney   = 0 if ($mymoney eq "");
    $education = "δ����" if ($education eq "");
    $marry     = "δ����" if ($marry eq "");
    $work      = "δ����" if ($work eq "");
    $born      = "δ����" if (($born eq "")||($born eq "//"));
    $userflag  = "blank" if ($userflag eq "");

$blank="δ����";
$China="�й�";
$Angola="������";
$Antigua="�����";
$Argentina="����͢";
$Armenia="��������";
$Australia="�Ĵ�����";
$Austria="�µ���";
$Bahamas="�͹���";
$Bahrain="����";
$Bangladesh="�ϼ���";
$Barbados="�ͰͶ�˹";
$Belgium="����ʱ";
$Bermuda="��Ľ��";
$Bolivia="����ά��";
$Brazil="����";
$Brunei="����";
$Canada="���ô�";
$Chile="����";
$Colombia="���ױ���";
$Croatia="���޵���";
$Cuba="�Ű�";
$Cyprus="����·˹";
$Czech_Republic="�ݿ�";
$Denmark="����";
$Dominican_Republic="�������";
$Ecuador="��϶��";
$Egypt="����";
$Estonia="��ɳ����";
$Finland="����";
$France="����";
$Germany="�¹�";
$Great_Britain="Ӣ��";
$Greece="ϣ��";
$Guatemala="Σ������";
$Honduras="�鶼��˹";
$Hungary="������";
$Iceland="����";
$India="ӡ��";
$Indonesia="ӡ��������";
$Iran="����";
$Iraq="������";
$Ireland="������";
$Israel="��ɫ��";
$Italy="�����";
$Jamaica="�����";
$Japan="�ձ�";
$Jordan="Լ��";
$Kazakstan="������";
$Kenya="������";
$Kuwait="������";
$Latvia="����ά��";
$Lebanon="�����";
$Lithuania="������";
$Malaysia="��������";
$Malawi="����ά";
$Malta="�����";
$Mauritius="ë����˹";
$Morocco="Ħ���";
$Mozambique="Īɣ�ȿ�";
$Netherlands="����";
$New_Zealand="������";
$Nicaragua="�������";
$Nigeria="��������";
$Norway="Ų��";
$Pakistan="�ͻ�˹̹";
$Panama="������";
$Paraguay="������";
$Peru="��³";
$Poland="����";
$Portugal="������";
$Romania="��������";
$Russia="����˹";
$Saudi_Arabia="ɳ�ذ�����";
$Singapore="�¼���";
$Slovakia="˹�工��";
$Slovenia="˹��������";
$Solomon_Islands="������";
$Somalia="������";
$South_Africa="�Ϸ�";
$South_Korea="����";
$Spain="������";
$Sri_Lanka="ӡ��";
$Surinam="������";
$Sweden="���";
$Switzerland="��ʿ";
$Thailand="̩��";
$Trinidad_Tobago="��͸�";
$Turkey="������";
$Ukraine="�ڿ���";
$United_Arab_Emirates="����������������";
$United_States="����";
$Uruguay="������";
$Venezuela="ί������";
$Yugoslavia="��˹����";
$Zambia="�ޱ���";
$Zimbabwe="��Ͳ�Τ";
$blank="δ����";

    $usersx    = "blank" if ($usersx eq "");
    if ($usersx eq "sx1")     {$showsx = "���� <IMG src=$imagesurl/sx/sx1s.gif  alt=���� align=absmiddle>";}
    elsif ($usersx eq "sx2")  {$showsx = "��ţ <IMG src=$imagesurl/sx/sx2s.gif  alt=��ţ align=absmiddle>";}
    elsif ($usersx eq "sx3")  {$showsx = "���� <IMG src=$imagesurl/sx/sx3s.gif  alt=���� align=absmiddle>";}
    elsif ($usersx eq "sx4")  {$showsx = "î�� <IMG src=$imagesurl/sx/sx4s.gif  alt=î�� align=absmiddle>";}
    elsif ($usersx eq "sx5")  {$showsx = "���� <IMG src=$imagesurl/sx/sx5s.gif  alt=���� align=absmiddle>";}
    elsif ($usersx eq "sx6")  {$showsx = "���� <IMG src=$imagesurl/sx/sx6s.gif  alt=���� align=absmiddle>";}
    elsif ($usersx eq "sx7")  {$showsx = "���� <IMG src=$imagesurl/sx/sx7s.gif  alt=���� align=absmiddle>";}
    elsif ($usersx eq "sx8")  {$showsx = "δ�� <IMG src=$imagesurl/sx/sx8s.gif  alt=δ�� align=absmiddle>";}
    elsif ($usersx eq "sx9")  {$showsx = "��� <IMG src=$imagesurl/sx/sx9s.gif  alt=��� align=absmiddle>";}
    elsif ($usersx eq "sx10") {$showsx = "�ϼ� <IMG src=$imagesurl/sx/sx10s.gif alt=�ϼ� align=absmiddle>";}
    elsif ($usersx eq "sx11") {$showsx = "�繷 <IMG src=$imagesurl/sx/sx11s.gif alt=�繷 align=absmiddle>";}
    elsif ($usersx eq "sx12") {$showsx = "���� <IMG src=$imagesurl/sx/sx12s.gif alt=���� align=absmiddle>";}
    else {$showsx = "δ����";}

    $userxz    = "blank" if ($userxz eq "");
    if ($userxz eq "z1")     {$showxz = "���� <IMG height=15 src=$imagesurl/star/z1.gif  width=15 alt=������ align=absmiddle>";}
    elsif ($userxz eq "z2")  {$showxz = "��ţ <IMG height=15 src=$imagesurl/star/z2.gif  width=15 alt=��ţ�� align=absmiddle>";}
    elsif ($userxz eq "z3")  {$showxz = "˫�� <IMG height=15 src=$imagesurl/star/z3.gif  width=15 alt=˫���� align=absmiddle>";}
    elsif ($userxz eq "z4")  {$showxz = "��з <IMG height=15 src=$imagesurl/star/z4.gif  width=15 alt=��з�� align=absmiddle>";}
    elsif ($userxz eq "z5")  {$showxz = "ʨ�� <IMG height=15 src=$imagesurl/star/z5.gif  width=15 alt=ʨ���� align=absmiddle>";}
    elsif ($userxz eq "z6")  {$showxz = "��Ů <IMG height=15 src=$imagesurl/star/z6.gif  width=15 alt=��Ů�� align=absmiddle>";}
    elsif ($userxz eq "z7")  {$showxz = "��� <IMG height=15 src=$imagesurl/star/z7.gif  width=15 alt=����� align=absmiddle>";}
    elsif ($userxz eq "z8")  {$showxz = "��Ы <IMG height=15 src=$imagesurl/star/z8.gif  width=15 alt=��Ы�� align=absmiddle>";}
    elsif ($userxz eq "z9")  {$showxz = "���� <IMG height=15 src=$imagesurl/star/z9.gif  width=15 alt=������ align=absmiddle>";}
    elsif ($userxz eq "z10") {$showxz = "ħ�� <IMG height=15 src=$imagesurl/star/z10.gif width=15 alt=ħ���� align=absmiddle>";}
    elsif ($userxz eq "z11") {$showxz = "ˮƿ <IMG height=15 src=$imagesurl/star/z11.gif width=15 alt=ˮƿ�� align=absmiddle>";}
    elsif ($userxz eq "z12") {$showxz = "˫�� <IMG height=15 src=$imagesurl/star/z12.gif width=15 alt=˫���� align=absmiddle>";}
    else {$showxz = "δ����";}

    $mymoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
    $moneyname ="�װ�Ԫ" if ($moneyname eq "");

    my $onlinetimehour = int($onlinetime/3600);
    my $onlinetimemin  = int(($onlinetime%3600)/60);
    my $onlinetimesec  = int(($onlinetime%3600)%60);
    $onlinetimehour = "0$onlinetimehour" if ($onlinetimehour <10);
    $onlinetimemin  = "0$onlinetimemin"  if ($onlinetimemin <10);
    $onlinetimesec  = "0$onlinetimesec"  if ($onlinetimesec <10);
    
    
    if (-e "${lbdir}soccer.cgi")
    {
    	my ($mywin, $mydraw, $mylose, $myplay, $myget) = split(/:/, $soccerdata);
    	$mywin = 0 if ($mywin eq "");
    	$mydraw = 0 if ($mydraw eq "");
    	$mylose = 0 if ($mylose eq "");
    	$myplay = 0 if ($myplay eq "");
    	$myget = 0  if ($myget eq "");
    	my $soccerwinrate = 0;
	$soccerwinrate = sprintf("%.2f", $mywin * 100 / ($mywin + $mydraw + $mylose)) if (($mywin + $mydraw + $mylose) > 0);
	$soccerinfo = qq~  <tr>
    <td valign=middle colSpan=5><font color=$fontcolormisc>����ս���� ʤ: <b><i>$mywin</i></b>����ƽ: <b><i>$mydraw</i></b>������: <b><i>$mylose</i></b>����ʤ��: <b><i>$soccerwinrate</i></b>%����������ʷͶע: <b><i>$myplay</i></b> $moneyname������ʷ����: <b><i>$myget</i></b> $moneyname</font></td>
  </tr>~ if (($mywin + $mydraw + $mylose) > 0);
     }

    my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $bankadd1, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
    if ($mystatus) {
	$mysaves .= " $moneyname";
	if ($myloan) {
	    $myloan .= " $moneyname";
	} else {
	    $myloan = "û����";
	}
    } else {
	$mysaves = "û����";
	$myloan = "û����";
    }
    
    $inmember = uri_escape($inmember);
    
    $jhcount = 0 if ($jhcount <0);

    $onlinetimehour = int($onlinetime/3600);
    $onlinetimemin  = int(($onlinetime%3600)/60);
    $onlinetimesec  = int(($onlinetime%3600)%60);
    $onlinetimehour = "0$onlinetimehour" if ($onlinetimehour <10);
    $onlinetimemin  = "0$onlinetimemin"  if ($onlinetimemin <10);
    $onlinetimesec  = "0$onlinetimesec"  if ($onlinetimesec <10);
    if ($onlinetimehour >= 1000) { my $onlinetime1 = $onlinetimehour; $onlinetime = int($onlinetime1/24); $onlinetime1 = $onlinetime1 - $onlinetime * 24; $onlinetime = "$onlinetime��$onlinetime1ʱ$onlinetimemin��$onlinetimesec��"; }
                                         else { $onlinetime = "$onlinetimehour ʱ $onlinetimemin �� $onlinetimesec ��"; }

    if (-e "${lbdir}pet.cgi") {

  eval{ require "${lbdir}petdata/config.pl"; } if ($pet_open eq "");
  if ($pet_open eq 'open') {
    if(-e"${lbdir}petdata/pet/$membername.cgi") {
	open(file,"${lbdir}petdata/pet/$membername.cgi");
	my $file=<file>;
	close(file);

	my $pet_zt;
	my $pet_style;
	my ($pet_name,$pet_jb,$x,$pet_sx,$pet_born,$pet_win,$pet_lose,$pet_gjl,$pet_fyl,$pet_exp,$pet_hp,$pet_sp,$x,$x,$x,$x,$x,$x,$x,$x,$pet_die,$x,$x,$pet_xz_time)=split(/\t/,$file);
	$pet_xz_time or $pet_xz_time = $pet_born;
	$pet_born=int((time-$pet_born)/86400)+1;
	if(time - $pet_xz_time > 86400*3) {$pet_xz_time="���������ģ������ϴ���";} else {$pet_xz_time='�����������ϴ����';}
	if ($pet_sp<0) {$pet_zt.='(�Һþ�û�Զ�����)';} elsif ($pet_sp<500) {$pet_zt.='(�ҿ������)';} elsif ($pet_sp<1000) {$pet_zt.='(�Һö���)';} elsif ($pet_sp<2000) {$pet_zt.='(�Һ���Զ���)';} else {$pet_zt.='(�Һñ�Ŷ)';}

	my $pet_exp1 = int(sqrt($pet_exp)/6);
	$pet_exp1 = 110 if ($pet_exp1 > 110);
	$pet_exp1 = qq~<img src=$imagesurl/images/jy_left.gif width=2 height=8><img src=$imagesurl/images/jy_0.gif width=$pet_exp1 height=8 alt="����: $pet_exp"><img src=$imagesurl/images/jy_right.gif width=4 height=8>~;

	my $pet_hp1 = int(sqrt($pet_hp));
	$pet_hp1 = 110 if ($pet_hp1 > 110);
	$pet_hp1 = qq~<img src=$imagesurl/images/vi_left.gif width=2 height=8><img src=$imagesurl/images/vi_0.gif width=$pet_hp1 height=8 alt="����: $pet_hp"><img src=$imagesurl/images/vi_right.gif width=4 height=8>~;

	my $pet_sp1 = int(sqrt($pet_sp)/6);
	$pet_sp1 = 110 if ($pet_sp1 > 110);
	$pet_sp1 = qq~<img src=$imagesurl/images/jy_left.gif width=2 height=8><img src=$imagesurl/images/jy_0.gif width=$pet_sp1 height=8 alt="ʳ��: $pet_sp"><img src=$imagesurl/images/jy_right.gif width=4 height=8>~;

	$pet_jb1=$pet_jb;
	$pet_jb=int($pet_jb/10);

	if($pet_die eq 'die'){$pet_name.='(�Ѿ�����)'; $pet_zt=''; $pet_xz_time='�Ѿ�����...'; $pet_style = qq~ style="filter:xray"~; }
	my $tempmembername = uri_escape($inmembername);
	$petinfo=qq~<tr><td bgcolor=$miscbacktwo valign=middle><font color=$fontcolormisc><b>�������ϣ�</b></font></td><td bgcolor=$miscbacktwo valign=middle><table border="1" width="320" style="border-collapse: collapse" bordercolor="$tablebordercolor" cellPadding=2 cellSpacing=0><tr><td colspan="2" height="23" bgcolor="$miscbacktwo">&nbsp;<img src=$imagesurl/pet_maiweb/cw.gif> �ǳƣ� <a href=pet.cgi?action=myspet&petname=$tempmembername target=_blank><b>$pet_name</b></a> $pet_zt�������䣺 $pet_born ��</td></tr><tr><td width="110" align=center $pet_style><img src=$imagesurl/pet_maiweb/pet/$pet_sx/$pet_sx$pet_jb.gif border=0></td><td width="*">&nbsp;ʤ�� $pet_win �� / ʧ�� $pet_lose ��<br>&nbsp;������ $pet_gjl �� / ������ $pet_fyl ��<br>&nbsp;���飺 $pet_exp1<br>&nbsp;������ $pet_hp1<br>&nbsp;ʳ� $pet_sp1<BR>&nbsp;״̬�� $pet_xz_time</td></tr></table></td></tr>~;
    } else { $petinfo='';}
} else { $petinfo='';}

}  else { $petinfo='';}

    $output .= qq~

	    <tr>
	    <td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center><font color=$fontcolormisc>"<b><font color=$fonthighlight>$membername</b></font>" �ĸ�������</td></tr>
  <tr>
    <td bgcolor=$miscbackone valign=middle width=150 align=center>$xnuseravatar</td>
    <td bgcolor=$miscbackone valign=middle>
<table width="100%" border="0" cellspacing="0" cellpadding="4">
  <tr bgcolor=$miscbacktwo>
    <td valign=middle><font color=$fontcolormisc>�û�����</font></td>
    <td valign=middle><font color=$fontcolormisc>$membername</font></td>
    <td valign=middle><font color=$fontcolormisc>�Ա�</font></td>
    <td valign=middle><font color=$fontcolormisc>$sex</font></td>
    <td valign=middle><font color=$fontcolormisc>ע��ʱ�䣺</font></td>
    <td valign=middle><font color=$fontcolormisc>$joineddate</font></td>
  </tr>
  <tr>
    <td valign=middle><font color=$fontcolormisc>�������£�</font></td>
    <td valign=middle><font color=$fontcolormisc>$born</font></td>
    <td valign=middle><font color=$fontcolormisc>��Ф��</font></td>
    <td valign=middle><font color=$fontcolormisc>$showsx</font></td>
    <td valign=middle><font color=$fontcolormisc>������</font></td>
    <td valign=middle><font color=$fontcolormisc>$showxz</font></td>
  </tr>
  <tr bgcolor=$miscbacktwo>
    <td valign=middle><font color=$fontcolormisc>����״����</font></td>
    <td valign=middle><font color=$fontcolormisc>$marry</font></td>
    <td valign=middle><font color=$fontcolormisc>ѧ����</font></td>
    <td valign=middle><font color=$fontcolormisc>$education</font></td>
    <td valign=middle><font color=$fontcolormisc>ְҵ��</font></td>
    <td valign=middle><font color=$fontcolormisc>$work</font></td>
  </tr>
  <tr>
    <td valign=middle><font color=$fontcolormisc>������</font></td>
    <td valign=middle><font color=$fontcolormisc>$rating</font></td>
    <td valign=middle><font color=$fontcolormisc>���֣�</font></td>
    <td valign=middle><font color=$fontcolormisc>$jifen</font></td>
    <td valign=middle><font color=$fontcolormisc>������;</font></td>
    <td valign=middle><font color=$fontcolormisc>$jhcount ƪ</font></td>
  </tr>
  <tr bgcolor=$miscbacktwo>
    <td valign=middle><font color=$fontcolormisc>��ǰ����</font></td>
    <td valign=middle><font color=$fontcolormisc><a href="lookinfo.cgi?action=style" target="_blank">$mtitle</a></font></td>
    <td valign=middle><font color=$fontcolormisc>��ǰͷ�Σ�</font></td>
    <td valign=middle><font color=$fontcolormisc>$membertitle</font></td>
    <td valign=middle><font color=$fontcolormisc>�������ɣ�</font></td>
    <td valign=middle><font color=$fontcolormisc>$jhmp</font></td>
  </tr>
  <tr>
    <td valign=middle><font color=$fontcolormisc>�ܹ�����</font></td>
    <td valign=middle><font color=$fontcolormisc>$numberofposts ƪ</font></td>
    <td valign=middle><font color=$fontcolormisc>�ܹ��ظ���</font></td>
    <td valign=middle><font color=$fontcolormisc>$numberofreplys ƪ</font></td>
    <td valign=middle><font color=$fontcolormisc>��ɾ����</font></td>
    <td valign=middle><font color=$fontcolormisc>$postdel ƪ</font></td>
  </tr>
  <tr bgcolor=$miscbacktwo>
    <td valign=middle><font color=$fontcolormisc>�ʼ���ַ��</font></td>
    <td valign=middle><font color=$fontcolormisc>$emailaddress</font></td>
    <td valign=middle><font color=$fontcolormisc>QQ ���룺</font></td>
    <td valign=middle><font color=$fontcolormisc>$qqlogo $oicqnumber</font></td>
    <td valign=middle><font color=$fontcolormisc>ICQ ���룺</font></td>
    <td valign=middle><font color=$fontcolormisc>$icqlogo $icqnumber</font></td>
  </tr>
  <tr>
    <td valign=middle><font color=$fontcolormisc>���ң�</font></td>
    <td valign=middle><font color=$fontcolormisc>$$userflag <img src=$imagesurl/flags/$userflag.gif alt="$$userflag" width=21 height=14></font></td>
    <td valign=middle><font color=$fontcolormisc>���ԣ�</font></td>
    <td valign=middle><font color=$fontcolormisc>$location</font></td>
    <td valign=middle><font color=$fontcolormisc>��ҳ��ַ��</font></td>
    <td valign=middle><font color=$fontcolormisc>$homepage</font></td>
  </tr>
  <tr bgcolor=$miscbacktwo>
    <td valign=middle><font color=$fontcolormisc>�ֽ�</font></td>
    <td valign=middle><font color=$fontcolormisc>$mymoney $moneyname</font></td>
    <td valign=middle><font color=$fontcolormisc>��</font></td>
    <td valign=middle><font color=$fontcolormisc>$mysaves</font></td>
    <td valign=middle><font color=$fontcolormisc>���</font></td>
    <td valign=middle><font color=$fontcolormisc>$myloan</font></td>
  </tr>
  <tr>
    <td valign=middle><font color=$fontcolormisc>����ʱ�䣺</font></td>
    <td valign=middle><font color=$fontcolormisc>$onlinetime</font></td>
    <td valign=middle><font color=$fontcolormisc>���ʴ�����</font></td>
    <td valign=middle><font color=$fontcolormisc>$visitno ��</font></td>
    <td valign=middle><font color=$fontcolormisc>�����ʣ�</font></td>
    <td valign=middle><font color=$fontcolormisc>$lastgone</font></td>
  </tr>
$soccerinfo
  <tr bgcolor=$miscbacktwo align=center>
    <td valign=middle colspan=2><span onClick="openScript('friendlist.cgi?action=adduser&adduser=$inmember', 420, 320)" style="cursor: hand">��$membername��Ϊ�ҵĺ���</span></td>
    <td valign=middle colspan=2><span onClick="openScript('messanger.cgi?action=new&touser=$inmember&actionto=msg', 600, 400)" style="cursor: hand">����һ������Ϣ��$membername</span></td>
    <td valign=middle colspan=2><a href=search.cgi?action=startsearch&TYPE_OF_SEARCH=username_search&NAME_SEARCH=topictitle_search&FORUMS_TO_SEARCH=all&SEARCH_STRING=$inmember target=_blank>����$membername�������������</a></td>
  </tr>
</table>
</td>
  </tr>
	    <tr>
	    <td bgcolor=$miscbacktwo valign=middle><font color=$fontcolormisc><b>��󷢱�</b></font></td>
	    <td bgcolor=$miscbacktwo valign=middle><font color=$fontcolormisc>$lastpostdetails</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>���Ҽ�飺</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>$interests</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbacktwo valign=middle><font color=$fontcolormisc><b>ǩ����</b></font></td>
	    <td bgcolor=$miscbacktwo valign=middle><font color=$fontcolormisc>$signature</font></td></tr>
	    <tr>
	    <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>����ͼƬ��</b></font></td>
	    <td bgcolor=$miscbackone valign=middle><br>$useravatar</td></tr>
		$petinfo
	    </table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR>
	    ~;
}
