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

$thisprog = "exportemail.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$action       = $query -> param("action");
$action       = &cleaninput("$action");
$inexport     = $query -> param('exporter');
$intarname    = $query -> param('tarname');
$intarname    =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
&getmember("$inmembername");
        
if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) { #s1
    if ($action eq "delete") {
    	unlink ("${imagesdir}$intarname.csv");
    	print qq(<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
<b>��ӭ������̳�������� / ������Ա Email</b></td></tr><tr>
<td bgcolor=#FFFFFF valign=middle colspan=2><b><br>
<center>ɾ���û����ϲ����ļ� $imagesdir$intarname.csv �ɹ�!<br><br><a href=exportemail.cgi>�ٴε��������û����͵� Email.</a></center>);
    }
    elsif ($action eq "process") {
	opendir (DIR, "$imagesdir"); 
	my @countvar = readdir(DIR);
	closedir (DIR);
	@countvar = grep(/\.csv$/i,@countvar);
	foreach (@countvar) {
            unlink ("${imagesdir}$_");
        }

        $inexportusers  = $query -> param('exportusers');
        $inexportusers  =~ s/\, /\,/gi;
        $inexportusers  =~ s/ \,/\,/gi;
        $inexportusers  =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
        @senduserlist   = split(/\,/,$inexportusers);
        print qq(<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
<b>��ӭ������̳�������� / ������Ա Email</b></td></tr><tr>
<td bgcolor=#FFFFFF valign=middle colspan=2><b>������������Ҫ�û����͵� Email �б�</b><br>
<table><tr><td bgcolor=#FFFFFF valign=middle align=center colspan=2>
<textarea cols=60 rows=10>
);
	open (MEMFILE, "${lbdir}data/lbmember.cgi");
	@cgi1 = <MEMFILE>;
	close(MEMFILE);
	$counts=0;
	if ($inexportusers ne "") {
    	    foreach $exusers (@senduserlist){
    	    	chomp $exusers;
		foreach (@cgi1) {
		    chomp $_;
		    (my $membername,$no,$no,$no,$email) = split(/\t/,$_);
		    if ($membername eq $exusers) {
		    	push (@cgi,"$membername,$email,$counts,\n");
		    	$counts++;
		    }
		}
	    }
	}
	else {
	    if ($inexport eq "allmanager") {
		foreach (@cgi1) {
		    chomp $_;
		    (my $membername,my $membercode,my $no,$no,my $email) = split(/\t/,$_);
		    if (($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "amo")||($membercode eq "mo")) {
		    	push (@cgi,"$membername,$email,$counts,\n");
		    	$counts++;
		    }
		}
	    }
	    elsif ($inexport eq "all") {
		foreach (@cgi1) {
		    chomp $_;
		    (my $membername,my $membercode,my $no,$no,my $email) = split(/\t/,$_);
	    	    push (@cgi,"$membername,$email,$counts,\n");
		    $counts++;
		}
	    }
	    else {
		foreach (@cgi1) {
		    chomp $_;
		    (my $membername,my $membercode,my $no,$no,my $email) = split(/\t/,$_);
		    if ($membercode eq $inexport) {
		    	push (@cgi,"$membername,$email,$counts,\n");
		    	$counts++;
		    }
		}
	    }
	}
	unshift (@cgi, "����,�����ʼ���ַ,foxaddrID,foxaddrListMembers\n");
        my $time=time;
        $time=crypt($time,"lb");
        $time=~s /\///isg;
        $time=~s /\.//isg;
        $tarname=$time;        
	$filetomake = "${imagesdir}$tarname" . ".csv";
	open(FILE, ">$filetomake");print FILE @cgi;close FILE;
	    
	print qq(@cgi</textarea><BR></td></tr>);
        print qq(<br><br><a href=$imagesurl/$tarname.csv>����˴������ʼ��б� (Foxmail-CSV��ַ����ʽ)</a><br>
<a href=$thisprog?action=delete&tarname=$tarname>����˴�ɾ�� FTP ������������ļ�</a><br><br><center><a href="exportemail.cgi">�ٴε��������û����͵�Email</a></center>);
    }
    else {
       my $memteam1 = qq~<option value="rz1">����$defrz1(��֤�û�)</option>~ if ($defrz1 ne "");
       my $memteam2 = qq~<option value="rz2">����$defrz2(��֤�û�)</option>~ if ($defrz2 ne "");
       my $memteam3 = qq~<option value="rz3">����$defrz3(��֤�û�)</option>~ if ($defrz3 ne "");
       my $memteam4 = qq~<option value="rz4">����$defrz4(��֤�û�)</option>~ if ($defrz4 ne "");
       my $memteam5 = qq~<option value="rz5">����$defrz5(��֤�û�)</option>~ if ($defrz5 ne "");
	print qq(<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>��ӭ������̳�������� / ������Ա Email</b></td></tr><tr>
<td bgcolor=#EEEEEE valign=middle align=center colspan=2><font color=#333333><b>������Ա Email</b></td></tr>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="process">
<tr><td bgcolor=#FFFFFF valign=middle colspan=2><br>
����<b>ͨ���⹦�ܿ��Խ������Ļ�Ա���ϵ��뵽 Foxmail �ĵ�ַ���ڣ��Ա�������ͨ���ʼ������õ����Ա��ϵ��</b><br><br>
<font color=#000000>�������󣺡���<select name="exporter" size="1"><option value="all">�����û�</option><option value="allmanager">���й���Ա</option><option value="ad">����̳��</option><option value="smo">�����ܰ���</option><option value="cmo">����������</option><option value="mo">���а���</option><option value="amo">���и�����</option><option value="rz">������֤��Ա</option>$memteam1$memteam2$memteam3$memteam4$memteam5<option value="me">������ͨ��Ա</option></select><br>
<font color=#000000>����ָ������<input type=text name="exportusers" size=30>�� (�ö��ŷֿ�����Ա ID )
<br></td></tr>
<tr><td bgcolor=#EEEEEE valign=middle align=center colspan=2>
<input type=submit name=submit value=�ύ></td></form></table></tr></td></tr></table>
);
    }
}
else {
    &adminlogin;
}
print qq~</td></tr></table></body></html>~;
exit;
