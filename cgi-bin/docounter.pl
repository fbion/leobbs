#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    &winlock("${lbdir}data/counter.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    if (-e "${lbdir}data/counter.cgi") {
    	open(FILE,"+<${lbdir}data/counter.cgi");
        $count = <FILE>;
        $onlinemax = @onlinedata;
        ($count1,$count2,$onlinemax1,$onlinemaxtime1) = split(/\t/, $count);
        $onlinemaxtime1 = $currenttime if ($onlinemaxtime1 eq "");
        $count1=0 if ($count1 eq "");
        $count2=0 if ($count2 eq "");
        $count2++;
        $count1++ if ($memberprinted eq "no");
        if ($onlinemax < $onlinemax1) {
	    $onlinemax = $onlinemax1; $onlinemaxtime = $onlinemaxtime1;
        } else { $onlinemaxtime = $currenttime; }

        seek(FILE,0,0);
        print FILE "$count1\t$count2\t$onlinemax\t$onlinemaxtime\t";
        close(FILE);
    } else {
        $onlinemax = @onlinedata;
        $onlinemaxtime = $currenttime;
        $count1 = $count2 = 1;
    	open(FILE,">${lbdir}data/counter.cgi");
        print FILE "1\t1\t$onlinemax\t$onlinemaxtime\t";
        close(FILE);
    }
    &winunlock("${lbdir}data/counter.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
1;
