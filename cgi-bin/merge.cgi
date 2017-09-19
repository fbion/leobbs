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
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
require "rebuildlist.pl";
$|++;

$thisprog = "merge.cgi";

$query = new LBCGI;


for ('action','oforum','dforum', 'delsource') {
    next unless defined $_;
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    ${$_} = $tp;
    }

my $delsource2;
if ($delsource eq "yes") {$delsource2 = "no";}
else {$delsource2 = "yes";}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
    &getmember("$inmembername","no");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
	if($action eq 'submit') {
		if($oforum == $dforum) {
			print qq~
			<tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
		        <b>��ӭ������̳�������� / �ϲ���̳</b>
		        </td></tr>
		        <tr>
		        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		        <font face=���� color=#990000><b>������\~\~\~һ����̳��ô�ϲ�ѽ��</td></tr>
        	        </table></td></tr></table>
        	        ~;
        	        print qq~</td></tr></table></body></html>~;
        	        exit;
        	}
        	$oforumpath = "${lbdir}forum$oforum";
        	$dforumpath = "${lbdir}forum$dforum";

        opendir (DIR, "$oforumpath");
        @dirdata = readdir(DIR);
        closedir (DIR);

        @olist = grep(/thd.cgi$/,@dirdata);

        $dirtoopen = "$lbdir" . "forum$dforum";
        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);
        @sorteddirdata = grep(/.thd.cgi$/,@dirdata);
        @newdirdata = sort numerically(@sorteddirdata);
        @neworderdirdata = reverse(@newdirdata);
        $highest = $neworderdirdata[0];
        $highest =~ s/.thd.cgi$//;
        $lastnum = $highest;

        	foreach(@olist) {
        		@fields = split(/\./);
        		$topicid = $fields[0];
        		$newid = ++$lastnum;
        		$topicids{$topicid} = $newid;
        		$fields[0] = $newid;
        		$_ = join("\t",@fields);
        	}

        	open(FILE,">$dforumpath/lastnum.cgi");
         	flock(FILE, 2) if ($OS_USED eq "Unix");
        	print FILE $newid;
        	close(FILE);

        $dirtoopen2 = "$imagesdir" . "$usrdir/$oforum";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);
        @files = grep(/^$oforum\_/,@dirdata2);

        	while(($oldid,$newid) = each %topicids) {
        		copy("$oforumpath/$oldid.pl","$dforumpath/$newid.pl");
        		copy("$oforumpath/$oldid.thd.cgi","$dforumpath/$newid.thd.cgi");
        		copy("$oforumpath/$oldid.mal.pl","$dforumpath/$newid.mal.pl") if (-e "$oforumpath/$oldid.mal.pl");
        		copy("$oforumpath/$oldid.poll.cgi","$dforumpath/$newid.poll.cgi") if (-e "$oforumpath/$oldid.poll.cgi");
        		copy("$oforumpath/rate$oldid.file.pl","$dforumpath/rate$newid.file.pl") if (-e "$oforumpath/rate$oldid.file.pl");
        		copy("$oforumpath/rateip$oldid.file.pl","$dforumpath/rateip$newid.file.pl") if (-e "$oforumpath/rateip$oldid.file.pl");

		        @files1 = grep(/^$oforum\_$oldid\./,@files);
		        $files1 = @files1;
			if ($files1 > 0) {
			    foreach (@files1) {
			    	(my $name,my $ext) = split(/\./,$_);
				copy("$dirtoopen2/$oforum\_$oldid\.$ext","${imagesdir}$usrdir/$dforum/$dforum\_$newid\.$ext");
			    }
			}
	                @files1 = grep(/^$oforum\_$oldid\_/,@files);
	                $files1 = @files1;
	    	  	if ($files1 > 0) {
	        	    foreach (@files1) {
	    	    		(my $name,my $ext) = split(/\./,$_);
	            		(my $name1,my $name2,my $name3) = split(/\_/,$name);
		    		copy("${imagesdir}$usrdir/$oforum/$name.$ext","${imagesdir}$usrdir/$dforum/$dforum\_$newid\_$name3\.$ext");
	        	    }
	    		}
	    		require "dopost.pl";
           		&moveallupfiles($oforum,$oldid,$dforum,$newid,$delsource2);
        	}
        	$inforum = $oforum;
        	&deleteforum if ($delsource eq "yes");
        	$inforum = $dforum;

	         rebuildLIST(-Forum=>"$dforum");

		print qq~
	        <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
	        <b>��ӭ������̳�������� / �ϲ���̳</b>
	        </td></tr>

	        ~;
		&recount;
	} else {
	open(FILE,"<${lbdir}data/allforums.cgi");
        flock(FILE, 1) if ($OS_USED eq "Unix");
	@forumlist = <FILE>;
	close(FILE);
	chomp @forumlist;
	$tempoutput = '';
	foreach(@forumlist) {
		($forumid,$no,$no,$forumname) = split(/\t/);
		$tempoutput .= "<option value=\"$forumid\">$forumname</option>\n";
	}

        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
        <b>��ӭ������̳�������� / �ϲ���̳</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=���� color=#990000><b>��ע��:</b>�˹��̽��ķѴ���CPUʱ���ϵͳ��Դ�������򲻵��ѣ���Ҫ���ñ����ܣ�<br>
        �ϲ�ǰ������ȹر�������̳��
        </td></tr>
        <tr>
        <td bgcolor=#FFFFFF valign=middle colspan=2 align=center>
        <form action=$thisprog method=post>
        ����̳<select name="oforum">$tempoutput</select>�ϲ�����̳<select name="dforum">$tempoutput</select><BR>
        <input type="checkbox" name="delsource" value='yes' checked> �ϲ���ɾ��ԭ����̳��һ�����ݣ�<BR><BR>
        <input type="submit" value="ȷ��">
        <input type="hidden" name="action" value="submit"></form>
        </td></tr>
       </table></td></tr></table>
        ~;
	    }

   } else {
	&adminlogin;
    }

print qq~</td></tr></table></body></html>~;
exit;
sub byupdate {
	(my $no,$no,$no,$no,$no,$no,$no,$no,$no,my $lastpostdatea, $no, $no) = split(/\t/,$a);
	(my $no,$no,$no,$no,$no,$no,$no,$no,$no,my $lastpostdateb, $no, $no) = split(/\t/,$b);
	$lastpostdateb <=> $lastpostdatea;
}



sub recount { #start

         $threadcount = "0" if (!$threadcount);
         $topiccount  = "0" if (!$topiccount);

         my $info = rebuildLIST(-Forum=>"$inforum");
         ($threadcount,$topiccount) = split (/\|/,$info);

        $threadcount = 0 if ($threadcount<0);
        $topiccount  = 0 if ($topiccount <0);
        
                open(FILE, "+<${lbdir}boarddata/foruminfo$inforum.cgi");
                ($lastposttime, $threads, $posts, $todayforumpost, $lastposter) = split(/\t/,<FILE>);
                seek(FILE,0,0);
                print FILE "$lastposttime\t$threadcount\t$topiccount\t$todayforumpost\t$lastposter\t\n";
        	close(FILE);
	        $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	        open(FILE, ">${lbdir}boarddata/forumposts$inforum.pl");
	        print FILE "\$threads = $threadcount;\n\$posts = $topiccount;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
                close(FILE);

         print qq~
         <tr>
         <td bgcolor=#FFFFFF colspan=2>
         <font color=#990000>
         <center><b>��̳�ϲ��ɹ�</b></center><p>
         �������� $threadcount<p>
         �ظ����� $topiccount
         </td></tr></table></td></tr></table>
         ~;


} # routine ends
sub deleteforum { #start

        $dirtoopen = "$lbdir" . "forum$inforum";
        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);

        foreach $file (@dirdata) {
            $filetoremove = "$dirtoopen/$file";
            unlink $filetoremove;
        }

        $dirtoopen2 = "$imagesdir" . "$usrdir/$inforum";
        opendir (DIR, "$dirtoopen2");
        @dirdata2 = readdir(DIR);
        closedir (DIR);
        @files = @dirdata2;

        foreach $file (@files) {
            $filetoremove = "$dirtoopen2/$file";
            unlink $filetoremove;
        }

         $dirtoremove = "$lbdir" . "forum$inforum";
         rmdir $dirtoremove;
         $dirtoremove = "$imagesdir" . "$usrdir/$inforum";
         rmdir $dirtoremove;

        $filetoremove = "$lbdir" . "boarddata/list$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/listno$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/listall$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/xzb$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/xzbs$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/lastnum$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "boarddata/ontop$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "data/news$inforum.cgi";
        unlink $filetoremove;
        $filetoremove = "$lbdir" . "data/style$inforum.cgi";
        unlink $filetoremove;

         $filetoopen = "$lbdir" . "data/allforums.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         @forums = <FILE>;
         close(FILE);

         open(FILE,">$filetoopen");
         flock(FILE,2) if ($OS_USED eq "Unix");
         foreach $forum (@forums) {
         chomp $forum;
	 next if ($forum eq "");
            ($forumid,$category,$notneeded,$notneeded) = split(/\t/,$forum);
    	    next if ($forumid !~ /^[0-9]+$/);
                unless ($forumid eq "$inforum") {
                    print FILE "$forum\n";
                    }
                }
         close(FILE);
         &winunlock($filetoopen) if ($OS_USED eq "Nt");


} # routine ends
