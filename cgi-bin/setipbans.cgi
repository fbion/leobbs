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

$thisprog = "setipbans.cgi";

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
        
                if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 

        $wordarray =~ s/\s+/\n/ig;
        $wordarray =~ s/\n\n/\n/ig;
        $wordarray =~ s/[^0-9\.\-\n\.\$]//isg;

        $wordarray2display = $wordarray;
        $wordarray2display =~ s/\n/<br>/g;

        $filetomake = "$lbdir" . "data/ipbans.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);

    opendir (DIRS, "${lbdir}cache/id");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	$_ =~ s/\.cgi//isg;
    	unlink ("${lbdir}cache/id/$_\.cgi");
    }


        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / IP ��ֹ</b>
		</td></tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#333333><center><b>���е���Ϣ�Ѿ�����</b></center><br><br>
		<b>���Ѿ������� IP �����˴�����һ���ַ��� - ��Ϊ��ֹ��</b><br><br>
		);
                    print qq(<b>$wordarray2display</b><br>);
                print qq(
                <br><br><br><center><a href="setipbans.cgi">�ٴ�����һЩ��ֹ�� IP</a></center>);
                }
                else {
                    print qq(
                    <tr><td bgcolor=#2159C9" colspan=2><font color=#FFFFFF>
			<b>��ӭ���� LeoBBS ��̳��������</b>
			</td></tr>
			<tr>
			<td bgcolor=#FFFFFF valign=middle align=center colspan=2>
			<font color=#333333><b>���е���Ϣû�б���</b><br>���ļ���Ŀ¼Ϊ����д������������ 777 ��
                    	</td></tr></table></td></tr></table>
		     	);
                    }
                }
        }
        
    else {
        
        &getmember("$inmembername","no");
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

                $filetoopen = "$lbdir" . "data/ipbans.cgi";
                open (FILE, "$filetoopen");
                @bannedips = <FILE>;
                close (FILE);
                
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / IP ��ֹ</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>IP ��ֹ�б�</b>
		</td></tr>
		<form action="$thisprog" method="post">
		<input type=hidden name="action" value="process">
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#000000>
		<b>��ע��:</b>������ֹ��һ�� IP �Ļ�����ô��� IP ���޷�������̳��<br>
		<br>
                    <table width="100%" border="1" height="122" cellspacing="0" cellpadding="0">
                      <tr> 
                        <td width="34%"> 
                          <div align="center">����</div>
                        </td>
                        <td width="33%"> 
                          <div align="center">����</div>
                        </td>
                        <td width="33%"> 
                          <div align="center">����</div>
                        </td>
                      </tr>
                      <tr> 
                        <td height="51" width="35%">���г��ĵ��������ε�ַΪ�����ַ<br>
                          ����ipǰ�ӡ�-��Ϊ������<br>
                          ��ͬһ���εģ�Ӧ����ַ��ǰ</td>
                        <td height="51" width="33%"> 
                          <p>80.32.96.11<br>
                            -80.32.96.<br>
                            <br>
                            ע��������80.32.96�Σ�ֻ����80.32.96.11<br>
                          </p>
                        </td>
                        <td height="51" width="33%">-80.32.96.11 <br>
                          80.32.96.<br>
                          <br>
                          ע������80.32.96�Σ�������80.32.96.11</td>
                      </tr>
                      <tr> 
                        <td> 
                          <div align="center">��ע</div>
                        </td>
                        <td>&nbsp;</td>
                        <td>&nbsp;</td>
                      </tr>
                      <tr> 
                        <td colspan="3">˵���������г��ĵ�ַĬ��Ϊ��������ע��</td>
                      </tr>
                      <tr>
                        <td colspan="3">˵��������ַ������λ����߲��ò�������Ҫ��������Ŷ����</td>
                      </tr>
                      <tr> 
                        <td colspan="3">˵�����������Ҫ��ֹһ�� B ��������ô����Բ����� IP �������λ�����磺202.100.��</td>
                      </tr>
                      <tr>
                        <td colspan="3">˵������ע�������д���������ֹ����һ�� C ����� B ����������������(.)���мǣ�</td>
                      </tr>
                      <tr> 
                        <td colspan="3">˵������ÿ��дһ�� IP��ע�����س���</td>
                      </tr>
                      <tr> 
                        <td colspan="3">˵���������Ҫ������210.126.1.������IP�Σ�����-210.126.1\.��</td>
                      </tr>
                      <tr> 
                        <td colspan="3">˵���������Ҫ������210.126.1.4������IP�Σ�����-210.126.1.4\$ ��</td>
                      </tr>
                    </table>
	                </font></td>
		</tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=center colspan=2>
		<textarea cols=60 rows=22  name="wordarray">);
		                foreach (@bannedips) {
		                   $singleip = $_;
		                   chomp $_;
		                   next if ($_ eq "");
		                   #$singleip =~ s/\n\s/\n/g;
		                   print qq($singleip);
		                }
		                print qq(</textarea><BR>
		</td>
		</tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<input type=submit name=submit value=�ύ></td></form></tr></table></td></tr></table>
);
                
                }
                else {
                    &adminlogin;
                    }
        }
print qq~</td></tr></table></body></html>~;
exit;
