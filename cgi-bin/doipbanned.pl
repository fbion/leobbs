#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

      unlink ("${lbdir}cache/id/$infilemembername.cgi");
      if (($inmembername ne "")&&($inmembername ne "����")) {
	if (open(FILE,"${lbdir}data/idbans.cgi")) {
           $term_idbannedmembers = <FILE>;  
           close(FILE);
           $term_idbannedmembers =~ s/\t/\_/isg;
           $term_idbannedmembers = "\_$term_idbannedmembers\_";
           $term_idbannedmembers =~ s/\_\_/\_/isg;
	   $term_idbannedmembers =~ s/(\.|\*|\(|\)|\||\\|\/|\?|\+|\[|\])//ig;
           $tempinmembername = "\_$inmembername\_";
	   $tempinmembername =~ s/(\.|\*|\(|\)|\||\\|\/|\?|\+|\[|\])//ig;
           if ($term_idbannedmembers =~ /$tempinmembername/i) { &error(" ID ����ֹ&������û���ر�վ�涨����� ID ($inmembername) ����ֹ���������ʣ�����ϵ����Ա��"); }
	}
      }

      if ($arrowformwhere ne "") {
	$arrowwhere = "no";
	use testinfo qw(ipwhere);
	$fromwhere = &ipwhere("$trueipaddress");
	if ($fromwhere ne "") {
	  $arrowformwhere =~ s/ ,/,/isg;
	  $arrowformwhere =~ s/, /,/isg;
	  my @arrowformwhere = split(/\,/,$arrowformwhere);
	  foreach (@arrowformwhere) {
	    next if ($_ eq "");
	    if (($fromwhere =~ m/$_/)||($_ =~ m/$fromwhere/)) { #����˵���
	    	$arrowwhere = "yes";
	    	last;
	    }
	  }
	}
	
      }

      if (open(FILE, "${lbdir}data/ipbans.cgi")) {
            my @term_bannedmembers = <FILE>;
            close(FILE);
            my @term_vipmembers = grep(/^[0-9]/, @term_bannedmembers);
            @term_bannedmembers = grep(/^\-/, @term_bannedmembers);
            my $ipallow = "yes";

            foreach (@term_bannedmembers) {
                s/\r//sg;
                s/^\-//sg;
                chomp;
                next if ($_ eq "");
                if ($trueipaddress =~ /^$_/ || $ipaddress =~ /^$_/) {
                    $ipallow = $_;
                    last;
                }
            }
            foreach (@term_vipmembers) {
                s/\r//sg;
                chomp;
                next if ($_ eq "");
                if ($trueipaddress =~ /^$_/ || $ipaddress =~ /^$_/) {
                    $ipallow = "yes";
                    $arrowwhere = "yes";
                    last;
                }
            }
            &error("��������ֹ&����̳���涨��������Ե��� ( $fromwhere) ����ֹ���ʱ���̳���������ʣ�����ϵ����Ա��") if ($arrowwhere eq "no");
#            if ($arrowwhere eq "no") { print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES"); exit; }
            &error(" IP ����ֹ&������û���ر�վ�涨����� IP ($ipallow) ����ֹ���������ʣ�����ϵ����Ա��") if ($ipallow ne "yes");
      }

      #д�뻺���־
      $infilemembername =~ s/\.\.//g;
      $infilemembername =~ s/[\\\/]//isg;
      open (FILE, ">${lbdir}cache/id/$infilemembername.cgi");
      print FILE "exit;";
      close(FILE);
1;
