#!/usr/bin/perl
###################################################################################
#	LeoBBS ������ʾ ver 1.5 a (tinha �޸İ�)
###################################################################################
#	ʹ�ð취�� getanc2.cgi?show=��ʾ�Ĺ�����Ŀ&maxlength=���ⳤ��&forum=����̳���
#	����������ҳ���ʵ�λ�ü����������
#	<script src="getanc2.cgi?show=5&maxlength=20&forum=1"></script>
#	�����Ϳ�������ҳ��ʾ��� 1 �ŷ���̳������ 5 �򹫸棬-����� 20 ��Ԫ��
#	������ʾ����̳���棬���԰� &forum=����̳��� ʡȥ��
#	��������������ʡ�ԣ�Ԥ����ʾ���й��棬������ʾ������Ԫ��
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
#print "document.write('<font color=red> �Բ��𣬲���\��\�Ǳ���̳�������ã�</font>');";
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
$show = $query -> param('show');
$show = 999 if ($show eq "");	# Ԥ����ʾ���й���
$maxlength = $query -> param('maxlength');
$maxlength = &stripMETA("$maxlength");
$maxlength = 999999999 if ($maxlength eq "");	 # Ԥ�������ʾ������Ԫ
$forum = $query -> param('forum');

print header(-charset=>gb2312);

if ($forum ne "") { $filetoopen = "$lbdir" . "data/news$forum.cgi";}
else { $filetoopen = "$lbdir" . "data/news.cgi";}

if (-e "$filetoopen") {
	open(FILE, "$filetoopen");
	@announcements = <FILE>;
	close(FILE);

	$lines = @announcements - 1;
	$show = $show - 1;
	if ($lines < $show) { $show = $lines;}

	foreach $announcements (@announcements [0 ... $show]) {
		($title, $dateposted, undef, $nameposted) = split(/\t/, $announcements);
		$dateposted = $dateposted + ($timedifferencevalue*3600) + ($timezone*3600);
		$dateposted = &dateformatshort("$dateposted");
		$newstitleid++;

		if (length($title) > $maxlength) { $title = &lbhz("$title",$maxlength);}
		        $title =~ s/\'/\`/;
			$title =~ s/\&/\&amp;/g;
			$title =~ s/\&amp;\#/\&\#/isg;
			$title =~ s/\&amp\;(.{1,6})\&\#59\;/\&$1\;/isg;
			$title =~ s/\&\#([0-9]{1,6})\&\#59\;/\&\#$1\;/isg;
			$title =~ s/\"/\&quot;/g;
			$title =~ s/</\&lt;/g;
			$title =~ s/>/\&gt;/g;
			$title =~ s/ /\&nbsp;/g;

		if ($forum ne "") { $showforum = "?forum=$forum";}
		else { $showforum = "";}

		$str.= qq~
		<tr align=left><td><font style="font-size:12pt;font-family:����"><a href=$boardurl/announcements.cgi$showforum#title$newstitleid target=_blank>$title</a></font></td></tr>
		<tr align=right valign=top><td><font style="font-size:9pt;����">$nameposted ������ $dateposted</font></td></tr><tr><td>  </td></tr>
		~;
		}
	}
else {
$str = "Ŀǰû�й��棡";
}
$str=~s /\n//isg;
print "document.write('<table width=100% border=0 cellspacing=0 cellpadding=0>$str</table>')\n";
exit;

