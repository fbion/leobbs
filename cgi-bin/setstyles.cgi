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
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setstyles.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
#&ipbanned; #��ɱһЩ ip

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
	$theparam =~ s/\\/\\\\/g;
        $theparam =~ s/\@/\\\@/g;

        if (($_ eq 'maintopicad')||($_ eq 'replytopicad')) {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g
	}

        $theparam = &unHTML("$theparam");

        if ($_ eq "footmark" || $_ eq "headmark" || $_ eq "footmark1" || $_ eq "headmark1") {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g
	}

	${$_} = $theparam;
        if ($_ ne 'action'&&$_ ne 'yxz') {
        	$_ =~ s/[\a\f\n\e\0\r]//isg;
        	$theparam =~ s/[\a\f\n\e\0\r]//isg;
            $printme .= "\$" . "$_ = \"$theparam\"\;\n" if (($_ ne "")&&($theparam ne ""));
            }
	}
$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");

if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {
    if ($action eq "process") {

        $membergone=$query->param('membergone');
        if (($membergone > 180)||($membergone < 5)) {
        print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>��ӭ������̳�������� / �������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>����</b><br><br><br><br>����ʱ�䲻��С�ڣ����ӻ��߳���180���ӣ�����<br><Br><Br>
                    </td></tr></table></td></tr></table>
                    ~;
        exit;
        }
        $printme .= "1\;\n";

        $filetomake = "$lbdir" . "data/styles.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");

	@yxz = $query -> param('yxz');
	print FILE "\$yxz=\"";
	$temp = 0;
	foreach(@yxz){
	    chomp;
	    print FILE ",$_";
	    $temp=1;
	}
	if ($temp eq "1") {
	    print FILE ",\";\n";
	} else {
	    print FILE "\";\n";
	}
        
        print FILE "$printme";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata1 = grep(/^forumstoptopic/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumshead/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumstitle/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumstopic/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^plcache/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }

        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / �������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE colspan=2>
                <font color=#333333><center><b>���µ���Ϣȫ���ɹ�����</b><br><br>
                </center>~;

	print "\$yxz=\"";
	$temp = 0;
	foreach(@yxz){
	    chomp;
	    print ",$_";
	    $temp=1;
	}
	if ($temp eq "1") {
	    print ",\";<BR>";
	} else {
	    print "\";<BR>";
	}
 
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                $printme =~ s/1\;//g;
                print $printme;

                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }

                else {
                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>��ӭ������̳�������� / �������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>������Ϣû�б���</b><br>�ļ�����Ŀ¼����д������������Ϊ 777 ��
                    </td></tr></table></td></tr></table>
                    ~;
                    }

            }
            else {

        $dirtoopen = "$lbdir" . "data/skin";
        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);
        my $myskin="";
        @thd = grep(/\.cgi$/,@dirdata);
        $topiccount = @thd;
        @thd=sort @thd;
        for (my $i=0;$i<$topiccount;$i++){
       	$thd[$i]=~s /\.cgi//isg;
        $myskin.=qq~<option value="$thd[$i]">Ƥ�� [ $thd[$i] ]~;
        }
        $myskin =~ s/value=\"$skinselected\"/value=\"$skinselected\" selected/;
                $inmembername =~ s/\_/ /g;

                print qq~
                <tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF>
                <b>��ӭ������̳�������� / Ƥ������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#333333><b>�趨Ƥ�����</b>
                </td></tr>
		~;
if ($cssname ne "") {print qq~<tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>Ƥ������</font></td><td bgcolor=#FFFFFF><input type=text name="cssname" size=10 value="$cssname"></td></tr><tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>��ɫ����</font></td><td bgcolor=#FFFFFF><input type=text name="cssmaker" size=10 value="$cssmaker"></td></tr><tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>��ɫ���</font></td><td bgcolor=#FFFFFF><textarea cols=40 name="cssreadme" rows=2>$cssreadme</textarea>
</td></tr>~};


print qq~
                <form action="$thisprog" method="post" name=FORM>
                <input type=hidden name="action" value="process">

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>ʹ��ϵͳ�Դ���Ƥ�����</b><br>��ѡ��ĳ�����󣬴�ҳ���еĺ���ɫ��ص�����һ����Ч<BR>���Ҫ�ô�ҳ���ڵ�������Ч,��ѡ��[Ĭ�Ϸ��]</font></td>
                <td bgcolor=#FFFFFF>
                <select name="skinselected">
                <option value="">Ĭ�Ϸ��$myskin
                </select>
                </td></tr>
~;

               $tempoutput = "<select name=\"usesuperannounce\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$usesuperannounce\"/value=\"$usesuperannounce\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=���� color=#333333><b>�Ƿ�ʹ����̳��������</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>������������</b><br>(֧��HTML��ʽ����ʾ�������û�)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="superannounce" cols="40">$superannounce</textarea><BR>
                </td>
                </tr>
		~;
	$footmark   =~ s/\[br\]/\n/isg;
	$headmark   =~ s/\[br\]/\n/isg;
	$footmark1   =~ s/\[br\]/\n/isg;
	$headmark1   =~ s/\[br\]/\n/isg;

               $tempoutput = "<select name=\"superannouncedisp\">\n<option value=\"oncepersession\">ÿ������ֻ��ʾһ��\n<option value=\"always\">������ʾ\n<option value=\"2\">50%��ʾ����\n<option value=\"3\">33%��ʾ����\n<option value=\"4\">25%��ʾ����\n<option value=\"10\">10%��ʾ����\n<option value=\"20\">5%��ʾ����\n<option value=\"50\">2%��ʾ����\n<option value=\"100\">1%��ʾ����\n</select>\n"; 
               $tempoutput =~ s/value=\"$superannouncedisp\"/value=\"$superannouncedisp\" selected/; 

               $tempoutput1 = "<select name=\"superannouncehide\">\n<option value=\"yes\">��ʮ����Զ�����\n<option value=\"no\">һֱ��ʾ\n</select>\n"; 
               $tempoutput1 =~ s/value=\"$superannouncehide\"/value=\"$superannouncehide\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=���� color=#333333><b>��̳��������ѡ��</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput $tempoutput1</td> 
               </tr> 

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳BODY��ǩ</b>
                </font></td>
                </tr>

                <input type=hidden name="skin" value="$skin" size=10 maxlength=10>
                <input type=hidden name="cssmaker" value="$cssmaker">
                <input type=hidden name="cssname" value="$cssname">
                <input type=hidden name="cssurl" value="$cssurl">
                <input type=hidden name="cssprogrammaker" value="$cssprogrammaker">
                <input type=hidden name="cssprogrammakerurl" value="$cssprogrammakerurl">
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����������̳���ı�����ɫ���߱���ͼƬ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lbbody" size=40 value="$lbbody"><br>Ĭ�ϣ�bgcolor=#FFFFFF  alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=0</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳ҳü��ҳ��</b>
                </font></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>��ҳ����ҳü</b><br>(������ʾ����ҳ�����Ϸ���HTML��ʽ)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="headmark1" cols="40">$headmark1</textarea><BR>
                </td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>��ҳ����ҳ��</b><br>(������ʾ���װ�Ȩ��Ϣ�·���HTML��ʽ)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="footmark1" cols="40">$footmark1</textarea><BR>
                </td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>ҳü</b><br>(��ʾ��ҳ�����Ϸ���HTML��ʽ)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="headmark" cols="40">$headmark</textarea><BR>
                </td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>ҳ��</b><br>(��ʾ�ڰ�Ȩ��Ϣ�·���HTML��ʽ)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="footmark" cols="40">$footmark</textarea><BR>
                </td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>��������������</b><br>(��ʾ�ڵ��������м�)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="navadd" cols="40">$navadd</textarea><BR>
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ���ʾԭ��ҳü</font></td>
                <td bgcolor=#FFFFFF>
		~;
                $tempoutput = "<select name=\"usetopm\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select><p>\n";
                $tempoutput =~ s/value=\"$usetopm\"/value=\"$usetopm\" selected/;
                print qq~
                $tempoutput</td>
		</tr>
<script>
function selcolor(obj,obj2){
var arr = showModalDialog("$imagesurl/editor/selcolor.html", "", "dialogWidth:18.5em; dialogHeight:17.5em; status:0");
obj.value=arr;
obj2.style.backgroundColor=arr;
}
</script>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳ҳ�ײ˵�</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�˵���������ɫ</font></td>
                <td bgcolor=$menufontcolor width=12 id=menufontcolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menufontcolor" value="$menufontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,menufontcolor2)" style="cursor:hand">��Ĭ�ϣ�#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�˵���������ɫ</font></td>
                <td bgcolor=$menubackground  width=12 id=menubackground2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menubackground" value="$menubackground" size=7 maxlength=7 onclick="javascript:selcolor(this,menubackground2)" style="cursor:hand">��Ĭ�ϣ�#DDDDDD</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�˵�������ͼƬ</font><BR>������ͼƬ���ƣ���ͼ������ images Ŀ¼�µ� $skin ��</td>
                <td background=$imagesurl/images/$skin/$menubackpic width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menubackpic" value="$menubackpic"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>�˵����߽���ɫ</font></td>
                <td bgcolor=$titleborder width=12 id=titleborder2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titleborder" value="$titleborder" size=7 maxlength=7 onclick="javascript:selcolor(this,titleborder2)" style="cursor:hand">��Ĭ�ϣ�#333333</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>������ۺ���ɫ</b>(����޸ģ���ô���޸ĺ���̳��ʼ������� Cache һ��)
                </font></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���������</font></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"font\">\n<option value=\"����\">����\n<option value=\"����_gb2312\">����\n<option value=\"����_gb2312\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"��Բ\">��Բ\n</select><p>\n";
                $tempoutput =~ s/value=\"$font\"/value=\"$font\" selected/;
                print qq~
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"�������"������ɫ</font></td>
                <td bgcolor=$lastpostfontcolor width=12 id=lastpostfontcolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lastpostfontcolor" value="$lastpostfontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,lastpostfontcolor2)" style="cursor:hand">��Ĭ�ϣ�#000000</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"������"������ɫ</font></td>
                <td bgcolor=$fonthighlight  width=12 id=fonthighlight2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="fonthighlight" value="$fonthighlight" size=7 maxlength=7 onclick="javascript:selcolor(this,fonthighlight2)" style="cursor:hand">��Ĭ�ϣ�#990000</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�鿴ʱ��������������</font></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"posternamefont\">\n<option value=\"����\">����\n<option value=\"����_gb2312\">����\n<option value=\"����_gb2312\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"��Բ\">��Բ\n</select><p>\n";
                $tempoutput =~ s/value=\"$posternamefont\"/value=\"$posternamefont\" selected/;
                print qq~
                $tempoutput</td>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>һ���û�����������ɫ</font></td>
                <td bgcolor=$posternamecolor  width=12 id=posternamecolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="posternamecolor" value="$posternamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,posternamecolor2)" style="cursor:hand">��Ĭ�ϣ�#000066</td>
                </tr>

		<tr>
		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>һ���û������ϵĹ�����ɫ</font></td>
		<td bgcolor=$memglow  width=12 id=memglow2>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="memglow" value="$memglow" size=7 maxlength=7 onclick="javascript:selcolor(this,memglow2)" style="cursor:hand">��Ĭ�ϣ�#9898BA</td>
		</tr>
               
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>̳������������ɫ</font></td>
                <td bgcolor=$adminnamecolor  width=12 id=adminnamecolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="adminnamecolor" value="$adminnamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,adminnamecolor2)" style="cursor:hand">��Ĭ�ϣ�#990000</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>̳�������ϵĹ�����ɫ</font></td>
		<td bgcolor=$adminglow  width=12 id=adminglow2>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="adminglow" value="$adminglow" size=7 maxlength=7 onclick="javascript:selcolor(this,adminglow2)" style="cursor:hand">��Ĭ�ϣ�#9898BA</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ܰ�������������ɫ</font></td>
                <td bgcolor=$smonamecolor  width=12 id=smonamecolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="smonamecolor" value="$smonamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,smonamecolor2)" style="cursor:hand">��Ĭ�ϣ�#009900</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>�ܰ��������ϵĹ�����ɫ</font></td>
		<td bgcolor=$smoglow  width=12 id=smoglow2>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="smoglow" value="$smoglow" size=7 maxlength=7 onclick="javascript:selcolor(this,smoglow2)" style="cursor:hand">��Ĭ�ϣ�#9898BA</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��������������������ɫ</font></td>
                <td bgcolor=$cmonamecolor  width=12 id=cmonamecolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="cmonamecolor" value="$cmonamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,cmonamecolor2)" style="cursor:hand">��Ĭ�ϣ�#009900</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>���������������ϵĹ�����ɫ</font></td>
		<td bgcolor=$cmoglow  width=12 id=cmoglow2>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="cmoglow" value="$cmoglow" size=7 maxlength=7 onclick="javascript:selcolor(this,cmoglow2)" style="cursor:hand">��Ĭ�ϣ�#9898BA</td>
		</tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��������������ɫ</font></td>
                <td bgcolor=$teamnamecolor  width=12 id=teamnamecolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="teamnamecolor" value="$teamnamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,teamnamecolor2)" style="cursor:hand">��Ĭ�ϣ�#0000ff</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>���������ϵĹ�����ɫ</font></td>
		<td bgcolor=$teamglow  width=12 id=teamglow2>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="teamglow" value="$teamglow" size=7 maxlength=7 onclick="javascript:selcolor(this,teamglow2)" style="cursor:hand">��Ĭ�ϣ�#9898BA</td>
		</tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������������ɫ</font></td>
                <td bgcolor=$amonamecolor  width=12 id=amonamecolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="amonamecolor" value="$amonamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,amonamecolor2)" style="cursor:hand">��Ĭ�ϣ�#009900</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>�����������ϵĹ�����ɫ</font></td>
		<td bgcolor=$amoglow  width=12 id=amoglow2>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="amoglow" value="$amoglow" size=7 maxlength=7 onclick="javascript:selcolor(this,amoglow2)" style="cursor:hand">��Ĭ�ϣ�#9898BA</td>
		</tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��֤�û�����������ɫ</font></td>
                <td bgcolor=$rznamecolor  width=12 id=rznamecolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="rznamecolor" value="$rznamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,rznamecolor2)" style="cursor:hand">��Ĭ�ϣ�#44ff00</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>��֤�û������ϵĹ�����ɫ</font></td>
		<td bgcolor=$rzglow  width=12 id=rzglow2>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="rzglow" value="$rzglow" size=7 maxlength=7 onclick="javascript:selcolor(this,rzglow2)" style="cursor:hand">��Ĭ�ϣ�#008736</td>
		</tr>
		
		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>���˺ͽ����û������ϵĹ�����ɫ</font></td>
		<td bgcolor=$banglow  width=12 id=banglow2>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="banglow" value="$banglow" size=7 maxlength=7 onclick="javascript:selcolor(this,banglow2)" style="cursor:hand">��Ĭ�ϣ�none</td>
		</tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>����ҳ����ɫ</center></b>
                <font color=#333333>��Щ��ɫ���ý�����ÿ��ҳ�档����ע�ᡢ��¼�������Լ�����ҳ�档
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>��������ɫһ</font></td>
                <td bgcolor=$fontcolormisc  width=12 id=fontcolormisc3>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="fontcolormisc" value="$fontcolormisc" size=7 maxlength=7 onclick="javascript:selcolor(this,fontcolormisc3)" style="cursor:hand">��Ĭ�ϣ�#333333</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>��������ɫ��</font></td>
                <td bgcolor=$fontcolormisc2  width=12 id=fontcolormisc4>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="fontcolormisc2" value="$fontcolormisc2" size=7 maxlength=7 onclick="javascript:selcolor(this,fontcolormisc4)" style="cursor:hand">��Ĭ�ϣ�#444444</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫһ</font></td>
                <td bgcolor=$miscbackone  width=12 id=miscbackone2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="miscbackone" value="$miscbackone" size=7 maxlength=7 onclick="javascript:selcolor(this,miscbackone2)" style="cursor:hand">��Ĭ�ϣ�#FFFFFF</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫ��</font></td>
                <td bgcolor=$miscbacktwo  width=12 id=miscbacktwo2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="miscbacktwo" value="$miscbacktwo" size=7 maxlength=7 onclick="javascript:selcolor(this,miscbacktwo2)" style="cursor:hand">��Ĭ�ϣ�#EEEEEE</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>�����ɫ</center></b>
                <font color=#333333>��Щ��ɫ�󲿷�����leobbs.cgi��forums.cgi��topic.cgi
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�����������ɫ</font></td>
                <td bgcolor=$catback  width=12 id=catback2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catback" value="$catback" size=7 maxlength=7 onclick="javascript:selcolor(this,catback2)" style="cursor:hand">��Ĭ�ϣ�#ebebFF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ͼƬ</font><BR>������ͼƬ���ƣ���ͼ������ images Ŀ¼�µ� $skin ��</td>
                <td background=$imagesurl/images/$skin/$catbackpic  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catbackpic" value="$catbackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>���������ͼƬ</font><BR>������ͼƬ���ƣ���ͼ������ images Ŀ¼�µ� $skin ��</td>
                <td background=$imagesurl/images/$skin/$catsbackpicinfo  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catsbackpicinfo" value="$catsbackpicinfo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�����������ɫ</font></td>
                <td bgcolor=$catfontcolor  width=12 id=catfontcolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catfontcolor" value="$catfontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,catfontcolor2)" style="cursor:hand">��Ĭ�ϣ�#333333</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>���б��߽���ɫ</font></td>
                <td bgcolor=$tablebordercolor  width=12 id=tablebordercolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="tablebordercolor" value="$tablebordercolor" size=7 maxlength=7 onclick="javascript:selcolor(this,tablebordercolor2)" style="cursor:hand">��Ĭ�ϣ�#000000</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���б����</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="tablewidth" value="$tablewidth" size=5 maxlength=5>��Ĭ�ϣ�750</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>��������ɫ</center></b>
                <font color=#333333>������ɫ�����������ÿ�ݲ�������������ɫ
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>������������ɫ</font></td>
                <td bgcolor=$navborder width=12 id=navborder2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="navborder" value="$navborder" size=7 maxlength=7 onclick="javascript:selcolor(this,navborder2)" style="cursor:hand">��Ĭ�ϣ�#E6E6E6</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>������������ɫ</font></td>
                <td bgcolor=$navbackground width=12 id=navbackground2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="navbackground" value="$navbackground" size=7 maxlength=7 onclick="javascript:selcolor(this,navbackground2)" style="cursor:hand">��Ĭ�ϣ�#F7F7F7</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>������������ɫ</font></td>
                <td bgcolor=$navfontcolor width=12 id=navfontcolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="navfontcolor" value="$navfontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,navfontcolor2)" style="cursor:hand">��Ĭ�ϣ�#4D76B3</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>������ɫ</center></b>
                <font color=#333333>������ɫ�������ڷ����һ������ı���
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��̳/����ı�����������ɫ</font></td>
                <td bgcolor=$titlecolor  width=12 id=titlecolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titlecolor" value="$titlecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,titlecolor2)" style="cursor:hand">��Ĭ�ϣ�#acbded</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>��̳/����ı�����������ɫ</font></td>
                <td bgcolor=$titlefontcolor  width=12 id=titlefontcolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titlefontcolor" value="$titlefontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,titlefontcolor2)" style="cursor:hand">��Ĭ�ϣ�#333333</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>��̳������ɫ</center></b>
                <font color=#333333>�鿴��̳����ʱ��ɫ (forums.cgi)
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>������ɫһ</font></td>
                <td bgcolor=$forumcolorone  width=12 id=forumcolorone2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumcolorone" value="$forumcolorone" size=7 maxlength=7 onclick="javascript:selcolor(this,forumcolorone2)" style="cursor:hand">��Ĭ�ϣ�#f0F3Fa</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>������ɫ��</font></td>
                <td bgcolor=$forumcolortwo  width=12 id=forumcolortwo2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumcolortwo" value="$forumcolortwo" size=7 maxlength=7 onclick="javascript:selcolor(this,forumcolortwo2)" style="cursor:hand">��Ĭ�ϣ�#F2F8FF</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ɫ</font></td>
                <td bgcolor=$forumfontcolor  width=12 id=forumfontcolor2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumfontcolor" value="$forumfontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,forumfontcolor2)" style="cursor:hand">��Ĭ�ϣ�#333333</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>�ظ���ɫ</center></b>
                <font color=#333333>�ظ�������ɫ(topic.cgi)
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ���ɫһ</font></td>
                <td bgcolor=$postcolorone  width=12 id=postcolorone2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcolorone" value="$postcolorone" size=7 maxlength=7 onclick="javascript:selcolor(this,postcolorone2)" style="cursor:hand">��Ĭ�ϣ�#EFF3F9</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ���ɫ��</font></td>
                <td bgcolor=$postcolortwo  width=12 id=postcolortwo2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcolortwo" value="$postcolortwo" size=7 maxlength=7 onclick="javascript:selcolor(this,postcolortwo2)" style="cursor:hand">��Ĭ�ϣ�#F2F4EF</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ�������ɫһ</font></td>
                <td bgcolor=$postfontcolorone  width=12 id=postfontcolorone2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postfontcolorone" value="$postfontcolorone" size=7 maxlength=7 onclick="javascript:selcolor(this,postfontcolorone2)" style="cursor:hand">��Ĭ�ϣ�#333333</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>�ظ�������ɫ��</font></td>
                <td bgcolor=$postfontcolortwo  width=12 id=postfontcolortwo2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postfontcolortwo" value="$postfontcolortwo" size=7 maxlength=7 onclick="javascript:selcolor(this,postfontcolortwo2)" style="cursor:hand">��Ĭ�ϣ�#555555</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>ҳ����</center></b><br>
                <font color=#333333>ÿҳ��ʾ����Ļظ�������һƪ����ظ�����һ������ʱ��ҳ��ʾ (topic.cgi)
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÿҳ������</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxthreads" value="$maxthreads" size=3 maxlength=3>��һ��Ϊ 20 -- 30</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÿ����ÿҳ�Ļظ���</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtopics" value="$maxtopics" size=3 maxlength=3>��һ��Ϊ 10 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�ظ����������ٺ������������</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hottopicmark" value="$hottopicmark" size=3 maxlength=3>��һ��Ϊ 10 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ͶƱ���������ٺ��������ͶƱ����</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hotpollmark" value="$hotpollmark" size=3 maxlength=3>��һ��Ϊ 10 -- 15</td>
                </tr>
                ~;

			   $tempoutput = "<select name=\"usehigest\"><option value=\"yes\">ͻ��<option value=\"no\">��ͻ��</select>\n"; 
               $tempoutput =~ s/value=\"$usehigest\"/value=\"$usehigest\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>�Ƿ�ͻ�����Ʊ���Ķ�Ŀ��</font></td> 
               <td bgcolor=#FFFFFF>$tempoutput</td> 
               </tr> 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>ͻ�����Ʊ���Ķ�Ŀ��������ɫ</font></td> 
               <td bgcolor=#FFFFFF> 
               <input type=text name="higestcolor" value="$higestcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,higestcolor)" style="cursor:hand;background-color:$higestcolor">  Ĭ�ϣ�#0000FF</td> 
               </tr> 
               ~; 

               $tempoutput = "<select name=\"higestsize\">\n<option value=\"3\">3\n<option value=\"4\">4\n<option value=\"5\">5\n<option value=\"6\">6\n</select>\n"; 
               $tempoutput =~ s/value=\"$higestsize\"/value=\"$higestsize\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>ͻ�����Ʊ���Ķ�Ŀ�����ִ�С</font></td> 
               <td bgcolor=#FFFFFF>$tempoutput  Ĭ�ϣ�3</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÿҳ��ʾ�ı���ͼ����</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxoneemot" value="$maxoneemot" size=3 maxlength=3>��Ĭ��Ϊ 15����������ҳ��������Ϊ999</td>
                </tr>
               ~; 

				print qq~
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>LeoBBS ��ǩ����</center></b>(̳���Ͱ������ܴ���)<br>
                </td></tr>
                ~;

                $tempoutput = "<select name=\"arrawpostpic\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostpic\"/value=\"$arrawpostpic\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ�������ͼ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostflash\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostflash\"/value=\"$arrawpostflash\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ����� Flash��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostreal\"><option value=\"off\">������<option value=\"on\" >����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostreal\"/value=\"$arrawpostreal\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ����� Real �ļ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostmedia\"><option value=\"off\">������<option value=\"on\" >����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostmedia\"/value=\"$arrawpostmedia\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ����� Media �ļ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostsound\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostsound\"/value=\"$arrawpostsound\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ����������ļ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawautoplay\">\n<option value=\"1\">����\n<option value=\"0\">������\n</select>\n";
                $tempoutput =~ s/value=\"$arrawautoplay\"/value=\"$arrawautoplay\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����еĶ�ý���ļ��Ƿ������Զ����ţ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostfontsize\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawpostfontsize\"/value=\"$arrawpostfontsize\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ�����ı����ִ�С��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"openiframe\">\n<option value=\"no\">������\n<option value=\"yes\">����\n</select>\n";
                $tempoutput =~ s/value=\"$openiframe\"/value=\"$openiframe\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333>��̳�Ƿ����� Iframe ��ǩ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
		
		$tempoutput = "<select name=\"boarddispsign\">\n<option value=\"yes\">Ĭ����ʾ\n<option value=\"noselect\">Ĭ�ϲ���ʾ\n<option value=\"no\">��ֹ��ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$boarddispsign\"/value=\"$boarddispsign\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ���ʾ�����е�ǩ����</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"arrawsignpic\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawsignpic\"/value=\"$arrawsignpic\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ�������ͼ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"arrawsignflash\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawsignflash\"/value=\"$arrawsignflash\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ����� Flash��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawsignsound\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawsignsound\"/value=\"$arrawsignsound\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ�����������</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawsignfontsize\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>\n";
                $tempoutput =~ s/value=\"$arrawsignfontsize\"/value=\"$arrawsignfontsize\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ�����ı����ִ�С��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���Ӻ�ǩ���� Flash Ĭ�ϴ�С</font></td>
                <td bgcolor=#FFFFFF>
                ��ȣ� <input type=text name="defaultflashwidth" value="$defaultflashwidth" size=3 maxlength=3>��Ĭ�� 410 ����<BR>
                �߶ȣ� <input type=text name="defaultflashheight" value="$defaultflashheight" size=3 maxlength=3>��Ĭ�� 280 ����</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>��̳ͼ������</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Զ���ͷ�������</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxposticonwidth" value="$maxposticonwidth" size=3 maxlength=3>���벻Ҫ���� 110</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Զ���ͷ�����߶�</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxposticonheight" value="$maxposticonheight" size=3 maxlength=3>���벻Ҫ���� 130</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ͷ���Ĭ��ͼ����(Ϊ������)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultwidth" value="$defaultwidth" size=3 maxlength=3>��Ĭ�� 32 ���������Ϊ�գ�������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ͷ���Ĭ��ͼ��߶�(Ϊ������)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultheight" value="$defaultheight" size=3 maxlength=3>��Ĭ�� 32 ���������Ϊ�գ�������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����ͼ��Ĭ�Ͽ��(Ϊ������)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsmilewidth" value="$defaultsmilewidth" size=3 maxlength=3>��Ĭ�� 13 ���������Ϊ�գ�������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����ͼ��Ĭ�ϸ߶�(Ϊ������)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsmileheight" value="$defaultsmileheight" size=3 maxlength=3>��Ĭ�� 13 ���������Ϊ�գ�������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ���������ͼģʽ</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = qq~<select name=imgslt><option value="">������</option><option value="Disp">����</option></select>~;
                $tempoutput =~ s/value=\"$imgslt\"/value=\"$imgslt\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����ͼĬ�Ͽ��(Ϊ����Ĭ��Ϊ60)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsltwidth" value="$defaultsltwidth" size=3 maxlength=3></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����ͼ��Ĭ�ϸ߶�(Ϊ����Ĭ��Ϊ60)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsltheight" value="$defaultsltheight" size=3 maxlength=3></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����ͼÿ������</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = qq~<select name=sltnoperline><option value="3">3</option><option value="1">1</option><option value="2">2</option><option value="4">4</option><option value="5">5</option><option value="6">6</option></select>~;
                $tempoutput =~ s/value=\"$sltnoperline\"/value=\"$sltnoperline\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>��̳������ʽ����</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����������ʾ��С</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = qq~<select name=postfontsize><option value="12">Ĭ��</option><option value="15">�Դ�</option><option value="18">��ͨ</option><option value="21">�ϴ�</option><option value="24">�ܴ�</option><option value="30">���</option></select>~;
                $tempoutput =~ s/value=\"$postfontsize\"/value=\"$postfontsize\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���Ӷ��������</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"paraspace\">\n<option value=\"130\">Ĭ�ϼ��<option value=\"100\">�����о�<option value=\"150\">1.5���о�<option value=\"200\">˫���о�";
                $tempoutput =~ s/value=\"$paraspace\"/value=\"$paraspace\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����ּ�����</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"wordspace\">\n<option value=\"0\">Ĭ�ϼ��<option value=\"-1\">����<option value=\"+2\">����<option value=\"+4\">�ӿ�";
                $wordspace =~ s/\+/\\+/;
                $tempoutput =~ s/value=\"$wordspace\"/value=\"$wordspace\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�ظ�ʱ��Ĭ���г������ظ�����</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxlistpost" value="$maxlistpost" size=2 maxlength=2>��һ�� 5 -- 8 ��������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����������ӱ������������<br>���Լ��ؼ�����Ҫ���ӵı��⡣</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxhightopic" value="$maxhightopic" size=2 maxlength=2>��һ�� 10 -- 20 ��������</td>
                </tr>
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>�����趨�������ӵı�����ɫ!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_hightopic" value="$color_of_hightopic" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_hightopic)" style="cursor:hand;background-color:$color_of_hightopic">���Ƽ�ѡ��#990000</td>
              </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����̶ܹ���������̳���˵���������<br>�����̶ܹ�������Ҫ������������̳�������档</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="absmaxtoptopic" value="$absmaxtoptopic" size=2 maxlength=2>��һ�� 1 -- 5 ��������</td>
                </tr>
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>�����趨�̶ܹ����ӵ�������ɫ!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_absontop" value="$color_of_absontop" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_absontop)" style="cursor:hand;background-color:$color_of_absontop">���Ƽ�ѡ��#990000</td>
              </tr>
		~;

               $tempoutput = "<select name=\"abstopshake\">\n<option value=\"\">�������κη�ʽ\n<option value=\"1\">�ζ�\n<option value=\"2\">��ɫ\n<option value=\"3\">��ɫ\n</select>\n"; 
               $tempoutput =~ s/value=\"$abstopshake\"/value=\"$abstopshake\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>�̶ܹ����Ӳ���ʲô��Ŀ��ʽ��</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̶���ĳ�������˵���������<br>�������̶�������Ҫ����������������̳�������档</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="absmaxcantopic" value="$absmaxcantopic" size=2 maxlength=2>��һ�� 1 -- 5 ��������</td>
                </tr>
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>�����趨���̶����ӵ�������ɫ!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_quontop" value="$color_of_quontop" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_quontop)" style="cursor:hand;background-color:$color_of_quontop">���Ƽ�ѡ��#e7840d</td>
              </tr>
		~;

               $tempoutput = "<select name=\"cattopshake\">\n<option value=\"\">�������κη�ʽ\n<option value=\"1\">�ζ�\n<option value=\"2\">��ɫ\n<option value=\"3\">��ɫ\n</select>\n"; 
               $tempoutput =~ s/value=\"$cattopshake\"/value=\"$cattopshake\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>���̶����Ӳ���ʲô��Ŀ��ʽ��</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
              <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̶��ڶ��˵���������<br>���Թ̶�������Ҫ��������̳�������档</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtoptopic" value="$maxtoptopic" size=2 maxlength=2>��һ�� 1 -- 5 ��������</td>
                </tr>
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>�����趨�̶����ӵ�������ɫ!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_ontop" value="$color_of_ontop" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_ontop)" style="cursor:hand;background-color:$color_of_ontop">���Ƽ�ѡ��#002299</td>
              </tr>
		~;

               $tempoutput = "<select name=\"topshake\">\n<option value=\"\">�������κη�ʽ\n<option value=\"1\">�ζ�\n<option value=\"2\">��ɫ\n<option value=\"3\">��ɫ\n</select>\n"; 
               $tempoutput =~ s/value=\"$topshake\"/value=\"$topshake\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>�̶����Ӳ���ʲô��Ŀ��ʽ��</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����������</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsignline" value="$maxsignline" size=5 maxlength=2>��һ�� 5 ��(������������ʹ��)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ��������ַ���</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsignlegth" value="$maxsignlegth" size=5 maxlength=4>��һ�� 200 ����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���˼�����������</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxinsline" value="$maxinsline" size=5 maxlength=2>��һ��  5 ��(������������ʹ��)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���˼�������ַ���</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxinslegth" value="$maxinslegth" size=5 maxlength=4>��һ�� 100 ����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��̳ͶƱ����������������Ŀ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpollitem" value="$maxpollitem" size=2 maxlength=2>�������� 5 - 50 ֮��</td>
                </tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><center><b>��ʼ����Ч����</b> (leobbs.cgi & Forums.cgi)</center><br>
</font></td>
</tr>
~;


$tempoutput = "<select name=\"pagechange\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
$tempoutput =~ s/value=\"$pagechange\"/value=\"$pagechange\" selected/;
print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>����ҳ��ʱ�Ƿ�ʹ����Ч?</b><br>IE 4.0 ���ϰ汾�������Ч</font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

$tempoutput = "<select name=\"cinoption\">\n
<option value=\"0\">��״����\n
<option value=\"1\">��״����\n
<option value=\"2\">Բ������\n
<option value=\"3\">Բ�η���\n
<option value=\"4\">���ϲ���\n
<option value=\"5\">���²���\n
<option value=\"6\">���Ҳ���\n
<option value=\"7\">�������\n
<option value=\"8\">��ֱ�ڱ�\n
<option value=\"9\">ˮƽ�ڱ�\n
<option value=\"10\">��������ʽ\n
<option value=\"11\">��������ʽ\n
<option value=\"12\">����ֽ�\n
<option value=\"13\">��������������\n
<option value=\"14\">������������չ\n
<option value=\"15\">��������������\n
<option value=\"16\">������������չ\n
<option value=\"17\">�����³��\n
<option value=\"18\">�����ϳ��\n
<option value=\"29\">�����³��\n
<option value=\"20\">�����ϳ��\n
<option value=\"21\">���ˮƽ����\n
<option value=\"22\">�����ֱ����\n
<option value=\"23\">���(�����κ�һ��)\n
</select>\n";
$tempoutput =~ s/value=\"$cinoption\"/value=\"$cinoption\" selected/;
print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>��Ч����?</b></font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

	print qq~

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>��������</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ĭ���û�����ʱ���Ƕ��ٷ��ӣ�<BR>����û��������ʱ�仹û�ж�����Ĭ���û��Ѿ��뿪����̳��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="membergone" value="$membergone" size=3 maxlength=3>��һ��Ϊ 5 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÿ���������ɾ�����Ӵ�����(��̳����Ч)<br>�����������,������Ϊ 999.</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxdeloneday" value="$maxdeloneday" size=3 maxlength=3>��һ�� 5 - 10</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÿ����������ƶ����Ӵ�����(��̳����Ч)<br>�����������,������Ϊ 999.</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxmoveoneday" value="$maxmoveoneday" size=3 maxlength=3>  һ�� 5 - 10</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����Сʱ�ڵ���������� new ��־��<BR>(�������Ҫ����������Ϊ 0)</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newmarktime" value="$newmarktime" size=3 maxlength=3>��һ�� 12 - 24 Сʱ</td>
                </tr>
		~;
		
		$tempoutput = "<select name=\"usetodayforumreply\">\n<option value=\"yes\">�ǵģ���¼\n<option value=\"no\">��������¼\n</select>\n";
                $tempoutput =~ s/value=\"$usetodayforumreply\"/value=\"$usetodayforumreply\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>����̳�Ľ�������ͳ���Ƿ�ѻظ�Ҳ��¼��</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

               $tempoutput = "<select name=\"usejhpoint\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$usejhpoint\"/value=\"$usejhpoint\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>�Ƿ�ʹ���ھ�������ʹ�ñ�ǣ�</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                ~;

               $tempoutput = "<select name=\"nodispown\">\n<option value=\"no\">��ʹ��\n<option value=\"yes\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$nodispown\"/value=\"$nodispown\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>�Ƿ��־��ʾ�Լ��������ӣ�</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                ~;

               $tempoutput = "<select name=\"cancmodoutput\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n"; 
               $tempoutput =~ s/value=\"$cancmodoutput\"/value=\"$cancmodoutput\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>����ҳ�Ƿ���ʾ������������</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                ~;

               $tempoutput = "<select name=\"canuseview\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n"; 
               $tempoutput =~ s/value=\"$canuseview\"/value=\"$canuseview\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>��̳�Ƿ��������ŷ�ʽ�����Ķ���</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                ~;

               $tempoutput = "<select name=\"canusetreeview\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n"; 
               $tempoutput =~ s/value=\"$canusetreeview\"/value=\"$canusetreeview\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>��̳�Ƿ�����ʹ�ÿ���չ���ظ���</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                ~;
	$maintopicad   =~ s/\[br\]/\n/isg;
	$replytopicad   =~ s/\[br\]/\n/isg;

               $tempoutput = "<select name=\"useads\">\n<option value=\"no\">������\n<option value=\"yes\">����\n</select>\n"; 
               $tempoutput =~ s/value=\"$useads\"/value=\"$useads\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>�Ƿ�������̳���������棿</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>������������д(���û�У�������)</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="maintopicad" rows="5" cols="40">$maintopicad</textarea>
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>���ӻظ������д(���û�У�������)</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="replytopicad" rows="5" cols="40">$replytopicad</textarea>
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����ˢ����̳��ʱ����(��)<BR>������Ч��ֹ����ˢ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="banfreshtime" value="$banfreshtime" size=3 maxlength=3>��������裬������ 0</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"look\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$look\"/value=\"$look\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ񿪷���̳��ɫ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"showskin\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$showskin\"/value=\"$showskin\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ������û��Զ��������̳ʱ�ķ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"announcemove\">\n<option value=\"on\">�ƶ�\n<option value=\"off\">���ƶ�\n</select>\n";
               	$tempoutput =~ s/value=\"$announcemove\"/value=\"$announcemove\" selected/;
               	print qq~

               	<tr>
               	<td bgcolor=#FFFFFF colspan=2>
               	<font color=#333333>��̳�����Ƿ�����ƶ����</font></td>
               	<td bgcolor=#FFFFFF>
               	$tempoutput</td>
               	</tr>
               	~;

                 $tempoutput = "<select name=\"newmsgpop\"><option value=\"off\">����ʾ<option value=\"popup\">����<option value=\"light\">��˸<option value=\"on\">���߾�Ҫ</select>\n";
                $tempoutput =~ s/value=\"$newmsgpop\"/value=\"$newmsgpop\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���µĶ���Ϣ���ú�����ʾ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"payopen\"><option value=\"no\">������֧����������<option value=\"yes\">����֧����������</select>\n";
                $tempoutput =~ s/value=\"$payopen\"/value=\"$payopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳֧�������������ܣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"pollopen\"><option value=\"yes\">��ͶƱ<option value=\"no\">�ر�ͶƱ</select>\n";
                $tempoutput =~ s/value=\"$pollopen\"/value=\"$pollopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳ͶƱ���ܣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"xzbopen\"><option value=\"yes\">��С�ֱ�<option value=\"no\">�ر�С�ֱ�</select>\n";
                $tempoutput =~ s/value=\"$xzbopen\"/value=\"$xzbopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳С�ֱ����ܣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������С�ֱ����������</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hownews" value="$hownews" size=4 maxlength=4>��Ĭ�ϣ�100</td>
                </tr>
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font color=#333333><B>��������������Ӳ�����ظ���</B></font><BR>���������һ�λظ�ʱ�����</td>
               <td bgcolor=#FFFFFF>
               <input type=text name="rdays" value="$rdays" size=4 maxlength=4>���� (������裬������)</td>
               </tr>
                ~;

                $tempoutput = "<select name=\"infosopen\"><option value=\"0\">�κ��˿��Բ鿴<option value=\"1\">ע���û����Բ鿴<option value=\"2\">̳���Ͱ������Բ鿴<option value=\"3\">ֻ��̳�����Բ鿴</select>\n";
                $tempoutput =~ s/value=\"$infosopen\"/value=\"$infosopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�б��������ϲ鿴���ŷ�ʽ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"searchopen\">\n<option value=\"0\">�����κ�������\n<option value=\"1\">ֻ����ע���Ա���ϼ�������\n<option value=\"2\">ֻ������֤��Ա���ϼ�������<option value=\"3\">ֻ����������ϼ�������<option value=\"4\">ֻ����̳������<option value=\"99\">�ر�����</select>\n";
                $tempoutput =~ s/value=\"$searchopen\"/value=\"$searchopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������ӹ��ܿ��ŷ�ʽ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"searchall\">\n<option value=\"yes\">����ȫ������\n<option value=\"no\">������ȫ������</select>\n";
                $tempoutput =~ s/value=\"$searchall\"/value=\"$searchall\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ�����ȫ������</font> ����Ļ���ȫ����������������Դ(��̳��������)</td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"viewadminlog\">\n<option value=\"0\">�����κ��˲鿴\n<option value=\"1\">ֻ����ע���Ա���ϼ���鿴\n<option value=\"2\">ֻ������֤��Ա���ϼ���鿴<option value=\"3\">ֻ����������ϼ���鿴</select>\n";
                $tempoutput =~ s/value=\"$viewadminlog\"/value=\"$viewadminlog\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>������־���ܿ��ŷ�ʽ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"regaccess\"><option value=\"off\">���������κ��˷���<option value=\"on\">�ǣ������¼����ܷ���</select>\n";
                $tempoutput =~ s/value=\"$regaccess\"/value=\"$regaccess\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left  colspan=2>
                <font face=���� color=#333333>��ֻ̳��ע���û����Է��ʣ�</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"allowsearch\"><option value=\"no\">������<option value=\"yes\">����</select>\n";
                $tempoutput =~ s/value=\"$allowsearch\"/value=\"$allowsearch\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left  colspan=2>
                <font face=���� color=#333333><B>�Ƿ�������������ֱ�ӷ��ʣ�</B></font><BR>���������ô��ʹ��������ֻ̳��ע���û�<BR>�ſ��Է��ʣ�������������Ȼ�ܹ���������̳<br>��˽�а��������Ա�������û�ͨ����������<br>���ʵ���̳�Ļ��ᣬ���趨Ҳ���ܻ����αװ<br>������������ݵ��û��ķ���!</td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"guestregistered\"><option value=\"on\">����<option value=\"off\">����</select>\n";
		$tempoutput =~ s/value=\"$guestregistered\"/value=\"$guestregistered\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=left  colspan=2>
		<font face=���� color=#333333>�����ܷ�鿴�������ݣ�</font></td>
		<td bgcolor=#FFFFFF valign=middle align=left>
		$tempoutput</td>
		</tr>
		~;
		
                $tempoutput = "<select name=\"pvtip\">\n<option value=\"on\">��ʾ IP �ͼ���\n<option value=\"off\">���� IP �ͼ���\n</select>\n";
                $tempoutput =~ s/value=\"$pvtip\"/value=\"$pvtip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><B>�Ƿ��� IP �ͼ�����</B><BR>��ʹѡ�������ʾ IP������ͨ�û�����<BR>ֻ�ܿ��� IP ��ǰ��λ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput���˹��ܶ�̳����Ч</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"smocanseeip\">\n<option value=\"yes\">��Ч\n<option value=\"no\">��Ч\n</select>\n";
                $tempoutput =~ s/value=\"$smocanseeip\"/value=\"$smocanseeip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>���� IP �ͼ������ܰ����Ƿ���Ч��</B><BR>��ѡ����Ч�����ܰ����ɲ鿴���е� IP<BR>���������� IP ���ܵ�����</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrowupload\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$arrowupload\"/value=\"$arrowupload\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���������Ƿ������ϴ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput���˹��ܶ԰�����̳����Ч</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"allowattachment\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$allowattachment\"/value=\"$allowattachment\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�ظ������Ƿ������ϴ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput���˹��ܶ԰�����̳����Ч</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��̳�ϴ��ļ���������ֵ(��λ��KB)<br>��������˲������ϴ����������Ч��</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxupload" value="$maxupload" size=5 maxlength=5>����Ҫ�� KB�����鲻Ҫ���� 500</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�û��ϴ��ļ�����ﵽ�ķ�������<br>ֻ����ͨע���û���Ч��̳�����������֤�û������ܴ����ƣ�</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="uploadreqire" value="$uploadreqire" size=4 maxlength=4>������������ƣ���������Ϊ0��</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"mastpostatt\">\n<option value=\"no\">���Բ�������\n<option value=\"yes\">���������\n</select>\n";
                $tempoutput =~ s/value=\"$mastpostatt\"/value=\"$mastpostatt\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���������Ƿ�����������</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput���˹�����Ҫ�������� BT ������</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���������ַ�������ֹ��ˮ<br>ֻ����ͨע���û���Ч��̳�����������֤�û������ܴ����ƣ�</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="minpoststr" value="$minpoststr" size=2 maxlength=2>���粻�����ƣ������գ����ö��� 50��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������������ַ���<br>ֻ����ͨע���û���Ч��̳�����������֤�û������ܴ����ƣ�</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpoststr" value="$maxpoststr" size=5 maxlength=5>���粻�����ƣ������գ��������� 100��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>������Ϣ����������ʱ��<br>����ʱ������������޷����Ͷ���Ϣ</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="onlinemessage" value="$onlinemessage" size=8 maxlength=8>����λ���룬�������� 600���粻�����ƣ������ա�</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��������������ʱ��<br>����ʱ������������޷�����</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="onlinepost" value="$onlinepost" size=8 maxlength=8>����λ���룬�������� 600���粻�����ƣ������ա�</td>
                </tr>
                ~;

               $tempoutput = "<select name=\"arrawrecordclick\">\n<option value=\"no\">������\n<option value=\"yes\">����\n</select>";
               $tempoutput =~ s/value=\"$arrawrecordclick\"/value=\"$arrawrecordclick\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font color=#333333>�Ƿ������¼���ӷ������</font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>               
               ~;
               
               $tempoutput = "<select name=\"nowater\">\n<option value=\"off\">������\n<option value=\"on\">����\n</select>";
               $tempoutput =~ s/value=\"$nowater\"/value=\"$nowater\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font color=#333333>�Ƿ��������߶Թ�ˮ��������</font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>               
               
	       <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>���ڶ����ַ����ˮ��</font></b><BR>�������ѡ���������ƣ���ô������Ч��</td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="gsnum" value="$gsnum" size=5 maxlength=5>����Ҫ�� byte�����鲻Ҫ���� 50��</td>
               </tr>      
               ~;

                $tempoutput = "<select name=\"defaulttopicshow\"><option value=>�鿴���е�����<option value=\"1\">�鿴һ���ڵ�����<option value=\"2\">�鿴�����ڵ�����<option value=\"7\">�鿴һ�����ڵ�����<option value=\"15\">�鿴������ڵ�����<option value=\"30\">�鿴һ�����ڵ�����<option value=\"60\">�鿴�������ڵ�����<option value=\"180\">�鿴�����ڵ�����</select>\n";
                $tempoutput =~ s/value=\"$defaulttopicshow\"/value=\"$defaulttopicshow\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ĭ����ʾ������</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"arrowavaupload\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$arrowavaupload\"/value=\"$arrowavaupload\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ������ϴ��Զ���ͷ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrowuserdel\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$arrowuserdel\"/value=\"$arrowuserdel\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ�����ע���û��Լ�������ɾ���Լ������ӣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"usereditpost\"><option value=\"yes\">���Ա༭�Լ�������<option value=\"no\">�����Ա༭�Լ�������</select>\n";
                $tempoutput =~ s/value=\"$usereditpost\"/value=\"$usereditpost\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��̳�Ƿ�����༭��(��̳����������Ч)</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"allowamoedit\">\n<option value=\"no\">������\n<option value=\"yes\">����\n</select>\n";
                $tempoutput =~ s/value=\"$allowamoedit\"/value=\"$allowamoedit\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ�����༭����̳�µ����ӣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"onlineview\">\n<option value=\"1\">��ʾ\n<option value=\"0\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$onlineview\"/value=\"$onlineview\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ĭ���Ƿ���ʾ�����û���ϸ�б�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                
               $tempoutput = "<select name=\"advreg\">\n<option value=\"0\">���ģʽ\n<option value=\"1\">�߼�ģʽ\n</select>\n"; 
               $tempoutput =~ s/value=\"$advreg\"/value=\"$advreg\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>Ĭ��ע��ģʽ��</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
               ~; 

		$tempoutput = "<select name=\"advlogin\">\n<option value=\"0\">���ģʽ\n<option value=\"1\">�߼�ģʽ\n</select>\n"; 
               $tempoutput =~ s/value=\"$advlogin\"/value=\"$advlogin\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>Ĭ�ϵ�¼ģʽ��</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
               ~; 

                $tempoutput = "<select name=\"sendwelcomemessage\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$sendwelcomemessage\"/value=\"$sendwelcomemessage" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ񷢻�ӭ��Ϣ����ע���û���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"refreshforum\">\n<option value=\"off\">��Ҫ�Զ�ˢ��\n<option value=\"on\">Ҫ�Զ�ˢ��\n</select>\n";
                $tempoutput =~ s/value=\"$refreshforum\"/value=\"$refreshforum" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳�Ƿ��Զ�ˢ��(�����������ü��ʱ��)��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Զ�ˢ����̳��ʱ����(��)<BR>����������һ��ʹ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="autofreshtime" value="$autofreshtime" size= 5 maxlength=5>��һ������ 5 ���ӣ����� 300 �롣</td>
                </tr>
		~;

                $tempoutput = "<select name=\"editusertitleself\">\n<option value=\"off\">������\n<option value=\"on\">����\n<option value=\"post\">��������Ҫ�ﵽ����Ļ�����\n</select>\n";
                $tempoutput =~ s/value=\"$editusertitleself\"/value=\"$editusertitleself" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ������û������޸ĸ���ͷ�Σ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		<tr>
		<td bgcolor=#FFFFFF colspan=2>
		<font color=#333333>�����Ա�����޸ĸ���ͷ����Ҫ�ﵽ�Ļ�����</font></td>
		<td bgcolor=#FFFFFF>
		<input type=text name="needpoststitle" value="$needpoststitle" size=5 maxlength=5> �����һ��������ʹ��</td>
		</tr>
		~;

                $tempoutput = "<select name=\"editjhmpself\">\n<option value=\"off\">������\n<option value=\"system\">���������ϵͳ��ѡ��\n<option value=\"on\">����\n<option value=\"post\">��������Ҫ�ﵽ����ķ�����\n</select>\n";
                $tempoutput =~ s/value=\"$editjhmpself\"/value=\"$editjhmpself" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ������û������޸Ľ������ɣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		<tr>
		<td bgcolor=#FFFFFF colspan=2>
		<font color=#333333>�����Ա�����޸Ľ���������Ҫ�ﵽ�ķ�����</font></td>
		<td bgcolor=#FFFFFF>
		<input type=text name="needpostsjhmp" value="$needpostsjhmp" size=5 maxlength=5> �����һ��������ʹ��</td>
		</tr>
		~;

                $tempoutput = "<select name=\"usenoimg\">\n<option value=\"no\">��ʹ��\n<option value=\"yes\">ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$usenoimg\"/value=\"$usenoimg" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ�����ͼƬ����ʱ�Զ�������</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"usefastpost\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$usefastpost\"/value=\"$usefastpost" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ����ÿ��ٷ������⣿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispquickreply\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$dispquickreply\"/value=\"$dispquickreply" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ����ÿ��ٻظ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"waterwhenguest\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$waterwhenguest\"/value=\"$waterwhenguest" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>���������ʱ���Զ���ˮӡ��(ͬʱ���޷���������)</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"sendmanageinfo\">\n<option value=\"no\">��֪ͨ�û�\n<option value=\"yes\">֪ͨ�û�\n</select>\n";
                $tempoutput =~ s/value=\"$sendmanageinfo\"/value=\"$sendmanageinfo" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������ӣ�ɾ�����ƶ������������εȣ���<BR>�Ƿ񷢶���Ϣ֪ͨ�û���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"treeview\">\n<option value=\"no\">ƽ����ʾ����\n<option value=\"yes\">������ʾ����\n</select>\n";
                $tempoutput =~ s/value=\"$treeview\"/value=\"$treeview" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ĭ��������ʾ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispjump\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispjump\"/value=\"$dispjump\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333>�Ƿ���ʾ��̳��ת</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispchildforumnum\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispchildforumnum\"/value=\"$dispchildforumnum\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333>�Ƿ�����ҳ����ʾ����̳����</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispview\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispview\"/value=\"$dispview\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>�Ƿ���ʾ��̳ͼ��</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"addtopictime\">\n<option value=\"no\">�����\n<option value=\"yes\">���\n</select>\n";
                $tempoutput =~ s/value=\"$addtopictime\"/value=\"$addtopictime\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>�Ƿ��Զ�������ǰ������ڣ�</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"abslink\">\n<option value=\"no\">��ֱ������\n<option value=\"yes\">ֱ������\n</select>\n";
                $tempoutput =~ s/value=\"$abslink\"/value=\"$abslink\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>ͼƬ�����Ƿ�ʹ��ֱ�����ط�ʽ��</b>������ֻ���ͼƬ�����ѡ��ֱ�����ء�����ô��������ͼƬˮӡ���ý���Ч��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"pvtdown\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$pvtdown\"/value=\"$pvtdown\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>�Ƿ񱣻��������ص�ַ����ֹ������</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

eval ('use GD;');
if ($@) {
    $gdfunc = 0;
}
else {
    $gdfunc = 1;
}
if ($gdfunc eq "1") {

		$tempoutput = "<select name=\"picwater\">\n<option value=\"no\">����ˮӡ\n<option value=\"yes\">����ˮӡ\n</select>\n";
                $tempoutput =~ s/value=\"$picwater\"/value=\"$picwater\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>�ϴ��� JPG ͼƬ�Ƿ����ˮӡ</b><BR>С�� 200*40 ��ͼƬ�Զ�����ˮӡ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

$watername = "http://bbs.leobbs.com/" if ($watername eq "");

		$tempoutput = "<select name=\"picwaterman\">\n<option value=\"0\">ֻ�Կ�����ʾ\n<option value=\"1\">�Կ��˺���ͨ�û���ʾ\n<option value=\"2\">�Կ��ˡ���ͨ�û�����֤�û���ʾ<option value=\"3\">����̳���⣬�����û�����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$picwaterman\"/value=\"$picwaterman\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��ʾˮӡ����ĸ�������</b><BR>ֻ�д�ˮӡ���ܺ󣬴���Ŀ����Ч</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                if ($picwaterplace1 eq "yes") { $checked1 = "checked" ; } else { $checked1 = "" ; }
                if ($picwaterplace2 eq "yes") { $checked2 = "checked" ; } else { $checked2 = "" ; }
                if ($picwaterplace3 eq "yes") { $checked3 = "checked" ; } else { $checked3 = "" ; }
                if ($picwaterplace4 eq "yes") { $checked4 = "checked" ; } else { $checked4 = "" ; }
		$tempoutput = qq~<input type="checkbox" name="picwaterplace1" value="yes" $checked1> ���Ͻǡ���<input type="checkbox" name="picwaterplace2" value="yes" $checked2> ���½�<BR><input type="checkbox" name="picwaterplace3" value="yes" $checked3> ���Ͻǡ���<input type="checkbox" name="picwaterplace4" value="yes" $checked4> ���½�<BR>~;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>ˮӡ��ʾ��λ��</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
        <tr>
        <td bgcolor=#FFFFFF colspan=2>
        <font color=#333333>ͼƬˮӡ����<BR>ע��ˮӡͼ����Ϊ PNG ��ʽ�����������ʹ������ˮӡ<br>������ͼƬ���ƣ���ͼ������ myimages Ŀ¼��<BR><b>�벻Ҫ���� URL ��ַ�����·����</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=20 name="waterpic" value="$waterpic">
~;

opendir (DIR, "${imagesdir}myimages");
@thd = readdir(DIR);
closedir (DIR);
@thd = grep(/png$/i,@thd);
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
document.FORM.waterpic.value=FORM.image.value;
if (FORM.waterpic.value != "") {
document.bbsimg.src = "$imagesurl/myimages/"+FORM.image.value;
} else {
document.bbsimg.src = "$imagesurl/myimages/blank.gif";
}
}
</script>
<select name="image" onChange=select()><option value="">��ʹ��ͼƬˮӡ$myimages</select><BR>
<IMG border=0 name=bbsimg src="$imagesurl/myimages/blank.gif" align="absmiddle" onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333">
<script>
if (FORM.waterpic.value != "") {
document.bbsimg.src = "$imagesurl/myimages/"+FORM.waterpic.value;
}
</script>

</td>
        </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�ϴ��� JPG ͼƬ��ˮӡ������<BR>ע��<font color=red>����������</font>��Ҳ��Ҫ����������Ӱ��Ч��<BR>�������ͼƬˮӡ���ƴ��ڣ����������Ч</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="watername" value="$watername" size=30></td>
                </tr>
		~;
} else {
	print qq~<input type=hidden name="picwater" value="no">~;
}
		$tempoutput = "<select name=\"wwjf\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$wwjf\"/value=\"$wwjf\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��̳�Ƿ�ʹ�����������ƶ�</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"cansale\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$cansale\"/value=\"$cansale\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳�Ƿ�ʹ�����������ƶ�</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>�������������Ŀ</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="moneymax" value="$moneymax" size=6 maxlength=6> Ĭ�� 99999����� 999999 </td>
               </tr>
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>������������˰��</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="postcess" value="$postcess" size=5 maxlength=5> %</td>
               </tr>
               ~;
		
		$tempoutput = "<select name=\"postjf\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$postjf\"/value=\"$postjf\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��̳�Ƿ�ʹ�÷�������ǩ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"jfmark\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$jfmark\"/value=\"$jfmark\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��̳�Ƿ�ʹ�û��ֲ鿴��ǩ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"noviewjf\">\n<option value=\"no\">���Խ��룬���޷������ܵ�����\n<option value=\"yes\">�޷��������\n</select>\n";
                $tempoutput =~ s/value=\"$noviewjf\"/value=\"$noviewjf\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>���������л��ֱ�ǩ����ô�ﲻ������Ҫ��Ļ�Ա������</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"hidejf\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$hidejf\"/value=\"$hidejf\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��̳�Ƿ�ʹ�ñ������ӱ�ǩ</b>���ظ�����ܿ����������ݣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"usewm\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$usewm\"/value=\"$usewm\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��̳�Ƿ�ʹ���Զ�ˮӡ</b>�����ӱ��⺬ԭ������ʱ�Զ���ˮӡ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"usecurl\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$usecurl\"/value=\"$usecurl\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��̳�Ƿ�����ʹ�ü�������</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
		$tempoutput = "<select name=\"rssinfo\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$rssinfo\"/value=\"$rssinfo\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��̳�Ƿ�����ʹ�� RSS ����</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
		$tempoutput = "<select name=\"magicface\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$magicface\"/value=\"$magicface\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��̳�Ƿ�����ʹ��ħ�����鹦��</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>һ�ν��ͻ����������</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="max1jf" value="$max1jf" size=3 maxlength=3> Ĭ�ϣ� 50</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>������������С������<BR>С�ڴ˻��ֵģ����ܷ�����ע�⣺������ֱ����Ǵ��� 0 �ġ�</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postminjf" value="$postminjf" size=10 maxlength=10>��ע���ð�ǣ�ǰ��Ҫ�пո��粻�����ƣ������ջ��� 0 ��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����ظ�����С������<BR>С�ڴ˻��ֵģ����ܻظ���ע�⣺������ֱ����Ǵ��� 0 �ġ�</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="replyminjf" value="$replyminjf" size=10 maxlength=10>��ע���ð�ǣ�ǰ��Ҫ�пո��粻�����ƣ������ջ��� 0 ��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����ͶƱ����С������<BR>С�ڴ˻��ֵģ����ܷ�ͶƱ����ע�⣺������ֱ����Ǵ��� 0 �ġ�</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="pollminjf" value="$pollminjf" size=10 maxlength=10>��ע���ð�ǣ�ǰ��Ҫ�пո��粻�����ƣ������ջ��� 0 ��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����ͶƱ����С������<BR>С�ڴ˻��ֵģ����ܶ�ͶƱ������ͶƱ��ע�⣺������ֱ����Ǵ��� 0 �ġ�</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="polledminjf" value="$polledminjf" size=10 maxlength=10>��ע���ð�ǣ�ǰ��Ҫ�пո��粻�����ƣ������ջ��� 0 ��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����е�ǩ���Ϸ��������°�Ȩ������<BR>�������Ҫ��������Ϊ�հ�</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcopyright" value="$postcopyright" size=30>��<BR>Ĭ�ϣ���Ȩ���У���������ת��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳����ͼƬ(֧�� Flash) <br>��ͼ������ myimages Ŀ¼�£�ֻ�������ƣ������Լ� URL ��ַ�����·��</font><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="boardlogo" value="$boardlogo"><BR></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳���� Flash ͼƬ��С<BR>(��������ͼƬ�� Flash ʱ��Ч�������� 160*60 ����)<BR></td>
                <td bgcolor=#FFFFFF>
                ��ȣ�<input type=text name="boardlogow" value="$boardlogow" size=3 maxlength=3>�� �߶ȣ�<input type=text name="boardlogoh" value="$boardlogoh" size=3 maxlength=3><BR></td>
                </tr>
               <tr>
               <td bgcolor=#EEEEEE align=center colspan=3>
               <font color=#990000><b><center>�Զ�����֤�û�����(�������Ҫ����ȫ������)</center></b>
               </td></tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա����һ</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrz1" value="$defrz1"></td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա����ͼ��һ</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzonline1" value="$defrzonline1" onChange="definerz1.src='$imagesurl/images/'+this.value"> <img id=definerz1 src=$imagesurl/images/$defrzonline1> ��������� non-cgi/images��</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա�Ŷ�ͼ��һ</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzpic1" value="$defrzpic1" onChange="definerz11.src='$imagesurl/images/'+this.value"> <img id=definerz11 src=$imagesurl/images/$defrzpic1> ��������� non-cgi/images��</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա���ƶ�</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrz2" value="$defrz2"></td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա����ͼ����</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzonline2" value="$defrzonline2" onChange="definerz2.src='$imagesurl/images/'+this.value"> <img id=definerz2 src=$imagesurl/images/$defrzonline2> ��������� non-cgi/images��</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա�Ŷ�ͼ����</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzpic2" value="$defrzpic2" onChange="definerz22.src='$imagesurl/images/'+this.value"> <img id=definerz22 src=$imagesurl/images/$defrzpic2> ��������� non-cgi/images��</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա������</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrz3" value="$defrz3"></td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա����ͼ����</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzonline3" value="$defrzonline3" onChange="definerz3.src='$imagesurl/images/'+this.value"> <img id=definerz3 src=$imagesurl/images/$defrzonline3> ��������� non-cgi/images��</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա�Ŷ�ͼ����</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzpic3" value="$defrzpic3" onChange="definerz33.src='$imagesurl/images/'+this.value"> <img id=definerz33 src=$imagesurl/images/$defrzpic3> ��������� non-cgi/images��</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա������</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrz4" value="$defrz4"></td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա����ͼ����</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzonline4" value="$defrzonline4" onChange="definerz4.src='$imagesurl/images/'+this.value"> <img id=definerz4 src=$imagesurl/images/$defrzonline4> ��������� non-cgi/images��</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա�Ŷ�ͼ����</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzpic4" value="$defrzpic4" onChange="definerz44.src='$imagesurl/images/'+this.value"> <img id=definerz44 src=$imagesurl/images/$defrzpic4> ��������� non-cgi/images��</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա������</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrz5" value="$defrz5"></td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա����ͼ����</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzonline5" value="$defrzonline5" onChange="definerz5.src='$imagesurl/images/'+this.value"> <img id=definerz5 src=$imagesurl/images/$defrzonline5> ��������� non-cgi/images��</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=���� color=#333333><b>��֤��Ա�Ŷ�ͼ����</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzpic5" value="$defrzpic5" onChange="definerz55.src='$imagesurl/images/'+this.value"> <img id=definerz55 src=$imagesurl/images/$defrzpic5> ��������� non-cgi/images��</td>
               </tr>
<tr>
              <td bgcolor=#EEEEEE align=center colspan=3>
              <font color=#990000><b><center>�������Ȩ�޹���</center></b>
              </td></tr>

              <tr>
              <td bgcolor=#FFFFFF>
              <font face=���� color=#333333><b>���������̳�ĳ�Ա��</b><br>�ʺ����а�飬��Ҫ���õ�����飬����롰��̳���ú͹���/����Ӹ������<BR>�������Ҫ������ܣ���ȫ����Ҫѡ��(����ȫ��ѡ��Ч��һ��)��</font></td>
              <td bgcolor=#FFFFFF colspan=2>~;
              my $memteam1 = qq~<input type=checkbox name="yxz" value="rz1">$defrz1(��֤�û�)<br>~ if ($defrz1 ne "");
   my $memteam2 = qq~<input type=checkbox name="yxz" value="rz2">$defrz2(��֤�û�)<br>~ if ($defrz2 ne "");
   my $memteam3 = qq~<input type=checkbox name="yxz" value="rz3">$defrz3(��֤�û�)<br>~ if ($defrz3 ne "");
   my $memteam4 = qq~<input type=checkbox name="yxz" value="rz4">$defrz4(��֤�û�)<br>~ if ($defrz4 ne "");
   my $memteam5 = qq~<input type=checkbox name="yxz" value="rz5">$defrz5(��֤�û�)<br>~ if ($defrz5 ne "");
              $all=qq~<input type=checkbox name="yxz" value="">����<br><input type=checkbox name="yxz" value="me">һ���û�<br>$memteam1$memteam2$memteam3$memteam4$memteam5
<input type=checkbox name="yxz" value="rz">��֤�û�<br>
<input type=checkbox name="yxz" value="banned">��ֹ���û�����<br>
<input type=checkbox name="yxz" value="masked">���δ��û�����<br>
<input type=checkbox name="yxz" value="mo">��̳����<br>
<input type=checkbox name="yxz" value="amo">��̳������<br>
<input type=checkbox name="yxz" value="cmo">����������<br>
<input type=checkbox name="yxz" value="smo">��̳�ܰ���<br>
<input type=checkbox name="yxz" value="ad">̳��<br>~;
              my @yxz = split(/\,/,$yxz);
              foreach(@yxz){
              chomp;
              next if ($_ eq '');
              $all=~s/<input type=checkbox name="yxz" value="$_"/<input type=checkbox name="yxz" value="$_" checked/g;
              }
              print qq~
$all
              </td>
              </tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <input type=submit value="�� ��"></td></form></tr></table></td></tr></table>
                ~;
                }
                }
                else {
                    &adminlogin;
                    }

print qq~</td></tr></table></body></html>~;
exit;
