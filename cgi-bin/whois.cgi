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
use IO::Socket;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$queryme = new LBCGI;
$inmembername   = $queryme->cookie("amembernamecookie");
$inpassword     = $queryme->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$query          = $queryme -> param('query');

if (($query eq "")||($query !~ /^[0-9\.]+$/)) {
    &error("��ͨ����&�벻Ҫ����ʹ�ñ����ܣ�") ;
}
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
my $host = "sunny.nic.com";
my $path = "/cgi-bin/whois";
my $content = "domain=$query";
my $port = 80;
my $socketaddr;
openSock();
post ($content);
@wholePage = <SOCK>;
close SOCK;
$out = join("",@wholePage);

$out =~ s/(.*?)(<pre>)(.+?)(<\/pre>)(.*?)/<pre>$3<\/pre>/isg;
$out =~ s/<br \/>//isg;
$out =~ s/<p>.*<\/p>//isg;
$out =~ s/<hr>(.*)$//isg;
$out =~ s/<\/pre>(.*)$//isg;
$out = "��ѯ���̫�̣��޷���ȡ��ϸ��Ϣ�����Ժ����ԣ�<BR><BR><BR>" if ($out =~ m/Forbidden/);
$out = qq~LeoBBS WHOIS ��ϸ��Ϣ($query)��<BR>������Դ��<a href=http://sunny.nic.com/cgi-bin/whois>NIC Whois</a><BR><BR><BR>~ . $out . "<center><hr width=500><font color=black>��Ȩ���У�<a href=http://www.leobbs.com target=_blank>�װ��Ƽ�</a> & <a href=http://bbs.leobbs.com target=_blank>�װ����ᳬ����̳</a>����Copyright 2003-2004<BR>";
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print $out;
exit;


sub openSock {
$socketaddr= sockaddr_in $port, inet_aton $host or return(1);  
#print "Connecting to $socketaddr $host, $port";
socket SOCK, PF_INET, SOCK_STREAM, getprotobyname('tcp') or return(1);
connect SOCK, $socketaddr or return(1);
select((select(SOCK), $| = 1)[0]);
return (0);
}
 
sub post {
my $content = shift @_;
print SOCK "POST http://$host/$path HTTP/1.0\n";
print SOCK "Content-type: application/x-www-form-urlencoded\n";
my $contentLength = length $content;
print SOCK "Content-length: $contentLength\n";
print SOCK "\n";
print SOCK "$content";
}
