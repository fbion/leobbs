#!/usr/bin/perl
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

#unless ($ENV{"HTTP_REFERER"} =~ /$ENV{"HTTP_HOST"}/i)
#{
#	print "Content-Type: text/html\n\n";
#	print "document.write('<font color=red>���Բ��𣬲�����Ǳ���̳�������ã�</font>');";
#	exit;
#}

use LBCGI;
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;

$query = new LBCGI;
$thisprog = "showmem.cgi";

&ReadParse;
$show = $in{"show"};
$show = 10 if ($show < 1);
$|++;

print "Content-type: text/html; charset=gb2312\n\n";

$filetoopen = "${lbdir}data/onlinedata.cgi";
open(FILE, $filetoopen);
@onlinedata1 = <FILE>;
close(FILE);

$filetoopen = "${lbdir}data/lbmember0.cgi";
open(FILE, $filetoopen);
@members = <FILE>;
close(FILE);

$str = "";
$str.= "<table cellSpacing=0 cellPadding=0 border=0 width=100%>";
$str.= "<tr><td align=center><b>����</b></td><td align=center><b>������</b></td><td align=center><b>״̬</b></td></tr>";

for ($i = 0; $i < $show && $i < @members; $i++)
{
	my ($membername, $post) = split(/\t/, $members[$i]);
	my $memberstat = grep(/^$membername\t/i, @onlinedata1) ? "<font color=#ff0000>����</font>" : "������";
	my $name = $uri_escape eq "no" ? $membername : uri_escape($membername);
	$str .= "<tr><td align=center><a href=$boardurl/profile.cgi?action=show&member=$name target=_blank>$membername</a></td><td align=center>$post</td><td align=center>$memberstat</td></tr>";
}

$str .= "</table>";
print "document.write('$str');";
exit;

sub ReadParse
{
	$buffer = $ENV{"QUERY_STRING"};
	@pairs = split(/&/, $buffer);
	foreach (@pairs)
	{
		($name, $value) = split(/=/, $_);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ s/<!--(.|\n)*-->//g;
		$value =~ s/__/--/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/</&lt;/g;
		$value =~ s/\t//g;
		$in{$name} = $value;
	}
	return;
}