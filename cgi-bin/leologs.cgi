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

$thisprog = "leologs.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

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
        
                if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
           $filetoopen = "$lbdir" . "data/baddel.cgi";
           unlink $filetoopen;
           print qq~
           <tr><td bgcolor=#2159C9"><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ɾ����־</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center>
		<font color=#333333><b>�ļ�ɾ��������־</b>
		</td></tr>
		<tr><td align=center><br><br>��ȫ��־�Ѿ�ɾ��!</td></tr>
           ~;
         
                }
        
        }
        
    else {
        
        &getmember("$inmembername","no");
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $filetoopen = "$lbdir" . "data/baddel.cgi";
                open (FILE, "$filetoopen");
                @baddel = <FILE>;
                close (FILE);
                
                print qq(
                <tr><td bgcolor=#2159C9" colspan=6><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ɾ����־</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=6>
		<font color=#333333><b>�ļ�ɾ��������־</b>
		</td></tr>
		<tr><td>������</td><td>����</td><td>IP��ַ</td><td>����IP</td><td>������̳</td><td>����ʱ��</td></tr>
		);
		foreach (@baddel){
		(my $name, my $pass, my $ip, my $proxy, my $forums,my $oldtime) = split(/\t/,$_);
		&getoneforum($forums);
		print qq~
		<tr><td>$name</td><td>$pass</td><td>$ip</td><td>$proxy</td><td>$forumname [ID:$forums]</td><td>$oldtime</td></tr>
		~;
		}
                print qq~
                <tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=6><br>
		<font color=#333333><b><a href=$thisprog?action=process>ɾ����ȫ��־</a></b>
		</td></tr>
                ~;
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
