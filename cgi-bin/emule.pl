#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

sub doemule {
  $codecount = 1 if ($codecount <= 0);
  $$post .= "<script src=$imagesurl/images/emu.js></script>" if ($codecount == 1);
	while ($$post =~ /\[emule\](.+?)\[\/emule\]/is) {
      my $view = "<br><table width=94% align=center cellspacing=1 cellpadding=5 bgColor=$tablebordercolor><tr bgColor=$titlecolor><td colspan=2 align=center><font color=$titlefontcolor><B>������ eMule ר�õ��������ӣ������밲װ eMule ���ܵ������</B></font></td></tr>";
	    my $post1 = $1;
	    $post1 =~ s/<p>/<br>/isg;
	    $post1 =~ s/<br><br>/<br>/isg;
	    my @lines = split(/<br>/i, $post1);
	    $post1 = "";
	    my $counters = 0;
	    my $total = 0;
	    my $totalper = 0;
		my $postbackcolor1 = "";
		my $postfontcolor1 = "";
	    foreach (@lines) {
	    	chomp $_;
        	$_ =~ s/[\a\f\e\0\r\t]//isg;
	        $_ =~ s/</\&lt;/g;
        	$_ =~ s/>/\&gt;/g;
	    	next if ($_ eq "");
	    	next if ($_ !~ /^ed2k:\/\//i);
		my @emu = split(/\|/i, $_);
	    	next if ($emu[3] eq "");
        	my $emuchg = &unescape($emu[2]);
		if ($emuchg ne $emu[2]) {
		    if ($loaduftmo ne 1) { use UTF8simple; $loaduftmo = 1; }
	    	    my $uref = new UTF8simple;
	    	    $emu[2]=$uref->fromUTF8("gb2312",$emuchg);
	    	}

		    $counters++;
    		if ($counters % 2 == 1) {
					$postbackcolor1 = $postcolorone;
					$postfontcolor1 = $postfontcolorone;
		    } else {
					$postbackcolor1 = $postcolortwo;
					$postfontcolor1 = $postfontcolortwo;
		    }

				$total+=$emu[3];
				$totalper=$emu[3];
        if($totalper>(1024*1024*1024*1024)){
                $totalper=int($totalper*100/1024/1024/1024/1024+0.5)/100;
                $totalper.="TB";
        } elsif ($totalper>(1024*1024*1024)){
                $totalper=int($totalper*100/1024/1024/1024+0.5)/100;
                $totalper.="GB";
        } elsif ($totalper>(1024*1024)){
                $totalper=int($totalper*100/1024/1024+0.5)/100;
                $totalper.="MB";
        } else {
                $totalper=int($totalper*100/1024+0.5)/100;
                $totalper.="KB";
        }
		$view.="<tr bgColor=$postbackcolor1><td width=88%><font color=$postfontcolor1><input type=\"checkbox\" name=\"emulefile$codecount\" value=\"$_\" onclick=\"em_size('emulefile$codecount');\" checked=\"checked\"><a href=\"$_\">$emu[2]</a></font></td><td align=center><font color=$postfontcolor1 title=$filename>$totalper</font></td></tr>";
	    }

        if($total>(1024*1024*1024*1024)){
                $total=int($total*100/1024/1024/1024/1024+0.5)/100;
                $total.="TB";
        } elsif ($total>(1024*1024*1024)){
                $total=int($total*100/1024/1024/1024+0.5)/100;
                $total.="GB";
        } elsif ($total>(1024*1024)){
                $total=int($total*100/1024/1024+0.5)/100;
                $total.="MB";
        } else {
                $total=int($total*100/1024+0.5)/100;
                $total.="KB";
        }
        
        $view.="<tr bgColor=$titlecolor><td align=left><input type=\"checkbox\" id=\"checkall_emulefile$codecount\" onclick=\"checkAll('emulefile$codecount',this.checked)\" checked=\"checked\"/> ȫѡ ���� <input type=\"button\" value=\"����ѡ�е��ļ�\" onclick=\"download('emulefile$codecount',0,1)\"> ��<input type=\"button\" value=\"����ѡ�е�����\" onclick=\"copy('emulefile$codecount')\"><div id=\"ed2kcopy_emulefile$codecount\" style=\"position:absolute;height:0px;width:0px;overflow:hidden;\"></div></td><td align=center id=\"size_emulefile$codecount\">$total</td></tr></table>";

	    $$post =~ s/\[emule\](.+?)\[\/emule\]/$view/is;
	    $codecount ++;
	}
}
1;
