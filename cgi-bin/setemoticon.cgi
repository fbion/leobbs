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
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "setemoticon.cgi";
$query = new LBCGI;

$addme=$query->param('addme');

for('action','emoticonid','emoticonname','emoticonurl','emoticoninfo') {
    my $theparam = $query->param($_);
    $theparam = &cleaninput("$theparam");
    ${$_} = $theparam;
}
$checkaction  =  ($query->param('checkaction') eq "yes") ? "yes" : "no";

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword   =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

my %Mode = (	'createnew'  => \&createnew,
		'processnew' => \&createaction,
		'edit'       => \&editemot,
		'editaction' => \&editaction,
		'delete'     => \&deleteaction
	   );

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;
&getmember("$inmembername","no");
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
    print qq~
    <tr><td bgcolor="#2159C9" colspan=2><font color=#FFFFFF>
    <b>��ӭ������̳�������� / ����ת�����ù�����</b>
    </td></tr>~;
    if ($Mode{$action}) {
        $Mode{$action}->();
    } else {
        &emoticonlist;
    }
    print qq~</table></td></tr></table>~;
} else {
    &adminlogin;
}
    
sub emoticonlist {
    print qq~<tr><td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>ע������</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=2 align=center>
    ���������棬��������Ŀǰ���е� EMOT ͼƬ������������һ���µ� EMOT ͼƬ��Ҳ���Ա༭��ɾ��Ŀǰ���ڵ� EMOT ͼƬ��<p>
    <table width=80% align=center>
    <tr><td>
    <li><u>ͼƬ����</u> Ϊ����ʹ�õ�ͼƬ,�ѻ���������ɿ���ͼƬ���ļ����ơ�<p>
    <li><u>ת������</u> Ϊת��ʱʹ�õĴ���,�����������������������ʾ��ص� EMOT ͼƬ��<p>
    <li><u>��������</u> Ϊת����ͼƬ������ע�⡣<p>
    </td></tr>
    </table>
    </td></tr>
~;

    $filetoopen = "${lbdir}data/emoticons.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @emoticons = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    print qq~
    <tr><td bgcolor=#FFFFFF align=center colspan=2><table width=90% cellspacing="0" cellpadding="2">
    <tr><td align="center" colspan="4" bgcolor="#EEEEEE">|| <a href="$thisprog?action=createnew">������ EMOT ͼƬ</a> ||</td></tr>
    <tr><td align="center" bgcolor=$catback><BR><b style="color:blue">ͼƬ����</b></td><td align="center" width="20%" bgcolor=$catback><b style="color:blue">ת������</b></td><td align="center" width="20%" bgcolor=$catback><b style="color:blue">��������</b></td><td align="center" width="30%" bgcolor=$catback><b style="color:blue">��ز���</b></td></tr>
~;

    $emoticonnum = 0;
    foreach $emoticon (@emoticons) {
    	chomp $emoticon;
    	next if ($emoticon eq "");
	($emoticonname, $emoticonurl, $emoticoninfo) = split(/\t/,$emoticon);
	$emoticonurl=~s/\\//g;
	$emoticonnum++;
	print qq~<tr><td align="left">����<img src="$imagesurl/emoticons/$emoticonname" align="absmiddle" border=0>$emoticonname</td><td align="right"><input type="text" value="$emoticonurl" maxlength="10" style="width:100%"></td><td align="right"><input type="text" value="$emoticoninfo"  style="width:100%"></td><td align="center"><a href="$thisprog?action=edit&emoticonid=$emoticonnum">[�༭]</a> <a href="$thisprog?action=delete&emoticonid=$emoticonnum">[ɾ��]</a></td></tr>\n~;
    }
    print qq~<tr><td align="center" colspan="4" bgcolor="#EEEEEE">���� EMOT ͼƬ $emoticonnum �� </td></tr></table>~;
}

sub createnew {
    opendir (DIR, "${imagesdir}emoticons");
    @emoticon = readdir(DIR);
    closedir (DIR);
    chomp @emoticon;
    @emoticon = grep(/.[gif|jpg|png|bmp]$/,@emoticon);
    @emoticon = sort @emoticon;
    $emoticon = join("\t",@emoticon);
    $emoticon=~s/^\t//;
    $emoticon="<option>".$emoticon."</option>";
    $emoticon=~s/\t/<\/option><option>/isg;
    $emoticon=~s/<option><\/option>//isg;
    print qq~
<script>
function selectimg(oj,fm) {
    img =oj.options[oj.selectedIndex].text;
    fm.emoticonname.value=img;
    document.emotimg.src = "$imagesurl/emoticons/"+img;
}
</script>
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="processnew">    
    <tr><td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b> EMOT ͼƬ����</b><br>�������� EMOT ͼƬ���ļ�����<BR></font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="emoticonname" value=""><select name="image" onChange="selectimg(this,this.form)">$emoticon</select><img name=emotimg src="$imagesurl/images/none.gif" align="absmiddle" border=0></td>
    </tr>
    <tr><td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>����ת������</b><br>�������� EMOT ͼƬ��ת������<BR>(ֻ�ް���Ӣ��,���ֺͷ���)</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=40 name="emoticonurl" value="" maxlength="10"></td>
    </tr>
    <tr><td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font  color=#333333><b> EMOT ͼƬ����</b><br>������ EMOT ͼƬ������</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=40 name="emoticoninfo"></td>
    </tr>
    <tr><td bgcolor=#FFFFFF valign=middle align=center colspan=2>
    <input type=submit value="�� ��"></form>
    </td>
    </tr>
    <tr><td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
}

sub editemot {
    $filetoopen = "$lbdir" . "data/emoticons.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE,"$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @emoticons = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    ($emoticonname,$emoticonurl,$emoticoninfo) = split(/\t/,$emoticons[$emoticonid-1]);   
    $emoticonurl=~s/\\//g;
    opendir (DIR, "${imagesdir}emoticons");
    @emoticon = readdir(DIR);
    closedir (DIR);
    chomp @emoticon;
    @emoticon = grep(/.[gif|jpg|png|bmp]$/,@emoticon);
    @emoticon = sort @emoticon;
    $emoticon = join("\t",@emoticon);
    $emoticon=~s/^\t//;
    $emoticon="<option>".$emoticon."</option>";
    $emoticon=~s/\t/<\/option><option>/isg;
    $emoticon=~s/<option><\/option>//isg;
    $emoticon=~s/<option>$emoticonname<\/option>/<option selected>$emoticonname<\/option>/;
    print qq~
<script>
function selectimg(oj,fm){
	img =oj.options[oj.selectedIndex].text;
	fm.emoticonname.value=img;
	document.emotimg.src = "$imagesurl/emoticons/"+img;
}
</script>
    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="editaction">
    <input type=hidden name="emoticonid" value="$emoticonid">
    <input type=hidden name="emoticon" value="$emoticonname">
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b> EMOT ͼƬ����</b><br>�������µ� EMOT ͼƬ�ļ�����<BR></font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=20 name="emoticonname" value="$emoticonname"><select name="image" onChange="selectimg(this,this.form)">$emoticon</select><img name=emotimg src="$imagesurl/emoticons/$emoticonname" align="absmiddle" border=0></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font color=#333333><b>����ת������</b><br>�������µ� EMOT ͼƬת������<BR>(ֻ�ް���Ӣ��,���ֺͷ���)</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=40 name="emoticonurl" value="$emoticonurl" maxlength="10"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left width=40%>
    <font  color=#333333><b> EMOT ͼƬ����</b><br>�������µ� EMOT ͼƬ����</font></td>
    <td bgcolor=#FFFFFF valign=middle align=left>
    <input type=text size=40 name="emoticoninfo" value="$emoticoninfo"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
    <input type=submit value="�� ��"></form>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
}

sub createaction {   
    if ($emoticonname eq "" || $emoticonurl eq ""){&errorout(" EMOT ͼƬ���Ƽ�����ת�����벻��Ϊ�գ�"); return;}
    $emoticonurl=&decode($emoticonurl);
    if ($errorout == 1){&errorout("����ת�����벻����ʹ��Ӣ��,���ֺͷ���������ִ���");return;}
    $filetoopen = "$lbdir" . "data/emoticons.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @emoticons = <FILE>;
    close(FILE);

    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach $emoticon (@emoticons) {
    next if ($emoticon eq "");
	chomp $emoticon;
    print FILE "$emoticon\n";
    }
    print FILE "$emoticonname\t$emoticonurl\t$emoticoninfo\t\n";
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    &doemote;
    
    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#333333><b>���ӽ��</b><p>
    <li>�� EMOT ͼƬ <B>$emoticonname</b> �Ѿ�������
    <br><BR><a href=$thisprog?action=createnew>�������� EMOT ͼƬ</a>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
}
sub editaction {   
    if ($emoticonname eq "" || $emoticonurl eq ""){&errorout(" EMOT ͼƬ���Ƽ�����ת�����벻��Ϊ�գ�"); return;}
    $emoticonurl=&decode($emoticonurl);
    if ($errorout == 1){&errorout("����ת�����벻����ʹ��Ӣ��,���ֺͷ���������ִ���");return;}
    $filetoopen = "$lbdir" . "data/emoticons.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @emoticons = <FILE>;
    close(FILE);
    open(FILE,">$filetoopen");
    flock(FILE,2) if ($OS_USED eq "Unix");
    $emoticonnum = 0;
    foreach $emoticon (@emoticons) {
        next if ($emoticon eq "");
	chomp $emoticon;
        $emoticonnum ++;
	if ($emoticonid eq $emoticonnum) {
	    ($oldemoticonname,undef,undef)=split(/\t/,$emoticon);
	    print FILE "$emoticonname\t$emoticonurl\t$emoticoninfo\t\n";
	} else {
	    print FILE "$emoticon\n";
	}
    }
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    &doemote;

    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#333333><b>�༭���</b><p>
    <li> EMOT ͼƬ <B>$oldemoticonname</b> �Ѿ����£�
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
}

sub deleteaction {
    if($checkaction ne "yes") {
        print qq~<tr>
    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
    <font color=#990000><b>���棡��</b>
    </td></tr>
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
    <font color=#333333>�����ȷ��Ҫɾ�� EMOT ͼƬ $emoticon����ô������������<p>
    >> <a href="$thisprog?action=delete&checkaction=yes&emoticonid=$emoticonid">ɾ�� EMOT ͼƬ</a> <<
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
        return;
    }
    $filetoopen = "$lbdir" . "data/emoticons.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE,"$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @emoticons = <FILE>;
    close(FILE);

    open(FILE,">$filetoopen");
    flock(FILE,2) if ($OS_USED eq "Unix");
    $emoticonnum = 0;
    foreach $emoticon (@emoticons) {
        next if ($emoticon eq "");
	chomp $emoticon;
        $emoticonnum ++;
	if ($emoticonid eq $emoticonnum) {
	    ($oldemoticonname,undef,undef)=split(/\t/,$emoticon);
	} else {
	    print FILE "$emoticon\n";
	}
    }
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    &doemote;

    print qq~
    <tr>
    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
    <fon color=#333333><b>ɾ�����</b><p>
    <li> EMOT ͼƬ <B>$oldemoticonname</B> �ѱ�ɾ����
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td>
    </tr>
    ~;
}

sub errorout{
    my($errortype,$errormsg)=@_;
    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>$errortype</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF align="center" colspan=2><font color=red>$errormsg</font></td></tr>
    <tr><td bgcolor=#FFFFFF align="center" height="100" valign="bottom" colspan=2>-- <a href="$thisprog">����</a> --</td></tr>
    ~;
}

sub decode{
    my $str=shift;
    my @strarr = split(//,$str);
    chomp @strarr;
    my $strlen = length($str);
    $str="";
    for ($i = 0; $i < $strlen; $i++) {
    	my $binchar = vec($str, $i, 8);
    	if($binchar > 126){
    	    $errorout=1;last;
    	}
	if ($strarr[$i] =~/[^a-zA-Z0-9]/) {
	    $str.="\\$strarr[$i]";
	} else {
	    $str.=$strarr[$i];
	}
    }
    return $str;
}
sub doemote {
    $subsmilecode = '';
    open(FILE, "${lbdir}data/emoticons.cgi");
    my @emoticonsdata = <FILE>;
    close (FILE);
    foreach (@emoticonsdata) {
	chomp;
	next if ($_ eq "");
	my ($emoticonname, $emoticonurl, $emoticoninfo) = split(/\t/, $_);
	$subsmilecode .= "\$\$post =~ s/(^|\\s|\\>|\\;)$emoticonurl(\\s|\$|\\<)/\$1<img src=\${imagesurl}\\/emoticons\\/$emoticonname alt=\"$emoticoninfo\">\$2/isg;\n";
    }

    open(FILE, ">${lbdir}data/emoticons.pl");
    print FILE $subsmilecode;
    close(FILE);
}
