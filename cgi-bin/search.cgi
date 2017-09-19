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
use File::Copy;
$loadcopymo = 1;
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "search.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

for ('TYPE_OF_SEARCH','NAME_SEARCH','POST_SEARCH','FORUMS_TO_SEARCH','action', 'forum', 'SEARCH_STRING',
    'REFINE_SEARCH','CUR_TIME','nextforum', 'start','JH_SEARCH','CAT_TO_SEARCH','SEARCH_DAY','SEARCH_TIME') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    $tp =~ s/[\a\b\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    ${$_} = $tp;
}

&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($forum) && ($forum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($CUR_TIME) && ($CUR_TIME !~ /^[0-9]+$/));
$SEARCH_STRING =~ s/^system //g;
$SEARCH_STRING = &stripMETA($SEARCH_STRING);

$ipaddress  = $ENV{'REMOTE_ADDR'};
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie");   }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ((!$inmembername) or ($inmembername eq "����")) {
    $inmembername = "����";
    $filename = "����$ipaddress";
    $filename =~ s/\.//g;
}
else {
    &getmember("$inmembername","no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
    if ($userregistered eq "no") { &error("��̳����&�㻹ûע���أ�"); }
    $filename = $inmembername;
}
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

opendir (DIRS, "$lbdir");
my @files = readdir(DIRS);
closedir (DIRS);
@files = grep(/^\w+?$/i, @files);
my @searchdir = grep(/^search/i, @files);
$searchdir = $searchdir[0];

if ($searchopen eq "99") {&error("����&���������Ѿ����رգ�");}

if (($searchopen ne "")&&($searchopen ne "0")) {
    if (($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")){
        if (($membercode eq "masked")||($membercode eq "banned")) {&error("����&��������ֻ������ͨ��Աʹ��"); }
        if (($searchopen eq 1)&&($inmembername eq "����")) {&error("����&��������ֻ����ע���Աʹ�ã���ע�ᣡ"); }
        if ($searchopen eq 2) {if ($membercode !~ /^rz/) {&error("����&��������ֻ������֤��Ա�����ϼ���ʹ�ã�");}}
        if ($searchopen eq 3) {&error("����&��������ֻ������������ϼ���ʹ�ã�");}
    }
    if (($searchopen eq 4)&&($membercode ne "ad")) {&error("����&��������Ŀǰֻ����̳��ʹ�ã�");}
}

$filename =~ y/ /_/;
$filename =~ tr/A-Z/a-z/;
$savefilename = "$lbdir" . "$searchdir/$filename\_sav.cgi";
$searchfilename = "$lbdir" . "$searchdir/$filename\_sch.cgi";

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&mischeader("��������");

$output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=8 cellspacing=1 width=100%>
~;

if ($action eq "") {
    &ipbanned; #��ɱһЩ ip
    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	&whosonline("$inmembername\t����\tboth\t��������Ҫ�������\t");
    }
    opendir(DIR, "${lbdir}$searchdir");
    my @dirdata = readdir(DIR);
    closedir(DIR);
    @dirdata = grep(/\_sch.cgi$/,@dirdata);
    foreach (@dirdata){
        if ((stat("${lbdir}$searchdir/$_"))[9] < (time - 30*60)) {  
            unlink("${lbdir}$searchdir/$_");
        }
    }
}

if ($action eq "saveresults") {
    if ($inmembername eq "����") { &error("�����������&���˲��ܱ������������"); }
    $filename = $inmembername;
    $filename =~ y/ /_/;
    $filename =~ tr/A-Z/a-z/;
    copy ("${lbdir}$searchdir/$filename\_sch.cgi","${lbdir}$searchdir/$filename\_sav.cgi");
    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�����������ɹ�</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>���������
<ul><li><a href="$boardurl/$thisprog?action=display">���ص�ǰ�������</a>
<li><a href="forums.cgi?forum=$inforum">������̳</a>
<li><a href="leobbs.cgi">������̳��ҳ</a>
</ul></td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog?action=display">
~;
    &output("$boardname - ��������",\$output);
}

elsif ($action eq "loadresults") {
    if ($inmembername eq "����") { &error("�����������&�����޷��������������"); }
    $filename = $inmembername;
    $filename =~ y/ /_/;
    $filename =~ tr/A-Z/a-z/;
    $savefilename = "${lbdir}$searchdir/$filename\_sav.cgi";
    open (READ, "$savefilename") or &error("�����������&�㻹û�б�������������");
    copy ("${lbdir}$searchdir/$filename\_sav.cgi","${lbdir}$searchdir/$filename\_sch.cgi") if (!-e "${lbdir}$searchdir/$filename_sch.cgi");
    $output.=qq~<meta http-equiv="refresh" content="0; url=$thisprog?action=display">~;
}

elsif ($action eq "startsearch") {
    $SEARCH_STRING =~ s/\, /\,/g;
    if($CAT_TO_SEARCH eq "all"){
    @FORUMS_TO_SEARCH=("all");
    }elsif($CAT_TO_SEARCH =~/^cat[0-9]+$/){
    $filetoopen = "$lbdir" . "data/allforums.cgi";
#    &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(FILE, "$filetoopen");
#    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
#    &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    @FORUMS_TO_SEARCH=();$CAT_TO_SEARCH=~s/^cat//;
    foreach(@forums){
    	chomp $_;
    	@getforum=split(/\t/,$_);
    	push(@FORUMS_TO_SEARCH,$getforum[0]) if($getforum[2] eq $CAT_TO_SEARCH);
    }
    }else{
    @FORUMS_TO_SEARCH = $query->param("FORUMS_TO_SEARCH");
    $FORUMS_TO_SEARCH = @FORUMS_TO_SEARCH;
    &error("����&������ѡ��һ��Ҫ��������̳��") if ($FORUMS_TO_SEARCH <= 0);
    }
    &error("����&����������һ���ؼ��֣�") if ($SEARCH_STRING eq "");
    if ($TYPE_OF_SEARCH eq "username_search") {
        $REFINE_SEARCH = "$NAME_SEARCH";
    }
    else {
        $REFINE_SEARCH = "$POST_SEARCH";
    }
    $SEARCH_DAY=($SEARCH_DAY != 1 && $SEARCH_DAY != 7 && $SEARCH_DAY != 14 && $SEARCH_DAY != 30 && $SEARCH_DAY != 60 && $SEARCH_DAY != 90 && $SEARCH_DAY != 180 && $SEARCH_DAY != 365)?"any":$SEARCH_DAY;
    $SEARCH_TIME=($SEARCH_TIME eq "b")?"b":"f";

    $CUR_TIME =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $SEARCH_STRING =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $TYPE_OF_SEARCH =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $SEARCH_DAY =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $SEARCH_TIME =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $REFINE_SEARCH =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    $JH_SEARCH =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;
    foreach (@FORUMS_TO_SEARCH) {
    	$_ =~ s/[\a\b\f\n\e\0\r\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\?]//isg;
    }

    open (SEARCH, ">$searchfilename");
    print SEARCH "$CUR_TIME\n";
    print SEARCH "$SEARCH_STRING\n";
    print SEARCH "$TYPE_OF_SEARCH,$SEARCH_DAY,$SEARCH_TIME\n";
    print SEARCH "$REFINE_SEARCH\n";
    print SEARCH "@FORUMS_TO_SEARCH,$JH_SEARCH\n";
    close (SEARCH);

    $relocurl = "$thisprog?action=continue";
        
    $output .= qq~<tr>
<td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>������....</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
��ȴ��������������<br>
<b>��ǰ���������</b>
<ul>
<li>�������....
</ul>
</tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="1; url=$relocurl">
~;
}

elsif ($action eq "display") {
     &displayresults;
}

elsif ($action eq "continue") {
    open (INSEARCH, "$searchfilename");
    @searchparam = <INSEARCH>;
    close (INSEARCH);

    my $SEARCH_STRING    = $searchparam[1];
    chomp $SEARCH_STRING;
    (my $TYPE_OF_SEARCH,my $DAY_TO_SEARCH,my $TIME_TO_SEARCH)   = split(/\,/,$searchparam[2]);
    chomp ($TYPE_OF_SEARCH,$DAY_TO_SEARCH,$TIME_TO_SEARCH);
    my $REFINE_SEARCH    = $searchparam[3];
    chomp $REFINE_SEARCH;
    chomp $searchparam[4];
    (my $FORUMS_TO_SEARCH,my $JH_SEARCH)=split(/\,/,$searchparam[4]);
    @FORUMS_TO_SEARCH=split(/\s/,$FORUMS_TO_SEARCH);

    @KEYWORDS = split(/\,/,$SEARCH_STRING);

    $filetoopen = "$lbdir" . "data/allforums.cgi";
#    &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(FILE, "$filetoopen");
#    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
#    &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

    @checkforums = @forums;
    @checkforums = reverse(@checkforums);

    $search_in_forum = $FORUMS_TO_SEARCH;


   if ($FORUMS_TO_SEARCH eq "all") { 
       @search_in_forum =split(/\t/,$forums[$nextforum]);
       $search_in_forum = $search_in_forum[0]; 
       $checkforums = @forums;
       $nextforum++;
       if ($nextforum >= $checkforums) { $FORUMS_TO_SEARCH = "done"; } 
   }elsif($FORUMS_TO_SEARCH =~m/\s/isg){ 
       $search_in_forum = $FORUMS_TO_SEARCH[$nextforum]; 
       @checkforums = @FORUMS_TO_SEARCH; 
       @checkforums = reverse(@checkforums); 
       $checkforums = @checkforums;
       $nextforum++; 
       if ($nextforum >= $checkforums) { $FORUMS_TO_SEARCH = "done"; } 
   }else{
       $search_in_forum = $FORUMS_TO_SEARCH;$FORUMS_TO_SEARCH = "done";
   }
   my $filetoopen = "${lbdir}forum$search_in_forum/foruminfo.cgi";
   if(-e $filetoopen){
   &getoneforum($search_in_forum);
   $nofile = "true" if (($privateforum eq "yes") && ($allowedentry{$search_in_forum} ne "yes") &&($membercode ne "ad")&&($membercode ne 'smo'));
   }else{
   $nofile = "true";
   }

    open(FILE, "${lbdir}boarddata/listall$search_in_forum.cgi") or $nofile = "true";
    @topics = <FILE>;
    close(FILE);

    if ($nofile ne "true") { #start nofile
	foreach $topic (@topics) { # start topic foreach
            chomp $topic;
            ($topicid, $topictitle, $startedby,$startedpostdate) = split(/\t/,$topic);
	    $topictitle =~ s/^����������//;
if($DAY_TO_SEARCH ne "any"){
if($TIME_TO_SEARCH eq "b"){
next if(time-$startedpostdate < (86400*$DAY_TO_SEARCH));
}elsif($TIME_TO_SEARCH eq "f"){
next if(time-$startedpostdate > (86400*$DAY_TO_SEARCH));
}
}

	    if ($TYPE_OF_SEARCH eq "keyword_search") {
                if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "topictitle_search") {
                    foreach (@KEYWORDS) {
                        if (($topictitle =~ m|$_|gi)  and ("$lida" ne "$topicid")) {
                            $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$startedpostdate\t�ҵ��ؼ��֣� <B>$_</B>");
                            push (@founditems, $founditem);
                            $lida = $topicid;
                        }
                    }
                }

                if (($REFINE_SEARCH eq "both_search") or ($REFINE_SEARCH eq "post_search")) {
                    $filetoopen = "$lbdir" . "forum$forumid/$topicid.thd.cgi";
                    open (THREAD, "$filetoopen") or next;
                    @thddata = <THREAD>;
                    close (THREAD);

                    foreach (@thddata) {
                        ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon,$topicvalue,$water) = split(/\t/,$_);
                        foreach (@KEYWORDS) {
                            if (($post =~ m|$_|gi) and ("$lida" ne "$topicid")) {
                                $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$postdate\t�ҵ� <B>$_</B> ��");
                                push (@founditems, $founditem);
                                $lida = $topicid;
                            }
                        }
                    }
                }
            } # END MAIN IF 'keyword_search'
            elsif ($TYPE_OF_SEARCH eq "username_search") {
                if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "topictitle_search") {
                    foreach (@KEYWORDS) {
                        if (($startedby =~ m|$_|gi) and ("$lidc" ne "$topicid")) {
                            $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$startedpostdate\t�������ߣ� <B>$_</B>");
                            push (@founditems, $founditem);
                            $lidc = $topicid;
                        }
                    }
                }

                if ($REFINE_SEARCH eq "both_search" || $REFINE_SEARCH eq "post_search") {
                    $filetoopen = "$lbdir" . "forum$forumid/$topicid.thd.cgi";
                    open (THREAD, "$filetoopen") or next;
                    @thddata = <THREAD>;
                    close (THREAD);
		    $toptttt = 0;
                    foreach (@thddata) {
			$toptttt++;
			next if ($toptttt == 1);
                        ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon,$topicvalue,$water) = split(/\t/,$_);
                        foreach (@KEYWORDS) {
                            if (($membername =~ m|$_|gi) and ($lidc != $topicid)) { # s 'if' n1
                                $founditem = ("$forumid\t$topicid\t$topictitle\t$topicdescription\t$forumname\t$postdate\t�ظ��ˣ� <B>$membername</B>");
                                push (@founditems, $founditem);
                                $lidc = $topicid;
                            }
                        }
			$toptttt++;
                    }
                }
            } # END MAIN ELSIF 'username_search'
        } # end main foreach list loop

        # What do we do next? First push all the data to the text file

        $matches_in_forum = @founditems;
        $matches_so_far   = @searchparam - 5;

        open (OUT, ">>$searchfilename");
        foreach (@founditems) {
            chomp $_;
            print OUT "$_\n";
        }
        close (OUT);
        undef @founditems;
        undef @KEYWORDS;
    } # end if no file

    if ($FORUMS_TO_SEARCH ne "done") { 
        $relocurl = "$thisprog?action=continue&nextforum=$nextforum"; 
    } 
    else {
        $relocurl = "$thisprog?action=display";
    }

    if (!$matches_in_forum) { $matches_in_forum = "������..."; }
                       else { $matches_in_forums = " ��" if ($matches_in_forum); }

    $matches_so_far   = "������..." if (!$matches_so_far);
    $forumname        = "������..." if (!$forumname);

    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>������....</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
��ȴ����������������С�<br><b>��ǰ���������</b>
<ul><li>��ϸ���....<BR>
<li>������̳�� <b>$forumname</b>
<li>��������� <b>$matches_so_far</b>
<li>ƥ����ϣ� <b>$matches_in_forum</b>$matches_in_forums
</ul><center><a href=$thisprog?action=display><b>>> ͣ ֹ �� �� <<</b></a></center>
</tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="1; url=$relocurl">
~;
}
else {
    $filetoopen = "$lbdir" . "data/allforums.cgi";
#    &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    open(FILE, "$filetoopen");
#    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
#    &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    $a=0;
    foreach $forum (@forums) { #start foreach @forums
	$a  = sprintf("%09d",$a);
	chomp $forum;
	($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl,$fgwidth,$fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);
	next if (($forumid !~ /^[0-9]+$/)||($categoryplace !~ /^[0-9]+$/));
	$categoryplace  = sprintf("%09d",$categoryplace);
	if ((($privateforum eq "yes") && ($userregistered ne "no") && ($allowedentry{$forumid} eq "yes"))||($membercode eq "ad")||($membercode eq 'smo')) {
	    $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t");
	}
	elsif ($privateforum ne "yes") {
	    $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t");
	}
	push (@rearrangedforums, $rearrange);
	$a++;
    } # end foreach (@forums)
    @rearrangedforums = sort (@rearrangedforums);
    $count=1; 
    foreach (@rearrangedforums) {
    	chomp $_;
        (my $categoryplace,my $a, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $miscad2, my $misc, my $forumpass, my $hiddenforum, my $indexforum,my $teamlogo,my $teamurl,my $fgwidth,my $fgheight, my $miscad4, my $todayforumpost, my $miscad5) = split(/\t/,$_);
        $categoryplace  = sprintf("%01d",$categoryplace);
            $child=($category =~/^childforum-[0-9]+/)?"��|":"";
            if ($hiddenforum eq "yes"){ $hidden="(����)"; }else{ $hidden=""; } 
            if ($categoryplace ne $lastcategoryplace) {
                $jumphtml .= "<option value=\"\" style=background-color:$titlecolor>��$category\n</option>";
                $jumphtml2 .= qq(<input type="radio" name="CAT_TO_SEARCH" value="cat$categoryplace">$category<BR>);
                $jumphtml .= "<option value=\"$forumid\">$child��|- $forumname$hidden\n</option>" if ($hidden eq "" || $membercode eq "ad");
            }
            else {
                $jumphtml .= "<option value=\"$forumid\">$child��|- $forumname$hidden\n</option>" if ($hidden eq "" || $membercode eq "ad");
            }
        $lastcategoryplace = $categoryplace;
    }
    if ($forum) { $jumphtml =~ s/\ value="$forum"/\ value="$forum" selected/isg; }
    
    $currenttime = time;
    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align="center">
<p><FORM action="$thisprog" method="post" name="Search">
<input type=hidden name="action" value="startsearch">
<input type=hidden name="CUR_TIME" value="$currenttime">
<input type=hidden name="JH_SEARCH" value="no">
<font face="$font" color=$fontcolormisc>$ssboom<b>������Ҫ�����Ĺؼ���</b></font></td></tr>
<tr><td bgcolor=$miscbackone width colspan=2 align="center" valign="middle"><font face="$font" color=$fontcolormisc>
(����ؼ���֮��ʹ�ö��� ',' �ָ����ؼ����в�Ҫʹ�� # \$ < > ( ) { } & ; | * ? ��Щ�������)</font><br><br>
<input type=text size=40 name="SEARCH_STRING"></td></tr>
<tr><td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc><b>����ѡ��</b></font></td></tr>
<tr><td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
<b>��������</b></font>&nbsp;<input name="TYPE_OF_SEARCH" type="radio" class=1 value="username_search"></td>
<td bgcolor="$miscbackone" align="left" valign="middle">
<select name="NAME_SEARCH">
<option value="topictitle_search">������������
~;
$output .= qq~
<option value="post_search">�����ظ�����
<option value="both_search">���߶�����
~ if ($searchall ne "no" || $membercode eq "ad");
$output .= qq~
</select>
</td></tr>
<tr><td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
<b>�ؼ�������</b></font>&nbsp;<input name="TYPE_OF_SEARCH" type="radio" class=1 value="keyword_search" checked></td>
<td bgcolor="$miscbackone" align="left" valign="middle">
<select name="POST_SEARCH">
<option value="topictitle_search">�������������ؼ���
~;
$output .= qq~
<option value="post_search">�����������������ؼ���
<option value="both_search">����������������������ؼ���
~ if ($searchall ne "no" || $membercode eq "ad");
$output .= qq~
</select>
</td></tr>
<tr><td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
<b>��Ѱ����</b></font></td>
<td bgcolor="$miscbackone" align="left" valign="middle">��
<select name="SEARCH_DAY"><option value="any" selected>�κ�����<option value="1">  1 ��<option value ="7"> 1 ��<option value = "14"> 2 ��<option value="30"> 1 ����<option value="90"> 3 ����<option value="180"> 6 ����<option value="365"> 1 ��</select>
<select name="SEARCH_TIME"><option value="b" selected>֮ǰ<option value="f">֮��</select>
</td></tr>
<tr><td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
<b>��ѡ��Ҫ��������̳�����</b></font></td>
<td bgcolor="$miscbackone" align="left" valign="middle">
<input type="radio" name="CAT_TO_SEARCH" value="all"$Seleced[0]>������̳<BR>$jumphtml2
</td></tr>
<tr><td bgcolor="$miscbackone" align="right" valign="middle"><font face="$font" color=$fontcolormisc>
<input type="radio" name="CAT_TO_SEARCH" value="select"$Seleced[1] checked><b>��ѡ��̳</b><br>�� Ctrl ����ѡ,������Ч</font></td>
<td bgcolor="$miscbackone" align="left" valign="middle">
<select name="FORUMS_TO_SEARCH" size="6" width=100% multiple>$jumphtml</select>
</td></tr>
<tr>
<td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center><BR>
<input type=submit value="��ʼ����">����<input value="�����������" type=button onclick="javascript:location.href='$boardurl/$thisprog?action=loadresults'">
</td></form></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
}

&output("$boardname - ��������",\$output);
exit;

sub displayresults {
    open (READ, "$searchfilename") or &error("�������&�Բ����������ֻ�ܱ��� 30 ���ӣ�������������");
    @completed_search = <READ>;
    close (READ);

    foreach (@completed_search) {
	push (@TRUE_RESULTS, $_) if ($_ =~ /\t/)
    }

    $total_results = @TRUE_RESULTS;

    $SEARCH_STRING    = $completed_search[1];
    chomp $SEARCH_STRING;
    ($TYPE_OF_SEARCH,$DAY_TO_SEARCH,$TIME_TO_SEARCH)   = split(/\,/,$completed_search[2]);
    chomp ($TYPE_OF_SEARCH,$DAY_TO_SEARCH,$TIME_TO_SEARCH);
    $REFINE_SEARCH    = $completed_search[3];
    chomp $REFINE_SEARCH;
    chomp $completed_search[4];
    ($FORUMS_TO_SEARCH,$JH_SEARCH)=split(/\,/,$completed_search[4]);
   
    $TYPE_OF_SEARCH = "�ؼ���"    if ($TYPE_OF_SEARCH eq "keyword_search");
    $TYPE_OF_SEARCH = "����"      if ($TYPE_OF_SEARCH eq "username_search");

    $REFINE_SEARCH = "����"       if ($REFINE_SEARCH eq "topictitle_search");
    $REFINE_SEARCH = "��������"   if ($REFINE_SEARCH eq "post_search");
    $REFINE_SEARCH = "����ͻظ�" if ($REFINE_SEARCH eq "both_search");

    $TYPE_SEARCH = "��������"     if ($JH_SEARCH eq "no");
    $TYPE_SEARCH = "��������"     if ($JH_SEARCH eq "jinghua");
    $TYPE_SEARCH = "��������"     if ($JH_SEARCH eq "recycle");
    $TYPE_SEARCH = "ͶƱ����"     if ($JH_SEARCH eq "poll");
    $TYPE_SEARCH = "��������"     if ($JH_SEARCH eq "lock");
    $TYPE_SEARCH = "��������"     if ($JH_SEARCH eq "hot");
    $TYPE_SEARCH = "�ö�����"     if ($JH_SEARCH eq "top");

    if ($total_results > 0) {
	$result_line = qq(ʹ��<b>$TYPE_OF_SEARCH</b>������ʽ����<b>$REFINE_SEARCH</b>�������� <b>$total_results</b> ����ƥ�������);
    }
    else {
        $result_line = qq(�Բ���ʹ��<b>$TYPE_OF_SEARCH</b>������ʽ����<b>$REFINE_SEARCH</b>��<b>û��</b>�������κ���ƥ�������);
    }	                  

    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=3 align=center>
<font face="$font" color=$fontcolormisc>$result_line</font>
</td></tr>
<tr><td bgcolor=$miscbackone valign=middle align=center>
<font face="$font" color=$fontcolormisc><b>����</b></font></td>
<td bgcolor=$miscbackone valign=middle align=center>
<font face="$font" color=$fontcolormisc><b>����ʱ�䡢λ��</b></font></td>
<td bgcolor=$miscbackone valign=middle align=center>
<font face="$font" color=$fontcolormisc><b>�ؼ���ƥ��˵��</b></font></font>
</td></tr>
~;

    $maxthreads = 25;
    $numberofitems = $total_results;
    $numberofpages = $numberofitems / $maxthreads;
    $instart = $start;

    if ($numberofitems > $maxthreads) {
        $showmore = "yes";
        if ($instart eq "" || $instart < 0) { $instart = 0; }
        if ($instart > 0) { $startarray = $instart; }
                     else { $startarray = 0; }
        $endarray = $instart + $maxthreads - 1;
        if ($endarray < ($numberofitems - 1)) { $more = "yes"; }
        if (($endarray > ($maxthreads - 1)) && ($more ne "yes")) { $endarray = $numberofitems - 1; }
    }
    else {
        $showmore = "no";
        $startarray = 0;
        $pages = qq~<font face="$font" color=$menufontcolor>�������ֻ��һҳ</font>~;
        $endarray = $numberofitems - 1;
    }

    if ($showmore eq "yes") { #1
	if ($maxthreads < $numberofitems) { #2
            ($integer,$decimal) = split(/\./,$numberofpages);
            if ($decimal > 0) { $numberofpages = $integer + 1; }
            $pagestart = 0;
            $counter = 0;
            while ($numberofpages > $counter) { #3
                $counter++;
                if ($instart ne $pagestart) { $pages .= qq~<a href="$thisprog?action=display&start=$pagestart"><font face="$font" color=$menufontcolor><b>$counter</b></font></a> ~; }
                                       else { $pages .= qq~<font face="$font" color=$fonthighlight><b>$counter</b></font> ~; }
		$pagestart = $pagestart + $maxthreads;
	    } #e3
	} #e2
        $pages = qq~<font face="$font" color=$menufontcolor><b>����������ж�ҳ</b> [ $pages ]~;
    } #1
    
    $timeadd = $timedifferencevalue*3600 + $timezone*3600;
    foreach (@TRUE_RESULTS[$startarray .. $endarray]) { # start foreach loop
        ($forumid, $topicid, $topictitle, $topicdescription, $forumname, $postdate, $string_returned) = split(/\t/,$_);
        $topictitle =~ s/^����������//;
        $postdate = $postdate + $timeadd;
        $longdate = &longdate("$postdate");
        $topicdescription = qq(&nbsp;-=> $topicdescription) if $topicdescription;

	$inforum = $forumid;
    if (($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes")) {
	$admini = qq~<DIV ALIGN=Right><font color=$titlecolor>|<a href=jinghua.cgi?action=add&forum=$inforum&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=locktop&forum=$inforum&topic=$topicid><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=puttop&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=lock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|<a href=postings.cgi?action=unlock&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|<a href=delpost.cgi?action=delete&forum=$inforum&topic=$topicid><font color=$titlecolor>ɾ</font></a>|<a href=delpost.cgi?action=movetopic&forum=$inforum&topic=$topicid&checked=yes><font color=$titlecolor>��</font></a>|</font>&nbsp;</DIV>~;
    }
    elsif ((lc($inmembername) eq lc($startedby)) && ($inpassword eq $password) && ($inmembername !~ /^����/)) {
	if ($arrowuserdel eq "on") {
	    $admini = qq~<DIV ALIGN=Right><font color=$titlecolor>| <a href=postings.cgi?action=lock&forum=$inforum&topic=$topicid><font color=$titlecolor>������������������˻ظ�</font></a> | <a href=delpost.cgi?action=delete&forum=$inforum&topic=$topicid><font color=$titlecolor>ɾ������</font></a> |</font>&nbsp;&nbsp;</DIV>~;
	}
	else { undef $admini; }
    }
    else { undef $admini; }

        $output .= qq(<tr><td bgcolor=$miscbackone valign=middle>
<font face="$font" color=$fontcolormisc><B><a href="topic.cgi?forum=$forumid&topic=$topicid" target=_blank>$topictitle</a></B><br>
$topicdescription$admini</td>
<td bgcolor=$miscbackone valign=middle>
<font face="$font" color=$fontcolormisc>������̳�� <a href="forums.cgi?forum=$forumid">$forumname</a><BR>����ʱ�䣺 $longdate</font></td>
<td bgcolor=$miscbackone valign=middle align=center>
<font face="$font" color=$fontcolormisc>$string_returned</font></td></tr>
);
	undef $topicdescription;
    } # end foreach

    $output .= qq(<tr><td bgcolor="$miscbacktwo" valign=middle colspan=2 align=center>
<font face="$font" color=$fontcolormisc>$pages</font></td>
<td bgcolor="$miscbacktwo" valign=middle colspan=1 align=center>
<font face="$font" color=$fontcolormisc>
<img src=$imagesurl/images/icon.gif align=absmiddle border=0> <a href="$thisprog"><b>�ٴ����� </b></a>
</font><br><font face="$font" color=$fontcolormisc>
<img src=$imagesurl/images/saveas.gif align=absmiddle> <a href="$thisprog?action=saveresults"><b>����������� </b></a>
</font></td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
);
    &output("$boardname - �������",\$output);

}
exit;
