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

$thisprog = "setbadwords.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$wordarray     = $query -> param('wordarray');
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
 
 	$wordarray =~ s/[\f\n\r]+/\n/ig;
	$wordarray =~ s/[\r \n]+$/\n/ig;
	$wordarray =~ s/^[\r\n ]+/\n/ig;
        $wordarray =~ s/\n\n//g;
        $wordarray =~ s/\n/\&/g;

        @savedwordarray = split(/\&/,$wordarray);
        
        $filetomake = "$lbdir" . "data/badwords.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=���� color=#333333><center><b>������Ϣ�Ѿ����ɹ����档</b></center><br><br>
                <b>���С������Զ�ת���������棡</b><br><br>
                );
                
                foreach (@savedwordarray) {
                    chomp $_;
                    ($bad, $good) = split(/\=/,$_);
                    print qq(���г��� <b>$bad</b> �ĵط����� <b>$good</b> �滻��<br>);
                }
                print qq(
                <br><br><br><center><a href="setbadwords.cgi">�ٴ����Ӵ����Զ�ת��</a><br></center>);
        }
        else {
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#333333><b>��Ϣû�б����棡</b><br>�ļ�����Ŀ¼����д��
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
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
                # Open the badword file

                $filetoopen = "$lbdir" . "data/badwords.cgi";
                open (FILE, "$filetoopen") or $badwords = "damn=d#amn\nhell=h#ll";
                $badwords = <FILE> if (!$badwords);
                close (FILE);
                
                $badwords =~ s/\&/\n/g;
        	$badwords =~ s/\n\n/\n/ig;
        	$emote =~ s/\f\r//ig;

                $inmembername =~ s/\_/ /g;

                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / �����Զ�ת��</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333><b>�����Զ�ת��</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=���� color=#000000>
                �����Զ�ת��������ֹһЩ���õ����۳�������̳�С����������д������ת����Ĵ��<br>
                ��������Щ������<b>��������</b>ʱ���ᱻ�Զ�ת����<br>
                <b>ʹ�÷�����</b>ʹ�÷�����</b>д��һ�������ת����Ĵ�������м���� "=" (���ں�)��<BR><br>
		<b>�ر���ʾ��</b>���������ǹ��ˣ������ں�ת����Ĵ����ô��ʹ��"<a href=setfilter.cgi>�����������</a>"���ܣ������������Ч�ʣ�<BR><BR><BR>
                <b>ע��1���뾡�����ٴ����Զ�ת������Ŀ����ʹ��"<a href=setfilter.cgi>�����������</a>"���ܣ�</b><br><br>
                <b>ע��2��ÿ��ֻ��дһ����</b><br><br>
                <b>ע��3����������ʹ�� * ( ) ֮��ķ��ţ�</b><br><br>
                <b>���磺</b>fuck=f##k<br><br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=60 rows=20 wrap="virtual" name="wordarray">$badwords</textarea>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <input type=submit name=submit value="�� ��"></form></td></tr></table></td></tr></table>
                );
                
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
