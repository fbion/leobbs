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
use MAILPROG qw(sendmail);
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";
require "code.cgi"; 
require "data/cityinfo.cgi";
$|++;

$thisprog = "setmembers.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$action          = $query -> param('action');
$box          = $query -> param('box');
$checkaction     = $query -> param('checkaction');
$inletter        = $query -> param('letter');
$inmember        = $query -> param('member');
$inmember        = &unHTML("$inmember");
$action          = &unHTML("$action");

$indellast       = $query -> param('dellast');
$indellast       = &unHTML("$indellast");
$indelposts      = $query -> param('delposts');
$indelposts      = &unHTML("$indelposts");
$indeltime       = $query -> param('deltime');
$indeltime       = &unHTML("$indeltime");
$delusetype       = $query -> param('delusetype');
$delusetype       = &unHTML("$delusetype");
$indelcdrom      = $query -> param('delcdrom'); 
$indelcdrom      = &unHTML("$indelcdrom"); 
$undelname		 = $query -> param('undelname'); 
$undelname		 = &unHTML("$undelname"); 

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");       
&admintitle;
        
&getmember("$inmembername","no");
        
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
	<script>
	function openScript(url, width, height){var Win = window.open(url,"openScript",'width=' + width + ',height=' + height + ',resizable=1,scrollbars=yes,menubar=yes,status=yes' );}
	</script>
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>��ӭ������̳�������� / �û�����</b>
            </td></tr>
            ~;
            
            my %Mode = ( 

            'viewletter'         =>    \&viewletter,
            'edit'               =>    \&edit,        
            'deletemember'       =>    \&deletemember,
            'unban'              =>    \&unban,
            'delnopost'		 =>    \&delnopost,
            'canceldel'		 =>    \&canceldel,
            'deleteavatar'	 =>    \&deleteavatar,
            'boxaction'          =>    \&boxaction,
            'delok'		 =>    \&delok,
            'viewip'         =>    \&viewip,
		'viewdelmembers' => \&viewdelmembers, 
		'undelmember' => \&undelmember 
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
            }
            else { &memberoptions; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        

############### delete member

sub deleteavatar {

    $oldmembercode = $membercode;
    &getmember("$inmember");
    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "mo")||($membercode eq "amo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�ܰ�����Ȩɾ��̳���Ͱ������ϣ�</b></td></tr>";
            exit;
    }
    $inmember = $inmember;
    $inmember =~ y/ /_/;
    $inmember =~ tr/A-Z/a-z/;

    	unlink ("${imagesdir}usravatars/$inmember.gif");
    	unlink ("${imagesdir}usravatars/$inmember.png");
    	unlink ("${imagesdir}usravatars/$inmember.jpg");
    	unlink ("${imagesdir}usravatars/$inmember.jpeg");
    	unlink ("${imagesdir}usravatars/$inmember.swf");
    	unlink ("${imagesdir}usravatars/$inmember.bmp");
    	$memberfiletitletemp = unpack("H*","$inmember");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.gif");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.png");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.jpg");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.swf");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.bmp");

	unlink ("${lbdir}cache/meminfo/$inmember.pl");
	
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>�û�ͷ���Ѿ�ɾ����</b>
        </td></tr>
         ~;


} # end routine

##################################################################################
######## Subroutes (forum list)


sub memberoptions {
   %iplist=();%lettlerlist=();
open (FILE, "$lbdir/data/lbmember4.cgi");
flock(FILE, 1) if ($OS_USED eq "Unix");
my @file = <FILE>;
close (FILE);
chomp @file;
@file=sort @file;
$nowcount_a = 0;$nowcount_b = 0;
foreach(@file){
    my ($getmembername,$getip)=split(/\t/,$_);
    my $fr;
    ($getip,$getip2)=split(/, /,$getip);
    $getip = $getip2 if (($getip2 ne "")&&($getip2 ne "unknown"));
    $getip=~s/\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$//;
    unless(defined($iplist{$getip})) {
        $iplist{$getip}="$_";
        $ipshow=sprintf("% 3s",$getip);
        $ipshow=~s/\s/\&nbsp\;/g;
        $tempoutput2 .= qq~<br>~ if ($nowcount_b%15 == 0);
        $tempoutput2 .= qq~ <a href="$thisprog?action=viewip&letter=$getip">$ipshow</a> ~;
        $nowcount_b++;
    }
    if ($getmembername =~ /^[\w\-]/) {
	$fr = substr($getmembername, 0, 1);
	$fr =~ tr/a-z/A-Z/;
        $frshow=sprintf("%- 2s",$fr);
        $frshow=~s/\s/\&nbsp\;/g;
    } else {
	$fr =substr($getmembername, 0, 2);
        $frshow=$fr;
    }
   unless(defined(($lettlerlist{$fr}))) {
	$lettlerlist{$fr}="$_";
        $tempoutput .= qq~<br>~ if ($nowcount_a%15 == 0);
        $tempoutput .= qq~ <a href="$thisprog?action=viewletter&letter=~ . uri_escape($fr) . qq~">$frshow</a> ~;
        $nowcount_a ++;
    }
    last if ($nowcount_a >= 300);
}

    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>��ѡ��һ��</b>
    </td>
    </tr>          
    ~;
  if ($membercode eq "ad") {
    print qq~

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="foruminit.cgi?action=uptop">�����û�����</a></b><br>
    �û�������ʵ�����Զ����µģ����������������һ�¡�<BR><BR>
    </td>
    </tr>
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="foruminit.cgi?action=updatecount">���¼����û�����</a></b><br>
    ��������ҳ��ʾ���û������������������ָ���ȷ���û�����<BR><BR>
    </td>
    </tr>
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b>ɾ�������������û�</b>(ͬʱ���Զ������û�����)<BR>
    Ԥɾ������������ɾ���û���ֻ����һ��ͳ�ơ������̳���ǲ�����������ɾ���ġ�<BR>
    Ԥɾ��������ɾ���ڼ䣬����û���������̳����ô������ɾ����ʱ�򣬴��û����Ͻ���������<BR>
    ����ɾ�����û����������϶��ᶪʧ���������������ݣ��������޷��ָ��ġ�
	<form action="setmembers.cgi" method=POST>
        <input type=hidden name="action" value="delnopost">
        <select name="deltime">
        <option value="30" >һ������û���� 
        <option value="60" >��������û���� 
        <option value="90" >��������û����
        <option value="121">�ĸ�����û����
        <option value="151">�������û����
        <option value="182">��������û����
        <option value="212">�߸�����û����
        <option value="243">�˸�����û����
        <option value="273">�Ÿ�����û����
        <option value="304">ʮ������û����
        <option value="365">һ��֮��û����
        <option value="730">����֮��û����
        </select> �� 
        <select name="delposts">
		<option value="9999999999">���ܷ������� 
        <option value="0"   >û�з�������
        <option value="10"  >�ܷ������� 10
        <option value="50"  >�ܷ������� 50
        <option value="100" >�ܷ������� 100
        <option value="200" >�ܷ������� 200
        <option value="300" >�ܷ������� 300
        <option value="500" >�ܷ������� 500
        <option value="800" >�ܷ������� 800
        <option value="1000">�ܷ������� 1000
        </select> �� 
        <select name="dellast">
        <option value="no"  >���ܷ��ʴ���
        <option value="5"   >�������� 5 ��
        <option value="10"  >�������� 10 ��
        <option value="20"  >�������� 20 ��
        <option value="50"  >�������� 50 ��
        <option value="80"  >�������� 80 ��
        <option value="100" >�������� 100 ��
        <option value="200" >�������� 200 ��
        <option value="500" >�������� 500 ��
        </select> �� 
       <select name="delcdrom"> 
       <option value="30" >һ������û���� 
       <option value="60" >��������û���� 
       <option value="90" >��������û���� 
       <option value="121">�ĸ�����û���� 
       <option value="151">�������û���� 
       <option value="182">��������û���� 
       <option value="212">�߸�����û���� 
       <option value="243">�˸�����û���� 
       <option value="273">�Ÿ�����û���� 
       <option value="304">ʮ������û���� 
       <option value="365">һ��֮��û���� 
       <option value="730">����֮��û���� 
       </select><BR>���Ϸ�ʽ 
      <select name="delusetype"> 
      <option value="And">AND(�������Ϸ���)
      <option value="OR">OR(ĳһ���Ϸ���)
      </select> <BR>����ÿ�ν��д�����û��� <input type=text name="users" size=4 maxlength=4 value=500> ����޷�������ɣ��뾡�����������Ŀ���ӳ�����ʱ��<BR>

        <input type=submit value="Ԥ ɾ ��">
        </form>
        ~;
	if (-e "${lbdir}data/delmember.cgi") {
	    open (FILE, "${lbdir}data/delmember.cgi");
	    @delmembers = <FILE>;
	    close (FILE);
	    $delmembersize = @delmembers;
	    $delmembersize --;
	    $pretime=$delmembers[0];
		if ($delmembersize ne "0") {
	    chomp $pretime;
    	    $nowtime = time;
    	    $nowtime = $nowtime - 3*24*3600;
    	    if ($nowtime > $pretime) {
    	    	$oooput = qq~�����ϴ�Ԥɾ��ʱ���Ѿ����������� [<a href=$thisprog?action=delok>ȷ��ɾ��</a>]~;
    	    }
    	    else {
    	    	$oooput = qq~�����ϴ�Ԥɾ��ʱ�仹δ������ [<a href=$thisprog?action=delok>���ܣ�ǿ��ɾ��</a>]~;
    	    }
    	    $pretime=&dateformat($pretime);
    	    print qq~
        	�ϴ�Ԥɾ��ʱ�䣺$pretime (Ԥɾ���û������� $delmembersize ) [<a href=$thisprog?action=canceldel>ȡ��Ԥɾ��</a>]<BR>
        	$oooput [<a href=$thisprog?action=viewdelmembers>�鿴Ԥɾ����Ա�б�</a>]
    	    ~;
			} 
			else { #�A�h�����T�� 0 �r�Ԅ�ȡ�� 
			unlink ("${lbdir}data/delmember.cgi"); 
			print qq~ 
			Ԥɾ���ļ������ڣ����ڿ��Խ���Ԥɾ���� 
			~; 
			} 

	}
	else {
    	    print qq~
        	Ԥɾ���ļ������ڣ����ڿ��Խ���Ԥɾ����
    	    ~;
	}
    print qq~
    <BR><BR>
    </td>
    </tr>
    ~;
  }
    print qq~
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b>�鿴���༭��ɾ������ֹ�û�</b><br>
    ����������ĸ����Բ鿴���û���ϸ���ϣ� ���ɱ༭���ı��û�����Ϣ��<br>
    ��ֹ�û���ֻҪ�򵥵ĵ�����༭�û�����Ȼ���ڡ��û����ԡ���ѡ�񡰽�ֹ�û����Ϳ��ԡ�<br>
    ɾ���û���ֻҪ�ҵ��û������ɾ���Ϳ��ԡ�<br>
	<form action="setmembers.cgi" method=POST>
        <input type=hidden name="action" value="edit">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="���ٶ�λ">
        </form>
    
    ~;
    
    print qq~
    ע���û������б�<br>$tempoutput
<P><a href=$thisprog?action=viewip>Ѱ�����ض��ɣ�ע����û�</a>
    <p>ע��ɣд����б�<br>$tempoutput2
    </td>
    </tr>           
                
                
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><BR>
    <b>ע�����</b><p>
    �����ϣ���������û�һ���Զ����ͷ�Σ�ֻҪ�༭�������������ϡ�<br>
    �����̳���ô���ķ�������ȷ�����ǵĳ�Ա���.<br>
    ���������һ���û�Ϊ��������������ȴû���Զ����ͷ�Σ���ô�ͻ��Զ����һ������ͷ�Ρ�
    ����������Զ���ĵȼ�����ô����ԭͷ�ν���������<br>
    ����ֻ�ܹ������Լ�����̳����������Ҳ������������̳��ʹ�� #Moderation Mode �µĹ��ܡ�<br>
    ��ȷ�����������İ����ǿɿ��ġ�<br>
    ����Ҳ��̳��һ�������ܹ�ˮԤ���������ơ�<br>
    ֻ��̳�����ܹ�����������ġ�<br><br>
    ������ֹ��һ���û�����ôҲͬʱ��ֹ��������ԭ���ơ��ʼ�����ע��Ŀ��ܡ�
    </td>
    </tr>             
     ~;        
     
     } # end routne
     
     
##################################################################################
######## Subroutes (Do member count)  
sub canceldel {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {
	unlink ("${lbdir}data/delmember.cgi");
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>ȡ��Ԥɾ��</b><p>
        <font color=#333333>Ԥɾ���Ѿ���ȡ����</font>
        </td></tr>
         ~;
}
}
sub delnopost
{
	$step = $query->param('step');
	$step = 1 unless ($step);
	$size1 = $query->param('size1');
	$size1 = 0 unless($size1);	
	$users = $query->param('users');
	$users = 500 unless($users);	
	
    opendir (DIR, "${lbdir}$memdir/old"); 
    @files = readdir(DIR);
    closedir (DIR);
    @memberfiles = grep(/\.cgi$/i,@files);
    $size = @memberfiles;

	$currenttime = time;

	if (-e "${lbdir}data/delmember.cgi" && $step == 1)
	{
		print qq~
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000>
<b>�����û�����</b><p>
<font color=#333333>Ԥɾ���ļ����ڣ������ظ�Ԥɾ����</font>
</td></tr>~;
	}
	else
	{
  		if ($step == 1)
		{
			open (FILE, ">${lbdir}data/delmember.cgi");
			print FILE "$currenttime\t\n";
			close (FILE);
			unlink("${lbdir}data/lbmember.cgi");
		}

		$sendtoemail = "";
		open(MEMFILE, ">>${lbdir}data/lbmember.cgi");
		flock(MEMFILE, 2) if ($OS_USED eq "Unix");
		for ($i = ($step - 1) * $users; $i < $step * $users && $i < $size; $i++)
		{
			($nametocheck,$no) = split(/\./,$memberfiles[$i]);
			my $namenumber = &getnamenumber($nametocheck);
			&checkmemfile($nametocheck,$namenumber);
			$memberfile = $memberfiles[$i];
		    	$usrname="${lbdir}$memdir/$namenumber/$memberfile";
	    		open (FILE, "$usrname");
			flock (FILE, 2) if ($OS_USED eq "Unix");
			$line = <FILE>;
			close (FILE);
			undef $joineddate;
			undef $lastgone;
			undef $anzahl;
			undef $lastpostdate;
			undef $userad;
			undef $visitno;
			undef $anzahl1;
			undef $anzahl2;
			undef $emailaddr;
			undef $membername;

			($membername, $no, $no, $userad, $anzahl, $emailaddr, $no, $no, $no, $no, $no ,$no ,$no, $joineddate, $lastpostdate, $no, $timedifference, $no, $no, $no, $no, $no, $no, $no, $no, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/,$line);

			($anzahl1, $anzahl2) = split(/\|/,$anzahl);
			$anzahl = $anzahl1 + $anzahl2;
			($lastpost, $posturl, $posttopic) = split(/\%\%\%/, $lastpostdate);

			$lastgone = $lastpost   if ($lastpost > $lastgone);
			$lastgone = $joineddate if ($joineddate > $lastgone);

			$lastposttime = $lastpost; 
			$lastposttime = $joineddate if ($joineddate > $lastposttime);
			$lastposttime1 = $lastposttime + $indelcdrom*3600*24; 

			$lastgone1 = $lastgone + $indeltime*3600*24;

			$DelThisMember="no";
			if($delusetype eq "And")
			{
				$DelThisMember="yes" if (($lastgone1 <= $currenttime)&&($anzahl <= $indelposts)&&($lastposttime1 <= $currenttime));
			}
			else
			{
				$DelThisMember="yes" if (($lastgone1 <= $currenttime)||($anzahl <= $indelposts && $indelposts ne 9999999999)||($lastposttime1 <= $currenttime));
			}
			$DelThisMember="no" if(($userad eq "ad")||($userad eq "mo")||($userad eq "smo")||($userad eq "cmo")||($userad eq "amo")||($userad =~ /^rz/) || ($useradd5 eq "1"));
			if ($DelThisMember eq "yes")
			{
				if ($indellast ne "no")
				{
					if (($visitno <= $indellast)||($delusetype eq "OR"))
					{
						open(FILE, ">>${lbdir}data/delmember.cgi");
						flock(FILE, 2) if ($OS_USED eq "Unix");
						print FILE "$memberfile\t$lastgone\t\n";
						close(FILE);
						$size1++;
						if ($sendtoemail eq "") { $sendtoemail = "$emailaddr"; } else { $sendtoemail = "$sendtoemail, $emailaddr"; }
					}
				}
				else
				{
					open(FILE, ">>${lbdir}data/delmember.cgi");
					flock(FILE, 2) if ($OS_USED eq "Unix");
					print FILE "$memberfile\t$lastgone\t\n";
					close(FILE);
					$size1++;
					if ($sendtoemail eq "") { $sendtoemail = "$emailaddr"; } else { $sendtoemail = "$sendtoemail, $emailaddr"; }
				}
			}
			print MEMFILE "$membername\t$userad\t$anzahl\t$joineddate\t\n";
		} 
		close(MEMFILE);

		if ($sendtoemail ne "" && $emailfunctions eq "on")
		{
			$from = "$adminemail_out";
			$subject = "����$boardname����Ҫ�ʼ�����";
			$message = "";
			$message .= "\n";
			$message .= "$boardname <br>\n";
			$message .= "$boardurl/leobbs.cgi <br>\n";
			$message .= "------------------------------------------\n<br><br>\n";
			$message .= "ϵͳ�������Ѿ���ʱ��δ���ʱ���̳�������ˣ� <br>\n";
			$message .= "Ϊ���ͷſռ䣬����û������ڣ��պ�ɾ���� <br>\n";
			$message .= "������뱣������û��������¼����̳һ�Ρ� <br>\n";
			$message .= "------------------------------------------<br>\n";
			$message .= "LeoBBS �� www.leobbs.com ������Ʒ��<br>\n";
			&sendmail($from, $from, $sendtoemail, $subject, $message);
		}
		
		if ($i < $size - 1)
		{
			$step++;
		print qq~<meta http-equiv="refresh" Content="0; url=$thisprog?action=delnopost&deltime=$indeltime&delposts=$indelposts&dellast=$indellast&delcdrom=$indelcdrom&delusetype=$delusetype&size1=$size1&step=$step&users=$users">
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#333333><br>�������������û���Զ�ǰ������<a href=$thisprog?action=delnopost&deltime=$indeltime&delposts=$indelposts&dellast=$indellast&delcdrom=$indelcdrom&delusetype=$delusetype&size1=$size1&step=$step&users=$users>�������</a>
</td></tr>
~;
		}
		else
		{
			if ($size1 == 0)
			{
				$delwarn = "<BR><BR><font color=red><B>��ǰû�з���ɾ��������ע���Ա��<B></font>";
			}
			elsif ($emailfunctions ne "on")
			{
				$delwarn = "<BR><BR><font color=red><B>�ʼ�����û�д򿪣������û��޷�����Ԥɾ����Ϣ��<B></font>";
			}
			else
			{
				$delwarn = "";
			}

			unlink("${lbdir}data/delmember.cgi") if ($size1 eq 0);
			print qq~
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000>
<b>�����û�����</b><p>
<font color=#333333>��ǰ���� $size ��ע���û������������Ѿ����£�</font><BR>
<font color=#333333>Ԥɾ�� $size1 ��ע���û������������Ѿ����£��������Խ����������������ɾ����</font>
$delwarn
</td></tr>~;
		}
	}
} # end routine

sub delok {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>����</b><p>
                    
        <font color=#333333>��û��Ȩ��ʹ��������ܣ�</font>
                    
        </td></tr>
         ~;
}
else {

if ($checkaction eq "yes") {
	$step = $query->param('step');
	$step = 0 unless ($step);
	$users = $query->param('users');
	$users = 200 unless($users);	
	$delno = $query->param('delno');
	$delno = 0 unless($delno);	

        open (FILE, "${lbdir}data/delmember.cgi");
        @alldelname=<FILE>;
        close (FILE);
 	$delsize = @alldelname;

    opendir (DIRS, "$lbdir");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^\w+?$/i, @files);
    my @recorddir = grep(/^record/i, @files);
    $recorddir = $recorddir[0];
    my @memfavdir = grep(/^memfav/i, @files);
    $memfavdir = $memfavdir[0];
$from = "$adminemail_out";
$subject = "����$boardname����Ҫ�ʼ�����";
$message = "";
$message .= "\n";
$message .= "$boardname <br>\n";
$message .= "$boardurl/leobbs.cgi <br>\n";
$message .= "------------------------------------------\n<br><br>\n";
$message .= "ϵͳ�������Ѿ���ʱ��δ���ʱ���̳�������ˣ� <br>\n";
$message .= "Ϊ���ͷſռ䣬����û����Ѿ�����ȫɾ���� <br>\n";
$message .= "�����ͷŵ��û���Ϊ��membername�� <br>\n";
$message .= "------------------------------------------<br>\n";
$sendtoemail = "";

    if ($step*$users < $delsize) {
 	for ($i=$step*$users;$i<=($step+1)*$users;$i++) {
 	    last if ($i > $delsize);
	    ($memberfile, $deltime)= split(/\t/,$alldelname[$i]);

	    ($nametocheck,$no) = split(/\./,$memberfile);
	    my $namenumber = &getnamenumber($nametocheck);
	    &checkmemfile($nametocheck,$namenumber);
	    $usrname="${lbdir}$memdir/$namenumber/$memberfile";
	    open (FILE, "$usrname");
    	    $line = <FILE>;
    	    close (FILE);
	    undef $joineddate;
	    undef $lastgone;
	    undef $anzahl;
	    undef $lastpostdate;
	    undef $userad;
	    undef $visitno;
	    undef $anzahl1;
	    undef $anzahl2;
	    undef $emailaddr;
	    undef $membername;

    	    ($membername, $no, $no, $userad, $anzahl, $emailaddr, $no, $no, $no, $no, $no ,$no ,$no, $joineddate, $lastpostdate, $no, $timedifference, $no, $no, $no, $no, $no, $no, $no, $no, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/,$line);
	$messageto = $message;
	$messageto =~ s/membername/$membername/isg;
	    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
	    $anzahl = $anzahl1 + $anzahl2;
	    ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	    $lastgone = $lastpost   if ($lastpost > $lastgone);
	    $lastgone = $joineddate if ($joineddate > $lastgone);
	    
	    $delbankno = 0;
	    $delbanksaves = 0;
	    if ($lastgone <= $deltime) {
	        $membername =~ s/ /\_/isg;
		$membername =~ tr/A-Z/a-z/;
		my $namenumber = &getnamenumber($membername);
		&checkmemfile($membername,$namenumber);
	        unlink ("${lbdir}$memdir/$namenumber/$membername.cgi");
	        unlink ("${lbdir}$memdir/old/$membername.cgi");
        	unlink ("${lbdir}$msgdir/in/${membername}_msg.cgi");
	        unlink ("${lbdir}$msgdir/out/${membername}_out.cgi");
        	unlink ("${lbdir}$msgdir/main/${membername}_mian.cgi");
	        unlink ("${lbdir}$memfavdir/$membername.cgi");
        	unlink ("${lbdir}$memfavdir/open/$membername.cgi");
	        unlink ("${lbdir}$memfavdir/close/$membername.cgi");
        	unlink ("${lbdir}memfriend/$membername.cgi");
        	unlink ("${lbdir}$recorddir/post/$membername.cgi");
      		unlink ("${lbdir}$recorddir/reply/$membername.cgi");
        	unlink ("${lbdir}memblock/$membername.cgi");
        	unlink ("${lbdir}cache/myinfo/$membername.cgi");
        	unlink ("${lbdir}cache/meminfo/$membername.cgi");
        	unlink ("${lbdir}cache/id/$membername.cgi");
	    	unlink ("${imagesdir}usravatars/$membername.gif");
    		unlink ("${imagesdir}usravatars/$membername.png");
	    	unlink ("${imagesdir}usravatars/$membername.jpg");
    		unlink ("${imagesdir}usravatars/$membername.swf");
	    	unlink ("${imagesdir}usravatars/$membername.bmp");
    	$memberfiletitletemp = unpack("H*","$membername");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.gif");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.png");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.jpg");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.swf");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.bmp");
		unlink ("${lbdir}ebankdata/log/" . $membername . ".cgi");
		my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $bankadd1, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
		if ($mystatus)
		{
			$delbankno++;
			$delbanksaves += $mysaves;
		}

	        $delno ++;
	  	if ($sendtoemail eq "") { $sendtoemail = $emailaddr; } else { $sendtoemail = "$sendtoemail, $emailaddr"; }
	    }
	    &updateallsave(-$delbankno, -$delbanksaves);
 	}
 	
  	if (($emailfunctions eq "on")&&($sendtoemail ne "")) {
            &sendmail($from, $from, $sendtoemail, $subject, $messageto);
        }
	$step++;
	print qq~<meta http-equiv="refresh" Content="0; url=$thisprog?action=delok&checkaction=yes&delno=$delno&step=$step&users=$users">
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#333333><br>�������������û���Զ�ǰ������<a href=$thisprog?action=delok&checkaction=yes&delno=$delno&step=$step&users=$users>�������</a>
</td></tr>
			~;

    } else {

 	 	
        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers=$totalmembers - $delno;
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

        # Delete the database for the member

	unlink ("${lbdir}data/delmember.cgi");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>$delno ������ע���û��Ѿ�������ɾ��<BR>
        �û����Ѿ�ȫ������</b><br><Br><a href=foruminit.cgi?action=uptop>����������û�����һ��</a><br>
        </td></tr>
         ~;
    }
}

else {
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���棡��</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>��ȫɾ�����з���������Ԥɾ���û��������������Ӽ�����<BR>
        ��Ԥɾ���ڼ���ʹ���̳���û����ᱻɾ��<p>
        <p>
        >> <a href="$thisprog?action=delok&checkaction=yes">��ʼɾ��</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
        }
}
} # end routine

sub viewletter {

open (FILE, "$lbdir/data/lbmember1.cgi");
my @membernames = <FILE>;
close (FILE);
undef @sortedfile;
foreach (@membernames) {
    chomp $_;
    ($no,$names) = split(/\t/,$_);
    push (@sortedfile, $names);
}

    @sortedfile = sort alphabetically(@sortedfile);
    
    foreach (@sortedfile) {
    	if ($_ =~ /^[\w\-]/) {
        $fr = substr($_, 0, 1);
        $fr =~ tr/a-z/A-Z/;
        }
        else {
           $fr =substr($_, 0, 2);
        }
        push(@letters,$fr);
        }
    @sortedletters = sort(@letters);

    print qq~
    <tr>
    <td bgcolor=#EEEEEE colspan=2><center>
    <font color=#990000><b>�鿴������ "$inletter" ��ͷ���û�</b><p>
	<form action="setmembers.cgi" method=POST>
        <input type=hidden name="action" value="edit">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="���ٶ�λ">
        </form>
</center>
    ~;

    print qq~
    </td>
    </tr>          
    <tr>
    <td bgcolor=#FFFFFF align=center colspan=2>
    &nbsp;
    </td>
    </tr>          
    ~;
               
               
    foreach (@sortedfile) {
    	if ($_ =~ /^[\w\-]/) {
        $frr = substr($_, 0, 1);
        $frr =~ tr/a-z/A-Z/;
        }
        else {
           $frr =substr($_, 0, 2);
        }
        if ($inletter eq $frr) {
            $_ =~ s/\.cgi$//;
            $member = $_;
            &getmember("$member");
            &showmember;
            }
        }
        
   } # end route

sub viewip {
    unless($inletter eq "findsame"){
	$inletters=$inletter;
	$inletter=($inletter !~/\./)?$inletter.".":$inletter;
	$inletter=~s/\./\\\./g;
	}
    %iplist=();%sameiplist=();@thatiplist=();
open (FILE, "$lbdir/data/lbmember4.cgi");
my @ipfile = <FILE>;
close (FILE);
chomp @ipfile;
	foreach(@ipfile){
		(my $membername,my $getip)=split(/\t/,$_);
		if($inletter ne "findsame"){
			push (@thatiplist,$membername) if($getip =~/^$inletter/);
		}else{
			$sameiplist{$getip}="" unless(defined($sameiplist{$getip}));
			$sameiplist{$getip}.=qq(<a href="$thisprog?action=edit&member=$membername">$membername</a>,);
		}
		($getip,$getip2)=split(/, /,$getip);
		$getip = $getip2 if (($getip2 ne "")&&($getip2 ne "unknown"));
		$getip=~s/\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$//;
		$iplist{$getip}="$getip" unless(defined($iplist{$getip}));
	}
	@iplist=keys %iplist;
    @iplist = sort(@iplist);
    
    print qq~
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>Ѱ�����ض��ɣ�ע����û�</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=left colspan=2>��������������������<b>˵��:</b><br>
�������������������������ҪѰ��һ�� IP������ֱ������ IP ��ַ��������磺 202.100.200.100��<br>
�������������������������ҪѰ��һ�� C ��������ô����Բ����� IP �����һλ�����磺202.100.200. <br>
�������������������������ҪѰ��һ�� B ��������ô����Բ����� IP �������λ�����磺202.100. <br>
��������������������ע�������д�������Ѱ�ҵ���һ�� C ����� B ����������������(.)���мǣ�</td></tr>
    <tr>
    <form action="setmembers.cgi" method=POST><input type=hidden name="action" value="viewip"><td bgcolor=#EEEEEE align=center colspan=2><input type=text name="letter" size20 maxlength=16> <input type=submit value="Ѱ���û�"></td></form></tr>
    <tr>
    <form action="setmembers.cgi" method=POST><input type=hidden name="action" value="viewip"><input type=hidden name="letter" value="findsame"><td bgcolor=#EEEEEE align=center colspan=2><input type=submit value="Ѱ��������ͬ�ɣе��û�"></td></form></tr>
    <tr><td bgcolor=#FFFFFF align=center colspan=2 height="20"></td></tr>
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>ע��ɣд����б�</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=left colspan=2>��������������������~;

    $nowcount =0;
    foreach (@iplist) {
        	$ipshow=sprintf("% 3s",$_);
        	$ipshow=~s/\s/\&nbsp\;/g;
            print qq~<br>��������������������~ if ($nowcount == int($nowcount/15)*15);
            print qq~ <a href="$thisprog?action=viewip&letter=$_">$ipshow</a> ~;
            $nowcount ++;
    }

    print qq~$tempoutput</td></tr>
    <tr><td bgcolor=#FFFFFF align=center colspan=2 height="20"></td></tr>~;
    if($inletter ne "findsame"){
    print qq~
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>���Уɣ��� "$inletters" ��ͷ���û�</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=center colspan=2 height="20"></td></tr>
    ~;
		foreach (@thatiplist) {
			$member = $_;
			&getmember("$member");
			&showmember;
			}
    }else{
    print qq~
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>������ͬ�ɣе��û�</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=left colspan=2>��������������������<b>ע��:</b><br>
����������������������ͬ�ɣв�һ��������ͬһ�ˡ�<br></td></tr>
    ~;
		while(($ip,$thisiplist)=each(%sameiplist)){
			my @listofthisip=split(/\,/,$thisiplist);
			my $listofthisipc=@listofthisip;
			next if($listofthisipc <= 1);
			$listofthisip=join(",",@listofthisip);
    print qq~
    <tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�ɣ�Ϊ "<font color=#990000>$ip</font>" ���û�</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF colspan=2 align=left>$listofthisip</td></tr>
    <tr><td bgcolor=#FFFFFF> </td><td bgcolor=#FFFFFF> </td></tr>
    ~;
		}
	}
}


##################################################################################
######## Subroutes (Show member) 


sub showmember {

    $joineddate = &longdate("$joineddate");
    
    $cleanmember = $member;
    $cleanmember =~ s/\_/ /g;
    
    ## Sort last post, and where
    
    ($postdate, $posturl, $posttopic) = split(/\%%%/,$lastpostdate);
    
    if ($postdate ne "û�з����") {
        $postdate = &longdate("$postdate");
        $lastpostdetails = qq~��󷢱� <a href="$posturl">$posttopic</a> �� $postdate~;
        }
        else {
            $lastpostdetails = "û�з����";
            }

    if ($membercode eq "banned") {
        $unbanlink = qq~ | [<a href="$thisprog?action=unban&member=~ . uri_escape($member) . qq~">ȡ����ֹ����</a>]~;
        }
    $totlepostandreply = $numberofposts+$numberofreplys;
    print qq~
    <tr>
    <td bgcolor=#EEEEEE colspan=2 align=center><font face=$font color=$fontcolormisc><b><font color=$fonthighlight>"$cleanmember"</b> ����ϸ���� �� [ <a href="$thisprog?action=edit&member=~ . uri_escape($member) . qq~">�༭</a> ] | [ <a href="$thisprog?action=deletemember&member=~ . uri_escape($member) . qq~">ɾ��</a> ]$unbanlink</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF width=30%><font color=#333333><b>ע��ʱ�䣺</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF width=30%><font color=#333333><b>ע��ɣУ�</b></font></td>
    <td bgcolor=#FFFFFF><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$ipaddress',420,320)" title="LB WHOIS��Ϣ"><font color=#333333>$ipaddress</font></span> (<a href="$thisprog?action=viewip&letter=$ipaddress">����ͬ�ɣе��û�</a>)</td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�û�ͷ�Σ�</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$membertitle</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��󷢱�</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastpostdetails</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����������</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$totlepostandreply</font> ƪ</td></tr>
    <tr>
    <td bgcolor=#FFFFFF>&nbsp;</td>
    <td bgcolor=#FFFFFF>&nbsp;</td></tr>
    
    ~;
    $unbanlink = "";
    } # end routine


##################################################################################
######## Subroutes (Edit member) 


sub edit {
    $oldmembercode = $membercode;
    
    if ($checkaction eq "yes") {
    
    
    $innewpassword      = $query -> param('password');
    $innewpassword      = &cleanarea("$innewpassword");
    $inrating           = $query -> param('rating');
    $inmembertitle      = $query -> param('membertitle');
    $inmembertitle      = &cleanarea("$inmembertitle");
    $inemailaddress     = $query -> param('emailaddress');
    $inhomepage         = $query -> param('homepage');
    $inoicqnumber          = $query -> param('oicqnumber');
    $inicqnumber        = $query -> param('icqnumber');
    $inlocation         = $query -> param('location');
    $innumberofposts    = $query -> param('numberofposts');
    $innumberofreplys   = $query -> param('numberofreplys');
    $intimedifference   = $query -> param('timedifference');
    $inmembercode       = $query -> param('membercode');
    $inmembercode       = &cleaninput("$inmembercode");
    $invisitno          = $query -> param('visitno');
    $injhmp             = $query -> param('jhmp');
    $injifen            = $query -> param('jifen');
    $inmymoney          = $query -> param('mymoney');
    $insex              = $query -> param('sex');
    $ineducation        = $query -> param('education');
    $inmarry            = $query -> param('marry');
    $inwork             = $query -> param('work');
    $inyear             = $query -> param('year');
    $inmonth            = $query -> param('month');
    $inday              = $query -> param('day');
    $inpostdel          = $query -> param('postdel');
    $newsignature       = $query -> param('newsignature');
    $notshowsignature      = ($query -> param('notshowsignature') eq "yes")?"yes":"no";
    $inuserflag         = $query -> param('userflag');
    $inusersx           = $query -> param('usersx');
    $inuserxz           = $query -> param('userxz');
    $injoineddate       = $query -> param('joineddate');
    $newsignature           = &unHTML("$newsignature");
    $newsignature           = &cleanarea("$newsignature");

    $inlocation = &cleaninput("$inlocation");
    $inonlinetime = $query -> param('onlinetime');

   $inuseradd1         = $query -> param('useradd1');
   $tinuseradd1        = $query -> param('tuseradd1');
   $tinuseradd2        = $query -> param('tuseradd2');
   $tinuseradd3        = $query -> param('tuseradd3');
   $tinuseradd4        = $query -> param('tuseradd4');
   $tinuseradd5        = $query -> param('tuseradd5');
   $tinuseradd6        = $query -> param('tuseradd6');

   $inawards=("$tinuseradd1:$tinuseradd2:$tinuseradd3:$tinuseradd4:$tinuseradd5:$tinuseradd6");

    $inyear =~ s/\D//g;
    if (($inyear eq "")||($inmonth eq "")||($inday eq "")) {
    	$inyear  = "";
    	$inmonth = "";
    	$inday   = "";
    }
    $inborn = "$inyear/$inmonth/$inday";
    
    if ($inborn ne "//") { #��ʼ�Զ��ж�����
    	if ($inmonth eq "01") {
    	    if (($inday >= 1)&&($inday <=19)) {
    	        $inuserxz = "z10";
    	    }
    	    else {
    	        $inuserxz = "z11";
    	    }
    	}
        elsif ($inmonth eq "02") {
    	    if (($inday >= 1)&&($inday <=18)) {
    	        $inuserxz = "z11";
    	    }
    	    else {
    	        $inuserxz = "z12";
    	    }
        }
        elsif ($inmonth eq "03") {
    	    if (($inday >= 1)&&($inday <=20)) {
    	        $inuserxz = "z12";
    	    }
    	    else {
    	        $inuserxz = "z1";
    	    }

        }
        elsif ($inmonth eq "04") {
    	    if (($inday >= 1)&&($inday <=19)) {
    	        $inuserxz = "z1";
    	    }
    	    else {
    	        $inuserxz = "z2";
    	    }
        }
        elsif ($inmonth eq "05") {
    	    if (($inday >= 1)&&($inday <=20)) {
    	        $inuserxz = "z2";
    	    }
    	    else {
    	        $inuserxz = "z3";
    	    }
        }
        elsif ($inmonth eq "06") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z3";
    	    }
    	    else {
    	        $inuserxz = "z4";
    	    }
        }
        elsif ($inmonth eq "07") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z4";
    	    }
    	    else {
    	        $inuserxz = "z5";
    	    }
        }
        elsif ($inmonth eq "08") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z5";
    	    }
    	    else {
    	        $inuserxz = "z6";
    	    }
        }
        elsif ($inmonth eq "09") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z6";
    	    }
    	    else {
    	        $inuserxz = "z7";
    	    }
        }
        elsif ($inmonth eq "10") {
    	    if (($inday >= 1)&&($inday <=23)) {
    	        $inuserxz = "z7";
    	    }
    	    else {
    	        $inuserxz = "z8";
    	    }
        }
        elsif ($inmonth eq "11") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z8";
    	    }
    	    else {
    	        $inuserxz = "z9";
    	    }
        }
        elsif ($inmonth eq "12") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z9";
    	    }
    	    else {
    	        $inuserxz = "z10";
    	    }
        }
        
    }

    $inmembertitle = "Member" if ($inmembertitle eq "");

    if (length($injhmp) > 21) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>�������ɵ������������20���ַ���10�����֣��ڡ�</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    if (length($inmembertitle) > 21) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>����ͷ�ε������������20���ַ���10�����֣��ڡ�</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    if (length($inlocation) > 12) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>���Ե������������12���ַ���6�����֣��ڡ�</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }

    if ($injhmp eq "") { $jhmp = "��������"; }
    else { $jhmp = ($jhmp); }
    if ($inrating eq "") { $inrating = 0; }
    elsif ($inrating > $maxweiwang) { $inrating = $maxweiwang; }
    elsif ($inrating < -6) { $inrating = -6 ; $inmembercode = "banned"; }

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        open(FILE,"$filetoopen");
        @forums = <FILE>;
        close(FILE);
        
        foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $trash) = split(/\t/,$forum);
            $namekey = "allow" . "$forumid";
            $tocheck = $query -> param("$namekey");
            if ($tocheck eq "yes") {
                $allowedforums2 .= "$forumid=$tocheck&";
                }
            }
            
        &getmember("$inmember");
        if ($innewpassword eq "") { $innewpassword = $password; }
        else {

        if ($innewpassword =~ /[^a-zA-Z0-9]/) { print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>����ֻ�����Сд��ĸ�����ֵ���ϣ���</b></td></tr>"; exit; }
        if ($innewpassword =~ /^lEO/) { print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>���벻������ lEO ��ͷ�����������</b></td></tr>"; exit; }
        if (length($innewpassword)<8) { print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>����̫���ˣ��������������� 8 λ���ϣ�</b></td></tr>"; exit; }
if ($innewpassword ne "") {
    eval {$innewpassword = md5_hex($innewpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$innewpassword = md5_hex($innewpassword);');}
    unless ($@) {$innewpassword = "lEO$innewpassword";}
}
    }
    
    if ((($inmembercode eq "ad")||($inmembercode eq "smo")||($inmembercode eq "cmo")||($inmembercode eq "amo")||($inmembercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�ܰ�����Ȩ�����κ���Ϊ̳���Ͱ���</b></td></tr>";
            exit;
    }

        $memberfiletitle = $inmember;
        $memberfiletitle =~ s/ /\_/isg;
	$memberfiletitle =~ tr/A-Z/a-z/;
	unlink ("${lbdir}cache/meminfo/$memberfiletitle.pl");
	unlink ("${lbdir}cache/myinfo/$memberfiletitle.pl");

        if ($inmembercode eq "banned") {
            $filetoopen = "$lbdir" . "data/banemaillist.cgi";
            open(FILE,">>$filetoopen");
            print FILE "$inemailaddress\t";
            close(FILE);
            $filetoopen = "$lbdir" . "data/baniplist.cgi";
            open(FILE,">>$filetoopen");
            print FILE "$ipaddress\t";
            close(FILE);
            $banresult = "��ֹ $membername ���Գɹ�";
       }
	if ($oldmembercode eq "smo") {
$innumberofposts = $numberofposts;
$innumberofreplys = $numberofreplys;
$inpostdel = $postdel;
$inmymoney = $mymoney;
$invisitno = $visitno;
$inawards = $awards;
	}
        if ($newsignature) {
        $newsignature =~ s/\t//g;
        $newsignature =~ s/\r//g;
        $newsignature =~ s/  / /g;
        $newsignature =~ s/\&amp;nbsp;/\&nbsp;/g;
        $newsignature =~ s/\n\n/\n\&nbsp;\n/isg;
        $newsignature =~ s/\n/\[br\]/isg;
        $newsignature =~ s/\[br\]\[br\]/\[br\]\&nbsp;\[br\]/isg;
        }
	require "dosignlbcode.pl";
	$signature1=&signlbcode($newsignature); 
       	$newsignature=$newsignature."aShDFSiod".$signature1;
       	$onlinetime=($inonlinetime =~/[^0-9]/)?$onlinetime:$inonlinetime;
       	my $namenumber = &getnamenumber($memberfiletitle);
	&checkmemfile($memberfiletitle,$namenumber);
        unless ((-e "${lbdir}$memdir/$namenumber/$memberfiletitle.cgi")||(-e "${lbdir}$memdir/old/$memberfiletitle.cgi")) { print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>���û������ڣ�</b></td></tr>"; exit; }
        $filetomake = "$lbdir" . "$memdir/$namenumber/$memberfiletitle.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$innewpassword\t$inmembertitle\t$inmembercode\t$innumberofposts|$innumberofreplys\t$inemailaddress\t$showemail\t$ipaddress\t$inhomepage\t$inoicqnumber\t$inicqnumber\t$inlocation\t$interests\t$injoineddate\t$lastpostdate\t$newsignature\t$intimedifference\t$allowedforums2\t$useravatar\t$inuserflag\t$inuserxz\t$inusersx\t$personalavatar\t$personalwidth\t$personalheight\t$inrating\t$lastgone\t$invisitno\t$inuseradd04\t$inuseradd02\t$inmymoney\t$inpostdel\t$insex\t$ineducation\t$inmarry\t$inwork\t$inborn\t$chatlevel\t$chattime\t$injhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$inawards\t$injifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
        open(FILE, ">${lbdir}$memdir/old/$memberfiletitle.cgi");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$innewpassword\t$inmembertitle\t$inmembercode\t$innumberofposts|$innumberofreplys\t$inemailaddress\t$showemail\t$ipaddress\t$inhomepage\t$inoicqnumber\t$inicqnumber\t$inlocation\t$interests\t$injoineddate\t$lastpostdate\t$newsignature\t$intimedifference\t$allowedforums2\t$useravatar\t$inuserflag\t$inuserxz\t$inusersx\t$personalavatar\t$personalwidth\t$personalheight\t$inrating\t$lastgone\t$invisitno\t$inuseradd04\t$inuseradd02\t$inmymoney\t$inpostdel\t$insex\t$ineducation\t$inmarry\t$inwork\t$inborn\t$chatlevel\t$chattime\t$injhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$inawards\t$injifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
if($oldmembercode ne "smo"){ 
       my $notshowsignaturefile = "$lbdir" . "data/notshowsignature.cgi"; 
       if(open(FILE,"$notshowsignaturefile")){ 
       $notshowsignaturemember = <FILE>; 
       close(FILE); 
       } 
       $notshowsignaturemember1=$notshowsignaturemember; 
       $notshowsignaturemember1=~s/^\t//; 
       $notshowsignaturemember1=~s/\t$//; 
       $notshowsignaturemember1="\t$notshowsignaturemember\t"; 
       if($notshowsignature eq "yes"){ 
       if($notshowsignaturemember1 !~/\t$membername\t/){ 
       open(FILE,">$notshowsignaturefile"); 
       print FILE "$notshowsignaturemember$membername\t"; 
       close(FILE); 
       $banresult.="<br>���� $membername ǩ���ɹ�"; 
       } 
       }else{ 
       if($notshowsignaturemember1 =~/\t$membername\t/){ 
       $notshowsignaturemember=~s/$membername\t//i; 
       open(FILE,">$notshowsignaturefile"); 
       print FILE "$notshowsignaturemember"; 
       close(FILE); 
       $banresult.="<br>���� $membername ǩ���ɹ�"; 
       } 
       } 
   }

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata1 = grep(/^forumstopic/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
   
                print qq~
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>������Ϣ�Ѿ�����</b><br><br>$banresult<br>
                </td></tr>
                ~;
    
    }
    
    else {
    
    $filetoopen = "$lbdir" . "data/allforums.cgi";
         open(FILE,"$filetoopen");
         @forums = <FILE>;
         close(FILE);

         
         foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);   
            if ($privateforum eq "yes") { 
                $grab = "$forumid\t$forumname";
                push(@newforums, $grab);
                }
            }
        $cleanmember = $inmember;
        $cleanmember =~ s/\_/ /g;
    
        &getmember("$inmember");
        $inmemberencode = uri_escape($inmember);
	$signature=$signatureorigin if ($signatureorigin);
	$signature="" if (($signatureorigin eq "")&&($signaturehtml eq ""));
	$signature =~ s/\[br\]/\n/isg;
        $signature =~ s/<br>/\n/isg;
        $signature =~ s/<p>/\n/isg;
        $signature =~ s/</&lt;/g;
        $signature =~ s/>/&gt;/g;
        $signature =~ s/\&amp;/\&/isg;
        $signature =~ s/&quot\;/\"/g;
        $signature =~ s/\&nbsp;/ /isg;
        if($privateforums) {
            @private = split(/&/,$privateforums);
            foreach $accessallowed (@private) {
                chomp $accessallowed;
                ($access, $value) = split(/=/,$accessallowed);
                $allowedentry2{$access} = $value;
                }
            }
    
        @allowedforums = sort alphabetically(@newforums);
        foreach $line (@allowedforums) {
            ($forumid, $forumname) = split(/\t/,$line);
            if ($allowedentry2{$forumid} eq "yes") { $checked = " checked"; }
            else { $checked = ""; }
            $privateoutput .= qq~<input type="checkbox" name="allow$forumid" value="yes" $checked>$forumname<br>\n~;
            }
            
    my $memteam1 = qq~<option value="rz1">$defrz1(��֤�û�)~ if ($defrz1 ne "");
    my $memteam2 = qq~<option value="rz2">$defrz2(��֤�û�)~ if ($defrz2 ne "");
    my $memteam3 = qq~<option value="rz3">$defrz3(��֤�û�)~ if ($defrz3 ne "");
    my $memteam4 = qq~<option value="rz4">$defrz4(��֤�û�)~ if ($defrz4 ne "");
    my $memteam5 = qq~<option value="rz5">$defrz5(��֤�û�)~ if ($defrz5 ne "");
    $memberstateoutput = qq~<select name="membercode"><option value="me">һ���û�$memteam1$memteam2$memteam3$memteam4$memteam5<option value="rz">��֤�û�<option value="banned">��ֹ���û�����<option value="masked">���δ��û�����<option value="mo">��̳����<option value="amo">��̳������<option value="cmo">����������<option value="smo">��̳�ܰ��� *<option value="ad">̳�� **</select>~;
    
    $memberstateoutput =~ s/value=\"$membercode\"/value=\"$membercode\" selected/g;
        if ($userregistered eq "no") {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�޴��û���</b></td></tr>";
            exit;
        }
    
    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "amo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�ܰ�����Ȩ�鿴̳���Ͱ������ϣ�</b></td></tr>";
            exit;
    }
$userflag = "blank" if ($userflag eq "");
$flaghtml = qq~
<script language="javascript">
function showflag(){document.images.userflags.src="$imagesurl/flags/"+document.creator.userflag.options[document.creator.userflag.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>���ڹ���:</b></td>
<td bgcolor=#ffffff>
<select name="userflag" size=1 onChange="showflag()">
<option value="blank">����</option>
<option value="China">�й�</option>
<option value="Angola">������</option>
<option value="Antigua">�����</option>
<option value="Argentina">����͢</option>
<option value="Armenia">��������</option>
<option value="Australia">�Ĵ�����</option>
<option value="Austria">�µ���</option>
<option value="Bahamas">�͹���</option>
<option value="Bahrain">����</option>
<option value="Bangladesh">�ϼ���</option>
<option value="Barbados">�ͰͶ�˹</option>
<option value="Belgium">����ʱ</option>
<option value="Bermuda">��Ľ��</option>
<option value="Bolivia">����ά��</option>
<option value="Brazil">����</option>
<option value="Brunei">����</option>
<option value="Canada">���ô�</option>
<option value="Chile">����</option>
<option value="Colombia">���ױ���</option>
<option value="Croatia">���޵���</option>
<option value="Cuba">�Ű�</option>
<option value="Cyprus">����·˹</option>
<option value="Czech_Republic">�ݿ�˹�工��</option>
<option value="Denmark">����</option>
<option value="Dominican_Republic">�������</option>
<option value="Ecuador">��϶��</option>
<option value="Egypt">����</option>
<option value="Estonia">��ɳ����</option>
<option value="Finland">����</option>
<option value="France">����</option>
<option value="Germany">�¹�</option>
<option value="Great_Britain">Ӣ��</option>
<option value="Greece">ϣ��</option>
<option value="Guatemala">Σ������</option>
<option value="Honduras">�鶼��˹</option>
<option value="Hungary">������</option>
<option value="Iceland">����</option>
<option value="India">ӡ��</option>
<option value="Indonesia">ӡ��������</option>
<option value="Iran">����</option>
<option value="Iraq">������</option>
<option value="Ireland">������</option>
<option value="Israel">��ɫ��</option>
<option value="Italy">�����</option>
<option value="Jamaica">�����</option>
<option value="Japan">�ձ�</option>
<option value="Jordan">Լ��</option>
<option value="Kazakstan">������</option>
<option value="Kenya">������</option>
<option value="Kuwait">������</option>
<option value="Latvia">����ά��</option>
<option value="Lebanon">�����</option>
<option value="Lithuania">������</option>
<option value="Malaysia">��������</option>
<option value="Malawi">����ά</option>
<option value="Malta">�����</option>
<option value="Mauritius">ë����˹</option>
<option value="Morocco">Ħ���</option>
<option value="Mozambique">Īɣ�ȿ�</option>
<option value="Netherlands">����</option>
<option value="New_Zealand">������</option>
<option value="Nicaragua">�������</option>
<option value="Nigeria">��������</option>
<option value="Norway">Ų��</option>
<option value="Pakistan">�ͻ�˹̹</option>
<option value="Panama">������</option>
<option value="Paraguay">������</option>
<option value="Peru">��³</option>
<option value="Poland">����</option>
<option value="Portugal">������</option>
<option value="Romania">��������</option>
<option value="Russia">���</option>
<option value="Saudi_Arabia">ɳ�ذ�����</option>
<option value="Singapore">�¼���</option>
<option value="Slovakia">˹�工��</option>
<option value="Slovenia">˹��������</option>
<option value="Solomon_Islands">������</option>
<option value="Somalia">������</option>
<option value="South_Africa">�Ϸ�</option>
<option value="South_Korea">����</option>
<option value="Spain">������</option>
<option value="Sri_Lanka">ӡ��</option>
<option value="Surinam">������</option>
<option value="Sweden">���</option>
<option value="Switzerland">��ʿ</option>
<option value="Thailand">̩��</option>
<option value="Trinidad_Tobago">��͸�</option>
<option value="Turkey">������</option>
<option value="Ukraine">�ڿ���</option>
<option value="United_Arab_Emirates">����������������</option>
<option value="United_States">����</option>
<option value="Uruguay">������</option>
<option value="Venezuela">ί������</option>
<option value="Yugoslavia">��˹����</option>
<option value="Zambia">�ޱ���</option>
<option value="Zimbabwe">��Ͳ�Τ</option>
</select>
<img src="$imagesurl/flags/$userflag.gif" name="userflags" border=0 height=14 width=21>
</td></tr>
~;
$flaghtml =~ s/value=\"$userflag\"/value=\"$userflag\" selected/;

        if ($userxz eq "") {$userxz = "blank"};
        $xzhtml =qq~
        <SCRIPT language=javascript>
        function showxz(){document.images.userxzs.src="$imagesurl/star/"+document.creator.userxz.options[document.creator.userxz.selectedIndex].value+".gif";}
        </SCRIPT>
	<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>����������</b>��ѡ����������������<br>������������յĻ�����ô������Ч��</td>
	<td bgcolor=#ffffff>
        <SELECT name=\"userxz\" onchange=showxz() size=\"1\"> <OPTION value=blank>����</OPTION> <OPTION value=\"z1\">������(3��21--4��19��)</OPTION> <OPTION value=\"z2\">��ţ��(4��20--5��20��)</OPTION> <OPTION value=\"z3\">˫����(5��21--6��21��)</OPTION> <OPTION value=\"z4\">��з��(6��22--7��22��)</OPTION> <OPTION value=\"z5\">ʨ����(7��23--8��22��)</OPTION> <OPTION value=\"z6\">��Ů��(8��23--9��22��)</OPTION> <OPTION value=\"z7\">�����(9��23--10��23��)</OPTION> <OPTION value=\"z8\">��Ы��(10��24--11��21��)</OPTION> <OPTION value=\"z9\">������(11��22--12��21��)</OPTION> <OPTION value=\"z10\">ħ����(12��22--1��19��)</OPTION> <OPTION value=\"z11\">ˮƿ��(1��20--2��18��)</OPTION> <OPTION value=\"z12\">˫����(2��19--3��20��)</OPTION></SELECT> <IMG border=0 height=15 name=userxzs src=$imagesurl/star/$userxz.gif width=15 align=absmiddle>
        </TD></TR>
	~;
        $xzhtml =~ s/value=\"$userxz\"/value=\"$userxz\" selected/;

        if ($usersx eq "") {$usersx = "blank"};
        $sxhtml =qq~
        <SCRIPT language=javascript>
        function showsx(){document.images.usersxs.src="$imagesurl/sx/"+document.creator.usersx.options[document.creator.usersx.selectedIndex].value+".gif";}
        </SCRIPT>
	<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>������Ф��</b>��ѡ������������Ф��</td>
	<td bgcolor=#ffffff>
        <SELECT name=\"usersx\" onchange=showsx() size=\"1\"> <OPTION value=blank>����</OPTION> <OPTION value=\"sx1\">����</OPTION> <OPTION value=\"sx2\">��ţ</OPTION> <OPTION value=\"sx3\">����</OPTION> <OPTION value=\"sx4\">î��</OPTION> <OPTION value=\"sx5\">����</OPTION> <OPTION value=\"sx6\">����</OPTION> <OPTION value=\"sx7\">����</OPTION> <OPTION value=\"sx8\">δ��</OPTION> <OPTION value=\"sx9\">���</OPTION> <OPTION value=\"sx10\">�ϼ�</OPTION> <OPTION value=\"sx11\">�繷</OPTION> <OPTION value=\"sx12\">����</OPTION></SELECT> <IMG border=0 name=usersxs src=$imagesurl/sx/$usersx.gif align=absmiddle>
        </TD></TR>
	~;
        $sxhtml =~ s/value=\"$usersx\"/value=\"$usersx\" selected/;
        if ($avatars eq "on") {
	    if (($personalavatar)&&($personalwidth)&&($personalheight)) { #�Զ���ͷ�����
	    	$personalavatar =~ s/\$imagesurl/${imagesurl}/o;
	        if (($personalavatar =~ /\.swf$/i)&&($flashavatar eq "yes")) {
	            $personalavatar=uri_escape($personalavatar);
		    $useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>��[ <a href="$thisprog?action=deleteavatar&member=$inmemberencode">ɾ �� ͷ ��</a> ]);
	        }
	        else {
	            $personalavatar=uri_escape($personalavatar);
		    $useravatar = qq(<br>&nbsp; <img src=$personalavatar border=0 width=$personalwidth height=$personalheight>��[ <a href="$thisprog?action=deleteavatar&member=$inmemberencode">ɾ �� ͷ ��</a> ]);
	        }
	    }
            elsif (($useravatar ne "noavatar") && ($useravatar)) {
		$useravatar=uri_escape($useravatar);
                $useravatar = qq(<br>&nbsp; <img src="$imagesurl/avatars/$useravatar.gif" border=0 $defaultwidth $defaultheight>);
            }
            else {$useravatar="û��"; }
        }
   $inmembert=$inmember;
   $inmembert=~tr/A-Z/a-z/;
   $inbox = "${lbdir}$msgdir/in/$inmembert\_msg.cgi";
   open(FILE,"$inbox");
   @inboxmsg=<FILE>;
   close(FILE);
   $inboxmsg=@inboxmsg;
   $outbox = "${lbdir}$msgdir/out/$inmembert\_out.cgi";
   open(FILE,"$outbox");
   @outboxmsg=<FILE>;
   close(FILE);
   $outboxmsg=@outboxmsg;

  $signature=~s/<br>/\n/g; 
  if ($oldmembercode eq "ad") {
       my $notshowsignaturefile = "$lbdir" . "data/notshowsignature.cgi"; 
       if(open(FILE,"$notshowsignaturefile")){ 
       $notshowsignaturemember = <FILE>; 
       close(FILE); 
       } 
       $notshowsignaturemember=~s/^\t//; 
       $notshowsignaturemember=~s/\t$//; 
       $notshowsignaturemember="\t$notshowsignaturemember\t"; 
       $nsscheck=($notshowsignaturemember !~/\t$inmember\t/i)?"":" checked"; 
    print qq~
    <form action="$thisprog" method=post name="creator">
    <input type=hidden name="action" value="edit">
    <input type=hidden name="checkaction" value="yes">
    <input type=hidden name="member" value="$inmember">
    <tr>
    <td bgcolor=#EEEEEE colspan=2><font color=#333333><b>Ҫ�༭���û����ƣ� </b>$membername</td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�û�ͷ�Σ�</b><br>�������Զ���һ��ͷ�Σ�<br>Ĭ�� Member ��ʾ��ͷ��</td>
    <td bgcolor=#FFFFFF><input type=text name="membertitle" value="$membertitle" maxlength=20></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����������</b></td>
    <td bgcolor=#FFFFFF><input type=text name="numberofposts" value="$numberofposts"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�ظ�������</b></td>
    <td bgcolor=#FFFFFF><input type=text name="numberofreplys" value="$numberofreplys"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>���ӱ�ɾ������</b></td>
    <td bgcolor=#FFFFFF><input type=text name="postdel" value="$postdel"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����(�粻�޸�������)��</b></td>
    <td bgcolor=#FFFFFF><input type=text name="password"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�ʼ���ַ/MSN��ַ��</b></td>
    <td bgcolor=#FFFFFF><input type=text name="emailaddress" value="$emailaddress"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��ҳ��ַ��</b></td>
    <td bgcolor=#FFFFFF><input type=text name="homepage" value="$homepage"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>OICQ �ţ�</b></td>
    <td bgcolor=#FFFFFF><input type=text name="oicqnumber" value="$oicqnumber"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ICQ �ţ�</b></td>
    <td bgcolor=#FFFFFF><input type=text name="icqnumber" value="$icqnumber"></td>
    </tr>$flaghtml<tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>���Ժη���</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="location" value="$location" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��������:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="jhmp" value="$jhmp" maxlength=20></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��������:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="rating" value="$rating" maxlength=2> (-5 �� $maxweiwang ֮��)</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����:</b></td>
    <td bgcolor=#FFFFFF><input type=text name="jifen" value="$jifen" maxlength=12 size=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����ǩ����</b></td>
    <td bgcolor=#FFFFFF><textarea name="newsignature" cols="60" rows="8">$signature</textarea><br><input type="checkbox" name="notshowsignature" value="yes" $nsscheck>���δ��û�ǩ����</td>
    </tr><tr>
	~;

        $tempoutput = "<select name=\"sex\" size=\"1\"><option value=\"no\">���� </option><option value=\"m\">˧�� </option><option value=\"f\">��Ů </option></select>\n";
        $tempoutput =~ s/value=\"$sex\"/value=\"$sex\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>�Ա�</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"education\" size=\"1\"><option value=\"����\">���� </option><option value=\"Сѧ\">Сѧ </option><option value=\"����\">���� </option><option value=\"����\">����</option><option value=\"��ר\">��ר</option><option value=\"��ר\">��ר</option><option value=\"����\">����</option><option value=\"˶ʿ\">˶ʿ</option><option value=\"��ʿ\">��ʿ</option><option value=\"��ʿ��\">��ʿ��</option></select>\n";
        $tempoutput =~ s/value=\"$education\"/value=\"$education\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>���ѧ����</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"marry\" size=\"1\"><option value=\"����\">���� </option><option value=\"δ��\">δ�� </option><option value=\"�ѻ�\">�ѻ� </option><option value=\"���\">��� </option><option value=\"ɥż\">ɥż </option></select>\n";
        $tempoutput =~ s/value=\"$marry\"/value=\"$marry\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>����״����</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"work\" size=\"1\"><option value=\"����\">���� </option><option value=\"�����ҵ\">�����ҵ </option><option value=\"����ҵ\">����ҵ </option><option value=\"��ҵ\">��ҵ </option><option value=\"������ҵ\">������ҵ </option><option value=\"����ҵ\">����ҵ </option><option value=\"ѧ��\">ѧ�� </option><option value=\"����ʦ\">����ʦ </option><option value=\"���ܣ�����\">���ܣ����� </option><option value=\"��������\">�������� </option><option value=\"����ҵ\">����ҵ </option><option value=\"����/���/�г�\">����/���/�г� </option><option value=\"ʧҵ��\">ʧҵ�� </option></select>\n";
        $tempoutput =~ s/value=\"$work\"/value=\"$work\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>ְҵ״����</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;
	($year, $month, $day) = split(/\//, $born);
        $tempoutput1 = "<select name=\"month\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option></select>\n";
        $tempoutput1 =~ s/value=\"$month\"/value=\"$month\" selected/;

        $tempoutput2 = "<select name=\"day\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option><option value=\"13\">13</option><option value=\"14\">14</option><option value=\"15\">15</option><option value=\"16\">16</option><option value=\"17\">17</option><option value=\"18\">18</option><option value=\"19\">19</option><option value=\"20\">20</option><option value=\"21\">21</option><option value=\"22\">22</option><option value=\"23\">23</option><option value=\"24\">24</option><option value=\"25\">25</option><option value=\"26\">26</option><option value=\"27\">27</option><option value=\"28\">28</option><option value=\"29\">29</option><option value=\"30\">30</option><option value=\"31\">31</option></select>\n";
        $tempoutput2 =~ s/value=\"$day\"/value=\"$day\" selected/;
	
 print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>���գ�</b>�粻����д����ȫ�����ա�</td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><input type="text" name="year" size=4 maxlength=4 value="$year">��$tempoutput1��$tempoutput2��</font></td>
	</tr>$xzhtml
        </tr>$sxhtml
	~;
	if (open(FILE2,"${lbdir}data/cityawards.cgi")) {
   @tempawards = <FILE2>;
   close(FILE2);
   foreach $tempaward (@tempawards) {
   chomp $tempaward;
           next if ($tempaward eq "");
   ($tempawardname,$tempawardurl,$tempawardinfo,$tempawardorder,$tempawardpic) = split(/\t/,$tempaward);
   $awardselect1.=qq~<option value="$tempawardname">$tempawardname~;
   $awardselect2.=qq~<option value="$tempawardname">$tempawardname~;
   $awardselect3.=qq~<option value="$tempawardname">$tempawardname~;
   $awardselect4.=qq~<option value="$tempawardname">$tempawardname~;
   $awardselect5.=qq~<option value="$tempawardname">$tempawardname~;   
   $awardselect6.=qq~<option value="$tempawardname">$tempawardname~;   
}
($tuseradd1, $tuseradd2, $tuseradd3, $tuseradd4, $tuseradd5, $tuseradd6) = split (/:/,$awards);
   $awardselect1 =~ s/value=\"$tuseradd1\"/value=\"$tuseradd1\" selected/;
   $awardselect2 =~ s/value=\"$tuseradd2\"/value=\"$tuseradd2\" selected/;
   $awardselect3 =~ s/value=\"$tuseradd3\"/value=\"$tuseradd3\" selected/;
   $awardselect4 =~ s/value=\"$tuseradd4\"/value=\"$tuseradd4\" selected/;
   $awardselect5 =~ s/value=\"$tuseradd5\"/value=\"$tuseradd5\" selected/;   
   $awardselect6 =~ s/value=\"$tuseradd6\"/value=\"$tuseradd6\" selected/;   
}
undef @tempawards;
   print qq~
   <td bgcolor=#FFFFFF><font color=#333333><b>��̳ѫ�£�</b></td>
   <td bgcolor=#FFFFFF>ѫ��һ��
   <select name="tuseradd1">
   <option value="">û��ѫ��
   $awardselect1
   </select> ѫ�¶���
   <select name="tuseradd2">
   <option value="">û��ѫ��
   $awardselect2
   </select><br>ѫ������
   <select name="tuseradd3">
   <option value="">û��ѫ��
   $awardselect3
   </select> ѫ���ģ�
   <select name="tuseradd4">
   <option value="">û��ѫ��
   $awardselect4
   </select><br>ѫ���壺
   <select name="tuseradd5">
   <option value="">û��ѫ��
   $awardselect5
   </select> ѫ������
   <select name="tuseradd6">
   <option value="">û��ѫ��
   $awardselect6
    </select></td>
   </tr><tr>
   ~;
    $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

    print qq~
    <td bgcolor=#FFFFFF><font color=#333333><b>�����Ǯ��</b></td>
    <td bgcolor=#FFFFFF><input type=text name="mymoney" value="$mymoney" maxlength=12 size=12> Ŀǰ�ֽ�$mymoney1 $moneyname</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>���ʴ�����</b></td>
    <td bgcolor=#FFFFFF><input type=text name="visitno" value="$visitno" maxlength=7 size=7></td>
    </tr><tr>
    ~;
   $timedifference = 0 if ($timedifference eq '');
   $tempoutput = "<select name=\"timedifference\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\">0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
   $tempoutput =~ s/value=\"$timedifference\"/value=\"$timedifference\" selected/;
   $joineddate = $lastgone if ($joineddate eq "");
   $joineddate1 = $joineddate;
   $joineddate = &dateformat($joineddate);
   if ($lastgone ne "") {$lastgone   = &dateformat($lastgone); } else {$lastgone = $joineddate; }
   print qq~
    <td bgcolor=#FFFFFF><font color=#333333><b>ʱ�</b></td>
    <td bgcolor=#FFFFFF>$tempoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF colspan=2><font color=#333333><b>˽����̳����Ȩ�ޣ�</b><br>
    $privateoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�û����ͣ�</b><br>ע�⣺̳��Ϊ��̳����Ա���о��Ըߵ�Ȩ�ޡ�<br>�����������Ӵ����͵��û���<br>�ܰ������κ���̳�����а���Ȩ�ޣ�<br>�ڹ�������ֻ��һ��Ȩ�ޡ�</td>
    <td bgcolor=#FFFFFF>$memberstateoutput</td>
    </tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ע��ʱ�䣺</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ע��ʱ�� IP ��ַ��</b></td>
    <td bgcolor=#FFFFFF><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$ipaddress',420,320)" title="LB WHOIS��Ϣ"><font color=#333333>$ipaddress</font></span> (<a href="$thisprog?action=viewip&letter=$ipaddress">����ͬ�ɣе��û�</a>)</td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>������ʱ�䣺</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastgone</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>����ʱ�䣺</b></td>
    <td bgcolor=#FFFFFF><font color=#333333><input type=text size=12 name="onlinetime" value="$onlinetime" maxlength=12> ��</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>�û�ͷ��</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$useravatar</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>�û���ѶϢ��</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>
      �ռ��乲 $inboxmsg ����[ <a href="$thisprog?action=boxaction&box=inbox&checkaction=delete&member=$inmemberencode">ɾ���ռ���</a> ]��[ <a href="$thisprog?action=boxaction&box=inbox&checkaction=viewbox&member=$inmemberencode">�����ռ���</a> ]<br>
      �����乲 $outboxmsg ����[ <a href="$thisprog?action=boxaction&box=outbox&checkaction=delete&member=$inmemberencode">ɾ��������</a> ]��[ <a href="$thisprog?action=boxaction&box=outbox&checkaction=viewbox&member=$inmemberencode">���ӷ�����</a> ]</font></td></tr>

    <input type=hidden name="joineddate" value="$joineddate1">
    <tr>
    <td colspan=2 bgcolor=#FFFFFF align=center>[ <a href="$thisprog?action=deletemember&member=$inmemberencode">ɾ �� �� �� ��</a> ]</td>
    </tr>
    <tr>
    <td colspan=2 bgcolor=#EEEEEE align=center><input type=submit value="�� ��" name=submit></form></td>
    </tr>
    ~;
  }
  else {
    my $memteam1 = qq~<option value="rz1">$defrz1(��֤�û�)~ if ($defrz1 ne "");
    my $memteam2 = qq~<option value="rz2">$defrz2(��֤�û�)~ if ($defrz2 ne "");
    my $memteam3 = qq~<option value="rz3">$defrz3(��֤�û�)~ if ($defrz3 ne "");
    my $memteam4 = qq~<option value="rz4">$defrz4(��֤�û�)~ if ($defrz4 ne "");
    my $memteam5 = qq~<option value="rz5">$defrz5(��֤�û�)~ if ($defrz5 ne "");
    $memberstateoutput = qq~<select name="membercode"><option value="me">һ���û�$memteam1$memteam2$memteam3$memteam4$memteam5<option value="rz">��֤�û�<option value="banned">��ֹ���û�����<option value="masked">���δ��û�����</select>~;
    $memberstateoutput =~ s/value=\"$membercode\"/value=\"$membercode\" selected/g;
    ($year, $month, $day) = split(/\//, $born);
    if ($lastgone ne "") {$lastgone   = &dateformat($lastgone); } else {$lastgone = $joineddate; }
    $joineddate = $lastgone if ($joineddate eq "");
    $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
    print qq~
    <form action="$thisprog" method=post>
    <input type=hidden name="action" value="edit">
    <input type=hidden name="checkaction" value="yes">
    <input type=hidden name="member" value="$inmember">
    <input type=hidden name="numberofposts" value="$numberofposts">
    <input type=hidden name="numberofreplys" value="$numberofreplys">
    <input type=hidden name="postdel" value="$postdel">
    <input type=hidden name="emailaddress" value="$emailaddress">
    <input type=hidden name="homepage" value="$homepage">
    <input type=hidden name="oicqnumber" value="$oicqnumber">
    <input type=hidden name="icqnumber" value="$icqnumber">
    <input type=hidden name="location" value="$location">
    <input type=hidden name="sex" value="$sex">
    <input type=hidden name="education" value="$education">
    <input type=hidden name="marry" value="$marry">
    <input type=hidden name="work" value="$work">
    <input type=hidden name="month" value="$month">
    <input type=hidden name="day" value="$day">
    <input type=hidden name="year" value="$year">
    <input type=hidden name="visitno" value="$visitno">
    <input type=hidden name="mymoney" value="$mymoney">
    <input type=hidden name="joineddate" value="$joineddate">
    <input type=hidden name="userflag" value="$userflag">
    <input type=hidden name="usersx" value="$usersx">
    <input type=hidden name="userxz" value="$userxz">
    <input type=hidden name="timedifference" value="$timedifference">
    <input type=hidden name="jifen" value="$jifen">

    <tr>
    <td bgcolor=#EEEEEE colspan=2><font color=#333333><b>Ҫ�༭���û����ƣ� </b>$membername</td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�û�ͷ�Σ�</b><br>�������Զ���һ��ͷ�Σ�<br>Ĭ�� Member ��ʾ��ͷ��</td>
    <td bgcolor=#FFFFFF><input type=text name="membertitle" value="$membertitle" maxlength=20></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����(�粻�޸�������)��</b></td>
    <td bgcolor=#FFFFFF><input type=text name="password"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��������:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="jhmp" value="$jhmp" maxlength=20></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>��������:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="rating" value="$rating" maxlength=2> (-5 �� $maxweiwang ֮��)</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>����ǩ����</b></td>
    <td bgcolor=#FFFFFF><textarea name="newsignature" cols="60" rows="8">$signature</textarea></td>
    </tr><tr>
    ~;
   $joineddate = &dateformat($joineddate);
   print qq~
    <td bgcolor=#FFFFFF colspan=2><font color=#333333><b>˽����̳����Ȩ�ޣ�</b><br>
    $privateoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>�û����ͣ�</b></td>
    <td bgcolor=#FFFFFF>$memberstateoutput</td>
    </tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ע��ʱ�䣺</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ע��ʱ�� IP ��ַ��</b></td>
    <td bgcolor=#FFFFFF><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$ipaddress',420,320)" title="LB WHOIS��Ϣ"><font color=#333333>$ipaddress</font></span> (<a href="$thisprog?action=viewip&letter=$ipaddress">����ͬ�ɣе��û�</a>)</td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>������ʱ�䣺</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastgone</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>����ʱ�䣺</b></td>
    <td bgcolor=#FFFFFF><font color=#333333><input type=text size=10 name="onlinetime" value="$onlinetime" maxlength=10> ��</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>�û�ͷ��</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$useravatar</font></td></tr>
    <tr>
    <td colspan=2 bgcolor=#FFFFFF align=center>[ <a href="$thisprog?action=deletemember&member=$inmemberencode">ɾ �� �� �� ��</a> ]</td>
    </tr>

    <tr>
    <td colspan=2 bgcolor=#EEEEEE align=center><input type=submit value="�� ��" name=submit></form></td>
    </tr>
    ~;
  	
  }  
 } # end else
    
} # endroute


############### delete member

sub deletemember {

    $oldmembercode = $membercode;
    &getmember("$inmember");
    my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $bankadd1, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);

    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "amo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�ܰ�����Ȩɾ��̳���Ͱ������ϣ�</b></td></tr>";
            exit;
    }
    if ($inmembername eq $inmember) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�Լ�����ɾ���Լ�������Ӵ��</b></td></tr>";
            exit;
    }

if ($checkaction eq "yes") {
####################################################
    # Check to see if they were the last member to register

    require "$lbdir" . "data/boardstats.cgi";
        
    if($inmember eq "$lastregisteredmember") { #start

        $dirtoopen = "$lbdir" . "$memdir";
        opendir (DIR, "$dirtoopen"); 
        @filedata = readdir(DIR);
        closedir (DIR);
        @inmembers = grep(/cgi$/i,@filedata);

        local($highest) = 0;

        foreach (@inmembers) {
            $_ =~ s/\.cgi$//g;
            &getmember("$_");
            if (($joineddate > $highest) && ($inmember ne $membername)) {
                $highest = $joineddate;
                $memberkeep = $membername;
                }
        }
        
        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers--;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$memberkeep\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        } # end if new/delete member

    else {
        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers--;
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
        } # end if else

    opendir (DIRS, "$lbdir");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^\w+?$/i, @files);
    my @recorddir = grep(/^record/i, @files);
    $recorddir = $recorddir[0];
    my @memfavdir = grep(/^memfav/i, @files);
    $memfavdir = $memfavdir[0];
    my @searchdir = grep(/^search/i, @files);
    $searchdir = $searchdir[0];

	&getmember("$inmember","no");

    $inmembername = $inmember;
        $inmembername =~ s/ /\_/isg;
	$inmembername =~ tr/A-Z/a-z/;

        # Delete the database for the member
	my $namenumber = &getnamenumber($inmembername);
	&checkmemfile($inmembername,$namenumber);
        unlink ("${lbdir}$searchdir/$inmembername\_sch.cgi");
        unlink ("${lbdir}$searchdir/$inmembername\_sav.cgi");
        unlink ("${lbdir}$memdir/$namenumber/$inmembername.cgi");
        unlink ("${lbdir}$memdir/old/$inmembername.cgi");
        unlink ("${lbdir}$msgdir/in/${inmembername}_msg.cgi");
        unlink ("${lbdir}$msgdir/out/${inmembername}_out.cgi");
        unlink ("${lbdir}$msgdir/main/${inmembername}_mian.cgi");
        unlink ("${lbdir}$memfavdir/$inmembername.cgi");
        unlink ("${lbdir}$memfavdir/open/$inmembername.cgi");
        unlink ("${lbdir}$memfavdir/close/$inmembername.cgi");
        unlink ("${lbdir}memfriend/$inmembername.cgi");
        unlink ("${lbdir}$recorddir/post/$inmembername.cgi");
        unlink ("${lbdir}$recorddir/reply/$inmembername.cgi");
        unlink ("${lbdir}memblock/$inmembername.cgi");
    	unlink ("${imagesdir}usravatars/$inmembername.gif");
    	unlink ("${imagesdir}usravatars/$inmembername.png");
    	unlink ("${imagesdir}usravatars/$inmembername.jpg");
    	unlink ("${imagesdir}usravatars/$inmembername.swf");
    	unlink ("${imagesdir}usravatars/$inmembername.bmp");
	unlink ("${lbdir}ebankdata/log/" . $inmembername . ".cgi");
	unlink ("${lbdir}cache/meminfo/$inmembername.pl");
	unlink ("${lbdir}cache/myinfo/$inmembername.pl");
	unlink ("${lbdir}cache/id/$inmembername.pl");
    	$memberfiletitletemp = unpack("H*","$inmembername");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.gif");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.png");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.jpg");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.swf");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.bmp");

	&updateallsave(-1, -$mysaves) if ($mystatus);

	my $charone = substr($emailaddress, 0, 1);
	$charone = lc($charone);
	$charone = ord($charone);

	$/ = "";
	open (MEMFILE, "${lbdir}data/lbemail/$charone.cgi");
 	my $allmemberemails = <MEMFILE>;
 	close(MEMFILE);
	$/ = "\n";
	$allmemberemails =~ s/$emailaddress\t.+?\n//isg;
   	if (open (MEMFILE, ">${lbdir}data/lbemail/$charone.cgi")) {
	    print MEMFILE "$allmemberemails";
	    close (MEMFILE);
   	}

        $filetoopen = "$lbdir" . "data/banemaillist.cgi";
        open(FILE,"$filetoopen");
        $emaildata = <FILE>;
        close(FILE);
        @emaildata = split(/\t/,$emaildata);
        open(FILE,">$filetoopen");
        foreach (@emaildata) {
            chomp $_;
            print FILE "$_\t" if ($emailaddress ne $_);
	}
        close(FILE);

        $filetoopen = "$lbdir" . "data/baniplist.cgi";
        open(FILE,"$filetoopen");
        $ipdata = <FILE>;
        close(FILE);
        @ipdata = split(/\t/,$ipdata);
        open(FILE,">$filetoopen");
        foreach (@ipdata) {
            chomp $_;
            print FILE "$_\t" if ($ipaddress ne $_);
	}
        close(FILE);

        open(FILE,"${lbdir}data/lbmember.cgi");
        @members = <FILE>;
        close(FILE);
        open(FILE,">${lbdir}data/lbmember.cgi");
        foreach (@members) {
            chomp $_;
            my ($usernamerbak,$no) = split(/\t/,$_);
            print FILE "$_\n" if ($usernamerbak ne $inmember);
	}
        close(FILE);
        open(FILE,"${lbdir}data/lbmember3.cgi");
        @members = <FILE>;
        close(FILE);
        open(FILE,">${lbdir}data/lbmember3.cgi");
        foreach (@members) {
            chomp $_;
            my ($usernamerbak,$no) = split(/\t/,$_);
            print FILE "$_\n" if ($usernamerbak ne $inmember);
	}
        close(FILE);
        open(FILE,"${lbdir}data/lbmember4.cgi");
        @members = <FILE>;
        close(FILE);
        open(FILE,">${lbdir}data/lbmember4.cgi");
        foreach (@members) {
            chomp $_;
            my ($usernamerbak,$no) = split(/\t/,$_);
            print FILE "$_\n" if ($usernamerbak ne $inmember);
	}
        close(FILE);

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>�û��Ѿ������ݿ�����ȫɾ����</b>
        </td></tr>
         ~;


} # end checkaction else

else {

        $cleanedmember = $inmember;
        $cleanedmember =~ s/\_/ /g;
	$inmember = uri_escape($inmember);

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���棡��</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>ֻ�е����������Ӳſ���ɾ���û�<b>"$cleanedmember"</b><p>
        >> <a href="$thisprog?action=deletemember&checkaction=yes&member=$inmember">ɾ���û�</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
        }

} # end routine

sub unban {

        &getmember("$inmember");
    
    if ($membercode ne "banned") {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>$inmember û�б���ֹ���԰���</b></td></tr>";
            exit;
    }

        $memberfiletitle = $inmember;
        $memberfiletitle =~ s/ /\_/isg;
	$memberfiletitle =~ tr/A-Z/a-z/;
        unlink ("${lbdir}cache/meminfo/$memberfiletitle.pl");

        # Remove from ban lists

        $filetoopen = "$lbdir" . "data/banemaillist.cgi";
        open(FILE,"$filetoopen");
        $emaildata = <FILE>;
        close(FILE);
        @emaildata = split(/\t/,$emaildata);
        open(FILE,">$filetoopen");
        foreach (@emaildata) {
            chomp $_;
            print FILE "$_\t" if ($emailaddress ne $_);
	}
        close(FILE);

        $filetoopen = "$lbdir" . "data/baniplist.cgi";
        open(FILE,"$filetoopen");
        $ipdata = <FILE>;
        close(FILE);
        @ipdata = split(/\t/,$ipdata);
        open(FILE,">$filetoopen");
        foreach (@ipdata) {
            chomp $_;
            print FILE "$_\t" if ($ipaddress ne $_);
	}
        close(FILE);

        my $namenumber = &getnamenumber($memberfiletitle);
        &checkmemfile($memberfiletitle,$namenumber);
        $filetomake = "$lbdir" . "$memdir/$memberfiletitle.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$password\t$membertitle\tme\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$allowedforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>$membername �Ѿ�ȡ����ֹ����</b>
        </td></tr>
        ~;

} # end route

sub viewdelmembers { 
unless ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
print qq~ 
<tr> 
<td bgcolor=#FFFFFF align=center colspan=2> 
<font color=#990000> 
<b>����</b><p> 
<font color=#333333>��û��Ȩ��ʹ��������ܣ�</font> 
</td> 
</tr> 
~; 
exit; 
} 
print qq~ 
<tr> 
<td bgcolor=#FFFFFF colspan=2><br> 
~; 

$filetoopen = "$lbdir" . "data/delmember.cgi"; 
open(FILE,"$filetoopen"); 
flock (FILE, 1) if ($OS_USED eq "Unix"); 
@memberfiles = <FILE>; 
close(FILE); 
$i=-1; 
print qq~ 
<table width=100% border=0> 
<tr>~; 
foreach $memtypedata (@memberfiles) { 
if ($i > -1) { 
chomp $memtypedata; 
($username, $membertype) = split(/\t/,$memtypedata); 
$username=~ s/.cgi//isg; 
&getmember("$username");
$membername = $username if ($membername eq "");
print qq~ 
<td width=10%><a href="setmembers.cgi?action=undelmember&undelname=$membername" title="����Ա $membername ��Ԥɾ����ȡ��">$membername</a></td>~; ### �@������Ū�e���޸� , ֮ǰ���޸��^����Ո����һ�� 
} 
$i++; 
if ($i / 5 eq int($i/5)) {print qq~</tr><tr>~; 
} 
} 
print qq~</table> 
<br><br> 
<b><center>���� $i ����Ա����Ԥɾ���ʸ�</center></b><br> 
</td></tr> 
~; 
} 

sub undelmember { 
unless ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
print qq~ 
<tr> 
<td bgcolor=#FFFFFF align=center colspan=2> 
<font color=#990000> 
<b>����</b><p> 
<font color=#333333>��û��Ȩ��ʹ��������ܣ�</font> 
</td> 
</tr> 
~; 
exit; 
} 
print qq~ 
<tr> 
<td bgcolor=#FFFFFF colspan=2><br> 
~; 
$filetoopen = "$lbdir" . "data/delmember.cgi"; 
open(FILE,"$filetoopen"); 
flock (FILE, 1) if ($OS_USED eq "Unix"); 
@memberfiles = <FILE>; 
close(FILE); 
$pretime=$memberfiles[0]; 
$i=0; 
open (FILE, ">${lbdir}data/delmember.cgi"); 
print FILE "$pretime"; 
close (FILE); 
foreach $memtypedata (@memberfiles) { 
if ($i > "0") { 
chomp $memtypedata; 
($username, $membertype) = split(/\t/,$memtypedata); 
$username=~ s/.cgi//isg; 
&getmember("$username"); 
if ($undelname ne $membername) { 
open (FILE, ">>${lbdir}data/delmember.cgi"); 
flock (FILE, 1) if ($OS_USED eq "Unix"); 
print FILE "$username\t$membertype\t\n"; 
close (FILE); 
} 
} 
$i++; 
} 
close(FILE); 
print qq~</table> 
<br><br> 
<b><center>��Ա $undelname �Ѵ�Ԥɾ��������ȡ��</center></b><br> 
</td></tr> 
~; 
} 

sub boxaction {

   $oldmembercode = $membercode;
   &getmember("$inmember");
   if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "amo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
           print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>�ܰ�����Ȩ�鿴̳���Ͱ������ϣ�</b></td></tr>";
           exit;
   }
   $inmembert=$inmember;
   $inmembert=~tr/A-Z/a-z/;
   if($box eq "inbox"){
   $filepath = "${lbdir}$msgdir/in/$inmembert\_msg.cgi";
   $boxname = "�ռ���";
   }else{
   $filepath = "${lbdir}$msgdir/out/$inmembert\_out.cgi";
   $boxname = "������";
   }
   if($checkaction eq "delete"){
   unlink $filepath;
    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>�û�$boxname�Ѿ�ɾ����</b>
    </td></tr>
    ~;
   }else{
    open (FILE, "$filepath");
    my @messanges = <FILE>;
close (FILE);
    print qq~
<script>function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
</script>
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>�û�$boxname��ѶϢ</b></td></tr>
    <tr>
    <form name="form2"><td bgcolor=#FFFFFF align=center colspan=2>
    <TEXTAREA name=inpost rows=12 style="width:90%">~;
$current_time=localtime;
foreach (@messanges) {
$messangeswords = $_;
($usrname, $msgread, $msgtime, $msgtitle, $msgwords) = split(/\t/,$_);
$usrname =~ s/^����������//isg;
$usrname =~ s/ /\_/g;
$usrname =~ tr/A-Z/a-z/;
$msgwords =~ s/\r//ig;
$msgwords =~ s/ / /g;
$msgwords =~ s/"/\&quot;/g;
$msgwords =~ s/\s+/ /g;
$msgwords =~ s/<br>/\n/g;
$msgwords =~ s/<p>/\n/g;
$msgtime = $msgtime + ($timedifferencevalue*3600) + ($timezone*3600);
$msgtime = &dateformat("$msgtime");
    print qq~[�շ�����]��$usrname\n[�շ�ʱ��]��$msgtime\n[���ű���]��$msgtitle\n[��������]��$msgwords\n\n~;
}
    print qq~</TEXTAREA><br>>> <a href="javascript:HighlightAll('form2.inpost')">���Ƶ������� <<</a></td></form></tr>~;
   }


}

sub updateallsave #���ñ仯��������������Ϣ
{
	my ($callusers, $callsaves) = @_;

	my $filetoopen = $lbdir . "ebankdata/allsaves.cgi";
	my $allusers = 0;
	my $allsaves = 0;
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	if (-e $filetoopen)
	{
		open(FILE, $lbdir . "ebankdata/allsaves.cgi");
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my $allinfo = <FILE>;
		close(FILE);
		chomp($allinfo);
		($allusers, $allsaves) = split(/,/, $allinfo);
	}

	$allusers += $callusers;
	$allsaves += $callsaves;

	if (open(FILE, ">$filetoopen"))
	{
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "$allusers,$allsaves";
		close(FILE);
	}
	&winunlock($filetoopen) if ($OS_USED eq "Nt");

	return;
}

print qq~</td></tr></table></body></html>~;
exit;
