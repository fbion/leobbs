#!/usr/bin/perl
#########################################################################################################################
# ��̳�������ӣ���ʾ������̳�������� ver 2.1
#########################################################################################################################
# ʹ�ð취�� allnews.cgi?maxlength=���ⳤ��&display=��ʾ��ʽ&name=������ʾ&link=��ɫ����&vlink=��ɫ����&alink=��ɫ����&max=��ʾ��������
# ���� ������ҳ���ʵ�λ�ü����������
#      <script src="allnews.cgi?maxlength=20&display=1&name=1&link=0000ff&vlink=7f007f&alink=ff0000&mode=topic&max=10"></script>
#      �����Ϳ�������Ӧλ����ʾ������̳������ 10 ���������ⳤ�� 20����ʾ����ʱ�䣬��ʾ�����ˣ�������ģʽ�鿴
#                                            (display=0 ��ʾ����ʾ����ʱ��)
#                                            (name=0 ��ʾ����ʾ������)
#                                            (mode=view ��ʾ������ģʽ�鿴)
# link�ǳ����ӵ���ɫ��vlink���ѷ��ʹ��ĳ����ӣ�alink�ǵ�ǰ������
# 
# ������ʾ���Ӹ�������̳���ֻ��¼ 30 �������ԣ�����������ֵ�ʱ�򲻱س��� 30 ��
#
# ���в���������ʡ�ԣ�Ĭ��Ϊ����10�������������20���ַ�����ʾʱ�䡢������ģʽ
#########################################################################################################################

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
$|++;
$query = new LBCGI;

$maxlength   = $query -> param('maxlength');
$maxlength   = &stripMETA("$maxlength");
$display     = $query -> param('display');
$display     = &stripMETA("$display");
$name        = $query -> param('name');
$name        = &stripMETA("$name");
$max	       = $query -> param('max');
$max           = &stripMETA("$max");
$link        = $query -> param('link');
$link        = &stripMETA("$link");
$vlink       = $query -> param('vlink');
$vlink       = &stripMETA("$vlink");
$alink       = $query -> param('alink');
$alink       = &stripMETA("$alink");
$mode        = $query -> param('mode');
$mode        = &stripMETA("$mode");
$mode      = "" if (($mode ne "topic")&&($mode ne "view"));
$mode      = "topic" if ($mode eq "");  # Ĭ�����ӷ�ʽ�鿴
$maxlength = 20 if ($maxlength eq "");  # Ĭ�ϱ������ 20 ���ַ�
$display   = 1  if ($display eq "");    # Ĭ����ʾ����ʱ��
$name      = 1  if ($name eq "");       # Ĭ����ʾ������
$max	   = 10 if ($max eq "");        # Ĭ����ʾ 10 ������
$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
print header(-charset=>gb2312);
    $filetoopen = "$lbdir" . "data/recentpost.cgi";
    if (-e $filetoopen) {
	open(FILE, "$filetoopen");
	flock (FILE, 1) if ($OS_USED eq "Unix");
        @topics = <FILE>;
        close(FILE);
        $topics = @topics;
        $max = $topics if ($topics<$max);
        $max--;

        $str="<span LINK=#$link VLINK=#$vlink ALINK=#$alink>";
	$addtime = $timedifferencevalue*3600 + $timezone*3600;
        foreach $topic (@topics[0 ... $max]) {
            chomp $topic;
            ($forumid, $topicid, $topictitle, $posttime, $posticon1, $membername) = split(/\t/,$topic);
            $topictitle =~ s/^����������//;
            next if (($forumid !~ /^[0-9]+$/)||($topicid !~ /^[0-9]+$/));
            $posttime = dateformat($posttime + $addtime);
            if (($posticon1 eq "")||($posticon1 !~ /^[0-9]+\.gif$/i)) {
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
	    if  ($display eq 1) {
	        $disptime= " ($posttime)";
	    }
	    else { undef $disptime; }
	    if ($name eq 1) {
	        $memberspace=16-length($membername)-1;
	        $addmspace = "";
	        for ($i=0;$i<$memberspace;$i++) {
	     	    $addmspace = $addmspace ."&nbsp;";
		}
		$addmspace = qq~����<a href=$boardurl/profile.cgi?action=show&member=~ . ($uri_escape eq "no" ? $membername : uri_escape($membername)) . qq~ title=����鿴$membername������ target=_blank>[$membername]</a>$addmspace~;
	    }
	    else { undef $addmspace; }

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
	        $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$forumid&topic=$topicid target=_blank><ACRONYM TITLE=\"���⣺ $topictitle\"><font color=$color>$topictitletemp</font></ACRONYM></a>$addmspace$disptime<br>";
	    }
	    else {
  	        $topicspace=$maxlength-length($topictitle);
	        $addspace = "";
	        for ($i=0;$i<$topicspace;$i++) {
	     	   $addspace = $addspace ."&nbsp;";
	        }
	        $str.="<img src=$imagesurl/posticons/$posticon1 $defaultsmilewidth $defaultsmileheight border=0> <a href=$boardurl/$mode.cgi?forum=$forumid&topic=$topicid target=_blank><font color=$color>$topictitle</font></a>$addspace$addmspace$disptime<br>";
	    }
        }
    }
    else {
        $str.="��̳��û����������";
    }    

print "document.write('$str')\n";
exit;
