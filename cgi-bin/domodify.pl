#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    require "cleanolddata.pl";
    &cleanolddata2;
    $helpurl = &helpfiles("��������");
    $helpurl = qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;

    if ("$userregistered" eq "no") {&error("�޸�����&û�д��û�����"); }
    if ("$inpassword" ne "$password") {&error("�޸�����&��̳������������µ�¼���޸ģ�"); }
    if (("$passwordverification" eq "yes") && ("$emailfunctions" ne "off")) {
	$newpassneeded = "<br><B>������޸����ʼ���ַ��һ���µ���̳���뽫ͨ���ʼ���������</B>";
	undef $newpasswordaddon;
    }
    $newpasswordaddon = qq~
<tr><td bgcolor=$miscbackone width=40%><font color=$fontcolormisc><b>��̳���룺</b> �������޸���̳���룬���ִ�Сд<br>ֻ��ʹ�ô�Сд��ĸ�����ֵ����,�������ڣ�λ</td>
<td bgcolor=$miscbackone width=60%><input type=password name="newpassword1" maxlength=20>��$helpurl</td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>��̳���룺 (����8λ)</b><br>����һ�飬�Ա�ȷ����</td>
<td bgcolor=$miscbackone><input type=password name="newpassword2" maxlength=20>��$helpurl</td>
</tr><tr>
<td bgcolor=$miscbacktwo valign=middle colspan=2 align=center>
<font color=$fonthighlight><b>����㲻���޸���̳���룬�뱣������հף�</b></font></td></tr>
~;

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        &whosonline("$inmembername\t��������\tnone\t�޸�<b>$inmembername</b>�ĸ�������\t");
    }

    if ($avatars eq "on") {
        if ($arrowavaupload eq "on") {
            $avaupload = qq~<br>�ϴ�ͷ�� <input type="file" size=20 name="addme">���ϴ��Զ���ͷ��<br>~;
        }
        else { undef $avaupload; }

    open (FILE, "${lbdir}data/lbava.cgi");
    my @images = <FILE>;
    close (FILE);
    chomp @images;

    $selecthtml .= qq~<option value="noavatar" selected>��Ҫͷ��</option>\n~;
    $currentface = "noavatar";
    foreach (@images) {
	$totleavator=@images -1;
        $cleanavatar =  $_;
        $cleanavatar =~ s/\.(gif|jpg)$//i;
        if (($cleanavatar =~ /admin_/) && ($membercode eq "me")) { next; }
        if ($cleanavatar eq "$useravatar") {
	    $selecthtml .= qq~<option value="$cleanavatar" selected>$cleanavatar</option>\n~;
            $currentface = "$cleanavatar";
        }
        elsif (($cleanavatar eq "noavatar") && (!$useravatar)) {
        }
	else {
            $selecthtml .= qq~<option value="$cleanavatar">$cleanavatar</option>\n~;
        }
    }
	    
    $personalavatar =~ s/\$imagesurl/${imagesurl}/o;
    $avatarhtml = qq~
<script>
function showimage(){document.images.useravatars.src="$imagesurl/avatars/"+document.creator.useravatar.options[document.creator.useravatar.selectedIndex].value+".gif";}
</script>
<tr>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>����ͼƬ��</b><br>������ѡ��һ������ͼƬ�����㷢��ʱ����ʾ�����������·���<BR>�������д��������Զ���ͷ�񲿷֣���ô���ͷ�����Զ����Ϊ׼���������������Զ���ͷ���������Ŀ��<BR>
<br><b>�����Զ���ͷ��</b>��<br>��Ҳ����������������Զ���ͷ��� URL ��ַ��ͷ��ĸ߶ȺͿ��(����)�� �������Ҫ�Զ���ͷ���뽫��Ӧ��Ŀȫ�����գ�<BR>�������дͷ��ĸ߶ȺͿ�ȣ���ϵͳ���Զ��жϲ����롣<BR><BR>
<br><b>����㲻��Ҫ�κε�ͷ����ô�������ڲ˵���ѡ��noavatar����Ȼ�����������Զ���ͷ��Ĳ��֣�</b><BR><br>
<BR>��Ҳ����������������������ḻ��ʵĸ�������<a href=face.cgi><font color=$fonthighlight>�밴�˽���</font></a>��<BR>
</td>
<td bgcolor=$miscbackone valign=top>��ͷ������� $totleavator ������<a href=viewavatars.cgi target=_blank><B>���˲鿴</B></a>����ͷ�������б�<BR>
<select name="useravatar" size=1 onChange="showimage()">
$selecthtml
</select>
<img src=$imagesurl/avatars/$currentface.gif name="useravatars" width=32 height=32 hspace=15><br><br><br>
$avaupload
<br>ͼ��λ�ã� <input type="text" name="newpersonalavatar" size="26" value="$personalavatar">������������ URL ·����<br>
<br>ͼ���ȣ� <input type="text" name="newpersonalwidth" size="2" maxlength=3 value="$personalwidth">�������� 20 -- $maxposticonwidth ֮���һ��������<br>
<br>ͼ��߶ȣ� <input type="text" name="newpersonalheight" size="2" maxlength=3 value="$personalheight">�������� 20 -- $maxposticonheight ֮���һ��������<br></td>
</td></tr>
~;
    }
    $userflag = "blank" if ($userflag eq "");
    $flaghtml = qq~
<script language="javascript">
function showflag(){document.images.userflags.src="$imagesurl/flags/"+document.creator.userflag.options[document.creator.userflag.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=$miscbackone valign=top><font face="$font" color=$fontcolormisc><b>���ڹ���:</b><br>��ѡ�������ڵĹ��ҡ�</td>
<td bgcolor=$miscbackone>
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
<img src="$imagesurl/flags/$userflag.gif" name="userflags" border=0 height=14 width=21>
</td></tr>
~;
    $flaghtml =~ s/value=\"$userflag\"/value=\"$userflag\" selected/;

    my ($getpassq, $getpassa) =split(/\|/,$userquestion); 
    $getpassFORM =qq~ 
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��̳������ʾ���⣺</b>����ȡ�������˵���̳����<br>��� 20 ���ַ���10�����֣�</td> 
<td bgcolor=$miscbackone><input type=text name="getpassq" value="$getpassq" size=20 maxlength=20></td> 
</tr> 
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��̳������ʾ�𰸣�</b>�������ʹ��<br>��� 20 ���ַ���10�����֣�</td> 
<td bgcolor=$miscbackone><input type=text name="getpassa" value="$getpassa" size=20 maxlength=20></td> 
</tr><tr> 
<td bgcolor=$miscbacktwo valign=middle colspan=2 align=center> 
<font color=$fonthighlight><b>��̳������ʾ����ʹ��ǲ��ܹ��޸ĵģ���������룡</b></font></td></tr>~ if(($userquestion eq "")||($userquestion eq "|"));

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
    $interests =~ s/<br>/\n/isg;
    $interests =~ s/<p>/\n/isg;
    $interests =~ s/\n+/\n/isg;

    $tempoutput = "<select name=\"newshowemail\">\n<option value=\"yes\">��\n<option value=\"msn\">MSN\n<option value=\"popo\">��������\n<option value=\"no\">��\n</select>\n";
    $tempoutput =~ s/value=\"$showemail\"/value=\"$showemail\" selected/;

    $output .= qq~
<script>
function chk(){
if(!document.creator.oldpassword.value){alert('Ϊ�˰�ȫ��������Ŀǰ��̳�����롣');document.creator.oldpassword.focus();return false;}
}
</script>
<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center>
<form action="$thisprog" method=post name="creator" enctype="multipart/form-data" onsubmit="return chk()">
<input type=hidden name="action" value="process">
<input type=hidden name="oldsex" value="$sex">
<input type=hidden name="membername" value="$inmembername">
<font color=$fontcolormisc>�޸� <font color=$fonthighlight><b>$inmembername</b></font> �ĸ�������</td></tr>
<tr><td bgcolor=$miscbacktwo width=40%><font color=$fonthighlight><b>Ŀǰ��̳���룺</b> <U>Ϊ�˰�ȫ������������Ŀǰ����̳����</U></td>
<td bgcolor=$miscbacktwo width=60%><input type=password name="oldpassword" maxlength=20>��<font color=$fonthighlight>*</td>
</tr>
<tr><td bgcolor=$miscbacktwo valign=middle colspan=2 align=center></td></tr>
$newpasswordaddon$getpassFORM
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�ʼ���ַ��</b><br>��������Ч���ʼ���ַ���⽫��֤������̳�е�˽�����ϡ�$newpassneeded</td>
<td bgcolor=$miscbackone><input type=text name="newemailaddress" value="$emailaddress"></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>��ʾ�ʼ���ַ</b><br>
���Ƿ�ϣ��������������֮����ʾ�����ʼ���</td>
<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
</tr>
~;

    $membertitle = "" if ($membertitle =~ m/^member$/i);
    if (($editusertitleself eq "post") && ($jifen >= $needpoststitle)) { $editusertitleself = "on"; }
    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>����ͷ�Σ�</b><BR>��� 20 ���ַ���10�����֣�</td>
<td bgcolor=$miscbackone><input type=text name="newmembertitle" value="$membertitle" size=14 maxlength=20></td>
</tr>
~ if ($editusertitleself eq "on");

    if (($editjhmpself eq "post") && (($numberofposts + $numberofreplys) >= $needpostsjhmp)) { $editjhmpself = "on"; }
    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�������ɣ�</b><BR>��� 20 ���ַ���10�����֣�</td>
<td bgcolor=$miscbackone><input type=text name="newjhmp" value="$jhmp" size=14 maxlength=20></td>
</tr>
~ if ($editjhmpself eq "on");

    if ($editjhmpself eq "system") {
	my $jumpfile="$lbdir" . "data/jhmp.cgi";
	open(FILE,$jumpfile);
	my @JUMP=<FILE>;
	close(FILE);
	chomp @JUMP;
	if($membercode eq "ad" || $membercode eq "smo"){
	    @JUMP = grep(/^(.+?)\t[1|0]\t/,@JUMP);
	} else {
            @JUMP1 = grep(/^$jhmp\t0\t/,@JUMP);
	    @JUMP = grep(/^(.+?)\t1\t/,@JUMP);
	    push(@JUMP,@JUMP1);
	}
	push(@JUMP,"");
	my $JUMP=join("\n",@JUMP);
	my $temp_c=0;
	$JUMP=~s/(.+?)\t[1|0]\t(.*?)\t\n/
	my $temp=$1;
	my $temp1=$2;
	$temp=qq(<option value="$temp_c">$temp����[��ʼ�ˣ�$temp1]<\/option>);
	$temp_c++;
	$temp;
	/ge;
	$JUMP=qq(<option value="1000">��������</option>$JUMP);
	my $jhmp_c=quotemeta($jhmp);
	$JUMP=~s/<option value="([0-9]+)">$jhmp_c����\[(.+?)\]<\/option>/<option value="$1" selected>$jhmp����\[$2\]<\/option>/;
	$output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�������ɣ�</b><BR>��ѡ��һ����ϲ��������</td>
<td bgcolor=$miscbackone><select name="newjhmp">$JUMP</select></td>
</tr>
~;
    }

    $tempoutput = "<select name=\"newsex\" size=\"1\"><option value=\"no\">���� </option><option value=\"m\">˧�� </option><option value=\"f\">��Ů </option></select>\n";
    $tempoutput =~ s/value=\"$sex\"/value=\"$sex\" selected/;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�Ա�</b></td>
<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
</tr>
~;

    $tempoutput = "<select name=\"neweducation\" size=\"1\"><option value=\"����\">���� </option><option value=\"Сѧ\">Сѧ </option><option value=\"����\">���� </option><option value=\"����\">����</option><option value=\"��ר\">��ר</option><option value=\"��ר\">��ר</option><option value=\"����\">����</option><option value=\"˶ʿ\">˶ʿ</option><option value=\"��ʿ\">��ʿ</option><option value=\"��ʿ��\">��ʿ��</option></select>\n";
    $tempoutput =~ s/value=\"$education\"/value=\"$education\" selected/;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>���ѧ����</b></td>
<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
</tr>
~;

    $tempoutput = "<select name=\"newmarry\" size=\"1\"><option value=\"����\">���� </option><option value=\"δ��\">δ�� </option><option value=\"�ѻ�\">�ѻ� </option><option value=\"���\">��� </option><option value=\"ɥż\">ɥż </option></select>\n";
    $tempoutput =~ s/value=\"$marry\"/value=\"$marry\" selected/;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>����״����</b></td>
<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
</tr>
~;

    $tempoutput = "<select name=\"newwork\" size=\"1\"><option value=\"����\">���� </option><option value=\"�����ҵ\">�����ҵ </option><option value=\"����ҵ\">����ҵ </option><option value=\"��ҵ\">��ҵ </option><option value=\"������ҵ\">������ҵ </option><option value=\"����ҵ\">����ҵ </option><option value=\"ѧ��\">ѧ�� </option><option value=\"����ʦ\">����ʦ </option><option value=\"���ܣ�����\">���ܣ����� </option><option value=\"��������\">�������� </option><option value=\"����ҵ\">����ҵ </option><option value=\"����/���/�г�\">����/���/�г� </option><option value=\"ʧҵ��\">ʧҵ�� </option></select>\n";
    $tempoutput =~ s/value=\"$work\"/value=\"$work\" selected/;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>ְҵ״����</b></td>
<td bgcolor=$miscbackone><font color=$fontcolormisc>$tempoutput</font></td>
</tr>
~;

    ($year, $month, $day) = split(/\//, $born);
    $tempoutput1 = "<select name=\"newmonth\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option></select>\n";
    $tempoutput1 =~ s/value=\"$month\"/value=\"$month\" selected/;

    $tempoutput2 = "<select name=\"newday\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option><option value=\"13\">13</option><option value=\"14\">14</option><option value=\"15\">15</option><option value=\"16\">16</option><option value=\"17\">17</option><option value=\"18\">18</option><option value=\"19\">19</option><option value=\"20\">20</option><option value=\"21\">21</option><option value=\"22\">22</option><option value=\"23\">23</option><option value=\"24\">24</option><option value=\"25\">25</option><option value=\"26\">26</option><option value=\"27\">27</option><option value=\"28\">28</option><option value=\"29\">29</option><option value=\"30\">30</option><option value=\"31\">31</option></select>\n";
    $tempoutput2 =~ s/value=\"$day\"/value=\"$day\" selected/;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>���գ�</b>�粻����д����ȫ�����ա������ѡ</td>
<td bgcolor=$miscbackone><font color=$fontcolormisc><input type="text" name="newyear" size=4 maxlength=4 value="$year">��$tempoutput1��$tempoutput2��</font></td>
</tr>
~;

    if ($usersx eq "") {$usersx = "blank"};

    $tempoutput="<SELECT name=\"usersx\" onchange=showsx() size=\"1\"> <OPTION value=blank>����</OPTION> <OPTION value=\"sx1\">����</OPTION> <OPTION value=\"sx2\">��ţ</OPTION> <OPTION value=\"sx3\">����</OPTION> <OPTION value=\"sx4\">î��</OPTION> <OPTION value=\"sx5\">����</OPTION> <OPTION value=\"sx6\">����</OPTION> <OPTION value=\"sx7\">����</OPTION> <OPTION value=\"sx8\">δ��</OPTION> <OPTION value=\"sx9\">���</OPTION> <OPTION value=\"sx10\">�ϼ�</OPTION> <OPTION value=\"sx11\">�繷</OPTION> <OPTION value=\"sx12\">����</OPTION></SELECT>\n";
    $tempoutput =~ s/value=\"$usersx\"/value=\"$usersx\" selected/;

    $output.=qq~
<SCRIPT language=javascript>
function showsx(){document.images.usersxs.src="$imagesurl/sx/"+document.creator.usersx.options[document.creator.usersx.selectedIndex].value+".gif";}
</SCRIPT>
<tr><td bgcolor=$miscbackone vAlign=top><font color=$fontcolormisc><b>������Ф��</b>��ѡ������������Ф��</td>
<td bgcolor=$miscbackone>$tempoutput<IMG border=0 name=usersxs src=$imagesurl/sx/$usersx.gif align=absmiddle>
</TD></TR>
~;
    if ($userxz eq "") {$userxz = "blank"};
    $tempoutput="<SELECT name=\"userxz\" onchange=showxz() size=\"1\"> <OPTION value=blank>����</OPTION> <OPTION value=\"z1\">������(3��21--4��19��)</OPTION> <OPTION value=\"z2\">��ţ��(4��20--5��20��)</OPTION> <OPTION value=\"z3\">˫����(5��21--6��21��)</OPTION> <OPTION value=\"z4\">��з��(6��22--7��22��)</OPTION> <OPTION value=\"z5\">ʨ����(7��23--8��22��)</OPTION> <OPTION value=\"z6\">��Ů��(8��23--9��22��)</OPTION> <OPTION value=\"z7\">�����(9��23--10��23��)</OPTION> <OPTION value=\"z8\">��Ы��(10��24--11��21��)</OPTION> <OPTION value=\"z9\">������(11��22--12��21��)</OPTION> <OPTION value=\"z10\">ħ����(12��22--1��19��)</OPTION> <OPTION value=\"z11\">ˮƿ��(1��20--2��18��)</OPTION> <OPTION value=\"z12\">˫����(2��19--3��20��)</OPTION></SELECT>\n";
    $tempoutput =~ s/value=\"$userxz\"/value=\"$userxz\" selected/;
    $output.=qq~
<SCRIPT language=javascript>
function showxz(){document.images.userxzs.src="$imagesurl/star/"+document.creator.userxz.options[document.creator.userxz.selectedIndex].value+".gif";}
</SCRIPT>
<tr><td bgcolor=$miscbackone vAlign=top><font color=$fontcolormisc><b>����������</b>��ѡ����������������<br>�������ȷ���������յĻ�����ô������Ч��</td>
<td bgcolor=$miscbackone>$tempoutput<IMG border=0 height=15 name=userxzs src=$imagesurl/star/$userxz.gif width=15 align=absmiddle>
</TD></TR>
~;

    $output .= qq~
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��ҳ��ַ��</b><br>���������ҳ����������ҳ��ַ�������ѡ</td>
<td bgcolor=$miscbackone><input type=text name="newhomepage" value="$homepage"></td>
</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>OICQ �ţ�</b><br>������� OICQ����������롣�����ѡ</td>
<td bgcolor=$miscbackone><input type=text name="newoicqnumber" value="$oicqnumber"></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>ICQ �ţ�</b><br>������� ICQ����������롣�����ѡ</td>
<td bgcolor=$miscbackone><input type=text name="newicqnumber" value="$icqnumber"></td>
</tr>$flaghtml<tr>
<script src=$imagesurl/images/comefrom.js></script>
<body onload="init()">
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>���ԣ�</b><br>�����������ڵĵط��������ѡ</td>
<td bgcolor=$miscbackone>
ʡ�� <select name="province" onChange = "select()"></select>������ <select name="city" onChange = "select()"></select><br>
���� <input type=text name="newlocation" value="$location" maxlength=12 size=20 style="font-weight: bold">�����ܳ���12���ַ���6�����֣�</td>
</tr><tr>
~;

    $timedifference = 0 if ($timedifference eq '');
    $tempoutput = "<select name=\"newtimedifference\"><option value=\"-23\">- 23</option><option value=\"-22\">- 22</option><option value=\"-21\">- 21</option><option value=\"-20\">- 20</option><option value=\"-19\">- 19</option><option value=\"-18\">- 18</option><option value=\"-17\">- 17</option><option value=\"-16\">- 16</option><option value=\"-15\">- 15</option><option value=\"-14\">- 14</option><option value=\"-13\">- 13</option><option value=\"-12\">- 12</option><option value=\"-11\">- 11</option><option value=\"-10\">- 10</option><option value=\"-9\">- 9</option><option value=\"-8\">- 8</option><option value=\"-7\">- 7</option><option value=\"-6\">- 6</option><option value=\"-5\">- 5</option><option value=\"-4\">- 4</option><option value=\"-3\">- 3</option><option value=\"-2\">- 2</option><option value=\"-1\">- 1</option><option value=\"0\">0</option><option value=\"1\">+ 1</option><option value=\"2\">+ 2</option><option value=\"3\">+ 3</option><option value=\"4\">+ 4</option><option value=\"5\">+ 5</option><option value=\"6\">+ 6</option><option value=\"7\">+ 7</option><option value=\"8\">+ 8</option><option value=\"9\">+ 9</option><option value=\"10\">+ 10</option><option value=\"11\">+ 11</option><option value=\"12\">+ 12</option><option value=\"13\">+ 13</option><option value=\"14\">+ 14</option><option value=\"15\">+ 15</option><option value=\"16\">+ 16</option><option value=\"17\">+ 17</option><option value=\"18\">+ 18</option><option value=\"19\">+ 19</option><option value=\"20\">+ 20</option><option value=\"21\">+ 21</option><option value=\"22\">+ 22</option><option value=\"23\">+ 23</select>";
    $tempoutput =~ s/value=\"$timedifference\"/value=\"$timedifference\" selected/;

    $output .= qq~
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>ʱ�</b><br>
����������ʱ����$basetimes<br>��������ڵ�λ�úͷ�������ʱ������롣<br>�Ժ����������е�ʱ�佫���������ڵĵ���ʱ����ʾ��</td>
<td bgcolor=$miscbackone>$tempoutput</td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>���Ҽ�飺 </b><BR>���ܳ��� <B>$maxinsline</B> �У�Ҳ���ܳ��� <B>$maxinslegth</B> ���ַ�<br><br>�������������ĸ��˼�顣�����ѡ</td>
<td bgcolor=$miscbackone><textarea name="newinterests" cols="60" rows="5">$interests</textarea></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>ǩ����</b><br>���ܳ��� <B>$maxsignline</B> �У�Ҳ���ܳ��� <B>$maxsignlegth</B> ���ַ�
<br><br>����ʹ�� HTML ��ǩ<br>����ʹ�� <a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS ��ǩ</a><BR>
<li>��ͼ��ǩ��: <b>$signpicstates</b><li>Flash ��ǩ: <b>$signflashstates</b><li>���ֱ�ǩ��: <b>$signsoundstates</b><li>���ִ�С��: <b>$signfontsizestates</b>
</td>
<td bgcolor=$miscbackone><textarea name="newsignature" cols="60" rows="8">$signature</textarea></td>
</tr>
$avatarhtml
<tr><td colspan=2 bgcolor=$miscbacktwo align=center><input type=submit value="�� ��" name=submit></td>
</form></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
1;
