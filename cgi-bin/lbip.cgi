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
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
use testinfo qw(ipwhere);

$queryme = new LBCGI;
$inmembername   = $queryme->cookie("amembernamecookie");
$inpassword     = $queryme->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$query = $queryme -> param('q');
if ((!$inmembername) or ($inmembername eq "����")) {
    $inmembername = "����";
}
else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("��ͨ����&�ϴ�͵�û�����͵������ʲô���أ�") if ($inpassword ne $password);
    &error("��ͨ����&�û�û�е�¼��ע�ᣡ") if ($userregistered eq "no");  
}
if (($membercode ne "ad")&&($membercode ne "smo")){
    &error("��ͨ����&�㲻�Ǳ���̳��̳�����ܰ������Բ���ʹ�øù��ܣ�") ;
}

if (($query ne "")&&($query !~ /^[0-9\.]+$/)) {
    &error("��ͨ����&�벻Ҫ����ʹ�ñ����ܣ�") ;
}
if ($query ne "") { $fromwhere = &ipwhere("$query"); $fromwhere = "�ɣ�: $query\n<BR>����: $fromwhere\n<BR><BR>����Խ�������ʣ���<a href=whois.cgi?query=$query>����ʹ�� NIC ���ݿ��ѯ</a>��"} else { $fromwhere = "û��IP����,�Ҳ�ʲô��!"; }
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print $fromwhere;
exit;
