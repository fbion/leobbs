#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

        open(FILE, "${lbdir}forum${inforum}/foruminfo.cgi");
        my $forums = <FILE>;
        close(FILE);
        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc, $forumpass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $forums);

        #����̳����̳�
        if ($category =~ /childforum-[0-9]+/) {
                my $tempforumno = $category;
                $tempforumno =~ s/childforum-//;
                open(FILE, "${lbdir}forum${tempforumno}/foruminfo.cgi");
                my $forums1 = <FILE>;
                close(FILE);
                (undef, undef, undef, undef, undef, my $fmod, undef) = split(/\t/, $forums1);
                $forummoderator .= ",$fmod";
        }

        #�����������
        if (open(CATEFILE, "${lbdir}boarddata/catemod${categoryplace}.cgi")) {
                my $catemods = <CATEFILE>;
                close(CATEFILE);
                chomp($catemods);
                $forummoderator .= ",$catemods";
        }

        $forummoderator =~ s/\, /\,/gi;
        $forummoderator =~ s/ \,/\,/gi;
        $forummoderator =~ s/\,\,/\,/gi;
        $forummoderator =~ s/\,$//gi;
        $forummoderator =~ s/^\,//gi;
	if (!(-e "${lbdir}cache/forumsone$inforum.pl")) {
	    open (FILE, ">${lbdir}cache/forumsone$inforum.pl");
	    $forums =~ s/\\/\\\\/isg;
	    $forums =~ s/~/\\\~/isg;
	    $forums =~ s/\$/\\\$/isg;
	    $forums =~ s/\@/\\\@/isg;
	    print FILE qq(\$forums = qq~$forums~;\n);
	    $forums =~ s/\\\~/~/isg;
	    $forums =~ s/\\\$/\$/isg;
	    $forums =~ s/\\\@/\@/isg;
	    $forums =~ s/\\\\/\\/isg;
	    print FILE qq~\$forummoderator = qq($forummoderator);\n~;
	    print FILE "1;\n";
	    close (FILE);
	}
1;
