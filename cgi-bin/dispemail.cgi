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

require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "dispemail.cgi";

$query = new LBCGI;

my $allow_eamil_file = "${lbdir}data/allow_email.cgi";
if(-e $allow_eamil_file){
	open(AEFILE,$allow_eamil_file);
	$allowtype = <AEFILE>;
	$allowmail = <AEFILE>;
	close(AEFILE);
	chomp $allowtype;
	chomp $allowmail;
}

$allowmail =~s/\t+/\t/g;
$allowmail =~s/^\t//;
$allowmail =~s/\t$//;
$allowmail =~s/\t/<br>/g;

$lbbody = 'topmargin="0" bottommargin="0" leftmargin="0" rightmargin="0"';
$allowtype_d = ($allowtype eq "allow")?'����ʹ�������������ע��':'������ʹ����������ע��';

$output = <<"HTML";
<table cellpadding=0 cellspacing=0 width=100% height="90%" bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100% height="100%">
<tr>
<td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>$allowtype_d</b></font></td></tr>
<td bgcolor=$miscbackone height="90%" valign="top"><font color=$fontcolormisc>$allowmail</font></td></tr>
</table>
</td></tr>
</table><br>
HTML

print header( -charset => gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output("$boardname - ��������",\$output,'msg');
exit;
