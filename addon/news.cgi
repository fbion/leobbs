#!/usr/bin/perl
###############################################################################################################################################
# LeoBBS ����̳������ ver 2.0
###############################################################################################################################################
# ʹ�ð취�� news.cgi?forum=����̳��&max=��ʾ��������&maxlength=���ⳤ��&display=1&link=��ɫ16���ƴ���&vlink=��ɫ16���ƴ���&alink=��ɫ16���ƴ���
# ���� ������ҳ���ʵ�λ�ü����������
#      <script src="news.cgi?forum=1&max=10&maxlength=20&link=0000ff&vlink=7f007f&alink=ff0000&mode=topic"></script>
#      �����Ϳ�������Ӧλ����ʾ1����̳������10�����ӣ����ⳤ��Ϊ 20����ʾ����ʱ�䣬������ģʽ�鿴
#                                                   (display=0 ��ʾ����ʾ����ʱ��)
#                                                   (mode=view ��ʾ������ģʽ�鿴)
# link���Զ��峬���ӵ���ɫ��vlink���Զ����ѷ��ʵĳ����ӵ���ɫ��alink���Զ��嵱ǰ�����ӵ���ɫ
#
# ���в���������ʡ�ԣ�Ĭ��Ϊ�鿴��1����̳��ǰ10�����ӣ��������20���ַ�����ʾʱ�䡢������ģʽ
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
$number    = 1  if ($number eq "");     # Ĭ�ϲ鿴��һ����̳
$display   = 1  if ($display eq "");    # Ĭ����ʾ����ʱ��
$max	   = 10 if ($max eq "");        # Ĭ����ʾ 10 ������
$maxlengths= 30 if ($maxlengths eq "");  # Ĭ�ϱ������ 30 ���ַ�
$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
print header(-charset=>gb2312);
if ($number !~ /^[0-9]+$/) {
   print "document.write('��ͨ&�ϴ󣬱��Һ��ҵĳ���ѽ��')\n";
   exit;
}

if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

if ($enterminmony > 0 || $enterminjf > 0 || $enterminweiwang > 0 || $allowusers ne '') {
    $str="-* ���Ǳ�����̳�������б� *-";
    goto ENDPPP;
}
    my $filetoopen = "${lbdir}forum$number/foruminfo.cgi";
    open(FILE, "$filetoopen");
    my $forums = <FILE>;
    close(FILE);
    (my $no, $no, $no, $no, $no, $no ,$no ,$no ,$privateforum, $startnewthreads,$no) = split(/\t/,$forums);

if (($startnewthreads eq "cert")&&($userincert eq "no")) {
    $str="-* ���Ǳ�����̳�������б� *-";
    goto ENDPPP;
}

if ($privateforum ne "yes") {
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
	        $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$number&topic=$topicid target=_blank><ACRONYM TITLE=\"���⣺ $topictitle\">$topictitletemp</ACRONYM></a>$disptime<br>";
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
    }
    else {
        $str="-* û���ҵ���Ӧ����̳ *-";
    }
}
else {
    $str="-* ���Ǳ�����̳�������б� *-";
}
ENDPPP:

print "document.write('<span LINK=#$link VLINK=#$vlink ALINK=#$alink>$str')\n";
exit;
