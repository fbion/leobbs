#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

unlink ("${lbdir}cache/forumonline.pl") if ((-M "${lbdir}cache/forumonline.pl") *86400 >= 180);
    foreach (@onlinedata) {
	chomp $_;
	next if ($_ eq "");
	(my $savedusername, my $no, $no, my $savedwhere, $no, $no, $no, $no, $no, $no, my $hiddened) = split(/\t/, $_);
	(my $lookfor, $no) = split(/\(/,$savedusername);
  	next if ($lookfor =~ m/[\(\)\*]/);
	$savedwhere=~ s/\(��\)$//isg;
	    if ($savedusername=~ /^����/) {
       	        $onlinehashguest{"$savedwhere"} ++;
	    } 
	    else {
	    	if ($hiddened eq 1) {
       	            $onlinehashguest{"$savedwhere"} ++;
       	        }
       	        else {
                    $onlinehashmember{"$savedwhere"} ++;
                    if ($onlinehashmember{"$savedwhere"} eq 1) { $onlinehashoutput{"$savedwhere"} .= qq~$savedusername~; } else { $onlinehashoutput{"$savedwhere"} .= qq~��$savedusername~; }
       	        }
	    }
    }
    my @forums1 = @rearrangedforums;
    push(@forums1, @forums);
    foreach (@forums1) {
    	chomp $_;
    	next if ($_ eq "");
    	($no,$no,$no,$fname) = split (/\t/,$_);
    	next if ($fname eq "");
	$onlinehashguest{"$fname"}  = 0 if ($onlinehashguest{"$fname"}  eq "");
	$onlinehashmember{"$fname"} = 0 if ($onlinehashmember{"$fname"} eq "");
        my $totleonline =$onlinehashguest{"$fname"}+$onlinehashmember{"$fname"};
	$onlinehashoutput{"$fname"} = qq~\|\| --= ��Ա�б��� $onlinehashmember{"$fname"} �ˣ� =--\|$onlinehashoutput{"$fname"}\|~ if ($onlinehashmember{"$fname"} > 0);
        if ($onlinehashguest{"$fname"} > 0) {
	    $guestadd = qq~������ $onlinehashguest{"$fname"} �����ˣ�~;
        }
        else { undef $guestadd; }
	$titleinfos{"$fname\n"} = qq~ TITLE="Ŀǰ���� $totleonline ���ڴ���̳��$guestadd��$onlinehashoutput{"$fname"}"~;
	$outfileinfo .= qq~$fname\n$titleinfos{"$fname\n"}\n~;
	$titleinfos{"$fname\n"} =~ s/\|/\n/isg;
    }
    if (!(-e "${lbdir}cache/forumonline.pl")) {
        open (FILE, ">${lbdir}cache/forumonline.pl");
        print FILE $outfileinfo;
        close(FILE);
    }
1;
