#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

	   if (($onlinedatanumber >= $arrowonlinemax)&&($arrowonlinemax > 0)&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")) {
       	      print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
              print "<BR>������æ���Ѿ�������̳������������������<BR><BR>Ŀǰ��̳���� $onlinedatanumber �ˣ��������ͬʱ���� $arrowonlinemax �ˡ�";
              exit;
           }
	   use testinfo qw(ipwhere osinfo browseinfo);
	   eval { $osinfo=&osinfo(); };
    	   if ($@) { $osinfo="Unknow"; }
	   eval { $browseinfo=&browseinfo(); };
    	   if ($@) { $browseinfo="Unknow"; }
           my $fromwhere = &ipwhere("$trueipaddress");
           my $tempdata = "$tempusername\t$currenttime\t$currenttime\t$where\t$ipall\t$osinfo\t$browseinfo\t$where2\t$fromwhere\t$membercode\t$hidden\t$sex\t" ;
           $fromwhere1 = $fromwhere;
           if ($tempusername !~ /^����/) { require "douplogintime.pl"; &uplogintime("$tempusername","T"); }
           $tempdata =~ s/[\a\f\n\e\0\r]//isg;
           push(@onlinedata,$tempdata);
1;
