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
require "data/cityinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setcity.cgi";

$query = new LBCGI;

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
	$theparam =~ s/\\/\\\\/g;
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/"//g;
        $theparam =~ s/'//g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
            $printme .= "\$" . "$_ = \'$theparam\'\;\n";
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");
        
        
if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {

    
    if ($action eq "process") {

        
        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/cityinfo.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / �����ṹ</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=���� color=#333333><center><b>������Ϣ�Ѿ��ɹ�����</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                print $printme;
                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                    <b>��ӭ������̳�������� / ��������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=���� color=#333333><b>������Ϣû�б���</b><br>�ļ�����Ŀ¼����д<br>������� data Ŀ¼�� cityinfo.cgi �ļ������ԣ�
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                
            }
            else {
                $inmembername =~ s/\_/ /g;
                $moneyname ="�װ�Ԫ" if ($moneyname eq "");
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / ��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>������������</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�������Ʒ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="moneyname" value="$moneyname" maxlength=6> Ĭ�ϣ��װ�Ԫ<BR>����޸ģ����޸ĺ���̳��ʼ������� Cache һ��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�Ƽ�һ�������ӵĻ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addtjhb" value="$addtjhb"> Ĭ�ϣ�100</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�������������ӵĻ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addjhhb" value="$addjhhb"> Ĭ�ϣ�100</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�Ƽ�һ�������ӵĻ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addtjjf" value="$addtjjf"> Ĭ�ϣ�0</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ��һ����������Ļ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="ttojf" value="$ttojf"> Ĭ�ϣ�2</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ��һ���ظ�����Ļ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="rtojf" value="$rtojf"> Ĭ�ϣ�1</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�α�ɾ�����Ӽ�ȥ�Ļ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="deltojf" value="$deltojf"> Ĭ�ϣ�3</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>���û�ע�����Ļ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="joinjf" value="$joinjf"> Ĭ�ϣ�10</td>
                </tr>  
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�η������ӵĻ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="addmoney" value="$addmoney"> Ĭ�ϣ�10</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�λظ����ӵĻ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="replymoney" value="$replymoney"> Ĭ�ϣ�8</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�ε�¼���ӵĻ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="loginmoney" value="$loginmoney"> Ĭ�ϣ�15</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�α�ɾ�����Ӽ�ȥ�Ļ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="delmoney" value="$delmoney"> Ĭ�ϣ�20</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>���û�ע�����Ļ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=20 name="joinmoney" value="$joinmoney"> Ĭ�ϣ�1000</td>
                </tr> 

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>���Ͷ���Ϣʱ��Ҫ�ɽ��ķ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=4 name="msgmm" value="$msgmm" maxlength=4> �粻��Ҫ�������գ��˹��ܶ԰�����̳����Ч</td>
                </tr>  

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>ÿ�η�С�ֱ����ѵĻ���</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=4 name="xzbcost" value="$xzbcost" maxlength=4> �粻��Ҫ��������</td>
                </tr>  
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
                ~;
                
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;
