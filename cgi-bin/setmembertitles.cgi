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
require "data/membertitles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setmembertitles.cgi";

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
          
if ($action eq "process") {
        &getmember("$inmembername","no");
        
        if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) { 
        	
        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/membertitles.cgi";

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
                <b>��ӭ������̳�������� / �û��ȼ�</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333><b>������Ϣ�ѱ���</b>
                </td></tr></table></td></tr></table>
                ~;
            }

        else {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333><b>���е���Ϣû�б���</b><br>���ļ���Ŀ¼Ϊ����д������������ 777 ��
                </td></tr></table></td></tr></table>
                ~;
            }
        
   }

   else {
       &adminlogin;
   }
        
}
        
else {
        
        &getmember("$inmembername","no");
        
                if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
                
                $inmembername =~ s/\_/ /g;
                
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / �û��ȼ�</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333><b>�û��ȼ�����</b>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                <b>����㲻��Ҫ��ô��ļ�����ô���԰ѵ��ں͸����㶨�����߼���Ļ�����ȫ����Ϊ 999999999 ���������ε��߼��𡣱��磺�㶨����߼�����5����ô���Ӧ�ð� 5 ���Ϻ���߼���Щ����Ļ�����Ŀȫ���� 999999999 ���ɡ�<BR><BR>
                ����޸�������κ�һ���֣���ô���޸ĺ���̳��ʼ������� Cache һ��</b>
                </td>
                </tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>��������ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>����������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle0" value="$mtitle0"></td>
                </tr>

               <tr>
               <td bgcolor=#FFFFFF valign=middle align=left width=40%>
               <font face=���� color=#333333><b>������ͼ��</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text size=40 name="mgraphic0" value="$mgraphic0"></td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�һ����ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�һ���������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark1" value="$mpostmark1"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�һ������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle1" value="$mtitle1"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�һ��ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic1" value="$mgraphic1"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�������ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ������������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark2" value="$mpostmark2"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ���������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle2" value="$mtitle2"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�����ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic2" value="$mgraphic2"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�������ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ������������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark3" value="$mpostmark3"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ���������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle3" value="$mtitle3"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�����ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic3" value="$mgraphic3"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ��ĵ���ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��ĵ��������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark4" value="$mpostmark4"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��ĵ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle4" value="$mtitle4"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��ĵ�ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic4" value="$mgraphic4"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ������ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ������������ (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark5" value="$mpostmark5"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle5" value="$mtitle5"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ����ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic5" value="$mgraphic5"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�������ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ������������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark6" value="$mpostmark6"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ���������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle6" value="$mtitle6"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�����ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic6" value="$mgraphic6"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ��ߵ���ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��ߵ��������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark7" value="$mpostmark7"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��ߵ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle7" value="$mtitle7"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��ߵ�ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic7" value="$mgraphic7"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ��˵���ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��˵��������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark8" value="$mpostmark8"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��˵�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle8" value="$mtitle8"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��˵�ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic8" value="$mgraphic8"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ��ŵ���ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��ŵ��������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark9" value="$mpostmark9"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��ŵ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle9" value="$mtitle9"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ��ŵ�ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic9" value="$mgraphic9"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�ʮ����ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ���������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark10" value="$mpostmark10"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle10" value="$mtitle10"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ��ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic10" value="$mgraphic10"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�ʮһ����ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮһ���������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark11" value="$mpostmark11"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮһ������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle11" value="$mtitle11"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮһ��ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic11" value="$mgraphic11"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�ʮ������ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ������������ (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark12" value="$mpostmark12"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ��������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle12" value="$mtitle12"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ����ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic12" value="$mgraphic12"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�ʮ������ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ������������ (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark13" value="$mpostmark13"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ��������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle13" value="$mtitle13"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ����ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic13" value="$mgraphic13"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�ʮ�ĵ���ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�ĵ��������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark14" value="$mpostmark14"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�ĵ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle14" value="$mtitle14"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�ĵ�ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic14" value="$mgraphic14"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�ʮ�����ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ����������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark15" value="$mpostmark15"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle15" value="$mtitle15"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ���ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic15" value="$mgraphic15"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�ʮ������ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ������������ (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark16" value="$mpostmark16"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ��������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle16" value="$mtitle16"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ����ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic16" value="$mgraphic16"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�ʮ�ߵ���ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�ߵ��������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark17" value="$mpostmark17"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�ߵ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle17" value="$mtitle17"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�ߵ�ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic17" value="$mgraphic17"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�ʮ�˵���ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�˵��������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark18" value="$mpostmark18"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�˵�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle18" value="$mtitle18"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�˵�ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic18" value="$mgraphic18"></td>
                </tr>
                

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ȼ�ʮ�ŵ���ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�ŵ��������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmark19" value="$mpostmark19"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�ŵ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitle19" value="$mtitle19"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ȼ�ʮ�ŵ�ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphic19" value="$mgraphic19"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>��ߵȼ�����ϸ����</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��ߵȼ����������� (�ﵽ������)</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mpostmarkmax" value="$mpostmarkmax"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��ߵȼ�������</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mtitlemax" value="$mtitlemax"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��ߵȼ���ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="mgraphicmax" value="$mgraphicmax"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>����Աר�õ����ƺ�ͼ�� (�������Ҫ����ȫ������)</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�������ĵȼ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="amotitle" value="$amotitle"><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>��������ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="amodgraphic" value="$amodgraphic"><BR><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�����ĵȼ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="motitle" value="$motitle"><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>������ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="modgraphic" value="$modgraphic"><BR><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�����������ĵȼ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="cmotitle" value="$cmotitle"><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>������������ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="cmodgraphic" value="$cmodgraphic"><BR><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ܰ����ĵȼ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="smotitle" value="$smotitle"><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>�ܰ�����ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="smodgraphic" value="$smodgraphic"><BR><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>̳���ĵȼ�����</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="adtitle" value="$adtitle"><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333><b>̳����ͼ��</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="admingraphic" value="$admingraphic"><BR><BR></td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit name=submit value="�� ��"></td></form></tr></table></td></tr></table>
                ~;
                
                }
                else {
                    &adminlogin;
                    }
        
        }
        
print qq~</td></tr></table></body></html>~;
exit;
