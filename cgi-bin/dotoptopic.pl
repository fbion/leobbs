#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

unlink("${lbdir}cache/forumstoptopic$inforum.pl") if ((-M "${lbdir}cache/forumstoptopic$inforum.pl") *86400 >= 300);
if ($abstopcount > 0) {
    foreach (@absontop) {
	chomp $_;
    	if ($_ eq "") { $abstopcount --; next; }
	my ($tempinforum,$tempintopic) = split (/\|/,$_);
	my $rr = &readthreadpl($tempinforum,$tempintopic);
	if ($rr ne "") {
	    (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp, my $addmetype) = split (/\t/,$rr);
	    push (@toptopic, "$topicid\t$tempinforum\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$addmetype");
	} else { $abstopcount --;}
    }
}
else { undef @toptopic; }

if ($cattopcount > 0) {
    foreach (@catontop) {
        chomp $_;
        my ($tempinforum, $tempintopic) = split (/\|/, $_);
        if ($_ eq "" || $absontopdata =~ /\_$tempinforum\|$tempintopic\_/) {
            $cattopcount--;
            next;
        }
        my $rr = &readthreadpl($tempinforum, $tempintopic);
        if ($rr ne "") {
            my ($lastpostdate, $topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $posticon, $posttemp, $addmetype) = split (/\t/, $rr);
            push(@toptopic, "$topicid\t$tempinforum\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$addmetype");
        } else { $cattopcount--; }
    }
}
else { undef @toptopic if ($abstopcount <= 0); }

if ($topcount > 0) {
    foreach (@ontop) {
        chomp $_;
  	if ($_ eq "") { $topcount --; next; }
        if ($absontopdata =~ /\_$inforum\|$_\_/) { $topcount --; next; }
        if ($catontopdata =~ /\_$inforum\|$_\_/) { $topcount --; next; }
        my $rr = &readthreadpl($inforum,$_);
        if ($rr ne "") {
            (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp, my $addmetype) = split (/\t/,$rr);
            push (@toptopic, "$topicid\t$inforum\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$addmetype");
        } else { $topcount --;}
    }
}
else { undef @toptopic if ($abstopcount + $cattopcount <= 0); }

if (!(-e "${lbdir}cache/forumstoptopic$inforum.pl")) {
    open (FILE, ">${lbdir}cache/forumstoptopic$inforum.pl");
    print FILE qq~\@toptopic = (~;
    foreach (@toptopic) {
        chomp $_;
        $_ =~ s/\\/\\\\/isg;
        $_ =~ s/\"/\\\"/isg;
        $_ =~ s/\$/\\\$/isg;
        $_ =~ s/\@/\\\@/isg;
        print FILE qq~"$_",~ if ($_ ne "");
        $_ =~ s/\\\"/\"/isg;
        $_ =~ s/\\\$/\$/isg;
        $_ =~ s/\\\@/\@/isg;
        $_ =~ s/\\\\/\\/isg;
    }
    print FILE ");\n";
    print FILE "\$abstopcount = $abstopcount;\n";
    print FILE "\$cattopcount = $cattopcount;\n";
    print FILE "\$topcount = $topcount;\n";
    print FILE "1;\n";
    close (FILE);
}
1;
