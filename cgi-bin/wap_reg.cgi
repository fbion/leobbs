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
require "data/boardinfo.cgi";
require "wap.pl";
&waptitle;
$show.= qq~\n<card  title="$boardname-ע��">\n ~;
$show.= qq~<p><b>��$boardnameע��</b>\n</p><p>ע���˺ţ�<input type="text" name="n"/>\n</p><p>ע�����룺<input type='password' name="p"/>\n</p><p>�ظ����룺<input type='password' name="p1"/>\n</p><p>�ʼ���ַ��<input type='text' name="email"/>\n</p><p>
<anchor>[ע��]<go href="wap_save_reg.cgi" method="post">\n
<postfield name="n" value="\$(n)"/>\n
<postfield name="p" value="\$(p)"/>\n
<postfield name="p1" value="\$(p1)"/>\n
<postfield name="email" value="\$(email)"/>\n
</go>\n
</anchor>\n <a href="wap_index.cgi">[����]</a> <a href="wap.cgi">[��¼]</a>\n~;
$show.= qq~
</p>~;
&wapfoot;
