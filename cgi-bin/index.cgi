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
$LBCGI::POST_MAX=20000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;

require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}

$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
$action = $query -> param('action');

if ($action eq "change_skin") {
    if ($inmembername eq "") { $inmembername = "����"; }
    else {
    &getmember("$inmembername","no");
    &error("��ͨ����&�ϴ�͵�û�����͵������ʲô���أ�") if ($inpassword ne $password);
    &error("��ͨ����&�û�û�е�¼��ע�ᣡ") if ($userregistered eq "no");  
    }
   $refrashurl = $query -> param('thisprog');
   $refrashurl = "leobbs.cgi" if($refrashurl eq "");
   $refrashurl = uri_escape($refrashurl);
#   unlink ("${lbdir}cache/myinfo/$inmembername.pl");
   $inselectstyle   = $query->param("skin");
#   $inselectstyle = "" if (lc($inselectstyle) eq "leobbs");
   &error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
   my $selectstylecookie= cookie(-name => "selectstyle" , -value => $inselectstyle, -path => "$cookiepath/");
   print header(-cookie  =>[$selectstylecookie], -charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
   print qq ~<script>location.href="$refrashurl";</script>~;
   print qq~ҳ���Ѿ����£������Զ�ˢ�£����û���Զ�ˢ�£����ֹ�ˢ��һ�Σ���<BR><BR><meta http-equiv="refresh" content="3; url=$refrashurl">~;
   exit;
}
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print "<script language='javascript'>document.location = 'leobbs.cgi'</script>";
print qq~ҳ���Ѿ����£������Զ�ˢ�£����û���Զ�ˢ�£����ֹ�ˢ��һ�Σ���<BR><BR><meta http-equiv="refresh" content="3; url=leobbs.cgi">~;
exit;
