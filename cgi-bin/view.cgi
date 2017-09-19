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
use VISITFORUM qw(getlastvisit setlastvisit);
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "view.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else
{
	$boardurltemp = $boardurl;
	$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
	$cookiepath = $boardurltemp;
	$cookiepath =~ s/\/$//;
}

$inforum = $query->param("forum");
$intopic = $query->param("topic");
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($inforum !~ /^[0-9]+$/);
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($intopic !~ /^[0-9]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

&error("��ͨ����&�Բ��𣬱���̳���������ŷ�ʽ�����Ķ���") if ($canuseview eq "no");

$inmembername = $query->cookie("amembernamecookie");
$inpassword = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
&ipbanned;

if ($useadscript ne 0) {
    $adscript = &HTML("$adscript");
    $adscript =~ s/\$imagesurl/$imagesurl/isg;
    $adscript =~ s/\[br\]/\n/isg;
}
else { $adscript =""; }

if ($useadfoot ne 0) {
$adfoot   = &HTML("$adfoot");
$adfoot   =~ s/\[br\]/\n/isg;
$adfoot   =~ s/\$imagesurl/$imagesurl/isg;
}
else { $adfoot =""; }

$nodisp = $query->cookie("nodisp");
(undef, undef, $nodispphoto) = split(/\|/, $nodisp);

$banfresh1 = $query->cookie("banfresh");
$banfresh1 = 0 if ($banfresh1 eq "");
($backtopic, $banfresh) = split(/=/, $banfresh1);
$currenttime = time;
$banfreshcookie = cookie(-name=>"banfresh", -value=>"$intopic=$currenttime", -path=>"$cookiepath/");

if ($currenttime - $banfresh - 1 <= $banfreshtime && $backtopic eq $intopic)
{
	print header(-cookie=>[$banfreshcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
	print "������æ���� $banfreshtime ���ˢ�¼�������<br><br>";
	print "����ԭ����ˢ��ҳ����죬��������˹��ര�����������վ��";
	exit;
}

&getoneforum($inforum);

if ($inmembername eq "" or $inmembername eq "����")
{
	$inmembername = "����";
	$myrating = -1;
	$mymembercode = "no";
    &error("��ͨ����&���˲��ܲ鿴�������ݣ���ע����¼������") if ($guestregistered eq "off");
}
else
{
	&getmember($inmembername,"no");
	&error("��ͨ����&�û�û�е�¼��ע�ᣡ") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
	$mymembercode = $membercode;
	$myinmembmod = $inmembmod;
	$myrating = $rating;
	$tempaccess = "forumsallowed" . $inforum;
	$testentry = $query->cookie($tempaccess);
	$allowed = $allowedentry{$inforum} eq "yes" || ($testentry eq $forumpass && $testentry ne "") || $mymembercode eq "ad" || $mymembercode eq "smo" || $myinmembmod eq "yes" ? "yes" : "no";
	&getlastvisit;
	$forumlastvisit = $lastvisitinfo{$inforum};
	&setlastvisit("$inforum,$currenttime");
}
&doonoff;  #��̳�������

$addtimes = ($timedifferencevalue + $timezone) * 3600;

&error("�����Ա��̳�鿴��������&���ǿ���û��Ȩ�޽���!") if ($inmembername eq "����" && $regaccess eq "on" && &checksearchbot);
&error("����˽����̳&�Բ�����û��Ȩ�޽����˽����̳��") if ($privateforum eq "yes" && $allowed ne "yes");
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

print header(-cookie=>[$tempvisitcookie, $permvisitcookie, $banfreshcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&error("������&������ⲻ���ڣ������Ѿ���ɾ����") unless (-e "${lbdir}forum${inforum}/${intopic}.thd.cgi");

opendir(DIR2, "${imagesdir}$usrdir/$inforum");
my @dirdata2 = readdir(DIR2);
closedir(DIR2);
my @files11 = grep(/^$inforum\_$intopic\_/, @dirdata2);

open(FILE, "${lbdir}forum${inforum}/${intopic}.thd.cgi");
@threads = <FILE>;
close(FILE);

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

if ($mymembercode eq "ad" || $mymembercode eq "smo" || $myinmembmod eq "yes")
{
	$viewhide = 1;
}
else
{
	$viewhide = 0;
	if ($hidejf eq "yes" )
	{
		my @viewhide = grep(/^$inmembername\t/i, @threads);
		$viewhide = @viewhide;
		$viewhide = 1 if ($viewhide > 1);
	}
}
$StartCheck = $numberofposts + $numberofreplys;

($membername, $topictitle, $postipaddresstemp, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/, $threads[0]);

    if (($inmembername eq "" || $inmembername eq "����")&&($waterwhenguest eq "yes")){
	$post="\[watermark]\n$post\[\/watermark]";
    }

$topictitle =~ s/^����������//;

	if ($addtopictime eq "yes") {
	    my $topictime = &dispdate($postdate + $addtimes);
	    $topictitle = "[$topictime] $topictitle";
	}
	
$postdate = &dateformat($postdate + $addtimes);
&getmember($membername,"no");
$inmembmod = $forummodnamestemp =~ /\Q,$membername,\E/i ? "yes" : "no";
          	       
if ((($post =~ /(\&\#35\;|#)Moderation Mode/i) && ($membercode eq 'mo' ||$membercode eq 'amo'||$membercode eq 'cmo'|| $membercode eq 'ad' || $membercode eq 'smo')) || $htmlstate eq 'on') {
        $post =~ s/(\&\#35\;|#)Moderation Mode/***** ����ģʽ *****\<BR\>/g;
        $post =~ s/&lt;/</g; $post =~ s/&gt;/>/g; $post =~ s/\&\#35\;/\#/g; $post =~ s/&quot;/\"/g; $post =~ s/( |\>)<br>/$1\n/sg; $post =~ s/( |\>)<p>/$1\n\n/sg;
} else { $post =~ s/style/\&\#115\;tyle/isg; }

$addmefile = 0;
my @files2 = grep(/^$inforum\_$intopic\./, @dirdata2);
if (@files2 > 0)
{
	my $files2s = $files2[0];
	($up_name, $up_ext) = split(/\./, $files2s);
	$up_ext =~ tr/A-Z/a-z/;
	$addmefile = 1;
}
undef @dirdata2;

if ($addmefile == 1)
{
	@fileinfo = stat("${imagesdir}$usrdir/${inforum}/${up_name}.${up_ext}");
	$filetype = "unknow";
	$filetype = $up_ext if (-e "${imagesdir}icon/${up_ext}.gif");
	if ($up_ext eq "gif" || $up_ext eq "jpg" || $up_ext eq "png" || $up_ext eq "bmp")
	{
		if ($nodispphoto eq "yes" || $arrawpostpic eq "off")
		{
			$addme = qq~<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=1&type=.$up_ext target=_blank><img src=$imagesurl/icon/$filetype.gif border=0 width=16></a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=1&type=.$up_ext target=_blank>�����ʾ���������ͼƬ</a><br><br>~;
		}
		else
		{
			$addme = qq~<img src=$imagesurl/icon/$filetype.gif border=0 width=16> ���������ͼƬ���£�<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=1&type=.$up_ext target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=1&type=.$up_ext border=0 alt="�������´������ͼƬ" onload="javascript: if(this.width > document.body.clientWidth - 333) this.width = document.body.clientWidth - 333" onmousewheel="return bbimg(this)"></a><br><br>~;
		}
	        $addme .= qq(<img src=$imagesurl/images/none.gif whidth=0 height=5><BR><span style=CURSOR:hand onclick=loadThreadFollow($forumid,$topicid,1,'$up_ext')><img id=followImg1 src=$imagesurl/images/cat.gif width=9 loaded=no nofollow="cat.gif" valign=absmiddle> ���˲鿴ͼƬ��ϸ��Ϣ<table cellpadding=0 class=ts1 cellspacing=0 width=50% id=follow1 style=DISPLAY:none><tr><td id=followTd1><DIV class=ts onclick=loadThreadFollow($forumid,$topicid,1,'$up_ext')>���ڶ�ȡ��ͼƬ����ϸ��Ϣ�����Ժ� ...</DIV></td></tr></table></span><BR><BR>);
	}
	elsif ($up_ext eq "swf")
	{
		if ($arrawpostflash eq "on")
		{
			$addme = qq~<img src=$imagesurl/icon/$filetype.gif border=0 width=16> ��������һ�� $up_ext ��ʽ Flash ���� (�� $fileinfo[7] �ֽ�)<br><br><param name=play value=true><param name=loop value=true><param name=quality value=high><embed src=attachment.cgi?forum=$inforum&topic=$intopic&postno=1&type=.$up_ext quality=high width=410 height=280 pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application/x-shockwave-flash"></embed><br>&nbsp;<img src=$imagesurl/images/fav.gif width=16> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=1&type=.$up_ext target=_blank>ȫ���ۿ�</a> (���Ҽ�����)<br><br>~;
		}
		else
		{
			$addme = qq~<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=1&type=.$up_ext target=_blank><img src=$imagesurl/icon/$filetype.gif border=0 width=16 height=16>������� Flash ����</a>~;
		}
	}
	else
	{
		$addme = qq~<font color=$fonthighlight>��ظ���</font>��<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=1&type=.$up_ext target=_blank><img src=$imagesurl/icon/$filetype.gif border=0 width=16 alt="��������һ����$filetype�����͸������������"></a> (�� $fileinfo[7] �ֽ�)<br><br>~;		
	}
}
else
{
	$addme = "";
}
if ($membercode eq "masked") {
    $addme = "";
    $post = qq(<br>------------------------<br><font color=$posternamecolor>���û��ķ����Ѿ������Σ�<br>�������ʣ�����ϵ����Ա��</font><br>------------------------<BR>);
}

$PollHidden = $post =~ m/\[hidepoll\]/isg ? "yes" : "no";
$post =~ s/\[hidepoll\]//isg;
$post =~ s/\[USECHGFONTE\]//isg;

if ($idmbcodestate eq "on")
{
	$rn = 0;
	&lbcode(\$post);
	if ($post =~/<blockquote><font face=����>����/isg)
	{
		$post =~ s/\&amp\;/\&/ig;
		$post =~ s/\&lt\;br\&gt\;/<br>/ig;
	}
}
else {
require "codeno.cgi";
&lbnocode(\$post);
$post =~ s/\[DISABLELBCODE\]//isg;
}
if ($emoticons eq "on" && $showemoticons eq "yes")
{
	&doemoticons(\$post);
	&smilecode(\$post);
}

$memberfilename = $membername;
$memberfilename =~ s/ /\_/g;
$memberfilename = uri_escape($memberfilename);
$homepage =~ s/^http\:\/\///isg;
$homepage = $homepage ne "" ? "http://$homepage" : "leobbs.cgi";
		
$posticon =~ s/\s//isg;
if ($posticon ne "")
{
	if ($posticon =~ /<br>/i && $postdelete ne "1")
	{
		$showsignature = "yes25" if ($showsignature eq "yes");
		$polltype = $showsignature =~ /^yes[0-9]+$/ ? "checkbox" : "radio";

		$posticon =~ s/<br><br>/<br>/isg;
		$posticon =~ s/<br>/\t/ig;
		my @temppoll = split(/\t/, $posticon);
		if ($#temppoll >= 1)
		{
			$maxpolllength = 0;
			@poll = split(/\t/, $posticon);
			unshift(@poll, "");
			$j = 0;
			$pollinput = "";
			for ($i = 1; $i <= $maxpollitem; $i++)
			{
				if ($poll[$i] ne "")
				{
					$j++;
					$pollinput .= qq~<input type=$polltype name=myChoice value="$i"> $poll[$i]<br>~;
					$maxpolllength = length($poll[$i]) if (length($poll[$i]) > $maxpolllength);
				}
			}
			$maxpolllength = $maxpolllength * 7 + 10;
			$maxpolllength = 150 if ($maxpolllength < 150);
			$maxpolllength = 510 if ($maxpolllength > 510);
			if ($showsignature =~ /^yes[0-9]+$/)
			{
				$showsignature =~ s/^yes//;
				$maxcanpoll = "����Ͷ $showsignature ��<br>";
			}

			$pollform = qq~<form action=poll.cgi method=POST>
<input type=hidden name=action value="poll"><input type=hidden name=forum value="$inforum"><input type=hidden name=threadname value="$intopic">
<table cellPadding=1 cellSpacing=0 width=$maxpolllength bgColor=$tablebordercolor><tr><td nowrap><table width=100% cellPadding=4 cellSpacing=0  bgColor=#f2f2f2>
<tr><td nowrap>$pollinput</td></tr>
<tr><td align=center nowrap><hr size=1 width=85%>$maxcanpoll<input type=submit name=results value="�μ�ͶƱ"></td></form></tr>
</table></td></tr></table>~;

			$showpoll = "";
			$pollnull = "";
			if ($mymembercode eq "ad" || $mymembercode eq "smo" || $myinmembmod eq "yes")
			{
				$adminview = 1;
				$maxpolllength = 550;
				$adminviewcolspan = 3;
			}
			else
			{
				$adminview = 0;
				$maxpolllength = 510;
				$adminviewcolspan = 2;
			}
			$poll = qq~<table width=$maxpolllength>~;
			if (open(FILE, "${lbdir}forum${inforum}/${intopic}.poll.cgi"))
			{
				@allpoll = <FILE>;
				close(FILE);
				$size = @allpoll;
			}
			else
			{
				$size = 0;
				@allpoll = ();
			}
			if ($size > 0)
			{
				$size = 0;
				@thispoll = ('0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0');
				@pollname = ('','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');

				foreach (@allpoll)
				{
					$_ =~ s/[\a\f\n\e\0\r]//isg;
					next if ($_ eq "");
					my ($tmpinmembername, $tmpmyChoice) = split(/\t/, $_);
					$tmpinmembername =~ s/^����������//isg;
					for ($i = 1; $i <= $j; $i++)
					{
						if ($i == $tmpmyChoice)
						{
							$thispoll[$i]++;
							$TheHigest=$thispoll[$i] if ($thispoll[$i] >= $TheHigest);
							$pollname[$i] = "$pollname[$i]$tmpinmembername\t";
							$size++;
						}
					}
					$showpoll = "true" if ($tmpinmembername eq $inmembername);
				}
				undef @allpoll;
			}
			if ($size > 0)
			{
				$poll .= $showsignature eq "yes" ? qq~<tr><td colspan=$adminviewcolspan><HR size=1 width=100%></td></tr><tr><td colspan=$adminviewcolspan>Ŀǰ�ܹ��� <font color=$fonthighlight><b>$size</b></font> ��ͶƱ��������£�<hr size=1 width=100%><br></td></tr>~ : qq~<tr><td colspan=$adminviewcolspan><hr size=1 width=100%></td></tr><tr><td colspan=$adminviewcolspan>Ŀǰ���� <font color=$fonthighlight><b>$size</b></font> �˲μ�ͶƱ��������£�<hr size=1 width=100%><br></td></tr>~;
				for ($i = 1; $i <= $j; $i++)
				{
					if ($poll[$i] ne "")
					{
						my $mypoll = int($thispoll[$i] / $size * 1000) / 10;
						my $width = int($mypoll / 100 * 160);
						if ($adminview == 1)
						{
							undef @pollmanname;
							$adminviewpoll = qq~</td><td nowarp><script language="JavaScript">function surfto(list) {var myindex1 = list.selectedIndex; var newwindow = list.options[myindex1].value; if (newwindow != "") {var msgwindow = window.open("profile.cgi?action=show&member=" + newwindow, "", "");}}</script><select OnChange="surfto(this);"><option>ͶƱ��������</option><option>----------</option>~;
							@pollmanname = split(/\t/, $pollname[$i]);
							$pollmanname = @pollmanname;
							foreach (@pollmanname)
							{
								my $tempname = uri_escape($_);
								$adminviewpoll .= qq~<option value="$tempname">$_ </option>~;
							}
							$adminviewpoll .= "</select>";
							$adminviewpoll = "</td><td nowarp>[û����ͶƱ]" if ($pollmanname eq 0);
						}
						else
						{
							undef $adminviewpoll;
						}
						$ii = $i;
						$ii = $ii - 40 if ($ii > 40);
						$ii = $ii - 30 if ($ii > 30);
						$ii = $ii - 20 if ($ii > 20);
						$ii = $ii - 10 if ($ii > 10);
						if ($thispoll[$i] >= $TheHigest)
						{
							$XA = "<font color=$fonthighlight><b><u>";
							$XB = "</u></b></font>";
						}
						else
						{
							$XA = $XB = "";
						}
						$poll .= qq~<tr><td nowarp>$XA$poll[$i]$XB������&nbsp;������</td><td nowarp> <img src=$imagesurl/images/bar$ii.gif width=$width height=10> <b>$thispoll[$i]</b> Ʊ�� $mypoll%��$adminviewpoll</td></tr>~;
					}
				}
			}
			else
			{
				$poll .= qq~<tr><td colspan=2><hr size=1 width=100%></td></tr><tr><td colspan=2>û���˲μӴ�ͶƱ��ѡ���б����£�<hr size=1 width=100%><br></td></tr>~;
				for ($i = 1; $i <= $j; $i++)
				{
					$poll .= qq~<tr><td colspan=2>$poll[$i] </td></tr>~;
				}
				$pollnull = "true";
			}
			$poll .= "</td></tr><tr><td colspan=$adminviewcolspan><hr size=1 width=100%></td></tr></table>";

			if ($threadstate eq "pollclosed" || $showpoll eq "true" || $inmembername eq "����")
			{
				my $poll1 = "<font color=$fonthighlight>���˲���ͶƱ����ע�ᣡ</font>" if ($inmembername eq "����");
				$poll1 = "<font color=$fonthighlight>лл�����Ѿ�Ͷ��Ʊ�ˣ�</font>" if ($showpoll eq "true");
				$poll1 = "<font color=$fonthighlight>�Բ��𣬴�ͶƱ�Ѿ��رգ�</font>" if ($threadstate eq "pollclosed");
				$poll = "<br><br><font color=$fonthighlight>�Բ����������ͶƱ�ſɿ������</font><br>" if ($PollHidden eq "yes" && $inmembername eq "����");
				$poll = "$poll$poll1";
			}
			else
			{
				if ($pollnull eq "true")
				{
					$poll = "$pollform<br><font color=$fonthighlight>Ŀǰ��ʱû����ͶƱ��</font>";
				}
				else
				{
					$poll = "<br><font color=$fonthighlight>�Բ����������ͶƱ�ſɿ������</font>" if ($PollHidden eq "yes" && $membername ne $inmembername);
					$poll = "$pollform$poll";
				}
			}
			$editgraphic = qq~<a href=editpoll.cgi?action=edit&forum=$inforum&topic=$intopic title="�༭���ͶƱ"><img src=$imagesurl/images/edit.gif border=0 width=16 height=15 align=absmiddle>�༭</a>~;
			$delgraphic  = "";
			$posticon = "";
		}
	}
	else
	{
		if ($posticon eq "")
		{
			$posticon = int(myrand(23));
			$posticon = "0$posticon" if ($posticon < 10);
			$posticon = "$posticon.gif";
		}
		$posticon = "<img src=$imagesurl/posticons/$posticon>";
	}
}
else
{
	$posticon = int(myrand(23));
	$posticon = "0$posticon" if ($posticon < 10);
	$posticon = "<img src=$imagesurl/posticons/$posticon.gif>";
}

if ($poll ne "")
{
	$post = $post . "<br>" . $poll;
	$poll = "";
}

($fgwidth,$fgheight) = split(/\|/,$fgwidth);
$forumgraphic = $boardlogo =~ /\.swf$/i ? qq~<param name=play value=true><param name=loop value=true><param name=quality value=high><embed src=$imagesurl/myimages/$boardlogo quality=high width=$fgwidth height=$fgheight pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application/x-shockwave-flash"></embed>~ : "<img src=$imagesurl/myimages/$boardlogo border=0>";
$topictitletemp = $topictitle;
$topictitletemp =~s/\'/\`/isg;

    if ($post=~/\[up\]/is) {
	$post =~ s/\[up\]/<br>$addme/is;
	$addme="";
    }

print qq~
<html><head><title>$topictitle</title>
<meta http-equiv="Content-Type" Content="text/html; charset=gb2312">
<script language="JavaScript" src=$imagesurl/images/board.js></script>
<style>
body	{font-size: 9pt; font-family: "MS Shell Dlg"}
p	{font-size: 9pt; font-family: "MS Shell Dlg"}
select	{font-size: 9pt; font-family: "MS Shell Dlg"}
td	{font-size: 12px; font-family: "MS Shell Dlg"}
input	{font-size: 9pt; font-family: ����}
textarea{font-size: 9pt; font-family: ����}
.input1	{border-right: #085d3f 1px solid; border-top: #085d3f 1px solid; border-left: #085d3f 1px solid; border-bottom: #085d3f 1px solid; background-color: white}
a	{font-size: 9pt; text-transform: none; color: #000000; text-decoration: none}
a.lefta	{font-size: 9pt; text-transform: none; color: #ffffff; text-decoration: none}
a.flink	{font-size: 9pt; text-transform: none; color: #000000; text-decoration: none}
a.lefta:hover	{color: #c0c0c0; text-decoration: none}
a:hover	{color: red; text-decoration: none}
a:visited	{text-decoration: none}
.smallsize	{font-size: 9px; color: #d9d9d9; font-family: verdana}
li	{font-size: 9pt; line-height: 15pt}
.tt2	{font-size: 9pt; line-height: 16pt}
.tt1	{font-size: 14px}
.tt3	{font-size: 9pt; line-heightT: 13pt}
a.hb	{font-size: 9pt; color: #000000; line-height: 10pt}
a.tt1	{color: #000000; text-decoration: none}
.ts {BORDER-RIGHT:black 1px solid;PADDING-RIGHT:2px;BORDER-TOP:black 1px solid;PADDING-LEFT:2px;PADDING-BOTTOM:2px;MARGIN-LEFT:18px;BORDER-LEFT:black 1px solid;WIDTH:250px;COLOR:black;PADDING-TOP:2px;BORDER-BOTTOM:black 1px solid;BACKGROUND-COLOR:lightyellow;cursor:hand;}
.ts1 {BORDER-RIGHT:$tablebordercolor 1px solid;PADDING-RIGHT:2px;BORDER-TOP:$tablebordercolor 1px solid;PADDING-LEFT:2px;PADDING-BOTTOM:2px;MARGIN-LEFT:18px;BORDER-LEFT:$tablebordercolor 1px solid;COLOR:black;PADDING-TOP:2px;BORDER-BOTTOM:$tablebordercolor 1px solid;BACKGROUND-COLOR:lightyellow;cursor:hand;}
</style>
<script>
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
if (targetImg.loaded=="no"){ document.frames["hiddenframe"].location.replace("getphotoinfo.cgi?forum="+f_id+"&topic="+t_id+"&reply="+r_id+"&ftype="+ftype+"&fname="+fname); }
}else{ targetDiv.style.display="none"; targetImg.src="$imagesurl/images/cat.gif"; }
}}
</script>
<iframe width=0 height=0 src="" id=hiddenframe></iframe>~;


if ($magicface ne 'off') {
    $output.=qq~
<script>
function MM_showHideLayers() {var i,p,v,obj,args=MM_showHideLayers.arguments;obj=document.getElementById("MagicFace");for (i=0; i<(args.length-2); i+=3) if (obj) { v=args[i+2];if (obj.style) { obj=obj.style; v=(v=='show')?'visible':(v=='hide')?'hidden':v; }obj.visibility=v; }}
function ShowMagicFace(MagicID) {var MagicFaceUrl = "$imagesurl/MagicFace/swf/" + MagicID + ".swf";document.getElementById("MagicFace").innerHTML = '<object codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,29,0" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="500" height="350"><param name="movie" value="'+ MagicFaceUrl +'"><param name="menu" value="false"><param name="quality" value="high"><param name="play" value="false"><param name="wmode" value="transparent"><embed src="' + MagicFaceUrl +'" wmode="transparent" quality="high" pluginspage="http://www.macromedia.com/go/getflashplayer" type="application/x-shockwave-flash" width="500" height="350"></embed></object>';document.getElementById("MagicFace").style.top = (document.body.scrollTop+((document.body.clientHeight-300)/2))+"px";document.getElementById("MagicFace").style.left = (document.body.scrollLeft+((document.body.clientWidth-480)/2))+"px";document.getElementById("MagicFace").style.visibility = 'visible';setTimeout("MM_showHideLayers('MagicFace','','hidden')",10000);}</script><DIV id=MagicFace style="Z-INDEX: 99; VISIBILITY: hidden; POSITION: absolute"></DIV>
~;
}

print qq~
<body background=$imagesurl/images/schedulebg.gif bgColor=#ffffff><a name=top></a>
<table width=90% border=0 cellSpacing=0 cellPadding=0 align=center>
<tr><td height=40 width=176 align=center>$forumgraphic</td><td height=40 colspan=2 align=right>$adscript</div></td></tr>
<tr align=right><td colspan=3>
<table border=1 cellSpacing=1 bordercolorlight=#49ade9 bordercolordark=#ffffff cellPadding=1 width=100%>
<tr bgColor=#caeaff><td colspan=7>&nbsp;</td></tr></table>
</td></tr>
</table>
<table height=100% cellSpacing=0 cellPadding=0 width=90% align=center border=0><tr>
<td valign=top align=center width=120>
<table height=100% cellSpacing=0 cellPadding=0 width=100% align=center border=0><tr>
<td valign=top width=1 bgColor=white></td>
<td valign=top align=center bgColor=#49ade9>
<table cellSpacing=0 cellPadding=0 width=100 align=center border=0>
<tr><td height=6></td></tr>
<tr><td style="color: white" align=center bgColor=#ffa200 height=18><b>��������Ϣ</b></td></tr>
<tr><td height=6></td></tr>
<tr><td OnMouseOver="this.style.background='#caeaff'; this.style.color='#000000'" OnMouseOut="this.style.background=''; this.style.color=''" align=center height=18><a class=lefta href=profile.cgi?action=show&member=$memberfilename>�� �� �� ��</a></td></tr>
<tr><td OnMouseOver="this.style.background='#caeaff'; this.style.color='#000000'" OnMouseOut="this.style.background=''; this.style.color=''" align=center height=18><a class=lefta href=$homepage>�� �� �� ҳ</a></td></tr>
<tr><td OnMouseOver="this.style.background='#caeaff'; this.style.color='#000000'" OnMouseOut="this.style.background=''; this.style.color=''" align=center height=18><a class=lefta href=fav.cgi?action=add&forum=$inforum&topic=$intopic>�� Ҫ �� ��</a></td></tr>
<tr><td OnMouseOver="this.style.background='#caeaff'; this.style.color='#000000'" OnMouseOut="this.style.background=''; this.style.color=''" align=center height=18><a class=lefta href=pag.cgi?forum=$inforum&topic=$intopic>�� �� �� ��</a></td></tr>
<tr><td OnMouseOver="this.style.background='#caeaff'; this.style.color='#000000'" OnMouseOut="this.style.background=''; this.style.color=''" align=center height=18><a class=lefta href=post.cgi?action=new&forum=$inforum>�� �� �� ��</a></td></tr>
<tr><td OnMouseOver="this.style.background='#caeaff'; this.style.color='#000000'" OnMouseOut="this.style.background=''; this.style.color=''" align=center height=18><a class=lefta href=lbfriend.cgi?forum=$inforum&topic=$intopic>ת �� �� ��</a></td></tr>
<tr><td height=6></td></tr>
</table>
</td>
<td valign=top width=1 bgColor=white></td>
</tr></table>
</td>
<td valign=top>
<table cellSpacing=0 cellPadding=0 width=100% border=0 style="table-layout: fixed"><tr>
<td width=22></td>
<td valign=top>
<table cellSpacing=0 cellPadding=0 width=100% border=0><tr><td width=100% bgColor=#49ade9 height=17><font color=#ffffff>&nbsp;&gt;&gt; <a href=leobbs.cgi><font color=#ffffff>$boardname</font></a>��<a href=forums.cgi?forum=$inforum><font color=#ffffff>$forumname</font></a>��<a href=topic.cgi?forum=$inforum&topic=$intopic><font color=#ffffff>$topictitle</font></a></font></td></tr></table>
<span style="font-size: 14px" $postipaddresstemp>
<br><center><b>$topictitle</b></center><br>
<span style="font-size: 9pt">(���������Ѿ����Ķ��� <font color=red>$threadviews</font> ��) ʱ�䣺$postdate����Դ��$membername</span>
<br><br>$addme<br>$post<br>
</span><br><br>
<table cellSpacing=0 cellPadding=0 width=100% border=0>
<tr><td width=100% bgColor=#ffa200 height=18 align=center>��<a href=pag.cgi?forum=$inforum&topic=$intopic target=_blank>�������</a>�ݡ�������<a href=post.cgi?action=copy1&forum=$inforum&topic=$intopic&postno=1>���ø���</a>�ݡ�������<a href=post.cgi?action=reply&forum=$inforum&topic=$intopic>��������</a>�ݡ�������<a href=lbfriend.cgi?forum=$inforum&topic=$intopic>ת�ĸ���</a>�ݡ�������<a href="javascript:window.close();">�رմ���</a>��</td></tr>
<tr><td width=100% height=18>�������������: </td></tr>~;

$hasadd = @threads - 1;
if ($hasadd == 0)
{
	print qq~
<tr><td width=100% height=18>�����»�û��������ۣ�(<a href=topic.cgi?forum=$inforum&topic=$intopic><font Color=#ffa200>�������̳��ʽ�鿴</font></a>) </td></tr>
</table>~;
}
else
{
	print qq~
<tr><td width=100% height=18>��������<font color=red>$hasadd</font>������������£�(<a href=topic.cgi?forum=$inforum&topic=$intopic><font Color=#ffa200>�������̳��ʽ�鿴</font></a>)<br><hr size=1 width=100%></td></tr>
</table>
~;
}

$membercode = "no";
for ($i = 1; $i < @threads; $i++)
{
	($membername, $topictitle, $postipaddresstemp, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/, $threads[$i]);
	$postdate = &dateformat($postdate + $addtimes);
	$rn = $i;

	$addmefile = 0;
	$rrn = $i;
	my @files1 = grep(/^$inforum\_$intopic\_$rrn\./, @files11);
	my $file1 = @files1;
	if ($file1 > 0)
	{
		my $files1s = $files1[0];
		($up_name, $up_ext) = split(/\./, $files1s);
		$up_ext =~ tr/A-Z/a-z/;
		$addmefile =1;
	}

	if ($addmefile == 1)
	{
		@fileinfo = stat("${imagesdir}$usrdir/${inforum}/${up_name}.${up_ext}");
		$filetype = "unknow";
		$filetype = $up_ext if (-e "${imagesdir}icon/${up_ext}.gif");
		my $rnrn = $rn + 1;
	if ($up_ext eq "gif" || $up_ext eq "jpg" || $up_ext eq "png" || $up_ext eq "bmp")
	{
		if ($nodispphoto eq "yes" || $arrawpostpic eq "off")
		{
			$addme = qq~<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$rnrn&type=.$up_ext target=_blank><img src=$imagesurl/icon/$filetype.gif border=0 width=16></a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$rnrn&type=.$up_ext target=_blank>�����ʾ���������ͼƬ</a><br><br>~;
		}
		else
		{
			$addme = qq~<img src=$imagesurl/icon/$filetype.gif border=0 width=16> ���������ͼƬ���£�<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$rnrn&type=.$up_ext target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$rnrn&type=.$up_ext border=0 alt="�������´������ͼƬ" onload="javascript: if(this.width > document.body.clientWidth - 333) this.width = document.body.clientWidth - 333" onmousewheel="return bbimg(this)"></a><br><br>~;
		}
	        $addme .= qq(<img src=$imagesurl/images/none.gif whidth=0 height=5><BR><span style=CURSOR:hand onclick=loadThreadFollow($forumid,$topicid,$rnrn,'$up_ext')><img id=followImg$rnrn src=$imagesurl/images/cat.gif width=9 loaded=no nofollow="cat.gif" valign=absmiddle> ���˲鿴ͼƬ��ϸ��Ϣ<table cellpadding=0 class=ts1 cellspacing=0 width=50% id=follow$rnrn style=DISPLAY:none><tr><td id=followTd$rnrn><DIV class=ts onclick=loadThreadFollow($forumid,$topicid,$rnrn,'$up_ext')>���ڶ�ȡ��ͼƬ����ϸ��Ϣ�����Ժ� ...</DIV></td></tr></table></span><BR><BR>);
	}
	elsif ($up_ext eq "swf")
	{
		if ($arrawpostflash eq "on")
		{
			$addme = qq~<img src=$imagesurl/icon/$filetype.gif border=0 width=16> ��������һ�� $up_ext ��ʽ Flash ���� (�� $fileinfo[7] �ֽ�)<br><br><param name=play value=true><param name=loop value=true><param name=quality value=high><embed src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$rnrn&type=.$up_ext quality=high width=410 height=280 pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application/x-shockwave-flash"></embed><br>&nbsp;<img src=$imagesurl/images/fav.gif width=16> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$rnrn&type=.$up_ext target=_blank>ȫ���ۿ�</a> (���Ҽ�����)<br><br>~;
		}
		else
		{
			$addme = qq~<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$rnrn&type=.$up_ext target=_blank><img src=$imagesurl/icon/$filetype.gif border=0 width=16 height=16>������� Flash ����</a>~;
		}
	}
	else
	{
		$addme = qq~<font color=$fonthighlight>��ظ���</font>��<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$rnrn&type=.$up_ext target=_blank><img src=$imagesurl/icon/$filetype.gif border=0 width=16 alt="��������һ����$filetype�����͸������������"></a> (�� $fileinfo[7] �ֽ�)<br><br>~;		
	}
	}
	else
	{
		$addme = "";
	}

	$inmembmod = $forummodnamestemp =~ /\Q,$membername,\E/i ? "yes" : "no";

	if ($idmbcodestate eq "on")
	{
		&lbcode(\$post);
		if ($post =~ /<blockquote><font face=����>����/isg)
		{
			$post =~ s/\&amp\;/\&/ig;
			$post =~ s/\&lt\;br\&gt\;/<br>/ig;
		}
	}
	else {
	require "codeno.cgi";
	&lbnocode(\$post);
	$post =~ s/\[DISABLELBCODE\]//isg;
	}
	if ($emoticons eq "on" && $showemoticons eq "yes")
	{
		&doemoticons(\$post);
		&smilecode(\$post);
	}

	$memberfilename = uri_escape($membername);
	$memberfilename =~ s/ /\_/g;

	$post =~ s/(<blockquote>)(.*?)(<hr noshade><\/blockquote>)//isg if ($post =~/<blockquote>/isg);

    if ($post=~/\[up\]/is) {
	$post =~ s/\[up\]/<br>$addme/is;
	$addme="";
    }

	print qq~
<table style="table-layout: fixed" cellPadding=8 cellSpacing=1 border=0 width=100%>
<tr>
<td bgColor=#ffffff rowspan=2 valign=top width=100 $postipaddresstemp><font color=#000000><b><a href=profile.cgi?action=show&member=$memberfilename target=_blank>$membername</a></b></font></td>
<td bgColor=#ffffff><font color=#000000><b>�����ڣ� $postdate</b><br>$addme</td>
</tr>
<tr>
<td bgColor=#ffffff style="left: 0px; width: 100%; word-wrap: break-word">$post</td>
</tr>
<tr>
<td colspan=2 bgColor=#eeeeee align=right>&nbsp;<a href=#top><img src=$imagesurl/images/gotop.gif border=0 weight=15 height=15 align=absmiddle>����</a></td>
</tr>
</table>~;
}

print qq~
</td>
</tr></table></td></tr></table>
</td></tr>
</table>
<div align=center><table height=22 cellSpacing=0 cellPadding=0 width=721 border=0>
<tr><td colspan=2 width=987 height=20 align=center>
<script language="JavaScript"><!--
function bbimg(o){var zoom=parseInt(o.style.zoom, 10)||100;zoom+=event.wheelDelta/12;if (zoom>0) o.style.zoom=zoom+'%';return false;}
var correctwidth = 800;
var correctheight = 600;
if (screen.width != correctwidth || screen.height != correctheight) document.write("����ʹ��" + correctwidth + "��" + correctheight + "���Ϸֱ���. ����ǰ�ķֱ�����:" + screen.width + "��" + screen.height+"��");
--></script>
</td></tr>
</table></div><br>
<center>$adfoot</center>
</body></html>~;
exit;
