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

$queryme = new LBCGI;
$inmembername   = $queryme->cookie("amembernamecookie");
$inpassword     = $queryme->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ((!$inmembername) or ($inmembername eq "����")) {
    $inmembername = "����";
    &error("��ͨ����&�Բ������ȵ�¼����ʹ�ñ����ܣ�")
}
else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("��ͨ����&�ϴ�͵�û�����͵������ʲô���أ�") if ($inpassword ne $password);
    &error("��ͨ����&�û�û�е�¼��ע�ᣡ") if ($userregistered eq "no");  
}

$cleanmembername = $inmembername;
$cleanmembername =~ s/ /\_/isg;
$cleanmembername =~ tr/A-Z/a-z/;
unlink ("${lbdir}cache/myinfo/$cleanmembername.pl");
unlink ("${lbdir}cache/meminfo/$cleanmembername.pl");
unlink ("${lbdir}cache/mymsg/$cleanmembername.pl");
unlink ("${lbdir}cache/online/$cleanmembername.pl");
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print qq~
<SCRIPT>
alert("������̳�����л��涼������ˣ�");
document.location = 'leobbs.cgi'
</SCRIPT>
~;
exit;
