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
require "wap_code.cgi";
require "wap.pl";
$|++;
&waptitle;
$show.= qq~<card  title="$boardname"> ~;
$lid = $query -> param('lid');
&check($lid);
$pa    = $query -> param('pa');
if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
} else {
    &getmember("$inmembername","no");
}  

$postno        = $query -> param('pno');
$ag        = $query -> param('ag');
open(file,"${lbdir}${msgdir}/in/${inmembername}_msg.cgi");
my @file=<file>;
close(file);		
	my($who,$zt,$sj,$ti,$post)=split(/\t/,$file[$postno]);
	
&lbcode(\$post);
if($ag<1){$ag=1;}
	$post=~s/<br>/\\n/g;
	$post=~s/<p>/\\n\\n/g;
	$post=~s/<(.*?)>//g;
	my $sa = $mastnum2*($ag-1); my $sb = $mastnum2*$ag;
	$postsize = length($post);
	$sb=($sb<=$postsize)?$mastnum2:($postsize-$sb-$mastnum2);
	$post = &waplbhz($post,$sa,$mastnum2);
	$yema = ($postsize/$mastnum2 >int($postsize/$mastnum2))?(int($postsize/$mastnum2)+1):int($postsize/$mastnum2);
	$post=~s/\\n/<br\/>/g;
	$post =~ s/\&/\&amp;/isg;
	$post =~ s/\&amp;nbsp;/\&nbsp;/g;
	$post =~ s/\&amp;gt;/\&gt;/g;
	$post =~ s/\&amp;lt;/\&lt;/g;
	$post =~ s/\&amp;#36;/\��/g;
	$post =~ s/\&amp\;(.{1,6})\&\#59\;/\&$1\;/isg;
    $post =~ s/\&\#([0-9]{1,6})\&\#59\;/\&\#$1\;/isg;
	$post =~ s/\&amp;quot;/\"/g;
	$post =~ s/\&amp;#59;/\;/g;
	$post =~ s/\&amp;#35;/\&#35;/g;
	$post =~ s/\&amp;amp;/\&amp;/g;
	$ag1=$ag+1;
	$ag2=$ag-1;chomp $post;
	$post .="<br/>[$ag/$yemaҳ]<br/>";
	$post.="<a href=\"wap_sms_all.cgi?lid=$lid&pno=$postno&amp;pa=$pa&amp;ag=$ag1\">[��һҳ]</a>&nbsp;"if($ag1<=$yema);
	$post.="<a href=\"wap_sms_all.cgi?lid=$lid&amp;pno=$postno&amp;pa=$pa&amp;ag=$ag2\">[��һҳ]</a>&nbsp;"if($ag2>=1);
 $sj = &dateformat($sj + ($timedifferencevalue*3600) + ($timezone*3600));
 	$who=~s/����������//;
	$who1=uri_escape($who);
	$ti1=uri_escape($ti);
 $a .= qq~<p>$post</p>~;
$show.= qq~<p><b>���⣺$ti</b><br/>����:$who<br/>ʱ��:$sj</p>$a<p><a href=\"wap_smssend.cgi?lid=$lid&amp;name=$who1&amp;ti=$ti1\">�ظ�</a><br/><a href="wap_sms.cgi?lid=$lid&amp;paGe=$pa">����Ϣ</a><br/><a href="wap_index.cgi?lid=$lid">��̳��ҳ</a></p>~;
&wapfoot;