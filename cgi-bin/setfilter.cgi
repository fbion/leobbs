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
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "setfilter.cgi";
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
            
if ($action eq "process") {
    &getmember("$inmembername","no");
    if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

	$userarray .= "\n";
        $userarray =~ s/[\a\f\e\0\r\t\|]//isg;
	$userarray =~ s/\r\n/\n/ig;
	$userarray =~ s/\n+/\n/ig;
	$userarray =~ s/\n/\t/isg;
	$userarray =~ s/����������//isg;

        @saveduserarray = split(/\t/,$userarray);
        
        $filetomake = "$lbdir" . "data/wordfilter.cgi";
        open (FILE, ">$filetomake");
        print FILE $userarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                
		print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><center><b>���е���Ϣ�Ѿ�����</b></center><br><br>
                <b>���в������ﱻ���棬��Щ�ʻ�����̳�н��Զ��� ****** �滻��</b><br><br>
                );
                
                foreach $user(@saveduserarray) {
                    chomp $user;
                    print qq($user<br>);
                }
                print qq(<br><br><br><center><a href="setfilter.cgi">��������Ҫ���˵Ĳ�������</a></center>);
	}
        else {
		print qq(
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>��ӭ������̳��������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF align=center colspan=2>
                    <font color=#333333><b>���е���Ϣû�б���</b><br>���ļ���Ŀ¼Ϊ����д������������ 777 ��
                    </td></tr></table></td></tr></table>
                );
	}
    }
    else {
        &adminlogin;
    }

}
else {
        
        &getmember("$inmembername","no");
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
		$badusers = "";
                $filetoopen = "$lbdir" . "data/wordfilter.cgi";
                open (FILE, "$filetoopen");
                $badusers = <FILE>;
                close (FILE);
                
                $badusers =~ s/\t/\n/g;
                $badusers =~ s/\&/\&amp;/g;

                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / �����������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>�����������</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#000000>
                <b>��ע�⣺</b> �˹�����������һЩ�����ʻ���й��ˡ�����������Щ�����ʻ�����ӽ��޷�������
                <BR><BR>�����ʱ��ÿ������һ�������ʻ㼴�ɡ�<BR><BR>
                �ر�ע�⣺������� | �ַ����й��ˡ�<BR><BR>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF align=center colspan=2>
                <textarea cols=60 rows=20 wrap="virtual" name="userarray">$badusers</textarea><BR><BR>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <input type=submit name=submit value="�� ��"></td></form></tr></table></td></tr></table>
                );
                
	}
	else {
	    &adminlogin;
	}
}
print qq~</td></tr></table></body></html>~;
exit;
