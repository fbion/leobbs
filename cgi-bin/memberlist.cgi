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
require "data/boardinfo.cgi";
require "data/boardstats.cgi";
require "data/styles.cgi";
require "data/membertitles.cgi";
require "bbs.lib.pl";
require "data/cityinfo.cgi";

$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");
$query = new LBCGI;
&ipbanned; #��ɱһЩ ip

$topanzahl       = $hottopicmark;       #��ʾ����ǰ����������ʾ���¶��ٸ�������û���
$startseite      = "1";         	#Ĭ������:  1->������, 2->ǰN��, 3->�û���, 4->ע������
$memberproseite  = $maxthreads; 	#ÿҳ��ʾ�û���
if (! $inmembername) { $inmembername = cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = cookie("apasswordcookie");   }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "����" ) {
   $inmembername = "����";
}

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($infosopen == 2) {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("�鿴��Ա�б�&������Ȩ�鿴��Ա�б�") if ($inmembername eq "����");
    if ($userregistered eq "no") { &error("�鿴��Ա�б�&�㻹ûע���أ�"); }
    elsif ($inpassword ne $password) { &error("�鿴��Ա�б�&������������⣡"); }
    &error("�鿴��Ա�б�&��̳��Ա�б�ֻ��̳���Ͱ������Բ鿴��") if (($membercode ne "ad")&&($membercode ne 'amo')&&($membercode ne 'smo')&&($membercode ne 'cmo')&&($membercode ne "mo"));
}
elsif ($infosopen == 3) {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("�鿴��Ա�б�&������Ȩ�鿴��Ա�б�") if ($inmembername eq "����");
    if ($userregistered eq "no") { &error("�鿴��Ա�б�&�㻹ûע���أ�"); }
    elsif ($inpassword ne $password) { &error("�鿴��Ա�б�&������������⣡"); }
    &error("�鿴��Ա�б�&��̳��Ա�б�ֻ��̳�����Բ鿴��") if ($membercode ne "ad");
}
elsif ($infosopen == 1) {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("�鿴��Ա�б�&������Ȩ�鿴��Ա�б�") if ($inmembername eq "����");
    if ($userregistered eq "no") { &error("�鿴��Ա�б�&�㻹ûע���أ�"); }
    elsif ($inpassword ne $password) { &error("�鿴��Ա�б�&������������⣡"); }
}
else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
}
&title;
my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
&whosonline("$inmembername\t�û��б�\tboth\t�鿴�û��б�\t");
}
open (FILE, "${lbdir}data/lbmember.cgi");
sysread(FILE, $totlemembertemp,(stat(FILE))[7]);
close (FILE);
$totlemembertemp =~ s/\r//isg;
@file = split (/\n/, $totlemembertemp);
$totlemembertemp=@file;
$query = new LBCGI;
$L = $query -> param ("L");
if($L){
$pagel="&L=$L";
$LL=lc($L) if($L ne "*");
@CCfile=@file;@file=();
if($L eq "*"){
@file=grep(/^[^a-zA-Z]/,@CCfile);
}else{
@file=grep(/^[$L|$LL]/,@CCfile);
}
}
foreach $line (@file) {
@tmpuserdetail = split (/\t/, $line);
chomp @tmpuserdetail;
if ($tmpuserdetail[1] eq banned) {push (@banned, "$tmpuserdetail[0]"); }
push (@cgi, "$tmpuserdetail[0]");
$postundmember {"$tmpuserdetail[0]"} = $tmpuserdetail[2];
$datumundmember {"$tmpuserdetail[0]"} = $tmpuserdetail[3];
$moneymember {"$tmpuserdetail[0]"} = $tmpuserdetail[5];
$jhmember {"$tmpuserdetail[0]"} = $tmpuserdetail[6] if ($tmpuserdetail[6] > 0);
$jfmember {"$tmpuserdetail[0]"} = $tmpuserdetail[7] if ($tmpuserdetail[7] > 0);
}
@cgi=sort(@cgi);
@sortiert = reverse sort { $postundmember{$a} <=> $postundmember{$b} } keys(%postundmember);
@sortiert1 = sort { $datumundmember{$a} <=> $datumundmember{$b} } keys(%datumundmember);
@sortiert2 = reverse(@sortiert1);
@sortiert3 = reverse sort { $moneymember{$a} <=> $moneymember{$b} } keys(%moneymember);
@sortiert4 = reverse sort { $jhmember{$a} <=> $jhmember{$b} } keys(%jhmember);
@sortiert5 = reverse sort { $jfmember{$a} <=> $jfmember{$b} } keys(%jfmember);

$output .= qq~<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> �����������Բ鿴����վ����ע���Ա���б����ϸ��Ϣ�Լ������������</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> �� <a href="memberlist.cgi">�û��б�</a> �� �鿴�û��б�/����<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
~;
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
$a = $query -> param ("a");
$buffer=~s/\&L=(\S+?)//isg;
$searchmembername = $query -> param ("searchmember"); 
$searchmembername = &cleaninput($searchmembername);
$searchmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]//isg;
if ($searchmembername  ne "") { 
$a = 0; 
&searchmember} 

if ($a eq '' && $buffer eq '')
{$buffer = "a=$startseite";}
else
{($buffer = "$buffer") || ($buffer = "a=$a");}
if ($buffer eq 'a=1') {&Postsortiert}
elsif ($buffer eq 'a=2') {&Topten}
elsif ($buffer eq 'a=3') {&Namensortiert}
elsif ($buffer eq 'a=4') {&datum}
elsif ($buffer eq 'a=5') {&redatum}
elsif ($buffer eq 'a=6') {&banned}
elsif ($buffer eq 'a=7') {&moneyum}
elsif ($buffer eq 'a=8') {&jhum}
elsif ($buffer eq 'a=9') {&jfum}

sub jhum {
    $query = new LBCGI;
    $inpage = $query -> param ("page");
    if ($inpage eq "") {$inpage = 1;}
    $a = 8;
    $Listenname = "�Ծ���������";
    &Tabellenanfang(2);
    @memberarray = @sortiert4;
    &splitting;
    foreach $member (@sortiert4[$startmember ... $endmember]) {
        $member =~s/ /_/g;
        $member =~s/_/\_/g;
        $member =~ tr/A-Z/a-z/;
	    my $namenumber = &getnamenumber($member);
	    &checkmemfile($member,$namenumber);
            $usrfile = "${lbdir}$memdir/$namenumber/$member.cgi";
            $usrfile = "${lbdir}$memdir/old/$member.cgi" unless (-e $usrfile);
	    if (-e "$usrfile") {
		open(FILE, "$usrfile" );
            $memberdaten = <FILE>;
            close(FILE);
            &Listing(2);
	}
    }
    $output .= qq~</table>~;
}

sub moneyum {
    $query = new LBCGI;
    $inpage = $query -> param ("page");
    if ($inpage eq "") {$inpage = 1;}
    $a = 7;
    $Listenname = "�Խ�Ǯ����";
    &Tabellenanfang(1);
    @memberarray = @sortiert3;
    &splitting;
    foreach $member (@sortiert3[$startmember ... $endmember]) {
        $member =~s/ /_/g;
        $member =~s/_/\_/g;
        $member =~ tr/A-Z/a-z/;
	    my $namenumber = &getnamenumber($member);
	    &checkmemfile($member,$namenumber);
            $usrfile = "${lbdir}$memdir/$namenumber/$member.cgi";
            $usrfile = "${lbdir}$memdir/old/$member.cgi" unless (-e $usrfile);
	    if (-e "$usrfile") {
		open(FILE, "$usrfile" );
            $memberdaten = <FILE>;
            close(FILE);
            &Listing(1);
	}
    }
    $output .= qq~</table>~;
}

sub Namensortiert {
    $query = new LBCGI;
    $inpage = $query -> param ("page");
    if ($inpage eq "") { $inpage = 1; }
	$a = 3;
	@memberarray = @cgi;
	&splitting;
	$Listenname = "���û�������";
	&Tabellenanfang;
	foreach $member (@cgi[$startmember ... $endmember]) {
	    $member =~s/ /_/g;
            $member =~ tr/A-Z/a-z/;
            $member =~s/_/\_/g;
	    my $namenumber = &getnamenumber($member);
	    &checkmemfile($member,$namenumber);
            $usrfile = "${lbdir}$memdir/$namenumber/$member.cgi";
            $usrfile = "${lbdir}$memdir/old/$member.cgi" unless (-e $usrfile);
	    if (-e "$usrfile") {
		open(FILE, "$usrfile" );
		$memberdaten = <FILE>;
		close(FILE);
		&Listing;
	    }
	}
	$output .= qq~</table>~;
}
sub banned {
    $query = new LBCGI;
    $inpage = $query -> param ("page");
    if ($inpage eq "") { $inpage = 1; }
	$a = 6;
	@memberarray = @banned;
	&splitting;
	$Listenname = "����ֹ���Ե�";
	&Tabellenanfang;
	foreach $member (@banned[$startmember ... $endmember]) {
	    $member =~s/ /_/g;
	    $member =~s/_/\_/g;
            $member =~ tr/A-Z/a-z/;
	    my $namenumber = &getnamenumber($member);
	    &checkmemfile($member,$namenumber);
            $usrfile = "${lbdir}$memdir/$namenumber/$member.cgi";
            $usrfile = "${lbdir}$memdir/old/$member.cgi" unless (-e $usrfile);
	    if (-e "$usrfile") {
		open(FILE, "$usrfile" );
		$memberdaten = <FILE>;
		close(FILE);
		&Listing;
	    }
	}
	$output .= qq~</table>~;
}

sub searchmember { 
        $output .= qq~<SCRIPT>valigntop()</SCRIPT>
           <table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center> 
          <tr>     
          <td> 
          <table cellpadding=6 cellspacing=1 border=0 width=100%> 
          <tr> 
          <td bgcolor=$miscbacktwo align=center><font color=$fontcolormisc><b>��Ա $searchmembername ���ϲ����� , ���Ժ�</b></font></td></tr> 
          <tr> 
          <td bgcolor=$miscbackone><font color=$fontcolormisc> 
          ������� : 
          <ul> 
          <li><a href="memberlist.cgi?a=4">�����û��б�</a> 
          <li><a href="leobbs.cgi">������̳��ҳ</a> 
          </ul> 
          </tr> 
          </td> 
          </table></td></tr></table>
          <meta http-equiv="refresh" content="3; url=profile.cgi?action=show&member=~ . uri_escape($searchmembername) . qq~"> 
          ~; 
          } 


sub Postsortiert {
	$query = new LBCGI;
    $inpage = $query -> param ("page");
    if ($inpage eq "") { $inpage = 1; }
	$a = 1;
	@memberarray = @sortiert;
	&splitting;
	$Listenname = "�Է�����������";
	&Tabellenanfang;
	foreach $member (@sortiert[$startmember ... $endmember]) {
	    $member =~s/ /_/g;
	    $member =~s/_/\_/g;
            $member =~ tr/A-Z/a-z/;
	    my $namenumber = &getnamenumber($member);
	    &checkmemfile($member,$namenumber);
            $usrfile = "${lbdir}$memdir/$namenumber/$member.cgi";
            $usrfile = "${lbdir}$memdir/old/$member.cgi" unless (-e $usrfile);
	    if (-e "$usrfile") {
		open(FILE, "$usrfile" );
		$memberdaten = <FILE>;
		close(FILE);
		&Listing;
	    }
	}
	$output .= qq~</table>~;

}
sub Topten {
    $Listenname = "��������ǰ $topanzahl ��";
    &Tabellenanfang;
    @sortiert = splice(@sortiert,0,$topanzahl);
    foreach $member (@sortiert) {
        $member =~s/ /_/g;
        $member =~s/_/\_/g;
        $member =~ tr/A-Z/a-z/;
	    my $namenumber = &getnamenumber($member);
	    &checkmemfile($member,$namenumber);
            $usrfile = "${lbdir}$memdir/$namenumber/$member.cgi";
            $usrfile = "${lbdir}$memdir/old/$member.cgi" unless (-e $usrfile);
	    if (-e "$usrfile") {
		open(FILE, "$usrfile" );
        $memberdaten = <FILE>;
        close(FILE);
        &Listing;
    }
    }
    $output .= qq~</table>~;
}
sub datum {
    $query = new LBCGI;
    $inpage = $query -> param ("page");
    if ($inpage eq "") {$inpage = 1;}
    $a = 4;
    $Listenname = "��ע��ʱ������";
    &Tabellenanfang;
    @memberarray = @sortiert1;
    &splitting;
    foreach $member (@sortiert1[$startmember ... $endmember]) {
        $member =~s/ /_/g;
        $member =~s/_/\_/g;
        $member =~ tr/A-Z/a-z/;
	    my $namenumber = &getnamenumber($member);
	    &checkmemfile($member,$namenumber);
            $usrfile = "${lbdir}$memdir/$namenumber/$member.cgi";
            $usrfile = "${lbdir}$memdir/old/$member.cgi" unless (-e $usrfile);
	    if (-e "$usrfile") {
		open(FILE, "$usrfile" );
            $memberdaten = <FILE>;
            close(FILE);
            &Listing;
	}
    }
    $output .= qq~</table>~;
}
sub redatum {
    $Listenname = "���� $topanzahl ��ע���û�";
    &Tabellenanfang;
    @memberarray = @sortiert2;
    @sortiert2 = splice(@sortiert2,0,$topanzahl);
    foreach $member (@sortiert2) {
            $member =~s/ /_/g;
            $member =~s/_/\_/g;
            $member =~ tr/A-Z/a-z/;
	    my $namenumber = &getnamenumber($member);
	    &checkmemfile($member,$namenumber);
            $usrfile = "${lbdir}$memdir/$namenumber/$member.cgi";
            $usrfile = "${lbdir}$memdir/old/$member.cgi" unless (-e $usrfile);
	    if (-e "$usrfile") {
		open(FILE, "$usrfile" );
            $memberdaten = <FILE>;
            close(FILE);
            &Listing;
	}
    }
    $output .= qq~</table>~;
}
sub jfum {
   $query = new LBCGI;
   $inpage = $query -> param ("page");
   if ($inpage eq "") {$inpage = 1;}
   $a = 9;
   $Listenname = "�Ի�������";
   &Tabellenanfang(3);
   @memberarray = @sortiert5;
   &splitting;
   foreach $member (@sortiert5[$startmember ... $endmember]) {
       $member =~s/ /_/g;
       $member =~s/_/\_/g;
       $member =~ tr/A-Z/a-z/;
   my $namenumber = &getnamenumber($member);
   &checkmemfile($member,$namenumber);
       $usrfile = "${lbdir}$memdir/$namenumber/$member.cgi";
       $usrfile = "${lbdir}$memdir/old/$member.cgi" unless (-e $usrfile);
   if (-e "$usrfile") {
   open(FILE, "$usrfile" );
           $memberdaten = <FILE>;
           close(FILE);
           &Listing(3);
   }
   }
   $output .= qq~</table>~;
}

sub Tabellenanfang {
    $xiaoguo = shift;
    $totalpostandthreads = $totalposts + $totalthreads;
    $output .= qq~<center><p>
<SCRIPT>valigntop()</SCRIPT>
      <table width=$tablewidth cellpadding=0 cellspacing=0 border=0 bordercolor=$tablebordercolor>
    	<tr><td bgcolor=$titlecolor>
      	<table cellpadding=6 cellspacing=1 border=0 width=100%>
    	<tr bgcolor=$forumcolorone><td colspan=3 valign=top>&nbsp;>> <B>$Listenname</B> <<<BR><BR>
	&nbsp;��ע���û����� $totlemembertemp �� ������������ $totalpostandthreads ƪ</font></td>
	<td colspan=7 align=right><form method=get action=memberlist.cgi>
        <select name=a>
            <option value=2>��������ǰ $topanzahl ��</option>
            <option value=5>���� $topanzahl ��ע���û�</option>
            <option value=3>���û�������</option>
            <option value=1>�Է�����������</option>
            <option value=4>��ע��ʱ������</option>
            <option value=6>����ֹ���Ե�</option>
            <option value=7>�ֽ�����</option>
            <option value=8>����������</option>
            <option value=9>��������</option>
        </select>
	<input type=submit value="�� ��"></form><form method=get action=memberlist.cgi>
	�û��� <input type=text name="searchmember">		<input type=submit value="�� ��">
	</td></form></tr>
~;
    @L=("*","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","All");
    $output.=qq~<tr bgcolor=$forumcolorone><td colspan="10"><table cellpadding=1 cellspacing=1 border=0 width=100%><tr bgcolor=$forumcolorone>~;
    for($i=0;$i<28;$i++){
    	if(($L eq lc($L[$i]))||(($L eq "")&&($L[$i] eq "All"))){
    $output.=qq~<td width="3%" align="center" bgcolor="$forumcolorone">[$L[$i]]</td>~;
    	}elsif($L[$i] eq "All"){
    $output.=qq~<td width="3%" align="center" bgcolor="$forumcolortwo"><a href="memberlist.cgi?a=$a" target="_self">$L[$i]</a></td>~;
    	}else{
    $output.=qq~<td width="3%" align="center" bgcolor="$forumcolortwo"><a href="memberlist.cgi?a=$a&L=$L[$i]" target="_self">$L[$i]</a></td>~;
    	}
    }
    $output.=qq~</tr></table></td></tr>~;
    if ($xiaoguo eq "") {
        $output.=qq~<tr bgcolor=$titlecolor><td align=center $catbackpic><b>�û���</b></td><td align=center $catbackpic><b>Email</b></td><td align=center $catbackpic><b>ICQ</b></td><td align=center $catbackpic><b>OICQ</b></td><td align=center $catbackpic><b>��ҳ</b></td><td align=center $catbackpic><b>����Ϣ</td><td align=center $catbackpic><b>�����</td><td align=center $catbackpic><b>ע��ʱ��</b></td><td align=center $catbackpic><b>�ȼ�״̬</b></td><td align=center $catbackpic><b>��������</b></td></font></tr>~;
    }
    elsif ($xiaoguo eq "1") {
        $output.=qq~<tr bgcolor=$titlecolor><td align=center $catbackpic><b>�û���</b></td><td align=center $catbackpic><b>Email</b></td><td align=center $catbackpic><b>ICQ</b></td><td align=center $catbackpic><b>OICQ</b></td><td align=center $catbackpic><b>��ҳ</b></td><td align=center $catbackpic><b>����Ϣ</td><td align=center $catbackpic><b>�����</td><td align=center $catbackpic><b>ע��ʱ��</b></td><td align=center $catbackpic><b>�ȼ�״̬</b></td><td align=center $catbackpic><b>�ֽ���</b></td></font></tr>~;
    }
    elsif ($xiaoguo eq "2") {
        $output.=qq~<tr bgcolor=$titlecolor><td align=center $catbackpic><b>�û���</b></td><td align=center $catbackpic><b>Email</b></td><td align=center $catbackpic><b>ICQ</b></td><td align=center $catbackpic><b>OICQ</b></td><td align=center $catbackpic><b>��ҳ</b></td><td align=center $catbackpic><b>����Ϣ</td><td align=center $catbackpic><b>�����</td><td align=center $catbackpic><b>ע��ʱ��</b></td><td align=center $catbackpic><b>�ȼ�״̬</b></td><td align=center $catbackpic><b>��������</b></td></font></tr>~;
    }
    elsif ($xiaoguo eq "3") {
       $output.=qq~<tr bgcolor=$titlecolor><td align=center $catbackpic><b>�û���</b></td><td align=center $catbackpic><b>Email</b></td><td align=center $catbackpic><b>ICQ</b></td><td align=center $catbackpic><b>OICQ</b></td><td align=center $catbackpic><b>��ҳ</b></td><td align=center $catbackpic><b>����Ϣ</td><td align=center $catbackpic><b>�����</td><td align=center $catbackpic><b>ע��ʱ��</b></td><td align=center $catbackpic><b>�ȼ�״̬</b></td><td align=center $catbackpic><b>������</b></td></font></tr>~;
   }

}

sub Listing {
    $xiaoguo = shift;
    @memberdaten = split(/\t/,$memberdaten);
    $name        = $memberdaten[0];
    $status      = $memberdaten[2];
    $anzahl      = $memberdaten[4];
    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
    $postdel = $memberdaten[31];
    $jifen      = $memberdaten[45];

	if ($jifen eq "") {
		$jifen = $anzahl1 * $ttojf + $anzahl2 * $rtojf - $postdel * $deltojf;
  }

    $anzahl = $anzahl1 + $anzahl2;
    $email       = $memberdaten[5];
    $home        = $memberdaten[8];
    $oicqnumber     = $memberdaten[9];
    $icq         = $memberdaten[10];
    $date        = $memberdaten[13] + ($memberdaten[16] * 3600) + ($timezone * 3600);
    $rang        = $memberdaten[3];
    $emailstatus = $memberdaten[6];
    $emailstatus = "no" if ($dispmememail eq "no");
    next if ($name eq "");

    $jhcount = $memberdaten[40];
    $mymoney = $memberdaten[30];
    $visitno = $memberdaten[27];

    ($postdate, $posturl, $posttopic) = split(/\%%%/, $memberdaten[14]);
    if (($postdate ne "û�з����")&&($postdate ne "")) {
        $postdate = $postdate + ($userdetail[16] * 3600) + ($timezone * 3600);
        $lastpostdate = &longdate ("$postdate");
        $lastposttime = &longdate ("$postdate");
        $posttopic =~ s/^����������//;
	$lastpostdetails = qq~<a href=$posturl><img border=0 src=$imagesurl/images/openfold.gif alt=$posttopic></a>~;
    }
    else{$lastpostdetails = "û��";}
    $date = &longdate($date + ($memberdaten[16]*3600) + ($timezone*3600));
    $postundmember {"$name"} = $anzahl;
    if (($icq) && ($icq =~ /[0-9]/)){
	$icqgraphic = qq~<a href="javascript:openScript('misc.cgi?action=icq&UIN=$icq',450,300)"><img src=$imagesurl/images/icq.gif border=0 width=16 height=16></a>~;
    }
    else{$icqgraphic = "û��";}

    if (($home eq "http://") || ($home eq "")) { $home = "û��"; }
    else{
	$home = "<a href=$home target=_blank><img border=0 src=$imagesurl/images/homepage.gif></a>"
    }

    if ($oicqnumber) { $oicqgraphic = qq~<a href=http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$oicqnumber target=_blank><img src=$imagesurl/images/oicq.gif alt="�鿴 OICQ:$oicqnumber ������" border=0 width=16 height=16></a>~; }
    else{$oicqgraphic = "û��";}
    $email = &encodeemail($email);
    if ($email eq "" || $emailstatus eq "no" || $emailstatus eq "msn" || $emailstatus eq "popo"){
	$email = "û��" if ($email eq "");
	$email = "����" if ($emailstatus eq "no");
	$email = "<a href=mailto:$email><img border=0 src=$imagesurl/images/msn.gif></a>" if ($emailstatus eq "msn");
	$email = "<a href=mailto:$email><img border=0 src=$imagesurl/images/popo.gif></a>" if ($emailstatus eq "popo");
    }
    else {$email = "<a href=mailto:$email><img border=0 src=$imagesurl/images/email.gif></a>" }
        if ($jifen >= $mpostmarkmax)   { $mtitle = $mtitlemax; $membergraphic = $mgraphicmax; }
        elsif ($jifen >= $mpostmark19) { $mtitle = $mtitle19;  $membergraphic = $mgraphic19; }
        elsif ($jifen >= $mpostmark18) { $mtitle = $mtitle18;  $membergraphic = $mgraphic18; }
        elsif ($jifen >= $mpostmark17) { $mtitle = $mtitle17;  $membergraphic = $mgraphic17; }
        elsif ($jifen >= $mpostmark16) { $mtitle = $mtitle16;  $membergraphic = $mgraphic16; }
        elsif ($jifen >= $mpostmark15) { $mtitle = $mtitle15;  $membergraphic = $mgraphic15; }
        elsif ($jifen >= $mpostmark14) { $mtitle = $mtitle14;  $membergraphic = $mgraphic14; }
        elsif ($jifen >= $mpostmark13) { $mtitle = $mtitle13;  $membergraphic = $mgraphic13; }
        elsif ($jifen >= $mpostmark12) { $mtitle = $mtitle12;  $membergraphic = $mgraphic12; }
        elsif ($jifen >= $mpostmark11) { $mtitle = $mtitle11;  $membergraphic = $mgraphic11; }
        elsif ($jifen >= $mpostmark10) { $mtitle = $mtitle10;  $membergraphic = $mgraphic10; }
        elsif ($jifen >= $mpostmark9)  { $mtitle = $mtitle9;   $membergraphic = $mgraphic9; }
        elsif ($jifen >= $mpostmark8)  { $mtitle = $mtitle8;   $membergraphic = $mgraphic8; }
        elsif ($jifen >= $mpostmark7)  { $mtitle = $mtitle7;   $membergraphic = $mgraphic7; }
        elsif ($jifen >= $mpostmark6)  { $mtitle = $mtitle6;   $membergraphic = $mgraphic6; }
        elsif ($jifen >= $mpostmark5)  { $mtitle = $mtitle5;   $membergraphic = $mgraphic5; }
        elsif ($jifen >= $mpostmark4)  { $mtitle = $mtitle4;   $membergraphic = $mgraphic4; }
        elsif ($jifen >= $mpostmark3)  { $mtitle = $mtitle3;   $membergraphic = $mgraphic3; }
        elsif ($jifen >= $mpostmark2)  { $mtitle = $mtitle2;   $membergraphic = $mgraphic2; }
        elsif ($jifen >= $mpostmark1)  { $mtitle = $mtitle1;   $membergraphic = $mgraphic1; }
        else { $mtitle = $mtitle0; $mgraphic0 ="none.gif" if ($mgraphic0 eq ""); $membergraphic = $mgraphic0; }
        if($rang eq "ad") {
        	$mtitle = $adtitle if ($adtitle ne "");
        	$membergraphic = "$admingraphic" if ($admingraphic ne "");
        }
        elsif ($rang eq "mo") {
        	$mtitle = $motitle if ($motitle ne "");
        	$membergraphic = "$modgraphic" if ($modgraphic ne "");
        }
        elsif ($rang eq "amo") {
        	$mtitle = $amotitle if ($amotitle ne "");
        	$membergraphic = "$amodgraphic" if ($amodgraphic ne "");
        }
        elsif ($rang eq "cmo") {
        	$mtitle = $cmotitle if ($cmotitle ne "");
        	$membergraphic = "$cmodgraphic" if ($cmodgraphic ne "");
        }
        elsif ($rang eq "smo") {
        	$mtitle = $smotitle if ($smotitle ne "");
        	$membergraphic = "$smodgraphic" if ($smodgraphic ne "");
        }
        elsif ($rang eq "banned") {
        	$mtitle = "�ѱ���ֹ����";
        	$membergraphic = "";
        }
        elsif ($rang eq "masked") {
        	$mtitle = "�����ѱ�����";
        	$membergraphic = "";
        }

        if ($membergraphic) { $membergraphic = "<img src=$imagesurl/images/$membergraphic border=0>"; }
	$memberfilename = $name;
	$memberfilename =~ y/ /_/;
	$memberfilename =~ tr/A-Z/a-z/;
	$message = "<a href=javascript:openScript('messanger.cgi?action=new&touser=$memberfilename',600,400)><img src=$imagesurl/images/message.gif border=0></a>";
	if ($xiaoguo eq "1") {
	    $anzahl = $anzahl1 * $addmoney + $anzahl2 * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	}
	elsif ($xiaoguo eq "2") {
	    $anzahl = $jhcount;
	}
	elsif ($xiaoguo eq "3") {
	   $anzahl = $jifen;
	}
	$output .= qq~<tr bgcolor=$forumcolortwo><td>&nbsp;<a href=profile.cgi?action=show&member=~ . uri_escape($memberfilename) . qq~>$name</a></td><td align=center $memberdaten[7]>$email</td><td align=center>$icqgraphic</td><td align=center>$oicqgraphic</td><td align=center>$home</td><td align=center>$message</td><td align=center>$lastpostdetails</td><td align=center>$date</td><td align=center>$mtitle<br>$membergraphic</td><td align=center>$anzahl</td></tr>~;

}
sub splitting {
	$prrepages= 12;
    $totalpages = @memberarray / $memberproseite;
    ($pagenumbers, $decimal) = split (/\./, $totalpages);
    if ($decimal > 0) {$pagenumbers++;}

    $currentpage = int(($inpage-1) / $prrepages) + 1;

    $pagelinks =qq~���������� $pagenumbers ҳ��~;
#$mypage-- if ($mypage eq $inpage); 
    if ($currentpage > 1){ $mypage = ($currentpage-1)*$prrepages; $pagelinks .= qq~[<a href=memberlist.cgi?a=$a&page=$mypage$pagel>��һ��</a>] ~;}

    for ($page=$mypage+1;$page<$mypage+$prrepages+1;$page++){
        if ($page<=$pagenumbers){
          if ($inpage ne $page) {$pagelinks .= qq~[<a href=memberlist.cgi?a=$a&page=$page$pagel>��$pageҳ</a>] ~; }
	    else{$pagelinks .= qq~[<B>��$pageҳ</B>] ~;}
        }
    }
    $nextpage=$currentpage*$prrepages+1;
    if ($pagenumbers> $nextpage){$pagelinks .= qq~[<a href=memberlist.cgi?a=$a&page=$nextpage$pagel>��һ��</a>] ~;}
    if ($totalpages <= 1) {$pagelinks = qq~~;}

    $startmember = ($inpage - 1) * $memberproseite;
    $endmember = $startmember + $memberproseite - 1;
    if ($endmember > (@memberarray-1)) {$endmember = @memberarray - 1;}

}
$output .= qq~</td></tr></table><SCRIPT>valignend()</SCRIPT><p>~;
$output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr>
<td><table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr bgcolor=$menubackground>
<td align=center><font face=���� color=$fontcolormisc>$pagelinks</font></td>
</tr>
</table></td>
</tr>
</table><SCRIPT>valignend()</SCRIPT></center>~ if ($pagelinks ne "");
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output("$boardname - �û��б�",\$output);
exit;
