#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    if ($startnewthreads eq "onlysub") {&error("����&�Բ��������Ǵ�����̳�����������ԣ�"); }
    $testentry = $query->cookie("forumsallowed$inforum");
    if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("����&�Բ������������ڴ���̳����"); }
    if ($postopen eq "no") { &error("�����ظ�����&�Բ��𣬱���̳���������ظ����⣡"); }
    &error("��ͨ����&���˲��ܲ鿴�������ݣ���ע����¼������") if (($guestregistered eq "off")&&($inmembername eq "����"));

    open(FILE, "${lbdir}forum$inforum/$intopic.thd.cgi");
    @threads = <FILE>;
    close(FILE);
    $posttoget = $inpostno - 1;

    ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon) = split(/\t/, $threads[$posttoget]);
    $topictitle =~ s/^����������//;

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") {
	    &whosonline("$inmembername\t$forumname\tnone\t���ûظ�<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t");
	}
	else {
    	    &whosonline("$inmembername\t$forumname(��)\tnone\t���ûظ���������\t");
	}
    }

    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     {  $onlinetime = $onlinetime + $onlinetimeadd; &error("�ظ�����&�Բ��𣬱���̳����������ʱ������ $onlinepost ����û��ظ����⣡��Ŀǰ�Ѿ����� $onlinetime �룡<BR>�������ʱ��ͳ�Ʋ���ȷ,�����µ�½��̳һ�μ��ɽ����"); }

    &getmember($membername,"no");
    $post = "���û��ķ����Ѿ������Σ�" if ($membercode eq "masked");
    $membercode = $mymembercode;
	
    if  ($post=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg){
	$checked=$1;
	if ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($mymembercode eq "mo") || ($mymembercode eq "amo") || ($inmembmod eq "yes")|| ($myrating >= $1) ){
	    $weiwangoptionbutton=~s/value=$checked/value=$checked selected/isg;
	    $weiwangoptionbutton=~s/value=\"yes\" /value=\"yes\" checked /;
	}
	undef $checked;
	$post="(��������)";
    }
    if  ($post=~/LBSALE\[(.*?)\]LBSALE/sg){
	$post="(��������)";
    }

    $post =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg;
    $post =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg;
    $post =~ s/\[hide\](.+?)\[\/hide\]//isg;
    $post =~ s/\[watermark\](.+?)\[\/watermark\]/\n\(ˮӡ���ֲ�������\)\n/isg;
    $post =~ s/(\&\#35\;|#)Moderation Mode//isg;
    $post =~ s/\<p\>/\n\n/ig;
    $post =~ s/\<br\>/\n/ig;
    $post =~ s/ \&nbsp;/  /ig;
    $post =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\[��������\]/isg if ($usecurl ne "no");
    $post =~ s/\[DISABLELBCODE\]//isg;
    $post =~ s/\[ADMINOPE=(.+?)\]//isg;
    $post  =~ s/\[ALIPAYE\](.*)\[ALIPAYE\]//isg; 
    $post2 =~ s/ \n/\n/isg;
    $post2 =~ s/��\n/\n/isg;
    if ($post =~ /\[POSTISDELETE=(.+?)\]/) {
    	if ($1 ne " ") { $presult = "�������ɣ�$1"; } else { $presult = ""; }
        $post = "�����������Ѿ����������Σ�$presult";
    }

    $membernametemp=$membername;

    $postdate = $postdate + ($timedifferencevalue + $timezone)*3600;
    $postdate = &dateformat("$postdate");
    $rawpost = $post;

    &mischeader("���ûظ�����");

    if ($emoticons eq "on") {
        $emoticonslink = qq~<li><a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">����<B>ʹ��</B>�����ַ�ת��</a>~;
        $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>���Ƿ�ϣ��<b>ʹ��</b>�����ַ�ת�������������У�<br>~;
    }

    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>�лظ�ʱʹ���ʼ�֪ͨ����<br>~;
    }

    $output .= qq~<script language="javascript">function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}</script>~;
    
    $rawpost =~ s/\[���(.+?)�����(.+?)�༭\]\n//isg;
    $rawpost =~ s/LBHIDDEN\[(.*?)\]LBHIDDEN//sg;
    $rawpost =~ s/LBSALE\[(.*?)\]LBSALE//sg;
    $rawpost =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
    $rawpost =~ s/\[quote\](.*)\[\/quote\]//isg;
    $rawpost =~ s/\[equote\](.*)\[\/equote\]//isg;
    $rawpost =~ s/\[fquote\](.*)\[\/fquote\]//isg;
    $rawpost =~ s/\[hide\](.*)\[hide\](.*)\[\/hide](.*)\[\/hide\]//isg; 
    $rawpost =~ s/\[hide\](.*)\[\/hide\]//isg; 
    $rawpost =~ s/\[post=(.+?)\](.+?)\[\/post\](.*)\[post=(.+?)\](.+?)\[\/post\]//isg; 
    $rawpost =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg; 
    $rawpost =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2/isg;
    $rawpost =~ s/\:.{0,20}\://isg;
    $rawpost =~ s/\<img\s*(.*?)\s*\>//isg;
    $rawpost =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|jpeg|bmp|gif|swf)/($2\.$3)/isg;
    $rawpost =~ s/\&nbsp;/ /ig;
    $rawpost =~ s/( )+$//isg;
    $rawpost =~ s/^( )+//isg;
    $rawpost =~ s/\[.+?\]//g;
    $rawpost =~ s/ \n/\n/isg;
    $rawpost =~ s/��\n/\n/isg;
    $rawpost =~ s/(\n)+/\n/isg;
    $rawpost =~ s/^\n//isg;
    chomp $rawpost;

    my @postall = split(/\n/,$rawpost);
    my $postall = @postall;
    if ($postall > 4) { $rawpost = "$postall[0]\n$postall[1]\n$postall[2]\n$postall[3]\n..."; }
    $rawpost = &lbhz($rawpost,200);

    $inpost = qq~\[quote\]\[b\]����������\[u\]$membernametemp\[\/u\]�� \[i\]$postdate\[\/i\] ��������ݣ�\[\/b\]\n$rawpost\n\[\/quote\]\n~;
    if ($htmlstate eq "on")     { $htmlstates = "����";     } else { $htmlstates = "������";     }
    if ($idmbcodestate eq "on") { $idmbcodestates = "����"; $canlbcode =qq~<input type=checkbox name="uselbcode" value="yes" checked>ʹ�� LeoBBS ��ǩ��<br>~; } else { $idmbcodestates = "������"; $canlbcode= "";}
    if ($useemote eq "no") { $emotestates = "������"; } else { $emotestates = "����"; }

    $output .= qq~<script>
var autoSave = false;
function storeCaret(textEl) {if (textEl.createTextRange) textEl.caretPos = document.selection.createRange().duplicate();if (autoSave)savePost();}
function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
</script>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic>
<form action=$thisprog method=post name=FORM enctype="multipart/form-data">
<input type=hidden name=action value=addreply>
<input type=hidden name=forum value=$inforum>
<input type=hidden name=topic value=$intopic>
<font color=$titlefontcolor><b>�������</b>�� $topictitle</td></tr>
~;
    &posttable(2);
    require "dothreadreview.pl";
1;
