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
    $rn=1;my $a;
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
			$paGe = $query->param('paGe');
			my $all_1 = @threads / $topicpre ;
			if($all_1>int($all_1)){$all_1=int($all_1)+1;}
            $paGe=($paGe eq '' || $paGe <=0)?"1":"$paGe";
            my $k=($paGe-1)*$topicpre;
            if($k>@threads){$k=0;}
            my $s=$k+$topicpre;
			for($ij=$paGe-2;$ij<=$paGe+3;$ij++){ 
			next if ($ij<1);
			next if ($ij>$all_1);
			if($ij ne $paGe){$newpage.="&nbsp;<a href=\"wap_topic.cgi?t=$intopic&amp;paGe=$ij&amp;f=$inforum&amp;lid=$lid&amp;pa=$pa\">$ij</a>";}else{$newpage.="&nbsp;<i>$ij</i>";}}
			$newpage or $newpage=' <i>1</i>';
for ($i = $k; $i < $s; $i++)
{   next if ($threads[$i] eq '');$rn=$i+1;
	($membername, my $topictitle, $no, $no, $no, my $postdate, my $post) = split(/\t/, $threads[$i]);
&lbcode(\$post);
my $postsize = length($post);
if($postsize>$mastnum){
	$post=~s/<br>/\n/g;
	$post=~s/<p>/\\n\\n/g;
	$post=~s/<(.*?)>//g;
	$post = substr($post,0,$mastnum);
	if ($post =~ /^([\000-\177]|[\241-\371][\75-\376])*([\000-\177]|[\241-\377][\75-\376])$/){}
else{chop($post);}
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
	chomp $post;
	$post .="<a href=\"wap_topic_all.cgi?f=$inforum&amp;lid=$lid&amp;t=$intopic&amp;pno=$i&amp;pa=$pa\">&gt;&gt;</a>"; 
}else{
	$post=~s/<br>/<br\/>/g;
	$post=~s/<p>/<br\/><br\/>/g;
	$post =~ s/\&amp;nbsp;/\&nbsp;/g;
}
 $postdate = &dateformat($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
 $a .= qq~<p>$rn¥��$postdate<br/>����:$membername<br/>$post($postsize��)<br/>------------</p>~;
}
my $r = &msg($inmembername);
$show.=  qq~<p>$r<b>���⣺$topictitle</b><br/><small>($threadviews,$#threads,$startedby)</small><br/>----------</p>$a<p>[$paGe/$all_1ҳ]</p><p>$newpage</p><p>����<input type="text" name="tz" size="5" maxlength="5" format="*N"/><a href="wap_topic.cgi?t=$intopic&amp;paGe=\$(tz)&amp;f=$inforum&amp;lid=$lid&amp;paGe=$pa">Go..</a></p><p><a href="wap_forum.cgi?forum=$inforum&amp;lid=$lid&amp;paGe=$pa">����$forumname</a><br/><a href="wap_re.cgi?f=$inforum&amp;lid=$lid&amp;t=$intopic">�ظ�����</a><br/><a href="wap_index.cgi?lid=$lid">��̳��ҳ</a></p>~;
&wapfoot;