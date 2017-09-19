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
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "face/config.pl";
$|++;
$query = new LBCGI;
$thisprog = "editface.cgi";

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
}

$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));

if ($inmembername eq "" || $inmembername eq "����" ) {
    &error("���ܽ��� $plugname &��Ŀǰ������Ƿÿͣ����ȵ�½!");
    exit;
} else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("��ͨ����&���û����������ڣ�") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie  = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie  = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("��ͨ����&�������û���������������µ�¼��");
     }
}

$tempmembername = $membername;
$tempmembername =~ s/ /\_/g;
$tempmembername =~ tr/A-Z/a-z/;
$admin_user =~ s/ /\_/g;
$admin_user =~ tr/A-Z/a-z/;

&error("$plugname �༭����&ֻ����̳̳����������Ա���ܽ��������") if (($membercode ne "ad")&&($admin_user ne "$tempmembername"));

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print qq~
<html>
<head>
<title>$plugname - �༭����</title>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<style>
A:visited{TEXT-DECORATION: none}
A:active{TEXT-DECORATION: none}
A:hover{TEXT-DECORATION: underline overline}
A:link{text-decoration: none;}
.t{LINE-HEIGHT: 1.4}
TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: ����; FONT-SIZE: 9pt} 
INPUT{BORDER-TOP-WIDTH: 1px; PADDING-RIGHT: 1px; PADDING-LEFT: 1px; BORDER-LEFT-WIDTH: 1px; FONT-SIZE: 9pt; BORDER-LEFT-COLOR: #cccccc; BORDER-BOTTOM-WIDTH: 1px; BORDER-BOTTOM-COLOR: #cccccc; PADDING-BOTTOM: 1px; BORDER-TOP-COLOR: #cccccc; PADDING-TOP: 1px; HEIGHT: 18px; BORDER-RIGHT-WIDTH: 1px; BORDER-RIGHT-COLOR: #cccccc}
textarea, select {border-width: 1; border-color: #000000; background-color: #efefef; font-family: ����; font-size: 9pt; font-style: bold;}
</style>
</head>
<body bgcolor="#ffffff" topmargin=0 leftmargin=0>
<table width=100% cellpadding=6 cellspacing=0 style="border:1 solid #555555;">~;
$action = $query -> param('action');

my %Mode = ('edit_sp' => \&edit_sp,'editok' => \&editok,'del_sp' => \&del_sp);

if ($Mode{$action})
{$Mode{$action} -> ();}
else{&error("$plugname&�ϴ󣬱��Һ��ҵĳ���ѽ��");}

sub edit_sp
{
    $num       = $query -> param('num');	# ��Ʒ����ļ�
    $id        = $query -> param('id');		# ��Ʒ��ID��
$num =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$id =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

    $/="";
    my $filetoopen = "$lbdir" . "face/wpdata/$num.pl";
    open(FILE,"$filetoopen");
    my $sort=<FILE>;
    close(FILE);
    $/="\n";

    $numid = $num;

    &errorout("1","�Ҳ���ָ������Ʒ��") if($sort !~ /$id\t(.*)/);	# �ҵ�ָ������ƷID

    ($sp_name,$sp_money,$sp_description,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$x,$x)=split(/\t/,$1);

    print qq~<tr><td bgcolor="#333333" height="20"><font color=#FFFFFF><b>����������� / �༭��Ʒ</b></td></tr></table>~;

    if($sp_suit eq 'Y')
    {
	@taoinfo=split(/\_/,$sp_suitid);
	$numid = @taoinfo[0];
    }
    $tempoutput = "<input type=radio name=newfit value=\"m\"> �� <input type=radio name=newfit value=\"f\"> Ů <input type=radio name=newfit value=\"t\"> ͨ��";
    $tempoutput =~ s/value=\"$sp_fitherd\"/value=\"$sp_fitherd\" checked/;

    opendir (DIR, "${imagesdir}face/$numid");
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
document.FORM.newgraphic.value=FORM.image.value;
document.dtdemo.src = "$imagesurl/face/$numid/"+FORM.image.value;}
function select1(){
document.FORM.newsxgraphic.value=FORM.image2.value;
document.xtdemo.src = "$imagesurl/face/$numid/"+FORM.image2.value;}
</script>
<table cellPadding=0 cellSpacing=2 width=100%>
<form action="$thisprog" method="post" name=FORM>
<input type=hidden name="action" value="editok">
<input type=hidden name="class" value="$num">
<input type=hidden name="id" value="$id">
  <TR bgColor=#eeeeee align=center><TD width=84>Сͼ</TD><TD width=140>��ͼ</TD><TD>��Ʒ����</TD></TR>
  <TR bgColor=#eeeeee>
    <TD rowSpan=9><img border=0 name=xtdemo src=$imagesurl/face/$numid/$sp_sxgraphic width=84 hegiht=84></TD>
    <TD rowSpan=9><img border=0 name=dtdemo src=$imagesurl/face/$numid/$sp_graphic width=140 hegiht=226></TD>
    <TD height=20>��Ʒ���ƣ�<input type=text size=20 name=newname value="$sp_name"></TD>
  </TR>
  <TR><TD bgColor=#eeeeee height=20>��Ʒ������<input type=text size=20 name=newdescription value="$sp_description"></TD></TR>
  <TR><TD bgColor=#eeeeee height=20>��Ʒ���ۣ�<input type=text size=20 name=newmoney value="$sp_money"></TD></TR>
  <TR><TD bgColor=#eeeeee height=20>������Ⱥ��$tempoutput</TD></TR>
  <TR><TD bgColor=#eeeeee height=20>��ƷͼƬ��<input type=text size=10 name=newgraphic value="$sp_graphic">
<select name="image" onChange=select()><option value="$sp_graphic">ѡ��ͼƬ$myimages</select></TD></TR>
  <TR><TD bgColor=#eeeeee height=20>��ƷСͼ��<input type=text size=10 name=newsxgraphic value="$sp_sxgraphic">
<select name="image2" onChange=select1()><option value="$sp_sxgraphic">ѡ��ͼƬ$myimages</select></TD></TR>
  <TR><TD bgColor=#eeeeee height=20 align=center><input type=submit value="�� Ҫ �� ��"> <input type=reset value=�ء���></TD></TR>
</form>
</TABLE>~;
#  <TR><TD bgColor=#eeeeee height=20>��Ʒ������<input type=text size=20 name=newwear value="$sp_wear"></TD></TR>
}

sub editok{
    $class	= $query -> param('class');		# ��Ʒ����
    $id		= $query -> param('id');		# ��ƷID��
$class =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$id =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

    $newname	= $query -> param('newname');			# ��Ʒ����
    $newmoney	= $query -> param('newmoney');			# ��Ʒ�۸�
    $newdescription	= $query -> param('newdescription');	# ��Ʒ����
    $newdescription	= &unHTML("$newdescription");
    $newwear	= $query -> param('newwear');			# ��Ʒ����
    $newwear	= &unHTML("$newwear");
    $newfit	= $query -> param('newfit');			# �ʺ���Ⱥ
    $newgraphic	= $query -> param('newgraphic');		# ��Ʒ��ͼ
    $newgraphic	= &unHTML("$newgraphic");
    $newsxgraphic	= $query -> param('newsxgraphic');	# ��ƷСͼ
    $newsxgraphic	= &unHTML("$newsxgraphic");

    &errorout("0","��Ʒ�����Ʋ���Ϊ�գ�") if ($newname eq '');
    &errorout("0","��Ʒ�ļ۸���Ϊ�գ�") if ($newmoney eq '');
    &errorout("0","��Ʒ�۸��к��зǷ��ַ�����������") unless ($newmoney=~ /^[0-9]+$/);
    &errorout("0","����ȷ������Ʒ���ۣ��۸���Ϊ������") if($newmoney < 0);
    &errorout("0","��Ʒ��������Ϊ�գ�") if ($newdescription eq '');
#    &errorout("0","��Ʒ�;����к��зǷ��ַ�����������") unless ($newwear=~ /^[0-9]+$/);
#    &errorout("0","����ȷ������Ʒ���;öȣ�����Ϊ�������") if($newwear <= 0);
    &errorout("0","��Ʒ��ͼƬ��ַ����Ϊ�գ�") if ($newgraphic eq '');
    &errorout("0","��Ʒ��ͼƬ��ַ����Ϊ�գ�") if ($newsxgraphic eq '');

    $/="";
    my $filetoopen = "$lbdir" . "face/wpdata/$class.pl";
    open(FILE,"$filetoopen");
    my $sort=<FILE>;
    close(FILE);
    $/="\n";

    if($sort =~ /$id\t(.*)/)	# �ҵ�ָ������ƷID
    {
	$sort =~ s/$1/$newname\t$newmoney\t$newdescription\t$newwear\t$newfit\t$newgraphic\t$newsxgraphic\t\t/;
	open(FILE,">$filetoopen");
	print FILE $sort;
	close(FILE);
    }

print qq~
<script>opener.location.reload();</script>
<tr>
<td bgcolor=#EEEEEE align=center>
<font color=#990000 size=1><b>�޸ĳɹ���3��󷵻أ�</b></font>
</td>
</tr></table><meta http-equiv="refresh" content="3; url=$thisprog?action=edit_sp&num=$class&id=$id">~;
exit;
}

sub del_sp
{
    $num        = $query -> param('num');	# ��Ʒ����ļ�
    $id        = $query -> param('id');		# ��Ʒ��ID��
$num =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$id =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

    $/="";
    my $filetoopen = "$lbdir" . "face/wpdata/$num.pl";
    open(FILE,"$filetoopen");
    my $sort=<FILE>;
    close(FILE);
    $/="\n";

    if($sort =~ s/$id\t(.*)\n//)	# �ҵ�ָ������ƷID
    {
	open(FILE,">$filetoopen");
	print FILE $sort;
	close(FILE);
    }
    else
    {
	&errorout("1","�����Ʒ�Ѿ������ڣ�");
    }

    print qq~<script>opener.location.reload();setTimeout("self.close()",3000);</script>
<tr><td bgcolor=#EEEEEE align=center><font color=#990000 size=1><b>ɾ���ɹ���3��󱾴����Զ��رգ�</b></font></td></tr>
</table>~;
    exit;
}

sub errorout{
    my($errortype,$errormsg)=@_;
    if($errortype eq 1)
    {
	print qq~<script>alert("$errormsg");self.close();</script>~;
    }
    else
    {
	print qq~<script>alert("$errormsg");history.back();</script>~;
    }
    exit;
}