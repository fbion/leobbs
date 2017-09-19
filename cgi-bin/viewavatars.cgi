#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

BEGIN {
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use LBCGI;
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$bgcolor = "white"; # ������ɫ
$interval = 10;   #һ�м���ͼ��
$linesperpage = 8; #һҳ����

########### No need to edit below this line ###################
$thisprog = "viewavatars.cgi";

$perpage = $interval * $linesperpage;
$query = new LBCGI;

$startimage  = $query -> param ("startimage");
$endimage    = $query -> param ("endimage");
$inpage      = $query -> param ("page");

if (($startimage < 0) || ($startimage eq "") || ($endimage <= 0) || ($endimage < $startimage)) {
 $startimage = 0;
 $endimage = $perpage - 1;
}
if ($inpage eq "") { $inpage = 1; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

$inmembername   = cookie("amembernamecookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

if ((!$inmembername) or ($inmembername eq "����")) {
  $inmembername = "����";
} else {
#  &getmember("$inmembername");
    &getmember("$inmembername","no");
  &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
}
$defaultwidth  = "width=$defaultwidth"   if ($defaultwidth ne "" );
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");


$count = 0;

$dirtoopen = "$imagesdir" . "avatars";
opendir (DIR, "$dirtoopen");
@dirdata = readdir(DIR);
closedir (DIR);

@images = grep(/\.gif$/i,@dirdata);

foreach $image (@images) {
  if ($membercode ne 'ad') {
    if ($image =~ /admin\_/ig) {
      next;
    }
  }
  if ($image =~ /noavatar/ig) {
    next;
  } else {
    push (@cleanimages, $image);
  }
}

$totalimages = @cleanimages - 1;

if ($endimage > $totalimages) { $endimage = $totalimages; }

@imagestoshow = @cleanimages[$startimage..$endimage];

$numimages = $endimage - $startimage;
$shownimages = 0;

foreach (@imagestoshow) {
  $avatar =  $_;
  $avatar =~ s/.gif//i;
  $avatarout .= qq~<td align="center" valign="center"><img src="$imagesurl/avatars/$avatar.gif" alt="$avatar" $defaultwidth $defaultheight><br>$avatar</td>\n~;
  $count++;
  $shownimages++;

  if (($count eq $interval) && ($shownimages <= $numimages)) {
    $count = 0;
    $countdown++;
    $avatarout .= qq~</tr><tr bgcolor="$bgcolor">\n~;
  }
}


print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&title;

$output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> �����������Բ鿴����վ���е�ͷ��</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> �� <a href="viewavatars.cgi">�û�ͷ���б�</a> �� �鿴�б�<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>

~;

$output .= qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellPadding=6 cellSpacing=1 border=0 width=100%>
<tr bgcolor="$bgcolor">
$avatarout~;

for($count; $count < $interval; $count++) {
     $output .= qq~<td>&nbsp;</td>~;
}

&splitpages;

$output .= qq~
</tr><tr><td colspan=$interval bgcolor="$bgcolor" align=center>
<center><font color=$fontcolormisc>$pagelinks</font></td></tr>
</table></td></tr>
</table><SCRIPT>valignend()</SCRIPT>
~;

&output("$boardname - �û�ͷ���б�",\$output);

sub splitpages {
 $totalpages = @cleanimages / $perpage;
 ($pagenumbers, $decimal) = split (/\./, $totalpages);
 if ($decimal > 0) { $pagenumbers++; }

 $page = 1;
 $start = 0;
 $end = $perpage - 1;
 $pagedigit = 0;

 while ($pagenumbers > $pagedigit) {
   $pagedigit++;
   if ($inpage ne $page) {
     $pagelinks .= qq~[<a href="$thisprog?startimage=$start&endimage=$end&page=$page">��$pagedigitҳ</a>] ~;
   }
   else { $pagelinks .= qq~[<B>��$pagedigitҳ</B>] ~; }
   $start += $perpage;
   $end += $perpage;
   $page++;
 }
 $page--;
 $pagelinks = qq~���б���$pageҳ��$pagelinks~;

 if ($totalpages <= 1) { 
  $pagelinks = qq~�û�ͷ���б�ֻ��һҳ.~; 
 }
}
