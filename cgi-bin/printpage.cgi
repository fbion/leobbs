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
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
use VISITFORUM qw(getlastvisit setlastvisit);
require "code.cgi";
require "data/boardinfo.cgi";
require "data/cityinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "printpage.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

&ipbanned; #��ɱһЩ ip

$inforum        = $query -> param('forum');
$intopic        = $query -> param('topic');

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "����" ) {
    $inmembername = "����";
    $myrating = -1;
	    if ($regaccess eq "on" && &checksearchbot) {
	    	print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
	    	print "<script language='javascript'>document.location = 'loginout.cgi?forum=$inforum'</script>";
	    	exit;
	    }
    &error("��ͨ����&���˲��ܲ鿴�������ݣ���ע����¼������") if ($guestregistered eq "off");
}
else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    $mymembercode=$membercode;
    $myrating=$rating;
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
#&getoneforum("$inforum");
#    &moderator("$inforum");
$myinmembmod = $inmembmod;
        &getlastvisit;
        $forumlastvisit = $lastvisitinfo{$inforum};
        $currenttime = time;
        &setlastvisit("$inforum,$currenttime");
    }
    &getoneforum("$inforum");
&doonoff;  #��̳�������

if ($privateforum eq "yes"){
    if ($inmembername eq "����") {
	print "<script language='javascript'>document.location = 'loginout.cgi?forum=$inforum'</script>";
	exit;
    }
    if (($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; } else { $allowed = "no"; }
}

&error("������̳&�����̳��û��Ȩ�޽�����̳��") if ($yxz ne '' && $yxz!~/,$membercode,/);
if ($allowusers ne ''){
    &error('������̳&�㲻����������̳��') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}

if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &error("������̳&�㲻����������̳���������Ϊ $rating��������ֻ̳���������ڵ��� $enterminweiwang �Ĳ��ܽ��룡") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0 ) {
	require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
	$mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	&error("������̳&�㲻����������̳����Ľ�ǮΪ $mymoney1��������ֻ̳�н�Ǯ���ڵ��� $enterminmony �Ĳ��ܽ��룡") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
	&error("������̳&�㲻����������̳����Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $enterminjf �Ĳ��ܽ��룡") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @threads = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    
    ($no, $topictitle, $no, $no, $no ,$startedpostdate, $no) = split(/\t/, @threads[0]);
    $topictitle =~ s/^����������//;

	if ($addtopictime eq "yes") {
	    my $topictime = &dispdate($startedpostdate + ($timedifferencevalue*3600) + ($timezone*3600));
	    $topictitle = "[$topictime] $topictitle";
	}

if (($startnewthreads eq "cert")&&(($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $membercode !~ /^rz/)||($inmembername eq "����"))&&($userincert eq "no")) { &error("������̳&��һ���Ա������������̳��"); }

    if (($privateforum eq "yes") && ($allowed ne "yes")) {
        &error("����˽����̳&�Բ�������Ȩ���������̳��");
    }
    else {
      my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
      $filetoopens = &lockfilename($filetoopens);
      if (!(-e "$filetoopens.lck")) {
        if ($privateforum ne "yes") {
            &whosonline("$inmembername\t$forumname\tboth\t���<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>(�ı���ʽ)\t");
        }
        else {
            &whosonline("$inmembername\t$forumname(��)\tboth\t�����������(�ı���ʽ)\t");
        }
      }
    }
if($category=~/childforum-[0-9]+/){
$tempforumno=$category;
$tempforumno=~s/childforum-//;
    $filetoopen = "${lbdir}forum$tempforumno/foruminfo.cgi";
    open(FILE, "$filetoopen");
    $forums = <FILE>;
    close(FILE);
    (undef, undef, undef, $tempforumname, undef) = split(/\t/,$forums);
    $addlink=qq~\n            <b>-- $tempforumname</b> ($boardurl/forums.cgi?forum=$tempforumno)<br>~;
    $addspace="-";
}

    $output .= qq~
    <html><head><title>$topictitle - $boardname</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}

	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}

		.t     {	LINE-HEIGHT: 1.4			}
		BODY   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: ����; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: ����; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: ����; FONT-SIZE: 9pt	}
	</style>
    </head>
    <body topmargin=10 leftmargin=0 onload="window.print()">
    <table cellpadding=0 cellspacing=0 width=90% align=center>
        <tr>
            <td>
            <p><b>���ı���ʽ�鿴����</b><p>
            <b>- $boardname</b> ($boardurl/leobbs.cgi)<br>$addlink
            <b>$addspace-- $forumname</b> ($boardurl/forums.cgi?forum=$inforum)<br>
            <b>$addspace--- $topictitle</b> ($boardurl/topic.cgi?forum=$inforum&topic=$intopic)
        </tr>
    </table>
    <p><p><p>
    <table cellpadding=0 cellspacing=0 width=90% align=center>
      <tr><td>
    ~;

if ($mymembercode eq "ad" or $mymembercode eq "smo" or $myinmembmod eq "yes") {
    $viewhide = 1;
}
else {
    $viewhide = 0;
    if ($hidejf eq "yes" ) { 
	my @viewhide=grep(/^$inmembername\t/i,@threads);
	$viewhide=@viewhide;
	$viewhide=1 if($viewhide >= 1);
    }
}
$StartCheck=$numberofposts+$numberofreplys;

$rn = 1;
    foreach $line (@threads) {
        ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post) = split(/\t/,$line);
        if ($rn eq 1) {
            &getmember("$membername","no");
            if ($membercode eq "masked") {
    	        $addme = "";
                $post = qq(<br>------------------------<br><font color=$posternamecolor>���û��ķ����Ѿ������Σ�<br>�������ʣ�����ϵ����Ա��</font><br>------------------------<BR>);
            }
	}
#        $post = "(��)" if ($post=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg);
#        $post =~ s/(\[hide\])(.+?)(\[\/hide\])/(�����������Ѿ�����)/isg;
#        $post =~s/\[post=(.+?)\](.+?)\[\/post\]/(�������ѱ�����)/isg; 

    if ($wwjf ne "no") {
	if ($post=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg) {
    	    if ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($myinmembmod eq "yes")|| ($myrating >= $1) ){
	    }else{
		$post=qq~<FONT COLOR=$fonthighlight><B>[Hidden Post: Rating $1]</B></FONT> <BR>  <BR> <FONT COLOR=$posternamecolor>����û��Ȩ�޿�������ӣ���������������Ҫ <B>$1<\/B>��</FONT><BR>  <BR> ~;
		$addme="��������!<br>";
	    }
	    $post=~s/LBHIDDEN\[(.*?)\]LBHIDDEN/<font color=$fonthighlight>������ֻ���������ڵ��� <B>$1<\/B> �Ĳ��ܲ鿴��<\/font><br>/sg;   
	}
    }
    else { $post=~s/LBHIDDEN\[(.*?)\]LBHIDDEN//; }

    $post  =~ s/\[ALIPAYE\](.*)\[ALIPAYE\]//isg; 

    if ($cansale ne "no") {
	if ($post=~/LBSALE\[(.*?)\]LBSALE/sg) {
    	    my $postno = $rn -1;
            my $isbuyer = "";
            my $allbuyer = "";
            my $allbuyerno = "";
            undef @allbuyer;
            if (open(FILE, "${lbdir}$saledir/$inforum\_$intopic\_$postno.cgi")) {
                my $allbuyer = <FILE>;
                close(FILE);
                chomp $allbuyer;
		$allbuyer =~ s/\t\t/\t/isg;
                $allbuyer =~ s/\t$//gi;
                $allbuyer =~ s/^\t//gi;
		@allbuyer = split(/\t/, $allbuyer);
		$allbuyerno = @allbuyer;
	        $allbuyer = "\t$allbuyer\t";
		$isbuyer="yes" if ($allbuyer =~ /\t$inmembername\t/i);
            }
            $allbuyerno = 0 if (($allbuyerno < 0)||($allbuyerno eq ""));
            unless ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad")||($mymembercode eq 'smo')||($mymembercode eq 'mo')||($mymembercode eq 'amo')||($myinmembmod eq "yes")||($isbuyer eq "yes")) {
                $post=qq~<FONT COLOR=$fonthighlight><B>[Sale Post: Money $1]</B></FONT><BR>  <BR><FONT COLOR=$posternamecolor>[�鿴���������Ҫ <b>$1</b> $moneyname��Ŀǰ���� <B>$allbuyerno</B> �˹���]</FONT><BR><br><FORM action=buypost.cgi method=post><input name=inforum type=hidden value=$inforum><input name=intopic type=hidden value=$intopic><input name=postnumber type=hidden value=$postno><input name=salemembername type=hidden value="$membername"><input name=moneynumber type=hidden value=$1><INPUT name=B1 type=submit value="����ݡ��������Ҹ�Ǯ"></form><BR> ~;
                $addme="��������!<br>";
	    }
	    else {
	    	$buyeroutput = "";
	    	if ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad")||($mymembercode eq 'smo')||($mymembercode eq 'mo')||($mymembercode eq 'amo')||($myinmembmod eq "yes")) {
                    if ($allbuyerno > 0 ) {
	                $buyeroutput = qq~<SCRIPT LANGUAGE="JavaScript">
function surfto(list) { var myindex1  = list.selectedIndex; if (myindex1 != 0 & myindex1 != 1) { var newwindow = list.options[myindex1].value; var msgwindow = window.open(newwindow,"",""); }}
</SCRIPT><form action="profile.cgi" method=post name="modjump"><img src=$imagesurl/images/team2.gif width=19 height=19 align=absmiddle>
<input type=hidden name=action value=show><select onchange="surfto(this)">
<option>����������</option><option>------------</option>
~;
	                foreach (@allbuyer) {
	                    chomp $_;
	                    next if ($_ eq "");
	                    my $cleanedmodname = $_;
	                    $cleanedmodname =~ s/ /\_/g;
	                    $cleanedmodname =~ tr/A-Z/a-z/;
    	                    $buyeroutput .= qq~<option value="profile.cgi?action=show&member=$cleanedmodname">$_</option>~;
	                }
	                $buyeroutput .= qq~</select><BR>\n~;
                    }
                }
	        $post=~s/LBSALE\[(.*?)\]LBSALE/$buyeroutput<font color=$fonthighlight>�������ۼ� <B>$1<\/B> $moneyname��Ŀǰ���� <B>$allbuyerno<\/B> �˹���<\/font><br><br>/sg;   
	    }
	}
    }
    else { $post=~s/LBSALE\[(.*?)\]LBSALE//; }

    if ($hidejf eq "yes" ) {
      if ($post =~m/(\[hide\])(.*)(\[\/hide\])/isg){ 
        if ($viewhide ne "1") { 
            $post =~ s/(\[hide\])(.*)(\[\/hide\])/<blockquote><font color=$posternamecolor>���أ� <hr noshade size=1><font color=$fonthighlight>�����������Ѿ����أ�����ظ��󣬲��ܲ鿴<\/font><hr noshade size=1><\/blockquote><\/font><\/blockquote>/isg;
            $addme="��������!<br><br>" if (($addme)&&($1 eq "[hide]"));
	} 
        else { 
            $post =~ s/\[hide\](.*)\[hide\](.*)\[\/quote](.*)\[\/hide\]/<blockquote><font color=$posternamecolor>���أ� <hr noshade>$1<blockquote><hr noshade size=1>$2<hr noshade size=1><\/blockquote>$3<\/font><hr noshade><\/blockquote>/isg; 
     	    $post =~ s/\[hide\]\s*(.*?)\s*\[\/hide\]/<blockquote><font color=$posternamecolor>���أ� <hr noshade size=1>$1<hr noshade size=1><\/blockquote><\/font>/isg; 
  	}
      }
    }

    if ($postjf eq "yes") {
	if ($post =~m/\[post=(\d+?)\](.+?)\[\/post\]/isg){ 
	    $viewusepost=$1; 
	    if ($StartCheck >= $viewusepost) { $Checkpost='ok'; } else { $Checkpost='not'; }

	    if(($Checkpost eq 'ok')||($mymembercode eq "ad")||($mymembercode eq "smo")||($myinmembmod eq "yes")||($membername eq $inmembername)){ 
	   	$post =~s/\[post=(\d+?)\](.+?)\[\/post\]/<blockquote><font color=$posternamecolor>�������ݣ��������������� <B>$viewusepost<\/B> ���ܲ鿴������ <hr noshade size=1>$2<hr noshade size=1><\/font><\/blockquote>/isg; 
	    }else{ 
   		$post =~s/(\[post=(\d+?)\])(.*)(\[\/post\])/<blockquote><font color=$posternamecolor>�������ݣ� <hr noshade size=1><font color=$fonthighlight>�������ѱ����� , ������������ <B>$viewusepost<\/B> ���ܲ鿴<\/font><hr noshade size=1><\/font><\/blockquote>/isg; 
                $addme="��������!<br><br>" if (($addme)&&($1 =~ m/^\[post/));
   	    }
   	}
    }


    if ($jfmark eq "yes") {
	if ($post =~m/\[jf=(\d+?)\](.+?)\[\/jf\]/isg){ 
	    $jfpost=$1; 

	    if (($jfpost <= $jifen)||($mymembercode eq "ad")||($mymembercode eq "smo")||($myinmembmod eq "yes")||(lc($membername) eq lc($inmembername))){ 
	   	$post =~s/\[jf=(\d+?)\](.*)\[\/jf\]/<blockquote><font color=$posternamecolor>�������ݣ������ֱ���ﵽ <B>$jfpost<\/B> ���ܲ鿴�����ݣ� <hr noshade size=1>$2<hr noshade size=1><\/font><\/blockquote>/isg; 
	    } else { 
	        &error("������&���ֱ���ﵽ $jfpost ���ܲ鿴����Ŀǰ�Ļ����� $jifen ��") if (($editpostnumber eq "1")&&($noviewjf eq "yes"));
   		$post =~s/(\[jf=(\d+?)\])(.*)(\[\/jf\])/<blockquote><font color=$posternamecolor>�������ݣ� <hr noshade size=1><font color=$fonthighlight>�������ѱ����� , ���ֱ���ﵽ <B>$jfpost<\/B> ���ܲ鿴<\/font><hr noshade size=1><\/font><\/blockquote>/isg;
                $addme="��������!<br><br>" if (($addme)&&($1 =~ m/^\[jf/));
   	    }
   	}
    }


#       	&lbcode(\$post);
	$post =~ s/\[USECHGFONTE\]//sg;
	$post =~ s/\[DISABLELBCODE\]//sg;
    $post =~ s/\[ADMINOPE=(.+?)\]//isg;

    if ($post =~ /\[POSTISDELETE=(.+?)\]/) {
    	if ($1 ne " ") { $presult = "<BR>�������ɣ�$1<BR>"; } else { $presult = "<BR>"; }
        $post = qq(<br>--------------------------<br><font color=$posternamecolor>�����������Ѿ����������Σ�$presult�������ʣ�����ϵ����Ա��</font><br>--------------------------<BR>);
    }

        $postdate = &dateformat($postdate + ($timedifferencevalue*3600) + ($timezone*3600));
$post =~ s/\[watermark\](.+?)\[\/watermark\]/<font color=red>��ˮӡ���ݲ��ܴ�ӡ<\/font>/isg;
$post =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\[��������\]/isg if ($usecurl ne "no");

        $output .= qq~
        <p>
        <hr><p>
        -- ���ߣ� $membername<BR>
        -- ����ʱ�䣺 $postdate<p>
        $post
        <p><p>
        ~;
        $rn ++;
    }
    my $boardcopyright = qq(&copy\; $copyrightinfo) if $copyrightinfo;

   $boardcopyright =~ s/&lt;/</g; $boardcopyright =~ s/&gt;/>/g; $boardcopyright =~ s/&quot;/\"/g;

    $output .= qq~
        </td></tr></table><center><hr width=90%><font color=$fontcolormisc>
           $boardcopyright�� �汾�� $versionnumber
           </font></center>
        </body></html>
    ~;
    print $output;
    exit;
