#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    my $filetoopen = "${lbdir}forum$inforum/foruminfo.cgi";
    open(FILE, "$filetoopen");
    my $forums = <FILE>;
    close(FILE);
    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forums);

    if ($category=~/childforum-[0-9]+/) {
	$tempforumno=$category;
	$tempforumno=~s/childforum-//;
	$filetoopen = "${lbdir}forum$tempforumno/foruminfo.cgi";
	open(FILE, "$filetoopen");
	$forums = <FILE>;
	close(FILE);
	(undef, undef, undef, $tempforumname, undef) = split(/\t/,$forums);
	$addlink  = qq~ �� <a href=forums.cgi?forum=$tempforumno>$tempforumname</a>~;
    }
    $forumdescription = &HTML("$forumdescription");
    $forumdescription =~ s/<BR>//isg;
    $forumdescription =~ s/<P>//isg;

    if ($indexforum ne "no") {
        $titleoutput = qq~<BR><table width=\$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> $forumdescription</td></tr></table><table width=\$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=\$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr height=25><td bgcolor=\$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=\$navfontcolor><a href=leobbs.cgi>$boardname</a>$addlink �� <a href=forums.cgi?forum=$inforum>$forumname</a> �� misctypehtc</td><td bgcolor=\$navbackground align=right></td></tr></table></td></tr></table>~;
    } else {
        $titleoutput = qq~<BR><table width=\$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> $forumdescription</td></tr></table><table width=\$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=\$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr height=25><td bgcolor=\$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=\$navfontcolor><a href=forums.cgi?forum=$inforum>$forumname</a> ����misctypehtc</td><td bgcolor=\$navbackground align=right></td></tr></table></td></tr></table>~;
    }

    $titleoutput .= qq~<br>~;
    if ((!(-e "${lbdir}cache/forumstitle$inforum.pl"))&&($forumid ne "")) {
	open (FILE, ">${lbdir}cache/forumstitle$inforum.pl");
	$titleoutput =~ s/\\/\\\\/isg;
	$titleoutput =~ s/~/\\\~/isg;
	$titleoutput =~ s/\$/\\\$/isg;
	$titleoutput =~ s/\@/\\\@/isg;
        $titleoutput =~ s/\\\$/\$/isg;
	print FILE qq(\$titleoutput = qq~$titleoutput~;\n);
        $titleoutput =~ s/\$/\\\$/isg;
	$titleoutput =~ s/\\\~/~/isg;
	$titleoutput =~ s/\\\$/\$/isg;
	$titleoutput =~ s/\\\@/\@/isg;
	$titleoutput =~ s/\\\\/\\/isg;
	print FILE "1;\n";
	close (FILE);
    }
$titleoutput  =~ s/\$tablewidth/$tablewidth/isg;
$titleoutput  =~ s/\$navborder/$navborder/isg;
$titleoutput  =~ s/\$navbackground/$navbackground/isg;
$titleoutput  =~ s/\$navfontcolor/$navfontcolor/isg;
1;
