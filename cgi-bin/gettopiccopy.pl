#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    $tempaccess = "forumsallowed". "$inforum";
    $testentry = $query->cookie("$tempaccess");
    if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("��������&�Բ������������Ʊ�����̳�����ӣ�"); }
    &error("��ͨ����&���˲��ܲ鿴�������ݣ���ע����¼������") if (($guestregistered eq "off")&&($inmembername eq "����"));
    &error("��ͨ����&���˲��ܲ鿴�������ݣ���ע����¼������") if ($waterwhenguest eq "yes" && $inmembername eq "����");

    open(FILE, "${lbdir}forum$inforum/$intopic.thd.cgi");
    my @threads = <FILE>;
    close(FILE);
    $posttoget = $inpostno - 1;
    ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post) = split(/\t/, $threads[$posttoget]);
    $topictitle =~ s/^����������//;

	if ($addtopictime eq "yes") {
	    my $topictime = &dispdate($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
	    $topictitle = "[$topictime] $topictitle";
	}

    $post =~ s/\<p\>/\n\n/ig;
    $post =~ s/\<br\>/\n/ig;
    
     if (($post=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg)||($post=~/LBSALE\[(.*?)\]LBSALE/sg)) {
        unless ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($inmembmod eq "yes")|| ($myrating >= $1)) {
	    &error("��������&�Բ������������Ʊ������ӣ�");
        }
        else {
	    $post=~ s/LBHIDDEN\[(.*?)\]LBHIDDEN//isg;
	    $post=~ s/LBSALE\[(.*?)\]LBSALE//isg;
	}        	
    }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") {
     	    &whosonline("$inmembername\t$forumname\tnone\t��������<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t");
	} else {
	    &whosonline("$inmembername\t$forumname(��)\tnone\t���Ʊ�������\t");
	}
    }

    &getmember($membername, "no");
    &error("��������&�Բ������������Ʊ����ε����ӣ�") if (($membercode eq "masked")&&($mymembercode ne "ad")&&($mymembercode ne 'smo')&&($inmembmod ne "yes"));

    $post =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg;
    $post =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg;
    $post =~ s/\[hide\](.+?)\[\/hide\]//isg;
    $post =~ s/\[watermark\](.+?)\[\/watermark\]/\n\(ˮӡ���ֲ��ܸ���\)\n/isg;
    $post =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\[��������\]/isg if ($usecurl ne "no");
    $postdate = $postdate + ($timedifferencevalue + $timezone)*3600;
    $postdate = &dateformat("$postdate");
    $rawpost  = $post;
    $rawpost  =~ s/\[ALIPAYE\](.*)\[ALIPAYE\]//isg; 
    $rawpost  =~ s/\[hide\](.*)\[\/hide\]//isg; 
    $rawpost =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg;
    $rawpost  =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg; 
    $rawpost =~ s/\[DISABLELBCODE\]//isg;
    $rawpost =~ s/\[ADMINOPE=(.+?)\]//isg;
    if ($rawpost =~ /\[POSTISDELETE=(.+?)\]/) {
    	if ($1 ne " ") { $presult = "�������ɣ�$1"; } else { $presult = "<BR>"; }
        $rawpost = "�����������Ѿ����������Σ�$presult";
    }

    &mischeader("��������");

    $temppost = qq~-=-=-=-=-=>\n$rawpost\n-=-=-=-=-=>~;
    $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=4 cellspacing=1 width=100%><tr><td bgcolor=$titlecolor $catbackpic colspan=2>
<form action="$thisprog" method=post><font color=$titlefontcolor>���⣺ $topictitle</td></tr>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>��������</b><p></font></td><td bgcolor=$miscbackone>&nbsp;&nbsp;<textarea cols=90 rows=12 wrap="soft" name="inpost">$temppost</textarea><BR><BR></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type="button" value="������ʾ����" onClick="this.form.inpost.focus();this.form.inpost.select();">����<input type="button" value="���Ƶ�������" name="cmdCopy" onClick="copy(this.form.inpost)"></center></td></tr></td></table></table>
<SCRIPT>valignend()</SCRIPT>
    ~;
1;
