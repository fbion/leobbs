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
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "gettopicno.cgi";

$query = new LBCGI;
$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic !~ /^[0-9]+$/)||($inforum !~ /^[0-9]+$/));
$inshow    = $query -> param('show');
$inact     = $query -> param('act');
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inact !~ "pre")&&($inact !~ "next"));

open(FILE, "${lbdir}boarddata/listno$inforum.cgi");
sysread(FILE, $listall,(stat(FILE))[7]);
close(FILE);
$listall =~ s/\r//isg;

if ($inact eq "pre") {
    if ($listall =~ m/^$intopic\n/) { &error("��ͨ����&���Ѿ��ǵ�һ�������ˣ�"); }
    else {
	$listall =~ m/.*(^|\n)(.+?)\n$intopic\n/;
        $intopic =$2;
    }
}
else {
    if ($listall =~ m/(^|\n)$intopic\n$/) { &error("��ͨ����&���Ѿ������һ�������ˣ�"); }
    else {
	$listall =~ m/.*(^|\n)$intopic\n(.+?)\n/;
        $intopic =$2;
    }
}
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print "<script language='javascript'>document.location = 'topic.cgi?forum=$inforum&topic=$intopic&show=$inshow'</script>";
exit;
