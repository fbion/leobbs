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
require "data/boardinfo.cgi";
require "wap.pl";
mkdir ("${lbdir}wap", 0777) if (!(-e "${lbdir}wap"));
chmod(0777,"${lbdir}wap");

$lid = $query -> param('lid');
&check($lid);
if ($inmembername ne ''&&$inmembername ne '����'){
	$ad="<a href=\"wap_index.cgi?lid=$lid\">��̳</a> <br/><a href=\"wap_login.cgi?lid=$lid&amp;check=loginout\">ע��$inmembername</a> <a href=\"wap_set.cgi?lid=$lid\">����</a>";}
else{
	$ad="<a href=\"wap_login.cgi\">��½</a> <a href=\"wap_reg.cgi\">ע��</a> <a href=\"wap_index.cgi\">��̳</a>";
}
&waptitle; 
$show.= qq~<card  title="$boardname">~;
$show.= qq~<p align='center'>$inmembername,��ӭ����$boardname</p><p>[��������]<br/>$ad<br/><a href="wap_new.cgi?lid=$lid">��������</a><br/><a href="wap_sms.cgi?lid=$lid">����Ϣ</a><br/>~;
$show.= qq~</p>~;
&wapfoot;
