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
require "code.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";
require "postjs.cgi";
$|++;
$thisprog = "xzb.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$hownews="100" if (($hownews eq "")||($hownews < 50));

for ('forum','membername','password','action','inpost','message','id') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$inforum       = $forum;
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inmembername  = $membername;
$inpassword    = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$currenttime   = time;
$inmembername = &stripMETA($inmembername);

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }
if ($catsbackpicinfo ne "")  { $catsbackpicinfo = "background=$imagesurl/images/$skin/$catsbackpicinfo"; }

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

    if ((!$inmembername) or ($inmembername eq "����")) {
        $inmembername = "����";
        $userregistered = "no";
        &error("��ͨ����&���¼����ʹ�ñ����ܣ�");
    }else{
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
	}
    &doonoff;  #��̳�������
    print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

    $helpurl = &helpfiles("�Ķ����");
    $helpurl = qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;

#        &moderator("$inforum");
&getoneforum("$inforum");
    if ($startnewthreads eq "onlysub") {&error("����&�Բ��������Ǵ�����̳�����������ԣ�"); }
&error("������̳&�����̳��û��Ȩ�޽�����̳��") if ($yxz ne '' && $yxz!~/,$membercode,/);
    if ($allowusers ne '') {
	&error('������̳&�㲻����������̳��') if (",$allowusers," !~ /\Q,$inmembername,\E/i);
    }

    my %Mode = (
    'new'	=>	\&newthread,
    'addnew'	=>	\&addnewthread,
    'view'	=>	\&view,
    'del'	=>	\&del,
    );

    if($Mode{$action}) {
        $Mode{$action}->();
    }
    else { &error("��ͨ����&������ȷ�ķ�ʽ���ʱ�����"); }

    &output("$boardname - ��$forumname�ڷ�С�ֱ�",\$output);

sub newthread {

    if (($privateforum eq "yes")||($xzbopen eq "no")||($startnewthreads eq "no")){
    	&error("����С�ֱ�&����̳����������С�ֱ�!");
    }

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    &whosonline("$inmembername\t$forumname\tboth\t����С�ֱ�\t") if ($privateforum ne "yes");
    &whosonline("$inmembername\t$forumname(��)\tboth\t�����µı���С�ֱ�\t") if ($privateforum eq "yes");
}
        if (($membercode eq "ad") ||($membercode eq 'smo')|| ($inmembmod eq "yes")) {
           &error("����С�ֱ�&�����̳�����ò���,лл������");
        }

    &mischeader("����С�ֱ�");
if (($xzbcost ne "")&&($xzbcost >= 0)) {
    $xzbcost = qq~<B>������ $xzbcost $moneyname��</B>~;
}

   $startthreads = "�κ�ע���Ա(�����������ϳ���)������������$xzbcost";

    	$output .= qq~
                <form action="$thisprog" method=post name="FORM" >
                <input type=hidden name="action" value="addnew">
                <input type=hidden name="forum" value="$inforum">
                <SCRIPT>valigntop()</SCRIPT>
        	<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            	<tr><td>
                <table cellpadding=6 cellspacing=1 width=100%>
                <tr>
                    <td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor><b>˭��������С�ֱ���</b> $startthreads</td>
                </tr>
                <tr>
                    <td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> �����Ҫ�������û���ݷ����������������û��������롣�������ı��û���ݣ������ա�</td>
                </tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td>
            <td bgcolor=$miscbackone>��<input type=text name="membername"></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td>
            <td bgcolor=$miscbackone>��<input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
		<tr>
		<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>С�ֱ�����(��� 80 ��)</b></td>
		<td bgcolor=$miscbackone>
		��<input type="text" maxlength="80" name=inpost onkeydown=ctlent() value="$inpost" size=80><br>

		</td></tr>
		<tr>
		<td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>С�ֱ�����</b> (��� $hownews ��)<p>
		 �ڴ���̳�У�<li>HTML ��ǩ: <b>������</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS ��ǩ</a>: <b>����</b>
		</td>
		<td bgcolor=$miscbacktwo valign=top>
		<b>����ÿСʱһ����һ�����������������48Сʱ</b><br>��
		<TEXTAREA cols=58 name=message rows=6 wrap=soft onkeydown=ctlent()>$message</TEXTAREA>
		</td>
		</tr>
		<tr>
                <td bgcolor=$miscbacktwo colspan=2 align=center>
                <input type=Submit value="�� ��" name=Submit"  onClick="return clckcntr();">������<input type="reset" name="Clear" value="�� ��">
                </td></form></tr>
            </table>
        </tr></td></table>
     <SCRIPT>valignend()</SCRIPT>
        ~;
}

sub addnewthread {

if (($xzbcost ne "")&&($xzbcost >= 0)) {
    $mymoney2 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
    if ($mymoney2 < $xzbcost) {
        &error ("����С�ֱ�&�Բ������Ǯ������������Ӧ�� $xzbcost $moneyname��");
    }
}
    if    ($userregistered eq "no")     { &error("����С�ֱ�&��û��ע�ᣡ"); }
    elsif ($inpassword ne $password)    { &error("����С�ֱ�&�����������"); }
    elsif (($membercode eq "banned")||($membercode eq "masked"))     { &error("����С�ֱ�&������ֹ���ԣ�"); }
    elsif ($inpost eq "")               { &error("����С�ֱ�&����������⣡"); }
    elsif (length($inpost) > 82)        { &error("������ͶƱ&���������"); }
    else  {
        if (($privateforum eq "yes")||($xzbopen eq "no")||($startnewthreads eq "no")||($startnewthreads eq "cert")){
    	    &error("����С�ֱ�&����̳����������С�ֱ�!");
    	}

        $dirtoopen = "$lbdir" . "boarddata";
        open (DIR, "<$dirtoopen/xzb$inforum.cgi");
        @xzbdata = <DIR>;
        close (DIR);
        chomp(@xzbdata);
        $sizexzb=@xzbdata;
        $currenttime = time;
        if (($membercode eq "ad") ||($membercode eq 'smo')|| ($inmembmod eq "yes")) {
           &error("����С�ֱ�&�����̳�����ò���,лл������");
        }

	($tmp, $tmp,$tmp,$tmp,$lastpost)=split(/\t/,$xzbdata[0]);
	$lastpost = ($lastpost + 3600);

	if ($lastpost > $currenttime)  {
           &error("����С�ֱ�&���Сʱ�Ѿ����˷����һ��С�ֱ��ˣ����һ��Сʱ������");
	}

        $inpost=~s/</&lt;/sg;
        $inpost=~s/>/&gt;/sg;
	my $temp = &dofilter("$inpost\t$message");
	($inpost,$message) = split(/\t/,$temp);

        $sizexzb=48 if ($sizexzb >48);
        $write="����������\t$inpost\t$inmembername\t$message\t$currenttime\t";
        @newxzb=($write,@xzbdata);
        open(DIR,">$dirtoopen/xzb$inforum.cgi");
        for ($i=0;$i<=$sizexzb;$i++){
             	print DIR "$newxzb[$i]\n";
        }

        &mischeader("��С�ֱ������ɹ�");

        $relocurl = "forums.cgi?forum=$inforum";

if (($xzbcost ne "")&&($xzbcost >= 0)) {
        $cleanmembername = $inmembername;
        $cleanmembername =~ s/ /\_/isg;
        $cleanmembername =~ tr/A-Z/a-z/;

        $cleanmembername = &stripMETA($cleanmembername);
        $cleanmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
        
	my $namenumber = &getnamenumber($cleanmembername);
	&checkmemfile($cleanmembername,$namenumber);
        $filetomake = "$lbdir" . "$memdir/$namenumber/$cleanmembername.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
	open (fh, "$filetomake");
	flock (fh, 1) if ($OS_USED eq "Unix");
        $filedata = <fh>;
        close (fh);
        chomp $filedata;
        (my $membername, my $password, my $membertitle, my $membercode, my $numberofposts, my $emailaddress, my $showemail, my $ipaddress, my $homepage, my $oicqnumber, my $icqnumber ,my $location ,my $interests, my $joineddate, my $lastpostdate, my $signature, my $timedifference, my $privateforums, my $useravatar, my $userflag,my  $userstar, my $usersx, my $personalavatar, my $personalwidth, my $personalheight, my $rating, my $lastgone, my $visitno,my  $useradd04,my  $useradd02, my $mymoney, my $postdel, my $sex, my $education, my $marry, my $work, my $born, my $chatlevel,my  $chattime, my $jhmp,my $jhcount,my $ebankdata,my $onlinetime,my $awards,my $jifen,my $userface, my $soccerdata, my $useradd5) = split(/\t/,$filedata);
        $mymoney -= $xzbcost;

        if ($password ne "") {
            if (open (fh, ">${lbdir}$memdir/$namenumber/$cleanmembername.cgi")) {
		flock (fh, 2) if ($OS_USED eq "Unix");
                print fh "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userstar\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
                close (fh);
            }
        }
        &winunlock($filetomake) if ($OS_USED eq "Nt");
}

        $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>лл��������С�ֱ��Ѿ������ɹ���</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ��������û���Զ����أ�������������ӣ�
            <ul>
            <li><a href="forums.cgi?forum=$inforum">������̳</a>
            <li><a href="leobbs.cgi">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;

    }
}



sub view {
&error("�ϴ������ҵĳ���!") if (($id eq "")||($inforum eq ""));
	$dirtoopen = "$lbdir" . "boarddata";
	open (DIR, "<$dirtoopen/xzb$inforum.cgi");
        @xzbdata = <DIR>;
        close (DIR);
        chomp(@xzbdata);
        $xzbdata[$id] =~ s/^����������\t//isg;
        ($title,$postid,$msg,$posttime)=split(/\t/,$xzbdata[$id]);
my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
        &whosonline("$inmembername\t$forumname\tboth\t�Ķ�С�ֱ�\t") if ($privateforum ne "yes");
        &whosonline("$inmembername\t$forumname(��)\tboth\t�Ķ�����С�ֱ�\t") if ($privateforum eq "yes");
}

	$dateposted = $posttime + ($timedifferencevalue*3600) + ($timezone*3600);
        $dateposted = &dateformat("$dateposted");
        &lbcode(\$msg);
       $admindelete=qq~
       <a href=xzb.cgi?action=del&forum=$inforum&id=$id OnClick="return confirm('ȷ��ɾ�����С�ֱ�ô��');">ɾ��</a>
       ~;
	$output=qq~<P><SCRIPT>valigntop()</SCRIPT>
	<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=#000000 align=center>
	                <tr>
	                    <td>
	                    <table cellpadding=3 cellspacing=1 width=100% style="TABLE-LAYOUT: fixed">
	~;




	$output .= qq~
	                  <tr>
	                  <td bgcolor=$titlecolor align=center valign=top $catbackpic><font face="$font" color=$titlefontcolor><b>>> $title <<</b></td></tr>
		    ~;
		    if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")||($postid eq "$inmembername")) {
			  $output .= qq~
	                      	<tr>
	                      	    <td bgcolor=$postcolortwo align=right>$admindelete</td>
	                       	</tr>
			  ~;
		    }

       $output .= qq~
	                 <tr>
	                    <td bgcolor="$postcolortwo" valign=top style="LEFT: 0px; WIDTH: 100%; WORD-WRAP: break-word"><font face="$font" color=$postfontcolortwo>
	                        $msg
	                    </td>
	                 </tr>
	                 <tr>
	                    <td bgcolor="$postcolortwo" valign=middle>
	                     <table width=100% border="0" cellpadding="0" cellspacing="0">
	                        <tr><td align=left>&nbsp;&nbsp;&nbsp;<font face="$font" color=$postfontcolortwo><b>������</b>�� $postid</font>
	                        </td><td align=right><font face="$font" color=$postfontcolortwo><b>����ʱ��</b>�� $dateposted</font>&nbsp;&nbsp;&nbsp;
	                        </tr>
	                        </table>
	                        </td>
	                        </font>
	                        </tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>

	              ~;
	             print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output("$boardname - ��$forumname�ڲ鿴С�ֱ�",\$output);

exit;
}

sub del {
	&error("�ϴ������ҵĳ���!") if (($id eq "")||($inforum eq ""));
	$dirtoopen = "$lbdir" . "boarddata";
	open (DIR, "<$dirtoopen/xzb$inforum.cgi");
        @xzbdata = <DIR>;
        $sizexzb=@xzbdata;
        close (DIR);
        chomp(@xzbdata);
        ($nouse, $title,$postid,$msg,$posttime)=split(/\t/,$xzbdata[$id]);
         if (($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes")&&($postid ne "$inmembername")) {
        &error("ɾ��С�ֱ�&��ûȨ��ɾ��!");
}

        open (DIR, ">$dirtoopen/xzb$inforum.cgi");
        for ($i=0;$i<$sizexzb;$i++){
        	if ($i ne $id){
             	print DIR "$xzbdata[$i]\n";

             	}
        }
        close (DIR);

	$output=qq~
	<script>alert("С�ֱ�ɾ���ɹ���");top.window.close();</script>
	~;
	             print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
	             print $output;

exit;
}
