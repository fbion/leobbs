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
use Image::Info qw(image_info);
$LBCGI::POST_MAX=800000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
require "rebuildlist.pl";

$|++;

$thisprog = "setforums.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

#&ipbanned; #��ɱһЩ ip

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

@params = $query->param;
foreach $param(@params) {
    next unless defined $param;
    next if $param eq 'SEND_MAIL';
    $theparam = $query->param($param);
    $theparam = &cleaninput("$theparam");
    $PARAM{$param} = $theparam;
}

    $action      =  $PARAM{'action'};
    $inforum     =  $PARAM{'forum'};
    $incategory  =  $PARAM{'category'};
    $checkaction =  $PARAM{'checkaction'};
    $inmovetype     =  $PARAM{'movetype'};
    $incforum     =  $PARAM{'cforum'};

    $new_categoryname     = $PARAM{'categoryname'};
    $new_categorynumber   = $PARAM{'categorynumber'};
    $new_forumname        = $PARAM{'forumname'};
    $new_forumdescription = $PARAM{'forumdescription'};
    $new_forummoderator   = $PARAM{'forummoderator'};
    $new_forummoderator =~ s/\, /\,/gi;
    $new_forummoderator =~ s/ \,/\,/gi;
    $new_catemods        = $PARAM{'catemods'}; 
    $new_catemods        =~ s/\, /\,/gi; 
    $new_catemods        =~ s/ \,/\,/gi;
    
    $new_htmlstate        = $PARAM{'htmlstate'};
    $new_idmbcodestate    = $PARAM{'idmbcodestate'};
    $new_privateforum     = $PARAM{'privateforum'};
    $new_forumpass	  = $PARAM{'forumpass'};
    $new_hiddenforum	  = $PARAM{'hiddenforum'};
    $new_indexforum	  = $PARAM{'indexforum'};
    $new_startnewthreads  = $PARAM{'startnewthreads'};
    $new_forumgraphic     = $PARAM{'forumgraphic'};
    $new_teamlogo         = $PARAM{'teamlogo'};
    $new_teamurl          = $PARAM{'teamurl'};
    $new_fgwidth          = $PARAM{'fgwidth'};
    $new_fgwidth1         = $PARAM{'fgwidth1'};
    $new_fgheight         = $PARAM{'fgheight'};
    $new_fgheight1        = $PARAM{'fgheight1'};

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;

&getmember("$inmembername","no");

if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) { #s1

            my %Mode = (
            'addforum'            =>    \&addforum,
            'processnew'          =>    \&createforum,
            'edit'                =>    \&editform,
            'doedit'              =>    \&doedit,
            'bakcat'              =>    \&bakcat,
            'upcat'               =>    \&upcat,
            'addcategory'         =>    \&catform,
            'doaddcategory'       =>    \&doaddcategory,
            'editcatname'         =>    \&editcatname,
            'reordercategories'   =>    \&reordercats,
            'updatecount'  	  =>    \&updatecount,
            'recount'             =>    \&recount,
            'reorder'             =>    \&reorder,
            'delxzb'              =>    \&delxzb,
            'delans'              =>    \&delans,
            'dellogs'             =>    \&dellogs

            );


    if($Mode{$action}) {
        $Mode{$action}->();
    }
    elsif (($action eq "delete") && ($checkaction ne "yes")) { &warning; }
    elsif (($action eq "delete") && ($checkaction eq "yes")) { &deleteforum; }
    else { &forumlist; }

}
else {
    &adminlogin;
}
print qq~</td></tr></table></body></html>~;
exit;

##################################################################################
sub dellogs {

                open (FILE, "${lbdir}boarddata/adminlog$inforum.cgi");
                @baddel = <FILE>;
                close (FILE);
		$baddels = @baddel;
		
		if ($baddels > 50) { $baddels = 50; }

                open (FILE, ">${lbdir}boarddata/adminlog$inforum.cgi");
                for ($i=0;$i<$baddels;$i++) {
                    $j=$i-$baddels;
                    $info = $baddel[$j];
                    chomp $info;
                    print FILE "$info\n";
                }
                close (FILE);
    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>ɾ�������İ�����־</b><p>
<font color=#333333>�������50����¼���������ڵİ�����־��¼�Ѿ�ɾ��!��</font>
</td></tr>
~;
}	

sub delxzb {
    unlink ("${lbdir}data/xzb$inforum.cgi");
    unlink ("${lbdir}data/xzbs$inforum.cgi");
    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>ɾ���������е�С�ֱ�</b><p>
<font color=#333333>�������е�С�ֱ��Ѿ���ɾ����</font>
</td></tr>
~;
}	

sub delans {
    unlink ("${lbdir}data/news$inforum.cgi");
    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>ɾ���������еĹ���</b><p>
<font color=#333333>�������еĹ����Ѿ���ɾ����</font>
</td></tr>
~;
}	

sub bakcat {
    $filetoopen = "$lbdir" . "data/allforums.cgi";
#    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
#    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @forums = <FILE>;
    close(FILE);
#    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    my $size=@forums;

    if ($size > 0) {
        unlink ("${lbdir}data/allforums.pl");
        copy("${lbdir}data/allforums.cgi","${lbdir}data/allforums.pl");
        chmod (0666,"${lbdir}data/allforums.pl");
        print qq~<tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF><b>��ӭ������̳�������� / ��̳����</b></td></tr>
<tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#333333><b>���з����Ѿ�����</b><br>��ǰ��̳ $size ���Ѿ����ݣ�</td></tr>
~;
    }
    else {
        print qq~<tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF><b>��ӭ������̳�������� / ��̳����</b></td></tr>
<tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#333333><b>���з���û�б���</b><br>��ǰ��̳�����ļ�û���ҵ�����ʹ�����½�����̳�����湦��һ�Σ�</td></tr>
~;
    }
}

sub upcat {
    open(FILE, "${lbdir}data/allforums.pl");
    my @forums = <FILE>;
    close(FILE);
    my $size=@forums;

    if ($size > 0) {
        unlink ("${lbdir}data/allforums.cgi");
        copy("${lbdir}data/allforums.pl","${lbdir}data/allforums.cgi");
        chmod (0666,"${lbdir}data/allforums.cgi");
        print qq~<tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF><b>��ӭ������̳�������� / ��̳����</b></td></tr>
<tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#333333><b>���з����Ѿ���ԭ</b><br>��ǰ��̳ $size ���Ѿ���ԭ��</td></tr>
~;
    }
    else {
        print qq~<tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF><b>��ӭ������̳�������� / ��̳����</b></td></tr>
<tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#333333><b>���з���û�л�ԭ</b><br>��ǰ���ݷ����ļ�û���ҵ���ʹ�û�ԭǰ���ȱ��ݣ�</td></tr>
~;
    }
    opendir (CATDIR, "${lbdir}cache");
    @dirdata = readdir(CATDIR);
    closedir (CATDIR);
    @dirdata = grep(/forumcache/,@dirdata);
    foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
}

sub updatecount {
    $filetoopen = "$lbdir" . "data/allforums.cgi";
#    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
#    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @forums = <FILE>;
    close(FILE);
#    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    $totle1 = 0;
    $totle2 = 0;

    foreach (@forums) {
        chomp $_;
        (my $tempno,my $no) = split(/\t/,$_);
   	next if ($tempno !~ /^[0-9]+$/);
   	eval{ require "${lbdir}boarddata/forumposts$tempno.pl";};
	$totle1 += $threads;
	$totle2 += $posts;
    }
    require "$lbdir" . "data/boardstats.cgi";

    $filetomake = "$lbdir" . "data/boardstats.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totle1\'\;\n";
        print FILE "\$totalposts = \'$totle2\'\;\n";
        print FILE "\n1\;";
        close (FILE);
    }
    &winunlock($filetomake) if ($OS_USED eq "Nt");

    print qq~<tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF><b>��ӭ������̳�������� / ��̳����</b></td></tr>
<tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#333333><b>������Ϣ�Ѿ�����</b><br>
����������$totle1 ƪ<BR>�ظ�������$totle2 ƪ</td></tr>
~;
}

sub forumlist {
    print qq~<tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF><b>��ӭ������̳�������� / ��̳����</b></td></tr>
<tr><td bgcolor=#FFFFFF colspan=3><font color=#333333>
<b>����<a href="$thisprog?action=updatecount">����ͳ��</a>��</b><br>��������̳����������ͳ�����������������޸���ҳ��������ʾ�Ĵ���<br><br>
</td></tr><tr><td bgcolor=#FFFFFF colspan=3><font color=#333333>
<b>����<a href="$thisprog?action=bakcat" OnClick="return confirm('ȷ��������̳����ô��');">������̳����</a>/<a href="$thisprog?action=upcat" OnClick="return confirm('ȷ����ԭ��̳����ô��');">��ԭ��̳����</a></b><br>
��������̳�ķ�����б��ݣ����������޸�������̳��ʧ�������(��̳Ҳ���Զ����б��ݺͻָ�)<br><br>
</td></tr><tr><td bgcolor=#FFFFFF colspan=3><font color=#333333>
<b>����ע�����</b><br>�����棬��������Ŀǰ���е���̳���ࡣ�����Ա༭��̳��������������һ���µ���̳����������С�Ҳ���Ա༭��ɾ��Ŀǰ���ڵ���̳�������Զ�Ŀǰ�ķ������½������С�<br>
</td></tr>
~;
    $filetoopen = "$lbdir" . "data/allforums.cgi";
#    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
#    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
#    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    $a = 0;
    foreach (@forums) {
	$a  = sprintf("%09d",$a);
        chomp $_;
        ($forumid, $category, $categoryplace, $forumname, my $no) = split(/\t/,$_);
    	next if ($forumid !~ /^[0-9]+$/);
	if ($category =~ /^childforum-[0-9]+/) {
	    $topforumno=$category;
	    $topforumno=~s/^childforum-//;
            my $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumid\t$topforumno\t");
            push (@cforums, $rearrange);
	    next;
	}
	$categoryplace  = sprintf("%09d",$categoryplace);
        my $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumid\t\t");
        push (@rearrangedforums, $rearrange);
        $a++;
    }
    my @rearrangedforums1 = sort (@rearrangedforums);
    undef @rearrangedforums;
    foreach (@rearrangedforums1) {
    	chomp $_;
        ($categoryplace,my $a,$category, $forumname, $forumid) = split(/\t/,$_);
        push (@rearrangedforums, "$categoryplace\t$a\t$category\t$forumname\t$forumid\t");
        @tempcforum = grep(/\t$forumid\t$/i, @cforums);
        push (@rearrangedforums,@tempcforum);
    }
    $highest = 0;
    foreach (@rearrangedforums) {
    	chomp $_;
        ($categoryplace,my $a,$category, $forumname, $forumid, $no) = split(/\t/,$_);
        $categoryplace  = sprintf("%01d",$categoryplace);
        if ($categoryplace ne $lastcategoryplace) {
            if ($categoryplace > $highest) { $highest = $categoryplace; }
            print qq~<tr><td bgcolor=#FFFFFF colspan=3 ><font color=#333333><hr noshade></td></tr><tr><td bgcolor=#EEEEEE width=20% nowrap><font color=#333333>�������� <b>$category</b><td bgcolor=#EEEEEE width=15% align=center nowrap><font color=#333333><a href="$thisprog?action=editcatname&category=$categoryplace">�༭��������</a></td><td bgcolor=#EEEEEE width=25%><font color=#333333><a href="$thisprog?action=addforum&category=$categoryplace">������̳���˷�����</a></font></td></td></tr>~;
        }
   	eval{ require "${lbdir}boarddata/forumposts$forumid.pl";};
        if($category =~/^childforum-[0-9]+/){
        $temp="����̳��";$addforumline="";$addspace="��";
        }else{
        $temp="��̳��";$addforumline=qq~<BR><a href="$thisprog?action=addforum&category=childforum-$forumid">��������̳������̳��</a>~;$addspace="";
        }
       $filerequire = "$lbdir" . "data/style${forumid}.cgi"; 
       if (-e $filerequire) { 
       $mydelthisstlye = qq~ <a href="forumstyles.cgi?action=delstyle&forum=$forumid">ɾ�������Զ�����</a> |~; 
       $mystyle = qq~| <a href="forumstyles.cgi?action=style&forum=$forumid"><font color=red>�޸ĸ������</font></a>~; 
       } 
       else { 
       $mystyle = qq~| <a href="forumstyles.cgi?action=style&forum=$forumid">��Ӹ������</a>~; 
       }
    
	print qq~<tr><td bgcolor=#FFFFFF colspan=3 nowrap>$addspace<font color=#333333>$temp�� <b>$forumname</b>��<br>$addspace�������� <b>$threads</b>��<-->��<font color=#333333>�ظ����� <b>$posts</b><br><br>$addspace<a href="$thisprog?action=edit&forum=$forumid">�༭����</a> | <a href="$thisprog?action=recount&forum=$forumid">���¼�������ͻظ��� / �޸�</a> $mystyle | <a href="$thisprog?action=reorder&forum=$forumid">�������������</a><BR>$addspace<a href="$thisprog?action=delxzb&forum=$forumid">ɾ����������С�ֱ�</a> | <a href="$thisprog?action=delans&forum=$forumid">ɾ���������й���</a> | <a href="$thisprog?action=dellogs&forum=$forumid">ɾ������������־</a> | $mydelthisstlye <a href="$thisprog?action=delete&forum=$forumid">ɾ��������������</a>$addforumline<BR><BR></td></font></td></tr>~;
        $lastcategoryplace = $categoryplace;
	undef $mydelthisstlye; 
        undef $mystyle;
    }
    $highest++;
    print qq~<td bgcolor=#FFFFFF colspan=3 ><font color=#333333><hr noshade></td></tr>
<tr><td bgcolor=#EEEEEE colspan=3 align=center><font color=#333333>
<a href="$thisprog?action=reordercategories">��̳������������</a>����--����<a href="$thisprog?action=addcategory&category=$highest">���ӷ���(ͬʱ����һ����̳)</a>
</font></td></tr></tr></table></td></tr></table>
~;
}

sub recount {
    mkdir ("${lbdir}forum$inforum", 0777) unless (-e "${lbdir}forum$inforum");
    my $truenumber = rebuildLIST(-Forum=>"$inforum");
    ($topiccount,$threadcount) = split (/\|/,$truenumber);
    $threadcount = 0 if (!$threadcount);
    $topiccount  = 0 if (!$topiccount);

        $filetoopen = "$lbdir" . "boarddata/listno$inforum.cgi";
        open(FILE, "$filetoopen");
        $topicid = <FILE>;
        close(FILE);
        chomp $topicid;
	my $rr = &readthreadpl($inforum,$topicid);
	(my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp) = split (/\t/,$rr);
            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
	    $lastposter = $startedby if ($lastposter eq "");
	    $filetoopen = "";
	    if (-e "${lbdir}boarddata/foruminfo$inforum.cgi") {
                open(FILE, "+<${lbdir}boarddata/foruminfo$inforum.cgi");
                ($no, $threads, $posts, $todayforumpost, $no) = split(/\t/,<FILE>);
                close(FILE);
	        seek(FILE,0,0);
                print FILE "$lastforumpostdate\t$topiccount\t$threadcount\t$todayforumpost\t$lastposter\t\n";
                close(FILE);
            } else {
                open(FILE, ">${lbdir}boarddata/foruminfo$inforum.cgi");
                print FILE "$lastforumpostdate\t$topiccount\t$threadcount\t$todayforumpost\t$lastposter\t\n";
                close(FILE);
            }
	    open(FILE, ">${lbdir}boarddata/forumposts$inforum.pl");
	    print FILE "\$threads = $topiccount;\n\$posts = $threadcount;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);

    print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>��ӭ������̳�������� / �ؼ�������ͻظ���</b>
</td></tr><tr><td bgcolor=#FFFFFF colspan=2><font color=#990000>
<center><b>��̳���³ɹ�</b></center><p>�������� $topiccount<p>�ظ����� $threadcount
</td></tr></table></td></tr></table>
~;
}

sub addforum {

        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
        <b>��ӭ������̳�������� / ������̳</b>
        </td></tr>
        ~;

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @forums = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");


# Find the category name from the number

	if($incategory !~/^childforum-[0-9]+/){
        foreach (@forums) {
            ($trash, $tempcategoryname, $tempcategoryplace, $trash) = split(/\t/, $_);
            if ($incategory eq $tempcategoryplace && $tempcategoryname !~/childforum-[0-9]+/) {
                $category = $tempcategoryname;
                $categoryn = "�� '$tempcategoryname' �����������µ���̳";
            }
        }
	}else{
        foreach (@forums) {
            ($tempforumno, $tempcategoryname, $tempcategoryplace, $tempforumname) = split(/\t/, $_);
            if ($incategory eq "childforum-$tempforumno") {
                $category = $incategory;
                $incategory = $tempcategoryplace;
                $categoryn = "�� '$tempforumname' �������µ�����̳";
		$modiii = "<BR><font color=blue>����̳���Զ��̳и���̳�İ�������ע�ⲻҪ�ظ��������</font>";
            }
        }
	}

    ($fgwidth,$fgwidth1) = split(/\|/,$fgwidth);
    ($fgheight,$fgheight1) = split(/\|/,$fgheight);

# Present the form to be filled in

        print qq~
        
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>$categoryn</b>
        </td></tr>

        <form action="$thisprog" method="post" enctype="multipart/form-data" name=FORM>
        <input type=hidden name="categorynumber" value="$incategory">
        <input type=hidden name="categoryname" value="$category">
        <input type=hidden name="action" value="processnew">       
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>����������̳������<BR>(������� 20 ��������)</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumname" value="$forumname" maxlength=40></td>
        </tr>       
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>����������̳��������֧�� HTML �﷨</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>   
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳�����������ϣ���ж����������ʹ�� "," (Ӣ�Ķ��ţ��������Ķ���)������<BR><B>����</B>��ɽӥ, ����ȱ</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forummoderator" value="$forummoderator">$modiii</td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� HTML ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="htmlstate">
        <option value="on">ʹ��<option value="off" selected>��ʹ��</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� LeoBBS ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="idmbcodestate">
        <option value="on" selected>ʹ��<option value="off">��ʹ��</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���Ϊ˽����̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="privateforum">
        <option value="yes">��<option value="no" selected>��</select> ��̳�����ܰ�����Ч
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>˽����̳����</b>(ֻ��˽����̳��Ч)</font></td>
        <td bgcolor=#FFFFFF>
       <input type=text size=12 name="forumpass" value="$forumpass" maxlength=20> ��̳�����ܰ�����Ч</td>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�������̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="hiddenforum">
        <option value="yes">��<option value="no" selected>��</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���ʾ��������</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="indexforum">
        <option value="yes" selected>��<option value="no" >��</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>1. ������̳-ֻ����ע���Ա����<br>2. ������̳-���������˷���<br>3. ������̳-̳���Ͱ��������ԣ�����ע���û�ֻ�ܻظ�<br>4. ������-ֻ���������̳�����ԺͲ���<br>5. ��֤��̳-��̳���Ͱ����⣬����ע���û�������Ҫ��֤<br>6. ������̳-����ֻ������̳��������̳���������ظ�<br></font></td>
        <td bgcolor=#FFFFFF>
        <select name="startnewthreads">
        <option value="yes" selected>������̳<option value="all">������̳<option value="follow">������̳<option value="no">������<option value="cert">��֤��̳<option value="onlysub">������̳</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳ͼƬ��֧��FLASH��</b><br>������ͼƬ���ƣ���ͼ������ myimages Ŀ¼�£���������������̳ҳ�����Ϸ�����С������� 160*60 ���ڡ�<BR><b>�벻Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=20 name="forumgraphic" value="logo.gif">
~;

opendir (DIR, "${imagesdir}myimages");
@thd = readdir(DIR);
closedir (DIR);
        my $myimages="";
        $topiccount = @thd;
        @thd=sort @thd;
        for (my $i=0;$i<$topiccount;$i++){
            next if (($thd[$i] eq ".")||($thd[$i] eq ".."));
            $myimages.=qq~<option value="$thd[$i]">$thd[$i]~;
        }
        $myimages =~ s/value=\"$action\"/value=\"$action\" selected/;        
print qq~
<script>
function select(){
document.FORM.forumgraphic.value=FORM.image.value;
document.bbsimg.src = "$imagesurl/myimages/"+FORM.image.value;}
function select2(){
document.FORM.teamlogo.value=FORM.image2.value;
document.bbsimg.src = "$imagesurl/myimages/"+FORM.image2.value;}
function select3(){
document.bbsimg.src = FORM.addme.value;}
</script>
<select name="image" onChange=select()><option value="blank.gif">ѡ��ͼƬ$myimages</select></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳FLASH�����߶ȡ����</b><br>����ȷ����FLASH�����ĸ߶ȼ���ȡ�<BR></font></td>
        <td bgcolor=#FFFFFF>
        ��ȣ�<input type=text size=3 name="fgwidth">�����߶ȣ�<input type=text size=3 name="fgwidth1"></td>
        </tr>
               
	<tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>����ͼƬ</b>(���û�У��뱣��ԭ��)<br>������ͼƬ���ƣ���ͼƬ��������������ҳ���¡�<BR><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=20 name="teamlogo" value=""> <select name="image2" onChange=select2()><option value="blank.gif">ѡ��ͼƬ$myimages</select></td>
        </tr> 
         
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>����ͼƬFLASH�����߶ȡ����</b><br>����ȷ����FLASH�����ĸ߶ȼ���ȡ�<BR></font></td>
        <td bgcolor=#FFFFFF>
        ��ȣ�<input type=text size=3 name="fgheight">�����߶ȣ�<input type=text size=3 name="fgheight1"></td>
        </tr>

	<tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�ϴ���̳/����ͼƬ</b><br>������ͼƬ���ƣ���ͼƬ��������̳ͼƬ/����ͼƬ��</font></td>
        <td bgcolor=#FFFFFF>
        <input type="file" size=20 name="addme" onchange="select3()"><br>֧�����ͣ�gif��jpg��bmp��png��swf</td>
        </tr> 

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>������ַ</b>(���û�У��뱣��ԭ��)<br>������������̳ͼƬ�ĵ�ַ����</td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamurl" value="http://"></td>
        </tr><tr>
        <td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>ͼ��Ԥ��(��֧�� Flash)</b></font><br><IMG border=0 name=bbsimg src="$imagesurl/myimages/blank.gif" align="absmiddle" onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333"></td>
        </tr>
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
        ~;
        
} # end route   


##################################################################################
######## Subroutes ( Create Forum )


sub createforum {
#		&errorout("������̳�����벻�ܿգ���") if (($new_privateforum eq "yes")&&($new_forumpass eq ""));
		&errorout("�Բ�����̳���ֹ������������ 20 �������ڣ�") if (length($new_forumname) >40);
		&errorout("��̳���ֲ��ܿգ���") if ($new_forumname eq "");
		&errorout("��̳�������ܿգ���") if ($new_forumdescription eq "");
		$new_privateforum = "yes" if ($new_forumpass ne "");

&douppics();

                $filetoopen = "$lbdir" . "data/allforums.cgi";
	        &winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE, "$filetoopen");
  	        flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                foreach (@forums) {
                    ($forumid, $binit) = split(/\t/,$_);
                    if ($forumid > $high) { $high = $forumid; }
                    }

                $high++;

                $newforumid = $high;

                $dirtomake = "$lbdir" . "forum$newforumid";
                mkdir ("$dirtomake", 0777);

                $dirtomake1 = "$lbdir" . "FileCount/$newforumid";
                mkdir ("$dirtomake1", 0777);

                $filetomake = "$dirtomake1/index.html";
                open(FILE,">$filetomake");
                print FILE "-";
                close(FILE);

                $dirtomake1 = "$imagesdir" . "$usrdir/$newforumid";
                mkdir ("$dirtomake1", 0777);

                $filetomake = "$dirtomake1/index.html";
                open(FILE,">$filetomake");
                print FILE "-";
                close(FILE);

                $filetomake = "$dirtomake/index.html";
                open(FILE,">$filetomake");
                print FILE "-";
                close(FILE);

                $filetomake = "$lbdir" . "boarddata/listno$newforumid.cgi";
                open(FILE,">$filetomake");
                close(FILE);
                $filetomake = "$lbdir" . "boarddata/listall$newforumid.cgi";
                open(FILE,">$filetomake");
                close(FILE);

	        open(FILE, ">${lbdir}boarddata/foruminfo$newforumid.cgi");
	        print FILE "%%%%%%\t0\t0\t\t\t\n";
                close(FILE);

                $filetomake = "$dirtomake/.htaccess";
                open(FILE, ">$filetomake");
                print FILE "AuthUserFile /dev/null\n";
                print FILE "AuthGroupFile /dev/null\n";
                print FILE "AuthName DenyViaWeb\n";
                print FILE "AuthType Basic\n";
                print FILE "\n\n\n\n";
                print FILE "<Limit GET>\n";
                print FILE "order allow,deny\n";
                print FILE "deny from all\n";
                print FILE "</Limit>\n";
                close (FILE);

my @molist = split(/\,/,$new_forummoderator);
foreach $_ (@molist){
    chomp $_;
    $_ =~ s/ /\_/g;
    $_ =~ tr/A-Z/a-z/;
    next if ($_ eq "");
    next if (($_ =~ /��Ƹ��/i)||($_ =~ /����/i)||($_ =~ /ȫ�������Ա/i)||($_ =~ /����Ա/i)||($_ =~ /��ʱ��ȱ/i)||($_ =~ /����/i)||($_ =~ /̳��/i));
    my $namenumber = &getnamenumber($_);
    &checkmemfile($_,$namenumber);
    if ((!(-e "${lbdir}$memdir/$namenumber/$_.cgi"))&&(!(-e "${lbdir}$memdir/old/$_.cgi"))) { &winunlock($filetoopen) if ($OS_USED eq "Nt"); &errorout("��̳���������У�$_ ����û� ID �ǲ����ڵģ�");}
}

                $filetomake1 = "$dirtomake/foruminfo.cgi";
                open(FILE,">$filetomake1");
                print FILE "$newforumid\t$new_categoryname\t$new_categorynumber\t$new_forumname\t$new_forumdescription\t$new_forummoderator\t$new_htmlstate\t$new_idmbcodestate\t$new_privateforum\t$new_startnewthreads\t\t\t0\t0\t$new_forumgraphic\t$new_ratings\t$misc\t$new_forumpass\t$new_hiddenforum\t$new_indexforum\t$new_teamlogo\t$new_teamurl\t$new_fgwidth|$new_fgwidth1\t$new_fgheight|$new_fgheight1\t$new_miscad4\t$todayforumpost\t$new_miscad5\t";
                close(FILE);

                $filetoopen = "$lbdir" . "data/allforums.cgi";
#		&winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE, "$filetoopen");
#	        flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

                open(FILE, ">$filetoopen");
                flock(FILE, 2) if ($OS_USED eq "Unix");
                foreach $line (@forums) {
                    chomp $line;
                    ($tempforumno,undef,$tempcategorynumber)=split(/\t/,$line);
                    print FILE "$line\n";
                    if($new_categoryname =~/childforum-[0-9]+/){
                print FILE "$newforumid\t$new_categoryname\t$new_categorynumber\t$new_forumname\t$new_forumdescription\t$new_forummoderator\t$new_htmlstate\t$new_idmbcodestate\t$new_privateforum\t$new_startnewthreads\t\t\t0\t0\t$new_forumgraphic\t$new_ratings\t$misc\t$new_forumpass\t$new_hiddenforum\t$new_indexforum\t$new_teamlogo\t$new_teamurl\t$new_fgwidth|$new_fgwidth1\t$new_fgheight|$new_fgheight1\t$new_miscad4\t$todayforumpost\t$new_miscad5\t\n" if($new_categoryname eq "childforum-$tempforumno");
                $Get=1;
                    }
                    }
                print FILE "$newforumid\t$new_categoryname\t$new_categorynumber\t$new_forumname\t$new_forumdescription\t$new_forummoderator\t$new_htmlstate\t$new_idmbcodestate\t$new_privateforum\t$new_startnewthreads\t\t\t0\t0\t$new_forumgraphic\t$new_ratings\t$misc\t$new_forumpass\t$new_hiddenforum\t$new_indexforum\t$new_teamlogo\t$new_teamurl\t$new_fgwidth|$new_fgwidth1\t$new_fgheight|$new_fgheight1\t$new_miscad4\t$todayforumpost\t$new_miscad5\t\n" if($new_categoryname !~/childforum-[0-9]+/);
                close(FILE);
#	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

	    open(FILE, ">${lbdir}boarddata/forumposts$newforumid.pl");
	    print FILE "\$threads = 0;\n\$posts = 0;\n\$todayforumpost = \"0\";\n1;\n";
            close(FILE);

                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / ������̳���</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>
                ~;

                print "<b>��ϸ����</b><p>\n";
                print "<ul>\n";
                if (-e $dirtomake) {
                print "<li><b>����̳Ŀ¼�Ѿ�����</b><p>\n";
                    }
                    else {
                        print "<li><b>����̳Ŀ¼û�н���</b><p>��鿴�Ƿ�ı���Ŀ¼���ԣ�������Ի� 777 ��<p>\n";
                        }


                $filetoopen = "$dirtomake/index.html";
                if (-e $filetoopen) {
                    print "<li><b>����̳ (index.html) �ļ�����</b><p>\n";
                    }
                    else {
                        print "<li><b>����̳ (index.html) �ļ�û�н���</b><p>��鿴�Ƿ�ı���Ŀ¼���ԣ�������Ի� 777 ��\n";
                        }
                print "$filetoopen<p>\n";
                print "</ul>\n";
&forumjump;
print "</td></tr></table></td></tr></table>";
} ######## end routine

sub warning {
    print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>��ӭ������̳�������� / ɾ����̳</b></td></tr>
<tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>���棡��</b></td></tr>
<tr><td bgcolor=#FFFFFF align=center colspan=2><font color=#333333>�����ȷ��Ҫɾ����̳����ô������������<p>
>> <a href="$thisprog?action=delete&checkaction=yes&forum=$inforum">ɾ����̳�Լ���̳�µ������ļ�</a> <<
</td></tr></table></td></tr></table>
~;
}

sub deleteforum { #start
    my $thistime=time;
    open(FILE, ">>${lbdir}data/baddel.cgi");
    print FILE "$inmembername\t���벻��ʾ\t$ENV{'REMOTE_ADDR'}\t$ENV{'HTTP_X_FORWARDED_FOR'}/$ENV{'HTTP_CLIENT_IP'}\tɾ����̳$forumname\t$thistime\t\n";
    close(FILE);
    undef $thistime;

    opendir (DIRS, "${imagesdir}$usrdir/$inforum");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	chomp $_;
	unlink ("${imagesdir}$usrdir/$inforum/$_");
    }
    unlink ("${imagesdir}$usrdir/$inforum/.htaccess");
    rmdir ("${imagesdir}$usrdir/$inforum");

    opendir (DIRS, "${lbdir}forum$inforum");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	chomp $_;
	unlink ("${lbdir}forum$inforum/$_");
    }
    unlink ("${lbdir}forum$inforum/.htaccess");
    rmdir ("${lbdir}forum$inforum");

    opendir (DIRS, "${lbdir}FileCount/$inforum");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	chomp $_;
	unlink ("${lbdir}FileCount/$inforum/$_");
    }
    unlink ("${lbdir}FileCount/$inforum/.htaccess");
    rmdir ("${lbdir}FileCount/$inforum");

    unlink ("${lbdir}data/news$inforum.cgi");
    unlink ("${lbdir}data/style$inforum.cgi");
    unlink ("${lbdir}boarddata/list$inforum.cgi");
    unlink ("${lbdir}boarddata/listno$inforum.cgi");
    unlink ("${lbdir}boarddata/listall$inforum.cgi");
    unlink ("${lbdir}boarddata/xzb$inforum.cgi");
    unlink ("${lbdir}boarddata/xzbs$inforum.cgi");
    unlink ("${lbdir}boarddata/lastnum$inforum.cgi");
    unlink ("${lbdir}boarddata/ontop$inforum.cgi");
    unlink ("${lbdir}boarddata/jinghua$inforum.cgi");
    unlink ("${lbdir}boarddata/recyclebin$inforum.cgi");
    unlink ("${lbdir}boarddata/adminlog$inforum.cgi");

		    opendir (DIRS, "${lbdir}$saledir");
		    my @files = readdir(DIRS);
		    closedir (DIRS);

		    my @files = grep(/^$inforum\_/i, @files);
		    foreach (@files) {
		        chomp $_;
		        unlink ("${lbdir}$saledir/$_");
    		    }


    $filetoopen = "$lbdir" . "data/allforums.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE,"$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @forums = <FILE>;
    close(FILE);

    open(FILE,">$filetoopen");
    flock(FILE,2) if ($OS_USED eq "Unix");
    foreach (@forums) {
        chomp $_;
	my ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$_);
    	next if ($forumid !~ /^[0-9]+$/);
	if ($forumid ne $inforum) {
            print FILE "$_\n";
        }
    }
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    open(FILE, "${lbdir}boarddata/foruminfo$inforum.cgi");
    ($no, $thdcount, $threadcount, $no) = split(/\t/,<FILE>);
    close(FILE);

    $threadcount = 0 if ($threadcount eq "");
    $thdcount    = 0 if ($thdcount eq "");

    require "$lbdir" . "data/boardstats.cgi";
    $totalthreads = $totalthreads - $thdcount;
    $totalposts   = $totalposts   - $threadcount;

    $filetomake = "$lbdir" . "data/boardstats.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    open(FILE, ">$filetomake");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
    print FILE "\$totalmembers = \'$totalmembers\'\;\n";
    print FILE "\$totalthreads = \'$totalthreads\'\;\n";
    print FILE "\$totalposts = \'$totalposts\'\;\n";
    print FILE "\n1\;";
    close (FILE);
    &winunlock($filetomake) if ($OS_USED eq "Nt");

    unlink ("${lbdir}boarddata/forumposts$inforum.pl");
    unlink ("${lbdir}boarddata/foruminfo$inforum.cgi");

    print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>��ӭ������̳�������� / ɾ����̳���</b></td></tr>
<tr><td bgcolor=#FFFFFF colspan=2><font color=#990000>
<center><b>��̳�ѱ�ɾ��</b></center><p>
���� $thdcount ���ⱻɾ��<p>
���� $threadcount �ظ���ɾ��<p>
</td></tr></table></td></tr></table>
~;
&forumjump;
}

sub editform {

         $filetoopen = "$lbdir" . "data/allforums.cgi";
         open(FILE,"$filetoopen");
         @forums = <FILE>;
         close(FILE);

         foreach $forum (@forums) {
            chomp $forum;
	    next if ($forum eq "");
            ($forumid,$notneeded,$notneeded,$gforumname) = split(/\t/,$forum);
    	    next if ($forumid !~ /^[0-9]+$/);
                if ($forumid eq "$inforum") {
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);
                }
            $forumname[$forumid]="$gforumname";
         }
		if($category=~/childforum-[0-9]+/){
			$category=~s/^childforum-//;
			$categoryn="�༭ '$forumname[$category]' �е�����̳ '$forumname' ";
			$modiii = "<BR><font color=blue>����̳���Զ��̳и���̳�İ�������ע�ⲻҪ�ظ��������</font>";
		}else{
			$categoryn="�༭ '$category' �����е� '$forumname' ��̳";
			$modiii = "";
		}
    ($fgwidth,$fgwidth1) = split(/\|/,$fgwidth);
    ($fgheight,$fgheight1) = split(/\|/,$fgheight);
    
# Present the form to be filled in


        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
        <b>��ӭ������̳�������� / �༭��̳</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>$categoryn</b>
        </td></tr>

        <form action="$thisprog" method="post" enctype="multipart/form-data" name=FORM>
        <input type=hidden name="action" value="doedit">
        <input type=hidden name="forum" value="$inforum">
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳����</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumname" value="$forumname"></td>
        </tr>       
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳������֧�� HTML �﷨</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>   
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳�����������ϣ���ж����������ʹ�� "," (Ӣ�Ķ��ţ��������Ķ���)������<BR><B>����</B>��ɽӥ, ����ȱ</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forummoderator" value="$forummoderator">$modiii</td>
        </tr>
        ~;
        
        $tempoutput = qq~<select name="htmlstate"><option value="on">ʹ��<option value="off">��ʹ��</select>~;
        $tempoutput =~ s/value=\"$htmlstate\"/value=\"$htmlstate\" selected/g;
        
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� HTML ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        ~;
        
        $tempoutput = qq~<select name="idmbcodestate"><option value="on">ʹ��<option value="off">��ʹ��</select>~;
        $tempoutput =~ s/value=\"$idmbcodestate\"/value=\"$idmbcodestate\" selected/g;
        
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� LeoBBS ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        ~;
        
        $tempoutput = qq~<select name="privateforum"><option value="yes">��<option value="no">��</select>~;
        $tempoutput =~ s/value=\"$privateforum\"/value=\"$privateforum\" selected/g;
        if (!$privateforum) { 
            $tempoutput = qq~<select name="privateforum"><option value="yes">��<option value="no" selected>��</select>~;
            }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���Ϊ˽����̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput  ��̳�����ܰ�����Ч
        </td>
        </tr>
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>˽����̳����</b>(ֻ��˽����̳��Ч)</font></td>
        <td bgcolor=#FFFFFF>
       <input type=text size=12 name="forumpass" value="$forumpass" maxlength=20> ��̳�����ܰ�����Ч</td>
        </td>
        </tr>
        ~;
        
        $tempoutput = qq~<select name="hiddenforum"><option value="yes">��<option value="no">��</select>~;
        $tempoutput =~ s/value=\"$hiddenforum\"/value=\"$hiddenforum\" selected/g;
        if (!$hiddenforum) { 
            $tempoutput = qq~<select name="hiddenforum"><option value="yes">��<option value="no" selected>��</select>~;
            }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�������̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        ~;
        
        $tempoutput = qq~<select name="indexforum"><option value="yes">��<option value="no">��</select>~;
        $tempoutput =~ s/value=\"$indexforum\"/value=\"$indexforum\" selected/g;
        if (!$indexforum) { 
            $tempoutput = qq~<select name="indexforum"><option value="yes" selected>��<option value="no" >��</select>~;
            }
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���ʾ��������</b></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        
        ~;
        
        $tempoutput = qq~<select name="startnewthreads"><option value="yes" selected>������̳<option value="all">������̳<option value="follow">������̳<option value="no">������<option value="cert">��֤��̳<option value="onlysub">������̳</select>~;
        $tempoutput =~ s/value=\"$startnewthreads\"/value=\"$startnewthreads\" selected/g;
        
        print qq~
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>1. ������̳-ֻ����ע���Ա����<br>2. ������̳-���������˷���<br>3. ������̳-̳���Ͱ��������ԣ�����ע���û�ֻ�ܻظ�<br>4. ������-ֻ���������̳�����ԺͲ���<br>5. ��֤��̳-��̳���Ͱ����⣬����ע���û�������Ҫ��֤<br>6. ������̳-����ֻ������̳��������̳���������ظ�<br></font></td>
        <td bgcolor=#FFFFFF>
        $tempoutput
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳ͼƬ</b><br>������ͼƬ���ƣ���ͼ������ myimages Ŀ¼�£���������������̳ҳ�����Ϸ�����С������� 160*60 ���ڡ�<BR><b>�벻Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=30 name="forumgraphic" value="$forumgraphic"> 
~;
opendir (DIR, "${imagesdir}myimages");
@thd = readdir(DIR);
closedir (DIR);
        my $myimages="";
        $topiccount = @thd;
        @thd=sort @thd;
        for (my $i=0;$i<$topiccount;$i++){
            next if (($thd[$i] eq ".")||($thd[$i] eq ".."));
            $myimages.=qq~<option value="$thd[$i]">$thd[$i]~;
        }
        $myimages =~ s/value=\"$action\"/value=\"$action\" selected/;        
print qq~
<script>
function select(){
document.FORM.forumgraphic.value=FORM.image.value;
document.bbsimg.src = "$imagesurl/myimages/"+FORM.image.value;}
function select2(){
document.FORM.teamlogo.value=FORM.image2.value;
document.bbsimg.src = "$imagesurl/myimages/"+FORM.image2.value;}
function select3(){
document.bbsimg.src = FORM.addme.value;}
</script>
<select name="image" onChange=select()><option value="blank.gif">ѡ��ͼƬ$myimages</select></td>
        </tr>
	<tr>
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳FLASH�����߶ȡ����</b><br>����ȷ���� FLASH �����ĸ߶ȼ���ȡ�<BR></font></td>
        <td bgcolor=#FFFFFF>
        ��ȣ�<input type=text size=3 name="fgwidth" value="$fgwidth">�����߶ȣ�<input type=text size=3 name="fgwidth1" value="$fgwidth1"></td>
        </tr>
	<tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>����ͼƬ</b>(���û�У��뱣��ԭ��)<br>������ͼƬ���ƣ���ͼ������ myimages Ŀ¼�£���������������ҳ���¡�<BR><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=30 name="teamlogo" value="$teamlogo"> <select name="image2" onChange=select2()><option value="blank.gif">ѡ��ͼƬ$myimages</select></td>
        </tr> 
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>����ͼƬFLASH�����߶ȡ����</b><br>����ȷ���� FLASH �����ĸ߶ȼ���ȡ�<BR></font></td>
        <td bgcolor=#FFFFFF>
        ��ȣ�<input type=text size=3 name="fgheight" value="$fgheight">�����߶ȣ�<input type=text size=3 name="fgheight1" value="$fgheight1"></td>
        </tr>
	<tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�ϴ���̳/����ͼƬ</b><br>������ͼƬ���ƣ���ͼƬ��������̳ͼƬ/����ͼƬ��</font></td>
        <td bgcolor=#FFFFFF>
        <input type="file" size=20 name="addme" onchange="select3()"><br>֧�����ͣ�gif��jpg��bmp��png��swf</td>
        </tr> 
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>������ַ</b>(���û�У��뱣��ԭ��)</td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamurl" value="$teamurl"></td>
        </tr><tr>
        <td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>ͼ��Ԥ��(��֧�� Flash)</b></font><br><IMG border=0 name=bbsimg src="$imagesurl/myimages/blank.gif" align="absmiddle"></td>
        </tr>
        <tr>
        <td bgcolor=#F0F0F0 align=center colspan=2>
        <input type=submit value="�� ��"></form></td></tr></table><center>
        ~;
        print "</td></tr></table>";
} # end route   

##################################################################################
######## Subroutes ( Processing the edit of a forum)


sub doedit {
#	&errorout("������̳�����벻�ܿգ���") if (($new_privateforum eq "yes")&&($new_forumpass eq ""));
	&errorout("�Բ�����̳���ֹ������������ 20 �������ڣ�") if (length($new_forumname) >40);
	&errorout("��̳���ֲ��ܿգ���") if ($new_forumname eq "");
	&errorout("��̳�������ܿգ���") if ($new_forumdescription eq "");
	$new_privateforum = "yes" if ($new_forumpass ne "");

         $filetoopen = "$lbdir" . "data/allforums.cgi";
#         &winlock($filetoopen) if ($OS_USED eq "Nt");
	 open(FILE,"$filetoopen");
#         flock(FILE, 1) if ($OS_USED eq "Unix");
         @forums = <FILE>;
         close(FILE);

         foreach $forum (@forums) {
             chomp $forum;
 	     next if ($forum eq "");
             ($forumid, $notneeded) = split(/\t/,$forum);
    	     next if ($forumid !~ /^[0-9]+$/);
             if ($forumid eq $inforum) {
                 ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc, $forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);
             }
        }

                $editedline = "$inforum\t$category\t$categoryplace\t$new_forumname\t$new_forumdescription\t$new_forummoderator\t$new_htmlstate\t$new_idmbcodestate\t$new_privateforum\t$new_startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$new_forumgraphic\t$new_ratings\t$misc\t$new_forumpass\t$new_hiddenforum\t$new_indexforum\t$new_teamlogo\t$new_teamurl\t$new_fgwidth|$new_fgwidth1\t$new_fgheight|$new_fgheight1\t$new_miscad4\t$todayforumpost\t$new_miscad5\t";
                chomp $editedline;


	&douppics();
	
                mkdir ("${lbdir}FileCount/$newforumid", 0777);
                mkdir ("${imagesdir}$usrdir/$newforumid", 0777);

my @molist = split(/\,/,$new_forummoderator);
foreach $_ (@molist){
    chomp $_;
    $_ =~ s/ /\_/g;
    $_ =~ tr/A-Z/a-z/;
    next if ($_ eq "");
    next if (($_ =~ /��Ƹ��/i)||($_ =~ /����/i)||($_ =~ /ȫ�������Ա/i)||($_ =~ /����Ա/i)||($_ =~ /��ʱ��ȱ/i)||($_ =~ /����/i)||($_ =~ /̳��/i));
    my $namenumber = &getnamenumber($_);
    &checkmemfile($_,$namenumber);
    if ((!(-e "${lbdir}$memdir/$namenumber/$_.cgi"))&&(!(-e "${lbdir}$memdir/old/$_.cgi"))) { 
#    	&winunlock($filetoopen) if ($OS_USED eq "Nt");
    	&errorout("��̳���������У�$_ ����û� ID �ǲ����ڵģ�");
    }
}

                $dirtomake = "$lbdir" . "forum$inforum";
                $filetomake1 = "$dirtomake/foruminfo.cgi";
                open(FILE,">$filetomake1");
                print FILE $editedline;
                close(FILE);

                # Lets re-open the file

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                open(FILE,"$filetoopen");
#                flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

                # Lets remake the file...

                open(FILE,">$filetoopen");
                flock(FILE,2) if ($OS_USED eq "Unix");
                open(FILEBAK, ">$filetoopen.pl");

				foreach $forum (@forums) {
                chomp $forum;
                ($tempforumid,$notneeded) = split(/\t/,$forum);
                    if ($tempforumid eq "$inforum") {
                        print FILE "$editedline\n";
                        print FILEBAK "$editedline\n";
						}
                        else {
                            print FILE "$forum\n";
							print FILEBAK "$forum\n";
                            }
                    }
                close(FILEBAK);
				close (FILE);
#	            &winunlock($filetoopen) if ($OS_USED eq "Nt");


                 print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / �༭��̳���</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>������Ϣ�Ѿ�����</b><p>
                ������趨��ĳ��Ϊ��������������ӹ������ı༭�������ϣ�ʹ����Ϊ������<BR>
                ��ʵ�����û��Ҫ�ġ��������Ӱ�췢�������ֱ��ϵ� '����' ͼ�꣬�ǰ�������ʾ <br>
				'����' ͼ�꣬���Ҳ��ڹ����Ŷ�����ʾ���������ְ���Ȩ����һ���ġ�</font>
                </td></tr></table><center>
                ~;
print "</td></tr></table>";
&forumjump;

            } # end routine

##################################################################################
######## Subroutes ( Add category/forum Form )


sub catform {

# Present the form to be filled in
        print qq~
        <form action="$thisprog" method="post" enctype="multipart/form-data" name=FORM>
        <input type=hidden name="action" value="doaddcategory">
        <input type=hidden name="category" value="$incategory">
        <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
        <b>��ӭ������̳�������� / ���ӷ���(ͬʱ����һ����̳)</b>
        </td></tr>
        <tr>
        
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���ӷ���(ͬʱ����һ����̳)</b>
        </td></tr>


        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��������</b><br>�������·�������</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="categoryname" value="$categoryname"></td>
        </tr>

	<tr>
	<td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>������</b><br>���������˷�����������������ϣ���ж������������ʹ�� "," (Ӣ�Ķ��ţ��������Ķ���)������<BR><B>����</B>��ɽӥ, ����ȱ</font></td> 
        <td bgcolor=#FFFFFF> 
        <input type=text size=40 name="catemods" value="$catemods"></td> 
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>����������̳������<BR>(������� 20 ��������)</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumname" value="$forumname" maxlength=40></td>
        </tr>       
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>����������̳��������֧�� HTML �﷨</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forumdescription" value="$forumdescription"></td>
        </tr>   
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>��������̳�����������ϣ���ж����������ʹ�� "," (Ӣ�Ķ��ţ��������Ķ���)������<BR><B>����</B>��ɽӥ, ����ȱ</font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="forummoderator" value="$forummoderator"></td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� HTML ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="htmlstate">
        <option value="on">ʹ��<option value="off" selected>��ʹ��</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�ʹ�� LeoBBS ��ǩ��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="idmbcodestate">
        <option value="on" selected>ʹ��<option value="off">��ʹ��</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���Ϊ˽����̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="privateforum">
        <option value="yes">��<option value="no" selected>��</select> ��̳�����ܰ�����Ч
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>˽����̳����</b>(ֻ��˽����̳��Ч)</font></td>
        <td bgcolor=#FFFFFF>
       <input type=text size=12 name="forumpass" value="$forumpass" maxlength=20> ��̳�����ܰ�����Ч</td>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ�������̳��</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="hiddenforum">
        <option value="yes">��<option value="no" selected>��</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�Ƿ���ʾ��������</b></font></td>
        <td bgcolor=#FFFFFF>
        <select name="indexforum">
        <option value="yes" selected>��<option value="no" >��</select>
        </td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳����</b><br>1. ������̳-ֻ����ע���Ա����<br>2. ������̳-���������˷���<br>3. ������̳-̳���Ͱ��������ԣ�����ע���û�ֻ�ܻظ�<br>4. ������-ֻ���������̳�����ԺͲ���<br>5. ��֤��̳-��̳���Ͱ����⣬����ע���û�������Ҫ��֤<br>6. ������̳-����ֻ������̳��������̳���������ظ�<br></font></td>
        <td bgcolor=#FFFFFF>
        <select name="startnewthreads">
        <option value="yes" selected>������̳<option value="all">������̳<option value="follow">������̳<option value="no">������<option value="cert">��֤��̳<option value="onlysub">������̳</select>
        </td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳ͼƬ��֧��FLASH��</b><br>������ͼƬ���ƣ���ͼ������ myimages Ŀ¼�£���������������̳ҳ�����Ϸ�����С������� 160*60 ���ڡ�<BR><b>�벻Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=20 name="forumgraphic" value="logo.gif">
~;

opendir (DIR, "${imagesdir}myimages");
@thd = readdir(DIR);
closedir (DIR);
        my $myimages="";
        $topiccount = @thd;
        @thd=sort @thd;
        for (my $i=0;$i<$topiccount;$i++){
            next if (($thd[$i] eq ".")||($thd[$i] eq ".."));
            $myimages.=qq~<option value="$thd[$i]">$thd[$i]~;
        }
        $myimages =~ s/value=\"$action\"/value=\"$action\" selected/;        
print qq~
<script>
function select(){
document.FORM.forumgraphic.value=FORM.image.value;
document.bbsimg.src = "$imagesurl/myimages/"+FORM.image.value;}
function select2(){
document.FORM.teamlogo.value=FORM.image2.value;
document.bbsimg.src = "$imagesurl/myimages/"+FORM.image2.value;}
function select3(){
document.bbsimg.src = FORM.addme.value;}
</script>
<select name="image" onChange=select()><option value="blank.gif">ѡ��ͼƬ$myimages</select></td>
        </tr>

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>��̳FLASH�����߶ȡ����</b><br>����ȷ����FLASH�����ĸ߶ȼ���ȡ�<BR></font></td>
        <td bgcolor=#FFFFFF>
        ��ȣ�<input type=text size=3 name="fgwidth">�����߶ȣ�<input type=text size=3 name="fgwidth1"></td>
        </tr>
               
	<tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>����ͼƬ</b>(���û�У��뱣��ԭ��)<br>������ͼƬ���ƣ���ͼƬ��������������ҳ���¡�<BR><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=20 name="teamlogo" value=""> <select name="image2" onChange=select2()><option value="blank.gif">ѡ��ͼƬ$myimages</select></td>
        </tr> 

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>����ͼƬFLASH�����߶ȡ����</b><br>����ȷ����FLASH�����ĸ߶ȼ���ȡ�<BR></font></td>
        <td bgcolor=#FFFFFF>
        ��ȣ�<input type=text size=3 name="fgheight">�����߶ȣ�<input type=text size=3 name="fgheight1"></td>
        </tr>
         
	<tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>�ϴ���̳/����ͼƬ</b><br>������ͼƬ���ƣ���ͼƬ��������̳ͼƬ/����ͼƬ��</font></td>
        <td bgcolor=#FFFFFF>
        <input type="file" size=20 name="addme" onchange="select3()"><br>֧�����ͣ�gif��jpg��bmp��png��swf</td>
        </tr> 

        <tr>
        <td bgcolor=#FFFFFF width=40%>
        <font color=#333333><b>������ַ</b>(���û�У��뱣��ԭ��)<br>������������̳ͼƬ�ĵ�ַ����</td>
        <td bgcolor=#FFFFFF>
        <input type=text size=40 name="teamurl" value="http://"></td>
        </tr> 
        <td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>ͼ��Ԥ��(��֧�� Flash)</b></font><br><IMG border=0 name=bbsimg src="$imagesurl/myimages/blank.gif" align="absmiddle" onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333"></td>
        </tr>
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
        ~;
        
} # end route   


##################################################################################
######## Subroutes ( Create New cat/forum )


sub doaddcategory {
#		&errorout("������̳�����벻�ܿգ���") if (($new_privateforum eq "yes")&&($new_forumpass eq ""));
		&errorout("�Բ�����̳���ֹ������������ 20 �������ڣ�") if (length($new_forumname) >40);
		&errorout("��̳���ֲ��ܿգ���") if ($new_forumname eq "");
		&errorout("��̳�������ܿգ���") if ($new_forumdescription eq "");
		&errorout("��̳����ܿգ���") if ($new_categoryname eq "");

	&douppics();
	
               my @catemolist = split(/\,/,$new_catemods); 
               foreach(@catemolist){ 
               chomp $_; 
               $_ =~ s/ /\_/g; 
               $_ =~ tr/A-Z/a-z/; 
               next if ($_ eq ""); 
               my $namenumber = &getnamenumber($_);
		&checkmemfile($_,$namenumber);
               if ((!(-e "${lbdir}$memdir/$namenumber/$_.cgi"))&&(!(-e "${lbdir}$memdir/old/$_.cgi"))) {&errorout("�����������У�$_ ����û� ID �ǲ����ڵģ�"); } 
               }

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                open(FILE, "$filetoopen");
                @forums = <FILE>;
                close(FILE);

                foreach (@forums) {
                    ($forumid, $binit) = split(/\t/,$_);
                    if ($forumid > $high) { $high = $forumid; }
                    }

                $high++;

                $newforumid = $high;

                $dirtomake = "$lbdir" . "forum$newforumid";
                mkdir ("$dirtomake", 0777);

                $dirtomake1 = "$lbdir" . "FileCount/$newforumid";
                mkdir ("$dirtomake1", 0777);

                $filetomake = "$dirtomake1/index.html";
                open(FILE,">$filetomake");
                print FILE "-";
                close(FILE);

                $dirtomake1 = "$imagesdir" . "$usrdir/$newforumid";
                mkdir ("$dirtomake1", 0777);

                $filetomake = "$dirtomake1/index.html";
                open(FILE,">$filetomake");
                print FILE "-";
                close(FILE);

                $filetomake = "$dirtomake/index.html";
                open(FILE,">$filetomake");
                print FILE "-";
                close(FILE);

                $filetomake = "$lbdir" . "boarddata/listno$newforumid.cgi";
                open(FILE,">$filetomake");
                close(FILE);
                $filetomake = "$lbdir" . "boarddata/listall$newforumid.cgi";
                open(FILE,">$filetomake");
                close(FILE);

	        open(FILE, ">${lbdir}boarddata/foruminfo$newforumid.cgi");
	        print FILE "%%%%%%\t0\t0\t\t\t\n";
                close(FILE);

                $filetomake = "$dirtomake/.htaccess";
                open(FILE, ">$filetomake");
                print FILE "AuthUserFile /dev/null\n";
                print FILE "AuthGroupFile /dev/null\n";
                print FILE "AuthName DenyViaWeb\n";
                print FILE "AuthType Basic\n";
                print FILE "\n\n\n\n";
                print FILE "<Limit GET>\n";
                print FILE "order allow,deny\n";
                print FILE "deny from all\n";
                print FILE "</Limit>\n";
                close (FILE);

my @molist = split(/\,/,$new_forummoderator);
foreach $_ (@molist){
    chomp $_;
    $_ =~ s/ /\_/g;
    $_ =~ tr/A-Z/a-z/;
    next if ($_ eq "");
    next if (($_ =~ /��Ƹ��/i)||($_ =~ /����/i)||($_ =~ /ȫ�������Ա/i)||($_ =~ /����Ա/i)||($_ =~ /��ʱ��ȱ/i)||($_ =~ /����/i)||($_ =~ /̳��/i));
    my $namenumber = &getnamenumber($_);
    &checkmemfile($_,$namenumber);
    if ((!(-e "${lbdir}$memdir/$namenumber/$_.cgi"))&&(!(-e "${lbdir}$memdir/old/$_.cgi"))) { &winunlock($filetoopen) if ($OS_USED eq "Nt"); &errorout("��̳���������У�$_ ����û� ID �ǲ����ڵģ�"); }
}

                $filetomake1 = "$dirtomake/foruminfo.cgi";
                open(FILE,">$filetomake1");
                print FILE "$newforumid\t$new_categoryname\t$incategory\t$new_forumname\t$new_forumdescription\t$new_forummoderator\t$new_htmlstate\t$new_idmbcodestate\t$new_privateforum\t$new_startnewthreads\t\t\t0\t0\t$new_forumgraphic\t$new_ratings\t$misc\t$new_forumpass\t$new_hiddenforum\t$new_indexforum\t$new_teamlogo\t$new_teamurl\t$new_fgwidth|$new_fgwidth1\t$new_fgheight|$new_fgheight1\t$new_miscad4\t$todayforumpost\t$new_miscad5\t";
                close(FILE);

                $filetoopen = "$lbdir" . "data/allforums.cgi";
#	        &winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE, "$filetoopen");
#                flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

                open(FILE, ">$filetoopen");
#               flock(FILE, 2) if ($OS_USED eq "Unix");
                foreach $line (@forums) {
                    chomp $line;
                    print FILE "$line\n";
                    }
                print FILE "$newforumid\t$new_categoryname\t$incategory\t$new_forumname\t$new_forumdescription\t$new_forummoderator\t$new_htmlstate\t$new_idmbcodestate\t$new_privateforum\t$new_startnewthreads\t\t\t0\t0\t$new_forumgraphic\t$new_ratings\t$misc\t$new_forumpass\t$new_hiddenforum\t$new_indexforum\t$new_teamlogo\t$new_teamurl\t$new_fgwidth|$new_fgwidth1\t$new_fgheight|$new_fgheight1\t$new_miscad4\t$todayforumpost\t$new_miscad5\t";
                close(FILE);
#	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

               $catefiletoopen = "$lbdir" . "boarddata/catemod$incategory.cgi"; 
               open(CATEFILE,">$catefiletoopen"); 
               print CATEFILE "$new_catemods\n"; 
               close(CATEFILE);

	    open(FILE, ">${lbdir}boarddata/forumposts$newforumid.pl");
	    print FILE "\$threads = 0;\n\$posts = 0;\n\$todayforumpost = \"0\";\n1;\n";
            close(FILE);

                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / ���ӷ���(ͬʱ����һ����̳)���</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>
                ~;

                print "<b>��ϸ��Ϣ��</b><p>\n";
                print "<ul>\n";
                if (-e $dirtomake) {
                print "<li><b>�µķ������̳�Ѿ�����</b><p>\n";
                    }
                    else {
                        print "<li><b>�µķ������̳û�н���</b><p>��鿴�Ƿ�ı���Ŀ¼���ԣ�������Ի� 777 ��<p>\n";
                        }


                $filetoopen = "$dirtomake/index.html";
                if (-e $filetoopen) {
                    print "<li><b>����̳ (index.html) �ļ�����</b><p>\n";
                    }
                    else {
                        print "<li><b>����̳ (index.html) �ļ�û�н���</b><p>��鿴�Ƿ�ı���Ŀ¼���ԣ�������Ի� 777 ��<p>\n";
                        }
                print "$filetoopen<p>\n";
                print "</ul>\n";

print "</td></tr></table></td></tr></table>";
&forumjump;
&writecatemod;

} # end routine


##################################################################################
######## Subroutes ( Edit Category Name )


sub editcatname {


        if ($checkaction ne "yes") {

            # Grab the line to edit.

            $filetoopen = "$lbdir" . "data/allforums.cgi";
#    	    &winlock($filetoopen) if ($OS_USED eq "Nt");
            open(FILE,"$filetoopen");
#            flock(FILE, 1) if ($OS_USED eq "Unix");
            @forums = <FILE>;
            close(FILE);
#            &winunlock($filetoopen) if ($OS_USED eq "Nt");

            foreach $forum (@forums) {
            chomp $forum;
 	    next if ($forum eq "");
                ($tempno, $category, $categoryplace) = split(/\t/,$forum);
    	    	next if ($tempno !~ /^[0-9]+$/);
                    if ($incategory eq "$categoryplace" && $category !~/^childforum-[0-9]+/) {
                        ($trash, $categoryname, $notneeded) = split(/\t/,$forum);
                        }
                    }

            # Present the form to be filled in
               $catefiletoopen = "$lbdir" . "boarddata/catemod$incategory.cgi"; 
               open(CATEFILE,"$catefiletoopen"); 
               $catemods =<CATEFILE>;
               close(CATEFILE);


            print qq~
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="editcatname">
            <input type=hidden name="category" value="$incategory">
            <input type=hidden name="checkaction" value="yes">
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>��ӭ������̳�������� / �༭��������</b>
            </td></tr>
            <tr>

            <tr>
            <td bgcolor=#EEEEEE align=center colspan=2>
            <font color=#990000><b>�༭ '$categoryname' ���������</b>
            </td></tr>


            <tr>
            <td bgcolor=#FFFFFF width=40%>
            <font color=#333333><b>��������</b><br>�������������</font></td>
            <td bgcolor=#FFFFFF>
            <input type=text size=40 name="categoryname" value="$categoryname"></td>
            </tr>
            <tr> 
            <td bgcolor=#FFFFFF width=40%> 
            <font color=#333333><b>������</b><br>���������˷�����������������ϣ���ж������������ʹ�� "," (Ӣ�Ķ��ţ��������Ķ���)������<BR><B>����</B>��ɽӥ, ����ȱ</font></td> 
            <td bgcolor=#FFFFFF> 
            <input type=text size=40 name="catemods" value="$catemods"></td> 
            </tr>

            <tr>
            <td bgcolor=#FFFFFF align=center colspan=2>
            <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
            ~;
            } # end if

            else {

                # Grab the lines to change.
               my @catemolist = split(/\,/,$new_catemods); 
               foreach(@catemolist){ 
               chomp $_; 
               $_ =~ s/ /\_/g; 
               $_ =~ tr/A-Z/a-z/; 
               next if ($_ eq ""); 
	       my $namenumber = &getnamenumber($_);
	       &checkmemfile($_,$namenumber);
               if ((!(-e "${lbdir}$memdir/$namenumber/$_.cgi"))&&(!(-e "${lbdir}$memdir/old/$_.cgi"))) { &winunlock($filetoopen) if ($OS_USED eq "Nt"); &errorout("�����������У�$_ ����û� ID �ǲ����ڵģ�"); } 
               }

                $filetoopen = "$lbdir" . "data/allforums.cgi";
#	        &winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE,"$filetoopen");
#	        flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

                # Lets remake the file with the new info

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                open(FILE,">$filetoopen");
                flock(FILE,2) if ($OS_USED eq "Unix");
                foreach $forum (@forums) {
                    chomp $forum;
		    next if ($forum eq "");
                    ($tempno, $category, $categorynumber) = split(/\t/,$forum);
    	    	    next if ($tempno !~ /^[0-9]+$/);
                    if ($incategory eq "$categorynumber" && $category !~/^childforum-[0-9]+/) {
                        ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);
                        $linetochange = "$forumid\t$new_categoryname\t$incategory\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t";
                        chomp $linetochange;
                        print FILE "$linetochange\n";
              	  	$dirtomake = "$lbdir" . "forum$forumid";
	                $filetomake1 = "$dirtomake/foruminfo.cgi";
          	        open(FILE1,">$filetomake1");
                        print FILE1 $linetochange;
                	close(FILE1);
                        $forumname = ""; $forumdescription = ""; $forummoderator = ""; $lastposter = ""; $lastposttime = ""; $threads = ""; $posts = ""; $forumgraphic = ""; $miscad2 = "";
                    }
                    else {
                        print FILE "$forum\n";
                    }
                }
                close (FILE);
#	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

               $catefiletoopen = "$lbdir" . "boarddata/catemod$incategory.cgi"; 
               open(CATEFILE,">$catefiletoopen"); 
               print CATEFILE "$new_catemods\n"; 
               close(CATEFILE);

                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / �༭�������ƽ��</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>������Ϣ�Ѿ��ɹ�����</b>
                </td></tr></table></td></tr></table>
                ~;
&forumjump;
&writecatemod;

                } # end else

            } # end routine


##################################################################################
######## Subroutes ( Edit Category Name )


sub reordercats {


        if ($checkaction ne "yes") {

            print qq~
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="reordercategories">
            <input type=hidden name="checkaction" value="yes">
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>��ӭ������̳�������� / ��̳������������</b>
            </td></tr>
            <tr><td bgcolor=#FFFFFF" colspan=3><font color=#333333>
            <b>ע�����</b><br><br>
            �ڴ������Խ���̳�����������򡣷��ཫ��������������ʾ��<BR><BR><b>1 ��ʾ��Ϊ��һ���࣬����ʾ����ǰ��</b>��<br><br>
            <b>�ύ֮ǰ����ϸ����������ã�����֤û���ظ����֣����ظ����ᵼ���еķ����޷���ʾ��</b><br><br>
            <b>������ע�ⲻҪ��ȫ�Ǻ��ֵ����֣����ұ������0��</b><br><br>
            </td></tr>
            ~;

            $filetoopen = "$lbdir" . "data/allforums.cgi";
#	    &winlock($filetoopen) if ($OS_USED eq "Nt");
            open(FILE, "$filetoopen");
#	    flock(FILE, 1) if ($OS_USED eq "Unix");
            @forums = <FILE>;
            close(FILE);
#	    &winunlock($filetoopen) if ($OS_USED eq "Nt");

	    $a=0;
            foreach $forum (@forums) { #start foreach @forums
		$a  = sprintf("%09d",$a);
                chomp $forum;
                ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);
		$categoryplace  = sprintf("%09d",$categoryplace);
                $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t");
                push (@rearrangedforums, $rearrange);
		$a++;
            } # end foreach (@forums)

            @finalsortedforums = sort(@rearrangedforums);

            foreach $sortedforums (@finalsortedforums) { #start foreach @finalsortedforums
                ($categoryplace,my $a, $category, $forumgraphic, $miscad2, $misc, $forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$sortedforums);
        	$categoryplace  = sprintf("%01d",$categoryplace);

                if ($categoryplace ne $lastcategoryplace) { #start if $categoryplace
                    print qq~
                    <tr>
                    <td bgcolor=#FFFFFF width=40%><font color=#333333>
                    <b>-=> $category</b></font></td>
                    <td bgcolor=#FFFFFF><font color=#333333>����λ�� [ <B>$categoryplace</B> ]���������µ������Ա�����<input type=text size=4 maxlength=2 name="$categoryplace" value="$categoryplace">
                    </td></tr>
                    ~;
                    } # end if

                    $lastcategoryplace = $categoryplace;

                 } # end foreach



                    print qq~
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <BR><input type=submit value="�� ��"></td></form></tr></table></td></tr></table>
                    ~;

            } # end if


            else {

                # Grab the lines to change.

                $filetoopen = "$lbdir" . "data/allforums.cgi";
#		&winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE,"$filetoopen");
#	        flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

                foreach $forum (@forums) {
                    chomp $forum;
	 	    next if ($forum eq "");
                    ($tempno, $notneeded, $categorynumber) = split(/\t/,$forum);
    	    	    next if ($tempno !~ /^[0-9]+$/);
    	    	    chomp $PARAM{$categorynumber};
                    if (($PARAM{$categorynumber} !~ /^[0-9]+$/)||($PARAM{$categorynumber} < 0)) {

                	print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / �༭�������ƽ��</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=red><b>�������������д����뷵���������ټ�����</b>
                </td></tr></table></td></tr></table>
                ~;
			exit;
                    }
		}


                $filetoopen = "$lbdir" . "data/allforums.cgi";
                open(FILE,">$filetoopen");
                flock(FILE,2) if ($OS_USED eq "Unix");
                foreach $forum (@forums) {
                    chomp $forum;
	 	    next if ($forum eq "");
                    ($tempno, $notneeded, $categorynumber) = split(/\t/,$forum);
    	    	    next if ($tempno !~ /^[0-9]+$/);
                    $newid = $PARAM{$categorynumber};
                    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);
                    print FILE "$forumid\t$category\t$newid\t$forumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t\n";
                }

                close (FILE);
#	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

foreach (@params) {
$catf = "${lbdir}boarddata/catemod$_.cgi";
if (-e $catf) { rename ($catf, "${catf}.pl"); }
$cattop = "${lbdir}boarddata/catontop$_.cgi"; 
if (-e $cattop) { rename($cattop,"$cattop.pl"); } 
}
foreach (@params) {
$catf="${lbdir}boarddata/catemod$_.cgi.pl";
if (-e $catf) {rename ($catf,"${lbdir}boarddata/catemod$PARAM{$_}.cgi");}
$cattop = "${lbdir}boarddata/catontop$_.cgi.pl"; 
if (-e $cattop) {rename ($cattop,"${lbdir}boarddata/catontop$PARAM{$_}.cgi");}
}

                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / �༭�������ƽ��</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>������Ϣ�Ѿ��ɹ�����</b>
                </td></tr></table></td></tr></table>
                ~;
&forumjump;
&writecatemod;
                } # end else


} # end routine

sub reorder {


        if ($checkaction ne "yes") {

            print qq~
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="reorder">
            <input type=hidden name="checkaction" value="yes">
            <input type=hidden name="category" value="$inforum">

            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>��ӭ������̳�������� / ��̳��������</b>
            </td></tr>
            <tr><td bgcolor=#FFFFFF" colspan=3><font color=#333333>
            <b>ע�����</b><br><br>
            �ڴ������Խ�����̳��������<br>����̳���Զ�����˳�����¸ı�˳��ͷ�������
            </td></tr>~;
            $filetoopen = "$lbdir" . "data/allforums.cgi";
#         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
#         flock(FILE, 1) if ($OS_USED eq "Unix");
         @forums = <FILE>;
         close(FILE);
#         &winunlock($filetoopen) if ($OS_USED eq "Nt");


         foreach $forum (@forums) {
            chomp $forum;
	    next if ($forum eq "");
            ($forumid,$category,$notneeded,$notneeded) = split(/\t/,$forum);
    	    next if ($forumid !~ /^[0-9]+$/);
                if ($forumid eq $inforum) {
                    ($forumid, $mycategory, $mycategoryplace, $myforumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);
                    last;
                }
         }
         $childmove=($mycategory =~/^childforum-[0-9]+$/)?1:0;
            print qq~
            <tr><td><input type="radio" name="movetype" value="tomove" checked>����̳ <font color=red>$myforumname</font> �Ƶ���̳
            <select name="forum">
            ~;



$a=0;
foreach my $forum (@forums) { #start foreach @forums
    $a  = sprintf("%09d",$a);
    chomp $forum;
    next if ($forum eq "");
    (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription) = split(/\t/,$forum);
    next if ($forumid !~ /^[0-9]+$/);
    next if ($categoryplace !~ /^[0-9]+$/);
    next if ($forumid eq $inforum);
#    next if ($category =~/childforum-[0-9]+/);
    $categoryplace  = sprintf("%09d",$categoryplace);
    $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t");
    push (@rearrangedforums, $rearrange);
    $a++;
}

@finalsortedforums = sort (@rearrangedforums);
foreach my $sortedforums (@finalsortedforums) {
    (my $categoryplace,my $a, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $miscad2, my $misc, my $forumpass, my $hiddenforum, my $indexforum,my $teamlogo,my $teamurl,my $fgwidth,my $fgheight,my $miscad4,my $todayforumpost,my $miscad5) = split(/\t/,$sortedforums);
    $categoryplace  = sprintf("%01d",$categoryplace);
    if ($category eq $mycategory){
	$jumphtml3 = "<option value=\"top$categoryplace\">������̳�б��\n" if ($jumphtml3 eq "");
        $jumphtml3 .= "<option value=\"$forumid\">��$forumname\n";
    }
#    else {$jumphtml3 .= "<option value=\"$forumid\">��$category eq $mycategory\n"; }
    next if ($category =~/childforum-[0-9]+/);

    if ($categoryplace ne $lastcategoryplace) {
        $jumphtml .= "<option value=\"top$forumid\" style=background-color:$titlecolor>��$category\n";
    }
    if (($forumname ne $myforumname)||($categoryplace ne $mycategoryplace)){
        $jumphtml .= "<option value=\"$forumid\">����$forumname\n";
    }

    $lastcategoryplace = $categoryplace;
}
$jumphtml .= qq~</select>\n~;
$jumphtml2=$jumphtml;
$jumphtml2=~s/<option value="top(.+?)" style=background-color:$titlecolor>��(.+?)\n//g;
$jumphtml2=~s/����//g;




                    print qq~
                    $jumphtml�£������Զ��ı�������ԡ�
                   </td></tr>
~;
                   	if($childmove){
                    print qq~
                   	<tr><td><input type="radio" name="movetype" value="movechild">������̳ <font color=red>$myforumname</font> �Ƶ�<select name="indexforum">$jumphtml3</select>�¡�</td></tr>~;
                   	}
                    print qq~                   	<tr><td><input type="radio" name="movetype" value="tochild">����̳ <font color=red>$myforumname</font> ��Ϊ<select name="cforum">$jumphtml2������̳�������Զ��ı�������ԡ�</td></tr>
                   	<tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <BR><input type=submit value="�� ��"></td></form></tr></table></td></tr></table>
                    ~;

            } # end if


            else {

                # Grab the lines to change.

                $filetoopen = "$lbdir" . "data/allforums.cgi";
#		&winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE,"$filetoopen");
#	        flock(FILE, 1) if ($OS_USED eq "Unix");
                @forums = <FILE>;
                close(FILE);

            foreach $forum (@forums) {
            	chomp $forum;
	    	next if ($forum eq "");
            	($forumid,$category,$categoryplace,$notneeded) = split(/\t/,$forum);
    	    	next if ($forumid !~ /^[0-9]+$/);
    	    	next if ($categoryplace !~ /^[0-9]+$/);
                if ($forumid eq "$incategory") {
                    ($oldforumid, $oldcategory, $oldcategoryplace, $oldmyforumname, $oldforumdescription, $oldforummoderator ,$oldhtmlstate ,$oldidmbcodestate ,$oldprivateforum, $oldstartnewthreads ,$oldlastposter ,$oldlastposttime, $oldthreads, $oldposts, $oldforumgraphic, $oldratings, $oldmisc,$oldforumpass,$oldhiddenforum,$oldindexforum,$oldteamlogo,$oldteamurl, $oldfgwidth, $oldfgheight, $oldmiscad4, $oldtodayforumpostno, $oldmiscad5) = split(/\t/,$forum);
                }elsif($category eq "childforum-$incategory"){
                push(@childforum,$forum);
                }elsif($category eq "childforum-$inforum"){
                push(@ochildforum,$forum);
                }
            }
				chomp @childforum,@ochildforum;

                $filetoopen = "$lbdir" . "data/allforums.cgi";
                open(FILE,">$filetoopen");
#                flock(FILE,2) if ($OS_USED eq "Unix");
    	    	   if($inmovetype eq "tomove"){
                foreach $forum (@forums) {
                    chomp $forum;
	 	    next if ($forum eq "");
                    ($forumid, $category, $categoryplace, $myforumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);
    	    	    next if ($forumid !~ /^[0-9]+$/);
                    if ($forumid ne $incategory && $category ne "childforum-$incategory" && $category ne "childforum-$inforum"){
                	if ($forumid eq $inforum){
                  	  print FILE "$forum\n";
                	  foreach(@ochildforum){
                  	  print FILE "$_\n";
                	  }
                  	  print FILE "$oldforumid\t$category\t$categoryplace\t$oldmyforumname\t$oldforumdescription\t$oldforummoderator\t$oldhtmlstate\t$oldidmbcodestate\t$oldprivateforum\t$oldstartnewthreads\t$oldlastposter\t$oldlastposttime\t$oldthreads\t$oldposts\t$oldforumgraphic\t$oldratings\t$oldmisc\t$oldforumpass\t$oldhiddenforum\t$oldindexforum\t$oldteamlogo\t$oldteamurl\t$oldfgwidth\t$oldfgheight\t$oldmiscadd4\t$oldtodayforumpostno\t$oldmiscad5\t\n";

	                  $filetomake1 = "$lbdir" . "forum$oldforumid/foruminfo.cgi";
          	          open(FILE1,">$filetomake1");
                  	  print FILE1 "$oldforumid\t$category\t$categoryplace\t$oldmyforumname\t$oldforumdescription\t$oldforummoderator\t$oldhtmlstate\t$oldidmbcodestate\t$oldprivateforum\t$oldstartnewthreads\t$oldlastposter\t$oldlastposttime\t$oldthreads\t$oldposts\t$oldforumgraphic\t$oldratings\t$oldmisc\t$oldforumpass\t$oldhiddenforum\t$oldindexforum\t$oldteamlogo\t$oldteamurl\t$oldfgwidth\t$oldfgheight\t$oldmiscadd4\t$oldtodayforumpostno\t$oldmiscad5\t";
                	  close(FILE1);
                	  foreach(@childforum){
                	  	  @childdata=split(/\t/,$_);
                	  	  chomp @childdata;
                	  	  $childdata[2]=$categoryplace;
                	  	  $childdata=join("\t",@childdata);
                  	  print FILE "$childdata\t\n";
	                  $filetomake1 = "$lbdir" . "forum$childdata[1]/foruminfo.cgi";
          	          open(FILE1,">$filetomake1");
                  	  print FILE1 "$childdata\t";
                	  close(FILE1);
                	  }
         		}
              		elsif ("top$forumid" eq $inforum) {
                	  print FILE "$oldforumid\t$category\t$categoryplace\t$oldmyforumname\t$oldforumdescription\t$oldforummoderator\t$oldhtmlstate\t$oldidmbcodestate\t$oldprivateforum\t$oldstartnewthreads\t$oldlastposter\t$oldlastposttime\t$oldthreads\t$oldposts\t$oldforumgraphic\t$oldratings\t$oldmisc\t$oldforumpass\t$oldhiddenforum\t$oldindexforum\t$oldteamlogo\t$oldteamurl\t$oldfgwidth\t$oldfgheight\t$oldmiscadd4\t$oldtodayforumpostno\t$oldmiscad5\t\n";
	                  $filetomake1 = "$lbdir" . "forum$oldforumid/foruminfo.cgi";
          	          open(FILE1,">$filetomake1");
                	  print FILE1 "$oldforumid\t$category\t$categoryplace\t$oldmyforumname\t$oldforumdescription\t$oldforummoderator\t$oldhtmlstate\t$oldidmbcodestate\t$oldprivateforum\t$oldstartnewthreads\t$oldlastposter\t$oldlastposttime\t$oldthreads\t$oldposts\t$oldforumgraphic\t$oldratings\t$oldmisc\t$oldforumpass\t$oldhiddenforum\t$oldindexforum\t$oldteamlogo\t$oldteamurl\t$oldfgwidth\t$oldfgheight\t$oldmiscadd4\t$oldtodayforumpostno\t$oldmiscad5\t";
                	  close(FILE1);
                	  foreach(@childforum){
                	  	  @childdata=split(/\t/,$_);
                	  	  chomp @childdata;
                	  	  $childdata[2]=$categoryplace;
                	  	  $childdata=join("\t",@childdata);
                  	  print FILE "$childdata\t\n";
	                  $filetomake1 = "$lbdir" . "forum$childdata[1]/foruminfo.cgi";
          	          open(FILE1,">$filetomake1");
                  	  print FILE1 "$childdata\t";
                	  close(FILE1);
                	  }
                	  print FILE "$forum\n";
              		}
             	    	else {
        			print FILE "$forum\n";
               	    	}
        	    }
        	}
    	    	   }
elsif($inmovetype eq "movechild"){
$newforuminfo="$oldforumid\t$oldcategory\t$oldcategoryplace\t$oldmyforumname\t$oldforumdescription\t$oldforummoderator\t$oldhtmlstate\t$oldidmbcodestate\t$oldprivateforum\t$oldstartnewthreads\t$oldlastposter\t$oldlastposttime\t$oldthreads\t$oldposts\t$oldforumgraphic\t$oldratings\t$oldmisc\t$oldforumpass\t$oldhiddenforum\t$oldindexforum\t$oldteamlogo\t$oldteamurl\t$oldfgwidth\t$oldfgheight\t$oldmiscadd4\t$oldtodayforumpostno\t$oldmiscad5\t\n";
                foreach $forum (@forums) {
                    chomp $forum;
                    next if ($forum eq "");
					($forumid,my $category, my $categoryplace, undef) = split(/\t/,$forum);
					next if ($forumid !~ /^[0-9]+$/);
					next if ($forumid eq $oldforumid);
					print FILE "$forum\n";
					if("top$categoryplace" eq $new_indexforum && $writeinfo ne 1) { print FILE $newforuminfo; $writeinfo = 1; }
					print FILE $newforuminfo if($forumid eq $new_indexforum);
                }
    	    	   }    	    	   
    	    	   else{
                foreach $forum (@forums) {
                    chomp $forum;
	 	    next if ($forum eq "");
                    ($forumid, $category, $categoryplace, $myforumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);
    	    	    next if ($forumid !~ /^[0-9]+$/);
                    if ($forumid ne $incategory){
                	if ($forumid eq $incforum){
                  	  print FILE "$forum\n";
                  	  print FILE "$oldforumid\tchildforum-$incforum\t$categoryplace\t$oldmyforumname\t$oldforumdescription\t$oldforummoderator\t$oldhtmlstate\t$oldidmbcodestate\t$oldprivateforum\t$oldstartnewthreads\t$oldlastposter\t$oldlastposttime\t$oldthreads\t$oldposts\t$oldforumgraphic\t$oldratings\t$oldmisc\t$oldforumpass\t$oldhiddenforum\t$oldindexforum\t$oldteamlogo\t$oldteamurl\t$oldfgwidth\t$oldfgheight\t$oldmiscadd4\t$oldtodayforumpostno\t$oldmiscad5\t\n";

                	  $dirtomake = "$lbdir" . "forum$oldforumid";
	                  $filetomake1 = "$dirtomake/foruminfo.cgi";
          	          open(FILE1,">$filetomake1");
                  	  print FILE1 "$oldforumid\tchildforum-$incforum\t$categoryplace\t$oldmyforumname\t$oldforumdescription\t$oldforummoderator\t$oldhtmlstate\t$oldidmbcodestate\t$oldprivateforum\t$oldstartnewthreads\t$oldlastposter\t$oldlastposttime\t$oldthreads\t$oldposts\t$oldforumgraphic\t$oldratings\t$oldmisc\t$oldforumpass\t$oldhiddenforum\t$oldindexforum\t$oldteamlogo\t$oldteamurl\t$oldfgwidth\t$oldfgheight\t$oldmiscadd4\t$oldtodayforumpostno\t$oldmiscad5\t";
                	  close(FILE1);
                	}elsif($category eq "childforum-$oldforumid"){
                  	  print FILE "$forumid\tchildforum-$incforum\t$categoryplace\t$myforumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t\n";

                	  $dirtomake = "$lbdir" . "forum$forumid";
	                  $filetomake1 = "$dirtomake/foruminfo.cgi";
          	          open(FILE1,">$filetomake1");
                  	  print FILE1 "$forumid\tchildforum-$incforum\t$categoryplace\t$myforumname\t$forumdescription\t$forummoderator\t$htmlstate\t$idmbcodestate\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$forumgraphic\t$miscad2\t$misc\t$forumpass\t$hiddenforum\t$indexforum\t$teamlogo\t$teamurl\t$fgwidth\t$fgheight\t$miscad4\t$todayforumpost\t$miscad5\t";
                	  close(FILE1);
                	}else {
        			print FILE "$forum\n";
                	}
                    }
                }
    	    	   }

                close (FILE);
#	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / ����̳�������ƽ��</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>������Ϣ�Ѿ��ɹ�����</b>
                </td></tr></table></td></tr></table>
                ~;
&forumjump;

                } # end else


}

sub errorout {
    print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>��ӭ������̳�������� / ��������</b></td></tr>
<tr><td bgcolor=#FFFFFF colspan=2><font color=#333333><b>$_[0]</b></td></tr></table></td></tr></table>
~;
    exit;
}

sub forumjump {
    unlink "${lbdir}wap/leoM.cgi";
    my $hidden;
    $jumphtml .= qq~<SCRIPT LANGUAGE="JavaScript">
function surfto1(list){
var myindex1  = document.jump.selectedIndex;
if (myindex1 != 0){
var URL = document.jump.jumpto.options[document.jump.jumpto.selectedIndex].value;
top.location.href = URL; target = '_self';
}}
</SCRIPT>
<form action="forums.cgi" method="post" name="jump">
<select name="jumpto" onchange="surfto1(this)">
<option value="leobbs.cgi">��ת��̳��...</option>
~;

	open(FILE, "${lbdir}data/allforums.cgi");
	sysread(FILE, my $forums,(stat(FILE))[7]);
	close(FILE);
        $forums =~ s/\r//isg;
	@forums = split (/\n/,$forums);

    $a=0;
    @rearrangedforums=();
    foreach my $forum (@forums) { #start foreach @forums
	$a  = sprintf("%09d",$a);
	chomp $forum;
	next if ($forum eq "");
	(my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription, my $tmp , $tmp , $tmp , $tmp,  $tmp , $tmp , $tmp,  $tmp,  $tmp,  $tmp, $tmp, $tmp, $tmp,my $hiddenforum,$tmp,$tmp,$tmp, $tmp, $tmp, $tmp, $tmp, $tmp) = split(/\t/,$forum);
	next if ($forumid !~ /^[0-9]+$/);
	next if ($categoryplace !~ /^[0-9]+$/);
	$categoryplace  = sprintf("%09d",$categoryplace);
	$rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$forumid\t$forumgraphic\t$miscad2\t$forumpass\t$hiddenforum\t$indexforum\t");
	push (@rearrangedforums, $rearrange);
	$a++;
    }

    @finalsortedforums = sort (@rearrangedforums);
$outputbutton = "";
foreach my $sortedforums (@finalsortedforums) {
    (my $categoryplace, my $a, my $category, my $forumname, my $forumdescription, my $forumid, my $forumgraphic, my $miscad2, my $forumpass, my $hiddenforum, my $indexforum) = split(/\t/,$sortedforums);
    $categoryplace  = sprintf("%01d",$categoryplace);
    if ($categoryplace ne $lastcategoryplace) {
    	    $jumphtml .= "<option value=\"category.cgi?category=$categoryplace\" style=background-color:\$titlecolor>��$category\n</option>";
#            $jumphtml .= "<option value=\"forums.cgi?forum=$forumid\" style=background-color:\$titlecolor>��$category\n</option>";
    }
    if ($hiddenforum eq "yes"){ $hidden="(����)"; }else{ $hidden=""; } 
    if ($category !~ /^childforum-[0-9]+/) {
	if ($hidden ne "") {
	    $jumphtml .= "<!--h <option value=\"forums.cgi?forum=$forumid\">��|-$forumname$hidden\n</option> -->";
	    $outputbutton .= "<!--h <option value=\"$forumid\">��|-$forumname$hidden\n</option> -->";
	    $fname.="\$fname$forumid=\"$forumname\";\n";
	} else {
	    $jumphtml .= "<option value=\"forums.cgi?forum=$forumid\">��|-$forumname\n</option>";
	    $outputbutton .= "<option value=\"$forumid\">��|-$forumname\n</option>";
	    $fname.="\$fname$forumid=\"$forumname\";\n";
	}
    }
    else {
        if ($hidden ne "") {
            $jumphtml .= "<!--h <!--c <option value=\"forums.cgi?forum=$forumid\">��|��|-$forumname$hidden\n</option> --> -->";
            $outputbutton .= "<!--h <!--c <option value=\"$forumid\">��|��|-$forumname$hidden\n</option> --> -->";
            $fname.="\$fname$forumid=\"$forumname\";\n";
        } else {
            $jumphtml .= "<!--c <option value=\"forums.cgi?forum=$forumid\">��|��|-$forumname$hidden\n</option> -->";
            $outputbutton .= "<!--c <option value=\"$forumid\">��|��|-$forumname$hidden\n</option> -->";
            $fname.="\$fname$forumid=\"$forumname\";\n";
        }
    }
    $lastcategoryplace = $categoryplace;
}
$jumphtml .= qq~</select>\n~;

mkdir ("${lbdir}cache", 0777) if (!(-e "${lbdir}cache"));
mkdir ("${lbdir}cache/myinfo", 0777) if (!(-e "${lbdir}cache/myinfo"));
mkdir ("${lbdir}cache/mymsg", 0777) if (!(-e "${lbdir}cache/mymsg"));
mkdir ("${lbdir}cache/meminfo", 0777) if (!(-e "${lbdir}cache/meminfo"));
mkdir ("${lbdir}cache/online", 0777) if (!(-e "${lbdir}cache/online"));
open (FILE, ">${lbdir}data/forumjump.pl");
$jumphtml  =~ s/\\/\\\\/isg;
$jumphtml  =~ s/~/\\\~/isg;
$jumphtml  =~ s/\$/\\\$/isg;
$jumphtml  =~ s/\@/\\\@/isg;
print FILE qq(\$jumphtml = qq~$jumphtml~;\n);
print FILE "1;\n";
close (FILE);
open (FILE, ">${lbdir}data/outputbutton.pl");
$outputbutton  =~ s/\\/\\\\/isg;
$outputbutton  =~ s/~/\\\~/isg;
$outputbutton  =~ s/\$/\\\$/isg;
$outputbutton  =~ s/\@/\\\@/isg;
print FILE qq(\$outputbutton = qq~$outputbutton~;\n);
print FILE "1;\n";
close (FILE);

open (FILE, ">${lbdir}data/fname.pl");
$fname  =~ s/\\/\\\\/isg;
$fname  =~ s/~/\\\~/isg;
$fname  =~ s/\@/\\\@/isg;
print FILE "$fname";
print FILE "1;\n";
close (FILE);

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata1 = grep(/forumcache/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }

@dirdata = grep(/^forums/,@dirdata);
foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
}

sub writecatemod {
	opendir (CATDIR, "${lbdir}boarddata");
	@dirdata = readdir(CATDIR);
	closedir (CATDIR);
	@dirdata = grep(/^catemod/,@dirdata);
	foreach (@dirdata) {
   	    if (open(CATEFILE,"${lbdir}boarddata/$_")) {
   	        my $catemods =<CATEFILE>;
   	        close(CATEFILE);
   	        my @catemodnames = split(/\,/, $catemods);
   	        my $cmodnumber=@catemodnames;
	        foreach (@catemodnames) {
   		    chomp $_;
   		    next if ($_ eq "");
	            my $cleanedmodname = $_;
	            $cleanedmodname =~ s/ /\_/g;
	            $cleanedmodname =~ tr/A-Z/a-z/;
   		    $cmodoutput .= qq~<option value="~ . uri_escape($cleanedmodname) . qq~">$_</option>~;
	        }
	    }
	    if ($cmodoutput ne "") {
	    	$_ =~ s/^catemod(.+?)\.cgi$/$1/isg;
	        $cmodoutputfile .= qq~\$cmodoutput[$_] = qq(<img src=$imagesurl/images/team2.gif width=19 align=absmiddle><select onchange="surfto(this)"><option style=background-color:\$titlecolor>�˷�����������</option>$cmodoutput);
~;
	        $cmodoutput = "";
	    }
	}

	mkdir ("${lbdir}cache", 0777) if (!(-e "${lbdir}cache"));
	mkdir ("${lbdir}cache/myinfo", 0777) if (!(-e "${lbdir}cache/myinfo"));
    	mkdir ("${lbdir}cache/mymsg", 0777) if (!(-e "${lbdir}cache/mymsg"));
	mkdir ("${lbdir}cache/meminfo", 0777) if (!(-e "${lbdir}cache/meminfo"));
	mkdir ("${lbdir}cache/online", 0777) if (!(-e "${lbdir}cache/online"));
    	mkdir ("${lbdir}cache/id", 0777) if (!(-e "${lbdir}cache/id"));
	open (FILE, ">${lbdir}data/forumcate.pl");
	$cmodoutputfile  =~ s/~/\\\~/isg;
	print FILE qq~$cmodoutputfile~;
	print FILE "1;\n";
	close (FILE);
opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata = grep(/^forums/,@dirdata);
foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
}


#�����̨�ϴ�logo��By Easunlee
sub douppics
{ #1
  # $addme=$query->upload('addme'); #���CGI.pm�汾>2.47���Ƽ�ʹ��
  $addme=$query->param('addme'); #���CGI.pm�汾<2.47�������滻�Ͼ�
  return unless ($addme);

  my ($tmpfilename) = $addme =~ m|([^/:\\]+)$|; #ע��,��ȡ�ļ����ֵ���ʽ�仯
  my @filename = split(/\./,$tmpfilename); #ע��
  my $up_name = $filename[0];
  my $up_ext = $filename[-1];
  $up_ext = lc($up_ext);

  &errorout("�ϴ�������֧�������ϴ���ͼƬ���ͣ�������ѡ��") if (($up_ext ne "gif") && ($up_ext ne "jpg") && ($up_ext ne "bmp")&&($up_ext ne "swf")&&($up_ext ne "png"));


  my $buffer;
  open (FILE,">$imagesdir/myimages/$up_name.$up_ext");
  binmode (FILE);
  binmode ($addme); #ע��

  while (read($addme,$buffer,4096) )
  {#2
   print FILE $buffer;
   $filesize=$filesize+4;
  } #2
  close (FILE);
  close ($addme); #ע��

  if ($up_ext eq "gif"||$up_ext eq "jpg"||$up_ext eq "bmp"||$up_ext eq "jpeg"||$up_ext eq "png"||$up_ext eq "ppm"||$up_ext eq "svg"||$up_ext eq "xbm"||$up_ext eq "xpm")
  { #3

     my $info = image_info("${imagesdir}myimages/$up_name.$up_ext");
     if ($info->{error} eq "Unrecognized file format")
     {
        unlink ("${imagesdir}myimages/$up_name.$up_ext");
        &errorout("�ϴ�����&�ϴ��ļ�����ͼƬ�ļ������ϴ���׼��ͼƬ�ļ���");
     }
     undef $info;
  } #3

} #1

