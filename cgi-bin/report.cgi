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

$thisprog = "report.cgi";

$query = new LBCGI;

&ipbanned; #��ɱһЩ ip

$inforum       = $query -> param('forum');
$intopic       = $query -> param('topic');
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$action          = $query -> param('action');

$insubject       = $query -> param('subject');
$inemailmessage  = $query -> param('emailmessage');
$emailtopictitle = $query -> param('emailtopictitle');
$intouser        = $query -> param('touser');
$inmembername    = $query -> param('membername');
$inpassword      = $query -> param('password');
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$inmsgtitle	 = $query -> param('subject');
$inmessage	 = $query -> param('emailmessage');
$inoriginalpost  = $query -> param('originalpost');
$inpost2 = "<BR><BR><b>����ԭʼλ�ã�</b> $boardurl/topic.cgi?forum=$inforum&topic=$intopic<br>";

$insubject           = &cleaninput($insubject);
$inemailmessage      = &cleaninput($inemailmessage);
$emailtopictitle     = &cleaninput($emailtopictitle);
$inforum             = &cleaninput($inforum);
$inoriginalpost      = &cleaninput($inoriginalpost);

$inmembername        = &cleaninput($inmembername);
$inpassword          = &cleaninput($inpassword);
$inpostno      	     = $query -> param('postno');

$inmessage2 = $inemailmessage.$inoriginalpost.$inpost2;

# new
$add_user2	= $query -> param('touser1');
# -- new

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&error("����Ϣ��ֹʹ��&�ܱ�Ǹ��̳������ĳ��ԭ���ѽ�ֹ�����û�ʹ�ö���Ϣ����") if ($allowusemsg eq "off");
&error("��̳�Ѿ��ر�&�ܱ�Ǹ��������̳��ʱ�رգ����Ժ�����ʹ�ö���Ϣ��лл������") if (($mainoff == 1)||($mainonoff == 1));
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "����" ) {
        $inmembername = "����";
        $userregistered = "no";
        }
        else {
#			&getmember("$inmembername");
		        &getmember("$inmembername","no");
			&error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
			if ($inpassword ne $password) { &error("���ͱ���&������������⣡"); }
            }

&title;

$output .= qq~<BR>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> �����������԰�����������ӷ��͸�������Ա����</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a>  �� ���������������<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>
        <td>
        <table cellpadding=6 cellspacing=1 width=100%>
        ~;

if ($action eq "send") {


#	&getmember("$inmembername");
	if ($userregistered eq "no") { &error("���ͱ���&�㻹ûע���أ�"); }
	elsif ($inpassword ne $password) { &error("���ͱ���&������������⣡"); }
	elsif ($inmembername eq "") { &login("$thisprog?action=reply&touser=$intouser"); }

	# Check for blanks

	if ($inmsgtitle eq "") { $blanks = "yes"; }
	if ($inmessage eq "")  { $blanks = "yes"; }
	if ($intouser eq "")   { $blanks = "yes"; }

	if ($blanks eq "yes") { &error("���ͱ���&��������д������Ҫ��©��"); }

		    $memberfilename = $intouser;
		    $memberfilename =~ s/ /\_/g;
		    $memberfilename =~ tr/A-Z/a-z/;
		    $currenttime = time;
	my $messfilename = "${lbdir}${msgdir}/main/${memberfilename}_mian.cgi";
	&error("�������Ͷ���Ϣ&�Է������˶���Ϣ����ţ��޷����ͣ�<br>") if (-e $messfilename);

#	            &getmember("$memberfilename");
		    &getmember("$memberfilename","no");
        	    if ($userregistered eq "no") {&error("���ͱ���&������������⣬�����һ�����ͱ��棡");}

		    $filetoopen = "$lbdir". "$msgdir/in/$memberfilename" . "_msg.cgi";
		    open (FILE, "$filetoopen");
		    @inboxmessages = <FILE>;
		    close (FILE);

		    open (FILE, ">$filetoopen");
	    	    flock (FILE, 2) if ($OS_USED eq "Unix");
		    print FILE "����������$inmembername\tno\t$currenttime\t$inmsgtitle\t$inmessage2\n";
		    foreach $line (@inboxmessages) {
			chomp $line;
			print FILE "$line\n";
			}
		    close (FILE);

        if ($refreshurl == 1) {
	        $relocurl = "topic.cgi?forum=$inforum&topic=$intopic";
	}
	else {
               	$relocurl = "forums.cgi?forum=$inforum";
        }

            $output .= qq~
            <tr>
                <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>лл��$inmembername���Ѿ��ɹ������淢�͸�������</b></td>
            </tr>

            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            ��������û���Զ����أ�������������ӣ�
            <ul>
            <li><a href="topic.cgi?forum=$inforum&topic=$intopic">��������</a>
            <li><a href="forums.cgi?forum=$inforum">������̳</a>
            <li><a href="leobbs.cgi">������̳��ҳ</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table><SCRIPT>valignend()</SCRIPT>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;


    } # end action

else {

   $filetoopen = "$lbdir" . "forum$inforum/foruminfo.cgi";
   open(FILE, "$filetoopen");
   $forums = <FILE>;
   close(FILE);
   ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forums);

$filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    open(FILE, "$filetoopen");
    flock(FILE, 2);
    $threads = <FILE>;
    close(FILE);
    chomp $threads;
($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon) = split(/\t/, $threads);
$topictitle =~ s/^����������//;

    $post =~ s/\<p\>/\n\n/g;
    $post =~ s/\<br\>/\n/g;

    $postdate = $postdate + ($timedifferencevalue*3600) + ($timezone*3600);
    $postdate = &dateformat("$postdate");

 $rawpost = $post;
	$rawpost =~ s/\[USECHGFONTE\]//sg;
	$rawpost =~ s/\[DISABLELBCODE\]//sg;
	$rawpost =~ s/\[ADMINOPE=(.+?)\]//isg;
        $rawpost  =~ s/\[ALIPAYE\](.*)\[ALIPAYE\]//isg; 

    if ($rawpost =~ /\[POSTISDELETE=(.+?)\]/) {
    	if ($1 ne " ") { $presult = "<BR>�������ɣ�$1<BR>"; } else { $presult = "<BR>"; }
        $rawpost = qq(<br>--------------------------<br><font color=$posternamecolor>�����������Ѿ����������Σ�$presult�������ʣ�����ϵ����Ա��</font><br>--------------------------<BR>);
    }

    $temppost = qq~ԭʼ������ $membername �� $postdate �������������£�\[br\]$rawpost~;


### print form
if ($forummoderator eq "") {
&error("���ͱ���&�����û�����ð�����"); }
else {
$recipient = $forummoderator }

@recipientname = split(",",$recipient);

$toto = qq~<select name="touser">~;
foreach (@recipientname) {
    $toto .= qq~<option value="$_">$_</option>~;
}
$toto .= qq~</select>~;
&getoneforum("$inforum");

&error("���ͱ���&����ǰ�������ʲô�ɻ���") if (($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"));

    $topictitle = &cleanarea("$topictitle");

    $output .= qq~
    <form action="$thisprog" method=post>
    <input type=hidden name="action" value="send">
    <input type=hidden name="forum" value="$inforum">
    <input type=hidden name="topic" value="$intopic">
    <input type=hidden size=40 name="subject" value="��������������ӣ� $topictitle">
	<tr>
    		<td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center>
			<font color=$fontcolormisc><b>�����Ա���������������</b></font>
		</td>
	</tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
	<tr>
                <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc><b>���淢�͸��ĸ�����</b></font>
		</td>
                <td bgcolor=$miscbackone valign=middle>$toto
		</td>
	</tr>
	<tr>
    		<td bgcolor=$miscbackone>
		<font color=$fontcolormisc><b>����ԭ��</b><br>����������������Ƿ����ȡ�����<BR>�Ǳ�Ҫ����²�Ҫʹ������ܣ�
		</td>
    		<td bgcolor=$miscbackone><textarea name="emailmessage" cols="55" rows="6">
����Ա�����ã���������ԭ�������㱨��������������ӣ�

</textarea><input type=hidden name="originalpost" value="$temppost"></td>
	</tr>
	<tr>
    		<td colspan=2 bgcolor=$miscbackone align=center><input type=hidden name="emailtopictitle" value="$topictitle"><input type=submit value="���ͱ���" name="Submit"></table></td></form></tr></table><SCRIPT>valignend()</SCRIPT>
    ~;


} # end routine.

&output($boardname,\$output);
exit;
