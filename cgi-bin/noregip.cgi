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
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "noregip.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
$userarray     = $query -> param('userarray');
$action        = $query -> param("action");
$action        = &cleaninput("$action");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");
            
if ($action eq "process") {
    if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
	$userarray .= "\n";
	$userarray =~ s/\t//isg;
	$userarray =~ s/\r\n/\n/ig;
	$userarray =~ s/\n+/\n/ig;
	$userarray =~ s/\n/\t/isg;
        $userarray =~ s/\*\[\]\(\)\?\+\=\|//isg;
        $filetomake = "$lbdir" . "data/baniplist.cgi";
        open (FILE, ">$filetomake");
        print FILE $userarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
	    print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>��ӭ������̳��������</b>
            </td></tr><tr><td bgcolor=#FFFFFF colspan=2><font color=#333333><center><b>���е���Ϣ�Ѿ�����</b></center><br><br>
            <b>���Ѿ���ֹ������ IP ��ʹ����Щ IP ���û������������롣</b><br><br>~;
            
            @saveduserarray = split(/\t/,$userarray);
            foreach (@saveduserarray) {
                chomp $_;
                print "$_<br>";
	    }
            print qq~<br><br><br><center><a href="noregip.cgi">��ֹ��������� IP ��ַע���û�</a></center>~;
	}
        else {
	    print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>��ӭ������̳��������</b></td></tr><tr>
            <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>���е���Ϣû�б���</b><br>���ļ���Ŀ¼Ϊ����д������������ 777 ��
            </td></tr></table></td></tr></table>~;
	}
    }
    else {
        &adminlogin;
    }

}
else {
    if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
        open (FILE, "${lbdir}data/baniplist.cgi");
        my $badusers = <FILE>;
        close (FILE);
        $badusers =~ s/\t/\n/g;
        print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>��ӭ������̳�������� / ��ֹһЩ����� IP ��ַע���û�</b></td></tr><tr>
	    <td bgcolor=#EEEEEE align=center colspan=2><font color=#333333><b>��ֹһЩ����� IP ��ַע���û�</b></td></tr>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="process">
            <tr><td bgcolor=#FFFFFF colspan=2><font color=#000000>
            <b>��ע�⣺</b> �˹�����������ֹһЩ����� IP ��ַ��ʹ����Щ IP ���û���������ע�ᡣ����������ֹһЩ���ҵ��˶��ע���û���<BR><BR>�����ʱ��ÿ������һ�� IP ��ַ����(�����������������磺 202.96.111.42 )��<BR><BR>
            </font></td></tr>
            <tr><td bgcolor=#FFFFFF align=center colspan=2>
            <textarea cols=60 rows=18 wrap="virtual" name="userarray">$badusers</textarea><BR><BR>
            </td></tr>
            <tr><td bgcolor=#EEEEEE align=center colspan=2>
            <input type=submit name=submit value="�� ��"></td></form></tr></table></td></tr></table>~;
    }
    else {
	&adminlogin;
    }
}
print qq~</td></tr></table></body></html>~;
exit;
