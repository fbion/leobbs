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
$lid = $query -> param('lid');
&check($lid);
&getmember("$inmembername")if($inmembername ne ''||$inmembername ne '����');        
$id = $query->param('forum');
$inforum = $id;
&getoneforum($inforum);
$show.= qq~<card  title="$forumname"> ~;
$mymembercode = $membercode;
	$myinmembmod = $inmembmod;
	$myrating = $rating;
	$tempaccess = "forumsallowed" . $inforum;
	$testentry = $query->cookie($tempaccess);
	$allowed = $allowedentry{$inforum} eq "yes" || ($testentry eq $forumpass && $testentry ne "") || $mymembercode eq "ad" || $mymembercode eq "smo" || $myinmembmod eq "yes" ? "yes" : "no";
&errorout("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if ($inforum !~ /^[0-9]+$/ && $inforum ne 'leobbs.cgi');
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }
&errorout("������̳&�����̳��û��Ȩ�޽�����̳��")if($yxz ne '' && $yxz!~/,$membercode,/);
$addtimes = ($timedifferencevalue + $timezone) * 3600;
&errorout("�����Ա��̳�鿴��������&���ǿ���û��Ȩ�޽���!") if ($inmembername eq "����" && $regaccess eq "on" && &checksearchbot);
&errorout("����˽����̳&�Բ�����û��Ȩ�޽����˽����̳��") if ($privateforum eq "yes" && $allowed ne "yes");
if (($startnewthreads eq "cert")&&(($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $membercode !~ /^rz/)||($inmembername eq "����"))&&($userincert eq "no")) { &errorout("������̳&��һ���Ա������������̳��"); }
$paGe = $query->param('paGe');

if ($allowusers ne ''){
    &errorout('������̳&�㲻����������̳��') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}

if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &errorout("������̳&�㲻����������̳���������Ϊ $rating��������ֻ̳���������ڵ��� $enterminweiwang �Ĳ��ܽ��룡") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
        if ($enterminmony > 0 || $enterminjf > 0 ) {
require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
$mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
&errorout("������̳&�㲻����������̳����Ľ�ǮΪ $mymoney1��������ֻ̳�н�Ǯ���ڵ��� $enterminmony �Ĳ��ܽ��룡") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
&errorout("������̳&�㲻����������̳����Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $enterminjf �Ĳ��ܽ��룡") if ($enterminjf > 0 && $jifen < $enterminjf);
   }
}
my $r = &msg($inmembername,$password2);		
$show.= "<p>$r<a href=\"wap_po.cgi?lid=$lid&amp;f=$inforum\">����</a> <a href=\"wap_index.cgi?lid=$lid\">����</a></p>";
open(file,"${lbdir}boarddata/listno$id.cgi");
		my	@allfav=<file>;
			close(file);
			my $allfile=@allfav;
			my $yema = $allfile/$pre;
    my $yema=($yema>int($yema))?int($yema)+1:$yema;
			$paGe=($paGe eq '' || $paGe <=0)?"1":"$paGe";
            my $k=($paGe-1)*$pre;
            if($k>$allfile){$k=0;}
            my $s=$k+$pre-1;
			for($ij=$paGe-2;$ij<=$paGe+3;$ij++){ 
			next if ($ij<1);
			next if ($ij>$allfile/$pre+1);
			if($ij ne $paGe){$newpage.="<a href=\"wap_forum.cgi?forum=$id&amp;paGe=$ij&amp;lid=$lid\">$ij</a>&nbsp;";}else{$newpage.="<i>$ij</i>&nbsp;";}
			}
			
			$newpage or $newpage='&nbsp;<i>1</i>';
			
	foreach(@allfav[$k..$s]){$k++;
		chomp;
		next if $_ eq '';			
		open(file2,"${lbdir}forum$id/$_.pl");
			my $c=<file2>;
			close(file2);
		  my ($top, $title,$no, $threadstate, $threadposts, $threadviews, $startedby) = split (/\t/,$c);
		  $title=~s/����������//isg;
$show.= qq~<p><a href="wap_topic.cgi?f=$id&amp;t=$top&amp;lid=$lid&amp;pa=$paGe">$k,$title</a>($threadposts/$threadviews, $startedby)</p>\n~;
			}	
			
$show.= qq~<p>[$paGe/$yemaҳ]<br/>$newpage</p><p>���� <input type="text" size="4" maxlength="4" name="tz" format="*N"/> <a href="wap_forum.cgi?forum=$id&amp;paGe=\$(tz)&amp;lid=$lid">ҳ</a><br/><a href="wap_index.cgi?lid=$lid">������ҳ</a></p>~;
&wapfoot;