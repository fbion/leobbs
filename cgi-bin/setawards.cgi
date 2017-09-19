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
$LBCGI::POST_MAX=1024*150;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";
require "code.cgi"; 
$|++;

$thisprog = "setawards.cgi";

$query = new LBCGI;

&ipbanned; #��ɱһЩ ip

@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        	$theparam = &cleaninput("$theparam");
		$PARAM{$param} = $theparam;
	    }


    $action          =  $PARAM{'action'};
    $awardid         =  $PARAM{'award'};
    $new_awardname   =  $PARAM{'awardname'};
    $new_awardurl    =  $PARAM{'awardurl'};
    $new_awardinfo   =  $PARAM{'awardinfo'};
    $new_awardorder  =  $PARAM{'awardorder'};
    $new_weblogo     =  $PARAM{'weblogo'}; 
    $checkaction     =  $PARAM{'checkaction'};
    $oldaward        =  $PARAM{'oldaward'};
    $oawardname	     =  $PARAM{'oawardname'};
    $action          = &unHTML("$action");
    
$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312);       
&admintitle;
        
&getmember("$inmembername","no");
        
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
            
           my %Mode = ( 

            'addaward'            =>    \&addaward,
            'processnew'          =>    \&createaward,
            'edit'                =>    \&editaward,
            'doedit'              =>    \&doedit,       
             );


            if($Mode{$action}) {$Mode{$action}->();}
            elsif (($action eq "delete") && ($checkaction ne "yes")) { &warning; }
            elsif (($action eq "delete") && ($checkaction eq "yes")) { &deleteaward; }
            else { &awardlist; }            
            }                
else {&adminlogin;}
        
sub awardlist {
    $highest = 0;
    print qq~
    <tr><td bgcolor=#2159C9 colspan=3><font face=���� color=#FFFFFF>
    <b>��ӭ������̳�������� / ����ѫ�¹���</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font face=���� color=#333333>
    <b>ע�����</b><br><br>
    �����棬��������Ŀǰ���е�����ѫ�¡������Ա༭����ѫ������������һ���µ�����ѫ�¡� 
    Ҳ���Ա༭��ɾ��Ŀǰ���ڵ�����ѫ�¡�<br>
    </td></tr>
    ~;

    $filetoopen = "$lbdir" . "data/cityawards.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @awards = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    foreach $award (@awards) { #start foreach @awards
        chomp $award;
	next if ($award eq "");
        ($awardname, $awardurl, $awardinfo, $awardorder, $awardpic) = split(/\t/,$award);
        $rearrange = ("$awardname\t$awardurl\t$awardinfo\t$awardorder\t$awardpic");
        push (@rearrangedawards, $rearrange);

    } # end foreach (@awards)

         print qq~
            <tr>
            <td bgcolor=#FFFFFF colspan=3 ><font face=���� color=#333333><hr noshade>
            </td></tr>
            <tr>
            <td bgcolor=#EEEEEE width=20% nowrap><font face=���� color=#333333>
       <a href="$thisprog?action=addaward">�����µ�����ѫ��</a></font></td>
            </td></tr>
       
       ~;
    @finalsortedawards = @rearrangedawards;
    $awardnamenum = 0;
    foreach $sortedawards (@finalsortedawards) { #start foreach @finalsortedawards

        ($awardname, $awardurl, $awardinfo, $awardorder, $awardpic) = split(/\t/,$sortedawards);
        $awardnamenum++;
       
               print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=3 align=left><hr noshade width=70%><font face=���� color=#333333>
                <b>����ѫ������</b>�� $awardname<BR><b>����ѫ��ͼƬ</b>�� <img src=$imagesurl/awards/$awardpic><br><b>����ѫ�¼��</b>�� $awardinfo<br>
                <br><a href="$thisprog?action=edit&award=$awardnamenum">�༭������ѫ��</a> | <font face=���� color=#333333><a href="$thisprog?action=delete&award=$awardnamenum&oawardname=$awardname">ɾ��������ѫ��</a> </td>
                </font></td></tr>
                ~;
       
            } # end foreach
    
               
        print qq~
        <td bgcolor=#FFFFFF colspan=3 ><font face=���� color=#333333><hr noshade>
        </td></tr>
             <tr>
            <td bgcolor=#EEEEEE width=20% nowrap><font face=���� color=#333333>
       <a href="$thisprog?action=addaward">�����µ�����ѫ��</a></font></td>
            </td></tr>
        </tr></table></td></tr></table>~;
    
} # end routine.

sub addaward {

        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
        <b>��ӭ������̳�������� / ��������ѫ��</b>
        </td></tr>
        ~;

 
        print qq~
        
                     
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="processnew">       
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>����ѫ������</b><br>������������ѫ�µ�����<BR>(������� 20 ��������)</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="awardname" maxlength=40></td>
        </tr>
        <input type=hidden size=40 name="awardurl" value="">
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>����ͼƬ����</b><br>������ͼƬ����(����non-cgi/images/awardsĿ¼��)</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="weblogo"></td>
        </tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>��������</b><br>�������½���������</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="awardinfo"></td>
        </tr>   
        
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
        ~;
        
}

sub createaward {   
		
		&errorout("�Բ�����̳���ֹ������������ 20 �������ڣ�") if (length($new_awardname) >40);
		&errorout("�����������ܿգ���") if ($new_awardinfo eq "");
                
                $filetoopen = "$lbdir" . "data/cityawards.cgi";
	        &winlock($filetoopen) if ($OS_USED eq "Nt");
                open(FILE, "$filetoopen");
  	        flock(FILE, 1) if ($OS_USED eq "Unix");
                my @awards = <FILE>;
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");

                # Create a new number for the new award folder, and files.

                open(FILE, ">$filetoopen");
                flock(FILE, 2) if ($OS_USED eq "Unix");
                foreach $line (@awards) {
                    chomp $line;
                    print FILE "$line\n";
                    }
                print FILE "$new_awardname\t$new_awardurl\t$new_awardinfo\t$new_awardorder\t$new_weblogo\t";
                close(FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");
                
                print qq~
                <tr><td bgcolor=#2159C9" colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / ��������ѫ�½��</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                <font face=���� color=#333333>
                ~;

                print "<b>��ϸ����</b><p>\n";
                print "<ul>\n";
               
                print "������ѫ�� <B>$new_awardname</b> �Ѿ�������";
                print "<a href=\"$thisprog?action=awardlist\">����</a> ";             
                print "</ul></td></tr></table></td></tr></table>\n";

}

sub warning { #start

        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
        <b>��ӭ������̳�������� / ɾ������ѫ��</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=���� color=#990000><b>���棡��</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <font face=���� color=#333333>�����ȷ��Ҫɾ������ѫ�� $oawardname����ô������������<p>
        >> <a href="$thisprog?action=delete&checkaction=yes&award=$awardid&oawardname=$oawardname">ɾ������ѫ��</a> <<
        <br><br>>> <a href=\"$thisprog?action=awardlist\">����,�ٿ���һ��</a> <<
        </td></tr>
        </table></td></tr></table>
        
        ~;
        
}
sub deleteaward {

         $filetoopen = "$lbdir" . "data/cityawards.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         my @awards = <FILE>;
         close(FILE);

         open(FILE,">$filetoopen");
         flock(FILE,2) if ($OS_USED eq "Unix");
         $awardname = 0;
         foreach $award (@awards) {
         chomp $award;
	 next if ($award eq "");
	 $awardname ++;
                unless ($awardid eq $awardname) {
                    print FILE "$award\n";
                    }
                }
         close(FILE);
         &winunlock($filetoopen) if ($OS_USED eq "Nt");

       
                    print qq~
                    <tr><td bgcolor=#2159C9" colspan=2><font face=���� color=#FFFFFF>
                    <b>��ӭ������̳�������� / ɾ������ѫ�½��</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                    <font face=���� color=#990000>
                    
                    <center><b>����ѫ�� <B>$oawardname</B> �ѱ�ɾ��</b>����ˢ������ѫ�¹���ҳ���ټ���������</center><p>
                    
                  
                                    
                    </td></tr></table>
                    <center>>> <a href=\"$thisprog?action=awardlist\">�����ﷵ��</a> <<</center></td></tr></table>
                    ~;


}

sub editaward {

         $filetoopen = "$lbdir" . "data/cityawards.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
         open(FILE,"$filetoopen");
         flock(FILE, 2) if ($OS_USED eq "Unix");
         @awards = <FILE>;
         close(FILE);
         &winunlock($filetoopen) if ($OS_USED eq "Nt");
         ($awardname,$awardurl,$awardinfo,$awardorder,$awardpic) = split(/\t/,$awards[$awardid-1]);   
         
        print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
        <b>��ӭ������̳�������� / �༭����ѫ��</b>
        </td></tr>
       
                
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="doedit">
        <input type=hidden name="award" value="$awardid">
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>����ѫ������</b><br>����������ѫ������<BR>(������� 20 ��������)</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="awardname" value="$awardname"  maxlength=40></td>
        </tr>
        <input type=hidden size=40 name="awardurl" value="">
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>����ѫ��ͼƬ</b><br>����������ѫ��ͼƬ(����non-cgi/images/awardsĿ¼��)</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="weblogo" value="$awardpic"></td>
        </tr> 
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=���� color=#333333><b>����ѫ������</b><br>����������ѫ������</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="awardinfo" value="$awardinfo"></td>
        </tr>   
        
            
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
        ~;
        
}

sub doedit {
        
	&errorout("�Բ��𣬽������ֹ������������ 20 �������ڣ�") if (length($new_awardname) >40);
	&errorout("�����������ܿգ���") if ($new_awardinfo eq "");
       
         $filetoopen = "$lbdir" . "data/cityawards.cgi";
         &winlock($filetoopen) if ($OS_USED eq "Nt");
	 open(FILE,"$filetoopen");
         flock(FILE, 1) if ($OS_USED eq "Unix");
         my @awards = <FILE>;
         close(FILE);

                $editedline = "$new_awardname\t$new_awardurl\t$new_awardinfo\t$new_awardorder\t$new_weblogo\t";
                chomp $editedline;

                $filetoopen = "$lbdir" . "data/cityawards.cgi";
                open(FILE,">$filetoopen");
                flock(FILE,2) if ($OS_USED eq "Unix");
                $tempawardid = 0;
                foreach $award (@awards) {
                chomp $award;
                $tempawardid ++;
                    if ($tempawardid eq $awardid) {
                        print FILE "$editedline\n";
                        }
                        else {
                            print FILE "$award\n";
                            }
                    }
                close (FILE);
	        &winunlock($filetoopen) if ($OS_USED eq "Nt");


                 print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / �༭����ѫ�½��</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#333333><b>������Ϣ�Ѿ�����</b><p>
               
                </td></tr></table>
                <center><a href=\"$thisprog?action=awardlist\">����</a></center> 
                </td></tr></table>
                ~;
                
            }



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
