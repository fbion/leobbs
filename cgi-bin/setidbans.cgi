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

$thisprog = "setidbans.cgi";
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
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 

	$wordarray =~ s/[\`\~\!\@\#\$\%\&\=\\\{\}\;\'\:\"\,\.\/\<\>]//isg;
        $wordarray =~ s/\s+/\n/ig;
        $wordarray =~ s/\n\n/\n/ig;
        my @hasbannedid=split(/\n/,$wordarray);
	foreach (@hasbannedid){
	    $nametocheck = $_; 
	    $nametocheck =~ s/ /\_/g; 
	    $nametocheck =~ tr/A-Z/a-z/; 
	    $nametocheck = &stripMETA($nametocheck); 
	    my $namenumber = &getnamenumber($nametocheck);
	    &checkmemfile($nametocheck,$namenumber);
	    $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi"; 
	    if (-e $filetoopen) { 
		open(FILE9,"$filetoopen"); 
		my $filedata = <FILE9>; 
		close(FILE9); 
		($lmembername, $lpassword, $lmembertitle, $lmembercode, $lnumberofposts) = split(/\t/,$filedata); 
		if (($lmembercode eq "ad")||($lmembercode eq "smo")||($lmembercode eq "cmo")||($lmembercode eq "mo")||($lmembercode eq "amo")){
		    print qq(
<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
<b>��ӭ������̳�������� / ID ��ֹ</b>
</td></tr>
<tr>
<td bgcolor=#FFFFFF valign=middle colspan=2>
<font color=#333333><center><b>���е���Ϣ�Ѿ�����</b></center><br><br>
<b>�㲻�ܽ�ֹ ID:$_,��Ϊ���������ǹ���Ա��</b><br><br>
);
		    print qq~</td></tr></table></body></html>~;
		    exit;
		}
	    }
	    unlink ("${lbdir}cache/id/$nametocheck.cgi") if (-e "${lbdir}cache/id/$nametocheck.cgi");

    opendir (DIRS, "${lbdir}cache/id");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/id/$_") if ((-M "${lbdir}cache/id/$_") *86400 > 600);
    }

	}
        $wordarray2display = $wordarray;
        $wordarray2display =~ s/\n/<br>/g;
	$wordarray =~ s/\n/\t/isg;
        $filetomake = "$lbdir" . "data/idbans.cgi";
        open (FILE, ">$filetomake");
        print FILE $wordarray;
        close (FILE);
        
        if (-e $filetomake && -w $filetomake) {
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ID ��ֹ</b>
		</td></tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#333333><center><b>���е���Ϣ�Ѿ�����</b></center><br><br>
		<b>���Ѿ���ֹ������ ID</b><br><br>
		);
                    print qq(<b>$wordarray2display</b><br>);
                print qq(
                <br><br><br><center><a href="setidbans.cgi">�ٴ�����һЩ��ֹ�� ID</a></center>);
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

                $idfiletoopen = "$lbdir" . "data/idbans.cgi";
                open (FILE, "$idfiletoopen");
                @bannedids = <FILE>;
                close (FILE);
                
                print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
		<b>��ӭ������̳�������� / ID ��ֹ</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>ID ��ֹ�б�</b>
		</td></tr>
		<form action="$thisprog" method="post">
		<input type=hidden name="action" value="process">
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#000000>
		<b>��ע��:</b>������ֹ��һ�� ID �Ļ�����ô��� ID �����޷���¼��<br>
		<br>
		<b>˵��:</b><BR>
		             �����Ҫ��ֹһ�� ID������ֱ������ ID ��������磺 Tom<BR>
		             ÿ��дһ�� ID��ע�����س���<BR><BR>
	                </font></td>
		</tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=center colspan=2>
		<textarea cols=60 rows=18  name="wordarray">);
		                foreach (@bannedids) {
		                   $singleid = $_;
		                   chomp $_;
		                   next if ($_ eq "");
						   #$singleid =~ s/\n\s/\n/g;
				   $singleid =~ s/\t/\n/isg;
		                   print qq($singleid);
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
