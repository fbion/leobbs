#########################
# �ֻ���̳WAP��
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
sub lbcode {
    my $post = shift;
    study($$post);
    	$$post =~s/\[UploadFile=(.*?)\]/(�ϴ��ļ�)<br>/ig;
    if ($wwjf ne "no") {
	if ($$post=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg) {
    	    if ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($myinmembmod eq "yes")|| ($myrating >= $1) ){
	    } else {
		$$post=qq~����û��Ȩ�޿�������ӣ���������������Ҫ <b>$1<\/b><br> ~;
		$addme="(��������!)<br><br>" if ($addme);
	    }
	    $$post=~s/LBHIDDEN\[(.*?)\]LBHIDDEN/������ֻ���������ڵ��� <b>$1<\/b> �Ĳ��ܲ鿴��<br>/sg;   
	}
    }
    else { $$post=~s/LBHIDDEN\[(.*?)\]LBHIDDEN//; }
        $$post =~s/\[Maiweb_leobbs(.+?)\]/(maiweb)����������Ч/g;
$$post =~ s/(\[cimg=)(\S+?)(\,)(\S+?)(\])\s*(\S+?)\s*(\[\/cimg\])/(maiweb)ͿѻͼƬ/isg;   
   
    if ($cansale ne "no") { 
if ($$post=~/LBSALE\[(.*?)\]LBSALE/sg) {
require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");

       my $postno = $rn-1;
           my $isbuyer = "";
           my $allbuyer = "";
           my $allbuyerno = "";
           undef @allbuyer;
           if (open(FILE, "${lbdir}$saledir/$inforum\_$intopic\_$postno.cgi")) {
               my $allbuyer = <FILE>;
               close(FILE);
               chomp $allbuyer;
$allbuyer =~ s/\t\t/\t/isg;
               $allbuyer =~ s/\t$//gi;
               $allbuyer =~ s/^\t//gi;
@allbuyer = split(/\t/, $allbuyer);
$allbuyerno = @allbuyer;
               $allbuyerno2=$allbuyerno-1;
              
       $allbuyer = "\t$allbuyer\t";
$isbuyer="yes" if ($allbuyer =~ /\t$inmembername\t/i);
           }
           $allbuyerno = 0 if (($allbuyerno < 0)||($allbuyerno eq ""));
           unless (($inmembername eq $membername )||($mymembercode eq "ad")||($mymembercode eq 'smo')||($myinmembmod eq "yes")||($isbuyer eq "yes")) {
         $$post=qq~(�쿴���������Ҫ <b>$1<\/b> $moneyname��Ŀǰ���� <b>$allbuyerno<\/b> �˹���<a href=\"buypost.cgi?inforum=$inforum&amp;intopic=$intopic&amp;postmast=$most&amp;postnumber=$postno&amp;salemembername=$membername&amp;moneynumber=$1\">\[����\]<\/a>)~;
               $addme="(��������!)<br><br>" if ($addme);
   } else {
       $$post=~s/LBSALE\[(.*?)\]LBSALE/�������ۼ� <b>$1<\/b> $moneyname��Ŀǰ���� <b>$allbuyerno<\/b> �˹���)<br><br>/sg;   
   }
}
   }
   else { $$post=~s/LBSALE\[(.*?)\]LBSALE//; }

    if ($$post =~/\[DISABLELBCODE\]/) {
	$$post =~ s/\[DISABLELBCODE\]//isg;
	return;
    }

    if (($arrawpostpic eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	$$post =~ s/\[url.+?\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]\[\/url\]/<img src=\'$1:\/\/$2\' alt=\'ͼƬ\' width=\'110\' \/>/isg;
	$$post =~ s/\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]/<img src=\'$1:\/\/$2\' alt=\'ͼƬ\' width=\'110\' \/>/isg;
	$$post =~ s/\[img\,(.+?)\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]/<img src=\'$2:\/\/$3\' align=\'$1\' alt=\'ͼƬ\' width=\'110\' \/>/isg;
	$$post =~ s/(^|\s|\>|\\|\;)(http|https|ftp):\/\/(\S+?\.)(png|bmp|gif|jpg|jpeg)(\s|$|\<|\[)/$1<img src=\'$2:\/\/$3$4\' width=\'110\' alt=\'ͼƬ\' \/>$5/isg;
    }
    
    $$post =~ s/(^|\s|\>|\\|\;)www\.(\S+?)(\s|$|\<|\[)/$1www.$2$3/isg;
    $$post =~ s/(^|\s|\>|\\|\;)(\w+\@\w+\.\w+)(\s|$|\<|\[)/$1$2$3/isg;
    $$post =~ s/\<p>/<br><br>/isg;
    $$post =~ s/\[br\]/<br>/isg;
    $$post =~ s/(<br>){10,}/<br><br><br>/ig;

    if (($$post =~/\[curl=(http|https|ftp):\/\/(.*?)\]/i)&&($usecurl ne "no")) {
        $$post =~ s/\[curl=(http|https|ftp):\/\/(.*?)\]/\(��������\)/ig;
    }
    unless ($$post =~ /\[\/.{1,12}]/) {
        $$post =~ s/\{br\}/<br>/sg;
	return;
    }

    $$post =~ s/\[url\](\[\S+\])(\S+?)(\[\S+\])\[\/url\]/$1$2$3/isg;
    $$post =~ s/\[url=\s*(.*?)\s*\]\s*(.*?)\s*\[\/url\]/$2/isg;
    $$post =~ s/\[url\]\s*(.*?)\s*\[\/url\]/$1/isg;
    $$post =~ s/(\[email\])(\S+?\@\S+?)(\[\/email\])/Email:$2)/isg;
    $$post =~ s/\[email=(\S+?\@\S+?)\]\s*(.*?)\s*\[\/email\]/Email:$2/isg;
## ָ�����Ӹ������Ա��
if ($$post =~m/\[qqh=(.+?)\](.+?)\[\/qqh\]/isg){ 
$cenviewer="$1";
if((lc($cenviewer) eq lc($inmembername))||(lc($membername) eq lc($inmembername))){ 
$$post =~s/\[qqh=(.+?)\](.+?)\[\/qqh\]/\(����$membername��������Ļ�����ע�Ᵽ��:$2\)<br>/isg; 
}else{ 
$$post =~s/\[qqh=(.+?)\](.+?)\[\/qqh\]/\(�㲻�ܲ鿴�����µ����ݣ�����ֻ��$1�鿴����Ǹ\)/isg; 
 }
}
## By maiweb end
    if ($jfmark eq "yes") {
	if ($$post =~m/\[jf=(\d+?)\](.+?)\[\/jf\]/isg){ 
	    $jfpost=$1;
	    if (($jfpost <= $jifen)||($mymembercode eq "ad")||($mymembercode eq "smo")||($myinmembmod eq "yes")||(lc($membername) eq lc($inmembername))){ 
	   	$$post =~s/\[jf=(\d+?)\](.*)\[\/jf\]/�������ݣ������ֱ���ﵽ $jfpost ���ܲ鿴�����ݣ�$2/isg; 
	    } else { 
	     #   &error("������&���ֱ���ﵽ $jfpost ���ܲ鿴����Ŀǰ�Ļ����� $jifen ��") if (($editpostnumber eq "1")&&($noviewjf eq "yes"));
   		$$post =~s/(\[jf=(\d+?)\])(.*)(\[\/jf\])/�������ݣ� �������ѱ����� , ���ֱ���ﵽ $jfpost ���ܲ鿴/isg; 
                $addme="��������!<br><br>" if (($addme)&&($1 =~ m/^\[jf/));
   	    }
   	}
    }
    if ($hidejf eq "yes" ) {
      if ($$post =~m/(\[hide\])(.*)(\[\/hide\])/isg){ 
        if ($viewhide ne "1") { 
            $$post =~ s/(\[hide\])(.*)(\[\/hide\])/\(�����������Ѿ����أ�����ظ��󣬲��ܲ鿴\)<br>/isg;
            $addme="(��������!)<br><br>" if (($addme)&&($1 eq "[hide]"));
	} else { 
            $$post =~ s/\[hide\](.*)\[hide\](.*)\[\/quote](.*)\[\/hide\]/\(���أ�$1<br>$2<br>$3\)/isg; 
     	    $$post =~ s/\[hide\]\s*(.*?)\s*\[\/hide\]/\(���أ�$1\)/isg; 
  	}
      }
    }
    # ֧����
if($$post=~m/\[payto\](.*?)\[\/payto\]/){
	$$post=~s/\[payto\](.*?)\[\/payto\]/<b>\(����֧�������ס�\)<\/b>/g;
	}
	# ������
    if ($postjf eq "yes") {
	if ($$post =~m/\[post=(.+?)\](.+?)\[\/post\]/isg){ 
	    $viewusepost=$1; 
	    if ($StartCheck >= $viewusepost) { $Checkpost='ok'; } else { $Checkpost='not'; }
	    if (($Checkpost eq 'ok')||($mymembercode eq "ad")||($mymembercode eq "smo")||($myinmembmod eq "yes")||(lc($membername) eq lc($inmembername))){ 
	   	$$post =~s/\[post=(.+?)\](.*)\[\/post\]/$2/isg; 
	    } else { 
   		$$post =~s/(\[post=(.+?)\])(.*)(\[\/post\])/\(�������ѱ����� , ������������ <b>$viewusepost<\/b> ���ܲ鿴\)/isg; 
                $addme="(��������!)<br><br>" if (($addme)&&($1 =~ m/^\[post/));
   	    }
   	}
    }
	$$post =~ s/\[hr\]/<br>/isg;
	$$post =~ s/\[b\](.+?)\[\/b\]/<b>$1<\/b>/isg;
	$$post =~ s/\[i\](.+?)\[\/i\]/<i>$1<\/i>/isg;
	$$post =~ s/\[u\](.+?)\[\/u\]/<u>$1<\/u>/isg;
	$$post =~ s/\[font=\s*(.*?)\s*\]\s*(.*?)\s*\[\/font\]/$2/isg;
	$$post =~ s/\[color=(\S+?)\]\s*(.*?)\s*\[\/color\]/$2/isg;
	$$post =~ s/(\[list\])(.+?)(\[\/list\])/$2/isg;
	$$post =~ s/(\[list=s\])(.+?)(\[\/list\])/$2/isg;
	$$post =~ s/(\[list=)(A|1|I)(\])(.+?)(\[\/list\])/$4/isg;
	$$post =~ s/(\[list=)(\S+?)(])(.+?)(\[\/list\])/$4/isg;
	$$post =~ s/\[\*\]//isg;
	$$post =~ s/(\[fly\])(.+?)(\[\/fly\])/$2/isg;
	$$post =~ s/(\[s\])(.+?)(\[\/s\])/$2/isg;
	$$post =~ s/(\[sup\])(.+?)(\[\/sup\])/$2/isg;
	$$post =~ s/(\[sub\])(.+?)(\[\/sub\])/$2/isg;
	$$post =~ s/(\[align=)(left|center|right)(\])(.+?)(\[\/align\])/$4/isg;
	$$post =~ s/(\[SHADOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/SHADOW\])/$8/isg;
	$$post =~ s/(\[GLOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/GLOW\])/$8/isg;
	$$post =~ s/(\[BLUR=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/BLUR\])/$8/isg;
	$$post =~ s/(\[FLIPH\])(.+?)(\[\/FLIPH\])/$2/isg;
	$$post =~ s/(\[FLIPV\])(.+?)(\[\/FLIPV\])/$2/isg;
	$$post =~ s/(\[INVERT\])(.+?)(\[\/INVERT\])/$2/isg;
	$$post =~ s/(\[xray\])(.+?)(\[\/xray\])/$2/isg;
	$$post =~ s/(\[MOVE\])(.+?)(\[\/Move\])/$2/isg;
	$$post =~ s/\[code(=.*?)?\](.+?)\[\/code\]/<br>(���룺$2<br>/isg;
	$$post=~s/\[(.+?)\]//g;
	$$post =~ s/javascript/\&\#106\;avascript/isg;
    $$post =~ s/value/\&\#118\;alue/isg;
    $$post =~ s/FORM/\&\#102\;orm/isg;
    $$post =~ s/about:/about\&\#58\;/isg;
    $$post =~ s/document.cookie/documents\&\#46\;cookie/isg;
    $$post =~ s/apasswordcookie/a\&\#112\;asswordcookies/isg;
    $$post =~ s/adminpass/admin\&\#112\;ass/isg;
    $$post =~ s/file:/file\&\#58\;/isg;
    $$post =~ s/on(mouse|exit|error|click|key)/\&\#111\;n$1/isg;
    $$post =~ s/title/\&\#116\;itle/isg;
    $$post =~ s/membercode/memberc\&\#111\;de/isg;
    $$post =~ s/setmembers.cgi/setmembers\&\#46\;cgi/isg;
#	$$post =~ s/\&/\&amp;/isg;
#	$$post =~ s/\&amp;nbsp;/\&nbsp;/isg;
	$$post =~ s/\$/\&#36;/isg;
#	$$post =~ s/\#/\\\#/isg;
#	$$post =~ s/\&amp;\\\#/\&\#/g;
#	$$post =~ s/\<p\>/\<br\/\>\<br\/\>/isg;
#   $$post =~ s/\<br\>/\<br\/\>/isg;
    return;
}
sub waplbhz {
   my ($str,$start,$len) = @_;
   $strlen=$start+$len; 
   my $tmpstr;
   for(my $i=0;$i<$strlen;$i++) {
       if(ord(substr($str,$i,1))>0xa0) {
           if ($i>=$start && $i<($start+$len)){
               $tmpstr .= substr($str,$i,2);
           }
           $i++;
       }
       else {
           if ($i>=$start && $i<($start+$len)){
               $tmpstr .= substr($str,$i,1);
           }
       }
   }
   return $tmpstr;
}
sub waplbhz1 { # by bbser
        my ($str, $strbegin, $strlength) =@_;
        my $strtmp = "";
        my $strtmp1 = "";
        my $ended = 0;  # ȡ�õ��ַ����Ƿ���ԭʼ�ַ��������һ��

        return -1 if (length($str) < $strbegin); # �����д�����ʼ�ַ����������ַ�����Ҫ��
	if (length($str) <= $strbegin + $strlength) { #�����г��ȹ����Զ�����һ��
		$strlength = length($str) - $strbegin ;
		$ended = 1;
	}

        $strtmp = substr($str, $strbegin, $strlength);

	if ($strbegin > 0) { # �����ͷ��һ�Σ�����Ҫ�жϵ�һ���ַ��ǲ�������

	    $strtmp1 = substr($str, 0, $strbegin);

            if ($strtmp1 =~ /^([\000-\177]|[\200-\377][\200-\377])*([\000-\177]|[\200-\377][\200-\377])$/) { #ǰ��һ���ַ����������ĺ���
            	$strtmp = $strtmp;
            } else {
		$strtmp =  substr($str, $strbegin -1 , 1) . $strtmp;
		chop ($strtmp);
            }

        }

	if ($ended == 0) {  # �������һ�Σ�����Ҫ�ж����һ���ַ��ǲ�������
            if ($strtmp =~ /^([\000-\177]|[\200-\377][\200-\377])*([\000-\177]|[\200-\377][\200-\377])$/) {
            	$strtmp = $strtmp;
            } else {
                chop ($strtmp);
            }
		
	}

        return $strtmp;

}

1;