#!/usr/bin/perl
#########################
# �ֻ���̳WAP��
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
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
$query = new LBCGI;
$LBCGI::POST_MAX = 2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "wap.lib.pl";
require "data/styles.cgi";
require "wap_code.cgi";
require "wap.pl";
$|++;
&waptitle;
$show.= qq~<card  title="$boardname"> ~;
$lid = $query -> param('lid');
&check($lid);
$pa    = $query -> param('pa');
if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
} else {
    &getmember("$inmembername","no");
}  
$inforum        = $query -> param('f');
$intopic        = $query -> param('t');
$postno        = $query -> param('pno');
$ag        = $query -> param('ag');
&getoneforum("$inforum");
$myinmembmod = $inmembmod;
&errorout("������&������ⲻ���ڣ������Ѿ���ɾ����") unless (-e "${lbdir}forum${inforum}/${intopic}.thd.cgi");
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
	$mymembercode = $membercode;
	$myinmembmod = $inmembmod;
	$myrating = $rating;
	$tempaccess = "forumsallowed" . $inforum;
	$testentry = $query->cookie($tempaccess);
	$allowed = $allowedentry{$inforum} eq "yes" || ($testentry eq $forumpass && $testentry ne "") || $mymembercode eq "ad" || $mymembercode eq "smo" || $myinmembmod eq "yes" ? "yes" : "no";

&errorout("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($inforum !~ /^[0-9]+$/);
&errorout("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($intopic !~ /^[0-9]+$/);
&getoneforum($inforum);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }
&errorout("������̳&�����̳��û��Ȩ�޽�����̳��")if($yxz ne '' && $yxz!~/,$membercode,/);
$addtimes = ($timedifferencevalue + $timezone) * 3600;
&errorout("�����Ա��̳�鿴��������&���ǿ���û��Ȩ�޽���!") if ($inmembername eq "����" && $regaccess eq "on" && &checksearchbot);
&errorout("����˽����̳&�Բ�����û��Ȩ�޽����˽����̳��") if ($privateforum eq "yes" && $allowed ne "yes");
if (($startnewthreads eq "cert")&&(($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $membercode !~ /^rz/)||($inmembername eq "����"))&&($userincert eq "no")) { &errorout("������̳&��һ���Ա������������̳��"); }

if ($allowusers ne ''){
    &errorout('������̳&�㲻����������̳��') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}

if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &errorout("������̳&�㲻����������̳���������Ϊ $rating��������ֻ̳���������ڵ��� $enterminweiwang �Ĳ��ܽ��룡") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
     if ($enterminmony > 0 || $enterminjf > 0 ) {
require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
$mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
&errorout("������̳&�㲻����������̳����Ľ�ǮΪ $mymoney1��������ֻ̳�н�Ǯ���ڵ��� $enterminmony �Ĳ��ܽ��룡") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
&errorout("������̳&�㲻����������̳����Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $enterminjf �Ĳ��ܽ��룡") if ($enterminjf > 0 && $jifen < $enterminjf);
   }
}
$topictitle=~s/^����������//;
    my $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    open(FILE, "$filetoopen");
    my @threads = <FILE>;
    close(FILE);
   my $a;
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
$membercode = "no";
			
	($membername, my $no, $no, $no, $no, my $postdate, my $post) = split(/\t/, $threads[$postno]);
$rn=$postno+1;
&lbcode(\$post);
if($ag<1){$ag=1;}
	$post=~s/<br>/\\n/g;
	$post=~s/<p>/\\n\\n/g;
	$post=~s/<(.*?)>//g;
	my $sa = $mastnum2*($ag-1); my $sb = $mastnum2*$ag;
	$postsize = length($post);
	$sb=($sb<=$postsize)?$mastnum2:($postsize-$sb-$mastnum2);
	$post = &waplbhz($post,$sa,$mastnum2);
	$yema = ($postsize/$mastnum2 >int($postsize/$mastnum2))?(int($postsize/$mastnum2)+1):int($postsize/$mastnum2);
	$post=~s/\\n/<br\/>/g;
	$post =~ s/\&/\&amp;/isg;
	$post =~ s/\&amp;nbsp;/\&nbsp;/g;
	$post =~ s/\&amp;gt;/\&gt;/g;
	$post =~ s/\&amp;lt;/\&lt;/g;
	$post =~ s/\&amp;#36;/\��/g;
	$post =~ s/\&amp\;(.{1,6})\&\#59\;/\&$1\;/isg;
    $post =~ s/\&\#([0-9]{1,6})\&\#59\;/\&\#$1\;/isg;
	$post =~ s/\&amp;quot;/\"/g;
	$post =~ s/\&amp;#59;/\;/g;
	$post =~ s/\&amp;#35;/\&#35;/g;
	$post =~ s/\&amp;amp;/\&amp;/g;
	$ag1=$ag+1;
	$ag2=$ag-1;
	$post .="<br/>[$ag/$yemaҳ]<br/>";
	$post.="<a href=\"wap_topic_all.cgi?f=$inforum&amp;lid=$lid&amp;t=$intopic&amp;pno=$postno&amp;pa=$pa&amp;ag=$ag1\">[��һҳ]</a>&nbsp;"if($ag1<=$yema);
	$post.="<a href=\"wap_topic_all.cgi?f=$inforum&amp;lid=$lid&amp;t=$intopic&amp;pno=$postno&amp;pa=$pa&amp;ag=$ag2\">[��һҳ]</a>&nbsp;"if($ag2>=1);
 $postdate = &dateformat($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
 $a .= qq~<p>$post</p>~;
$show.= qq~<p><b>���⣺<a href="wap_topic.cgi?f=$inforum&amp;t=$intopic&amp;lid=$lid&amp;pa=$pa">$topictitle</a></b></p>$a<p>����<input type="text" name="tz" size="5" maxlength="5" format="*N"/><a href="wap_topic_all.cgi?f=$inforum&amp;lid=$lid&amp;t=$intopic&amp;pno=$postno&amp;pa=$pa&amp;ag=\$(tz)">Go..</a></p><p><a href="wap_forum.cgi?forum=$inforum&amp;lid=$lid&amp;pa=$pa">����$forumname</a><br/><a href="wap_re.cgi?f=$inforum&amp;lid=$lid&amp;t=$intopic">�ظ�����</a><br/><a href="wap_index.cgi?lid=$lid">��̳��ҳ</a></p>~;

&wapfoot;