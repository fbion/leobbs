#!/usr/bin/perl
###############################################################################################################################################
# LeoBBS ����̳������ ver 2.0
# ʹ�ð취�� news.cgi?forum=����̳��1,����̳��2,����̳��3,����̳��4&max=��ʾ��������&maxlength=���ⳤ��&display=1&link=��ɫ16���ƴ���&vlink=��ɫ16���ƴ���&alink=��ɫ16���ƴ���
# <span id="show1">���ڶ�ȡ���ݣ����Ժ�...</span>
# <span id="show2">���ڶ�ȡ���ݣ����Ժ�...</span>
###############################################################################################################################################

#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
#  ����ɽӥ��������ȱ������ LB5000 XP 2.30 ��Ѱ�   #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBoard.com/          #
#      ��̳��ַ�� http://www.LeoBBS.com/            #
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

#unless ($ENV{'HTTP_REFERER'} =~ /$ENV{'HTTP_HOST'}/) {
#print "Content-Type:text/html\n\n";
#print "document.write('<font color=red>���Բ��𣬲�����Ǳ���̳�������ã�</font>');";
#exit;
#}
use LBCGI;
$LBCGI::POST_MAX=2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "rebuildlist.pl";

$|++;
$query = new LBCGI;
$number        = $query -> param('forum');
$number        = &stripMETA("$number");
#$number    = 1  if ($number eq "");     # Ĭ�ϲ鿴��һ����̳

@number = split(/\,/,$number);

$max	       = $query -> param('max');
$max           = &stripMETA("$max");
$display       = $query -> param('display');
$display       = &stripMETA("$display");
$maxlengths    = $query -> param('maxlength');
$maxlengths    = &stripMETA("$maxlengths");
$link	       = $query -> param('link');
$link          = &stripMETA("$link");
$alink	       = $query -> param('alink');
$alink         = &stripMETA("$alink");
$vlink	       = $query -> param('vlink');
$vlink         = &stripMETA("$vlink");
$mode       = $query -> param('mode');
$mode       = &stripMETA("$mode");
$mode = "" if (($mode ne "topic")&&($mode ne "view"));
$mode      = "topic" if ($mode eq "");  # Ĭ�����ӷ�ʽ�鿴
$display   = 1  if ($display eq "");    # Ĭ����ʾ����ʱ��
$max	   = 10 if ($max eq "");        # Ĭ����ʾ 10 ������
$maxlengths= 30 if ($maxlengths eq "");  # Ĭ�ϱ������ 30 ���ַ�
$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
print header(-charset=>gb2312);
$allstr = "";

foreach $number (@number) {
    $str = "";
    $filetoopen = "$lbdir" . "boarddata/listno$number.cgi";
    if (-e $filetoopen) {
        open(FILE, "$filetoopen");
        @topics = <FILE>;
        $topics = @topics;
        $max = $topics if ($topics<$max);
    
        $max--;
        undef $str;
        $addtime = $timedifferencevalue*3600 + $timezone*3600;
        foreach $topic (@topics[0 ... $max]) {
	    chomp $topic;
            $maxlength = $maxlengths;
            ($topicid, $no) = split(/\t/,$topic);

    my $rr = &readthreadpl($number,$topicid);
    if ($rr ne "") {
	($lastpostdate, $topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $posticon, $posttemp) = split (/\t/,$rr);
    }
    else { next; }

            next if ($topicid !~ /^[0-9]+$/);
            $lastpostdate = &longdate($lastpostdate + $addtime);
 	    $topictitle =~ s/^����������//;
 	    
            if (($posticon1 eq "")||($posticon1 !~ /^[0-9]+$/)) {
		$posticon1 = int(myrand(23));
		if ($posticon1 <10 ) {$posticon1="0$posticon1.gif"};
                if ($posticon1 > 9 ) {$posticon1="$posticon1.gif"};
            }
	    $topictitle = &cleanarea("$topictitle");
 	    $topictitle =~ s/\'/\`/g;
            $topictitle =~ s/\&amp;/\&/g;
	    $topictitle =~ s/\&quot;/\"/g;
#	    $topictitle =~ s/\&lt;/</g;
#	    $topictitle =~ s/\&gt;/>/g;
	    $topictitle =~ s/\"/\&quot;/g;
	    $topictitle =~ s/ \&nbsp;/��/g;
	    $topictitle =~ s/  /��/g;
	    if  ($display eq 1) {
	        $disptime= " $lastpostdate";
	    }
	    else { undef $disptime; }
	    if (length($topictitle)>$maxlength) {
	        $topictitletemp=&lbhz("$topictitle",$maxlength); 
	        $topictitletemp =~ s/\'/\`/;
		$topictitletemp =~ s/\&/\&amp;/g;
		$topictitletemp =~ s/\&amp;\#/\&\#/isg;
		$topictitletemp =~ s/\&amp\;(.{1,6})\&\#59\;/\&$1\;/isg;
		$topictitletemp =~ s/\&\#([0-9]{1,6})\&\#59\;/\&\#$1\;/isg;
		$topictitletemp =~ s/\"/\&quot;/g;
		$topictitletemp =~ s/</\&lt;/g;
		$topictitletemp =~ s/>/\&gt;/g;
		$topictitletemp =~ s/ /\&nbsp;/g;
	        $topictitletemp = $topictitletemp ."&nbsp;" if (length($topictitletemp) < $maxlength);
	        $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$number&topic=$topicid target=_blank><span TITLE=\\\\\\\"���⣺ $topictitle\\\\\\\">$topictitletemp</span></a>$disptime<br>";
	    }
	    else {
	        $topicspace=$maxlength-length($topictitle);
	        $topictitle =~ s/ /\&nbsp;/g;
	        $addspace = "";
	        for ($i=0;$i<$topicspace;$i++) {
	     	    $addspace = $addspace ."&nbsp;";
	        }
	        $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$number&topic=$topicid target=_blank>$topictitle</a>$addspace$disptime<br>";
	    }
        }
        $allstr .= qq~document.write('<span LINK=#$link VLINK=#$vlink ALINK=#$alink><script>document.getElementById("show$number").innerHTML = "$str";</script></span>')\n~;
    }
    else {
    	$allstr .= qq~document.write('<span LINK=#$link VLINK=#$vlink ALINK=#$alink><script>document.getElementById("show$number").innerHTML = "-* û���ҵ���Ӧ����̳ *-";</script></span>')\n~;
    }
}

print "$allstr\n";
exit;
