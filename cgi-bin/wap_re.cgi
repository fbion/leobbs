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
require "data/styles.cgi";
&waptitle;
$show.= qq~<card  title="$boardname">~;
$lid = $query -> param('lid');
$inforum        = $query -> param('f');
$intopic        = $query -> param('t');   
$show.= qq~<p><b>�ظ����ݣ�</b><br/><input type="text" name="inpost" value=""/><br/>���б�ǩ��[br]</p><p><anchor>�ظ�<go href="wap_reply.cgi" method="post">
<postfield name="inpost" value="\$(inpost)"/>
<postfield name="lid" value="$lid"/>
<postfield name="f" value="$inforum"/>
<postfield name="t" value="$intopic"/>
</go>
</anchor></p>~;
$show.= qq~<p><br/><br/><a href="wap_forum.cgi?forum=$inforum&amp;lid=$lid&amp;paGe=$pa">�����б�</a></p><p><a href="wap_topic.cgi?f=$inforum&amp;lid=$lid&amp;t=$intopic">��������</a></p>~;
&wapfoot;