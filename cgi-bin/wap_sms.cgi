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
require "wap.lib.pl";
require "wap_code.cgi";
$lid = $query -> param('lid');
&check($lid);
if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
} else {
    &getmember("$inmembername","no");
}  

&waptitle;
$show.= qq~<card  title="�ռ���"><p>$boardname�ռ���<br/>~;
open(file,"${lbdir}${msgdir}/in/${inmembername}_msg.cgi");
my @file=<file>;
close(file);
$paGe = $query->param('paGe');
	my $allfile=@file;$pre=5;
	my $yema = $allfile/$pre;
    my $yema=($yema>int($yema))?int($yema)+1:$yema;
			$paGe=($paGe eq '' || $paGe <=0)?"1":"$paGe";
            my $k=($paGe-1)*$pre;
            if($k>$allfile){$k=0;}
            my $s=$k+$pre-1;
			for($ij=$paGe-2;$ij<=$paGe+2;$ij++){ 
			next if ($ij<1);
			next if ($ij>$allfile/$pre+1);
			if($ij ne $paGe){$newpage.="<a href=\"wap_sms.cgi?paGe=$ij&amp;lid=$lid\">$ij</a>&nbsp;";}else{$newpage.="<i>$ij</i>&nbsp;";}
			}
			$newpage or $newpage='&nbsp;<i>1</i>';
			my $j=0;$h=$k;
foreach(@file[$k..$s]){
	chomp;next if($_ eq '');$h++;
	my($who,$zt,$sj,$ti,$post)=split(/\t/,$_);
	 $sj = &dateformat($sj + ($timedifferencevalue*3600) + ($timezone*3600));
	$who=~s/����������//;
	$who1=uri_escape($who);
	$ti1=uri_escape($ti);

&lbcode(\$post);
my $postsize = length($post);
if($postsize>$mastnum){
	$post=~s/<br>/\n/g;
	$post=~s/<p>/\\n\\n/g;
	$post=~s/<(.*?)>//g;
	$post = substr($post,0,$mastnum);
	if ($post =~ /^([\000-\177]|[\241-\371][\75-\376])*([\000-\177]|[\241-\377][\75-\376])$/){}
else{chop($post);}
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
	chomp $post;
	$post .="<a href=\"wap_sms_all.cgi?lid=$lid&amp;pno=$k&amp;pa=$paGe\">&gt;&gt;</a>"; 
}else{
	$post=~s/<br>/<br\/>/g;
	$post=~s/<p>/<br\/><br\/>/g;
	$post =~ s/\&amp;nbsp;/\&nbsp;/g;
}

	 if ($zt eq 'no'){$zt = '(��)';}else{$zt='';}
	$show.= "$h,$ti$zt<br/>����:$who<br/>ʱ��:$sj<br/>$post<br/><a href=\"wap_smssend.cgi?lid=$lid&amp;name=$who1&amp;ti=$ti1\">�ظ�</a><br/>----------<br/>";
}
$show.= "[$paGe/$yemaҳ]</p><p>$newpage</p>";
$show.= qq~<p>����<input type="text" name="tz" size="5" maxlength="5" format="*N"/><a href="wap_sms.cgi?paGe=\$(tz)&amp;lid=$lid">Go..</a></p>~;
$show.= "<p><a href=\"wap_index.cgi?lid=$lid\">$boardname�б�</a>&nbsp;<a href=\"wap_smssend.cgi?lid=$lid\">������Ϣ</a></p>";
open(file,"${lbdir}${msgdir}/in/${inmembername}_msg.cgi");
my @file=<file>;
close(file);
open(FILE,">${lbdir}${msgdir}/in/${inmembername}_msg.cgi");
foreach(@file){ $m++;
	chomp;next if($_ eq '');
	my ($from, $readstate, $date, $messagetitle, $post, $attach) = split(/\t/, $_);
	if($m>=$k && $m<=$s-2){
	print FILE "$from\tyes\t$date\t$messagetitle\t$post\t$attach\n";}else{
	print FILE "$_\n";
	}
}
close(FILE);
&wapfoot;
