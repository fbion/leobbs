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
use VISITFORUM qw(getlastvisit setlastvisit);
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/mpic.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "dispclick.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}

$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic !~ /^[0-9]+$/)||($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$instart        = $query -> param('start');
$instart	= 0 if ($instart eq "");

$inmembername   = $query->cookie("amembernamecookie");
$inpassword     = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&ipbanned; #��ɱһЩ ip

$currenttime = time;

if ((!$inmembername) or ($inmembername eq "����")) { $inmembername = "����"; $myrating= "-1"; $mymembercode="no"; &error("��ͨ����&���˲��ܲ鿴!");}
else {
    &getmember("$inmembername","no");
    $mymembercode=$membercode;
    $myrating=$rating;
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
    &error("��ͨ����&�û�û�е�¼��ע�ᣡ") if ($userregistered eq "no");
}

&getoneforum("$inforum");
$myinmembmod = $inmembmod;

if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($inmembmod eq "yes")||($membercode eq 'smo')) { $allowed = "yes"; } else { $allowed  = "no"; }

$addtimes = ($timedifferencevalue + $timezone)*3600;
$myrating = -6 if ($myrating eq "");
&error("������̳&�����̳��û��Ȩ�޽�����̳��") if ($yxz ne '' && $yxz!~/,$membercode,/);
if ($allowusers ne ''){
    &error('������̳&�㲻����������̳��') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}

if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &error("��ͨ����&����Ȩ�鿴��");
}

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

print header(-expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

    my $filetoopen = "${lbdir}forum$inforum/$intopic.pl";
    open(FILE, "$filetoopen");
    my $topicinfo = <FILE>;
    close(FILE);
    chomp $topicinfo;
    $topicinfo =~ s/[\a\f\n\e\0\r]//isg;
    ($topicid, $topictitle, $topicdescription) = split (/\t/,$topicinfo);
$topictitletemp = $topictitle;
$topictitletemp =~ s/^����������//;
$topictitletemp =~s/ \(������\)$//;
$topictitletemp =~s/\&\#039\;//isg;
$topictitletemp = &cleaninput($topictitletemp);

if (open(FILE, "${lbdir}forum$inforum/$intopic.clk.pl")) {
    sysread(FILE, my $threads,(stat(FILE))[7]);
    close(FILE);
    $threads =~ s/\r//isg;
    @threads = split(/\n/, $threads);
    @threads = reverse(@threads);
    $numberofitems = @threads;
}

my $tempnumberofpages = $numberofitems / $maxtopics;
$numberofpages = int($tempnumberofpages);
$numberofpages++ if ($numberofpages != $tempnumberofpages);

if ($numberofpages > 1) {
	$startarray = $instart;
	$endarray = $instart + $maxtopics - 1;
	$endarray = $numberofitems - 1 if ($endarray >= $numberofitems);

	if ($replynum eq "last" && $treeview ne "yes") {
		$instart = ($numberofpages - 1) * $maxtopics;
		$startarray = $instart;
		$endarray = $numberofitems - 1;
	}

	my $currentpage = int($instart / $maxtopics) + 1;
	my $endstart = ($numberofpages - 1) * $maxtopics;
	my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=0 title="�� ҳ" ><font face=webdings>9</font></a>~;
	my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$endstart title="β ҳ" ><font face=webdings>:</font></a>~;

	my $uppage = $currentpage - 1;
	my $nextpage = $currentpage + 1;
	my $upstart = $instart - $maxtopics;
	my $nextstart = $instart + $maxtopics;
	my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$upstart title="��$uppageҳ"><font face=webdings>7</font></a>~;
	my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$nextstart title="��$nextpageҳ"><font face=webdings>8</font></a>~;

	my $tempstep = $currentpage / 7;
	my $currentstep = int($tempstep);
	$currentstep++ if ($currentstep != $tempstep);
	my $upsteppage = ($currentstep - 1) * 7;
	my $nextsteppage = $currentstep * 7 + 1;
	my $upstepstart = ($upsteppage - 1) * $maxtopics;
	my $nextstepstart = ($nextsteppage - 1) * $maxtopics;
	my $showupstep = $upsteppage < 1 ? "" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$upstepstart class=hb title="��$upsteppageҳ">��</a> ~;
	my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$nextstepstart class=hb title="��$nextsteppageҳ">��</a> ~;

	$pages = "";
	my $currentstart = $upstepstart + $maxtopics;
	for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++)
	{
		last if ($i > $numberofpages);
		$pages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$currentstart class=hb>$i</a> ~;
		$currentstart += $maxtopics;
	}
	$pages = "<font color=$menufontcolor><b>�� <font color=$fonthighlight>$numberofpages</font> ҳ</b> $beginpage $showup \[ $showupstep$pages$shownextstep\] $shownext $endpage</font><br>";
}
else {
	$startarray = 0;
	$endarray = $numberofitems - 1;
	$pages = "<font color=$menufontcolor>ֻ��һҳ</font><br>";
}

&title;

$output .= qq~<br>~;
if (-e "${lbdir}cache/forumstopic$inforum.pl") {
  eval{ require "${lbdir}cache/forumstopic$inforum.pl";};
  if ($@) { unlink ("${lbdir}cache/forumstopic$inforum.pl"); require "dotopic.pl"; }
} else { require "dotopic.pl"; }

my $topictitletempshow = &lbhz($topictitletemp,34);
$tempoutput =~ s/topictitletempshow/$topictitletempshow �ķ��ʼ�¼/isg;
$tempoutput =~ s/jhimage/$jhimage/isg;

$output .= $tempoutput;

$output .= qq~<BR>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr bgcolor=$titlecolor>
<td width=33% align=center $catbackpic><font face="$font" color=$titlefontcolor><b>�� �� ��</b></td>
<td width=33% align=center $catbackpic><font face="$font" color=$titlefontcolor><b>�� �� �ɣ�</b></td>
<td width=33% align=center $catbackpic><font face="$font" color=$titlefontcolor><b>�� �� ʱ ��</b></td>
</tr>
~;
$addtimes = ($timedifferencevalue + $timezone)*3600;

foreach (@threads[$startarray .. $endarray]) {
  chomp $_;
#    next if ($_ eq "");
    ($recordmembername, $recordipaddress, $recordtrueipaddress, $recordtime) = split(/\t/,$_);
#    next if ($membername eq "");

    if ($recordipaddress eq $recordtrueipaddress) { $recordipaddress = ""; } else { $recordipaddress = qq~<BR><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$recordipaddress',420,320)" title="LB WHOIS��Ϣ">$recordipaddress</span>~; }
    
    ($ip1,$ip2,$ip3,$ip4) = split(/\./,$recordtrueipaddress);

    if ($mymembercode eq "ad") {
	$recordtrueipaddress=qq~<span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$recordtrueipaddress',420,320)" title="LB WHOIS��Ϣ">$recordtrueipaddress</span>$recordipaddress~;
    }
    elsif ($mymembercode eq "smo") {
	if ($smocanseeip eq "no") { $recordtrueipaddress=qq~<span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$recordtrueipaddress',420,320)" title="LB WHOIS��Ϣ">$recordtrueipaddress</span>$recordipaddress~; }
	else {
       	    if ($pvtip eq "on") { $recordtrueipaddress=qq~<span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$recordtrueipaddress',420,320)" title="LB WHOIS��Ϣ">$recordtrueipaddress</a>$recordipaddress~; }
       	    else { $recordtrueipaddress="�����ñ���"; }
	}
    }
    elsif ($myinmembmod eq "yes") {
	if ($pvtip eq "on") { $recordtrueipaddress="$ip1.$ip2.$ip3.*"; } else { $recordtrueipaddress="�����ñ���"; }
    }

         if ($lastcolor eq $postcolortwo) {
             $color = $postcolorone;
             $fontcolor = $postfontcolorone; }
         else {
             $color = $postcolortwo;
             $fontcolor = $postfontcolortwo; }

$recordtime = &dateformat($recordtime + $addtimes);

    unless ($recordmembername eq "����") {
	$ppp = qq~<a href="profile.cgi?action=show&member=~ . uri_escape($recordmembername) . qq~" target=_blank><font face=$font color=$fontcolor>$recordmembername</font></a>~;
    }
    else {
	$ppp = qq~<font face="$font" color=$fontcolor>$recordmembername~;
    }

$output .= qq~
<tr bgcolor=$color>
<td width=33% align=center>$ppp</td>
<td width=33% align=center><font face="$font" color=$fontcolor>$recordtrueipaddress</td>
<td width=33% align=center><font face="$font" color=$fontcolor>$recordtime</td>
</tr>
~;
        $lastcolor = $color;

}

$output .= qq~</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT><img src=$imagesurl/images/none.gif height=3 width=0><BR><table cellpadding=0 cellspacing=2 width=$tablewidth align=center><tr bgcolor=$menubackground height=4></tr><tr><td><font color=$menufontcolor>&nbsp;$pages</td>~;
$output .= qq~</tr></table><br>~;

&output("$topictitletemp �ķ��ʼ�¼ @ $forumname",\$output);
exit;
