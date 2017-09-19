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
#######################################################################
#
#  Programming(��д) By �ӳ�(JackyCheng)��http://www.leohacks.com & http://blog.mycrazy.info)
#  �޸�����: ��ǿ (CPower)
#  ��һ����д: BBSER
#
#######################################################################
# RSS ���ϣ���̳���������ġ�����̳����������
#######################################################################

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
require "bbs.lib.pl";
require "data/styles.cgi";
require "code.cgi";
$|++;

$max=$query->param('max') || 15; #Ĭ����ʾ��� 15 �����ӵ��б�

$number = $query -> param('forum');
$number1 = $query -> param('forums');

$number = $number1 if ($number eq "");

if ($number ne "") {&forums;} else {&viewall;}

sub viewall
{ # ������̳��������

    my $rssdir = "$lbdir" . "cache/rssdata";
    if (!( -e "$rssdir")){mkdir("$rssdir",0777);chmod(0777,"$rssdir");}

    if((-e "$rssdir/allrss.xml")&&((-M "$rssdir"."/allrss.xml") * 86400 < 300)) # ���С�� 5 ����
    {
	undef $/;
	my $filetoopen = "$lbdir" . "cache/rssdata/allrss.xml";
	open(FILE,"$filetoopen");
	my $rssdata = <FILE>;
	close(FILE);
	$/="\n";
	print "$rssdata";
	exit;
    }

    $rssout = qq~Content-type:application/xml\n\n~;
    $rssout .= qq~<?xml version="1.0" encoding="gb2312"?>\n<rss version="2.0">\n~;
    $rssout .= qq~<channel>\n~;
    $rssout .= qq~\t<title><![CDATA[$boardname - ��̳������]]></title>\n~;
    $rssout .= qq~\t<link>$boardurl/leobbs.cgi</link>\n~;
    $rssout .= qq~\t<description><![CDATA[$boardname ���� $max �������б�]]></description>\n~;
    $rssout .= qq~\t<copyright>$boardname</copyright>\n~;
    $rssout .=  qq~\t<managingEditor>$adminemail_in</managingEditor>\n~;
    $rssout .= qq~\t<language>zh-cn</language>\n~;
    $rssout .= qq~\t<generator>LEOBBS X -- http://bbs.leobbs.com/</generator>\n~;
    $rssout .= qq~\t<image><url>$imagesurl/images/lblogo.gif</url>\n<title>$boardname</title>\n<link>$boardurl</link>\n</image>\n~;

    if ($rssinfo eq "no") {
   	    my $addtime = time;
	    $addtime = $timedifferencevalue*3600 + $timezone*3600 + $addtime;
	    my $posttime = &dateformat ($posttime + $addtime);
	    $rssout .= qq~\t<item>\n~;
	    $rssout .= qq~\t\t<title><![CDATA[����Ա���������̳ʹ�� RSS ���ܣ�]]></title>\n~;	# ����
	    $rssout .= qq~\t\t<author>ϵͳ����Ա</author>\n~;	# ����
	    $rssout .= qq~\t\t<pubDate>$posttime</pubDate>\n~;		# ����
	    $rssout .= qq~\t\t<description><![CDATA[����Ա���������̳ʹ�� RSS ���ܣ�]]></description>\n~;	#
	    $rssout .= qq~\t</item>\n~;
	    $rssout .= qq~</channel>\n~;
	    $rssout .= qq~</rss>\n~;
	    print "$rssout";
	    exit;
    } 

    if ($regaccess eq "on") {
   	    my $addtime = time;
	    $addtime = $timedifferencevalue*3600 + $timezone*3600 + $addtime;
	    my $posttime = &dateformat ($posttime + $addtime);
	    $rssout .= qq~\t<item>\n~;
	    $rssout .= qq~\t\t<title><![CDATA[����̳����ֻ��ע���Ա���ܲ鿴�������޷�ʹ�� RSS ���ܣ�]]></title>\n~;	# ����
	    $rssout .= qq~\t\t<author>ϵͳ����Ա</author>\n~;	# ����
	    $rssout .= qq~\t\t<pubDate>$posttime</pubDate>\n~;		# ����
	    $rssout .= qq~\t\t<description><![CDATA[����̳����ֻ��ע���Ա���ܲ鿴�������޷�ʹ�� RSS ���ܣ�]]></description>\n~;	#
	    $rssout .= qq~\t</item>\n~;
	    $rssout .= qq~</channel>\n~;
	    $rssout .= qq~</rss>\n~;
	    print "$rssout";
	    exit;
   }

    $filetoopen = "$lbdir" . "data/recentpost.cgi";
    if (-e $filetoopen) {
	open(LEO, "$filetoopen");
	flock (LEO, 1) if ($OS_USED eq "Unix");
	@topics = <LEO>;
	close(LEO);

	$topics = @topics;
	$max = $topics if ($topics<$max);
	$max--;
	my $addtime = $timedifferencevalue*3600 + $timezone*3600;

	foreach $topic (@topics[0 ... $max]) {
	    chomp $topic;
	    ($forumid, $topicid, $topictitle, $posttime,undef, $membername) = split(/\t/,$topic);
	    my $posttime = &dateformat ($posttime + $addtime);

	    $topictitle =~ s/^����������//;

	if ($addtopictime eq "yes") {
	    my $topictime = &dispdate($posttime + ($timedifferencevalue*3600) + ($timezone*3600));
	    $topictitle = "[$topictime] $topictitle";
	}

	    &banname($forumid);

	    my $rr = &readthreadpl($forumid,$topicid);
	    if ($rr ne "") {
	           ($x, $x, $x, $x, $x, $x, $x, $x, $x, $x, $x, $posttemp) = split (/\t/,$rr);
	    }
	    else { next; }
	    next if (($forumid !~ /^[0-9]+$/)||($topicid !~ /^[0-9]+$/));

	    $topictitle = &cleanarea("$topictitle");
	    $topictitle =~ s/\'/\`/g;
	    $topictitle =~ s/\&amp;/\&/g;
	    $topictitle =~ s/\&quot;/\"/g;
	    $topictitle =~ s/ \&nbsp;/��/g;

	    $link=$boardurl."/";
	    $link1="topic.cgi?forum=".$forumid."&amp;topic=". $topicid ."&amp;show=0";
	    $link2="post.cgi?action=reply&amp;forum=$forumid&amp;topic=$topicid";

	    $rssout .= qq~\t<item>\n~;
	    $rssout .= qq~\t\t<title><![CDATA[$topictitle]]></title>\n~;	# ����
	    $rssout .= qq~\t\t<author>$membername</author>\n~;	# ����
	    $rssout .= qq~\t\t<pubDate>$posttime</pubDate>\n~;		# ����
	    $rssout .= qq~\t\t<link>$link$link1</link>\n~;		# ����
	    $rssout .= qq~\t\t<comments>$link$link2</comments>\n~;	# ����
	    $rssout .= qq~\t\t<description><![CDATA[$posttemp]]></description>\n~;	#
	    $rssout .= qq~\t\t<category>$forumname</category>\n~;	# ���
	    $rssout .= qq~\t</item>\n~;
      	   }
    }

    $rssout .= qq~</channel>\n~;
    $rssout .= qq~</rss>\n~;

    my $filetoopen = "$lbdir" . "cache/rssdata/allrss.xml";
    open(FILE, ">$filetoopen");
    print FILE "$rssout";
    close(FILE);

    print "$rssout";
    exit;
}

sub forums
{ # ��̳�ְ������������
    if ($number =~ /[^0-9]/ or $number eq ""){ print "������Ŵ���";exit; }

if (-e "${lbdir}data/style${number}.cgi") { require "${lbdir}data/style${number}.cgi"; }

    my $rssdir = "$lbdir" . "cache/rssdata";
    if (!( -e "$rssdir")){mkdir("$rssdir",0777);chmod(0777,"$rssdir");}

    if((-e "$rssdir/forums$number.xml")&&((-M "$rssdir"."/forums$number.xml") * 86400 < 300)) # ���С�� 5 ����
    {
	undef $/;
	my $filetoopen = "$lbdir" . "cache/rssdata/forums$number.xml";
	open(FILE,"$filetoopen");
	my $rssdata = <FILE>;
	close(FILE);
	$/="\n";
	print "$rssdata";
	exit;
    }
    &banname($number);

    $rssout = qq~Content-type:application/xml\n\n~;
    $rssout .= qq~<?xml version="1.0" encoding="gb2312"?>\n<rss version="2.0">\n~;
    $rssout .= qq~<channel>\n~;
    $rssout .= qq~\t<title><![CDATA[$boardname - $forumname ��������]]></title>\n~;
    $rssout .= qq~\t<link>$boardurl/forums.cgi&amp;forum=$number</link>\n~;
    $rssout .= qq~\t<description><![CDATA[$boardname - $forumname ���� $max �������б�]]></description>\n~;
    $rssout .= qq~\t<copyright>$boardname</copyright>\n~;
    $rssout .= qq~\t<managingEditor>$adminemail_in</managingEditor>\n~;
    $rssout .= qq~\t<language>zh-cn</language>\n~;
    $rssout .= qq~\t<generator>LEOBBS X -- http://bbs.leobbs.com/</generator>\n~;
    $rssout .= qq~\t<image><url>$imagesurl/images/lblogo.gif</url>\n<title>$boardname</title>\n<link>$boardurl</link>\n</image>~;

    if ($rssinfo eq "no") {
   	    my $addtime = time;
	    $addtime = $timedifferencevalue*3600 + $timezone*3600 + $addtime;
	    my $posttime = &dateformat ($posttime + $addtime);
	    $rssout .= qq~\t<item>\n~;
	    $rssout .= qq~\t\t<title><![CDATA[����Ա���������̳����ʹ�� RSS ���ܣ�]]></title>\n~;	# ����
	    $rssout .= qq~\t\t<author>ϵͳ����Ա</author>\n~;	# ����
	    $rssout .= qq~\t\t<pubDate>$posttime</pubDate>\n~;		# ����
	    $rssout .= qq~\t\t<description><![CDATA[����Ա���������̳����ʹ�� RSS ���ܣ�]]></description>\n~;	#
	    $rssout .= qq~\t</item>\n~;
	    $rssout .= qq~</channel>\n~;
	    $rssout .= qq~</rss>\n~;
	    print "$rssout";
	    exit;
    } 

if ($enterminmony > 0 || $enterminjf > 0 || $enterminweiwang > 0 || $allowusers ne '') {
   	    my $addtime = time;
	    $addtime = $timedifferencevalue*3600 + $timezone*3600 + $addtime;
	    my $posttime = &dateformat ($posttime + $addtime);
	    $rssout .= qq~\t<item>\n~;
	    $rssout .= qq~\t\t<title><![CDATA[������̳������ʹ�� RSS ���ܣ�]]></title>\n~;	# ����
	    $rssout .= qq~\t\t<author>ϵͳ����Ա</author>\n~;	# ����
	    $rssout .= qq~\t\t<pubDate>$posttime</pubDate>\n~;		# ����
	    $rssout .= qq~\t\t<description><![CDATA[������̳������ʹ�� RSS ���ܣ�]]></description>\n~;	#
	    $rssout .= qq~\t</item>\n~;
	    $rssout .= qq~</channel>\n~;
	    $rssout .= qq~</rss>\n~;
	    print "$rssout";
	    exit;
}
   if ($regaccess eq "on") {
   	    my $addtime = time;
	    $addtime = $timedifferencevalue*3600 + $timezone*3600 + $addtime;
	    my $posttime = &dateformat ($posttime + $addtime);
	    $rssout .= qq~\t<item>\n~;
	    $rssout .= qq~\t\t<title><![CDATA[����̳����ֻ��ע���Ա���ܲ鿴�������޷�ʹ�� RSS ���ܣ�]]></title>\n~;	# ����
	    $rssout .= qq~\t\t<author>ϵͳ����Ա</author>\n~;	# ����
	    $rssout .= qq~\t\t<pubDate>$posttime</pubDate>\n~;		# ����
	    $rssout .= qq~\t\t<description><![CDATA[����̳����ֻ��ע���Ա���ܲ鿴�������޷�ʹ�� RSS ���ܣ�]]></description>\n~;	#
	    $rssout .= qq~\t</item>\n~;
	    $rssout .= qq~</channel>\n~;
	    $rssout .= qq~</rss>\n~;
	    print "$rssout";
	    exit;
   }

    my $filetoopen = "${lbdir}forum$number/foruminfo.cgi";
    open(FILE, "$filetoopen");
    my $forums = <FILE>;
    close(FILE);
    (my $no, $no, $no, $no, $no, $no ,$no ,$idmbcodestate ,$privateforum, $startnewthreads,$no) = split(/\t/,$forums);

if (($startnewthreads eq "cert")&&($userincert eq "no")) {
   	    my $addtime = time;
	    $addtime = $timedifferencevalue*3600 + $timezone*3600 + $addtime;
	    my $posttime = &dateformat ($posttime + $addtime);
	    $rssout .= qq~\t<item>\n~;
	    $rssout .= qq~\t\t<title><![CDATA[������̳������ʹ�� RSS ���ܣ�]]></title>\n~;	# ����
	    $rssout .= qq~\t\t<author>ϵͳ����Ա</author>\n~;	# ����
	    $rssout .= qq~\t\t<pubDate>$posttime</pubDate>\n~;		# ����
	    $rssout .= qq~\t\t<description><![CDATA[������̳������ʹ�� RSS ���ܣ�]]></description>\n~;	#
	    $rssout .= qq~\t</item>\n~;
	    $rssout .= qq~</channel>\n~;
	    $rssout .= qq~</rss>\n~;
	    print "$rssout";
	    exit;
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
                ($topicid, $no) = split(/\t/,$topic);
	        my $rr = &readthreadpl($number,$topicid);
	        if ($rr ne "") {
	           ($lastpostdate, $topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $posticon, $posttemp) = split (/\t/,$rr);
	        }
	        else { next; }

                next if ($topicid !~ /^[0-9]+$/);

                $lastpostdate = &dateformat($lastpostdate + $addtime);
 	        $topictitle =~ s/^����������//;

	if ($addtopictime eq "yes") {
	    my $topictime = &dispdate($startedpostdate + ($timedifferencevalue*3600) + ($timezone*3600));
	    $topictitle = "[$topictime] $topictitle";
	}
 	    
  	        $topictitle = &cleanarea("$topictitle");
 	        $topictitle =~ s/\'/\`/g;
                $topictitle =~ s/\&amp;/\&/g;
	        $topictitle =~ s/\&quot;/\"/g;
	        $topictitle =~ s/ \&nbsp;/��/g;
	        $topictitle =~ s/  /��/g;

	        $link=$boardurl."/";
	        $link1="topic.cgi?forum=".$number."&amp;topic=". $topicid ."&amp;show=0";
	        $link2="post.cgi?action=reply&amp;forum=$number&amp;topic=$topicid";

	        $rssout .= qq~\t<item>\n~;
	        $rssout .= qq~\t\t<title><![CDATA[$topictitle]]></title>\n~;	# ����
	        $rssout .= qq~\t\t<author>$startedby</author>\n~;	# ����
	        $rssout .= qq~\t\t<pubDate>$lastpostdate</pubDate>\n~;		# ����
	        $rssout .= qq~\t\t<link>$link$link1</link>\n~;		# ����
	        $rssout .= qq~\t\t<comments>$link$link2</comments>\n~;	# ����
	        $rssout .= qq~\t\t<description><![CDATA[$posttemp]]></description>\n~;	#
	        $rssout .= qq~\t\t<category>$forumname</category>\n~;	# ���
	        $rssout .= qq~\t</item>\n~;
            }
	}
        else {

   	    my $addtime = time;
	    $addtime = $timedifferencevalue*3600 + $timezone*3600 + $addtime;
	    my $posttime = &dateformat ($posttime + $addtime);
	    $rssout .= qq~\t<item>\n~;
	    $rssout .= qq~\t\t<title><![CDATA[û���ҵ��˷���̳]]></title>\n~;	# ����
	    $rssout .= qq~\t\t<author>ϵͳ����Ա</author>\n~;	# ����
	    $rssout .= qq~\t\t<pubDate>$posttime</pubDate>\n~;		# ����
	    $rssout .= qq~\t\t<description><![CDATA[û���ҵ��˷���̳]]></description>\n~;	#
	    $rssout .= qq~\t</item>\n~;
	    $rssout .= qq~</channel>\n~;
	    $rssout .= qq~</rss>\n~;
	    print "$rssout";
	    exit;
        }
    }
    else {
   	    my $addtime = time;
	    $addtime = $timedifferencevalue*3600 + $timezone*3600 + $addtime;
	    my $posttime = &dateformat ($posttime + $addtime);
	    $rssout .= qq~\t<item>\n~;
	    $rssout .= qq~\t\t<title><![CDATA[������̳������ʹ�� RSS ���ܣ�]]></title>\n~;	# ����
	    $rssout .= qq~\t\t<author>ϵͳ����Ա</author>\n~;	# ����
	    $rssout .= qq~\t\t<pubDate>$posttime</pubDate>\n~;		# ����
	    $rssout .= qq~\t\t<description><![CDATA[������̳������ʹ�� RSS ���ܣ�]]></description>\n~;	#
	    $rssout .= qq~\t</item>\n~;
	    $rssout .= qq~</channel>\n~;
	    $rssout .= qq~</rss>\n~;
	    print "$rssout";
	    exit;
    }

    $rssout .= qq~</channel>\n~;
    $rssout .= qq~</rss>\n~;

    my $filetoopen = "$lbdir" . "cache/rssdata/forums$number.xml";
    open(FILE, ">$filetoopen");
    print FILE "$rssout";
    close(FILE);

    print "$rssout";
    exit;
}

sub readthreadpl {
    ($inforum,$intopic) = @_;
    open (THDFILE, "${lbdir}forum$inforum/$intopic.thd.cgi");
    my @topicall = <THDFILE>;
    close (THDFILE);
    my $topicall = @topicall;
    my $postfirst = $topicall[0];
    $postfirst =~ s/[\a\f\n\e\0\r]//isg;

    (my $membername1, my $topictitle1, my $postipaddress1, my $showemoticons1, my $showsignature1, my $postdate1, my $post, my $posticon1) = split(/\t/,$postfirst);

    $threadviews = ($topicall+1) * 8 if ($threadviews eq "");
    $post = "(����)" if ($post=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg);
    $post = "(����)" if ($post=~/LBSALE\[(.*?)\]LBSALE/sg);
    $post =~ s/\[hidepoll\]//isg;
    $post =~ s/\[USECHGFONTE\]//sg;
    $post =~ s/\[DISABLELBCODE\]//sg;
    $post =~ s/\[POSTISDELETE=(.+?)\]//sg;
    $post =~ s/(^|\>|\n)\[���(.+?)�����(.+?)�༭\]/$1\<font color=$posternamecolor\>\[���$2�����$3�༭\]\<\/font\>/isg;

    if ($emoticons eq "on")
    {
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
    $post =~ s/=attachment.cgi\?/=$boardurl\/attachment.cgi?/isg;
    $post =~ s/\"attachment.cgi\?/\"$boardurl\/attachment.cgi?/isg;
    $post =~ s/\'attachment.cgi\?/\'$boardurl\/attachment.cgi?/isg;
    
    $post = &lbhz($post, 1500);	# ��ʾ����1000���ֽڣ������Ҫ��ʾȫ�����ݣ�������ɾ����

    if ($topictitle1 eq "") { return ""; }
    else {
	$topictitle1 =~ s/^����������//;
	my $line = "$postdate1\t$intopic\t$topictitle1\t$topicdescription\t$threadstate\t$topicall\t$threadviews\t$membername1\t$postdate1\t$membername1\t\t$post\t\t";
        $line =~ s/[\a\f\n\e\0\r]//isg;
	return ("$line");
    }
}


sub banname{
	local $inforum = shift;
       if (-e "${lbdir}cache/forums${forumid}.pl") {
	 eval{ require "${lbdir}cache/forums${forumid}.pl";};
	 if ($@) { unlink ("${lbdir}cache/forums${forumid}.pl");  require "domoderator.pl"; }
	   (undef,$category,undef, $forumname, undef) = split(/\t/, $thisforums);}
	 else {require "domoderator.pl";}
}
