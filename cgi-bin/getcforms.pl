#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

require "${lbdir}data/category_display.cgi" if(-e "${lbdir}data/category_display.cgi");
my $is_in_other_mode = 0;
my $now_display_count = 0;

$output .= qq~<p><SCRIPT>valigntop()</SCRIPT><table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td height=1></td></tr></table>~;

&getonlineno() if ($dispboardonline ne "no");

foreach (@childforum) {
    chomp $_;
    ($cforumname, $cforumdescription, $cprivateforum, $cstartnewthreads, $clastposter, $clastposttime1, $cthreads, $cposts,$chiddenforum,$cforumid, $modout, $cteam, $cmiscad4, $ctodayforumpost, $cmiscad5) = split(/\t/,$_);
    next unless (($chiddenforum eq "no")||($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo"));
    if ($pforum_display_type{$forumid} ne "basic") {
    $cforumnameadd = $cforumname;
    $cforumnameadd1 = $cforumnameadd;
    $cforumnameadd1 =~ s/\'/\\'/g;
    $titleinfos{"$cforumname\n"} =~ s/\|/\n/isg;

    $cforumname = qq~<a href=forums.cgi?forum=$cforumid$titleinfos{"$cforumname\n"}><font color=$fontcolormisc2>$cforumname</a>~;
    my $forumlastvisit = $lastvisitinfo{$cforumid};
    $folderpicture = qq(��);

    ($clastposttime,$threadnumber,$topictitle)=split(/\%\%\%/,$clastposttime1);

    my ($ctodayforumpost, $ctodayforumposttime) = split(/\|/,$ctodayforumpost);
    $ctodayforumpost = 0 if (($nowtime ne $ctodayforumposttime)||($ctodayforumpost eq ""));

    if (($clastposttime > $forumlastvisit)&&($inmembername ne "����")&&($action ne "resetall")) {
	if (($cforumpass)||($cprivateforum eq "yes")) { $folderpicture = qq~<img src=$imagesurl/images/$skin/$bm_havenew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
	    elsif ($cstartnewthreads eq "follow")     { $folderpicture = qq~<img src=$imagesurl/images/$skin/$pl_havenew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
	    elsif ($cstartnewthreads eq "yes")        { $folderpicture = qq~<img src=$imagesurl/images/$skin/$zg_havenew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
	    elsif ($cstartnewthreads eq "all")        { $folderpicture = qq~<img src=$imagesurl/images/$skin/$kf_havenew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
	    elsif ($cstartnewthreads eq "cert")       { $folderpicture = qq~<img src=$imagesurl/images/$skin/$rz_havenew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
        $cposts   = qq~<font color=$fonthighlight><b>$cposts</b></font>~;
	$cthreads = qq~<font color=$fonthighlight><b>$cthreads</b></font>~;
	$ctodayforumpost = qq~<font color=$fonthighlight><b>$ctodayforumpost</b></font>~;
    } else {
       	if (($cforumpass)||($cprivateforum eq "yes")) { $folderpicture = qq~<img src=$imagesurl/images/$skin/$bm_nonew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
	    elsif ($cstartnewthreads eq "follow")     { $folderpicture = qq~<img src=$imagesurl/images/$skin/$pl_nonew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
	    elsif ($cstartnewthreads eq "yes")        { $folderpicture = qq~<img src=$imagesurl/images/$skin/$zg_nonew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
	    elsif ($cstartnewthreads eq "all")        { $folderpicture = qq~<img src=$imagesurl/images/$skin/$kf_nonew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
	    elsif ($cstartnewthreads eq "cert")       { $folderpicture = qq~<img src=$imagesurl/images/$skin/$rz_nonew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
       	$cposts   = qq~<font color=$forumfontcolor>$cposts</b></font>~;
	$cthreads = qq~<font color=$forumfontcolor>$cthreads</b></font>~;
	$ctodayforumpost = qq~<font color=$fonthighlight>$ctodayforumpost</b></font>~;
    }
    if ($cstartnewthreads eq "no") { $folderpicture = qq~<img src=$imagesurl/images/$skin/$jh_pic border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }

    if ($clastposttime) {
        $clastposttime  = &longdateandtime("$clastposttime");
        $forumlastpost = qq~<BR>&nbsp;$clastposttime<BR>~;
    } else { $forumlastpost = qq~<BR>&nbsp;û�����ӣ������ڷ�����<BR>&nbsp;��æ��������ʱδ֪ ...~; $clastposter  = ""; }

    $topictitle = "" unless ((($cprivateforum ne "yes")||($membercode eq "ad")||($membercode eq "smo"))&&($topictitle));

    $forumbookmark = qq~<span style=CURSOR: hand onClick="window.external.AddFavorite('$boardurl/forums.cgi?forum=$cforumid', '$boardname - $cforumnameadd1')"><IMG SRC=$imagesurl/images/fav_add.gif BORDER=0 width=16 ALT="��$cforumnameadd��ӵ��ղؼ�"></span>~;
    if ($chiddenforum eq "yes") { $hiddeninfo = "��<I>(����)</I>"; } else { $hiddeninfo = ""; }

    if ($forumnamedisp eq 1) { $cforumnamelink = qq~<table width=100% cellpadding=2 cellspacing=0><tr><td width=93%>$cforumname$hiddeninfo</td><td width=12><a href=post.cgi?action=new&forum=$cforumid><img src=$imagesurl/images/$skin/fpost2.gif alt=�ڴ˷���̳���������� width=12 border=0></a></td><td width=12><a href=poll.cgi?action=new&forum=$cforumid><img src=$imagesurl/images/$skin/fpost1.gif alt=�ڴ˷���̳������ͶƱ width=12 border=0></a></td><td width=12><a href=jinghua.cgi?action=list&forum=$cforumid><img src=$imagesurl/images/$skin/fpost3.gif alt=�鿴�˷���̳�ľ������� width=12 border=0></a></td></tr><tr><td colspan=4 width=100%><img src=$imagesurl/images/forumme.gif width=9> <font color=$forumfontcolor>$cforumdescription</td></tr></table></td></tr></table>~; }
	                else { $cforumnamelink = "$cforumname$hiddeninfo<font color=$forumfontcolor><br><img src=$imagesurl/images/forumme.gif width=9> $cforumdescription</td></tr></table>"; }

    $output .= qq~<table cellpadding=6 cellspacing=0 width=$tablewidth height=24 align=center bordercolor=$tablebordercolor border=1><tr><td bgcolor=$forumcolorone align=center width=26>$folderpicture</td><td bgcolor=$forumcolortwo valign=top width=*>
<table width=100% cellpadding=1><tr><td width=1%>$cteam</td><td width=12></td><td width=*>$cforumnamelink</td><td bgcolor=$forumcolorone align=center width=90><font color=$forumfontcolor>$modout</td>
<td bgcolor=$forumcolortwo align=left width=97><table width=100% cellpadding=0 cellspacing=0><tr><td align=left><font color=$fontcolormisc2>&nbsp;���գ�<BR>&nbsp;���⣺<BR>&nbsp;�ظ���</td><td align=right>$ctodayforumpost&nbsp;<BR>$cthreads&nbsp;<BR>$cposts&nbsp;</td></tr></table></td>
<td bgcolor=$forumcolorone width=168><font color=$lastpostfontcolor>$topictitle$clastposter$forumlastpost</td><td bgcolor=$forumcolortwo align=center width=26>$forumbookmark</td></tr></table>
~;
}else{

   $cforumnameadd = $cforumname;
   $cforumnameadd1 = $cforumnameadd;
   $cforumnameadd1 =~ s/\'/\\'/g;
   $titleinfos{"$cforumname\n"} =~ s/\|/\n/isg;

   $cforumdescription =~ s/<.+?>//isg;
   $cforumname = qq~<a href=forums.cgi?forum=$cforumid$titleinfos{"$cforumname\n"} title="$cforumdescription"><font color=$fontcolormisc2>$cforumname</a>~;
   my $forumlastvisit = $lastvisitinfo{$cforumid};
   $folderpicture = qq(��);

   ($clastposttime,$threadnumber,$topictitle)=split(/\%\%\%/,$clastposttime1);

   my ($ctodayforumpost, $ctodayforumposttime) = split(/\|/,$ctodayforumpost);
   $ctodayforumpost = 0 if (($nowtime ne $ctodayforumposttime)||($ctodayforumpost eq ""));

   if (($clastposttime > $forumlastvisit)&&($inmembername ne "����")&&($action ne "resetall")) {
if (($cforumpass)||($cprivateforum eq "yes")) { $folderpicture = qq~<img src=$imagesurl/images/$skin/$bm_havenew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
   elsif ($cstartnewthreads eq "follow")     { $folderpicture = qq~<img src=$imagesurl/images/$skin/$pl_havenew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
   elsif ($cstartnewthreads eq "yes")        { $folderpicture = qq~<img src=$imagesurl/images/$skin/$zg_havenew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
   elsif ($cstartnewthreads eq "all")        { $folderpicture = qq~<img src=$imagesurl/images/$skin/$kf_havenew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
   elsif ($cstartnewthreads eq "cert")       { $folderpicture = qq~<img src=$imagesurl/images/$skin/$rz_havenew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
       $cposts   = qq~<font color=$fonthighlight><b>$cposts</b></font>~;
$cthreads = qq~<font color=$fonthighlight><b>$cthreads</b></font>~;
$ctodayforumpost = qq~<font color=$fonthighlight><b>$ctodayforumpost</b></font>~;
   } else {
      if (($cforumpass)||($cprivateforum eq "yes")) { $folderpicture = qq~<img src=$imagesurl/images/$skin/$bm_nonew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
   elsif ($cstartnewthreads eq "follow")     { $folderpicture = qq~<img src=$imagesurl/images/$skin/$pl_nonew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
   elsif ($cstartnewthreads eq "yes")        { $folderpicture = qq~<img src=$imagesurl/images/$skin/$zg_nonew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
   elsif ($cstartnewthreads eq "all")        { $folderpicture = qq~<img src=$imagesurl/images/$skin/$kf_nonew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
   elsif ($cstartnewthreads eq "cert")       { $folderpicture = qq~<img src=$imagesurl/images/$skin/$rz_nonew border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
      $cposts   = qq~<font color=$forumfontcolor>$cposts</b></font>~;
$cthreads = qq~<font color=$forumfontcolor>$cthreads</b></font>~;
$ctodayforumpost = qq~<font color=$fonthighlight>$ctodayforumpost</b></font>~;
   }
   if ($cstartnewthreads eq "no") { $folderpicture = qq~<img src=$imagesurl/images/$skin/$jh_pic border=0 style=cursor:hand onClick=javascript:O4($cforumid)>~; }
$hiddeninfo = ($chiddenforum eq "yes")?"��<I>(����)</I>":"";
$output .= qq~<table cellpadding=6 cellspacing=0 width=$tablewidth height=24 align=center bordercolor=$tablebordercolor border=1>~  if($is_in_other_mode == 0);
$output .=qq~<tr>~ if($now_display_count == 0);
$output .=qq~<td width="25%" bgcolor=$forumcolortwo><table width="100%" cellspacing="0" cellpadding="1"><tr><td colspan="3" valign="middle">$folderpicture $cforumname$hiddeninfo</td></tr><tr><td width="30%" align="left">��: $cthreads</td><td width="30%" align="left">��: $cposts</td><td width="30%" align="left">��: $ctodayforumpost</td></tr></table></td>~;
if($now_display_count == 3){
$now_display_count = -1;
$output .=qq~</tr>~;
}
$now_display_count++;
   $is_in_other_mode = 1;
}
}
if ($is_in_other_mode != 0) {
  $is_in_other_mode = 0;
if ($now_display_count > 0) {
$output .= qq~<td width="25%" bgcolor=$forumcolorone>&nbsp;</td>~ x (4-$now_display_count);
}
$output .= qq~</table>~;
}
$output.=qq~<SCRIPT>valignend()</SCRIPT><br>~;

sub getonlineno {
    open (FILE, "${lbdir}cache/forumonline.pl");
    %titleinfos = <FILE>;
    close(FILE);
}

1;
