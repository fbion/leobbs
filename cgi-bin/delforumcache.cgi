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

$inforum = $queryme -> param('forum');
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ����") if (($inforum !~ /^[0-9]+$/)||($inforum eq ""));

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
&getoneforum("$inforum");
if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")){
    &error("��ͨ����&�㲻�Ǳ���̳�Ĺ���Ա�����Բ���ʹ�øù��ܣ�") if ($membercode ne "amo");
}
unlink ("${lbdir}cache/forums$inforum.pl");
unlink ("${lbdir}cache/forumshead$inforum.pl");
unlink ("${lbdir}cache/forumsone$inforum.pl");
unlink ("${lbdir}cache/forumstitle$inforum.pl");
unlink ("${lbdir}cache/forumstop$inforum.pl");
unlink ("${lbdir}cache/forumstopic$inforum.pl");
unlink ("${lbdir}cache/forumstoptopic$inforum.pl");

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata1 = grep(/^plcache$inforum\_/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^threadages$inforum\_/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print qq~
<SCRIPT>
alert("���������л��涼������ˣ�");
document.location = 'forums.cgi?forum=$inforum'
</SCRIPT>
~;
exit;
