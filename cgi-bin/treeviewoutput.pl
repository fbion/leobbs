#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    @treelist=();
    $pages = qq~<font color=$menufontcolor><b>�����⹲��һҳ</b>~;

if ($tablewidth > 100) {
    if ($tablewidth > 1000) { $topictitlemax = 115; } elsif ($tablewidth > 770) { $topictitlemax = 94; } else { $topictitlemax = 58; }
} else {
    if ($screenmode >=10) { $topictitlemax = 115; } elsif ($screenmode >=8) { $topictitlemax = 94; } else { $topictitlemax = 58; }
}

    $output .= qq~<SCRIPT>valignend()</SCRIPT><p><SCRIPT>valigntop()</SCRIPT><table cellpadding="5" style="border-collapse: collapse" width=$tablewidth cellspacing="0" bordercolor=$tablebordercolor border=1 align=center><tr><td colspan=3 bgcolor=$titlecolor $catbackpic><font color=$titlefontcolor><B>&nbsp;* ����Ŀ¼</B></td></tr>~;
    $i = 0;
    foreach (@threads) {

	  if ($man ne '') {
	    ($none,$membername, $topictitle, $postipaddresstemp, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/,$_);
	  } else {
	    ($membername, $topictitle, $postipaddresstemp, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/,$_);
	  }

    if ($jfmark eq "yes" &&  $i == 0) {
	if ($post =~m/\[jf=(.+?)\](.+?)\[\/jf\]/isg){ 
	    $jfpost=$1;
	    if (($jfpost <= $jifen)||($mymembercode eq "ad")||($mymembercode eq "smo")||($myinmembmod eq "yes")||(lc($membername) eq lc($inmembername))){ 
	    } else { 
	        &error("������&���ֱ���ﵽ $jfpost ���ܲ鿴����Ŀǰ�Ļ����� $jifen ��") if ($noviewjf eq "yes");
   	    }
   	}
    }

	$topictitle =~ s/^����������//;

	chomp $posticon;
	$postdate = &shortdate($postdate + $addtimes);

        $post =~ s/\[ADMINOPE=(.+?)\]//isg;

	if ($post =~ /\[POSTISDELETE=(.+?)\]/) {
	    $post = "�˻ظ��Ѿ�������";
	}

        if (($post =~ /LBHIDDEN\[(.*?)\]LBHIDDEN/)||($post =~ /LBSALE\[(.*?)\]LBSALE/)) {
            $post = "����";
        } else {
	    $post =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
	    $post =~ s/\[quote\](.*)\[\/quote\]//isg;
	    $post =~ s/\[equote\](.*)\[\/equote\]//isg;
	    $post =~ s/\[fquote\](.*)\[\/fquote\]//isg;
	    $post =~ s/\[hidepoll\]//isg;
	    $post =~ s/\[���(.+?)�����(.+?)�༭\]\n//isg;
	    $post =~ s/\[hide\](.*)\[hide\](.*)\[\/hide](.*)\[\/hide\]//isg; 
	    $post =~ s/\[hide\](.*)\[\/hide\]//isg; 
	    $post =~ s/\[post=(.+?)\](.+?)\[\/post\](.*)\[post=(.+?)\](.+?)\[\/post\]//isg; 
	    $post =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg;
	    $post =~ s/\[jf=(.+?)\](.+?)\[\/jf\](.*)\[jf=(.+?)\](.+?)\[\/jf\]//isg; 
	    $post =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg;
	    $post =~ s/\[curl=(http|https|ftp):\/\/(.*?)\]/\[��������\]/isg;
	    $post = &temppost("$post");
	}

	if (length($post)>=$topictitlemax) {
            $post=&lbhz($post,$topictitlemax);
	}

	if ($post eq "") { $post="(������)"; }

	if (($posticon ne "")&&($posticon !~ /\<br\>/i)) { $posticon = qq~<img src=$imagesurl/posticons/$posticon $defaultsmilewidth $defaultsmileheight>~; } else { $posticon = ""; }

	my $memberfilename = $membername;
	$memberfilename =~ y/ /_/;
	$memberfilename =~ tr/A-Z/a-z/;
	if ($membername=~/\(��\)/) {
	    $membername=~s/\(��\)//isg;
	    $h4 = qq~<font color=$postfontcolorone title=��Ϊδע���û�>$membername</font>~;
	}
	else {
	    $h4 = qq~<a href=profile.cgi?action=show&member=~ . uri_escape($memberfilename) . qq~ title=\"�鿴$membername�ĸ�������\">$membername</a>~;
	}
	
	$editpostnumber=$i+1; 
	$h5="����"; 
   	$h5 =qq(<input type="checkbox" name="postno$editpostnumber" value="yes">) if(($mymembercode eq "ad")||($mymembercode eq 'smo')||($mymembercode eq 'cmo')||($myinmembmod eq "yes"));
	if ($i==0) { $h3 = "��������"; } else { $h3 = "$h5�ظ���"; } 

	if ($treebackcolor ne $postcolorone) { $treebackcolor=$postcolorone; } else { $treebackcolor=$postcolortwo; }
	if ($i==$replynum) {
	    $treefontcolor="$fonthighlight";
            $h1=$h2="";
	}
	else {
	    $treefontcolor=$postfontcolorone;
	    $h1="<a href=$thisprog?forum=${inforum}&topic=${intopic}&show=$show&replynum=$i>";
	    $h2="</a>";
	}
	$output .=qq~<tr bgcolor="$treebackcolor"><td><font color=$treefontcolor> $h3 $posticon $h1 $post $h2</td><td width=130> &nbsp ���ߣ�$h4</td><td width=70 align=right> $postdate&nbsp;</font></td></tr>~;
	$i ++;
    }
    $output .= qq~</table>~;
1;