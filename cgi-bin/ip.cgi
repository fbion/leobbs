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
require "data/boardinfo.cgi";
use testinfo qw(ipwhere osinfo browseinfo);

print "Content-type: text/html\n\n";

$ipaddress     = $ENV{"REMOTE_ADDR"};
$trueipaddress = $ENV{"HTTP_CLIENT_IP"};
$trueipaddress = $ENV{"HTTP_X_FORWARDED_FOR"} if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
$trueipaddress = $ipaddress if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
$fromwhere1 = &ipwhere("$trueipaddress");
print "���� IP ��ַ��$trueipaddress����Դ������$fromwhere1<BR>";
if ($ipaddress ne $trueipaddress) { $fromwhere2 = &ipwhere("$ipaddress"); print "���� IP ��ַ��$ipaddress����Դ������$fromwhere2<BR>"; } else { print "���� IP ��ַδ֪(û��ʹ�ô������������ IP ��ʾ����ֹ)"; }
eval { $osinfo=&osinfo(); };
if ($@) { $osinfo="Unknow"; }
eval { $browseinfo=&browseinfo(); };
if ($@) { $browseinfo="Unknow"; }
print "<BR><BR>���Ĳ���ϵͳ�ǣ�$osinfo��ʹ�õ�������ǣ�$browseinfo<BR>($ENV{\"HTTP_USER_AGENT\"})<BR>";
