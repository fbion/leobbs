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
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$thisprog = "setregrules.cgi";

$query = new LBCGI;

$rules        = $query -> param('therules');
$action       = $query -> param("action");
$action       = &cleaninput("$action");

$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
            
        &getmember("$inmembername","no");
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

if ($action eq "process") {
        
        $rules =~ s/\n\n/\n/ig;
        $rules =~ s/\s+/\n/ig;

        $filetomake = "$lbdir" . "data/register.dat";
        open (FILE, ">$filetomake");
        print FILE $rules;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <font color=#333333><center><b>������Ϣ�Ѿ�����</b></center><br><br>
                <b>ע������������Ѿ�����.Ŀǰ��ע��������������£�</b><br><HR><ul>$rules</ul>
                <HR><br><br><br><center><a href="setregrules.cgi">�޸�ע�����������</a></center>);
                }
                else {
                    print qq(
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>��ӭ������̳��������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                    <font color=#333333><b>��Ϣ�޷�����</b><br>�ļ�����Ŀ¼����д��
                    </td></tr></table></td></tr></table>
                    );
                    }
                }
        
    else {

                $filetoopen = "$lbdir" . "/data/register.dat";
                open (FILE, "$filetoopen") or $rules = "����ע�����������";
                @rules = <FILE> if (!$rules);
                close (FILE);

                $inmembername =~ s/\_/ /g;

                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / ע���������������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font color=#333333><b>����ע�����������</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle colspan=2>
                <br>
                <b>ע��:</b>������ʹ�� HTML ��������ʹ�� LeoBBS ��ǩ��<br>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <textarea cols=70 rows=15 wrap="virtual" name="therules">);
		                foreach (@rules) {
		                   $rules = $_;
		                   #$rules =~ s/\n//isg;
		                   print qq($rules);
		                }
		                print qq(</textarea>
                </td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit name=submit value=�ύ></form></td></tr></table></td></tr></table>
                );
                
        }
                }
                else {
                    &adminlogin;
                    }

print qq~</td></tr></table></body></html>~;
exit;
