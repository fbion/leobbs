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
use LBCGI;
$query = new LBCGI;
&waptitle;
$show.= qq~<head><meta forua="true" http-equiv="Cache-Control" content="max-age=0"/><meta http-equiv="Cache-Control" content="no-cache"/></head><card  title="$boardname">~;
$lid = $query -> param('lid');
$inforum        = $query -> param('f');
$show.= qq~<p><b>���⣺</b><input type="text" name="title" value="" /></p><p><b>���ݣ�</b><input type="text" name="inpost" value=""/><br/>���б�ǩ��[br]</p><p><anchor>����&gt;&gt;<go href="wap_post.cgi" method="post">
<postfield name="inpost" value="\$(inpost)"/>
<postfield name="lid" value="$lid"/>
<postfield name="f" value="$inforum"/>
<postfield name="title" value="\$(title)"/>
</go>
</anchor></p>~;
$show.= qq~<p><br/><br/><a href="wap_forum.cgi?forum=$inforum&amp;lid=$lid&amp;paGe=$pa">�����б�</a></p>~;
&wapfoot;