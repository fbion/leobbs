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
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "massmsg.cgi";

$query = new LBCGI;
$inmsgtitle       = $query -> param('msgtitle');
$inmessage        = $query -> param('message');
$action           = $query -> param('action');
$insendto         = $query -> param('sendto');
$inmessage        = &cleaninput($inmessage);
$inmsgtitle       = &cleaninput($inmsgtitle);

$inmembername = $query->cookie('adminname');
$inpassword   = $query->cookie('adminpass');
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&getmember("$inmembername","no");

&admintitle;

if (($membercode ne "ad") || ($inpassword ne $password) || (lc($inmembername) ne lc($membername))) {
	&adminlogin;
	exit;
}

if ($action ne "send") {
       my $memteam1 = qq~<option value="rz1">����$defrz1(��֤�û�)</option>~ if ($defrz1 ne "");
       my $memteam2 = qq~<option value="rz2">����$defrz2(��֤�û�)</option>~ if ($defrz2 ne "");
       my $memteam3 = qq~<option value="rz3">����$defrz3(��֤�û�)</option>~ if ($defrz3 ne "");
       my $memteam4 = qq~<option value="rz4">����$defrz4(��֤�û�)</option>~ if ($defrz4 ne "");
       my $memteam5 = qq~<option value="rz5">����$defrz5(��֤�û�)</option>~ if ($defrz5 ne "");

    $output .= qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
	<b>��ӭ������̳�������� / ����Ϣ�㲥</b></td></tr><tr><td><BR>
	<B>ע�⣺�뾡����Ҫʹ�ô���ܣ��˹��ܼ�������ϵͳ��Դ�����һ�ʹ�û����С�</b></td></tr><tr><td>
	<FORM METHOD="post" ACTION="$thisprog">
	<INPUT TYPE="HIDDEN" NAME="action" VALUE="send"><BR>
	<TABLE BORDER="0"><TR VALIGN="TOP"><TD>����Ϣ���⣺ </td>
	<TD><INPUT TYPE="TEXT" SIZE="20" NAME="msgtitle"></TD>
	<TR VALIGN="TOP"><TD>���ܷ�ѡ�� </td><TD>
	<select name="sendto" size="1">
      	  <option value="online">���������û� </option>
       	  <option value="all"   >����ע���û� </option>
       	  <option value="amo"   >ȫ�������� </option>
       	  <option value="mo"    >ȫ������ </option>
       	  <option value="cmo"   >���������� </option>
       	  <option value="smo"   >ȫ���ܰ��� </option>
       	  <option value="ad"    >ȫ��̳�� </option>
       	  <option value="allmo" >���й���Ա </option>$memteam1$memteam2$memteam3$memteam4$memteam5
       	  <option value="rz"    >������֤��Ա </option>
       	  <option value="me"    >������ͨ��Ա </option>
       	</select>
       	</td></tr><TR VALIGN="TOP"><TD>����Ϣ���ݣ� </td><TD>
	<TEXTAREA NAME="message" COLS="50" ROWS="8"></textarea><BR><BR><center>
	<INPUT TYPE="SUBMIT" NAME="Submit" VALUE="�� ��">
	</td></tr></table></form>
    ~;
    print $output;
    print qq~</td></tr></table></body></html>~;
    exit;
}
else {
    if ($inmsgtitle eq "") { $blanks = "yes"; }
    if ($inmessage eq "")  { $blanks = "yes"; }
    &error("����Ϣ�㲥&��ѱ����������д������&msg") if ($blanks eq "yes");
    $currenttime = time;
    if ($insendto eq "all") {
	open (MEMFILE, "${lbdir}data/lbmember.cgi");
	@sendmemlist = <MEMFILE>;
	close(MEMFILE);
    }
    elsif (($insendto eq "me")||($insendto eq "rz")||($insendto eq "rz1")||($insendto eq "rz2")||($insendto eq "rz3")||($insendto eq "rz4")||($insendto eq "rz5")||($insendto eq "mo")||($insendto eq "amo")||($insendto eq "smo")||($insendto eq "ad")||($insendto eq "allmo")) {
	open (MEMFILE, "${lbdir}data/lbmember.cgi");
	my @sendmemlist1 = <MEMFILE>;
	close(MEMFILE);
	undef @sendmemlist;
	foreach (@sendmemlist1) {
	    chomp $_;
	    my ($membername,$membercode,$no) = split(/\t/,$_);
	    push (@sendmemlist, $_) if (($membercode eq "me")&&($insendto eq "me"));
	    push (@sendmemlist, $_) if (($membercode eq "rz")&&($insendto eq "rz"));
	    push (@sendmemlist, $_) if (($membercode eq "rz1")&&($insendto eq "rz1"));
	    push (@sendmemlist, $_) if (($membercode eq "rz2")&&($insendto eq "rz2"));
	    push (@sendmemlist, $_) if (($membercode eq "rz3")&&($insendto eq "rz3"));
	    push (@sendmemlist, $_) if (($membercode eq "rz4")&&($insendto eq "rz4"));
	    push (@sendmemlist, $_) if (($membercode eq "rz5")&&($insendto eq "rz5"));
	    push (@sendmemlist, $_) if (($membercode eq "mo")&&($insendto eq "mo"));
	    push (@sendmemlist, $_) if (($membercode eq "cmo")&&($insendto eq "cmo"));
	    push (@sendmemlist, $_) if (($membercode eq "smo")&&($insendto eq "smo"));
	    push (@sendmemlist, $_) if (($membercode eq "amo")&&($insendto eq "amo"));
	    push (@sendmemlist, $_) if (($membercode eq "ad")&&($insendto eq "ad"));
	    push (@sendmemlist, $_) if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "amo")||($membercode eq "mo"))&&($insendto eq "allmo"));
	}
    }
    else {
	$filetoopen = "${lbdir}data/onlinedata.cgi";
	open(FILE,"$filetoopen");
	my @sendmemlist1 = <FILE>;
	close(FILE);
	undef @sendmemlist;
	foreach (@sendmemlist1) {
	    chomp $_;
	    my ($membername,$no) = split(/\t/,$_);
	    push (@sendmemlist, $_) if ($membername !~ /^����/);
	}
    }
    $totlemembers = @sendmemlist;

    $inmessage = "$inmessage<BR><BR>---------------------------<BR>LeoBBS ���װ��Ƽ�������Ʒ<BR>��ҳ:<a href=http://www.LeoBBS.com target=_blank>http://www.LeoBBS.com</a>";
    foreach (@sendmemlist) {
	my ($thisMember,$no) = split(/\t/,$_);
        $thisMember =~ s/ /\_/isg;
	$thisMember =~ tr/A-Z/a-z/;
	my $filetoopen = "$lbdir". "$msgdir/in/$thisMember" . "_msg.cgi";
	$filetoopen = &stripMETA($filetoopen);
	open (FILE, "$filetoopen");
	@inboxmessages = <FILE>;
	close (FILE);
	open (FILE, ">$filetoopen");
	print FILE "����������ϵͳ����Ϣ�㲥\tno\t$currenttime\t$inmsgtitle\t$inmessage\n";
	foreach (@inboxmessages) {
	    chomp $_;
	    print FILE "$_\n";
	}
	close (FILE);
    }
    $output .= qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
	<b>��ӭ������̳�������� / ����Ϣ�㲥</b></td></tr>
	<tr><td bgcolor=#FFFFFF valign=middle colspan=2>
	<font color=#333333><center><b>����Ϣ�㲥������ɣ������� $totlemembers ����Ϣ��</b></center><br><br>
    ~;
    print $output;
    print qq~</td></tr></table></body></html>~;
    exit;
}
1;
