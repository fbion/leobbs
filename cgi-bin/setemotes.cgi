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

$thisprog = "setemotes.cgi";
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
        $wordarray =~ s/\n\n//ig;
        $wordarray =~ s/\n/\&/ig;

        @savedwordarray = split(/\&/,$wordarray);
        
        $filetomake = "$lbdir" . "data/emote.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / EMOTE �趨</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=���� color=#333333><center><b>������Ϣ�Ѿ����ɹ����档</b></center><br><br>
                <b>����EMOTE�����棡</b><br><br>
                );
                
                foreach (@savedwordarray) {
                    chomp $_;
                    ($toemote, $beemote) = split(/\=/,$_);
                    print qq(���г��� <b>$toemote</b> �ĵط����� <b>$beemote</b> �滻��<br>);
                }
                print qq(
                <br><br><br><center><a href="setemotes.cgi">�ٴ�����EMOTE�б�</a></center>);
        }
        else {
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / EMOTE �趨</b>
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

                $filetoopen = "$lbdir" . "data/emote.cgi";
                open (FILE, "$filetoopen");
                $emote = <FILE> if (!$emote);
                close (FILE);
                
                $emote =~ s/\&/\n/g;
        	$emote =~ s/\n\n/\n/ig;
        	$emote =~ s/\f\r//ig;

                $inmembername =~ s/\_/ /g;

                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / EMOTE �趨</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333><b>EMOTE�趨</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font face=���� color=#000000>
                EMOTE�趨����ʵ�����������ҵ�EMOTEת��,ʹ������̳���ӷḻ���.<br>
                <br>
                <b>ʹ�÷�����</b><br>1.����һ��Ҫת����EMOTE��ת����Ķ����������м���� "=" (���ں�)��<BR>
                2.ÿһ��Ҫת����EMOTEǰ����ü���/// ���������������ʻ㡣��ת����Ķ����У������󡱽��ڷ���ʱת����Ϊ�����˵�������Ҳ���Բ��������󡱣���������ȫ�������ʾ�����������趨�Ժ�Ķ�����<BR>
                <b>ע�⣺<br>1.ÿ��ֻ��дһ����<br>
                2.����Ҫת����EMOTE����,���������ģ�Ӣ�ģ��������֣���ò�Ҫ���а��״̬�µı����ţ���������������еĴ���
                <br>3.���õ�EMOTE��Ҫ�ظ�������///hi��///hide�ǲ�������ģ���ת��ʱ///hide����ת��Ϊ///hi�Ķ�����Ȼ���ڶ������渽��de��
                ����˵������///hi=����˵������Һá�����ô///hide������ʾ������˵������Һá���de����///hi��///sohi��������ġ�</b><br><br>
                <b>���磺</b>///bug=�������һ�֣�˵���������Ǻ��棬����˭����<br>
                �����������"��������"����仰�ڲ鿴����ʱ����ʾ:<br>
                ���������졽����һ�֣�˵���������Ǻ��棬����˭����<br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=60 rows=15 wrap="virtual" name="wordarray">$emote</textarea>
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
