#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    if ($avatars eq "on") {
	if (($personalavatar)&&($personalwidth)&&($personalheight)) { #�Զ���ͷ�����
	    $personalavatar =~ s/\$imagesurl/${imagesurl}/o;
	    if (($personalavatar =~ /\.swf$/i)&&($flashavatar eq "yes")) {
		$personalavatar=uri_escape($personalavatar);
	        $useravatar = qq(<br><OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>);
	    }
	    else {
	        $personalavatar=uri_escape($personalavatar);
		$useravatar = qq(<br><a href=profile.cgi?action=modify title=�༭���ĸ�������><img src=$personalavatar width=$personalwidth height=$personalheight border=1></a>);
	    }
	}
        elsif (($useravatar ne "noavatar") && ($useravatar)) {
            $useravatar=uri_escape($useravatar);
	    $useravatar = qq(<br><a href=profile.cgi?action=modify title=�༭���ĸ�������><img src=$imagesurl/avatars/$useravatar.gif border=1></a>);
        }
	elsif (($oicqnumber) && ($oicqnumber =~ /[0-9]/)) {
	    $useravatar = qq~<a href=profile.cgi?action=modify title="���� QQ ������"><img src=http://qqshow-user.tencent.com/$oicqnumber/11/00/ width=70 height=113 border=1></a>~;
	}
        else { $useravatar=qq(<br><a href=profile.cgi?action=modify title=�༭���ĸ�������><img src=$imagesurl/avatars/noavatar.gif border=1></a>); }
    }
    else { $useravatar=qq(<br><a href=profile.cgi?action=modify title=�༭���ĸ�������><img src=$imagesurl/avatars/noavatar.gif border=1></a>); }

    open (MSGOUT, "${lbdir}$msgdir/out/${memberfilename}_out.cgi");
    sysread(MSGOUT, my $totalmessagesout,(stat(MSGOUT))[7]);
    close (MSGOUT);
    $totalmessagesout =~ s/\r//isg;
    my @allmessages = split (/\n/,$totalmessagesout);
    $totalmessagesout = @allmessages;

    if ($unread eq "0") { $inboximg = qq~<img src=$imagesurl/images/inboxnonew.gif width=17>~; } else { $inboximg = qq~<img src=$imagesurl/images/inboxnew.gif width=17>~; }

    require "${lbdir}data/cityinfo.cgi";
    $mymoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

    $mymoney = "<font title=$mymoney>>999999999</font>" if ($mymoney > 999999999 );
    $moneyname ="�װ�Ԫ" if ($moneyname eq "");

    my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $bankadd1, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
    unless ($mystatus eq "1" || $mystatus eq "-1" || $ebankdata eq "") {
	$mysaves = "<B>û����</B>";
	$myloan = "<B>û����</B>";
    }
    else {
        if ($mystatus) {
	    $mysaves = "<B>$mysaves</B> $moneyname";
	    if ($myloan) {
	        $myloan = "<B>$myloan</B> $moneyname";
	    } else {
	        $myloan = "<B>û����</B>";
	    }
        } else {
	    $mysaves = "<B>û����</B>";
	    $myloan = "<B>û����</B>";
        }
    }

    $modscard_link = qq~\n :: [ <span style=cursor:hand onClick="javascript:openScript('modscard.cgi',420,320)"><font color=$fonthighlight><B>����ǩ��</B></font></span> ]~ if($membercode eq "ad" || $membercode eq "smo" || $membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo");

    $mysaves = "<font title=$mysaves>>999999999</font>" if ($mysaves > 999999999 );
    $myloan = "<font title=$myloan>>999999999</font>" if ($myloan > 999999999 );
    $postdel = 0 if ($postdel eq "");
    
    my $lasttimes = $lastgone + ($timedifferencevalue + $timezone)*3600;
    $lasttimes = &dateformat($lasttimes);

    my $inmembernames = uri_escape($inmembername);
    if (($maxmsgno eq "")||($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "amo")||($membercode eq "mo")) { $maxmsgno = qq~<B>û������</B>~; } else { $maxmsgno = qq~<font color=$fonthighlight><B>$maxmsgno</B></font> ��~; }
    my $myoutput = qq~<tr><td bgcolor=\$titlecolor colspan=4 \$catbackpic><font color=\$titlefontcolor><B>-=>  ����״̬</B>  [ ���ԣ�$trueipaddress��$fromwhere1 ��ϵͳ��$osinfo��$browseinfo��������ʱ�䣺$lasttimes ]</td></tr>
<tr><td bgcolor=\$forumcolorone align=center width=18>$inboximg</td>
<td bgcolor=\$forumcolortwo width=130 align=center>$useravatar</td>
<td bgcolor=\$forumcolortwo width=*><img src=$imagesurl/images/none.gif width=340 height=1><BR>
<table cellpadding=6 cellspacing=0 width=100%>
<tr><td nowarp>
<font color=\$fontcolormisc>* <B>�ҵĲƲ�</B></font><BR><img src=$imagesurl/images/none.gif height=6><BR>
�ֽ�: <B>$mymoney</B> $moneyname<BR>
���: $mysaves<BR>
����: $myloan
</td>
<td nowarp>
<font color=\$fontcolormisc>* <B>�ҵĶ���Ϣ</B></font><BR><img src=$imagesurl/images/none.gif height=6><BR>
[<a href=messanger.cgi?action=inbox target=_blank>�ռ���</a>]: <B>totalmessageshtc</B><BR>
[<a href=messanger.cgi?action=outbox target=_blank>������</a>]: <B>$totalmessagesout</B><BR>
��������: $maxmsgno<BR>
</td>
<td nowarp>
<font color=\$fontcolormisc>* <B>�ҵ�����</B></font><BR><img src=$imagesurl/images/none.gif height=6><BR>
������: <B>$numberofposts</B><BR>
�ظ���: <B>$numberofreplys</B><BR>
��ɾ��: <B>$postdel</B><BR>
</td></tr></table><img src=$imagesurl/images/none.gif height=9><BR><center>
[ <a href=fav.cgi?action=show&member=$inmembernames>�ҵ��ղؼ�</a> ] :: [ <span style=cursor:hand onClick="javascript:openScript('recopr.cgi?action=post',420,320)">�ұ��ظ�������</span> ] :: [ <span style=cursor:hand onClick="javascript:openScript('recopr.cgi?action=reply',420,320)">�Ҳ��������</span> ] :: [ <span style=cursor:hand onClick="javascript:openScript('recopr.cgi?action=new',420,320)">��̳������</span> ]$modscard_link</center>
</td>~;
if ($forumcached eq "yes") {
    open (FILE, ">${lbdir}cache/myinfo/$memberfilename.pl");
    $myoutput =~ s/\\/\\\\/isg;
    $myoutput =~ s/~/\\\~/isg;
    $myoutput =~ s/\$/\\\$/isg;
    $myoutput =~ s/\@/\\\@/isg;
    $myoutput =~ s/\\\$/\$/isg;
    print FILE qq(\$output .= qq~$myoutput~;\n);
    $myoutput =~ s/\$/\\\$/isg;
    $myoutput =~ s/\\\~/~/isg;
    $myoutput =~ s/\\\$/\$/isg;
    $myoutput =~ s/\\\@/\@/isg;
    $myoutput =~ s/\\\\/\\/isg;
    print FILE "1;\n";
    close (FILE);
}
$myoutput =~ s/\$titlecolor/$titlecolor/isg;
$myoutput =~ s/\$catbackpic/$catbackpic/isg;
$myoutput =~ s/\$titlefontcolor/$titlefontcolor/isg;
$myoutput =~ s/\$forumcolorone/$forumcolorone/isg;
$myoutput =~ s/\$forumcolortwo/$forumcolortwo/isg;
$myoutput =~ s/\$fontcolormisc/$fontcolormisc/isg;
$output .= $myoutput;
1;
