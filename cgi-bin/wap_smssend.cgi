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
$name        = $query -> param('name');
$title        = $query -> param('ti');
$title = 'Re:'.$title if($title ne '');
&waptitle;
$show.= qq~<head><meta forua="true" http-equiv="Cache-Control" content="max-age=0"/><meta http-equiv="Cache-Control" content="no-cache"/></head><card  title="������Ϣ">~;
$lid = $query -> param('lid');
&check($lid);
if($name ne ''){
	$a="";$c="<postfield name=\"name\" value=\"$name\"/>";
}else{
	$a="<p><b>�ռ��ˣ�</b><input type=\"text\" name=\"name\" value=\"\" /></p>";$c="<postfield name=\"name\" value=\"\$(name)\"/>";
}
if($title ne ''){
	$b="";$d="<postfield name=\"title\" value=\"$title\"/>";
}else{
	$b="<p><b>���⣺</b><input type=\"text\" name=\"title\" value=\"\" /></p>";$d="<postfield name=\"title\" value=\"\$(title)\"/>";
}
$show.= qq~$a$b<p><b>���ݣ�</b><input type="text" name="inpost" value=" "/></p><p><anchor>����&gt;&gt;<go href="wap_smssave.cgi" method="post">
<postfield name="inpost" value="\$(inpost)"/>
<postfield name="lid" value="$lid"/>
$c
$d
</go>
</anchor></p>~;
$show.= qq~<p><br/><br/><a href="wap_index.cgi?lid=$lid">������ҳ</a></p>~;
&wapfoot;