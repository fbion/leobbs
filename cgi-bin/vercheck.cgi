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
use Socket;

$LBCGI::POST_MAX=50000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;             
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "vercheck.cgi";

$query = new LBCGI;

$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
$action       = $query -> param('action');

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");
        
if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {
            
    if ($action eq "process") {
	$versionnumbertemp = $versionnumber;
        $versionnumbertemp =~ s/\<(.+?)\>//isg;
	$out=&lbagent("www.leobbs.com","download/reg.cgi","ver=$versionnumbertemp&url=$boardurl");

        ($lastver, $finishfunc, $downtime, $nowdownloadver, $nowfunc,     $downloadtimes, $formtime, $gburl, $bigurl, $engurl, $temp ) = split(/\t/,$out);
        #���°汾  ���¹���  �����ṩʱ��  Ŀǰ�������ذ汾  �Ѿ���ɹ���  ���ش���        ��ʼʱ��   

($gburl1,$gburl1show,$gburl2,$gburl2show,$gburl3,$gburl3show,$gburl4,$gburl4show,$gburl5,$gburl5show) = split(/\|/,$gburl);
$gbdownloadinfo = "";
if ($gburl1 ne "") {
    if ($gburl1show eq "") { $gburl1show = "�������������"; }
    $gbdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=gb1 onClick='return gbconfirm();' title="�������������"><B>$gburl1show</B></a>~;
}
if ($gburl2 ne "") {
    if ($gburl2show eq "") { $gburl1show = "�������������"; }
    $gbdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=gb2 onClick='return gbconfirm();' title="�������������"><B>$gburl2show</B></a>~;
}
if ($gburl3 ne "") {
    if ($gburl3show eq "") { $gburl1show = "�������������"; }
    $gbdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=gb3 onClick='return gbconfirm();' title="�������������"><B>$gburl3show</B></a>~;
}
if ($gburl4 ne "") {
    if ($gburl4show eq "") { $gburl1show = "�������������"; }
    $gbdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=gb4 onClick='return gbconfirm();' title="�������������"><B>$gburl4show</B></a>~;
}
if ($gburl5 ne "") {
    if ($gburl5show eq "") { $gburl1show = "�������������"; }
    $gbdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=gb5 onClick='return gbconfirm();' title="�������������"><B>$gburl5show</B></a>~;
}

($bigurl1,$bigurl1show,$bigurl2,$bigurl2show,$bigurl3,$bigurl3show,$bigurl4,$bigurl4show,$bigurl5,$bigurl5show) = split(/\|/,$bigurl);
$bigdownloadinfo = "";
if ($bigurl1 ne "") {
    if ($bigurl1show eq "") { $bigurl1show = "�������������"; }
    $bigdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=big1 onClick='return bigconfirm();' title="�������������"><B>$bigurl1show</B></a>~;
}
if ($bigurl2 ne "") {
    if ($bigurl2show eq "") { $bigurl1show = "�������������"; }
    $bigdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=big2 onClick='return bigconfirm();' title="�������������"><B>$bigurl2show</B></a>~;
}
if ($bigurl3 ne "") {
    if ($bigurl3show eq "") { $bigurl1show = "�������������"; }
    $bigdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=big3 onClick='return bigconfirm();' title="�������������"><B>$bigurl3show</B></a>~;
}
if ($bigurl4 ne "") {
    if ($bigurl4show eq "") { $bigurl1show = "�������������"; }
    $bigdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=big4 onClick='return bigconfirm();' title="�������������"><B>$bigurl4show</B></a>~;
}
if ($bigurl5 ne "") {
    if ($bigurl5show eq "") { $bigurl1show = "�������������"; }
    $bigdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=big5 onClick='return bigconfirm();' title="�������������"><B>$bigurl5show</B></a>~;
}

($engurl1,$engurl1show,$engurl2,$engurl2show,$engurl3,$engurl3show,$engurl4,$engurl4show,$engurl5,$engurl5show) = split(/\|/,$engurl);
$engdownloadinfo = "";
if ($engurl1 ne "") {
    if ($engurl1show eq "") { $engurl1show = "�������������"; }
    $engdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=eng1 onClick='return engconfirm();' title="�������������"><B>$engurl1show</B></a>~;
}
if ($engurl2 ne "") {
    if ($engurl2show eq "") { $engurl1show = "�������������"; }
    $engdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=eng2 onClick='return engconfirm();' title="�������������"><B>$engurl2show</B></a>~;
}
if ($engurl3 ne "") {
    if ($engurl3show eq "") { $engurl1show = "�������������"; }
    $engdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=eng3 onClick='return engconfirm();' title="�������������"><B>$engurl3show</B></a>~;
}
if ($engurl4 ne "") {
    if ($engurl4show eq "") { $engurl1show = "�������������"; }
    $engdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=eng4 onClick='return engconfirm();' title="�������������"><B>$engurl4show</B></a>~;
}
if ($engurl5 ne "") {
    if ($engurl5show eq "") { $engurl1show = "�������������"; }
    $engdownloadinfo .= qq~��<a href=http://www.leobbs.com/download/getleobbs.cgi?action=down&type=eng5 onClick='return engconfirm();' title="�������������"><B>$engurl5show</B></a>~;
}

#$lastver="<b>L<font color=#F26522>eo</font>B<font color=#00AEEF>BS</font></b> X Build040101";
#$finishfunc="1. 123<BR>2.123";
#$downtime="2004/01/07";
#$nowdownloadver="<b>L<font color=#F26522>eo</font>B<font color=#00AEEF>BS</font></b> X Build040101";
#$nowfunc="1. 2222<BR>2.3123";
#$downloadtimes="500";
#$formtime="2003/01/01";
#$gburl="http://111";
#$big5url="";
#$engurl="";
	
	if ($lastver eq "-1") {
	    print qq~
              <tr><td bgcolor=#2159C9" colspan=2><font face=����  color=#FFFFFF>
              <b>��ӭ���� LeoBBS ��̳��������/�鿴��̳�汾����</b>
              </td></tr>
              <tr><td bgcolor=#EEEEEE valign=middle align=center colspan=2>
              <font color=#333333><b>$finishfunc</b><BR><BR>��ֱ�ӷ��� <a href=http://www.LeoBBS.com target=_blank>http://www.LeoBBS.com</a> �鿴��������� ��
              </td></tr></table></td></tr></table>
            ~;
            exit;
	}

	if (($lastver ne "")&&($formtime ne "")&&($downtime ne "")) {
	    print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=����  color=#FFFFFF>
                <b>��ӭ������̳�������� / �鿴��̳�汾����</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2><br><br>
            ~;
            $versionnumbertemp = $versionnumber;
            $versionnumbertemp =~ s/\<(.+?)\>//isg;
            if ($versionnumbertemp =~/LeoBBS/g) {
                $myver = $versionnumbertemp;
                $myver =~ s/LeoBBS X Build//isg;
                $myver =~ s/(.*)Build//isg;
                $myver =~ s/(.*)v//isg;

                $newver = $nowdownloadver;
            	$newver =~ s/\<(.+?)\>//isg;
                $newver =~ s/LeoBBS X Build//isg;
                $newver =~ s/(.*)Build//isg;
                $newver =~ s/(.*)v//isg;

                my $gengxin="";
                if ($myver >= $newver) {
                    print qq~<font face=���� color=#333333><center><b>������ʹ�õ������°汾����л��ʹ���װ����ᳬ����̳ ��</b><br><br><br>~;
                    $gengxin="����������";
                } else {
		    print qq~<font face=���� color=#333333><center><b>��ǰ $nowdownloadver �Ѿ��ṩ���أ��������Ҫ��������ο���������� ��</b><br><br><br>~;
                    $gengxin="����Ҫ����";
               }
#               if ($big5url eq "") { $big5url = "û��"; } else { $big5url = qq~<a href=$big5url>$big5url</a>~; }
#               if ($engurl  eq "") { $engurl = "û��";  } else { $engurl  = qq~<a href=$engurl>$engurl</a>~;   }

               print qq~
               <table width=75%><tr><td>��ǰ���°汾: $lastver  [ �㵱ǰʹ�ð汾: $versionnumber]<br><hr>
               <img src=$imagesurl/icon/txt.gif width=16 height=16 border=0> <font color=blue>����ɹ���:</font> �������ṩ����ʱ��: <B>$downtime</b> ��<br><br>
               $finishfunc<br>
               <hr>
               </td></tr>
               <tr><td><br><br>��ǰ���ṩ���ص����°汾: <B>$nowdownloadver</b>�� [<font color=red><B>$gengxin</B></font>]<br><hr>
               <img src=$imagesurl/icon/txt.gif width=16 height=16 border=0> <font color=red>���������б�:</font><br><br>
               $nowfunc<br><br><br>
               <hr>
               <img src=$imagesurl/icon/txt.gif width=16 height=16 border=0> <b>���ص�ַ:<br>
               ~;
               if ($gbdownloadinfo ne "") {
                   print qq~<B>[����汾]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>$gbdownloadinfo<br>~;
               } else {
                   print qq~<B>[����汾]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>����ʱ���ṩ<br>~;
               }
               if ($bigdownloadinfo ne "") {
               	   print qq~<B>[����汾]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>$bigdownloadinfo<br>~;
               } else {
               	   print qq~<B>[����汾]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>����ʱ���ṩ<br>~;
               }
               if ($engdownloadinfo ne "") {
               	   print qq~<B>[Ӣ�İ汾]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>$engdownloadinfo<br>~;
               } else {
               	   print qq~<B>[Ӣ�İ汾]</B> <img src=$imagesurl/icon/zip.gif width=16 height=16 border=0>����ʱ���ṩ<br>~;
               }
               print qq~
               <hr><br>
               <b>�� $formtime �������Ѿ��� <b><font color=blue>$downloadtimes</font></b> ����վ��װ�˱���̳��</b>
               <hr>
               </td></tr></table>
               ~;
	    } else {
                print qq~
                <font face=���� color=#333333><center><b>��Ƿ��޸İ汾�ţ��뼰ʱ�Ļ����ӺͰ汾��ʾ��лл������</b><br><br>
                ~;
	    }
            print qq~
            </center>
            </td></tr></table></td></tr></table>
            ~;
	}
	else {
	    print qq~
              <tr><td bgcolor=#2159C9" colspan=2><font face=����  color=#FFFFFF>
              <b>��ӭ���� LeoBBS ��̳��������/�鿴��̳�汾����</b>
              </td></tr>
              <tr><td bgcolor=#EEEEEE valign=middle align=center colspan=2>
              <font color=#333333><b>�޷���ȡ�汾��Ϣ</b><br>Socket ģ�鲻������ʹ�ã������Ƿ������ķ���ǽ���������� LeoBBS �������ڵ�����<BR>����� <a href=http://www.LeoBBS.com target=_blank>http://www.LeoBBS.com</a> �鿴��������� ��
              </td></tr></table></td></tr></table>
            ~;
	}
    }
    else {
	$versionnumbertemp = $versionnumber;
        $versionnumbertemp =~ s/\<(.+?)\>//isg;
        if ($versionnumbertemp =~/LeoBBS/g) {
            print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=����  color=#FFFFFF>
                <b>��ӭ������̳�������� / ��̳�汾���</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333 ><b>��̳�汾���</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                
                <font face=���� color=#990000 ><b><center>LeoBBS ��̳�������� / ��̳�汾���</center></b><br>
                <font face=���� color=#333333 >����Բ鿴��ǰ LeoBBS վ����̳�İ汾�����<br>֪����ǰ���°汾���Ƿ����������õĹ��ܣ��Ƿ��ʺ���������<br><br>
                ������û��Σ���ԣ�������������û�в��ü��ܷ�ʽ���ͣ�<br>������Ϊ���ô�һ�����°汾�������лл������װ�������̳��
                
                </td>
                </tr>
                              
               <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="���汾�������"></form></td></tr></table></td></tr></table>
               ~;
	} else {
            print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=����  color=#FFFFFF>
                <b>��ӭ������̳�������� / ��̳�汾���</b>
                </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333 ><center><b>��Ƿ��޸İ汾�ţ��뼰ʱ�Ļ����ӺͰ汾��ʾ��лл������</b><br><br>
                    </td></tr></table></td></tr></table>
                ~;
       }
    }

} else {
    &adminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;

sub lbagent {
    eval("use Socket;");
    ($host,$path,$content) = @_;
    $host =~ s/^http:\/\///isg;
    $port = 80;
    $path = "/$path" if ($path !~ /^\//);
    my ($name, $aliases, $type, $len, @thataddr, $a, $b, $c, $d, $that);
    my ($name, $aliases, $type, $len, @thataddr) = gethostbyname($host);
    my ($a, $b, $c, $d) = unpack("C4", $thataddr[0]);
    my $that = pack('S n C4 x8', 2, $port, $a, $b, $c, $d);
    return unless (socket(S, 2, 1, 0));
    select(S);
    $| = 1;
    select(STDOUT);
    return unless (connect(S, $that));
    print S "POST http://$host/$path HTTP/1.0\n";
    print S "Content-type: application/x-www-form-urlencoded\n";
    my $contentLength = length $content;
    print S "Content-length: $contentLength\n";
    print S "\n";
    print S "$content";
    @results = <S>;
    close(S);
    undef $|;
    my $result = join("", @results);
    @results = split("\r\n\r\n", $result);
    @results = split("\n\n", $result) if (@results == 1);
    shift(@results);
    $result = join("", @results);
    return $result;
}
