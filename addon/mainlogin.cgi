#!/usr/bin/perl
#############################################################
#  ����: 1.�Կ�����ʾ��¼��, 2.���Ե�¼����ʾ��ӭ��Ϣ,
#
#  ˵��: �����ļ����Ƶ� leobbs.cgi ͬĿ¼��,
#        ����ҳ���ϴ���:
#        <SCRIPT type="text/javascript" language="javascript" src="��̳url��ַ/mainlogin.cgi"></SCRIPT>
#
#############################################################

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

use LBCGI;
$LBCGI::POST_MAX=2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "mainlogin.cgi";
$query = new LBCGI;

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
}
else {
    &getmember("$inmembername");
    $inmembername = "����" if ($userregistered eq "no");
}

if ($inmembername eq "����") {
    $str = qq~<FORM name=login action="$boardurl/loginout.cgi" method=post><INPUT type=hidden value=login name=action><INPUT type=hidden name=forum><BR>�û���<INPUT size=10 name=inmembername><BR>���룺<INPUT type=password size=10 name=inpassword><BR>Cookie <SELECT name=CookieDate><OPTION value="0" selected>������</OPTION><OPTION value=+1d>����һ��</OPTION><OPTION value=+30d>����һ��</OPTION><OPTION value=+20y>���ñ���</OPTION></SELECT><BR><INPUT type=submit value=���� name=Submit><INPUT type=reset value=ȡ�� name=Submit></FORM><A target=_blank href="$boardurl/leobbs.cgi">�ι�</A> <A target=_blank href="$boardurl/register.cgi">ע��</A> <A target=_blank href="$boardurl/profile.cgi?action=lostpassword">��������</A><BR>~;
}
else {
    $str = qq~<BR>��ӭ��<BR>$inmembername<BR><BR><A target=_blank href="$boardurl/leobbs.cgi">����</A> <A target=_blank href="$boardurl/loginout.cgi">�ص�¼</A> <A href="$boardurl/loginout.cgi?action=logout">�˳�</A><BR>~;
}

print header(-charset=>gb2312);
print "document.write('$str')\n";
exit;
