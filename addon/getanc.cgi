#!/usr/bin/perl
###################################################################################
# LeoBBS ������ʾ ver 1.5
###################################################################################
# ʹ�ð취�� getanc.cgi?max=��ʾ���泤��
# ���� ������ҳ���ʵ�λ�ü����������
#      <script src="getanc.cgi?max=500"></script>
#      �����Ϳ�������Ӧλ����ʾ��̳�����¹����ǰ 500 �ַ���
#      ����벻������ʾ�ַ������������� max ������ֵΪ 99999999�����磺
#      <script src="getanc.cgi?max=99999999"></script>
#
#      ���в���������ʡ�ԣ�Ĭ����ʾ�����ǰ�� 500 �ַ���
###################################################################################

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
require "code.cgi";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;
$query = new LBCGI;
$max	= $query -> param('max');
$max    = &stripMETA("$max");
$max	= 500 if ($max eq "");        # Ĭ����ʾ�����ǰ 500 �ַ�

print header(-charset=>gb2312);

    $filetoopen = "$lbdir" . "data/news.cgi";
    if (-e "$filetoopen") {
    	open(FILE, "$filetoopen");
    	flock (FILE, 1) if ($OS_USED eq "Unix");
        @announcements = <FILE>;
        close(FILE);
        ($title, $dateposted, $post, $nameposted) = split(/\t/, $announcements[0]);
                
      if ($post ne "") {
        $dateposted = $dateposted + ($timedifferencevalue*3600) + ($timezone*3600);
	$dateposted = &dateformat("$dateposted");
	        
	&lbcode(\$post);
	&doemoticons(\$post);
	&smilecode(\$post);
	$title =~ s/\'/\`/;
	$title =~ s/\&amp;/\&/g;
	$title =~ s/\&quot;/\"/g;
	$title =~ s/\&lt;/</g;
	$title =~ s/\&gt;/>/g;
	$title =~ s/ \&nbsp;/��/g;
	$title =~ s/  /��/g;
	$post =~ s/\'/\`/;
	$post =~ s/\&amp;/\&/g;
	$post =~ s/\&quot;/\"/g;
	$post =~ s/\&lt;/</g;
	$post =~ s/\&gt;/>/g;
	$post =~ s/ \&nbsp;/��/g;
	$post =~ s/  /��/g;
	if (length($post)>$max) {
	    $post = &lbhz("$post",$max) . "<p align=right><a href=announcements.cgi target=_blank>More>>></a>&nbsp;</p>";
	}
	$str=qq~ 
	<table width=95% border=0 cellspacing=0 cellpadding=0>
	<tr valign=top><td height=158> 
	<b>$title</b><br>$post
	</td></tr>
	<tr valign=top><td height=18 align=right>
	<br>$nameposted����$dateposted&nbsp;
	</td></tr>
	</table>~;
      }
      else {
	$str = "��ǰû�й��棡";
      }
    }
    else {
	$str = "��ǰû�й��棡";
    }
$str=~s /\n//isg;
print "document.write('$str')\n";
exit;
