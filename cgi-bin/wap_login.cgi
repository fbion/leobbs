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
$check = $query -> param('check');
$lid = $query -> param('lid');
&waptitle;
$show.= qq~<card  title="$boardname-��½">~;
if($check eq 'loginout'){
	unlink "${lbdir}wap/$lid";
	$show.= qq~<p>�ɹ�ע��$inmembername������ȥ����ǩ��������ֱ�����½</p><p><a href='wap.cgi'>������ҳ</a></p>~;&wapfoot;
}
my $xh2 = $ENV{'REMOTE_ADDR'};
$show.=  qq~<p><b>��¼$boardname</b> <br/>�����ֻ�IP��$xh2<br/>��������ֻ����޷�����ID���е�½�����ס����IP��������̳��loginwap.cgi���������½Url��<br/>\n</p><p>�˺ţ�<input type="text" name="n1" value="$a1"/><br/>\n</p><p>���룺<input type='password' name="p" value="$b1"/><br/>\n</p><p>
<anchor>[��¼]<go href="wap_index.cgi" method="post">
<postfield name="n1" value="\$(n1)"/>
<postfield name="p" value="\$(p)"/>
</go>
</anchor> <a href="wap_index.cgi">[����]</a> <a href="wap_reg.cgi">[ע��]</a>~;
$show.=  qq~
</p>~;
&wapfoot;
