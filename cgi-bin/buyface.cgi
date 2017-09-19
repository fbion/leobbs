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
$LBCGI::POST_MAX=600000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "data/cityinfo.cgi";
require "face/config.pl";
require "facelib.pl";
$|++;
$query = new LBCGI;
$thisprog = "buyface.cgi";

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

$action = $query->param('action');

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

$tempmembername = $inmembername;
$tempmembername =~ s/ /\_/g;
$tempmembername =~ tr/A-Z/a-z/;

$mymoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

&readface("$tempmembername",0);

$currenttime = time();
$currenttime = &dateformat("$currenttime");

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print qq~
<html>
<head>
<title>$plugname</title>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<style>
A:visited{TEXT-DECORATION: none}
A:active{TEXT-DECORATION: none}
A:hover{TEXT-DECORATION: underline overline}
A:link{text-decoration: none;}
TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: ����; FONT-SIZE: 9pt} 
.S1{LINE-HEIGHT: 1.2}
</style>
</head>
<body bgcolor="#ffffff" topmargin=0 leftmargin=0>~;

my %Mode = ('buy' => \&buy_sp,'save' => \&savesp,'bag' => \&bag,'delsp' => \&delsp,'zeng' => \&zengsp,'zengok' => \&zengok);

if ($Mode{$action})
{
$Mode{$action} -> ();
}
else{&error("$plugname&�ϴ󣬱��Һ��ҵĳ���ѽ����");}

sub buy_sp
{
    $cartLength = $query->cookie("cartLength");
    &errorout("������Ʒ&��ǰ�Ĺ����Ϊ�գ�&1") if(($cartLength eq '')||($cartLength eq '0'));

    for ($i = 0; $i < $cartLength; $i++)
    {
	$itemsinfo = $query->cookie("items[$i]");
	($name,$sort_id,$id,$buy_num,$x,$x)=split(/\|/,$itemsinfo);
###
	$/="";
	my $filetoopen = "$lbdir" . "face/wpdata/$sort_id.pl";
	&errorout("������Ʒ&��Ʒ�����ļ������ڣ�&1") if (!( -e "$filetoopen")); # ����������ļ�
	open(FILE,"$filetoopen");
	my $sort=<FILE>;
	close(FILE);
	$/="\n";

	&errorout("������Ʒ&�ǳ���Ǹ��$name ��Ʒ�����ݿ��в����ڣ�&1") if($sort !~ /$id\t(.*)/); # �ҵ�ָ������ƷID
        ($sp_name,$sp_money,$x,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$sp_suit,$sp_suitid)=split(/\t/,$1);

###
	for($j=0;$j<$buy_num;$j++)
	{
	    $array1{$sort_id} .= "$id,N\_";	# �����ʽ
	}
	$array2{$sort_id} += "$buy_num";					# ���������ʽ�����š�����
	$array3{$id} = "1\t$sp_name\t$buy_num\t$sp_money\t$currenttime\t\t\n";	# ��¼���˹�����Ϣ
    }

    @array2 = keys(%array2);

    for($i=0;$i<@array2;$i++)
    {
	$aaaa = @array2[$i];
	@tempnum = split(/\_/,@buy_sp[$aaaa]);
	$tempnum = @tempnum;
	$temp = $tempnum + $array2{$aaaa};
	&errorout("������Ʒ&�ǳ���Ǹ����ͬ����Ʒ���������涨ֵ��$samnum ��(���ѹ����)��&1") if($temp > $samnum);
    }

    $TotalCost = $query->cookie("totalCost");	# ��ȡ�ܼ۸�
    &errorout("������Ʒ&�ǳ���Ǹ�������ֽ𲻹�֧�����������Ʒ��&1") if ($mymoney < $TotalCost);

    @array1 = keys(%array1);

    for($i=0;$i<@array1;$i++)
    {
	$aaaa = @array1[$i];
	@buy_sp[$aaaa] = @buy_sp[$aaaa] ne '' ? "@buy_sp[$aaaa]_$array1{$aaaa}" : "$array1{$aaaa}";
	chop(@buy_sp[$aaaa]);
    }

    for($i=1;$i<26;$i++)
    {
	$newdata .= "@buy_sp[$i]-";
    }
    chop($newdata);

    &upplugdata("$tempmembername","$currequip|$newdata|$loadface","-$TotalCost");

##### ͳ��ʹ����
    $filetoopen = "$lbdir" . "face/totaluser.cgi";
    open(FILE,"$filetoopen");
    my $totaluser=<FILE>;
    close(FILE);
    if($totaluser !~ /$tempmembername\t/)
    {
	open(FILE, ">>$filetoopen");
	print FILE "$tempmembername\t";
	close(FILE);
    }
#####

    $filetoopen = "$lbdir" . "face/log/$tempmembername.pl";
    open(FILE,"$filetoopen");
    my @mylog=<FILE>;
    open(FILE, ">$filetoopen");
    @array3 = values(%array3);
    foreach (@array3)
    {
	print FILE $_;
    }

    foreach $z (@mylog){
	$a=$a+1;
	if ($a < $lognum){print FILE "$z";}
    }
    close(FILE);

    print qq~
<SCRIPT language="javaScript" SRC="$imagesurl/face/js/buy.js"></SCRIPT>
<SCRIPT>
function delAlls()
{
  var cartLength = getCookie('cartLength');
  if((cartLength  == "") || (cartLength == 0))
      return;

  for (var i = 0; i < cartLength; i ++)
  {
      eval("deleteCookie('items["+i+"]')");
  }
  cartLength = 0;
  setCookie('cartLength', cartLength);
}
delAlls();
alert("��Ʒ����ɹ����뵽 �ҵ��¹� װ����");
self.close();
</SCRIPT>~;
}

sub savesp
{
    &errorout("����ʧ��&��������������ݲ����ڣ�����ʧ��&1��") if ($userface eq '');

    my $spsort1	= $query->cookie("_SortArray");	# �����
    my $spid1	= $query->cookie("_SPIDArray");	# ��ƷID��
    my $spstate1= $query->cookie("_StateArray");# ��Ʒ״̬
    my @SPSort = split(/\,/,$spsort1);
    my @SPID = split(/\,/,$spid1);
    my @SPState = split(/\,/,$spstate1);

    for($i=0;$i<@SPSort;$i++)
    {
	$SPINFO{@SPSort[$i]} .= "@SPID[$i]-@SPState[$i]|";
    }

    for($i=1;$i<26;$i++)
    {
	@tempsp=split(/\_/,@buy_sp[$i]);
	next if(@tempsp eq "");

	$/="";
	my $filetoopen = "$lbdir" . "face/wpdata/$i.pl";
	open(FILE,"$filetoopen");
	my $sort=<FILE>;
	close(FILE);
	$/="\n";
	$temp1 = 0;
	$tempdata = '';
	for($j=0;$j<@tempsp;$j++)
	{
	    my ($info1,$info2)=split(/\,/,@tempsp[$j]);
	    my $ladesign = $info2 eq 'Y' ? 1 : 0 ;
	    $spsort2 .= qq~$i,~;
	    $spid2 .= qq~$info1,~;
	    $spstate2 .= qq~$ladesign,~;

	    if($SPINFO{$i} ne '')
	    {
		my @temparray = split(/\|/,$SPINFO{$i});
		my ($tempid,$tempstate) = split(/\-/,@temparray[$j]);
		my $ladesign = $tempstate eq '1' ? 'Y' : 'N';
		$info2 = $ladesign if($tempid eq $info1);
		$tempdata .= qq~$info1,$info2\_~;
	    }
###
	    if($sort =~ /$info1\t(.*)/)
	    {
	        my ($sp_name,$sp_money,$x,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$sp_suit,$sp_suitid)=split(/\t/,$1);

	        if($info2 eq 'Y')
	        {
		    $sp_graphic =~s /\.gif//;
		    @currequip[$i] = $sp_graphic;
		    $temp1 = 1;
	        }
	        else
	        {
		     next if($temp1 eq '1');
		     if(($i eq '7')||($i eq '8')||($i eq '9')||($i eq '11')||($i eq '13')||($i eq '14')||($i eq '18'))
		     {
			@currequip[$i] = $sex eq 'f' ? "initf" : "init";
		     }
		     else
		     {
			@currequip[$i] = 0;
		     }
		}
	    }
###
	}
	chop($tempdata);
	$outinfo .= qq~$tempdata-~;
    }
    chop($spsort2);
    chop($spid2);
    chop($spstate2);
    chop($outinfo);

    &errorout("����ʧ��&�벻Ҫ����&1��") if(($spsort1 ne $spsort2) || ($spid1 ne $spid2));
    &errorout("����ʧ��&ϵͳ��������װ��״̬û�иı䣬������Ҫ���棡&1") if($spstate1 eq $spstate2);

    $newequip = join('-',@currequip);
    &upplugdata("$tempmembername","$newequip|$outinfo|$loadface","");

print qq~
<SCRIPT LANGUAGE="JavaScript">
document.cookie = "_SortArray=" + "" +"; path=$cookiepath/";
document.cookie = "_SPIDArray=" + "" +"; path=$cookiepath/";
document.cookie = "_StateArray=" + "" +"; path=$cookiepath/";
opener.location.reload();
alert("��ǰ���󱣴�ɹ���");
self.close();
</SCRIPT>~;
    exit;
}

sub bag
{ # �����
    print qq~
<SCRIPT>
function openCart() 
{
   var url="$boardurl/buyface.cgi?action=bag"
   var cart;
   cart =window.open(url,"Cart","menubar=no,toolbar=no,location=no,directories=no,status=no,width=530,height=400,left=150,top=100,scrollbars=yes");
   cart.focus();
}
</SCRIPT>
<SCRIPT language="javaScript" type="text/javascript" SRC="$imagesurl/face/js/buy.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
function subItemQuantity(num, typeid) 
{
	var i;
	var infoArray = new Array;
	var cartLength = getCookie('cartLength');
	if(cartLength  == "" || cartLength == 0) 
	    return;
	infoArray[1] = typeid;
	infoArray[2] = num;

	var i = checkExistItem(infoArray, cartLength);
	if(i != -1) //�ҵ���item[i]
	{
	    infoArray = getItemsInfo(i); 
	    var count = infoArray[3];
	    count --;
	    if(count == 0) //item����������0
	    {
		delItem(i);
		return;
	    }

	    infoArray[3] = count;
	    saveItemsinfo(infoArray, i);
	    openCart();
	    return;
	}
}

function delItem(i)
{
  var tmpArray = new Array;
  var cartLength = getCookie('cartLength');
  if((cartLength  == "") || (cartLength == 0))
      return;

  if(cartLength == 1)
  {
      deleteCookie('items[0]');
      setCookie('cartLength', 0);  
      openCart();
      return;
  }
  cartLength --;
      for (i = i; i < cartLength; i ++)
      {
	tmpArray = getItemsInfo(i + 1);
	saveItemsinfo(tmpArray, i);
      }
      eval("deleteCookie('items["+cartLength+"]')");
      setCookie('cartLength', cartLength);
      openCart();
}

function delAll()
{
  var cartLength = getCookie('cartLength');
  if((cartLength  == "") || (cartLength == 0))
      return;
  for (var i = 0; i < cartLength; i ++)
  {
      eval("deleteCookie('items["+i+"]')");
  }
  cartLength = 0;
  setCookie('cartLength', cartLength);
  alert("������Ѿ���գ�");
  self.close();
}

function delAlls()
{
  var cartLength = getCookie('cartLength');
  if((cartLength  == "") || (cartLength == 0))
      return;

  for (var i = 0; i < cartLength; i ++)
  {
      eval("deleteCookie('items["+i+"]')");
  }
  cartLength = 0;
  setCookie('cartLength', cartLength);
}

function displayCart()
{
  var s = '';
  var totalCost = 0;
  var name, typeid, num, price, quantity;
  var cartLength = getCookie('cartLength');

  var infoArray = new Array;
  if ((cartLength == "") || (cartLength == 0))
  {
    alert("Ŀǰ�����Ϊ�գ�");
    self.close();
    return;
  }
  for (var i = 0; i < cartLength; i++)
  {
	infoArray = getItemsInfo(i);

	if(infoArray == -1)
	{
		alert("ȡ���ﳵ��Ϣ���������Զ���չ��ﳵһ��!");
		delAll();
		return;
	}
	name = infoArray[0];
	typeid = infoArray[1];
	num = infoArray[2];
	quantity = infoArray[3];
	price = infoArray[4];

	total = price*quantity;
	totalCost = totalCost + total;

	ID = typeid+""+num;
	s = s + '<tr align=center bgcolor=$miscbackone>';
	s = s + '<td width=60>' + ID + '</td>';
	s = s + "<td width=260 align=center>";
	s = s + ''+ name + '';
	s = s + '</td>';
	s = s + '<td width=80>';
        s = s + '' + quantity + '��<img src="$imagesurl/face/images/del.gif" style=cursor:hand alt = "����" width=11 height=11'; 
	s = s + ' onClick="subItemQuantity(';
	s = s + "'" + num + "','" + typeid + "');";
	s = s + '"> ';
        s = s + '<img src="$imagesurl/face/images/add.gif" alt="����" width="11" height="11" style=cursor:hand onClick="addItemQuantity(';
	s = s + "'" + name + "','" + typeid + "'," + num + "," + price + ");";
	s = s + '"></td>';
        s = s + '<td width=60 align=right>';
	s = s + price ; 
	s = s + '</td>';
 	s = s + '<td width="40" align=center><img src="$imagesurl/face/images/delt.gif" style=cursor:hand width="24" height="11" alt="ɾ��" onclick="var truth =confirm(';
	s = s + "'ȷ��Ҫɾ����'); if (truth)  delItem(" + i + ");";
	s = s + '" > </td>'; 
	s = s + '</tr>';
  }
  setCookie('totalCost', totalCost);
  document.write(s);
}

function displayTotal()
{
  var totalCost;
  var cartLength = getCookie('cartLength');  
  if ((cartLength == "") || (cartLength == 0))
      totalCost = 0;
  else
  {
      totalCost = getCookie('totalCost');
  }
  document.write(totalCost);
}
function jz()
{
totalCost = getCookie('totalCost');
  if (confirm('�ܼƣ�'+totalCost+' $moneyname �����Ƿ�ȷ�Ϲ���'))
	window.location='buyface.cgi?action=buy';
}
</SCRIPT>

<table cellspacing=1 cellpadding=5 width=100% bgcolor=$tablebordercolor border=0>
<tr bgcolor=$miscbacktwo align=left><td><font color=$titlefont size=2><B>�ҵĹ����</B></font></td></tr>
</table>
<BR>
<table cellspacing=1 cellpadding=5 width=100% bgcolor=$tablebordercolor border=0>
<tr bgcolor=$miscbacktwo align=center>
   <td width=60>��ƷID</td>
   <td width=260>��Ʒ����</td>
   <td width=80>��������</td>
   <td width=60>��Ʒ����</td>
   <td width=40>&nbsp;</td>
</tr>
<SCRIPT>displayCart();</SCRIPT>
<tr bgcolor=$miscbacktwo>
   <td width=60></td>
   <td width=260></td>
   <td width=80 align=right>�ܼƣ�</td>
   <td width=60 align=right><SCRIPT>displayTotal();</SCRIPT></td>
   <td width=40>&nbsp;</td>
</tr>
<tr bgcolor=$miscbackone>
   <td width=60></td>
   <td width=260></td>
   <td width=80 align=right>����ǰ�ֽ�</td>
   <td width=60 align=right>$mymoney</td>
   <td width=40>$moneyname</td>
</tr>
</table>

<table width="100%" border="0" cellspacing="0" cellpadding="0" height="20">
<tr><td>&nbsp;</td></tr>
<tr> 
<td align="center">
<a href="javascript:jz();">��Ҫ����</a> <a href="#" onclick="if (confirm('ȷ��Ҫȫ��ɾ����')) delAll(); else return false; ">��չ����</a> <a href="javascript:window.close();">��������</a>
</td>
</tr>
</table>~;
exit;
}

sub delsp
{
    $class	= $query -> param('class');	# ��Ʒ����
    $id		= $query -> param('id');	# ��ƷID��

    @tempsp = split(/\_/, @buy_sp[$class]);	# ����ƷͼƬ�ֿ���ʹ֮����Ʒ������Ӧ

    ($info1,$info2)=split(/\,/,@tempsp[$id]);
    &errorout("����ʧ��&���Ƿ��Ѿ������˸���Ʒ��&1") if(@tempsp[$id] eq '');
    &errorout("����ʧ��&����Ʒ����װ���У����ܽ��ж���������&1") if($info2 eq 'Y');


    for($i=0;$i<@tempsp;$i++)
    {
	$newid .= qq~@tempsp[$i]_~ if($i ne $id);
    }
    chop($newid);
    @buy_sp[$class] = $newid;

    for($i=1;$i<26;$i++)
    {
	$newdata .= "@buy_sp[$i]-";
    }
    chop($newdata);

    &upplugdata("$tempmembername","$currequip|$newdata|$loadface","");

print qq~
<SCRIPT LANGUAGE="JavaScript">
document.cookie = "tempequip=" + "$currequip" +"; path=$cookiepath/";
opener.location.reload();
alert("��Ʒ�����ɹ���");
self.close();
</SCRIPT>
~;
    exit;
}

sub zengsp
{
    $class      = $query -> param('class');		# ��Ʒ����ļ�
    $id	        = $query -> param('id');		# ��Ʒ��ID��

    @tempsp = split(/\_/, @buy_sp[$class]);		# ����ƷͼƬ�ֿ���ʹ֮����Ʒ������Ӧ

    ($info1,$info2)=split(/\,/,@tempsp[$id]);

    &errorout("������Ʒ&����ҳ�����ָ������Ʒ������&1��") if(@tempsp[$id] eq '');
    &errorout("������Ʒ&����Ʒװ���У�����ж�²������ͣ������Ʒ\\n�Ѿ�ж�£����Ƿ����ǵ�� '���浱ǰ����' �ˣ�&1") if($info2 eq 'Y');

###
    $/="";
    my $filetoopen = "$lbdir" . "face/wpdata/$class.pl";
    open(FILE,"$filetoopen");
    my $sort=<FILE>;
    close(FILE);
    $/="\n";

    if($sort =~ /$info1\t(.*)/)	# �ҵ�ָ������ƷID
    {
	($sp_name,$sp_money,$x,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$sp_suit,$sp_suitid)=split(/\t/,$1);
	&errorout("������Ʒ&С���������Ʒ�������͸����ѵģ�&1") if($sp_money eq '0');
	$fitherd = "��" if($sp_fitherd eq 'm');
	$fitherd = "Ů" if($sp_fitherd eq 'f');
	$fitherd = "ͨ��" if($sp_fitherd eq 't');
    }
    else
    {
	&errorout("������Ʒ&����ҳ���������Ʒ�Ѿ������ڣ��붪������Ʒ��&1");
    }
###
## �����б� ###
    if (open(FILE, "${lbdir}memfriend/$tempmembername.cgi"))
    {
	$/="";
	my $currentlist = <FILE>;
	close(FILE);
	$/="\n";
	@currentlist = split (/\n/, $currentlist);
    }

    my $friendlist = qq~<select name=friends onchange="myfriend();"><option style=background-color:$miscbacktwo>�����б�</option>~;

    foreach (@currentlist)
    {
	chomp;
	s/^����������//isg;
	$friendlist .= qq~<option value="$_">$_</option>~;
    }
## ���� ##

    print qq~<SCRIPT>
function checkzeng()
{
   if(document.Zeng.zengname.value == "")
   {
	alert("�Է������ֲ���Ϊ�գ�");
	document.Zeng.zengname.focus();
	return false;
   }
   if(document.Zeng.zengly.value == "")
   {
	alert("���Բ���Ϊ�գ�");
	document.Zeng.zengly.focus();
	return false;
   }
   if(!confirm("������Ϣ��$sp_name Ҽ�������Ƿ�ȷ�����͸� " + document.Zeng.zengname.value + "��"))return false;
}
function myfriend()
{
    var myfriend = document.Zeng.friends.options[document.Zeng.friends.selectedIndex].value;
    if (myfriend != "") document.Zeng.zengname.value = myfriend;
}
</SCRIPT>
<table width=100% border=0 cellspacing=1 cellpadding=5 bgcolor=$tablebordercolor>
<tr><td bgcolor=$miscbacktwo height=20><font color=$titlefont size=2><B>������Ʒ</B></font></td></tr>
</table>
<table width=100% border=0 cellspacing=0 cellpadding=4>
<form action="$thisprog" method="post" name=Zeng>
<input type=hidden name="action" value="zengok">
<input type=hidden name="class" value="$class">
<input type=hidden name="id" value="$id">
<TR align=center bgColor=$miscbackone>
  <TD width=40%>��Ʒ����</TD><TD width=30%>������Ⱥ</TD><TD width=30%>��Ʒ�۸�</TD>
</TR>
<TR align=center bgcolor=$miscbacktwo>
  <TD>$sp_name</TD><TD>$fitherd</TD><TD>$sp_money</TD>
</TR>
<TR align=center bgColor=$miscbackone> 
  <TD colspan=3> ��</TD>
</TR>
<TR bgColor=$miscbacktwo> 
  <TD align=center>���͸�</TD><TD colspan=2><input type=text size=12 name="zengname"> $friendlist</TD>
</TR>
<TR bgColor=$miscbacktwo> 
  <TD align=center>����</TD><TD colspan=2><input type=text size=30 name="zengly"></TD>
</TR>
<TR align=center bgColor=$miscbackone>
  <TD colspan=3><input type=submit value="ȷ ��" onClick="return checkzeng();">
  </TD>
</TR>
</form>
</table>~;
}

sub zengok
{
    $class	= $query -> param('class');	# ��Ʒ����
    $id		= $query -> param('id');	# ��ƷID��
    $zengname	= $query -> param('zengname');	# ����������
    $zengname	= &cleanarea("$zengname");
    $zengly	= $query -> param('zengly');	# ������������
    $zengly	= &cleanarea("$zengly");

    $zengname = &unHTML("$zengname");
    $zengname =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    $zengname =~ s/ /\_/g;
    $zengname =~ tr/A-Z/a-z/;

    my $namenumber = &getnamenumber($zengname);
    &checkmemfile($zengname,$namenumber);
    my $filetoopen = "${lbdir}$memdir/$namenumber/$zengname.cgi";
    &errorout("������Ʒ&�ǳ���Ǹ�������в����ڴ��û�����&0") unless(-e $filetoopen);
    &errorout("������Ʒ&��ͷ�Ի���������ô�ܸ��Լ����ͣ�����&0") if($tempmembername eq $zengname);

    @tempsp = split(/\_/, @buy_sp[$class]);			# ����ƷͼƬ�ֿ���ʹ֮����Ʒ������Ӧ
    &errorout("������Ʒ&�ǳ���Ǹ�����������Ʒѡ�����&1") if(@tempsp[$id] eq '');
    ($info1,$info2)=split(/\,/,@tempsp[$id]);

###
    $/="";
    my $filetoopen = "$lbdir" . "face/wpdata/$class.pl";
    open(FILE,"$filetoopen");
    my $sort=<FILE>;
    close(FILE);
    $/="\n";

    if($sort =~ /$info1\t(.*)/)	# �ҵ�ָ������ƷID
    {
	($sp_name,$sp_money,$x,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$sp_suit,$sp_suitid)=split(/\t/,$1);
    }
    else
    {
	&errorout("������Ʒ&����ҳ���������Ʒ�Ѿ������ڣ��붪������Ʒ��&1");
    }
###

    for($i=0;$i<@tempsp;$i++)
    {
	$newid .= qq~@tempsp[$i]_~ if($i ne $id);
    }
    chop($newid);
    @buy_sp[$class] = $newid;

    for($i=1;$i<26;$i++)
    {
	$newdata .= "@buy_sp[$i]-";
    }
    chop($newdata);

    &upplugdata("$tempmembername","$currequip|$newdata|$loadface","");
#####

    my $filetoopen = "$lbdir" . "face/log/$tempmembername.pl";	# д���û���¼�ļ�������Ϊ 1
    open(FILE,"$filetoopen");
    my @mylog=<FILE>;
    close(FILE);

    open(FILE, ">$filetoopen");
    print FILE "2\t$sp_name\t1\t$sp_money\t$currenttime\t$zengname\t$zengly\n";

    foreach $m (@mylog){
	$a=$a+1;
	if ($a < $lognum){print FILE "$m";}
    }
    close(FILE);
######

    my $filetoopen = "$lbdir" . "face/log/$zengname.pl";	# д���û���¼�ļ�������Ϊ 1
    open(FILE,"$filetoopen");
    my @mylog=<FILE>;
    open(FILE, ">$filetoopen");
    print FILE "3\t$sp_name\t1\t$sp_money\t$currenttime\t$tempmembername\t$zengly\n";

    foreach $z (@mylog){
	$a=$a+1;
	if ($a < $lognum){print FILE "$z";}
    }
    close(FILE);

    my $mcon = qq~������� <font color=blue>$tempmembername</font> ��������һ����Ʒ�� $sp_name ���������˵�� <font color=blue>$zengly</font><BR><BR><a href=face.cgi?action=mybureau target=_blank>�鿴������������</a>~;
    &write_messages("$tempmembername","$zengname","������������ѶϢ","$mcon");

######

    &readface("$zengname",1);

    @buy_sp[$class] = @buy_sp[$class] ne '' ? "@buy_sp[$class]_$info1,N" : "$info1,N";

    $newdata = '';
    for($i=1;$i<26;$i++)
    {
	$newdata .= "@buy_sp[$i]-";
    }
    chop($newdata);

    &upplugdata("$zengname","$currequip|$newdata|$loadface","");
    print qq~<SCRIPT>opener.location.reload();setTimeout("self.close()",100);alert("��Ʒ���ͳɹ���");</SCRIPT>~;
    exit;
}