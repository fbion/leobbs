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
require "data/boardskin.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setplugin.cgi";

$query = new LBCGI;

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
	$theparam =~ s/\\/\\\\/g;
        $theparam =~ s/\@/\\\@/g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
            $printme .= "\$" . "$_ = \"$theparam\"\;\n";
            }
	}

$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");
        
if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {
            
             
    if ($action eq "process") {


        $printme .= "1\;\n";

        $filetomake = "$lbdir" . "data/boardskin.cgi";

        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        close(FILE);
        
         
        
        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=����  color=#FFFFFF>
                <b>��ӭ������̳�������� / ��̳����趨</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=���� color=#333333 ><center><b>���е���Ϣ�Ѿ�����</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                $printme =~ s/1\;//g;
                print $printme;

                print qq~
                </td></tr></table></td></tr></table>
                ~;
                require "${lbdir}data/boardskin.cgi"; require "${lbdir}addplugin.pl";
open (FILE, ">${lbdir}data/skincache.pl");
$pluginadd   =~ s/\\/\\\\/isg;
$loggedinas  =~ s/\\/\\\\/isg;
$pluginadd   =~ s/~/\\\~/isg;
$loggedinas  =~ s/~/\\\~/isg;
$pluginadd   =~ s/\$/\\\$/isg;
$loggedinas  =~ s/\@/\\\@/isg;
$pluginadd   =~ s/\$/\\\$/isg;
$loggedinas  =~ s/\@/\\\@/isg;
print FILE qq(\$pluginadd = qq~$pluginadd~;\n);
print FILE qq(\$loggedinas .= qq~$loggedinas~;\n);
print FILE "1;\n";
close (FILE);

                }

                else {
                    print qq~
                    <tr><td bgcolor=#2159C9" colspan=2><font face=����  color=#FFFFFF>
                    <b>��ӭ���� LeoBBS ��̳��������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font color=#333333><b>���е���Ϣû�б���</b><br>���ļ���Ŀ¼Ϊ����д������������ 777 ��
                    </td></tr></table></td></tr></table>
                    ~;
                    }
        
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                               print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=����  color=#FFFFFF>
                <b>��ӭ������̳�������� / ��̳����趨</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333 ><b>��̳����趨</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
            
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000 ><b><center>LeoBBS ��̳����趨</center></b><br>
                <font face=���� color=#333333 >��������Ӻ�ɾ����̳��һЩ���Ӳ����������̳�����������̳�����ԣ�
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 1 </a></b><br>��̳��� 1 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin1name" value="$plugin1name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 1 URL</b><br>��̳���1������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin1url" value="$plugin1url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 2 </a></b><br>��̳��� 2 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin2name" value="$plugin2name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 2 URL</b><br>��̳���2������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin2url" value="$plugin2url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 3 </a></b><br>��̳��� 3 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin3name" value="$plugin3name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 3 URL</b><br>��̳���3������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin3url" value="$plugin3url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 4 </a></b><br>��̳��� 4 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin4name" value="$plugin4name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 4 URL</b><br>��̳���4������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin4url" value="$plugin4url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 5 </a></b><br>��̳��� 5 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin5name" value="$plugin5name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 5 URL</b><br>��̳���5������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin5url" value="$plugin5url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 6 </a></b><br>��̳��� 6 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin6name" value="$plugin6name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 6 URL</b><br>��̳���6������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin6url" value="$plugin6url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 7 </a></b><br>��̳��� 7 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin7name" value="$plugin7name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 7 URL</b><br>��̳���7������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin7url" value="$plugin7url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 8 </a></b><br>��̳��� 8 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin8name" value="$plugin8name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 8 URL</b><br>��̳���8������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin8url" value="$plugin8url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 9 </a></b><br>��̳��� 9 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin9name" value="$plugin9name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 9 URL</b><br>��̳���9������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin9url" value="$plugin9url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 10 </a></b><br>��̳��� 10 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin10name" value="$plugin10name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 10 URL</b><br>��̳���10������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin10url" value="$plugin10url"></td>
                </tr>      

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 11 </a></b><br>��̳��� 11 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin11name" value="$plugin11name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 11 URL</b><br>��̳���11������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin11url" value="$plugin11url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 12 </a></b><br>��̳��� 12 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin12name" value="$plugin12name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 12 URL</b><br>��̳���12������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin12url" value="$plugin12url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 13 </a></b><br>��̳��� 13 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin13name" value="$plugin13name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 13 URL</b><br>��̳���13������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin13url" value="$plugin13url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 14 </a></b><br>��̳��� 14 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin14name" value="$plugin14name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 14 URL</b><br>��̳���14������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin14url" value="$plugin14url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 15 </a></b><br>��̳��� 15 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin15name" value="$plugin15name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 15 URL</b><br>��̳���15������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin15url" value="$plugin15url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 16 </a></b><br>��̳��� 16 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin16name" value="$plugin16name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 16 URL</b><br>��̳���16������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin16url" value="$plugin16url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 17 </a></b><br>��̳��� 17 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin17name" value="$plugin17name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 17 URL</b><br>��̳���17������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin17url" value="$plugin17url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 18 </a></b><br>��̳��� 18 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin18name" value="$plugin18name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 18 URL</b><br>��̳���18������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin18url" value="$plugin18url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 19 </a></b><br>��̳��� 19 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin19name" value="$plugin19name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 19 URL</b><br>��̳���19������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin19url" value="$plugin19url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 20 </a></b><br>��̳��� 20 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin20name" value="$plugin20name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 20 URL</b><br>��̳���10������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin20url" value="$plugin20url"></td>
                </tr>      

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 21 </a></b><br>��̳��� 21 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin21name" value="$plugin21name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 21 URL</b><br>��̳���21������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin21url" value="$plugin21url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 22 </a></b><br>��̳��� 22 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin22name" value="$plugin22name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 22 URL</b><br>��̳���22������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin22url" value="$plugin22url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 23 </a></b><br>��̳��� 23 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin23name" value="$plugin23name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 23 URL</b><br>��̳���23������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin23url" value="$plugin23url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 24 </a></b><br>��̳��� 24 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin24name" value="$plugin24name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 24 URL</b><br>��̳���24������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin24url" value="$plugin24url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 25 </a></b><br>��̳��� 25 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin25name" value="$plugin25name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 25 URL</b><br>��̳���25������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin25url" value="$plugin25url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 26 </a></b><br>��̳��� 26 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin26name" value="$plugin26name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 26 URL</b><br>��̳���26������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin26url" value="$plugin26url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 27 </a></b><br>��̳��� 27 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin27name" value="$plugin27name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 27 URL</b><br>��̳���27������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin27url" value="$plugin27url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 28 </a></b><br>��̳��� 28 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin28name" value="$plugin28name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 28 URL</b><br>��̳���28������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin28url" value="$plugin28url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 29 </a></b><br>��̳��� 29 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin29name" value="$plugin29name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 29 URL</b><br>��̳���29������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin29url" value="$plugin29url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 30 </a></b><br>��̳��� 30 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin30name" value="$plugin30name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 30 URL</b><br>��̳���30������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin30url" value="$plugin30url"></td>
                </tr>      

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 31 </a></b><br>��̳��� 31 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin31name" value="$plugin31name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 31 URL</b><br>��̳���31������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin31url" value="$plugin31url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 32 </a></b><br>��̳��� 32 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin32name" value="$plugin32name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 32 URL</b><br>��̳���32������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin32url" value="$plugin32url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 33 </a></b><br>��̳��� 33 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin33name" value="$plugin33name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 33 URL</b><br>��̳���33������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin33url" value="$plugin33url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 34 </a></b><br>��̳��� 34 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin34name" value="$plugin34name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 34 URL</b><br>��̳���34������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin34url" value="$plugin34url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 35 </a></b><br>��̳��� 35 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin35name" value="$plugin35name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 35 URL</b><br>��̳���35������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin35url" value="$plugin35url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 36 </a></b><br>��̳��� 36 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin36name" value="$plugin36name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 36 URL</b><br>��̳���36������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin36url" value="$plugin36url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 37 </a></b><br>��̳��� 37 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin37name" value="$plugin37name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 37 URL</b><br>��̳���37������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin37url" value="$plugin37url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 38 </a></b><br>��̳��� 38 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin38name" value="$plugin38name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 38 URL</b><br>��̳���38������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin38url" value="$plugin38url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 39 </a></b><br>��̳��� 39 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin39name" value="$plugin39name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 39 URL</b><br>��̳���39������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin39url" value="$plugin39url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 40 </a></b><br>��̳��� 40 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin40name" value="$plugin40name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 40 URL</b><br>��̳���40������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin40url" value="$plugin40url"></td>
                </tr>      

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 41 </a></b><br>��̳��� 41 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin41name" value="$plugin41name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 41 URL</b><br>��̳���41������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin41url" value="$plugin41url"></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 42 </a></b><br>��̳��� 42 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin42name" value="$plugin42name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 42 URL</b><br>��̳���42������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin42url" value="$plugin42url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 43 </a></b><br>��̳��� 43 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin43name" value="$plugin43name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 43 URL</b><br>��̳���43������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin43url" value="$plugin43url"></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 44 </a></b><br>��̳��� 44 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin44name" value="$plugin44name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 44 URL</b><br>��̳���44������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin44url" value="$plugin44url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 45 </a></b><br>��̳��� 45 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin45name" value="$plugin45name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 45 URL</b><br>��̳���45������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin45url" value="$plugin45url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 46 </a></b><br>��̳��� 46 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin46name" value="$plugin46name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 46 URL</b><br>��̳���46������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin46url" value="$plugin46url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 47 </a></b><br>��̳��� 47 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin47name" value="$plugin47name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 47 URL</b><br>��̳���47������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin47url" value="$plugin47url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 48 </a></b><br>��̳��� 48 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin48name" value="$plugin48name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 48 URL</b><br>��̳���48������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin48url" value="$plugin48url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 49 </a></b><br>��̳��� 49 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin49name" value="$plugin49name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 49 URL</b><br>��̳���49������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin49url" value="$plugin49url"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#AD0000 ><b>��̳��� 50 </a></b><br>��̳��� 50 ������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin50name" value="$plugin50name" maxlength=12></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font face=���� color=#333333 ><b>��̳��� 50 URL</b><br>��̳���50������</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <input type=text size=40 name="plugin50url" value="$plugin50url"></td>
                </tr>      

               <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="�ύ"></form></td></tr></table></td></tr></table>
               
               ~;

                            
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;

