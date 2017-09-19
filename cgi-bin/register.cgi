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
$LBCGI::POST_MAX=1000000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
use MAILPROG qw(sendmail);
require "data/boardinfo.cgi";
require "data/cityinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "register.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}

$addme=$query->param('addme');

$inforum  = $query -> param('forum');
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));

&ipbanned; #��ɱһЩ ip

if ($arrowavaupload ne "on") { undef $addme; }
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($regonoff == 2) {
   $regonoff = 1;
   $regonoffinfo = "1";
   my (undef, undef, $hour, $mday, undef, undef, $wday, undef) = localtime(time + $timezone * 3600);
   $regautovalue =~ s/[^\d\-]//sg;
   my ($starttime, $endtime) = split(/-/, $regautovalue);
   if ($regauto eq "day") {
	$regonoff = 0 if ($hour == $starttime && $endtime eq "");
	$regonoff = 0 if ($hour >= $starttime && $hour < $endtime);
   }
   elsif ($regauto eq "week") {
	$wday = 7 if ($wday == 0);
	$regonoff = 0 if ($wday == $starttime && $endtime eq "");
	$regonoff = 0 if ($wday >= $starttime && $wday <= $endtime);
   }
   elsif ($regauto eq "month") {
	$regonoff = 0 if ($mday == $starttime && $endtime eq "");
	$regonoff = 0 if ($mday >= $starttime && $mday <= $endtime);
   }
}
if ($regonoff == 1) {
    $inmembername = $query->cookie("amembernamecookie"); 
    $inpassword   = $query->cookie("apasswordcookie"); 
    $inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\|\'\:\"\,\.\/\<\>\?]//isg;
    $inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
    unless ($inmembername eq "" || $inmembername eq "����") { &getmember("$inmembername"); &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");	&error("��ͨ����&��̳�������û���������������µ�¼��") if ($inpassword ne $password);  $regonoff = 0 if ($membercode eq "ad"); } 
}

for ('inmembername','password','password2','emailaddress','showemail','homepage','oicqnumber','icqnumber','newlocation','recommender',
     'interests','signature','timedifference','useravatar','action','personalavatar','personalwidth','personalheight','mobilephone',
     'sex','education','marry','work','year','month','day','userflag','userxz','usersx') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    ${$_} = $tp;
}
$recommender =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\|\'\:\"\,\.\/\<\>\?]//isg;

&error("��̳������ʾ����ʹ�&��̳������ʾ����ʹ��У��������зǷ��ַ�����������ʺʹ𰸣�") if ($query -> param('getpassq') =~ /[\||\a|\f|\n|\e|\0|\r|\t]/ || $query -> param('getpassa') =~ /[\||\a|\f|\n|\e|\0|\r|\t]/);
$userquestion = $query -> param('getpassq')."|".$query -> param('getpassa'); 
$userquestion = "" if ($passwordverification eq "yes" && $emailfunctions ne "off");

$helpurl = &helpfiles("�û�ע��");
$helpurl = qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;

if ($arrawsignpic eq "on")      { $signpicstates = "����";     } else { $signpicstates = "��ֹ";     }
if ($arrawsignflash eq "on")    { $signflashstates = "����";   } else { $signflashstates = "��ֹ";   }
if ($arrawsignfontsize eq "on") { $signfontsizestates = "����";} else { $signfontsizestates = "��ֹ";}
if ($arrawsignsound eq "on")    { $signsoundstates = "����";   } else { $signsoundstates = "��ֹ";   }

&mischeader("�û�ע��");
$output .= qq~<p><SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
~;

if ($regonoff eq 1) {
    if ($regonoffinfo eq "1") {
        if ($regauto eq "day") { $regauto = "ÿ��"; } elsif ($regauto eq "week") { $regauto = "ÿ��"; } elsif ($regauto eq "month") { $regauto = "ÿ��"; }
        $regauto = "������ע��ʱ�䣺$regauto $regautovalue ��";
    }
    else { $regauto = ""; }

    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>�Բ�����̳Ŀǰ��ʱ������ע�����û�$regauto</b>
    </td></tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc size=3><BR><BR>~;
    if ($noregwhynot ne "") { $noregwhynot=&HTML($noregwhynot); $noregwhynot =~ s/\n/<BR>/isg;$output.=qq~$noregwhynot~; }
                       else { $output.=qq~����һЩ�����ԭ�򣬱���̳��ʱ�������û�ע�ᣡ~; }
    $output.=qq~<BR><BR><BR></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}
elsif ($action eq "addmember") {
    &error("����&�벻Ҫ���ⲿ���ӱ�����") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '')&&($canotherlink ne "yes"));
    $membercode    = "me";
    $membertitle   = "Member";
    $numberofposts = "0|0";
    $joineddate    = time;
    $lastgone      = $joineddate;
    $mymoney	   = $joinmoney;
    $jifen	   = $joinjf;
    $jhmp          = "��������";
    $lastpostdate  = "û�з����";
    $emailaddress  = lc($emailaddress);
    
    if (($inmembername eq "")||($emailaddress eq "")) {
        &error("�û�ע��&�������û������ʼ���ַ����Щ�Ǳ���ģ�");
    }

    $ipaddress     = $ENV{'REMOTE_ADDR'};
    my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $trueipaddress = $ipaddress if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
    my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
    $trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 !~ m/a-z/i && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
    $ipaddress = $trueipaddress;
    $year =~ s/\D//g;
    $year = "19$year"if ($year < 1900 && $year ne "");
    my (undef, undef, undef, undef, undef, $yeartemp, undef, undef) = localtime(time + $timezone * 3600);
    $yeartemp = 1900 + $yeartemp if ($yeartemp < 1900);
    if ($year ne "") {
        &error("�û�ע��&����ȷ������ĳ�����ݣ�") if ($year <= 1900 || $year >= $yeartemp - 3);
    }
    if (($year eq "")||($month eq "")||($day eq "")) { $year  = "";$month = "";$day   = "";}
    $born = "$year/$month/$day";

    if ($born ne "//") { #��ʼ�Զ��ж�����
    	if ($month eq "01") {
    	    if (($day >= 1)&&($day <=19)) { $userxz = "z10"; }
    	    else { $userxz = "z11"; }
    	}
        elsif ($month eq "02") {
    	    if (($day >= 1)&&($day <=18)) { $userxz = "z11"; }
    	    else { $userxz = "z12"; }
        }
        elsif ($month eq "03") {
    	    if (($day >= 1)&&($day <=20)) { $userxz = "z12"; }
    	    else { $userxz = "z1"; }

        }
        elsif ($month eq "04") {
    	    if (($day >= 1)&&($day <=19)) { $userxz = "z1"; }
    	    else { $userxz = "z2"; }
        }
        elsif ($month eq "05") {
    	    if (($day >= 1)&&($day <=20)) { $userxz = "z2"; }
    	    else { $userxz = "z3"; }
        }
        elsif ($month eq "06") {
    	    if (($day >= 1)&&($day <=21)) { $userxz = "z3"; }
    	    else { $userxz = "z4"; }
        }
        elsif ($month eq "07") {
    	    if (($day >= 1)&&($day <=22)) { $userxz = "z4"; }
    	    else { $userxz = "z5"; }
        }
        elsif ($month eq "08") {
    	    if (($day >= 1)&&($day <=22)) { $userxz = "z5"; }
    	    else { $userxz = "z6"; }
        }
        elsif ($month eq "09") {
    	    if (($day >= 1)&&($day <=22)) { $userxz = "z6"; }
    	    else { $userxz = "z7"; }
        }
        elsif ($month eq "10") {
    	    if (($day >= 1)&&($day <=23)) { $userxz = "z7"; }
    	    else { $userxz = "z8"; }
        }
        elsif ($month eq "11") {
    	    if (($day >= 1)&&($day <=21)) { $userxz = "z8"; }
    	    else { $userxz = "z9"; }
        }
        elsif ($month eq "12") {
    	    if (($day >= 1)&&($day <=21)) { $userxz = "z9"; }
    	    else { $userxz = "z10"; }
        }
    }

	my $charone = substr($emailaddress, 0, 1);
	$charone = lc($charone);
	$charone = ord($charone);
	if ($oneaccountperemail eq "yes") {
	    mkdir ("${lbdir}data/lbemail", 0777) if (!(-e "${lbdir}data/lbemail"));
	    chmod(0777,"${lbdir}data/lbemail");

	    $/ = "";
	    open (MEMFILE, "${lbdir}data/lbemail/$charone.cgi");
 	    my $allmemberemails = <MEMFILE>;
 	    close(MEMFILE);
	    $/ = "\n";
	    $allmemberemails = "\n$allmemberemails\n";
	    chomp($allmemberemails);
	    $allmemberemails = "\t$allmemberemails";

	    if ($allmemberemails =~ /\n$emailaddress\t(.+?)\n/i) {
		&error("�û�ע��&�Բ���������� Email �Ѿ���ע���û���<u>$1</u> ʹ����");
	    }
	}

	#�ʼ����� _S
	my $allow_eamil_file = "$lbdir" . "data/allow_email.cgi";
	if(-e $allow_eamil_file){
		open(AEFILE,$allow_eamil_file);
		my $allowtype = <AEFILE>;
		my $allowmail = <AEFILE>;
		close(AEFILE);
		chomp $allowtype;
		chomp $allowmail;
		my $check_result = 0;
		my $get_email_server = substr($emailaddress,rindex($emailaddress,'@')+1);
		if ($allowmail ne "") {
			my @allowmail = split(/\t/,$allowmail);
			chomp @allowmail;
			foreach (@allowmail){
				next if($_ eq "");
				if(lc($get_email_server) eq lc($_)){
					$check_result = 1;
					last;
				}
			}
		    if ($allowtype eq "allow") {
			if($check_result == 0){
				&error("�û�ע��&����ʹ��ָ�����������ע�ᣡ<a href=\"javascript:openScript('dispemail.cgi',200,300);\">[�б�]</a>");
			}
		    } else {
			if ($check_result == 1) {
				&error("�û�ע��&���ṩ�����䱻��ֹʹ��ע�ᣡ<a href=\"javascript:openScript('dispemail.cgi',200,300);\">[�б�]</a>");
			}
		    }
		}
	}
	#�ʼ����� _E

    &error("�û�ע��&�Բ�����������û��������⣬�벻Ҫ���û����а���\@\#\$\%\^\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]\|�����ַ���") if ($inmembername =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\|\;\'\:\"\,\.\/\<\>\?\[\]]/);
    if($inmembername =~ /_/)  { &error("�û�ע��&�벻Ҫ���û�����ʹ���»��ߣ�"); }

    $inmembername =~ s/\&nbsp\;//ig;
    $inmembername =~ s/��/ /g;
    $inmembername =~ s/��/ /g;
    $inmembername =~ s/[ ]+/ /g;
    $inmembername =~ s/[ ]+/_/;
    $inmembername =~ s/[_]+/_/;
    $inmembername =~ s/�//isg;
    $inmembername =~ s///isg;
    $inmembername =~ s/��//isg;
    $inmembername =~ s/��//isg;
    $inmembername =~ s/()+//isg;
    $inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\|\'\:\"\,\.\/\<\>\?\[\]]//isg;
    $inmembername =~ s/\s*$//g;
    $inmembername =~ s/^\s*//g;

    &error("�û�ע��&�Բ�����������û��������⣬�����һ��") if ($inmembername =~ /^q(.+?)-/ig || $inmembername =~ /^q(.+?)q/ig);
    
    $bannedmember = "no";
    open(FILE,"${lbdir}data/banemaillist.cgi");
    my $bannedemail = <FILE>;
    close(FILE);
    chomp $bannedemail;
    $bannedemail = "\t$bannedemail\t";
    $bannedemail =~ s/\t\t/\t/isg;
    my $emailaddresstemp = "\t$emailaddress\t";
    $bannedmember = "yes" if ($bannedemail =~ /$emailaddresstemp/i);

    $filetoopen = "$lbdir" . "data/baniplist.cgi";
    open(FILE,"${lbdir}data/baniplist.cgi");
    my $bannedips = <FILE>;
    close(FILE);
    chomp $bannedips;
    $bannedips = "\t$bannedips\t";
    $bannedips =~ s/\t\t/\t/isg;
    
    (my $ipaddresstemp = $ipaddress) =~ s/\./\\\./g;
    $ipaddresstemp =~ /^((((.*?\\\.).*?\\\.).*?\\\.).*?)$/;
    $bannedmember = "yes" if ($bannedips =~ /\t($1|$2|$3|$4)\t/);

    $bannedmember = "yes" if (($inmembername =~ /^m-/i)||($inmembername =~ /^s-/i)||($inmembername =~ /tr-/i)||($inmembername =~ /^y-/i)||($inmembername =~ /ע��/i)||($inmembername =~ /guest/i)||($inmembername =~ /qq-/i)||($inmembername =~ /qq/i)||($inmembername =~ /qw/i)||($inmembername =~ /q-/i)||($inmembername =~ /qx-/i)||($inmembername =~ /qw-/i)||($inmembername =~ /qr-/i)||($inmembername =~ /^ȫ��/i)||($inmembername =~ /register/i)||($inmembername =~ /��Ƹ��/i)||($inmembername =~ /����/i)||($inmembername =~ /����ϵͳѶϢ/i)||($inmembername =~ /leobbs/i)||($inmembername =~ /leoboard/i)||($inmembername =~ /�װ�/i)||($inmembername =~ /LB5000/i)||($inmembername =~ /ȫ�������Ա/i)||($inmembername =~ /����Ա/i)||($inmembername =~ /����/i)||($inmembername =~ /����Ϣ�㲥/i)||($inmembername =~ /��ʱ��ȱ/i)||($inmembername =~ /����������/i)||($inmembername =~ /����/i)||($inmembername =~ /̳��/i)||($inmembername =~ /nodisplay/i)||($inmembername =~ /^system/i)||($inmembername =~ /---/i)||($inmembername eq "admin")||($inmembername eq "root")||($inmembername eq "copy")||($inmembername =~ /^sub/)||($inmembername =~ /^exec/)||($inmembername =~ /\@ARGV/i)||($inmembername =~ /^require/)||($inmembername =~ /^rename/i)||($inmembername =~ /^dir/i)||($inmembername =~ /^print/i)||($inmembername =~ /^con/i)||($inmembername =~ /^nul/i)||($inmembername =~ /^aux/i)||($inmembername =~ /^com/i)||($inmembername =~ /^lpt/i)||($inmembername =~ /^open/i));

    if ($bannedmember eq "yes") { &error("�û�ע��&������ע�ᣬ����д���û�����Email ��ǰ�� IP ������T���óɽ�ֹע�����û��ˣ������������ϵ����T�Ա�����"); }
    
    open(THEFILE,"${lbdir}data/noreglist.cgi");
    $userarray = <THEFILE>;
    close(THEFILE);
    chomp $userarray;
    @saveduserarray = split(/\t/,$userarray);
    $noreg = "no";
    foreach (@saveduserarray) {
	chomp $_;
	$_ =~ s/\|/\\\|/isg;
	if ($inmembername =~ m/$_/isg) {
	    $noreg = "yes";
	    last;
	}
    }
    &error("�û�ע��&�Բ�������ע����û����Ѿ����������߱���ֹע�ᣬ�����һ���û�����") if ($noreg eq "yes");
	
    if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {
        $seed = int(myrand(100000));
        $password = crypt($seed, aun);
        $password =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
        $password =~ s/[^a-zA-Z0-9]//isg;
        $password = substr($password, 4, 8);
    }
        
    if ($interests) {
        $interests =~ s/[\t\r]//g;
        $interests =~ s/  / /g;
        $interests =~ s/\n\n/\<p\>/g;
        $interests =~ s/\n/\<br\>/g;
    }
        
    if ($signature) {
        $signature =~ s/[\t\r]//g;
        $signature =~ s/  / /g;
        $signature =~ s/\n\n/\n\&nbsp;\n/isg;
        $signature =~ s/\n/\[br\]/isg;
        $signature =~ s/\[br\]\[br\]/\[br\]\&nbsp;\[br\]/isg;
	$signature = &dofilter("$signature");
	$signature =~ s/(ev)a(l)/$1&#97;$2/isg;
    }   
    
    my @testsig = split(/\[br\]/,$signature);
    my $siglines = @testsig;
    
    if ($siglines > $maxsignline)           { &error("�û�ע��&�Բ���������ǩ����ֻ������ $maxsignline �У�"); }
    if (length($signature) > $maxsignlegth) { &error("�û�ע��&�Բ���ǩ�����ܳ��� $maxsignlegth �ַ���"); }

    my @testins = split(/\<br\>/,$interests);
    my $inslines = @testins;
    if ($inslines > $maxinsline)           { &error("�û�ע��&�Բ��𣬸��˼��ֻ������ $maxinsline �У�"); }
    if (length($interests) > $maxinslegth) { &error("�û�ע��&�Բ��𣬸��˼�鲻�ܳ��� $maxinslegth �ַ���"); }

    if (($personalavatar)&&($personalwidth)&&($personalheight)) {
        if ($personalavatar !~ /^http:\/\/[\w\W]+\.[\w\W]+$/) { &error("�û�ע��&�Զ���ͷ��� URL ��ַ�����⣡"); }
        if (($personalavatar !~ /\.gif$/isg)&&($personalavatar !~ /\.jpg$/isg)&&($personalavatar !~ /\.png$/isg)&&($personalavatar !~ /\.bmp$/isg)) { &error("�û�ע��&�Զ���ͷ�����Ϊ PNG��GIF �� JPG ��ʽ") ; }
        if (($personalwidth  < 20)||($personalwidth  > $maxposticonwidth))  { &error("�û�ע��&�Բ�������д���Զ���ͼ���ȱ����� 20 -- $maxposticonwidth ����֮�䣡"); }
        if (($personalheight < 20)||($personalheight > $maxposticonheight)) { &error("�û�ע��&�Բ�������д���Զ���ͼ��߶ȱ����� 20 -- $maxposticonheight ����֮�䣡"); }
        $useravatar = "noavatar";
        $personalavatar =~ s/${imagesurl}/\$imagesurl/o;
    }
    else {
    	if ($addme) { $personalavatar=""; } else { $personalavatar=""; $personalwidth=""; $personalheight=""; }
    } #����Զ���ͷ����Ϣ

    if($inmembername =~ /\t/) { &error("�û�ע��&�벻Ҫ���û�����ʹ�������ַ���"); }
    if($password =~ /[^a-zA-Z0-9]/)     { &error("�û�ע��&��̳����ֻ�����Сд��ĸ�����ֵ���ϣ���"); }
    if($password =~ /^lEO/)     { &error("�û�ע��&��̳���벻������ lEO ��ͷ�����������"); }

    $recomm_q = $recommender;
    $recomm_q =~ y/ /_/;
    $recomm_q =~ tr/A-Z/a-z/;
    $member_q = $inmembername;
    $member_q =~ y/ /_/;
    $member_q =~ tr/A-Z/a-z/;
    if ($recomm_q eq $member_q) { &error("�û�ע��&�������Ƽ��Լ���"); }
    
    $tempinmembername =$inmembername;
    $tempinmembername =~ s/ //g;
    $tempinmembername =~ s/��//g;
    if ($tempinmembername eq "")  { &error("�û�ע��&����û����е�����Ӵ����һ����"); }
    if ($inmembername =~ /^����/) { &error("�û�ע��&�벻Ҫ���û����Ŀ�ͷ��ʹ�ÿ���������"); }
    if (length($inmembername)>12) { &error("�û�ע��&�û���̫�����벻Ҫ����12���ַ���6�����֣���"); }
    if (length($inmembername)<2)  { &error("�û�ע��&�û���̫���ˣ��벻Ҫ���2���ַ���1�����֣���"); }
    if (length($newlocation)>16)  { &error("�û�ע��&���Ե����������벻Ҫ����16���ַ���8�����֣���"); }
    
    if (($inmembername =~ m/_/)||(!$inmembername)) { &error("�û�ע��&�û����к��зǷ��ַ���"); }

    if ($passwordverification eq "no"){
	if ($password ne $password2) { &error("�û�ע��&�Բ����������������̳���벻��ͬ��");   }
        if(length($password)<8)      { &error("�û�ע��&��̳����̫���ˣ����������̳������� 8 λ���ϣ�"); }
#       if ($password =~ /^[0-9]+$/) { &error("�û�ע��&��̳�����벻Ҫȫ��Ϊ���֣��������"); }
    }

    if ($inmembername eq $password) { &error("�û�ע��&�����û�������̳�������ó���ͬ��"); } 

    if($emailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,4})(\]?)$/) { &error("�û�ע��&�ʼ���ַ����"); }
    $emailaddress =~ s/[\ \a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
    $homepage =~ s/[\ \a\f\n\e\0\r\t\|\$\@]//isg;
    $homepage =~ s/ARGV//isg;
    $homepage =~ s/system//isg;

    &getmember("$inmembername","no");
    if ($userregistered ne "no") { &error("�û�ע��&���û��Ѿ����ڣ�����������һ���µ��û�����"); }
    $membercode    = "me";
    
    $memberfiletitle = $inmembername;
    $memberfiletitle =~ y/ /_/;
    $memberfiletitle =~ tr/A-Z/a-z/;
    $memberfiletitletemp = unpack("H*","$memberfiletitle");
if ($addme) {

    my ($filename) = $addme =~ m|([^/:\\]+)$|; #ע��,��ȡ�ļ����ֵ���ʽ�仯
    my $fileexp;

    $fileexp =  ($filename =~ /\.jpe?g\s*$/i) ? 'jpg'
	        :($filename =~ /\.gif\s*$/i)  ? 'gif'
		:($filename =~ /\.png\s*$/i)  ? 'png'
		:($filename =~ /\.swf\s*$/i)  ? 'swf'
		:($filename =~ /\.bmp\s*$/i)  ? 'bmp'
		:undef;
    $maxuploadava = 200 if (($maxuploadava eq "")||($maxuploadava < 1));
	
    if (($fileexp eq "swf")&&($flashavatar ne "yes")) { &error("��֧�������ϴ���ͼƬ��������ѡ��&��֧�� GIF��JPG��PNG��BMP ����!"); }
    if (!defined $fileexp) { &error("��֧�������ϴ���ͼƬ��������ѡ��&��֧�� GIF��JPG��PNG��BMP��SWF ����!"); }

    my $filesize=0;
    my $buffer;
    open (FILE,">${imagesdir}/usravatars/$memberfiletitletemp.$fileexp");
    binmode (FILE);
    binmode ($addme); #ע��
    while (((read($addme,$buffer,4096)))&&!($filesize>$maxuploadava)) {
	print FILE $buffer;
	$filesize=$filesize+4;
    }
    close (FILE);
    close ($addme);

    if ($fileexp eq "gif"||$fileexp eq "jpg"||$fileexp eq "bmp"||$fileexp eq "jpeg"||$fileexp eq "png") {
      eval("use Image::Info qw(image_info);"); 
      if ($@ eq "") { 
        my $info = image_info("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
	if ($info->{error} eq "Unrecognized file format"){
            unlink ("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
            &error("�ϴ�����&�ϴ��ļ�����ͼƬ�ļ������ϴ���׼��ͼƬ�ļ���");
        }
            if ($personalwidth eq "" || $personalwidth eq 0) {
            	if ($info->{width} ne "") { $personalwidth = $info->{width}; }
            	elsif ($info->{ExifImageWidth} ne "") { $personalwidth = $info->{ExifImageWidth}; }
            }
            if ($personalheight eq "" || $personalheight eq 0) {
            	if ($info->{height} ne "") { $personalheight = $info->{height}; }
            	elsif ($info->{ExifImageLength} ne "") { $personalheight = $info->{ExifImageLength}; }
            }
        undef $info;
      }
    }
    if ($filesize>$maxuploadava) {
        unlink ("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
	&error("�ϴ�����&�ϴ��ļ���С����$maxuploadava��������ѡ��");
    }

    if (($personalwidth  < 20)||($personalwidth  > $maxposticonwidth))  { &error("�û�ע��&�Բ�������д���Զ���ͼ����($personalwidth)������ 20 -- $maxposticonwidth ����֮�䣡"); }
    if (($personalheight < 20)||($personalheight > $maxposticonheight)) { &error("�û�ע��&�Բ�������д���Զ���ͼ��߶�($personalheight)������ 20 -- $maxposticonheight ����֮�䣡"); }

    $useravatar="noavatar";
    $personalavatar="\$imagesurl/usravatars/$memberfiletitletemp.$fileexp";
}
    if ($useverify eq "yes") {
        &error("�û�ע��&�Բ����������У��������������Ѿ����ڣ�") if (&checkverify);
    }

    $regcontrollimit = 30 if (($regcontrollimit eq "")||($regcontrollimit < 0 ));
    $regcontrol = 0;

    $filetoopen = "$lbdir" . "data/lastregtime.cgi";
    if (-e "$filetoopen") {
	open(FILE,"$filetoopen");
	my $lastfiledate = <FILE>;
        close(FILE);
        chomp $lastfiledate;
        my ($lastregtime,$lastregip) = split(/\|/,$lastfiledate);
        $lastregtime = $lastregtime + $regcontrollimit;
        if (($lastregtime > $joineddate)&&($ipaddress eq $lastregip)) { $regcontrol = 1; }
    }
    open(FILE,">$filetoopen");
    print FILE "$joineddate|$ipaddress";
    close(FILE);
        
    if ($regcontrol eq 1) { &error("�û�ע��&�Բ���������ȴ� $regcontrollimit ���Ӳ����ٴ�ע�ᣡ"); }

    if ($adminverification eq "yes") {
	$emailaddress1 = $emailaddress;
        $emailaddress  = $adminemail_out;
    }

if ($password ne "") {
    $notmd5password = $password;
    eval {$password = md5_hex($password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$password = md5_hex($password);');}
    unless ($@) {$password = "lEO$password";}
}
else {
    $notmd5password = $password;
}

    $signature=~s/\n/<br>/g; 
    require "dosignlbcode.pl";
    $signature1=&signlbcode($signature); 
    $signature=$signature."aShDFSiod".$signature1; 
    mkdir ("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
    chmod(0777,"${lbdir}$memdir/old");
    my $namenumber = &getnamenumber($memberfiletitle);
    $filetomake = "$lbdir" . "$memdir/$namenumber/$memberfiletitle.cgi";
    if (open(FILE, ">$filetomake")) {
        print FILE "$inmembername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$newlocation\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t0\t$lastgone\t1\t$useradd04\t$useradd02\t$mymoney\t0\t$sex\t$education\t$marry\t$work\t$born\t\t\t\t\t\t\t$userquestion\t\t$jifen\t\t$soccerdata\t0\t";
        close(FILE);
    }
    $filetomake = "$lbdir" . "$memdir/old/$memberfiletitle.cgi";
    if (open(FILE, ">$filetomake")) {
        print FILE "$inmembername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$newlocation\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t0\t$lastgone\t1\t$useradd04\t$useradd02\t$mymoney\t0\t$sex\t$education\t$marry\t$work\t$born\t\t\t\t\t\t\t$userquestion\t\t$jifen\t\t$soccerdata\t0\t";
        close(FILE);
    }

    if (($recommender ne "") && ($recomm_q ne $member_q)) {
        $recomm_q = &stripMETA($recomm_q);
	$namenumber = &getnamenumber($recomm_q);
	&checkmemfile($recomm_q,$namenumber);
        my $filetoopen = "${lbdir}$memdir/$namenumber/$recomm_q.cgi";
        if (-e $filetoopen) { &recommfunc("$recommender");  $recommfuncerror = ""; }
                       else { $recommfuncerror = " (ע�⣺�Ƽ����û��������ڣ�)"; }
    }

    $filetomakeopen = "${lbdir}data/lbmember.cgi";
    if (open (MEMFILE, ">>$filetomakeopen")) {
	print MEMFILE "$inmembername\t$membercode\t0\t$joineddate\t$emailaddress\t\n";
	close (MEMFILE);
    }

   $filetomakeopen = "${lbdir}data/lbemail/$charone.cgi";
   if (open (MEMFILE, ">>$filetomakeopen")) {
	print MEMFILE "$emailaddress\t$inmembername\n";
	close (MEMFILE);
   }

    if (($born ne "")&&($born ne "//")) {
	$filetomakeopen = "${lbdir}data/lbmember3.cgi";
	if (open (MEMFILE, ">>$filetomakeopen")) {
	    print MEMFILE "$inmembername\t$born\t\n";
	    close (MEMFILE);
	}
	$month = int($month);
	if (open (MEMFILE, ">>${lbdir}calendar/borninfo$month.cgi")) {
	    print MEMFILE "$inmembername\t$born\t\n";
	    close (MEMFILE);
	}
    }

    $filetomakeopen = "${lbdir}data/lbmember4.cgi";
    if (open (MEMFILE, ">>$filetomakeopen")) {
	print MEMFILE "$inmembername\t$ipaddress\t\n";
	close (MEMFILE);
    }

    $inmembername =~ y/_/ /;
    $inmemberfile = $inmembername;
    $inmemberfile =~ y/ /_/;
    $inmemberfile =~ tr/A-Z/a-z/;
    $currenttime = time ;
    if ($sendwelcomemessage ne "no" && $allowusemsg ne "off") {
        $filetoopen = "$lbdir" . "data/newusrmsg.dat";
	open(FILE,$filetoopen);
	sysread(FILE, $tempoutput,(stat(FILE))[7]);
    	close(FILE);
        $tempoutput =~ s/\r//isg;

	$tempoutput =~ s/\n//;

        $filetoopen = "$lbdir". "$msgdir/in/$inmemberfile" . "_msg.cgi";
        if (open (FILE, ">$filetoopen")) {
            print FILE "����������ȫ�������Ա\tno\t$currenttime\t��ӭ������$boardname��ף��ʹ����죡\t$tempoutput<BR><BR>----------------------------<BR>LeoBBS ���װ��Ƽ�������Ʒ<BR>��ҳ:<a href=http://www.LeoBBS.com target=_blank>http://www.LeoBBS.com</a>\n";
            close (FILE);
        }
    }
    ###����ע���ż�
    if  (($passwordverification eq "no") && ($emailfunctions ne "off")) {
	$to = $emailaddress;
        $from = $adminemail_out;
	$subject = "��л����$boardname��ע�ᣡ";              
        $message .= "\n��ӭ�����$boardname! <br>\n";
        $message .= "��̳URL: $boardurl/leobbs.cgi\n <br><br>\n <br>\n";
        $message .= "------------------------------------<br>\n";
        $message .= "�����û�������̳�������¡�\n <br>\n";
        $message .= "�û����� $inmembername <br>\n";
        $message .= "��̳���룺 $notmd5password\n <br><br>\n <br>\n";
        $message .= "Ҫע����̳���������ִ�Сд��\n <br>\n";
        $message .= "����ʱ����ʹ���û������޸�������̳���� <br>\n";
        $message .= "������ı��������ʼ���ַ�� <br>\n";
        $message .= "������һ���µ���̳����ĸ�����\n <br><br>\n";
        $message .= "------------------------------------<br>\n";      
        &sendmail($from, $from, $to, $subject, $message);
    }
    ####����ע���ż�����
  
    if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {
	$namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/", -expires => "now");
	$passcookie = cookie(-name => "apasswordcookie"  , -value => "", -path => "$cookiepath/", -expires => "now");

	if ($adminverification eq "yes") {
	    $to = $adminemail_out;
	    $from = $emailaddress;
	    $subject = "�ȴ�����֤$boardname�е�ע�ᣡ";
	    $message .= "\n��ӭ�����$boardname��\n";
	    $message .= "��̳URL:$boardurl/leobbs.cgi\n\n\n";
	    $message .= "------------------------------------\n";
	    $message .= "�����û�������̳�������¡�\n\n";
	    $message .= "�û����� $inmembername\n";
	    $message .= "��̳���룺 $notmd5password\n\n\n";
	    $message .= "��  �䣺 $emailaddress1\n\n\n";
	    $message .= "��̳���������ִ�Сд��\n\n";
	    $message .= "��������¼���޸�����(���������ǹ���Ա��\n";
	    $message .= "����)���������µ���̳����ֱ�Ӽĸ�����\n\n";
	    $message .= "------------------------------------\n";
	    $message .= "��ظ���ת����֤�û�Ա����Ҫ�����޸����䣡\n";
	} else {
	    $to = $emailaddress;
	    $from = $adminemail_out;
	    $subject = "��л����$boardname��ע�ᣡ";
	    $message .= "\n��ӭ�����$boardname��<br>\n";
	    $message .= "��̳URL:$boardurl/leobbs.cgi\n <br><br>\n <br>\n";
	    $message .= "------------------------------------<br>\n";
	    $message .= "�����û�������̳�������¡�\n<br><br>\n";
            $message .= "�û����� $inmembername <br>\n";
	    $message .= "��̳���룺 $notmd5password\n <br><br>\n<br>\n";
	    $message .= "��̳���������ִ�Сд�� \n<br><br>\n";
	    $message .= "����ʱ����ʹ���û������޸�������̳���� <br>\n";
	    $message .= "������ı��������ʼ���ַ�� <br>\n";
	    $message .= "������һ���µ���̳����ĸ����� <br><br>\n\n";
	    $message .= "------------------------------------<br>\n";
	}
	&sendmail($from, $from, $to, $subject, $message);
    }

    if ($newusernotify eq "yes" && $emailfunctions ne "off") {
	$to = $adminemail_in;
	$from = $adminemail_out;
	$subject = "$boardname�����û�ע���ˣ�";
	$message = "\n��̳��$boardname <br>\n";
	$message .= "��̳URL:$boardurl/leobbs.cgi <br>\n";
	$message .= "-------------------------------------\n<br><br>\n";
	$message .= "���û�ע�����Ϣ���¡� <br><br>\n\n";
	$message .= "�û����� $inmembername <br>\n";
	$message .= "��  �룺 $notmd5password <br>\n";
	$message .= "��  ���� $emailaddress <br>\n";
	$message .= "��  ҳ�� $homepage <br>\n";
	$message .= "IP��ַ�� $ipaddress\n <br><br>\n";
	$message .= "�Ƽ��ˣ� $recommender\n <br><br>\n" if ($recommender ne "");
	$message .= "------------------------------------<br>\n";
	&sendmail($from, $from, $to, $subject, $message);
    }

    if ($inforum eq "") { $refrashurl = "leobbs.cgi"; } else { $refrashurl = "forums.cgi?forum=$inforum"; }
    $output .= qq~<tr>
	<td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>��л��ע�ᣬ$inmembername</b>$recommfuncerror</font></td></tr><tr>
        <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>���������<ul><li><a href="$refrashurl">���˷�����̳</a>
        <meta http-equiv="refresh" content="3; url=$refrashurl">
	</ul></tr></td></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;

    if (($passwordverification eq "yes") && ($emailfunctions ne "off")) { $output =~ s/���˷�����̳/������̳�����Ѿ��ĳ������˷�����̳��Ȼ��ʹ���ʼ��е������¼/; }
    else {
        $namecookie = cookie(-name => "amembernamecookie", -value => "$inmembername", -path => "$cookiepath/", -expires => "+30d");
        $passcookie = cookie(-name => "apasswordcookie"  , -value => "$password"    , -path => "$cookiepath/", -expires => "+30d");
    }
    require "$lbdir" . "data/boardstats.cgi";
    $filetomake = "$lbdir" . "data/boardstats.cgi";
    my $filetoopens = &lockfilename($filetomake);
    if (!(-e "$filetoopens.lck")) {
	$totalmembers++;
	&winlock($filetomake) if ($OS_USED eq "Nt");
	if (open(FILE, ">$filetomake")) {
	    flock(FILE, 2) if ($OS_USED eq "Unix");
	    print FILE "\$lastregisteredmember = \'$inmembername\'\;\n";
	    print FILE "\$totalmembers = \'$totalmembers\'\;\n";
	    print FILE "\$totalthreads = \'$totalthreads\'\;\n";
	    print FILE "\$totalposts = \'$totalposts\'\;\n";
	    print FILE "\n1\;";
	    close (FILE);
	}
	&winunlock($filetomake) if ($OS_USED eq "Nt");
    }
    else {
    	unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
    }
}
elsif ($action eq "agreed") {
require "cleanolddata.pl";
&cleanolddata1;
    if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {
	if ($adminverification eq "yes") {
	    $requirepass = qq~<tr><td bgcolor=$miscbackone colspan=2 align=center><font color=$fontcolormisc><b>������̳���뽫ͨ���ʼ��ĸ�����Ա���ھ�������Ա��֤�󽫳������ע�ᣡ</td></tr>~;
        } else {
    	    $requirepass = qq~<tr><td bgcolor=$miscbackone colspan=2 align=center><font color=$fontcolormisc><b>������̳���뽫ͨ���ʼ��ĸ���<BR>�����һֱû���յ��ʼ�����ô����ע�����Ƿ񱻷ŵ������������ˣ�</td></tr>~;
	}
	$qa=qq~~;
    } else {
        $requirepass = qq~<tr>
        <td bgcolor=$miscbackone width=40%><font color=$fontcolormisc><b>��̳���룺 (����8λ)</b><br>��������̳���룬���ִ�Сд<br>ֻ��ʹ�ô�Сд��ĸ�����ֵ����</td>
        <td bgcolor=$miscbackone width=60%><input type=password name="password" maxlength=20>&nbsp;* ���������д</td>
        </tr><tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc><b>��̳���룺 (����8λ)</b><br>����һ�飬�Ա�ȷ����</td>
        <td bgcolor=$miscbackone><input type=password name="password2" maxlength=20>&nbsp;* ���������д</td>
        </tr>~;
        $qa=qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��̳������ʾ���⣺</b>����ȡ�������˵���̳����<br>��� 20 ���ֽڣ�10�����֣�</td> 
<td bgcolor=$miscbackone><input type=text name="getpassq" value="" size=20 maxlength=20></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��̳������ʾ�𰸣�</b>�������ʹ��<br>��� 20 ���ֽڣ�10�����֣�</td> 
<td bgcolor=$miscbackone><input type=text name="getpassa" value="" size=20 maxlength=20></td></tr>~;
	$passcheck = qq~	if (document.creator.password.value == '')
	{
		window.alert('����û�������������룡');
		document.creator.password.focus();
		return false;
	}
	if (document.creator.password.value != document.creator.password2.value)
	{
		window.alert('������������벻һ�£�');
		document.creator.password.focus();
		return false;
	}
	if (document.creator.password.value.length < 8)
	{
		window.alert('����̫���ˣ��������������� 8 λ���ϣ�');
		document.creator.password.focus();
		return false;
	}~;
    }

    if ($avatars eq "on") {
	if ($arrowavaupload eq "on") { $avaupload = qq~<br>�ϴ�ͷ�� <input type="file" size=20 name="addme">���ϴ��Զ���ͷ��<br>~;} else { undef $avaupload; }
        open (FILE, "${lbdir}data/lbava.cgi");
	sysread(FILE, $totleavator,(stat(FILE))[7]);
        close (FILE);
        $totleavator =~ s/\r//isg;
        my @images = split (/\n/, $totleavator);
        $totleavator = @images -1;
        $selecthtml .= qq~<option value="noavatar" selected>��Ҫͷ��</option>\n~;
        $currentface = "noavatar";

        foreach (@images) {
            $_ =~ s/\.(gif|jpg)$//i;
            next if ($_ =~ /admin_/);
            if ($_ ne "noavatar") { $selecthtml .= qq~<option value="$_">$_</option>\n~; }
        }

        $avatarhtml = qq~<script language="javascript">
function showimage(){document.images.useravatars.src="$imagesurl/avatars/"+document.creator.useravatar.options[document.creator.useravatar.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>����ͼƬ��</b><br>������ѡ��һ������ͼƬ�����㷢��ʱ����ʾ�����������·���<BR>�������д��������Զ���ͷ�񲿷֣���ô���ͷ�����Զ����Ϊ׼���������������Զ���ͷ���������Ŀ��<BR>
<br><br><b>�����Զ���ͷ��</b>��<br>��Ҳ����������������Զ���ͷ��� URL ��ַ��ͷ��ĸ߶ȺͿ��(����)�� �������Ҫ�Զ���ͷ���뽫��Ӧ��Ŀȫ�����գ�<BR>�������дͷ��ĸ߶ȺͿ�ȣ���ϵͳ���Զ��жϲ����롣<BR><BR>
<br><b>����㲻��Ҫ�κε�ͷ����ô�������ڲ˵���ѡ����Ҫͷ�񡱣�Ȼ�����������Զ���ͷ��Ĳ��֣�</b><BR><br>
<td bgcolor=$miscbackone valign=top>��ͷ������� $totleavator ������<a href=viewavatars.cgi target=_blank><B>���˲鿴</B></a>����ͷ�������б�<BR>
<select name="useravatar" size=1 onChange="showimage()">
$selecthtml
</select>
<img src=$imagesurl/avatars/$currentface.gif name="useravatars" width=32 height=32 hspace=15><br><br><br>
$avaupload
<br>ͼ��λ�ã� <input type=text name="personalavatar" size=20 value="">������������ URL ·����<br>
<br>ͼ���ȣ� <input type=text name="personalwidth" size=2 maxlength=3 value=32>�������� 20 -- $maxposticonwidth ֮���һ��������<br>
<br>ͼ��߶ȣ� <input type=text name="personalheight" size=2 maxlength=3 value=32>�������� 20 -- $maxposticonheight ֮���һ��������<br></td>
</td></tr>~;
    }

    $flaghtml = qq~<script language="javascript">
function showflag(){document.images.userflags.src="$imagesurl/flags/"+document.creator.userflag.options[document.creator.userflag.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=$miscbackone valign=top><font face=$font color=$fontcolormisc><b>���ڹ���:</b><br>��ѡ�������ڵĹ��ҡ�</td>
<td bgcolor=$miscbackone>
<select name="userflag" size=1 onChange="showflag()">
<option value="blank" selected>����</option>
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
<option value="Czech_Republic">�ݿ�</option>
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
<option value="Russia">����˹</option>
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
<img src="$imagesurl/flags/blank.gif" name="userflags" border=0 height=14 width=21>
</td></tr>~;

if ($useverify eq "yes") {

    if ($verifyusegd ne "no") {
	eval ('use GD;');
	if ($@) {
            $verifyusegd = "no";
        }
    }
    if ($verifyusegd eq "no") {
	$houzhui = "bmp";
    } else {
	$houzhui = "png";
    }

    require 'verifynum.cgi';
    $venumcheck = qq~
    	if (document.creator.verifynum.value.length < 4)
	{
		window.alert('��������ȷ��У���룡');
		return false;
	}
    ~;
}
    $output .= qq~<script>
function Check(){
var Name=document.creator.inmembername.value;
window.open("./checkname.cgi?name="+Name,"Check","width=200,height=20,status=0,scrollbars=0,resizable=1,menubar=0,toolbar=0,location=0");
}
function CheckInput()
{
	if (document.creator.inmembername.value == '')
	{
		window.alert('����û����д�û����أ�');
		document.creator.inmembername.focus();
		return false;
	}
	if (document.creator.inmembername.value.length > 12)
	{
		window.alert('�����û���̫���ˣ��벻Ҫ����12���ַ���6�����֣���');
		document.creator.inmembername.focus();
		return false;
	}

$passcheck

	var s = document.creator.emailaddress.value;
	if (s.length > 50)
	{
		window.alert('Email��ַ���Ȳ��ܳ���50λ!');
		return false;
	}

$venumcheck;
	return true;
}
</script>

<form action="$thisprog" method=post name="creator" enctype="multipart/form-data" OnSubmit="return CheckInput()"><tr>
<input type=hidden name="forum" value="$inforum">
<td bgcolor=$miscbacktwo width=40%><font color=$fontcolormisc><b>�û�����</b><br>ע���û������ܳ���12���ַ���6�����֣�</td>
<td bgcolor=$miscbacktwo width=60%><input type=text maxlength="12" name="inmembername">&nbsp;<input onClick="javascript:Check()" type=button value="����ʺ�" name="button" class="button">&nbsp;* ���������д</td>
</tr>$requirepass
<tr><td bgcolor=$miscbacktwo><font color=$fontcolormisc><b>�ʼ���ַ��</b><br>��������Ч���ʼ���ַ���⽫ʹ�����õ���̳�е����й���</td>
<td bgcolor=$miscbacktwo><input type=text name="emailaddress">&nbsp;* ���������д</td></tr>
~;

#	var regu = "^(([0-9a-zA-Z]+)|([0-9a-zA-Z]+[_.0-9a-zA-Z-]*[0-9a-zA-Z]+))\@([a-zA-Z0-9-]+[.])+([a-zA-Z]{4}|net|NET|com|COM|gov|GOV|mil|MIL|org|ORG|edu|EDU|int|INT|name|shop|NAME|SHOP)\$";
#	var re = new RegExp(regu);
#	if (s.search(re) == -1)
#	{
#		window.alert ('��������Ч�Ϸ���E-mail��ַ��')
#		return false;
#       }

$output .= qq~<tr><td bgcolor=$miscbacktwo><font color=$fontcolormisc><b>ע����֤�룺(��֤����Ч��Ϊ20����)</b><br>���������е���֤�룬���벻��ȷʱ����������ע�ᡣ<br>��ע�⣺ֻ�����֣� 0 ���������Ӣ����ĸ�� O��</font></td><td bgcolor=$miscbacktwo><input type=hidden name=sessionid value="$sessionid"><input type=text name="verifynum" size=4 maxlength=4> * <img src=$imagesurl/verifynum/$sessionid.$houzhui align=absmiddle> һ�����ĸ����֣���������壬��ˢ��</td></tr>~  if ($useverify eq "yes");
$output .= qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�Ƽ����û�����</b><br>��˭�Ƽ����������ǵ������ģ�(�⽫ʹ����Ƽ��˻���ֵ����)</td>
<td bgcolor=$miscbackone><input type=text name="recommender">&nbsp;��û���뱣�ֿհ�</td>
</tr></table></td></tr></table>
~;
    if ($advreg == 1) { 
	$advregister = "true"; 
	$advmode = qq~<td width=50%><INPUT id=advcheck name=advshow type=checkbox value=1 checked onclick=showadv()><span id="advance">�رո���ע��ѡ��</a></span> </td><td width=50%><input type=submit value="ע ��" name=submit></td>~;
    } else {
	$advregister = "none"; 
	$advmode = qq~<td width=50%><INPUT id=advcheck name=advshow type=checkbox value=1 onclick=showadv()><span id="advance">��ʾ����ע��ѡ��</a></span> </td><td width=50%><input type=submit value="ע ��" name=submit></td>~;
    }
    $output .=qq~<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center id=adv style="DISPLAY: $advregister"><tr><td>
<table cellpadding=4 cellspacing=1 width=100%>
$qa
<tr><td bgcolor=$miscbacktwo valign=middle colspan=2 align=center> 
<font color=$fonthighlight><b>��̳������ʾ����ʹ��ǲ��ܹ��޸ĵģ���������룡</b></font></td></tr>
<tr>
<td bgcolor=$miscbackone width=40%><font color=$fontcolormisc><b>��ʾ�ʼ���ַ</b><br>���Ƿ�ϣ��������������֮����ʾ�����ʼ���</td>
<td bgcolor=$miscbackone width=60%><font color=$fontcolormisc><input name="showemail" type="radio" value="yes" checked> �ǡ� <input name="showemail" type="radio" value="msn"> MSN�� <input name="showemail" type="radio" value="popo"> �������ݡ� <input name="showemail" type="radio" value="no"> ��</font></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>�Ա�</b></td><td bgcolor=$miscbackone>
<select name="sex" size="1">
<option value="no">���� </option>
<option value="m">˧�� </option>
<option value="f">��Ů </option>
</select>
</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>���ѧ��</b></td>
<td bgcolor=$miscbackone>
<select name="education" size="1">
<option value="����">���� </option>
<option value="Сѧ">Сѧ </option>
<option value="����">���� </option>
<option value="����">����</option>
<option value="��ר">��ר</option>
<option value="����">����</option>
<option value="˶ʿ">˶ʿ</option>
<option value="��ʿ">��ʿ</option>
<option value="��ʿ��">��ʿ��</option>
</select>
</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>����״��</b></td>
<td bgcolor=$miscbackone>
<select name="marry" size="1">
<option value="����">���� </option>
<option value="δ��">δ�� </option>
<option value="�ѻ�">�ѻ� </option>
<option value="���">��� </option>
<option value="ɥż">ɥż </option>
</select>
</td></tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>ְҵ״��</b></td>
<td bgcolor=$miscbackone>
<select name="work" size="1">
<option value="����">���� </option>
<option value="�����ҵ">�����ҵ </option>
<option value="����ҵ">����ҵ </option>
<option value="��ҵ">��ҵ </option>
<option value="������ҵ">������ҵ </option>
<option value="����ҵ">����ҵ </option>
<option value="ѧ��">ѧ�� </option>
<option value="����ʦ">����ʦ </option>
<option value="���ܣ�����">���ܣ����� </option>
<option value="��������">�������� </option>
<option value="����ҵ">����ҵ </option>
<option value="����/���/�г�">����/���/�г� </option>
<option value="ʧҵ��">ʧҵ�� </option>
</select>
</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>���գ�</b>�粻����д����ȫ�����ա������ѡ</td>
<td bgcolor=$miscbackone><input type="text" name="year" size=4 maxlength=4>�� 
  <select name="month">
      <option value="" selected></option>
      <option value="01">01</option>
      <option value="02">02</option>
      <option value="03">03</option>
      <option value="04">04</option>
      <option value="05">05</option>
      <option value="06">06</option>
      <option value="07">07</option>
      <option value="08">08</option>
      <option value="09">09</option>
      <option value="10">10</option>
      <option value="11">11</option>
      <option value="12">12</option>
  </select>��
   <select name="day">
      <option value="" selected></option>
      <option value="01">01</option>
      <option value="02">02</option>
      <option value="03">03</option>
      <option value="04">04</option>
      <option value="05">05</option>
      <option value="06">06</option>
      <option value="07">07</option>
      <option value="08">08</option>
      <option value="09">09</option>
      <option value="10">10</option>
      <option value="11">11</option>
      <option value="12">12</option>
      <option value="13">13</option>
      <option value="14">14</option>
      <option value="15">15</option>
      <option value="16">16</option>
      <option value="17">17</option>
      <option value="18">18</option>
      <option value="19">19</option>
      <option value="20">20</option>
      <option value="21">21</option>
      <option value="22">22</option>
      <option value="23">23</option>
      <option value="24">24</option>
      <option value="25">25</option>
      <option value="26">26</option>
      <option value="27">27</option>
      <option value="28">28</option>
      <option value="29">29</option>
      <option value="30">30</option>
      <option value="31">31</option>
  </select>��
</td>
</tr>
<tr><SCRIPT language=javascript>
function showsx(){document.images.usersxs.src="$imagesurl/sx/"+document.creator.usersx.options[document.creator.usersx.selectedIndex].value+".gif";}
</SCRIPT>
<td bgcolor=$miscbackone vAlign=top><font color=$fontcolormisc><b>������Ф��</b><br>��ѡ������������Ф��</td>
<td bgcolor=$miscbackone><SELECT name=\"usersx\" onchange=showsx() size=\"1\"> <OPTION value=blank>����</OPTION> <OPTION value=\"sx1\">����</OPTION> <OPTION value=\"sx2\">��ţ</OPTION> <OPTION value=\"sx3\">����</OPTION> <OPTION value=\"sx4\">î��</OPTION> <OPTION value=\"sx5\">����</OPTION> <OPTION value=\"sx6\">����</OPTION> <OPTION value=\"sx7\">����</OPTION> <OPTION value=\"sx8\">δ��</OPTION> <OPTION value=\"sx9\">���</OPTION> <OPTION value=\"sx10\">�ϼ�</OPTION> <OPTION value=\"sx11\">�繷</OPTION> <OPTION value=\"sx12\">����</OPTION></SELECT> <IMG border=0 name=usersxs src="$imagesurl/sx/blank.gif" align="absmiddle">
</TD></tr><tr>
<SCRIPT language=javascript>
function showxz(){document.images.userxzs.src="$imagesurl/star/"+document.creator.userxz.options[document.creator.userxz.selectedIndex].value+".gif";}
</SCRIPT>
<td bgcolor=$miscbackone vAlign=top><font color=$fontcolormisc><b>����������</b><br>��ѡ����������������<br>�������ȷ���������յĻ�����ô������Ч��</td>
<td bgcolor=$miscbackone><SELECT name=\"userxz\" onchange=showxz() size=\"1\"> <OPTION value=blank>����</OPTION> <OPTION value=\"z1\">������(3��21--4��19��)</OPTION> <OPTION value=\"z2\">��ţ��(4��20--5��20��)</OPTION> <OPTION value=\"z3\">˫����(5��21--6��21��)</OPTION> <OPTION value=\"z4\">��з��(6��22--7��22��)</OPTION> <OPTION value=\"z5\">ʨ����(7��23--8��22��)</OPTION> <OPTION value=\"z6\">��Ů��(8��23--9��22��)</OPTION> <OPTION value=\"z7\">�����(9��23--10��23��)</OPTION> <OPTION value=\"z8\">��Ы��(10��24--11��21��)</OPTION> <OPTION value=\"z9\">������(11��22--12��21��)</OPTION> <OPTION value=\"z10\">ħ����(12��22--1��19��)</OPTION> <OPTION value=\"z11\">ˮƿ��(1��20--2��18��)</OPTION> <OPTION value=\"z12\">˫����(2��19--3��20��)</OPTION></SELECT> <IMG border=0 name=userxzs src="$imagesurl/star/blank.gif" width=15 height=15 align="absmiddle">
</TD>
</TR><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>��ҳ��ַ��</b><br>���������ҳ����������ҳ��ַ�������ѡ</td>
<td bgcolor=$miscbackone><input type=text name="homepage" value="http://"></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>OICQ �ţ�</b><br>������� OICQ����������롣�����ѡ</td>
<td bgcolor=$miscbackone><input type=text name="oicqnumber"></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>ICQ �ţ�</b><br>������� ICQ����������롣�����ѡ</td>
<td bgcolor=$miscbackone><input type=text name="icqnumber"></td>
</tr>$flaghtml<tr>
<script src=$imagesurl/images/comefrom.js></script>
<body onload="init()">
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>���ԣ�</b><br>�����������ڹ��ҵľ���ط��������ѡ</td>
<td bgcolor=$miscbackone>
ʡ�� <select name="province" onChange = "select()"></select>������ <select name="city" onChange = "select()"></select><br>
���� <input type=text name="newlocation" maxlength=12 size=12 style="font-weight: bold">�����ܳ���12���ַ���6�����֣�
</td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>ʱ�</b><br>
����������ʱ����$basetimes<br>��������ڵ�λ�úͷ�������ʱ������롣<br>���������е�ʱ�佫���������ڵĵ���ʱ����ʾ��</td>
<td bgcolor=$miscbackone>
<select name="timedifference"><option value="-23">- 23</option><option value="-22">- 22</option><option value="-21">- 21</option><option value="-20">- 20</option><option value="-19">- 19</option><option value="-18">- 18</option><option value="-17">- 17</option><option value="-16">- 16</option><option value="-15">- 15</option><option value="-14">- 14</option><option value="-13">- 13</option><option value="-12">- 12</option><option value="-11">- 11</option><option value="-10">- 10</option><option value="-9">- 9</option><option value="-8">- 8</option><option value="-7">- 7</option><option value="-6">- 6</option><option value="-5">- 5</option><option value="-4">- 4</option><option value="-3">- 3</option><option value="-2">- 2</option><option value="-1">- 1</option><option value="0" selected>0</option><option value="1">+ 1</option><option value="2">+ 2</option><option value="3">+ 3</option><option value="4">+ 4</option><option value="5">+ 5</option><option value="6">+ 6</option><option value="7">+ 7</option><option value="8">+ 8</option><option value="9">+ 9</option><option value="10">+ 10</option><option value="11">+ 11</option><option value="12">+ 12</option><option value="13">+ 13</option><option value="14">+ 14</option><option value="15">+ 15</option><option value="16">+ 16</option><option value="17">+ 17</option><option value="18">+ 18</option><option value="19">+ 19</option><option value="20">+ 20</option><option value="21">+ 21</option><option value="22">+ 22</option><option value="23">+ 23</option></select> Сʱ
</td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>���Ҽ�飺 </b><BR>���ܳ��� <B>$maxinsline</B> �У�Ҳ���ܳ��� <B>$maxinslegth</B> ���ַ�<br><br>�������ڴ��������ĸ��˼�顣�����ѡ</td>
<td bgcolor=$miscbackone><textarea name="interests" cols="60" rows="5"></textarea></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>ǩ����</b><br>���ܳ��� <B>$maxsignline</B> �У�Ҳ���ܳ��� <B>$maxsignlegth</B> ���ַ�
<br><br>����ʹ�� HTML ��ǩ<br>����ʹ�� <a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS ��ǩ</a><BR>
<li>��ͼ��ǩ��: <b>$signpicstates</b><li>Flash ��ǩ: <b>$signflashstates</b><li>���ֱ�ǩ��: <b>$signsoundstates</b><li>���ִ�С��: <b>$signfontsizestates</b>
</td>
<td bgcolor=$miscbackone><textarea name="signature" cols="60" rows="8"></textarea></td>
</tr>
$avatarhtml
</table></td></tr><SCRIPT>valignend()</SCRIPT>
<script>
function showadv(){
if (document.creator.advshow.checked == true) {
adv.style.display = "";
advance.innerText="�رո����û�����ѡ��"
}else{
adv.style.display = "none";
advance.innerText="��ʾ�����û�����ѡ��"
}
}
</script>
</tr></table><img src="" width=0 height=4><BR>
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
<tr>
$advmode 
<input type=hidden name=action value=addmember></form></tr></table><BR>
~;
}
else {
    require "cleanolddata.pl";
    &cleanolddata;
    $regdisptime = 15 if ($regdisptime <1);
    $filetoopen = "$lbdir" . "data/register.dat";
    open(FILE,$filetoopen);
    sysread(FILE, my $tempoutput,(stat(FILE))[7]);
    close(FILE);
    $tempoutput =~ s/\r//isg;

    $output .= qq~<tr>
    <td bgcolor=$titlecolor $catbackpic align=center>
    <form action="$thisprog" method="post" name="agree">
    <input name="action" type="hidden" value="agreed">
    <input type=hidden name="forum" value="$inforum">
    <font color=$fontcolormisc>
    <b>�������������</b>
    </td></tr>
    <td bgcolor=$miscbackone><font color=$fontcolormisc>
    $tempoutput
    </td></tr>
    <tr><td bgcolor=$miscbacktwo align=center>
    <center><input type="submit" value="������鿴<�������������> ($regdisptime ������)" name="agreeb">����
    <input onclick=history.back(-1) type="reset" value=" �� �� ͬ �� ">
    </center>
    </td></form></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<SCRIPT language=javascript>
<!--
var secs = $regdisptime;
document.agree.agreeb.disabled=true;
for(i=1;i<=secs;i++) {
 window.setTimeout("update(" + i + ")", i * 1000);
}
function update(num) {
 if(num == secs) {
 document.agree.agreeb.value =" �� ͬ �� ";
 document.agree.agreeb.disabled=false;
 }
else {
 printnr = secs-num;
 document.agree.agreeb.value = "������鿴<�������������> (" + printnr +" ������)";
 }
}
//-->
</SCRIPT>

    ~;
}
print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output("$boardname - ע�����û�",\$output);
exit;

sub recommfunc {
    my $recommender = shift;
    $recommender =~ s/ /\_/g;
    $recommender =~ tr/A-Z/a-z/;
    $recommender =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    $namenumber = &getnamenumber($recommender);
    my $filetoopen = "${lbdir}$memdir/$namenumber/$recommender.cgi";
    if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
	open(REFILE,"+<$filetoopen");
	flock(REFILE, 2) if ($OS_USED eq "Unix");
	my $filedata = <REFILE>;
	chomp $filedata;
	($lmembername, $lpassword, $lmembertitle, $lmembercode, $lnumberofposts, $lemailaddress, $lshowemail, $lipaddress, $lhomepage, $loicqnumber, $licqnumber ,$llocation ,$linterests, $ljoineddate, $llastpostdate, $lsignature, $ltimedifference, $lprivateforums, $luseravatar, $luserflag, $luserxz, $lusersx, $lpersonalavatar, $lpersonalwidth, $lpersonalheight, $lrating, $llastgone, $lvisitno, $luseradd04, $luseradd02, $lmymoney, $lpostdel, $lsex, $leducation, $lmarry, $lwork, $lborn, $lchatlevel, $lchattime, $ljhmp, $ljhcount,$lebankdata,$lonlinetime,$luserquestion,$lawards,$ljifen,$luserface,$lsoccerdata,$luseradd5) = split(/\t/,$filedata);

		my ($numberofposts, $numberofreplys) = split(/\|/,$lnumberofposts);
		$numberofposts ||= "0";
		$numberofreplys ||= "0";
	      	$ljifen = $numberofposts * 2 + $numberofreplys - $lpostdel * 5 if ($ljifen eq "");

	$addtjjf = 0 if ($addtjjf eq "");
	$addtjhb = 0 if ($addtjhb eq "");
	if ($lmymoney eq "") { $lmymoney = $addtjhb; }
                   else { $lmymoney += $addtjhb; }

	$ljifen += $addtjjf;

	if (($lmembername ne "")&&($lpassword ne "")) {
	    seek(REFILE,0,0);
	    print REFILE "$lmembername\t$lpassword\t$lmembertitle\t$lmembercode\t$lnumberofposts\t$lemailaddress\t$lshowemail\t$lipaddress\t$lhomepage\t$loicqnumber\t$licqnumber\t$llocation\t$linterests\t$ljoineddate\t$llastpostdate\t$lsignature\t$ltimedifference\t$lprivateforums\t$luseravatar\t$luserflag\t$luserxz\t$lusersx\t$lpersonalavatar\t$lpersonalwidth\t$lpersonalheight\t$lrating\t$llastgone\t$lvisitno\t$luseradd04\t$luseradd02\t$lmymoney\t$lpostdel\t$lsex\t$leducation\t$lmarry\t$lwork\t$lborn\t$lchatlevel\t$lchattime\t$ljhmp\t$ljhcount\t$lebankdata\t$lonlinetime\t$luserquestion\t$lawards\t$ljifen\t$luserface\t$lsoccerdata\t$luseradd5\t";
	    close(REFILE);
   	} else {
	    close(REFILE);
	}
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
    }
}

sub checkverify {
	my $verifynum = $query->param('verifynum');
	my $sessionid = $query->param('sessionid');
	$sessionid =~ s/[^0-9a-f]//isg;
	return 1 if (length($sessionid) != 32 && $useverify eq "yes");

	###��ȡ��ʵ�� IP ��ַ
	my $ipaddress = $ENV{'REMOTE_ADDR'};
	my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
	$ipaddress = $trueipaddress if (($trueipaddress ne "") && ($trueipaddress ne "unknown"));
	$trueipaddress = $ENV{'HTTP_CLIENT_IP'};
	$ipaddress = $trueipaddress if (($trueipaddress ne "") && ($trueipaddress ne "unknown"));

	###��ȡ��ǰ���̵���֤�����֤�����ʱ�䡢�û�����
	my $filetoopen = "${lbdir}verifynum/$sessionid.cgi";
	open(FILE, $filetoopen);
	my $content = <FILE>;
	close(FILE);
	chomp($content);
	my ($trueverifynum, $verifytime, $savedipaddress) = split(/\t/, $content);
	my $currenttime = time;
	return ($verifynum ne $trueverifynum || $currenttime > $verifytime + 1200 + 120 || $ipaddress ne $savedipaddress) ? 1 : 0;
}
