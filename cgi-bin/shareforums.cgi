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
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "shareforums.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

	@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        	$theparam = &cleaninput("$theparam");
		$PARAM{$param} = $theparam;
	    }



    $action      =  $PARAM{'action'};
    $forumid     =  $PARAM{'forum'};
    $new_forumname   =  $PARAM{'forumname'};
    $new_forumurl    =  $PARAM{'forumurl'};
    $new_foruminfo   =  $PARAM{'foruminfo'};
    $new_forumorder  =  $PARAM{'forumorder'};
    $new_weblogo     =  $PARAM{'weblogo'}; 
    $checkaction     =  $PARAM{'checkaction'};
    $oldforum        =  $PARAM{'oldforum'};
    $oforumname	     =  $PARAM{'oforumname'};
    
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
            'order'               =>    \&orderform,
            'reorder'             =>    \&reorderformnow,
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
               }
                elsif (($action eq "delete") && ($checkaction ne "yes")) { &warning; }
                elsif (($action eq "delete") && ($checkaction eq "yes")) { &deleteforum; }
                else { &forumlist; }
            
            } #e1
                
                else {
                    &adminlogin;
                    }
        

##################################################################################
sub reorderformnow {
    $filetoopen = "$lbdir" . "data/shareforums.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @forums = <FILE>;
    close(FILE);
    $forumnamenum = 0;
    foreach $forum (@forums) { #start foreach @forums
        chomp $forum;
	next if ($forum eq "");
	$forumnamenum++;
        ($forumname, $forumurl, $foruminfo, $forumorder, $weblogo) = split(/\t/,$forum);
	next if ($forumname eq "");
	if ($forumnamenum eq $oldforum) {
	    $holdforuminfo = $forum;
	    last;
	}
    } # end foreach (@forums)

    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    $forumnamenum = 0;
    foreach $forum (@forums) { #start foreach @forums
        chomp $forum;
	next if ($forum eq "");
	$forumnamenum ++;
        ($forumname, $forumurl, $foruminfo, $forumorder, $weblogo) = split(/\t/,$forum);
	next if ($forumname eq "");
    	next if ($forumnamenum eq $oldforum);
	print FILE "$forum\n";
	if ($forumnamenum eq $forumid) {
	    print FILE "$holdforuminfo\n";
	}

    } # end foreach (@forums)
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / ������̳�������ƽ��</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>������Ϣ�Ѿ��ɹ�����</b>
                </td></tr></table></td></tr></table>
                ~;
&outunion;
}

sub orderform {
    print qq~
    <tr><td bgcolor=#2159C9 colspan=3><font face=���� color=#FFFFFF>
    <b>��ӭ������̳�������� / ������̳����</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font face=���� color=#333333>
    <b>ע�����</b><br><br>
    �ڴ������Խ�������̳��������</td></tr>
    ~;

         print qq~
            <tr>
            <td bgcolor=#FFFFFF colspan=3 ><font face=���� color=#333333><hr noshade>
            </td></tr>
            <tr>
            <td bgcolor=#EEEEEE width=20% nowrap><font face=���� color=#333333>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="reorder">
            <input type=hidden name="oldforum" value="$forumid">
       ��������̳ "<font color=red>$oforumname</font>" �ƶ���<BR> </font>
            <select name="forum">
       ~;
    $filetoopen = "$lbdir" . "data/shareforums.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @forums = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
$forumnamenum = 0;
    foreach $forum (@forums) { #start foreach @forums
        chomp $forum;
	next if ($forum eq "");
	$forumnamenum++;
        ($forumname, $forumurl, $foruminfo, $forumorder, $weblogo) = split(/\t/,$forum);
	next if ($forumname eq "");
    	next if ($forumnamenum eq $forumid);
         print qq~
	<option value=\"$forumnamenum\"> $forumname\n
	~;

    } # end foreach (@forums)
         print qq~</select> ���档
                   </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE>
                    <BR>������<input type=submit value="�� ��"></td></form></tr></table></td></tr></table>~;
    
} # end routine.

sub forumlist {
    $highest = 0;
    print qq~
    <tr><td bgcolor=#2159C9 colspan=3><font face=���� color=#FFFFFF>
    <b>��ӭ������̳�������� / ������̳����</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font face=���� color=#333333>
    <b>ע�����</b><br><br>
    �����棬��������Ŀǰ���е�������̳�������Ա༭������̳����������һ���µ�������̳�� 
    Ҳ���Ա༭��ɾ��Ŀǰ���ڵ�������̳�������Զ�Ŀǰ���������½������С�<br>
    </td></tr>
    ~;

    $filetoopen = "$lbdir" . "data/shareforums.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @forums = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    foreach $forum (@forums) { #start foreach @forums
        chomp $forum;
	next if ($forum eq "");
        ($forumname, $forumurl, $foruminfo, $forumorder, $weblogo) = split(/\t/,$forum);
        $rearrange = ("$forumname\t$forumurl\t$foruminfo\t$forumorder\t$weblogo");
        push (@rearrangedforums, $rearrange);

    } # end foreach (@forums)

         print qq~
            <tr>
            <td bgcolor=#FFFFFF colspan=3 ><font face=���� color=#333333><hr noshade>
            </td></tr>
            <tr>
            <td bgcolor=#EEEEEE width=20% nowrap><font face=���� color=#333333>
       <a href="$thisprog?action=addforum">�����µ�������̳</a></font></td>
            </td></tr>
       
       ~;
    @finalsortedforums = @rearrangedforums;
    $forumnamenum = 0;
    foreach $sortedforums (@finalsortedforums) { #start foreach @finalsortedforums

        ($forumname, $forumurl, $foruminfo, $forumorder, $weblogo) = split(/\t/,$sortedforums);
        $forumnamenum++;
        my $uriforumname = &uri_escape($forumname);
               print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=3 align=left><hr noshade width=70%><font face=���� color=#333333>
                <b>������̳����</b>�� $forumname<BR><b>������̳ URL</b>�� $forumurl<br><b>������̳LOGO</b>�� $weblogo<br><b>������̳���</b>�� $foruminfo<br>
                <br><a href="$thisprog?action=edit&forum=$forumnamenum">�༭��������̳</a> | <font face=���� color=#333333><a href="$thisprog?action=delete&forum=$forumnamenum&oforumname=$uriforumname">ɾ����������̳</a> | <font face=���� color=#333333><a href="$thisprog?action=order&forum=$forumnamenum&oforumname=$uriforumname">��������������̳</a> </font></td>
                </font></td></tr>
                ~;
       
            } # end foreach
    
               
        print qq~
        <td bgcolor=#FFFFFF colspan=3 ><font face=���� color=#333333><hr noshade>
        </td></tr>
             <tr>
            <td bgcolor=#EEEEEE width=20% nowrap><font face=���� color=#333333>
       <a href="$thisprog?action=addforum">�����µ�������̳</a></font></td>
            </td></tr>
        </tr></table></td></tr></table>~;
    
} # end routine.

sub addforum {

        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
        <b>��ӭ������̳�������� / ����������̳</b>
        </td></tr>
        ~;

 
        print qq~
        
                     
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="processnew">       
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>������̳����</b><br>��������������̳������<BR>(������� 20 ��������)</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumname" maxlength=40></td>
        </tr>       
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>������̳ URL</b><br>��������������̳�� URL</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumurl" value="http://"></td>
        </tr>   
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>��վ LOGO ��ַ</b><br>������������̳վ��� LOGO ��ַ��88*31��</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="weblogo" value="http://"></td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>��̳����</b><br>����������̳������</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="foruminfo"></td>
        </tr>   
        
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
        ~;
        
} # end route   


##################################################################################
######## Subroutes ( Create Forum )


sub createforum {   
		
		&errorout("�Բ�����̳���ֹ������������ 20 �������ڣ�") if (length($new_forumname) >40);
		&errorout("��̳�������ܿգ���") if ($new_foruminfo eq "");
                $new_forumurl=~s ! !!ig;
		&errorout("��̳��ַ���ܿգ���") if ($new_forumurl eq "");
                $filetoopen = "$lbdir" . "data/shareforums.cgi";
	        &winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE, "$filetoopen");
  	        flock(FILE, 1) if ($OS_USED eq "Unix");
                my @forums = <FILE>;
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                # Create a new number for the new forum folder, and files.

                open(FILE, ">$filetoopen");
                flock(FILE, 2) if ($OS_USED eq "Unix");
                foreach $line (@forums) {
                    chomp $line;
                    print FILE "$line\n";
                    }
                print FILE "$new_forumname\t$new_forumurl\t$new_foruminfo\t$new_forumorder\t$new_weblogo\t";
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");
                
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / ����������̳���</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                <font face=���� color=#333333>
                ~;

                print "<b>��ϸ����</b><p>\n";
                print "<ul>\n";
               
                print "��������̳ <B>$new_forumname</b> �Ѿ�������";
                               
                print "</ul></td></tr></table></td></tr></table>\n";
&outunion;
} ######## end routine
        
##################################################################################
######## Subroutes ( Warning of Delete Forum )  

sub warning { #start

        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
        <b>��ӭ������̳�������� / ɾ��������̳</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=���� color=#990000><b>���棡��</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <font face=���� color=#333333>�����ȷ��Ҫɾ��������̳ $oforumname����ô������������<p>
        >> <a href="$thisprog?action=delete&checkaction=yes&forum=$forumid&oforumname=$oforumname">ɾ��������̳</a> <<
        </td></tr>
        </table></td></tr></table>
        
        ~;
        
} # end routine     
        
##################################################################################
######## Subroutes ( Deletion of a Forum )  

sub deleteforum { #start

         $filetoopen = "$lbdir" . "data/shareforums.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         my @forums = <FILE>;
         close(FILE);

         open(FILE,">$filetoopen");
         flock(FILE,2) if ($OS_USED eq "Unix");
         $forumname = 0;
         foreach $forum (@forums) {
         chomp $forum;
	 next if ($forum eq "");
	 $forumname ++;
                unless ($forumid eq $forumname) {
                    print FILE "$forum\n";
                    }
                }
         close(FILE);
         &winunlock($filetoopen) if ($OS_USED eq "Nt");

       
                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                    <b>��ӭ������̳�������� / ɾ��������̳���</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                    <font face=���� color=#990000>
                    
                    <center><b>������̳ <B>$oforumname</B> �ѱ�ɾ��</b>����ˢ��������̳����ҳ���ټ���������</center><p>
                    
                  
                                    
                    </td></tr></table></td></tr></table>
                    ~;
&outunion;

} # routine ends

######## Subroutes ( Editing of a Forum )   
sub editform {

        
        # Grab the line to edit.
        
         $filetoopen = "$lbdir" . "data/shareforums.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
         flock(FILE, 2) if ($OS_USED eq "Unix");
         @forums = <FILE>;
         close(FILE);
         &winunlock($filetoopen) if ($OS_USED eq "Nt");
         ($forumname,$forumurl,$foruminfo,$forumorder,$weblogo) = split(/\t/,$forums[$forumid-1]);   
         
# Present the form to be filled in


        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
        <b>��ӭ������̳�������� / �༭������̳</b>
        </td></tr>
       
                
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="doedit">
        <input type=hidden name="forum" value="$forumid">
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>������̳����</b><br>������������̳����<BR>(������� 20 ��������)</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumname" value="$forumname"  maxlength=40></td>
        </tr>       
        
         <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>������̳URL</b><br>������������̳ URL</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="forumurl" value="$forumurl"></td>
        </tr>   
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>��վ LOGO ��ַ</b><br>������������̳վ���LOGO��ַ��88*31��</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="weblogo" value="$weblogo"></td>
        </tr> 
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>������̳����</b><br>������������̳����</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="foruminfo" value="$foruminfo"></td>
        </tr>   
        
            
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
        ~;
        
} # end route   

##################################################################################
######## Subroutes ( Processing the edit of a forum)    


sub doedit {
        
        # Grab the line to edit.
	
	&errorout("�Բ�����̳���ֹ������������ 20 �������ڣ�") if (length($new_forumname) >40);
	&errorout("��̳�������ܿգ���") if ($new_foruminfo eq "");

         $new_forumurl=~s ! !!ig;
 	 &errorout("��̳��ַ���ܿգ���") if ($new_forumurl eq "");
         
         $filetoopen = "$lbdir" . "data/shareforums.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
	 open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         my @forums = <FILE>;
         close(FILE);

               # Time to process the forms

                $editedline = "$new_forumname\t$new_forumurl\t$new_foruminfo\t$new_forumorder\t$new_weblogo\t";
                chomp $editedline;

                # Lets re-open the file
                
                
                # Lets remake the file...
                
                $filetoopen = "$lbdir" . "data/shareforums.cgi";
                open(FILE,">$filetoopen");
                flock(FILE,2) if ($OS_USED eq "Unix");
                $tempforumid = 0;
                foreach $forum (@forums) {
                chomp $forum;
                $tempforumid ++;
                    if ($tempforumid eq $forumid) {
                        print FILE "$editedline\n";
                        }
                        else {
                            print FILE "$forum\n";
                            }
                    }
                close (FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");


                 print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / �༭������̳���</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333><b>������Ϣ�Ѿ�����</b><p>
                
                </td></tr></table></td></tr></table>
                ~;
                &outunion;
            } # end routine



print qq~</td></tr></table></body></html>~;
exit;

sub errorout {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / ��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                <font face=���� color=#333333>
                <font face=���� color=#333333><b>$_[0]</b>
                </td></tr></table></td></tr></table>
                ~;
exit;	
}

sub outunion {

if (open(SFFILE,"${lbdir}data/shareforums.cgi")) {
#    flock(SFFILE, 1) if ($OS_USED eq "Unix");
    @lmforums = <SFFILE>;
    close(SFFILE);
    $lmforums = @lmforums;
}
$uniontitle="<font color=$fontcolormisc>������ $lmforums ��������̳��</font>";
$unionoutput = "";
  if (($lmforums ne "")&&($lmforums > 0)) {
    $unionoutput .= qq~
<tr><td bgcolor=\$titlecolor colspan=2  \$catbackpic>
<font color=\$titlefontcolor><b>-=> ������̳ $uniontitle</b>�� [<a href=leobbs.cgi?action=union><font color=$fontcolormisc>\$unionview</font></a>]�� [<span style="cursor:hand" onClick="javascript:openScript('lmcode.cgi',480,240)">��̳���˴���</span>]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<span style="font-family:webdings;font-size:13px;"> 
<font onMouseOver="document.all.lmforum.direction='left';document.all.lmforum.scrollAmount=6;document.all.lmforum1.direction='left';document.all.lmforum1.scrollAmount=6;" onMouseOut="document.all.lmforum.scrollAmount=4;document.all.lmforum1.scrollAmount=4;" onMouseUp="document.all.lmforum.scrollAmount=6;document.all.lmforum1.scrollAmount=6;" onMouseDown="document.all.lmforum.scrollAmount=10;document.all.lmforum1.scrollAmount=10;" style="cursor:hand;" title=���������ʾ>7</font> 
<font onClick="stop=0;document.all.lmforum.start();stop=0;document.all.lmforum1.start();" style="cursor:hand;" title=��ʼ����>4</font> 
<font onClick="stop=1;document.all.lmforum.stop();stop=1;document.all.lmforum1.stop();" style="cursor:hand;" title=ֹͣ����><</font> 
<font onMouseOver="document.all.lmforum.direction='right';document.all.lmforum.scrollAmount=6;document.all.lmforum1.direction='right';document.all.lmforum1.scrollAmount=6;" onMouseOut="document.all.lmforum.scrollAmount=4;document.all.lmforum1.scrollAmount=4;" onMouseUp="document.all.lmforum.scrollAmount=6;document.all.lmforum1.scrollAmount=6;" onMouseDown="document.all.lmforum.scrollAmount=10;document.all.lmforum1.scrollAmount=10;" style="cursor:hand;" title=���ҹ�����ʾ>8</font> 
</span>&nbsp;[����������ư�ť]
</td></tr>~;

$unionoutput1 = "";
	$lmtexts = "";
	$lmlogos = "";
	foreach $lmforum (@lmforums) {
	    chomp $lmforum;
            next if ($lmforum eq "");
            ($lmforumname,$lmforumurl,$lmforuminfo,$lmforumorder,$lmweblogo) = split(/\t/,$lmforum);
            if (($lmweblogo ne "")&&($lmweblogo ne "http:\/\/")) { $lmlogos .= qq~<a href=$lmforumurl target=_blank onmouseover="document.all.lmforum.stop();" onmouseout="document.all.lmforum.start();"><img src=$lmweblogo width=88 height=31 border=0 title="$lmforumname\n$lmforuminfo"></a> ~; }
            else { $lmtexts .= qq~<a href=$lmforumurl target=_blank title="$lmforuminfo" onmouseover="document.all.lmforum1.stop();" onmouseout="document.all.lmforum1.start();">$lmforumname</a>��~; }
	}
	if ($lmlogos ne "") {
	    $unionoutput1 .= qq~<tr><td bgcolor=\$forumcolorone width=26 align=center><img src=\$imagesurl/images/\$skin/shareforum.gif width=16></td><td bgcolor=\$forumcolortwo width=*><table width=100% cellpadding=0 cellspacing=0><tr><td width=100%><img src=\$imagesurl/images/none.gif width=680 height=1><BR><marquee name="lmforum" id="lmforum">$lmlogos</marquee></td></tr></table></td></tr>~;
	} else {
	    $unionoutput1 .= qq~<tr style=display:none><td colspan=2 height=0><marquee name="lmforum" id="lmforum"></marquee></td></tr>~;
	}
	if ($lmtexts ne "") {
	    $unionoutput1 .= qq~<tr><td bgcolor=\$forumcolorone width=26 align=center><img src=\$imagesurl/images/\$skin/shareforum.gif width=16></td><td bgcolor=\$forumcolortwo width=*><table width=100% cellpadding=0 cellspacing=0><tr><td width=100%><img src=\$imagesurl/images/none.gif width=680 height=1><BR><marquee name="lmforum1" id="lmforum1">$lmtexts</marquee></td></tr></table></td></tr>~;
	} else {
	    $unionoutput1 .= qq~<tr style=display:none><td colspan=2 height=0><marquee name="lmforum1" id="lmforum1"></marquee></td></tr>~;
	}

  }

mkdir ("${lbdir}cache", 0777) if (!(-e "${lbdir}cache"));
open (FILE, ">${lbdir}data/unionoutput.pl");
$unionoutput =~ s/(\\|\"|\'|\@|\~)/\\$1/isg;
$unionoutput   =~ s/\(/\\\(/isg;
$unionoutput   =~ s/\)/\\\)/isg;
$unionoutput1 =~ s/(\\|\"|\'|\@|\~)/\\$1/isg;
$unionoutput1  =~ s/\(/\\\(/isg;
$unionoutput1  =~ s/\)/\\\)/isg;
print FILE qq~if (\$union==0) { \$unionview="��ʾ�����б�"; } else { \$unionview="�ر������б�"; }\n
\$output .= qq($unionoutput);\n
\$output .= qq($unionoutput1) if (\$union == 1);
~;
print FILE "1;\n";
close (FILE);

}
