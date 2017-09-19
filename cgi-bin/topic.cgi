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

$thisprog = "topic.cgi";
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

$jumpto         = $query -> param('jumpto'); if ($jumpto) { print redirect(-location=>"$jumpto"); exit; }
$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic !~ /^[0-9]+$/)||($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }
$man  = $query -> param('man');
$man  = $query->cookie("man") if ($man eq "");
$man  = "" if ($man eq "[]");
$man1 = uri_escape($man);
$mancookie = cookie(-name => "man", -value => "$man1", -path => "$cookiepath/", -expires => "0");

$instart        = $query -> param('start');
$instart	= 0 if ($instart eq "");
$inshow         = $query -> param('show');
$inshow		= 0 if ($inshow eq "");
$inmax          = $query -> param('max');
$maxtopics      = 99999 if ($inmax eq "yes");

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$instart = int($instart/$maxtopics+0.5)*$maxtopics;
$action     = $query -> param('action');
$action     = &stripMETA("$action");
my $onlineview1 = $query->cookie("onlineview");
$onlineview = $onlineview1 if ($onlineview1 ne "");
$onlineview = 0 if ($onlineview eq "");
$onlineview = $onlineview == 1 ? 0 : 1 if ($action eq "onlineview");
$onlineviewcookie = cookie(-name => "onlineview", -value => "$onlineview", -path => "$cookiepath/", -expires => "+30d");
$onlinetitle = $onlineview == 1 ? "[<a href=$thisprog?action=onlineview&forum=$inforum&topic=$intopic&start=$instart&show=$inshow><font color=$titlefontcolor>�ر���ϸ�б�</font></a>]" : "[<a href=$thisprog?action=onlineview&forum=$inforum&topic=$intopic&start=$instart&show=$inshow><font color=$titlefontcolor>��ʾ��ϸ�б�</font></a>]";

if ((($forumimagead eq "1")&&($useimageadtopic eq "1"))||(($forumimagead1 eq "1")&&($useimageadtopic1 eq "1"))) { require "${lbdir}imagead.cgi"; }

$inmembername   = $query->cookie("amembernamecookie");
$inpassword     = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$nodisp = $query->cookie("nodisp");
($nodispavatar, $nodispsign, $nodispphoto)  = split(/\|/,$nodisp);
if ($boarddispsign eq "no") { $nodispsign="yes"; } else { if (!($nodispsign)) { if ($boarddispsign eq "noselect") { $nodispsign="yes"; } else { $nodispsign="no"; } } }

$treeview1  = $query -> cookie("treeview");
$treeview   = $treeview1 if ($treeview1 ne "");
$treeview   = "no" if ($treeview eq "");

$changemode = $query -> param('changemode');
$replynum   = $query -> param('replynum');
if ($changemode ne "") { $treeview=($treeview eq "yes")?"no":"yes"; }

$screenmode = $query->cookie("screenmode");
$screenmode = 8 if ($screenmode eq "");

&ipbanned; #��ɱһЩ ip
$paraspace = "line-height:$paraspace%"   if ($paraspace ne "130");
$wordspace = "letter-spacing:$wordspace" if ($wordspace ne "0");
if (($defaultflashwidth eq "")||($defaultflashwidth < 200)||($defaultflashheight eq "")||($defaultflashheight < 100)) {
    $defaultflashwidth = 410;
    $defaultflashheight = 280;
}

$currenttime = time;

if ((!$inmembername) or ($inmembername eq "����")) { $inmembername = "����"; $myrating= "-1"; $mymembercode="no"; $jifen = -1; &error("��ͨ����&���˲��ܲ鿴�������ݣ���ע����¼������") if ($guestregistered eq "off");}
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
    &getlastvisit;
    $forumlastvisit = $lastvisitinfo{$inforum};
    &setlastvisit("$inforum,$currenttime");
}
$testentry = $query->cookie("forumsallowed$inforum");

&getoneforum("$inforum");
$myinmembmod = $inmembmod;

if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($inmembmod eq "yes")||($membercode eq 'smo')) { $allowed = "yes"; } else { $allowed  = "no"; }

$addtimes = ($timedifferencevalue + $timezone)*3600;
$myrating = -6 if ($myrating eq "");
if (($privateforum eq "yes" && $allowed ne "yes")) { &error("����˽����̳&�Բ�����û��Ȩ�޽����˽����̳��"); }
if (($startnewthreads eq "cert")&&(($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $membercode !~ /^rz/)||($inmembername eq "����"))&&($userincert eq "no")) { &error("������̳&��һ���Ա������������̳��"); }
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

$treeviewcookie  = cookie(-name => "treeview" , -value => "$treeview", -path => "$cookiepath/" , -expires => "+30d");

print header(-cookie=>[$treeviewcookie, $onlineviewcookie,$mancookie, $tempvisitcookie, $permvisitcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

if (open(FILE, "${lbdir}forum$inforum/$intopic.thd.cgi")) {
    sysread(FILE, my $threads,(stat(FILE))[7]);
    close(FILE);
    $threads =~ s/\r//isg;
    @threads = split(/\n/, $threads);
    $numberofitems = @threads;

    if ($man ne '') {
	my $i;
	foreach (@threads) {
	    chomp;
	    $i++;
	    push(@threads1,"$i\t$_\n") if ($_=~/^$man\t/i);
        }
	$numberofitems = @threads1;
    }

} else {
    unlink("${lbdir}forum$inforum/$intopic.pl");
    &error("������&������ⲻ���ڣ������Ѿ���ɾ����");
}

if ($mymembercode eq "ad" or $mymembercode eq "smo" or $myinmembmod eq "yes") {
    $viewhide = 1;
} else {
    $viewhide = 0;
    if ($hidejf eq "yes" ) { 
	my @viewhide=grep(/^$inmembername\t/i,@threads);
	$viewhide=@viewhide;
	$viewhide=1 if ($viewhide >= 1);
    }
}
$StartCheck=$numberofposts+$numberofreplys;

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

    my $filetoopen = "${lbdir}forum$inforum/$intopic.pl";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    my $topicinfo = <FILE>;
    close(FILE);
    chomp $topicinfo;
    $topicinfo =~ s/[\a\f\n\e\0\r]//isg;
    ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $inposttemp, $addmetype) = split (/\t/,$topicinfo);
    if (($topictitle eq "")||($startedby eq "")||($startedpostdate eq "")||($threadposts eq "")||($threadposts > 1000000)) {
	require "dorepiretopic.pl";
    }
    else {
	$posticon =~ s/\s//isg;
	if ($posticon =~/<br>/i) { $posticon = "<br>"; }
        $threadviews = ($threadposts+1) * 8 if ($threadviews eq "");
    }
    $threadviews ++;

    if ($topictitle ne "") {
        open(FILE, ">$filetoopen");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$topicid\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$inposttemp\t$addmetype\t";
        close(FILE);
    }
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

if ($treeview eq "yes") { $viewstyle="&nbsp;<a href=topic.cgi?forum=$inforum&topic=$intopic&changemode=1&show=$inshow><img src=$imagesurl/images/flatview.gif width=40 height=12 border=0 alt=ƽ����ʾ����></a>"; }
                   else { $viewstyle="&nbsp;<a href=topic.cgi?forum=$inforum&topic=$intopic&changemode=1&show=$inshow><img src=$imagesurl/images/treeview.gif width=40 height=12 border=0 alt=������ʾ����></a>"; }
if ($postopen eq "no") { $newthreadbutton = ""; } else { $newthreadbutton = qq~<a href=post.cgi?action=new&forum=$inforum><img src=$imagesurl/images/$skin/$newthreadlogo border=0 alt=����һ��������></a> ~; }
if ($pollopen eq "no") { $newpollbutton = "";   } else { $newpollbutton   = qq~<a href=poll.cgi?action=new&forum=$inforum><img src=$imagesurl/images/$skin/$newpolllogo border=0 alt=����һ����ͶƱ></a> ~; }
if ($payopen eq "no")  { $newpaybutton  = "";   } else { $newpaybutton    = qq~<a href=post.cgi?action=pay&forum=$inforum><img src=$imagesurl/images/$skin/newpay.gif border=0 alt="����һ���½��ף�����֧�����ľ���˵������� http://www.alipay.com/"></a>��~; }

if (($threadstate ne "closed")&&($threadstate ne "pollclosed")&&($postopen ne "no")) {
    $newreplybutton = qq~<a href=post.cgi?action=reply&forum=$inforum&topic=$intopic><img src=$imagesurl/images/$skin/$newreplylogo border=0 alt=�ظ�����></a> ~;
    $replynow = qq~<a href=post.cgi?action=reply&forum=$inforum&topic=$intopic><img src=$imagesurl/images/replynow.gif border=0 alt=�ظ����� width=16>�ظ�</a>��~;
}
else { $replynow=""; $newreplybutton=""; }

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
	my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=0&show=$inshow title="�� ҳ" ><font face=webdings>9</font></a>~;
	my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$endstart&show=$inshow title="β ҳ" ><font face=webdings>:</font></a>~;

	my $uppage = $currentpage - 1;
	my $nextpage = $currentpage + 1;
	my $upstart = $instart - $maxtopics;
	my $nextstart = $instart + $maxtopics;
	my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$upstart&show=$inshow title="��$uppageҳ"><font face=webdings>7</font></a>~;
	my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$nextstart&show=$inshow title="��$nextpageҳ"><font face=webdings>8</font></a>~;

	my $tempstep = $currentpage / 7;
	my $currentstep = int($tempstep);
	$currentstep++ if ($currentstep != $tempstep);
	my $upsteppage = ($currentstep - 1) * 7;
	my $nextsteppage = $currentstep * 7 + 1;
	my $upstepstart = ($upsteppage - 1) * $maxtopics;
	my $nextstepstart = ($nextsteppage - 1) * $maxtopics;
	my $showupstep = $upsteppage < 1 ? "" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$upstepstart&show=$inshow class=hb title="��$upsteppageҳ">��</a> ~;
	my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$nextstepstart&show=$inshow class=hb title="��$nextsteppageҳ">��</a> ~;

	$pages = "";
	my $currentstart = $upstepstart + $maxtopics;
	for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++)
	{
		last if ($i > $numberofpages);
		$pages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<a href=$thisprog?forum=$inforum&topic=$intopic&start=$currentstart&show=$inshow class=hb>$i</a> ~;
		$currentstart += $maxtopics;
	}
	$pages = "<font color=$menufontcolor><b>�� <font color=$fonthighlight>$numberofpages</font> ҳ</b> $beginpage $showup \[ $showupstep$pages$shownextstep\] $shownext $endpage</font><br>";
}
else {
	$startarray = 0;
	$endarray = $numberofitems - 1;
	$pages = "<font color=$menufontcolor>������ֻ��һҳ</font><br>";
}

if ($usefake eq "yes") {
    $pages =~ s/topic.cgi\?forum=([0-9]+?)&topic=([0-9]+?)&start=([0-9]+?)&show=([0-9]+?)([\ \'\"\>])/topic-$1-$2-$3-$4-.htm$5/isg;
    $pages =~ s/topic.cgi\?forum=([0-9]+?)&topic=([0-9]+?)&show=([0-9]+?)([\ \'\"\>])/topic-$1-$2-0-$3-.htm$4/isg;
    $pages =~ s/topic.cgi\?forum=([0-9]+?)&topic=([0-9]+?)&replynum=([^\"\+\ ]+?)([\ \'\"\>])/topic-$1-$2-0-0-$3.htm$4/isg;

    $printpageicon = qq~ <a href=printpage-$inforum-$intopic.htm><img src=$imagesurl/images/printpage.gif border=0 width=16 alt=��ʾ�ɴ�ӡ�İ汾></a>&nbsp;~;
} else {
    $printpageicon = qq~ <a href=printpage.cgi?forum=$inforum&topic=$intopic><img src=$imagesurl/images/printpage.gif border=0 width=16 alt=��ʾ�ɴ�ӡ�İ汾></a>&nbsp;~;
}

$reporticon    = qq~ <a href=report.cgi?forum=$inforum&topic=$intopic><img src=$imagesurl/images/report.gif border=0 width=16 alt=���������⣬���Ͷ���Ϣ���������></a>&nbsp;~;
$favicon       = qq~ <a href=fav.cgi?action=add&forum=$inforum&topic=$intopic><img src=$imagesurl/images/fav.gif border=0 width=13 alt=��������ղ�&��ע����></a>&nbsp;~;
if (($privateforum ne "yes")&&($emailfunctions eq "on")) { $sendtofriendicon = qq~ <a href=lbfriend.cgi?forum=$inforum&topic=$intopic><img src=$imagesurl/images/emailtofriend.gif border=0 width=16 alt=���ͱ�ҳ�������></a>&nbsp;~; }
$pagpageicon   = qq~ <img src=$imagesurl/images/pag.gif border=0 width=16 alt=�ѱ�������ʵ� style=cursor:hand onClick="javascript:openScript('pag.cgi?forum=$inforum&topic=$intopic',500,400)">&nbsp;~ if ($emailfunctions eq "on");
$fontsizeselect = qq~<select OnChange="SetPostFont(this.value)"><option value="12">Ĭ��</option><option value="15">�Դ�</option><option value="18">��ͨ</option><option value="21">�ϴ�</option><option value="24">�ܴ�</option><option value="30">���</option></select>~;
$postfontsize1 = $query->cookie("postfontsize");
$postfontsize1 = $postfontsize if ($postfontsize1 eq "");
$postfontsize1 = "12" unless ($postfontsize1 =~ /^[0-9]+$/);
$postfontsize = $postfontsize1;
$fontsizeselect =~ s/<option value="$postfontsize">/<option value="$postfontsize" selected>/;

$replynum=0 if ($replynum eq "");
if ($replynum > $numberofitems-1) { $replynum = $numberofitems - 1;};
if($replynum eq "last" && $treeview ne "yes"){
   $movetobottom=qq(document.location="#bottom";);
}
if ($treeview eq "yes") {
     $replynum   = $instart if (($instart ne "")&&($instart ne "0")&&($replynum ne "last"));
     $replynum   = $numberofitems - 1 if ($replynum eq "last");
     $startarray = $replynum;
     $endarray   = $replynum;
}

(my $trash, $topictitle) = split(/\t/,$threads[0]);
$topictitletemp = $topictitle;
$topictitletemp =~ s/^����������//;

	if ($addtopictime eq "yes") {
	    my $topictime = &dispdate($startedpostdate + $addtimes);
	    $topictitletemp = "[$topictime] $topictitletemp";
	}
	
$topictitletemp =~s/ \(������\)$//;
$topictitletemp =~s/\&\#039\;//isg;
$topictitletemp = &cleaninput($topictitletemp);
$bookmarkpage  = qq~ <span style=CURSOR:hand onClick="window.external.AddFavorite('$boardurl/topic.cgi?forum=$inforum&topic=$intopic', ' $boardname - $topictitletemp')"><IMG SRC=$imagesurl/images/fav_add1.gif width=15 alt=�ѱ��������ղؼ�></span>&nbsp;~;

&title;

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (-e "$filetoopens.lck"){
    $memberoutput = "";
    $membertongji = " <b>���ڷ�������æ�����Ա����������������ʱ���ṩ��ʾ��</b>";
    $onlinetitle = "";
    unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
} else {
   if ($privateforum ne "yes") { &whosonline("$inmembername\t$forumname\t$forumname<>�����$topictitletemp��\t���<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitletemp</b></a>\t"); }
                          else { &whosonline("$inmembername\t$forumname(��)\t$forumname<>topictitletemp(��)\t�����������\t"); }
    $membertongji =~ s/����̳/����/o;
    $membertongji =~ s/������/�����/o;
    undef $memberoutput if ($onlineview != 1);
}

$output .= qq~<br>~;
if (-e "${lbdir}cache/forumstopic$inforum.pl") {
  eval{ require "${lbdir}cache/forumstopic$inforum.pl";};
  if ($@) { unlink ("${lbdir}cache/forumstopic$inforum.pl"); require "dotopic.pl"; }
} else { require "dotopic.pl"; }

if (($usejhpoint eq "yes")&&($jhdata =~ /\_$topicid\_/)) {
    $jhimage = qq~ <img src="$imagesurl/images/$skin/$new_JH" align=absmiddle alt=����Ϊ��������> ~;
}

my $topictitletempshow = &lbhz($topictitletemp,34);
$tempoutput =~ s/topictitletempshow/$topictitletempshow/isg;
$tempoutput =~ s/jhimage/$jhimage/isg;

$output .= $tempoutput;

if ($usefake eq "yes") {

    $output =~ s/forums.cgi\?forum=([0-9]+?)&show=([0-9]+?)([\ \'\"\>])/forums-$1-$2.htm$3/isg;
    $output =~ s/forums.cgi\?forum=([0-9]+?)([\ \'\"\>])/forums-$1-0.htm$2/isg;

    $output =~ s/leobbs.cgi\?action=(.+?)([\ \'\"\>])/=leobbs-$1.htm$2/isg;
    $output =~ s/([\=\'\"\/])leobbs.cgi/${1}leobbs.htm/isg;

}

if ($startarray eq "0" && $arrawrecordclick eq "yes") {
    my $ipaddress  = $ENV{'REMOTE_ADDR'};
    $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $trueipaddress = $ipaddress if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
    my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
    $trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 !~ m/a-z/i && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
    open(FILECLICK,">>${lbdir}forum$inforum/$intopic.clk.pl");
    print FILECLICK  "$inmembername\t$ipaddress\t$trueipaddress\t$currenttime\t\n";
    close(FILECLICK);
}

$insidead  = "" if (($forumimagead ne "1")&&($useimageadtopic ne "1"));
$insidead1 = "" if (($forumimagead1 ne "1")&&($useimageadtopic1 ne "1"));
if ($threadviews > 0) {
    $threadviewstemp = "���������Ķ� <b>$threadviews</b> �Ρ�";
    $threadviewstemp = "<a href=dispclick.cgi?forum=$inforum&topic=$intopic title=�鿴�����ķ��ʼ�¼ target=_blank>$threadviewstemp</a>" if ($membercode eq 'ad' || $membercode eq 'smo' || $inmembmod eq 'yes');
}

$output .= qq~<script>
var setpostno=Array(); 
var start=($startarray==0)?$startarray+2:$startarray+1; 
var end=$endarray+2; 
start=("$treeview" == "yes")?2:start; 
end=("$treeview" == "yes")?$numberofitems+1:end; 
function DelReply(){
DReply.postno.value="";
for(i=start;i<end;i++){
var tempval=eval("document.all.postno"+i+".checked");
if(tempval == true){
DReply.postno.value+=i+" ";
}}
DReply.submit();
}
</script>
~ if(($mymembercode eq "ad")||($mymembercode eq 'smo')||($mymembercode eq 'cmo')||($myinmembmod eq "yes"));

$noimg = qq~
window.onload=addSenToEventHandle(window.onload,"checkImages();")
function checkImages(){
if (document.getElementById){
var imagesArr = new Array();var setDefaultErrImg = NoImagesURL;var setDefaultErrTxt = "���Ӳ�����";imagesArr = document.getElementsByTagName("img");
for(var i = 0; i < imagesArr.length; i++){
if(!imagesArr[0].getAttribute("nc") == "1"){
var tempImgAttrib = imagesArr[i].getAttribute("alt");imagesArr[i].setAttribute("alt", "");
if(imagesArr[i].width == "28" && imagesArr[i].height == "30"){
imagesArr[i].src = setDefaultErrImg;imagesArr[i].setAttribute("alt", setDefaultErrTxt);
}
else{
imagesArr[i].setAttribute("alt", tempImgAttrib);
}}}}}
var NoImagesURL = "$imagesurl/images/imageno.gif";
~ if ($usenoimg eq "yes");

$output .= qq~$insidead$insidead1
<a name="top"></a><br>
<script>
$noimg
function bbimg(o){var zoom=parseInt(o.style.zoom,10)||100;zoom+=event.wheelDelta/12;if (zoom>0) o.style.zoom=zoom+'%';return false;}
$movetobottom
~;
if ($usefake eq "yes") {
$output .= qq~function O9(id) {if(id != "") window.open("profile-"+id+".htm");}~;
} else {
$output .= qq~function O9(id) {if(id != "") window.open("profile.cgi?action=show&member="+id);}~;
}
$output .= qq~
function loadThreadFollow(f_id,t_id,r_id,ftype,fname){
if (r_id != "") {
    var targetImg =eval("document.images.followImg" + r_id);
}
else {
    var targetImg =eval("document.images.followImg" + fname);
}
if (r_id != "") {
var targetDiv =eval("follow" + r_id);
}
else {
var targetDiv =eval("follow" + fname);
}
if (targetImg.nofollow <= 0){return false;}
if (typeof(targetImg) == "object"){
if (targetDiv.style.display!='block'){
targetDiv.style.display="block"; targetImg.src="$imagesurl/images/cat1.gif";
if (typeof fname=="undefined") {fname = "";}
if (typeof r_id=="undefined") {r_id = "";}
if (targetImg.loaded=="no"){ document.frames["hiddenframe"].location.replace("getphotoinfo.cgi?forum="+f_id+"&topic="+t_id+"&reply="+r_id+"&ftype="+ftype+"&fname="+fname); }
}else{ targetDiv.style.display="none"; targetImg.src="$imagesurl/images/cat.gif"; }
}}
</script>
<style>
.ts {BORDER-RIGHT:black 1px solid;PADDING-RIGHT:2px;BORDER-TOP:black 1px solid;PADDING-LEFT:2px;PADDING-BOTTOM:2px;MARGIN-LEFT:18px;BORDER-LEFT:black 1px solid;WIDTH:250px;COLOR:black;PADDING-TOP:2px;BORDER-BOTTOM:black 1px solid;BACKGROUND-COLOR:lightyellow;cursor:hand;}
.ts1 {BORDER-RIGHT:$tablebordercolor 1px solid;PADDING-RIGHT:2px;BORDER-TOP:$tablebordercolor 1px solid;PADDING-LEFT:2px;PADDING-BOTTOM:2px;MARGIN-LEFT:18px;BORDER-LEFT:$tablebordercolor 1px solid;COLOR:black;PADDING-TOP:2px;BORDER-BOTTOM:$tablebordercolor 1px solid;BACKGROUND-COLOR:lightyellow;cursor:hand;}
</style>
<iframe width=0 height=0 src="" id=hiddenframe></iframe>
~;
if ($privateforum ne "yes") {
    $output .= qq~<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor width=92% $catbackpic><font color=$titlefontcolor>$membertongji�� $onlinetitle</td>
<td bgcolor=$titlecolor width=8% align=center $catbackpic><a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 width=40 height=12></a></td>
</tr>
~;
    $output .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><table cellPadding=1 cellSpacing=0>$memberoutput</table></td></tr>~ if ($onlineview == 1 && $memberoutput);
    $output .= qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}

if ($topicad ne "") {
    $topicad = &HTML("$topicad");
    $topicad =~ s/\$imagesurl/$imagesurl/isg;
    $topicad =~ s/\$tablebordercolor/$tablebordercolor/isg;
    $topicad =~ s/\$forumcolorone/$forumcolorone/isg;
    $topicad =~ s/\$forumcolortwo/$forumcolortwo/isg;
    $topicad =~ s/\[br\]/\n/isg;
}

$output .= qq~$topicad<table cellpadding=1 cellspacing=0 width=$tablewidth align=center><tr><td height=22><span id=LeoBBSgg style=display:none></span></td></tr>
<tr><td align=center width=1></td>
<td width=435 valign=bottom>$newthreadbutton$newreplybutton$newpollbutton$newpaybutton</td>
<td align=right valign=bottom width=* nowarp><font color=$forumfontcolor>$threadviewstemp�� <a href=gettopicno.cgi?forum=$inforum&topic=$topicid&show=$inshow&act=pre><img src=$imagesurl/images/prethread.gif border=0 alt=�����һƪ���� width=52 height=12></a>&nbsp;��<a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 alt=ˢ�±����� width=40 height=12></a> $viewstyle��<a href=gettopicno.cgi?forum=$inforum&topic=$topicid&show=$inshow&act=next><img src=$imagesurl/images/nextthread.gif border=0 alt=�����һƪ���� width=52 height=12></a></td><td align=center width=2></td></tr></table>
<SCRIPT>valigntop()</SCRIPT>
<table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td height=1></td></tr></table>
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center><tr><td bgcolor=$tablebordercolor width=1 height=24><img src=$imagesurl/images/none.gif width=1></td><td bgcolor=$titlecolor colspan=2 $catbackpic>
<table cellpadding=0 cellspacing=1 width=100%><tr><td><font color=$titlefontcolor>&nbsp;<b>* ��������</B>�� $topictitletemp</td>
<td align=right> <a href=$thisprog?forum=$inforum&topic=$intopic&start=$instart&max=yes&show=$inshow><img src=$imagesurl/images/showall.gif border=0 width=14 alt=����ҳ��ʾ����></a>&nbsp;$reporticon$favicon$printpageicon$pagpageicon$bookmarkpage$sendtofriendicon $fontsizeselect&nbsp;</td></tr></table></td><td bgcolor=$tablebordercolor width=1 height=24></td></tr></table>
<table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td height=1></td></tr></table>
~;

if (open (FILE, "${lbdir}FileCount/$inforum/$inforum\_$intopic.pl")) {
    @usruploaddata =<FILE>;
    close(FILE);
    chomp @usruploaddata;
    my $usruploaddatano1 = @usruploaddata;
    my @usruploaddata1 = grep(/^$inforum\_$intopic(\.|\_)/,@usruploaddata);
    my $usruploaddatano2 = @usruploaddata1;
    if (($usruploaddatano1 ne $usruploaddatano2) && ($usruploaddata2 > 0)) {
        unlink ("${lbdir}FileCount/$inforum/$inforum\_$intopic.pl");
        print "ҳ���Ѿ����£������Զ�ˢ�£����û���Զ�ˢ�£����ֹ�ˢ��һ�Σ���<BR><BR><meta http-equiv='refresh' content='0;'>";
        exit;
    }
} else {
    opendir (USRDIR, "${imagesdir}$usrdir/$inforum");
    @usruploaddata = readdir(USRDIR);
    closedir (USRDIR);
    @usruploaddata = grep(/^$inforum\_$intopic(\.|\_)/,@usruploaddata);
    chomp @usruploaddata;
#    open (FILE, ">${lbdir}FileCount/$inforum/$inforum\_$intopic.pl");
#    print FILE join("\n",@usruploaddata);
#    print FILE "\n" if ($#usruploaddata > 0);
#    close(FILE);
}
$usruploaddata = @usruploaddata;
if ($usruploaddata > 0) {
    @usruploaddatareply = grep(/^$inforum\_$intopic\_/,@usruploaddata);
    $usruploaddatareply = @usruploaddatareply;
}

$editpostnumber = $startarray + 1;
$postcountnumber = 0;
$endarraytemp = $endarray + 1;
$rn=$startarray;
$postcopyright = "<font color=$fonthighlight>$postcopyright</font><br>" if ($postcopyright ne "");
$output .= qq~
<script>
function SetPostFont(value){
for (i = $editpostnumber; i <= $endarraytemp; i++){
var target = eval("post" + i);
target.style.fontSize = value + "px";
}
var exp = new Date();exp.setTime(exp.getTime() + 30*86400*1000);
SetCookie("postfontsize", value, exp,"$cookiepath/");
}
function submitonce(theform){
if (document.all||document.getElementById){
for (i=0;i<theform.length;i++){
var tempobj=theform.elements[i]
if(tempobj.type.toLowerCase()=="submit"||tempobj.type.toLowerCase()=="reset")
tempobj.disabled=true
}}}
function addpost(num){
var postnum = eval('postnum'+num);
postnum.innerHTML="<form method=post action=addpost.cgi onSubmit=submitonce(this)><input name=id type=hidden value="+num+"><input name=forum type=hidden value=$inforum><input name=topic type=hidden value=$intopic><textarea rows=6 name=inpost cols=35></textarea><p></p><input type=submit value=��д����></form>";
}
function ResetReplyTitle(no) {
        document.forms('FORM').floor.value= no ;
        return true;
}
function SetCookie (name, value) { var argv = SetCookie.arguments;var argc = SetCookie.arguments.length;var expires = (argc > 2) ? argv[2] : null;var path = (argc > 3) ? argv[3] : null;var domain = (argc > 4) ? argv[4] : null;var secure = (argc > 5) ? argv[5] : false; document.cookie = name + "=" + escape (value) + ((expires == null) ? "" : ("; expires=" + expires.toGMTString())) + ((path == null) ? "" : ("; path=" + path)) + ((domain == null) ? "" : ("; domain=" + domain)) + ((secure == true) ? "; secure" : ""); } 
</script>
~;

if ($magicface ne 'off') {
    $output.=qq~
<script>
function MM_showHideLayers() {var i,p,v,obj,args=MM_showHideLayers.arguments;obj=document.getElementById("MagicFace");for (i=0; i<(args.length-2); i+=3) if (obj) { v=args[i+2];if (obj.style) { obj=obj.style; v=(v=='show')?'visible':(v=='hide')?'hidden':v; }obj.visibility=v; }}
function ShowMagicFace(MagicID) {var MagicFaceUrl = "$imagesurl/MagicFace/swf/" + MagicID + ".swf";document.getElementById("MagicFace").innerHTML = '<object codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,29,0" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="500" height="350"><param name="movie" value="'+ MagicFaceUrl +'"><param name="menu" value="false"><param name="quality" value="high"><param name="play" value="false"><param name="wmode" value="transparent"><embed src="' + MagicFaceUrl +'" wmode="transparent" quality="high" pluginspage="http://www.macromedia.com/go/getflashplayer" type="application/x-shockwave-flash" width="500" height="350"></embed></object>';document.getElementById("MagicFace").style.top = (document.body.scrollTop+((document.body.clientHeight-300)/2))+"px";document.getElementById("MagicFace").style.left = (document.body.scrollLeft+((document.body.clientWidth-480)/2))+"px";document.getElementById("MagicFace").style.visibility = 'visible';setTimeout("MM_showHideLayers('MagicFace','','hidden')",10000);}</script><DIV id=MagicFace style="Z-INDEX: 99; VISIBILITY: hidden; POSITION: absolute"></DIV>
~;
}

if (($useads ne "no")&&(-e "${imagesdir}leogg.js")) {
    $addads = "<span id=LeoBBSgg>$boardname���λ��</span>";
}
else { $addads = ""; }

if($man ne '') { @threads=@threads1; }
foreach (@threads[$startarray .. $endarray]) {
  chomp $_;
#    next if ($_ eq "");
  if ($usruploaddata > 0) {
    my $addmefile =0;
    if ($rn>0) {
	if ($usruploaddatareply > 0) {
            $rrn = $rn;
            my @usruploaddata1 = grep(/^$inforum\_$intopic\_$rrn\./,@usruploaddatareply);
	    my @downcount      = grep(/$inforum\_$intopic\_$rrn\./,@filedowncount);
            if ($#usruploaddata1 >= 0) {
               my $usruploadfile = $usruploaddata1[0]; chomp $usruploadfile;
               ($up_name, $up_ext) = split(/\./,$usruploadfile);
                $up_ext =~ tr/A-Z/a-z/;
          	$addmefile =1;
          	$usruploaddatareply --;
            }
	}
    }
    else {
        my @usruploaddata2 = grep(/^$inforum\_$intopic\./,@usruploaddata);
	my @downcount      = grep(/$inforum\_$intopic\./,@filedowncount);
        if ($#usruploaddata2 >= 0) {
	    my $usruploadfile = $usruploaddata2[0]; chomp $usruploadfile;
            ($up_name, $up_ext) = split(/\./,$usruploadfile);
            $up_ext =~ tr/A-Z/a-z/;
            $addmefile =1;
        }
    }
    if (!(-e "${imagesdir}$usrdir/$inforum/$up_name.$up_ext")) {
        unlink ("${lbdir}FileCount/$inforum/$inforum\_$intopic.pl");
        print "ҳ���Ѿ����£������Զ�ˢ�£����û���Զ�ˢ�£����ֹ�ˢ��һ�Σ�<BR><BR><meta http-equiv='refresh' content='0;'>";
        exit;
    }
    if ($addmefile == 1) {
   	@fileinfo = stat("${imagesdir}$usrdir/$inforum/$up_name.$up_ext");
	$filetype = "unknow";
	$filetype = $up_ext if (-e "${imagesdir}icon/$up_ext.gif");
	if (($up_ext eq "gif")||($up_ext eq "jpg")||($up_ext eq "jpe")||($up_ext eq "jpeg")||($up_ext eq "tif")||($up_ext eq "png")||($up_ext eq "bmp")) {
            if (($nodispphoto eq 'yes')||($arrawpostpic eq 'off')) {
	    	$addme = qq(<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&type=.$up_ext target=_blank><img src=$imagesurl/icon/$filetype.gif border=0 width=16></a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&type=.$up_ext target=_blank>�����ʾ���������ͼƬ</a><br>);
	    } else{
	    	$addme = qq(<img src=$imagesurl/icon/$filetype.gif border=0 width=16> ���������ͼƬ���£�<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&type=.$up_ext target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&type=.$up_ext border=0 alt=�������´������ͼƬ onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"></a><br>);
	    }
	    $addme .= qq(<img src=$imagesurl/images/none.gif whidth=0 height=5><BR><span style=CURSOR:hand onclick=loadThreadFollow($forumid,$topicid,$editpostnumber,'$up_ext')><img id=followImg$editpostnumber src=$imagesurl/images/cat.gif width=9 loaded=no nofollow="cat.gif" valign=absmiddle> ���˲鿴ͼƬ��ϸ��Ϣ<table cellpadding=0 class=ts1 cellspacing=0 width=50% id=follow$editpostnumber style=DISPLAY:none><tr><td id=followTd$editpostnumber><DIV class=ts onclick=loadThreadFollow($forumid,$topicid,$editpostnumber,'$up_ext')>���ڶ�ȡ��ͼƬ����ϸ��Ϣ�����Ժ� ...</DIV></td></tr></table></span><BR><BR>);
	}
	elsif ($up_ext eq "swf") {
	    if ($arrawpostflash eq "on") {
	        $addme = qq(<img src=$imagesurl/icon/$filetype.gif border=0 width=16> ��������һ�� $up_ext ��ʽ Flash ���� (�� $fileinfo[7] �ֽ�)<br><br><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&type=.$up_ext quality=high width=$defaultflashwidth height=$defaultflashheight pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed><br>&nbsp;<img src=$imagesurl/images/fav.gif width=16> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&type=.$up_ext target=_blank>ȫ���ۿ�</a> (���Ҽ�����)<br><br>)
	    } else {
	        $addme=qq(<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&type=.$up_ext target=_blank><img src=$imagesurl/icon/$filetype.gif border=0 width=16 height=16>������� Flash ����</a>);
	    }
	}
	elsif (($up_ext eq "torrent")&&(($rn eq 0)||($rn eq ""))) {
	    require "dobtinfo.pl";
	}
	else {
        	$addme = qq(<font color=$fonthighlight>��ظ���</font>��<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&type=.$up_ext target=_blank><img src=$imagesurl/icon/$filetype.gif border=0 width=16 alt="��������һ����$filetype�����͸������������"></a> (�� $fileinfo[7] �ֽ�)<br><br>);		
	}
    } else { $addme = ""; }
  } else { $addme = ""; }

  if ($man ne '') {
    ($editpostnumber,$membername, $topictitle, $postipaddresstemp, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/,$_);
  } else {
    ($membername, $topictitle, $postipaddresstemp, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/,$_);
  }

#    next if ($membername eq "");

    if (($inmembername eq "" || $inmembername eq "����")&&($waterwhenguest eq "yes")){
	$post="\[watermark]\n$post\[\/watermark]";
    }

    $postsize = length($post);

    if ($membername =~ /\(��\)/isg) {
    	$tempname = "";
    	$membername=~s/\(��\)/ \(����\)/isg;
	$membername{"����"}  = $membername;
	$membername = "����";
	require "guestinfo.pl" if ($membercode{"����"} eq "");
    }
    else {
    	$tempmname = $membername;  #�� getnameinfo.pl �õ�
    	$tempname =  uri_escape($membername);
	$membername =~ s/ /\_/g;
	$membername =~ tr/A-Z/a-z/;
	$membername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
        if ($membercode{$membername} eq "") {
	    if (-e "${lbdir}cache/meminfo/$membername.pl") {
	        eval{ require "${lbdir}cache/meminfo/$membername.pl";};
	        if (($@)||($membername{$membername} eq "")||($membercode{$membername} eq "")) { unlink ("${lbdir}cache/meminfo/$membername.pl"); require "getnameinfo.pl" if ($onloadinfopl ne 1); &getmemberinfo($membername); }
	    }
	    else {
                require "getnameinfo.pl" if ($onloadinfopl ne 1);
                &getmemberinfo($membername);
            }
        }
    }

    $topictitle =~ s/^����������//;
    ($postipaddress,$truepostipaddress) = split(/\=/,$postipaddresstemp);

    if (($truepostipaddress eq "")||($truepostipaddress eq $postipaddress)) {
	$truepostipaddress = $postipaddress;
	$proxyip = 1;
    }
    else { $proxyip = 0; }

    if (($threadstate ne "closed")&&($threadstate ne "pollclosed")&&($postopen ne "no")) {
        $replygraphic = qq~<a href=post.cgi?action=replyquote&forum=$inforum&topic=$intopic&postno=$editpostnumber title=���ûظ��������><img src=$imagesurl/images/reply.gif border=0 width=16 align=absmiddle>����</a>��~;
    } else { $replygraphic="";}
    
    if ($waterwhenguest eq "yes" && $inmembername eq "����") {
    	$copygfx = "";
    } else {
        $copygfx = qq~<a href=post.cgi?action=copy1&forum=$inforum&topic=$intopic&postno=$editpostnumber title=�����������><img src=$imagesurl/images/copy.gif border=0 width=16 align=absmiddle>����</a>��~;
    }
    

    $postdate = &dateformat($postdate+$addtimes);
    $mynodispsign=$nodispsign;

    if ($forummodnamestemp =~ /\Q\,$membername{$membername}\,\E/i) { $inmembmod = "yes"; } else { $inmembmod = "no"; }
    $mynodispsign="no" if ($membercode{$membername} eq 'ad' || $membercode{$membername} eq 'smo'|| $inmembmod eq "yes");

    if ($onlineuserlist =~ /\_$membername{$membername}\_/i) { $onlineinfo = "���û�Ŀǰ����";$onlinepic="online1.gif"; } else { $onlineinfo = "���û�Ŀǰ������";$onlinepic="offline1.gif"; }
    if (($mymembercode eq "ad")&&($onlineuserlisthidden =~ /\_$membername{$membername}\_/i)) { $onlineinfo = "���û�Ŀǰ��������״̬";$onlinepic="onlinehidden.gif"; }
    $online = qq~<IMG SRC=$imagesurl/images/$onlinepic width=15 alt=$onlineinfo align=absmiddle>~;

    if ($post =~m/\[hidepoll\]/isg) { $PollHidden='yes'; } else { $PollHidden='no'; }
    $post =~ s/\[hidepoll\]//isg;

    if ($count eq 1) { $postbackcolor = "$postcolorone"; $postfontcolor = "$postfontcolorone"; $count++; } else { $postbackcolor = "$postcolortwo"; $postfontcolor = "$postfontcolortwo"; $count = 1; }

    if ((($post =~ /(\&\#35\;|#)Moderation Mode/i) && ($membercode{$membername} eq 'mo' ||$membercode{$membername} eq 'amo'||$membercode{$membername} eq 'cmo'|| $membercode{$membername} eq 'ad' || $membercode{$membername} eq 'smo')) || $htmlstate eq 'on') {
        $post =~ s/(\&\#35\;|#)Moderation Mode/***** ����ģʽ *****\<BR\>/g;
        $post =~ s/&lt;/</g; $post =~ s/&gt;/>/g; $post =~ s/\&\#35\;/\#/g; $post =~ s/&quot;/\"/g; $post =~ s/( |\>)<br>/$1\n/sg; $post =~ s/( |\>)<p>/$1\n\n/sg;
    } else { $post =~ s/style/\&\#115\;tyle/isg; }
    if (($mymembercode eq "ad")||($mymembercode eq 'smo')||($myinmembmod eq "yes")||(($usereditpost ne "no")&&(lc($inmembername) eq lc($membername{$membername}))))  {
    	if ($post=~m/\[ALIPAYE\]/) {
    	    $editgraphic    = qq~<a href=editpay.cgi?action=edit&forum=$inforum&topic=$intopic title=�༭���������><img src=$imagesurl/images/edit.gif border=0 width=16 align=absmiddle>�༭</a>��~;
    	} else {
    	    $editgraphic    = qq~<a href=editpost.cgi?action=edit&forum=$inforum&topic=$intopic&postno=$editpostnumber title=�༭�������><img src=$imagesurl/images/edit.gif border=0 width=16 align=absmiddle>�༭</a>��~;
    	}
    } else { $editgraphic =""; }

    if (($mymembercode eq "ad")||($mymembercode eq 'smo')||($myinmembmod eq "yes")) {
    	if ($post =~ /\[POSTISDELETE=(.+?)\]/) {
    	    $pbgraphic = qq~<a href=delpost.cgi?action=unpostdeleteonce&forum=$inforum&topic=$intopic&postno=$editpostnumber title=ȡ����������ظ�><img src=$imagesurl/images/yes.gif border=0 width=15 align=absmiddle>ȡ������</a>��~; 
    	} else {
    	    $pbgraphic = qq~<a href=delpost.cgi?action=postdeleteonce&forum=$inforum&topic=$intopic&postno=$editpostnumber title=��������ظ�><img src=$imagesurl/images/no.gif border=0 width=15 align=absmiddle>����</a>��~; 
    	}
    } else { $pbgraphic = ""; }

    if (($emoticons eq 'on') and ($showemoticons eq 'yes')) {
        &doemoticons(\$post);
	&smilecode(\$post);
    }

    if ($idmbcodestate eq 'on') {
	&lbcode(\$post);
        if ($post =~/<blockquote><font face=$font>����/isg){
            $post =~ s/\&amp\;/\&/ig ;
            $post =~ s/\&lt\;br\&gt\;/<br>/ig;
	}
    } else {
    	require "codeno.cgi";
	&lbnocode(\$post);
	$post =~ s/\[DISABLELBCODE\]//isg;
    }

    $post =~ s/(^|\>|\n)\[���(.+?)�����(.+?)�༭\]/$1\<font color=$posternamecolor\>\[���$2�����$3�༭\]\<\/font\>/isg;

    if ($canchgfont ne "no") {
      if ($post =~/\[USECHGFONTE\]/) {
	$post =~ s/\[USECHGFONTE\]//isg;
        $post =~ s/(^|\>|\n)(\[���.+?�����.+?�༭\])(.*)/$1$2<div id=CArea$inforum$editpostnumber>$3<\/div><script>var _old$inforum$editpostnumber=CArea$inforum$editpostnumber.innerHTML;ConFONT('$inforum$editpostnumber','$imagesurl','1');<\/script>/isg;
	if (!($2)) { $post = qq~<div id=CArea$inforum$editpostnumber>$post</div><script>var _old$inforum$editpostnumber=CArea$inforum$editpostnumber.innerHTML;ConFONT('$inforum$editpostnumber','$imagesurl','1');</script>~; }
	$chgposticon = "<span id=OArea$inforum$editpostnumber></span>��";
      }
      else { $chgposticon = ""; }
    } else { $post =~ s/\[USECHGFONTE\]//isg; $chgposticon = "";}

    $posticon =~ s/[\a\f\n\e\0\r]//isg;
    if ($posticon =~/<br>/i) {
        require "topicpoll.pl";
    }
    else {
        $posticon = qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight>~ if ($posticon ne "");
    }
    
    if ((lc($inmembername) eq lc($membername))&&($inmembername ne "����")&&(($threadstate ne "closed")&&($threadstate ne "pollclosed")&&($postopen ne "no"))){
	$post.="<br><br><br><span id=postnum$editpostnumber><span style=cursor:hand onClick=javascript:addpost('$editpostnumber');><font color=$fonthighlight><b>[�������...]</b></span></span><br>";
    }

    if ($membercode{$membername} eq "masked") {
    	$addme = "";
	$signature{$membername} = "";
        $post = qq(<br>------------------------<br><font color=$posternamecolor>���û��ķ����Ѿ������Σ�<br>�������ʣ�����ϵ����Ա��</font><br>------------------------<BR></td><td width=16>);
    }

    if ($man eq '') {
        my $man=uri_escape($membername{$membername});
        $postmanbuttom ="<a href=$thisprog?forum=$inforum&topic=$intopic&show=$inshow&man=$man><img src=$imagesurl/images/lookme.gif border=0 width=16 align=absmiddle>ֻ����</a>��";
    } else {
        $postmanbuttom ="<a href=$thisprog?forum=$inforum&topic=$intopic&show=$inshow&man=[]><img src=$imagesurl/images/find.gif border=0 width=16 align=absmiddle>ȡ��ֻ����</a>��";
    }

    $signature{$membername} = "<font color=$posternamecolor>���û���ǩ���Ѿ������Σ�</font>" if ($notshowsignaturemember =~/\t$membername{$membername}\t/i);

### ÿ������ǩ��ֻ��ʾһ�Σ�
    if(",$signature_check"=~/,$membername{$membername},/){
        $showsignature = 'no';
    }else{
        $signature_check.=$membername{$membername}.',';
    }
### ÿ������ǩ��ֻ��ʾһ�Σ�

    if (($signature{$membername}) and ($showsignature eq 'yes') and ($nodispsign eq "no"||$mynodispsign eq "no") and ($posticon !~/<br>/i)) {
        if ($signature{$membername} ne "") { $post = qq($post<BR></td><td width=16></td></tr><tr><td></td><td valign=bottom><BR><BR><BR><BR>$postcopyright<img src=$imagesurl/images/none.gif width=1 height=3><BR><img src=$imagesurl/images/signature.gif height=12><br><img src=$imagesurl/images/none.gif width=1 height=5><BR>$signature{$membername}<BR>); $post.="$pet{$membername}<BR>" if ($pet{$membername} ne ''); }
	                 else { $post = qq($post<BR></td><td width=16></td></tr><tr><td></td><td valign=bottom><BR><BR><BR><BR>$postcopyright<BR>); $post.="$pet{$membername}<BR>" if ($pet{$membername} ne ''); }
    }
    else { $post = qq($post<BR></td><td width=16></td></tr><tr><td></td><td valign=bottom><BR><BR><BR><BR>$postcopyright<BR>); }

    if (($mymembercode eq "ad")||($mymembercode eq 'smo')||($myinmembmod eq "yes")||(($arrowuserdel ne "off")&&(lc($inmembername) eq lc($membername{$membername})))) { $delgraphic = qq~<a href=delpost.cgi?action=directdel&forum=$inforum&topic=$intopic&postno=$editpostnumber title=ɾ������ظ�><img src=$imagesurl/images/del.gif border=0 width=16 align=absmiddle>ɾ��</a>��~; } else { $delgraphic = ""; }
    $delgraphic .=qq(<input type="checkbox" name="postno$editpostnumber" value="yes">) if((($mymembercode eq "ad")||($mymembercode eq 'smo')||($myinmembmod eq "yes"))&&($treeview ne "yes"));

    if ((($mymembercode eq "ad")||($mymembercode eq "mo")||($mymembercode eq 'smo')||(($myinmembmod eq "yes")&&($mymembercode ne 'amo')))&&($membercode{$membername} ne "ad")&&($tempname ne "")&&($membername ne "����")) { $rateuser = qq~ <a href="userrating.cgi?membername=$tempname&oldforum=$inforum&oldtopic=$intopic&oldpostno=$editpostnumber" title=�����û��������������><img src=$imagesurl/images/poll1.gif border=0 width=16 height=14></a>~; } else { $rateuser=""; }

    ($ip1,$ip2,$ip3,$ip4) = split(/\./,$postipaddress);

    if ($mymembercode eq "ad") {
	$postipaddress=qq~<span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$postipaddress',420,320)" title="LB WHOIS��Ϣ">$postipaddress</span>~;
    }
    elsif ($mymembercode eq "smo") {
	if ($smocanseeip eq "no") { $postipaddress=qq~<span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$postipaddress',420,320)" title="LB WHOIS��Ϣ">$postipaddress</span>~; }
	else {
       	    if ($pvtip eq "on") { $postipaddress=qq~<span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$postipaddress',420,320)" title="LB WHOIS��Ϣ">$postipaddress</a>~; }
       	    else { $postipaddress="�����ñ���"; }
	}
    }
    elsif ($myinmembmod eq "yes") {
	if ($pvtip eq "on") { $postipaddress="$ip1.$ip2.$ip3.*"; } else { $postipaddress="�����ñ���"; }
    }
    else {
	if (($pvtip eq "on")&&($inmembername ne "����")) { $postipaddress="$ip1.$ip2.*.*"; } else { $postipaddress="�����ñ���"; }
    }

    if ($proxyip ne 1) { if ($mymembercode eq "ad") { $fromproxy ="��ʵ IP�� $truepostipaddress"; } else { $fromproxy = "�� IP Ϊ���������"; } } else { $fromproxy=""; }

    $editgraphic = "" if (($usereditpost eq "no")&&($mymembercode ne "ad")&&($mymembercode ne 'smo')&&($myinmembmod ne "yes"));
    $useravatar  = "" if ($nodispavatar eq "yes");
    $delgraphic  = "" if ($editpostnumber == 1);

    $output .= qq~<a name=$editpostnumber><table cellpadding=0 cellspacing=0 width=$tablewidth align=center><tr><td bgcolor=$tablebordercolor width=1 height=24></td><td bgcolor=$postbackcolor>~;

    $replycounter = $postcountnumber + $instart; 
    if ($instart < $maxtopics) {$replycounter = $replycounter - 1;} 
    if ($editpostnumber eq $endarraytemp) { $output .= qq~<a name="bottom"></a>~; }
    if ($onlinetimehour{$membername} >= 1000) { my $onlinetime1 = $onlinetimehour{$membername}; $onlinetime = int($onlinetime1/24); $onlinetime1 = $onlinetime1 - $onlinetime * 24; $onlinetime = "$onlinetime��$onlinetime1ʱ$onlinetimemin{$membername}��$onlinetimesec{$membername}��"; }
                                         else { $onlinetime = "$onlinetimehour{$membername} ʱ $onlinetimemin{$membername} �� $onlinetimesec{$membername} ��"; }
    if ($editpostnumber eq 1) { $louceng =qq~<b>[<a onclick="ResetReplyTitle('$editpostnumber');" href="#sub" title="�������ûظ�����"><FONT COLOR=$fonthighlight>¥ ��</font></a>]~; $topicsthad = $maintopicad;} else { $louceng = qq~<b>[�� <a onclick="ResetReplyTitle('$editpostnumber');" href="#sub" title="�������ûظ�����"><FONT COLOR=$fonthighlight>$editpostnumber</FONT></a> ¥]~;  $topicsthad = $replytopicad;}

        $topicsthad = &HTML("$topicsthad");
        $topicsthad =~ s/\$imagesurl/$imagesurl/isg;
	$topicsthad =~ s/\[br\]/\n/isg;

$profilegraphic{$membername} =~ s/profile.cgi\?action=show&member=([^\"\+\ ]+?)([\ \'\"\>])/profile-$1.htm$2/isg if ($usefake eq "yes");

    $lastgone{$membername} = "δ֪" if ($lastgone{$membername} eq "");
    $topicsthad = "$topicsthad<BR>" if ($topicsthad ne "");
    $output .= qq~<table width=100% cellpadding=0 cellspacing=8 bgcolor=$postbackcolor>
<tr><td valign=top width=168 rowspan=5>
<table style="filter:glow(color=$glowing{$membername},direction=135)">&nbsp;<font color=$posterfontcolor{$membername}><b>$membername{$membername}&nbsp;</b></table>
<font color=$postfontcolortwo>$membertitle{$membername}
$showawards{$membername}
<font color=$postfontcolorone>$jhmp{$membername}
$useravatar{$membername}
<br><a href=lookinfo.cgi?action=style target=_blank title="$mtitle{$membername}">$membergraphic{$membername}</a>
<br><font color=$postfontcolorone>�ȼ�: <a href=lookinfo.cgi?action=style target=_blank title="�鿴������Ϣ"><font color=$fonthighlight>$mtitle{$membername}</a>
<BR><font color=$postfontcolortwo>��Ϣ: $online $membernameimg{$membername} $seximages{$membername} $showsx{$membername} $showxz{$membername}
<br><font color=$fonthighlight>����: $rating{$membername}������: $jifen{$membername}$rateuser
<br><font color=$postfontcolortwo>�ֽ�: $mymoney{$membername}
<br><font color=$postfontcolorone>���: $mysaves{$membername}
<br><font color=$postfontcolortwo>����: $myloan{$membername}
<br><font color=$postfontcolorone>����: $location{$membername}$userflag{$membername}
<br><font color=$postfontcolortwo>����: <b>$numberofposts{$membername}</b> ƪ
<br><font color=$postfontcolorone>����: <b><font color=$fonthighlight>$jhcount{$membername}</font></b> ƪ
~;
$output .= qq~<br><font color=$postfontcolortwo>����: $soccerinfo{$membername}~ if (-e "${lbdir}soccer.cgi" && $soccerinfo{$membername} ne "");
$output .= qq~<br><font color=$postfontcolorone>����: $emailgraphic{$membername}$homepagegraphic{$membername}$oicqgraphic{$membername}$icqgraphic{$membername}~ if ($emailgraphic{$membername} ne "" || $homepagegraphic{$membername} ne "" || $oicqgraphic{$membername} ne "" || $icqgraphic{$membername} ne "");
$output .= qq~
<br><font color=$postfontcolortwo>����: $onlinetime
<br><font color=$postfontcolorone>ע��: $joineddate{$membername}
<br><font color=$postfontcolortwo>���: $lastgone{$membername}<br>
</td>
<td width=1 height=100% rowspan=5 bgcolor=$titlecolor></td>
<td valign=top width=600>$pvmsggraphic{$membername}$profilegraphic{$membername}$searchgraphic{$membername}$friendgraphic{$membername}$copygfx$replygraphic$replynow$postmanbuttom$chgposticon</td><td align=right>$louceng</td>
</tr>
<tr><td colspan=2 height=1 bgcolor=$tablebordercolor></td></tr>
<tr><td colspan=2 valign=top>
<table cellspacing=0 cellpadding=0 width=100% style=TABLE-LAYOUT:fixed height=$vheight{$membername}>
<tr><td width=32 valign=top>$posticon&nbsp;</td><td style="WORD-WRAP:break-word;$paraspace;$wordspace\pt" valign=top>$topicsthad<span id=post$editpostnumber style=color:$postfontcolor;font-size:${postfontsize}px>$addme$post</span><BR></td></tr>
<tr><td colspan=2 height=22 valign=bottom>$addads<BR></td></tr>
</table>
</td></tr>
<tr><td colspan=2 height=1 bgcolor=$tablebordercolor></td></tr>
<tr><td><font color=$postfontcolor>$editgraphic$pbgraphic$delgraphic<img src=$imagesurl/images/posttime.gif width=16 alt=����ʱ�� align=absmiddle>$postdate��<img src=$imagesurl/images/ip.gif width=13 alt="$fromproxy" align=absmiddle>IP: $postipaddress</td><td align=right valign=bottom width=20%>[���Ĺ�$postsize�ֽ�]��<a href=#top><img src=$imagesurl/images/p_up.gif height=17 border=0 align=absmiddle title=���ض���></a>&nbsp;</td>
</tr></table></td><td bgcolor=$tablebordercolor width=1></td></tr></table>
<table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td height=1></td></tr></table>
~;
    $editpostnumber++; $postcountnumber++;
    $rn++;
}

if ($treeview eq "yes") {
    require "treeviewoutput.pl";
}

$output .= qq~<SCRIPT>valignend()</SCRIPT><img src=$imagesurl/images/none.gif height=3 width=0><BR><table cellpadding=0 cellspacing=2 width=$tablewidth align=center><tr bgcolor=$menubackground height=4></tr><tr><td><font color=$menufontcolor>&nbsp;$pages</td>~;

if (($indexforum ne "no")&&($dispjump ne "no")) {
    require "${lbdir}data/forumjump.pl" if (-e "${lbdir}data/forumjump.pl");
    $jumphtml =~ s/\<\!\-\-h (.+?) \-\-\>/$1/isg if (($disphideboard eq "yes")||($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "mo")||($membercode eq "amo"));
    $jumphtml =~ s/\<\!\-\-c (.+?) \-\-\>/$1/isg if ($dispchildjump ne "no");

    if ($usefake eq "yes") {

	$jumphtml =~ s/forums.cgi\?forum=([0-9]+?)&show=([0-9]+?)([\ \'\"\>])/forums-$1-$2.htm$3/isg;
	$jumphtml =~ s/forums.cgi\?forum=([0-9]+?)([\ \'\"\>])/forums-$1-0.htm$2/isg;

	$jumphtml =~ s/leobbs.cgi\?action=(.+?)([\ \'\"\>])/=leobbs-$1.htm$2/isg;
	$jumphtml =~ s/([\=\'\"\/])leobbs.cgi/${1}leobbs.htm/isg;

    }
    $output .= qq~<td align=right nowrap>$jumphtml</td></form>~;
}
$output .= qq~</tr></table><br>~;

if (($threadstate ne "closed")&&($threadstate ne "pollclosed")&&($postopen ne "no")&&($dispquickreply ne "no")) { require "fastreplay.pl"; }

$output .= qq~<table cellspacing=0 cellpadding=0 width=$tablewidth align=center>
<tr><td>&nbsp;<a href=#top><img src=$imagesurl/images/gotop.gif width=15 border=0 align=absmiddle>����</a>��<a href=fav.cgi?action=add&forum=$inforum&topic=$intopic><img src=$imagesurl/images/addfavorite.gif height=15 border=0 align=absmiddle>�ӵ�"�����ղؼ�"</a></td><td nowrap align=right><font color=$menufontcolor><img src=$imagesurl/images/forumme.gif> <b>�������</B>��
<a href=postings.cgi?action=abslocktop&forum=$inforum&topic=$intopic>�̶ܹ�</a> <img src=$imagesurl/images/fg.gif>
<a href=postings.cgi?action=absunlocktop&forum=$inforum&topic=$intopic>ȡ���̶ܹ�</a> <img src=$imagesurl/images/fg.gif>
<a href=postings.cgi?action=catlocktop&forum=$inforum&topic=$intopic>���̶�</a> <img src=$imagesurl/images/fg.gif>
<a href=postings.cgi?action=catunlocktop&forum=$inforum&topic=$intopic>ȡ�����̶�</a> <img src=$imagesurl/images/fg.gif>
<a href=postings.cgi?action=locktop&forum=$inforum&topic=$intopic>�̶�</a> <img src=$imagesurl/images/fg.gif>
<a href=postings.cgi?action=unlocktop&forum=$inforum&topic=$intopic>ȡ���̶�</a> <img src=$imagesurl/images/fg.gif>
<a href=postings.cgi?action=puttop&forum=$inforum&topic=$intopic>����</a> <img src=$imagesurl/images/fg.gif>
<a href=postings.cgi?action=putdown&forum=$inforum&topic=$intopic>����</a> <img src=$imagesurl/images/fg.gif>
<BR>
<a href=postings.cgi?action=highlight&forum=$inforum&topic=$intopic>����</a> <img src=$imagesurl/images/fg.gif>
<a href=postings.cgi?action=lowlight&forum=$inforum&topic=$intopic>ȡ������</a> <img src=$imagesurl/images/fg.gif>
<a href=jinghua.cgi?action=add&forum=$inforum&topic=$intopic>����</a> <img src=$imagesurl/images/fg.gif>
<a href=jinghua.cgi?action=del&forum=$inforum&topic=$intopic>ȡ������</a> <img src=$imagesurl/images/fg.gif>
<a href=postings.cgi?action=lock&forum=$inforum&topic=$intopic>����</a> <img src=$imagesurl/images/fg.gif>
<a href=postings.cgi?action=unlock&forum=$inforum&topic=$intopic>����</a> <img src=$imagesurl/images/fg.gif>
<a href=delpost.cgi?action=delete&forum=$inforum&topic=$intopic>ɾ��</a> <img src=$imagesurl/images/fg.gif>
<span style=cursor:hand onClick="javascript:DelReply();">ɾ���ظ�</span> <img src=$imagesurl/images/fg.gif> 
<a href=delpost.cgi?action=movetopic&forum=$inforum&topic=$intopic>�ƶ�</a> <img src=$imagesurl/images/fg.gif>
</td></tr></table><p><p>
<form action="delpost.cgi" method=post name="DReply"> 
<input type=hidden name="forum" value="$inforum"> 
<input type=hidden name="topic" value="$intopic"> 
<input type=hidden name="action" value="directdel"> 
<input type=hidden name="postno"></form>
~;
if (($useads ne "no")&&(-e "${imagesdir}leogg.js")) {
    $output .= qq~<SCRIPT src=$imagesurl/leogg.js></SCRIPT>~;
}

&output("$topictitletemp @ $forumname",\$output);
exit;
