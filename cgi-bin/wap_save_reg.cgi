#!/usr/bin/perl
#########################
# �ֻ���̳WAP��
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
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
$query = new LBCGI;
$LBCGI::POST_MAX = 2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "wap.lib.pl";
require "data/styles.cgi";
require "wap.pl";
$|++;
&waptitle;
$show.= qq~
<card  title="$boardname">~;
$inmembername   = $query -> param('n');
$inmembername= $uref->fromUTF8("gb2312",$inmembername);
$password     = $query -> param('p');
$password2     = $query -> param('p1');
$emailaddress     = $query -> param('email');
$emailaddress  = lc($emailaddress);
if (($inmembername eq "")||($emailaddress eq "")) {
        &errorout("�û�ע��&�������û������ʼ���ַ����Щ�Ǳ���ģ�");
    }
$ipaddress     = $ENV{'REMOTE_ADDR'};
    my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $trueipaddress = $ipaddress if ($trueipaddress eq "" || $trueipaddress eq "unknown" || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
    my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
    $trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 ne "unknown" && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
    $ipaddress = $trueipaddress;
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
		&errorout("�û�ע��&�Բ���������� Email �Ѿ���ע���û���<u>$1</u> ʹ����");
	    }
	}
	 &errorout("�û�ע��&�Բ�����������û�����$inmembername�������⣬�벻Ҫ���û����а���\@\#\$\%\^\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]�����ַ���") if ($inmembername =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/);
    if($inmembername =~ /_/)  { &errorout("�û�ע��&�벻Ҫ���û�����ʹ���»��ߣ�"); }
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
    $inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]//isg;
    $inmembername =~ s/\s*$//g;
    $inmembername =~ s/^\s*//g;
    &errorout("�û�ע��&�Բ�����������û���������") if ($inmembername =~ /^q(.+?)-/ig || $inmembername =~ /^q(.+?)q/ig);
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
    $bannedmember = "yes" if (($inmembername =~ /^m-/i)||($inmembername =~ /^s-/i)||($inmembername =~ /tr-/i)||($inmembername =~ /^y-/i)||($inmembername =~ /ע��/i)||($inmembername =~ /guest/i)||($inmembername =~ /qq-/i)||($inmembername =~ /qq/i)||($inmembername =~ /qw/i)||($inmembername =~ /q-/i)||($inmembername =~ /qx-/i)||($inmembername =~ /qw-/i)||($inmembername =~ /qr-/i)||($inmembername =~ /^ȫ��/i)||($inmembername =~ /register/i)||($inmembername =~ /��Ƹ��/i)||($inmembername =~ /����/i)||($inmembername =~ /����ϵͳѶϢ/i)||($inmembername =~ /leobbs/i)||($inmembername =~ /leoboard/i)||($inmembername =~ /�װ�/i)||($inmembername =~ /LB5000/i)||($inmembername =~ /ȫ�������Ա/i)||($inmembername =~ /����Ա/i)||($inmembername =~ /����/i)||($inmembername =~ /����Ϣ�㲥/i)||($inmembername =~ /��ʱ��ȱ/i)||($inmembername =~ /����������/i)||($inmembername =~ /����/i)||($inmembername =~ /̳��/i)||($inmembername =~ /nodisplay/i)||($inmembername =~ /^system/i)||($inmembername =~ /---/i)||($inmembername eq "admin")||($inmembername eq "root")||($inmembername eq "copy")||($inmembername =~ /^sub/)||($inmembername =~ /^exec/)||($inmembername =~ /\@ARGV/i)||($inmembername =~ /^require/)||($inmembername =~ /^rename/i)||($inmembername =~ /^dir/i)||($inmembername =~ /^print/i)||($inmembername =~ /^con/i)||($inmembername =~ /^nul/i)||($inmembername =~ /^aux/i)||($inmembername =~ /^com/i)||($inmembername =~ /^lpt/i));
    if ($bannedmember eq "yes") { &errorout("�û�ע��&������ע�ᣬ����д���û�����Email ��ǰ�� IP ��̳�����óɽ�ֹע�����û��ˣ������������ϵ̳���Ա�����"); }
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
    &errorout("�û�ע��&�Բ�������ע����û����Ѿ����������߱���ֹע�ᣬ�����һ���û�����") if ($noreg eq "yes");
    if($inmembername =~ /\t/) { &errorout("�û�ע��&�벻Ҫ���û�����ʹ�������ַ���"); }
    if($password =~ /[^a-zA-Z0-9]/)     { &errorout("�û�ע��&��̳����ֻ�����Сд��ĸ�����ֵ���ϣ���"); }
    if($password =~ /^lEO/)     { &errorout("�û�ע��&��̳���벻������ lEO ��ͷ�����������"); }
    $tempinmembername =$inmembername;
    $tempinmembername =~ s/ //g;
    $tempinmembername =~ s/��//g;
    if ($tempinmembername eq "")  { &errorout("�û�ע��&����û����е�����Ӵ����һ����"); }
    if ($inmembername =~ /^����/) { &errorout("�û�ע��&�벻Ҫ���û����Ŀ�ͷ��ʹ�ÿ���������"); }
    if (length($inmembername)>12) { &errorout("�û�ע��&�û���̫�����벻Ҫ����12���ַ���6�����֣���"); }
    if (length($inmembername)<2)  { &errorout("�û�ע��&�û���̫���ˣ��벻Ҫ���2���ַ���1�����֣���"); }
    if (length($newlocation)>12)  { &errorout("�û�ע��&���Ե����������벻Ҫ����12���ַ���6�����֣���"); }
    if (($inmembername =~ m/_/)||(!$inmembername)) { &errorout("�û�ע��&�û����к��зǷ��ַ���"); }
    if ($passwordverification eq "no"){
	if ($password ne $password2) { &errorout("�û�ע��&�Բ����������������̳���벻��ͬ��");   }
        if(length($password)<8)      { &errorout("�û�ע��&��̳����̫���ˣ����������̳������� 8 λ���ϣ�"); }
#       if ($password =~ /^[0-9]+$/) { &errorout("�û�ע��&��̳�����벻Ҫȫ��Ϊ���֣��������"); }
    }
    if ($inmembername eq $password) { &errorout("�û�ע��&�����û�������̳�������ó���ͬ��"); } 
    if($emailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,4})(\]?)$/) { &errorout("�û�ע��&�ʼ���ַ����"); }
    $emailaddress =~ s/[\ \a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
    &getmember("$inmembername","no");
    if ($userregistered ne "no") { &errorout("�û�ע��&���û��Ѿ����ڣ�����������һ���µ��û�����"); }
    $membercode    = "me";
    $memberfiletitle = $inmembername;
    $memberfiletitle =~ y/ /_/;
    $memberfiletitle =~ tr/A-Z/a-z/;
    $memberfiletitletemp = unpack("H*","$memberfiletitle");
    $joineddate=time;
    
    mkdir ("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
    chmod(0777,"${lbdir}$memdir/old");
    my $namenumber = &getnamenumber($memberfiletitle);
    $filetomake = "$lbdir" . "$memdir/$namenumber/$memberfiletitle.cgi";
    if (open(FILE, ">$filetomake")) {
        print FILE "$inmembername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$newlocation\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t0\t$lastgone\t1\t$addjy\t$meili\t$mymoney\t0\t$sex\t$education\t$marry\t$work\t$born\t\t\t\t\t\t\t$userquestion\t\t\t\t$soccerdata\t0\t";
        close(FILE);
    }
    $filetomake = "$lbdir" . "$memdir/old/$memberfiletitle.cgi";
    if (open(FILE, ">$filetomake")) {
        print FILE "$inmembername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$newlocation\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t0\t$lastgone\t1\t$addjy\t$meili\t$mymoney\t0\t$sex\t$education\t$marry\t$work\t$born\t\t\t\t\t\t\t$userquestion\t\t\t\t$soccerdata\t0\t";
        close(FILE);
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


    $filetomakeopen = "${lbdir}data/lbmember4.cgi";
    if (open (MEMFILE, ">>$filetomakeopen")) {
	print MEMFILE "$inmembername\t$ipaddress\t\n";
	close (MEMFILE);
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
    	FILE:my $x = &myrand(1000000000);
    $x = crypt($x, aun);
    $x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
    $x =~ s/[^\w\d]//g;
    $x = substr($x, 2, 9);  
    if(-e "${lbdir}wap/$x"){goto FILE;}
    my $xh2 = $ENV{'REMOTE_ADDR'};
    open(file,">${lbdir}wap/$x");
    print file "$inmembername,$xh2,$pre,$topicpre,$pre_index,$mastnum,$mastnum2";
    close(file);
    
    open(file,"${lbdir}wap/all.h");
    my @s=<file>;
    close(file);
    
    open(file,">${lbdir}wap/all.h");
    foreach(@s){
    	chomp;
    	my($n,$s)=split(/\,/,$_);
    	if($inmembername eq $n){
    		unlink "${lbdir}wap/$s";
    	}else{print file "$_\n";}
    }
    print file "$inmembername,$x\n";
    close(file);
$show.= qq~<p>
	ע��ɹ�����������IDΪ��$x,����IPΪ��$xh2���벻Ҫй©��������ID���κ��ˣ�����������ֻ��������ֻ�Ϊ˽�У��������������ҳ��ַ������ǩ(��ǩ��ַ��$boardurl/wap.cgi?lid=$x ������֮������½) �������벻Ҫ������ǩ��</p><p><a href="wap.cgi?lid=$x">����˴�������ҳ</a>
	</p>~;
&wapfoot;