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
$LBCGI::POST_MAX=20000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "lookemotes.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

    $query = new LBCGI;

	@params = $query->param;
	foreach $param(@params) {
		$theparam = $query->param($param);
        $theparam = &cleaninput("$theparam");
		$PARAM{$param} = $theparam;
	    }



$action      =  $PARAM{'action'};
$inforum     =  $PARAM{'forum'};
&error("���ļ�&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inforum) && ($inforum !~ /^[0-9]+$/));

$inmember            = $query -> param('member');
$inmembername        = $query -> param("membername");
$inpassword          = $query -> param("password");
$action              = &cleaninput("$action");
$inmember            = &cleaninput("$inmember");
$inmembername        = &cleaninput("$inmembername");
$inpassword          = &cleaninput("$inpassword");
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

    if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
    if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "����" ) { $inmembername = "����"; }
    else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
        }   

&mischeader("��̳EMOTE�б�");

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
    
            my %Mode = (             
            'style'               =>    \&styleform,                                
                       
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
               }
                
        


##################################################################################
sub styleform {
&mischeader("�鿴��̳ EMOTE �б�");
$filetoopen = "$lbdir" . "data/emote.cgi";
open (FILE, "$filetoopen");
flock (FILE, 1) if ($OS_USED eq "Unix");
$emote = <FILE>;
close (FILE);

$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table width=$tablewidth border=1 bordercolor=$tablebordercolor align=center cellpadding=5 cellspacing=0 style="border-collapse: collapse">
        <tr><td bgcolor=$forumcolorone $catbackpic colspan=2 align=center>ע��:�������е�"����"�����滻�ɷ����˵��û���.</td>
       ~;  
       @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		($toemote, $beemote) = split(/=/,$_);
		chomp $beemote;
	$output .= qq~
	<tr><td bgcolor=$forumcolorone>$toemote</td><td  bgcolor=$forumcolortwo>$beemote</td>	           
~;
}
}

$output .= qq~</tr></table><SCRIPT>valignend()</SCRIPT><br><br></body></html>~;
&output("$boardname - �鿴��̳ EMOTE �б�",\$output);
exit;

