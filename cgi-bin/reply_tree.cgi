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
$LBCGI::POST_MAX=100000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;

require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "reply_tree.cgi";
$query = new LBCGI;
#Cookie ·��
if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
	$boardurltemp =$boardurl;
	$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
	$cookiepath = $boardurltemp;
	$cookiepath =~ s/\/$//;
#	$cookiepath =~ tr/A-Z/a-z/;
}

#ȡ����̳��������
$inforum			= int($query -> param('forum'));
$intopic			= int($query -> param('topic'));
$instart			= int($query -> param('start'));
&ERROROUT("�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum !~ /^[0-9]+$/)||($intopic !~ /^[0-9]+$/)||($instart !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

$screenmode = $query->cookie("screenmode");
$screenmode = 8 if ($screenmode eq "");
$addtimes = ($timedifferencevalue + $timezone)*3600;

#ȡ�����} ID
$id_of_this_topid	= sprintf("%04d%05d",$inforum,$intopic);
#�û�����
$inmembername	= $query->cookie("amembernamecookie");
$inpassword 	= $query->cookie("apasswordcookie");
$userregistered	= "no";
&ERROROUT("�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));
unless ((!$inmembername) or ($inmembername eq "����")) { 
	&getmember("$inmembername","no");
	$mymembercode=$membercode;
	$myrating=$rating;
	&ERROROUT("�������û���������������µ�¼��") if ($inpassword ne $password);
}
&ERROROUT("��Աר�ù��ܣ����ȵ�¼��") if ($userregistered eq "no");
#ȡ�÷���̳����
&getoneforum("$inforum");
$myinmembmod = $inmembmod;
$testentry = cookie("forumsallowed$inforum");
if (((($testentry ne $forumpass)||($testentry eq ""))&&($privateforum eq "yes"))||(($startnewthreads eq "cert")&&($membercode eq "me")&&($userincert eq "no"))) {
	&ERROROUT("�㲻����������̳��") if(($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes"));
}

&error("������̳&�����̳��û��Ȩ�޽�����̳��") if ($yxz ne '' && $yxz!~/,$membercode,/);
if ($allowusers ne ''){
    &ERROROUT("�㲻����������̳��") if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}

if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &ERROROUT("�㲻����������̳���������Ϊ $rating��������ֻ̳���������ڵ��� $enterminweiwang �Ĳ��ܽ��룡") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0 ) {
	require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
	$mymoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	&ERROROUT("�㲻����������̳����Ľ�ǮΪ $mymoney��������ֻ̳�н�Ǯ���ڵ��� $enterminmony �Ĳ��ܽ��룡") if ($enterminmony > 0 && $mymoney < $enterminmony);
	&ERROROUT("�㲻����������̳����Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $enterminjf �Ĳ��ܽ��룡") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

#��ʼ�����ݣ��ظ���
my($OUTPUT_TABLE,$REPLY_COUNT);
$addtimes = ($timedifferencevalue + $timezone)*3600;
#��ȡ����
$file_of_this_topic = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
open(FILE, "$file_of_this_topic") or &ERROROUT("������ⲻ���ڣ������Ѿ���ɾ����");
@threads = <FILE>;
close(FILE);

(my $membername1, my $topictitle1, my $postipaddresstemp1, my $showemoticons1, my $showsignature1, my $postdate1, my $post1, my $posticon1) = split(/\t/, $threads[0]);

    if ($jfmark eq "yes") {
	if ($post1 =~m/\[jf=(.+?)\](.+?)\[\/jf\]/isg){ 
	    $jfpost=$1;
	    if (($jfpost <= $jifen)||($mymembercode eq "ad")||($mymembercode eq "smo")||($myinmembmod eq "yes")||(lc($membername) eq lc($inmembername))){ 
	    } else { 
	    &ERROROUT("���������������л��ֱ�ǩ�������޷����ٲ鿴��������鿴������лл��") if ($noviewjf eq "yes");
   	    }
   	}
    }


shift(@threads);


@threads = reverse(@threads);
chomp @threads;
#ȡ����������
$TREPLY_COUNT = @threads;
$REPLY_COUNT = $TREPLY_COUNT+1;
my $numberofitems = $TREPLY_COUNT;
#ȡ����������
&ERROROUT("������û���κλظ���") unless(@threads);

if ($tablewidth > 100) {
    if ($tablewidth > 1000) { $topictitlemax = 85; } elsif ($tablewidth > 770) { $topictitlemax = 70; } else { $topictitlemax = 40; }
} else {
    if ($screenmode >=10) { $topictitlemax = 85; } elsif ($screenmode >=8) { $topictitlemax = 70; } else { $topictitlemax = 40; }
}

#��ҳ//add by hztz
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
	my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<font face=webdings><span style=cursor:hand title="�� ҳ" onclick="loadThreadFollows($inforum, \\\'$intopic&start=0\\\')">9</span></font>~;
	my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<font face=webdings><span style=cursor:hand title="β ҳ" onclick="loadThreadFollows($inforum, \\\'$intopic&start=$endstart\\\')">:</span></font>~;

	my $uppage = $currentpage - 1;
	my $nextpage = $currentpage + 1;
	my $upstart = $instart - $maxtopics;
	my $nextstart = $instart + $maxtopics;
	my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<font face=webdings><span style=cursor:hand title="��$uppageҳ" onclick="loadThreadFollows($inforum, \\\'$intopic&start=$upstart\\\')">7</span></font>~;
	my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<font face=webdings><span style=cursor:hand title="��$nextpageҳ" onclick="loadThreadFollows($inforum, \\\'$intopic&start=$nextstart\\\')">8</span></font>~;

	my $tempstep = $currentpage / 7;
	my $currentstep = int($tempstep);
	$currentstep++ if ($currentstep != $tempstep);
	my $upsteppage = ($currentstep - 1) * 7;
	my $nextsteppage = $currentstep * 7 + 1;
	my $upstepstart = ($upsteppage - 1) * $maxtopics;
	my $nextstepstart = ($nextsteppage - 1) * $maxtopics;
	my $showupstep = $upsteppage < 1 ? "" : qq~<span style=cursor:hand title="��$upsteppageҳ" onclick="loadThreadFollows($inforum, \\\'$intopic&start=$upstepstart\\\')">��</span> ~;
	my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<span style=cursor:hand title="��$nextsteppageҳ" onclick="loadThreadFollows($inforum, \\\'$intopic&start=$nextstepstart\\\')">��</span> ~;

	$pages = "";
	my $currentstart = $upstepstart + $maxtopics;
	for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++)
	{
		last if ($i > $numberofpages);
		$pages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<span style=cursor:hand onclick="loadThreadFollows($inforum, \\\'$intopic&start=$currentstart\\\')">$i</span> ~;
		$currentstart += $maxtopics;
	}
	$pages = "<font color=$menufontcolor>ҳ�Σ�<b><font color=$fonthighlight>$currentpage</font> / $numberofpagesҳ</b> ÿҳ��� <font color=$fonthighlight>$maxtopics</font> �� �� <font color=$fonthighlight>$numberofitems</font> �� $beginpage $showup \[ $showupstep$pages$shownextstep\] $shownext $endpage</font>";
}
else {
	$startarray = 0;
	$endarray = $numberofitems - 1;
	$pages = "<font color=$menufontcolor>������Ļظ�ֻ��һҳ</font>";
}

$REPLY_COUNT = $REPLY_COUNT - $startarray;
#ȡ���������
foreach (@threads[$startarray .. $endarray]){
	my @postdata = split(/\t/,$_);
	#���»ظ���
	$REPLY_COUNT--;
	$OUTPUT_TABLE .= &OUTPUT_TABLE($postdata[0], $postdata[5], $postdata[6], $postdata[7]);
}
	$OUTPUT_TABLE .= qq(<br><br><DIV style="BORDER-RIGHT: black 1px solid; PADDING-RIGHT: 2px; BORDER-TOP: black 1px solid; PADDING-LEFT: 2px; PADDING-BOTTOM: 2px; MARGIN-LEFT: 18px; BORDER-LEFT: black 1px solid; WIDTH: 600px; COLOR: black; PADDING-TOP: 2px; BORDER-BOTTOM: black 1px solid; BACKGROUND-COLOR: lightyellow;text-align:center">[ $pages ]</DIV>);
OUTPUT_TREE($boardname,$OUTPUT_TABLE,0);


#�����ʾ
sub OUTPUT_TABLE{
	#ȡ�����ݣ��ظ���
	my ($OUTPUT_NAME, $OUTPUT_TIME, $OUTPUT_MSG, $OUTPUT_ICON) = @_;
	#������������
        $OUTPUT_TIME = &dateformat($OUTPUT_TIME + $addtimes);

    $OUTPUT_MSG =~ s/\[ADMINOPE=(.+?)\]//isg;
	if ($OUTPUT_MSG =~ /\[POSTISDELETE=(.+?)\]/) {
	    $OUTPUT_MSG = "�˻ظ��Ѿ�������";
	}

        if (($OUTPUT_MSG =~ /LBHIDDEN\[(.*?)\]LBHIDDEN/)||($OUTPUT_MSG =~ /LBSALE\[(.*?)\]LBSALE/)) {
            $OUTPUT_MSG = "����";
        } else {
	    $OUTPUT_MSG =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	    $OUTPUT_MSG =~ s/\[quote\](.*)\[\/quote\]//isg;
	    $OUTPUT_MSG =~ s/\[equote\](.*)\[\/equote\]//isg;
	    $OUTPUT_MSG =~ s/\[fquote\](.*)\[\/fquote\]//isg;
	    $OUTPUT_MSG =~ s/\[hidepoll\]//isg;
	    $OUTPUT_MSG =~ s/\[���(.+?)�����(.+?)�༭\]\n//isg;
	    $OUTPUT_MSG =~ s/\[hide\](.*)\[hide\](.*)\[\/hide](.*)\[\/hide\]//isg; 
	    $OUTPUT_MSG =~ s/\[hide\](.*)\[\/hide\]//isg; 
	    $OUTPUT_MSG =~ s/\[post=(.+?)\](.+?)\[\/post\](.*)\[post=(.+?)\](.+?)\[\/post\]//isg; 
	    $OUTPUT_MSG =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg; 
	    $OUTPUT_MSG =~ s/\[jf=(.+?)\](.+?)\[\/jf\](.*)\[jf=(.+?)\](.+?)\[\/jf\]//isg; 
	    $OUTPUT_MSG =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg; 
	    $OUTPUT_MSG = &temppost("$OUTPUT_MSG");
	}
	
	if (length($OUTPUT_MSG)>=$topictitlemax) {
            $OUTPUT_MSG=&lbhz($OUTPUT_MSG,$topictitlemax);
	}

	$OUTPUT_MSG = "(������)" unless($OUTPUT_MSG ne "");
	#��ʼ���������
	my $OUTPUT_TABLE;
	#��������ֵ
	my $START=0;my $SID=$REPLY_COUNT+1;
	if($REPLY_COUNT >= $maxtopics){
		my ($crelyid,undef)=split(/\./,($REPLY_COUNT/$maxtopics));
		$START=$crelyid*$maxtopics;
	}
	$SID="bottom" if($SID eq $TREPLY_COUNT+1);
	if (($OUTPUT_ICON eq "")||($OUTPUT_ICON =~ /\<br\>/i)) {
	    $OUTPUT_ICON = int(myrand(23));
    	    $OUTPUT_ICON = "0$OUTPUT_ICON" if ($OUTPUT_ICON<10);
	    $OUTPUT_ICON = "$OUTPUT_ICON.gif";
	}
	$OUTPUT_ICON = qq~<img src=$imagesurl/posticons/$OUTPUT_ICON $defaultsmilewidth $defaultsmileheight>~;

	#������ݱ��
	$REPLY_COUNT1 = $REPLY_COUNT+1;
	$OUTPUT_TABLE .= qq~<span style=width:100%><span style=width:58%>��������$OUTPUT_ICON��<a href=topic.cgi?forum=$inforum&topic=$intopic&start=$START#$SID target=_blank>$OUTPUT_MSG</a></span><span style=width:12%><a href=post.cgi?action=replyquote&forum=$inforum&topic=$intopic&postno=$REPLY_COUNT1 title=���ûظ�������� target=_blank><img src=$imagesurl/images/replynow.gif border=0 width=16 align=absmiddle></a></span><span style="width:14%">[ <span style="cursor:hand" onClick="javascript:O9('~ . ($uri_escape eq "no" ? $OUTPUT_NAME : uri_escape($OUTPUT_NAME)) . qq~')">$OUTPUT_NAME</span> ]</span><span style=width:14%>$OUTPUT_TIME</span>~;
	#�����������
	$OUTPUT_TABLE =~ s/\n//g;
	$OUTPUT_TABLE =~ s/\'/\\\'/g;
	return "$OUTPUT_TABLE";
}

sub ERROROUT{
	my $ERROR_MSG = shift;
	my $OUTPUT_TABLE;
	$OUTPUT_TABLE .= qq(<DIV style="BORDER-RIGHT: black 1px solid; PADDING-RIGHT: 2px; BORDER-TOP: black 1px solid; PADDING-LEFT: 2px; PADDING-BOTTOM: 2px; MARGIN-LEFT: 18px; BORDER-LEFT: black 1px solid; WIDTH: 240px; COLOR: black; PADDING-TOP: 2px; BORDER-BOTTOM: black 1px solid; BACKGROUND-COLOR: lightyellow;cursor:hand" onclick="loadThreadFollow($inforum,$intopic,'$id_of_this_topid')">$ERROR_MSG</DIV>);
	$OUTPUT_TABLE =~ s/\n//g;
	$OUTPUT_TABLE =~ s/\'/\\\'/g;
	&OUTPUT_TREE($boardname,$OUTPUT_TABLE,1);
}

sub OUTPUT_TREE{
	my ($title,$output,$err) = @_;
	chomp $output;

	print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

print <<"HTML";
<html>
<head> 
<title>������</title>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
</head>
<body>
<SCRIPT>
<!--
//��ʼ������ֵ
parent.followTd$id_of_this_topid.innerHTML='$output';
//�Ѷ�ȡ
parent.document.images.followImg$id_of_this_topid.loaded='yes';
-->
</SCRIPT>
</body>
</html>
HTML
		
	exit;
}