#!/usr/bin/perl
#########################
# �ֻ���̳WAP��
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
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
$query = new LBCGI;
$LBCGI::POST_MAX = 2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "wap.lib.pl";
require "wap.pl";
require "data/styles.cgi";
$|++;
&waptitle;
$show.= qq~<card  title="�������Ϣ">~;
$lid = $query -> param('lid');
&check($lid);
$intopictitle        = $query -> param('title');
if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
} else {
    &getmember("$inmembername","no");
}   
$name     = $query -> param('name');
$name = $uref->fromUTF8("gb2312",$name);
&getmember("$name","no");
    &erroroutout("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
$inpost        = $query -> param('inpost');
$inpost=$uref->fromUTF8("gb2312",$inpost);
$intopictitle=$uref->fromUTF8("gb2312",$intopictitle);
$inpost = &cleaninput("$inpost");
$intopictitle = &cleaninput("$intopictitle");

	my $currenttime = time;
		my $filetomake = "$lbdir$msgdir/in/$name\_msg.cgi";
		if (open(FILE, $filetomake))
		{
		@filedata = <FILE>;
		close(FILE);
		}
		open(FILE, ">$filetomake");
		print FILE "$inmembername\tno\t$currenttime\t$intopictitle\t$inpost\n";
		foreach (@filedata)
		{
		chomp;
		print FILE "$_\n";
		}
		close(FILE);
		undef @filedata;
    $show.= qq~<p>�ɹ�����!<br/><a href="wap_index.cgi?lid=$lid">������ҳ</a></p><p><a href="wap_sms.cgi?lid=$lid">���ض���Ϣ</a></p>~;
&wapfoot;