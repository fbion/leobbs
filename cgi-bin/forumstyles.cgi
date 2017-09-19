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
require "data/mpic.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "forumstyles.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

@params = $query->param;
foreach $param(@params) {
    $theparam = $query->param($param);

        if (($_ eq 'maintopicad')||($_ eq 'replytopicad')) {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g
	}

    $theparam = &unHTML("$theparam");

        if ($_ eq "footmark" || $_ eq "headmark" || $_ eq "adfoot" || $_ eq "adscript") {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g
	}
    $PARAM{$param} = $theparam;
}

$action      =  $PARAM{'action'};
$inforum     =  $PARAM{'forum'};
$incategory  =  $PARAM{'category'};

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");

if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) { #s1

            my %Mode = (
            'style'               =>    \&styleform,
            'dostyle'             =>    \&dostyle,
            );


    if($Mode{$action}) {
        $Mode{$action}->();
    }
    else {

    if ($action eq "delstyle") {
        print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>��ӭ������̳�������� / ����̳���ɾ��</b>
                    </td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���棡��</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>��ȫɾ���˷���̳�������Զ����񣬲��ɻָ�<p>
        <p>
        >> <a href="$thisprog?action=delstyleok&forum=$inforum">��ʼɾ��</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
    }
    elsif ($action eq "delstyleok") {
        $filetomake = "$lbdir" . "data/style$inforum.cgi";
    	unlink $filetomake;
        $filetomake = "${imagesdir}css/style$inforum.cgi";
    	unlink $filetomake;
                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>��ӭ������̳�������� / ����̳���ɾ��</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>������Ϣ�Ѿ�����</b><br>�˷���̳�ķ���Ѿ���ȫɾ����
                    </td></tr></table></td></tr></table>
                    ~;

    }
    	
   }
}
else {
    &adminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;

##################################################################################

sub styleform {

        if ($incategory ne "main"){
         $filerequire = "$lbdir" . "data/style${inforum}.cgi";
        if (-e $filerequire) {
         	require $filerequire;
                }
        if ($incategory ne ""){
        $stylefile = "$lbdir" . "data/skin/$incategory.cgi";
                if (-e $stylefile) {
         	require $stylefile;
        }
        }
        }


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

&getoneforum("$inforum");

	$footmark   =~ s/\[br\]/\n/isg;
	$headmark   =~ s/\[br\]/\n/isg;
	$adfoot   =~ s/\[br\]/\n/isg;
	$adscript   =~ s/\[br\]/\n/isg;
	$maintopicad   =~ s/\[br\]/\n/isg;
	$replytopicad   =~ s/\[br\]/\n/isg;

print qq~
        <tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF>
        <b>��ӭ������̳�������� / �༭����̳Ƥ�����</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=3>
        <font color=#000000><b>�༭ $forumname �ķ���̳Ƥ�����,<Br>����㲻����ģ�������ѡ�����д������</b>
        </td></tr>
        <tr><td bgcolor=#FFFFFF align=center colspan=3><font color=#ffffff>LeoBBS</font></td></tr>

        <tr>
        <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳���ѡ��</b>
                </font></td>
                </tr>

        <form name=MAINFORM action="$thisprog" method="post">
        <input type=hidden name="action" value="dostyle">
        <input type=hidden name="forum" value="$inforum">
        <input type=hidden name="skin" value="$skin" size=10 maxlength=10>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>ϵͳ�Դ���Ƥ�����</b><br>��ѡ�����Ҫ��ʽȷ���ύ����Ч</font></td>
                <td bgcolor=#FFFFFF>
                <select name="skinselected">
                <option value="">Ĭ�Ϸ��$myskin
                </select>
                </td></tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳״̬����</b>
                </font></td>
                </tr>
                ~;
                $tempoutput1 = "<select name=\"mainonoff\">\n<option value=\"0\">��̳����\n<option value=\"1\">��̳�ر�\n<option value=\"2\">�Զ����ڿ���\n</select>\n";
                $tempoutput1 =~ s/value=\"$mainonoff\"/value=\"$mainonoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font face=���� color=#333333 ><b>��̳״̬</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput1</td>
                </tr>
                ~;
	$tempoutput1 = "<select name=\"mainauto1\">\n<option value=\"day\">ÿ��\n<option value=\"week\">ÿ����\n<option value=\"month\">ÿ��\n</select>\n";
	$tempoutput1 =~ s/value=\"$mainauto1\"/value=\"$mainauto1\" selected/;
	print qq~
              <tr>
              <td bgcolor=#FFFFFF width=40% colspan=2>
              <font face=���� color=#333333 ><b>�Զ�������̳��</b><br>(ֻ��ѡ���Զ����ڿ��Ŵ�����Ч)</font></td>
              <td bgcolor=#FFFFFF>
              $tempoutput1 <input name=mainautovalue1 value="$mainautovalue1" size=8><br>ע: ����ʹ�õ�һ���ֻ��Ƿ�Χ����ÿ��6, ÿ��0-6, ÿ����6, ÿ��10-15</td>
              </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font face=���� color=#333333 ><b>ά��˵��</b> (֧�� HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <textarea name="line1" cols="40">$line1</textarea><BR><BR></td>
                </tr>
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

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333>����������̳���ı�����ɫ���߱���ͼƬ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lbbody" size=40 value="$lbbody"><br>Ĭ�ϣ�bgcolor=#FFFFFF  alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=0</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>��ҳ��ַ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="homeurl" value="$homeurl"></td>
                </tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b>��̳ҳü��ҳ��</b>
</font></td>
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
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ���ʾԭ��ҳü</font></td>
                <td bgcolor=#FFFFFF>
		~;
                $tempoutput = "<select name=\"usetopm\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select><p>\n";
                $tempoutput =~ s/value=\"$usetopm\"/value=\"$usetopm\" selected/;
                print qq~
                $tempoutput</td>
		</tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b>��̳ҳ�ײ˵�</b>
</font></td>
</tr>
<script>
function selcolor(obj,obj2){
var arr = showModalDialog("$imagesurl/editor/selcolor.html", "", "dialogWidth:18.5em; dialogHeight:17.5em; status:0");
obj.value=arr;
obj2.style.backgroundColor=arr;
}
</script>
<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>�˵���������ɫ</font></td>
<td bgcolor=$menufontcolor  width=12 id=menufontcolor2>��</td>
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
<td background=$imagesurl/images/$skin/$menubackpic  width=12>��</td>
<td bgcolor=#FFFFFF>
<input type=text name="menubackpic" value="$menubackpic"></td>
</tr>

<tr>
<td bgcolor=#FFFFFF width=40%>
<font color=#333333>�˵����߽���ɫ</font></td>
<td bgcolor=$titleborder  width=12 id=titleborder2>��</td>
<td bgcolor=#FFFFFF>
<input type=text name="titleborder" value="$titleborder" size=7 maxlength=7 onclick="javascript:selcolor(this,titleborder2)" style="cursor:hand">��Ĭ�ϣ�#333333</td>
</tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b>������ۺ���ɫ</b>
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
<td bgcolor=$lastpostfontcolor  width=12 id=lastpostfontcolor2>��</td>
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
		<font color=#333333>һ���û������ϵĹ�����ɫ</font></td>
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
		<font color=#333333>̳�������ϵĹ�����ɫ</font></td>
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
		<font color=#333333>�ܰ��������ϵĹ�����ɫ</font></td>
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
		<font color=#333333>���������������ϵĹ�����ɫ</font></td>
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
		<font color=#333333>���˺ͽ����û������ϵĹ�����ɫ</font></td>
		<td bgcolor=$banglow  width=12 id=banglow2>��</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="banglow" value="$banglow" size=7 maxlength=7 onclick="javascript:selcolor(this,banglow2)" style="cursor:hand">��Ĭ�ϣ�none</td>
		</tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b><center>����ҳ����ɫ</center></b><br>
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
<font color=#990000><b><center>�����ɫ</center></b><br>
<font color=#333333>��Щ��ɫ�󲿷�����leobbs.cgi��forums.cgi��topic.cgi
</td></tr>

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
<font color=#990000><b><center>������ɫ</center></b><br>
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
                <font color=#333333>����������ͼƬ</font><BR>������ͼƬ���ƣ���ͼ������ images Ŀ¼�µ� $skin ��</td>
                <td background=$imagesurl/images/$skin/$catbackpic  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catbackpic" value="$catbackpic"></td>
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
<font color=#990000><b><center>��̳������ɫ</center></b><br>
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
<font color=#990000><b><center>�ظ���ɫ</center></b><br>
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
               ~; 

                $tempoutput = "<select name=\"arrawpostpic\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostpic\"/value=\"$arrawpostpic\" selected/;
                print qq~
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>LeoBBS ��ǩ����</center></b>(̳���Ͱ������ܴ���)<br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ�������ͼ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostflash\"><option value=\"off\">������<option value=\"on\" >����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostflash\"/value=\"$arrawpostflash\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ����� Flash��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
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

	            $tempoutput = "<select name=\"arrawpostsound\"><option value=\"off\">������<option value=\"on\" >����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostsound\"/value=\"$arrawpostsound\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ����������ļ���</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		        </td>
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

                $tempoutput = "<select name=\"arrawpostfontsize\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$arrawpostfontsize\"/value=\"$arrawpostfontsize\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������Ƿ�����ı����ִ�С��</font></td>
                <td bgcolor=#FFFFFF>
                 $tempoutput
		         </td>
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
                
		$tempoutput = "<select name=\"arrawsignpic\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$arrawsignpic\"/value=\"$arrawsignpic\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ�������ͼ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;
		$tempoutput = "<select name=\"arrawsignflash\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$arrawsignflash\"/value=\"$arrawsignflash\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ����� Flash��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;


		$tempoutput = "<select name=\"arrawsignsound\"><option value=\"off\">������<option value=\"on\">����</select>\n";
                $tempoutput =~ s/value=\"$arrawsignsound\"/value=\"$arrawsignsound\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ǩ�����Ƿ�����������</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"arrawsignfontsize\"><option value=\"off\">������<option value=\"on\">����</select>\n";
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
                $tempoutput = qq~<select name=sltnoperline><option value="1">1</option><option value="2>2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option></select>~;
                $tempoutput =~ s/value=\"$sltnoperline\"/value=\"$sltnoperline\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>

		<tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳��ť����</b> (Ĭ�ϴ�ͼ������ images/$skin Ŀ¼�£�ֻ�������ƣ������Լ� URL ��ַ�����·��)<br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��������ťͼ��</font>��(��С��99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newthreadlogo" value="$newthreadlogo" onblur="document.images.i_newthreadlogo.src='$imagesurl/images/$skin/'+this.value;">��
                <img src=$imagesurl/images/$skin/$newthreadlogo name="i_newthreadlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����ͶƱ��ťͼ��</font>��(��С��99*25)</td>
                <td bgcolor=#FFFFFF>
		<input type=text name="newpolllogo" value="$newpolllogo" onblur="document.images.i_newpolllogo.src='$imagesurl/images/$skin/'+this.value;">��
                <img src=$imagesurl/images/$skin/$newpolllogo name="i_newpolllogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>С�ֱ���ťͼ��</font>��(��С��99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newxzblogo" value="$newxzblogo" onblur="document.images.i_newxzblogo.src='$imagesurl/images/$skin/'+this.value;">��
                <img src=$imagesurl/images/$skin/$newxzblogo name="i_newxzblogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�ظ����Ӱ�ťͼ��</font>��(��С��99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newreplylogo" value="$newreplylogo" onblur="document.images.i_newreplylogo.src='$imagesurl/images/$skin/'+this.value;">��
                <img src=$imagesurl/images/$skin/$newreplylogo name="i_newreplylogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ԭ���ڰ�ťͼ��</font>��(��С��74*21)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="wlogo" value="$wlogo" onblur="document.images.i_wlogo.src='$imagesurl/images/$skin/'+this.value;">��
                <img src=$imagesurl/images/$skin/$wlogo name="i_wlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�´��ڰ�ťͼ��</font>��(��С��74*21)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="nwlogo" value="$nwlogo" onblur="document.images.i_nwlogo.src='$imagesurl/images/$skin/'+this.value;">��
                <img src=$imagesurl/images/$skin/$nwlogo name="i_nwlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>������ťͼ��</font>��(��С������)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="help_blogo" value="$help_blogo" onblur="document.images.i_help_blogo.src='$imagesurl/images/$skin/'+this.value;">��
                <img src=$imagesurl/images/$skin/$help_blogo name="i_help_blogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�������� new ͼ��</font>��(��С������)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="new_blogo" value="$new_blogo" onblur="document.images.i_new_blogo.src='$imagesurl/images/$skin/'+this.value;">��
                <img src=$imagesurl/images/$skin/$new_blogo name="i_new_blogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Լ��Ƿ����˵ı��ͼʾ</font>��(��С������)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="mypost_blogo" value="$mypost_blogo" onblur="document.images.i_new_mypost.src='$imagesurl/images/$skin/'+this.value;">��
                <img src=$imagesurl/images/$skin/$mypost_blogo name="i_new_mypost"></td>
                </tr>
				
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>�������ӵı��ͼʾ</font>  (��С������)</td> 
               <td bgcolor=#FFFFFF> 
               <input type=text name="new_JH" value="$new_JH" onblur="document.images.i_new_JH.src='$imagesurl/images/$skin/'+this.value;">��
               <img src=$imagesurl/images/$skin/$new_JH name="i_new_JH"></td> 
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
		~;
               
               $tempoutput = "<select name=\"dispabstop\">\n<option value=\"1\">��ʾ\n<option value=\"0\">����ʾ\n</select>\n"; 
               $tempoutput =~ s/value=\"$dispabstop\"/value=\"$dispabstop\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=���� color=#333333><b>�Ƿ�������ʾ�̶ܹ���</b></font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
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
		~;
               
               $tempoutput = "<select name=\"dispcattop\">\n<option value=\"1\">��ʾ\n<option value=\"0\">����ʾ\n</select>\n"; 
               $tempoutput =~ s/value=\"$dispcattop\"/value=\"$dispcattop\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=���� color=#333333><b>�Ƿ�������ʾ���̶���</b></font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
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
                <font color=#333333>����̶��ڶ��˵���������</font></td>
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
                <font color=#333333>��̳ͶƱ����������������Ŀ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpollitem" value="$maxpollitem" size=2 maxlength=2>�������� 5 - 50 ֮��</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emoticons\">\n<option value=\"off\">��ʹ��\n<option value=\"on\">ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$emoticons\"/value=\"$emoticons\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>�Ƿ�ʹ�ñ����ַ�ת����</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"canchgfont\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$canchgfont\"/value=\"$canchgfont\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>�Ƿ�ʹ����������ת����</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>�������</center></b><br>
                </td></tr>
		~;
	$adscript   =~ s/\[br\]/\n/isg;
	$adfoot   =~ s/\[br\]/\n/isg;

               $tempoutput = "<select name=\"useadscript\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useadscript\"/value=\"$useadscript\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=���� color=#333333><b>�Ƿ�ʹ����̳���</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                    
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��̳�����д</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adscript" rows="5" cols="40">$adscript</textarea>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"useadfoot\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useadfoot\"/value=\"$useadfoot\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=���� color=#333333><b>�Ƿ�ʹ����̳β������</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��̳β��������д</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adfoot" rows="5" cols="40">$adfoot</textarea><BR><BR>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"forumimagead\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
               $tempoutput =~ s/value=\"$forumimagead\"/value=\"$forumimagead\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>�Ƿ�ʹ�÷���̳�������</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳�������ͼƬ URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage" value="$adimage"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳�����������Ŀ����ַ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink" value="$adimagelink"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳�������ͼƬ���</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth" value="$adimagewidth" maxlength=3>&nbsp;����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳�������ͼƬ�߶�</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight" value="$adimageheight" maxlength=3>&nbsp;����</td>
                </tr>
                ~;

               $tempoutput = "<select name=\"useimageadtopic\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
               $tempoutput =~ s/value=\"$useimageadtopic\"/value=\"$useimageadtopic\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>�鿴�˷���̳������ʱ�Ƿ�<BR>ʹ�ô˸������</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput�������������<BR>����̳��ʹ�ø������Ļ�����ѡ����Ч<BR><BR></td>
               </tr>
		~;
        
               $tempoutput = "<select name=\"forumimagead1\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
               $tempoutput =~ s/value=\"$forumimagead1\"/value=\"$forumimagead1\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>�Ƿ�ʹ�÷���̳���¹̶����</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳���¹̶����ͼƬ URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage1" value="$adimage1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳���¹̶��������Ŀ����ַ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink1" value="$adimagelink1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳���¹̶����ͼƬ���</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth1" value="$adimagewidth1" maxlength=3>&nbsp;����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳���¹̶����ͼƬ�߶�</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight1" value="$adimageheight1" maxlength=3>&nbsp;����</td>
                </tr>
                ~;

               $tempoutput = "<select name=\"useimageadtopic1\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
               $tempoutput =~ s/value=\"$useimageadtopic1\"/value=\"$useimageadtopic1\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>�鿴�˷���̳������ʱ�Ƿ�<BR>ʹ�ô����¹̶����</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput�������������<BR>����̳��ʹ�����¹̶����Ļ�����ѡ����Ч</td>
               </tr>

		<tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>���������</b><br>�� HTML �﷨��д��</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="topicad" cols="40" rows="10">$topicad</textarea><BR>
                </td>
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
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>��Ȩ��Ϣ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="copyrightinfo" value="$copyrightinfo"></td>
                </tr>
                 ~;

                $tempoutput = "<select name=\"floodcontrol\"><option value=\"off\">��<option value=\"on\">��</select>\n";
                $tempoutput =~ s/value=\"$floodcontrol\"/value=\"$floodcontrol\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>�Ƿ��ˮԤ�����ƣ�</b><br>ǿ���Ƽ�ʹ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>�û����������ʱ��</b><br>��ˮԤ�����Ʋ���Ӱ�쵽̳�������</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="floodcontrollimit" value="$floodcontrollimit" size=3 maxlength=3></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
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

		$tempoutput = "<select name=\"nodispown\">\n<option value=\"no\">����ʾ\n<option value=\"yes\">��ʾ\n</select>\n"; 
               $tempoutput =~ s/value=\"$nodispown\"/value=\"$nodispown\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>�Ƿ��־��ʾ�Լ��������ӣ�</font></td> 
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

               $tempoutput = "<select name=\"useads\">\n<option value=\"no\">������\n<option value=\"yes\">����\n</select>\n"; 
               $tempoutput =~ s/value=\"$useads\"/value=\"$useads\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>�Ƿ�������̳���������棿</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
		~;
		
                $tempoutput = "<select name=\"look\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$look\"/value=\"$look\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ񿪷ű�����ɫ���ܣ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"wwjf\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$wwjf\"/value=\"$wwjf\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>����̳�Ƿ�ʹ�����������ƶ�</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
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
               <font face=���� color=#333333><b>������������˰��</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="postcess" value="$postcess" size=5 maxlength=5> %  : ������ 1 - 100 ֮�䣬����ʹ�������ÿհ�</td>
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
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=���� color=#333333><b>һ�ν��ͻ����������</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="max1jf" value="$max1jf" size=3 maxlength=3> Ĭ�ϣ� 50</td>
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
		
		$tempoutput = "<select name=\"magicface\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$magicface\"/value=\"$magicface\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>��̳�Ƿ�����ʹ��ħ�����鹦��</b></font></td>
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

                $tempoutput = "<select name=\"announcements\"><option value=\"no\">��ʹ��<option value=\"yes\">ʹ��</select>\n";
                $tempoutput =~ s/value=\"$announcements\"/value=\"$announcements\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>�Ƿ�ʹ�ù�����̳</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;

		$tempoutput = "<select name=\"refreshurl\"><option value=\"0\">�Զ����ص�ǰ��̳<option value=\"1\">�Զ����ص�ǰ����</select>\n";
                $tempoutput =~ s/value=\"$refreshurl\"/value=\"$refreshurl\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>�����ظ����༭���Ӻ��Զ�ת�Ƶ���</b></font></td>
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

                $tempoutput = "<select name=\"postopen\"><option value=\"yes\">���Է����ظ�����<option value=\"no\">���������ظ�����</select>\n";
                $tempoutput =~ s/value=\"$postopen\"/value=\"$postopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����̳�����ظ����⹦�ܣ�</font></td>
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

                $tempoutput = "<select name=\"useemote\"><option value=\"yes\">ʹ��<option value=\"no\">��ʹ��</select>\n";
                $tempoutput =~ s/value=\"$useemote\"/value=\"$useemote\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ�ʹ�� EMOTE ��ǩ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"regaccess\"><option value=\"off\">���������κ��˷���<option value=\"on\">�ǣ������¼����ܷ���</select>\n";
                $tempoutput =~ s/value=\"$regaccess\"/value=\"$regaccess\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>��ֻ̳��ע���û����Է��ʣ�</font></td>
                <td bgcolor=#FFFFFF>
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

                $tempoutput = "<select name=\"arrowuserdel\">\n<option value=\"on\">����\n<option value=\"off\">������\n</select>\n";
                $tempoutput =~ s/value=\"$arrowuserdel\"/value=\"$arrowuserdel\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Ƿ�����ע���û��Լ�ɾ���Լ������ӣ�</font></td>
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

                $tempoutput = "<select name=\"pvtip\">\n<option value=\"on\">��ʾ IP �ͼ���\n<option value=\"off\">���� IP �ͼ���\n</select>\n";
                $tempoutput =~ s/value=\"$pvtip\"/value=\"$pvtip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>�Ƿ��� IP �ͼ�����</b><BR>��ʹѡ�������ʾ IP������ͨ�û�����<BR>ֻ�ܿ��� IP ��ǰ��λ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput���˹��ܶ�̳����Ч</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"smocanseeip\">\n<option value=\"yes\">��Ч\n<option value=\"no\">��Ч\n</select>\n";
                $tempoutput =~ s/value=\"$smocanseeip\"/value=\"$smocanseeip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>���� IP �ͼ������ܰ����Ƿ���Ч��</b><BR>��ѡ����Ч�����ܰ����ɲ鿴���е� IP<BR>���������� IP ���ܵ�����</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>֧���ϴ��ĸ�������</b><br>��,�ָ�</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="addtype" value="$addtype"></td>
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
                <input type=text name="maxupload" value="$maxupload" size=5 maxlength=5>����Ҫ�� KB ���������鲻Ҫ���� 500 ��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�û��ϴ��ļ�����ﵽ�ķ�������<br>ֻ����ͨע���û���Ч��̳�����������֤�û������ܴ����ƣ�</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="uploadreqire" value="$uploadreqire" size=4 maxlength=4>������������ƣ���������Ϊ0��</td>
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
                <font color=#333333>�ϴ��� JPG ͼƬ��ˮӡ������<BR>ע��<font color=red>����������</font>��Ҳ��Ҫ����������Ӱ��Ч��</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="watername" value="$watername" size=30></td>
                </tr>
		~;
} else {
	print qq~<input type=hidden name="picwater" value="no">~;
}

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
                <font color=#333333>��������������ʱ��<br>����ʱ������������޷�����</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="onlinepost" value="$onlinepost" size=8 maxlength=8>����λ���룬�������� 600���粻�����ƣ������ջ��� 0��</td>
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

                $tempoutput = "<select name=\"dispguest\">\n<option value=\"1\">��ϵͳ���ɶ���\n<option value=\"2\">��Զ��ʾ\n<option value=\"3\">��Զ����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispguest\"/value=\"$dispguest\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>�����б����Ƿ���ʾ���ˣ�</b></font></td>
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

                $tempoutput = "<select name=\"dispview\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispview\"/value=\"$dispview\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=���� color=#333333><b>�Ƿ���ʾ��̳ͼ��</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�����е�ǩ���Ϸ��������°�Ȩ������<BR>�������Ҫ��������Ϊ�հ�</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcopyright" value="$postcopyright" size=30>��<BR>Ĭ�ϣ���Ȩ���У���������ת��</td>
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

                $tempoutput = "<select name=\"refreshforum\">\n<option value=\"off\">��Ҫ�Զ�ˢ��\n<option value=\"on\">Ҫ�Զ�ˢ��\n</select>\n";
                $tempoutput =~ s/value=\"$refreshforum\"/value=\"$refreshforum" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>������̳�Ƿ��Զ�ˢ��(�����������ü��ʱ��)��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>�Զ�ˢ����̳��ʱ����(��)<BR>����������һ��ʹ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="autofreshtime" value="$autofreshtime" size= 5 maxlength=4>��һ������ 5 ���ӣ����� 300 �롣</td>
                </tr>
		<tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>���淢�����ӵ��������� (������ʹ������Ĭ�ϣ����ѡ���˱��淢���������������Ч)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumpostmoney" value="$forumpostmoney" size= 8 maxlength=7></td>
             </tr>

             <tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>����������ӵ��������� (������ʹ������Ĭ�ϣ����ѡ���˱��淢���������������Ч)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumreplymoney" value="$forumreplymoney" size= 8 maxlength=7></td>
             </tr>

             <tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>���汻ɾ����ȥ���������� (������ʹ������Ĭ�ϣ����ѡ���˱���ɾ���������������Ч)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumdelmoney" value="$forumdelmoney" size= 8 maxlength=7></td>
             </tr>
		<tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>���淢�����ӵĻ��� (������ʹ������Ĭ�ϣ����ѡ���˱��淢���������������Ч)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumpostjf" value="$forumpostjf" size= 8 maxlength=7></td>
             </tr>

             <tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>����������ӵĻ��� (������ʹ������Ĭ�ϣ����ѡ���˱��淢���������������Ч)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumreplyjf" value="$forumreplyjf" size= 8 maxlength=7></td>
             </tr>

             <tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>���汻ɾ����ȥ�Ļ��� (������ʹ������Ĭ�ϣ����ѡ���˱���ɾ���������������Ч)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumdeljf" value="$forumdeljf" size= 8 maxlength=7></td>
             </tr>
<script>
function AddAllow()
{
	if (name = prompt("������Ҫ��ӵ�ֻ���������û���ID��", ""))
	{
		if (MAINFORM.allowusers.innerText) MAINFORM.allowusers.innerText += "," + name;
		else MAINFORM.allowusers.innerText = name;
	}
}
function DeleteAllow()
{
	if (name = prompt("������Ҫȥ����ֻ���������û���ID��", ""))
	{
var myString = new String("," + window.MAINform.allowusers.innerText + ",");
var replaceString = eval("myString.replace(/," + name + ",/ig, ',')");
window.MAINform.allowusers.innerText = replaceString.substr(1, replaceString.length - 2);
	}
}
function ClearAllow()
{
	if (confirm("��ȷ��Ҫ�������ֻ���������û�ID��"))
		MAINFORM.allowusers.innerText = "";
}
</script>
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font color=#333333><b>ֻ���������û����뱾����</b><BR>���ϣ����ȫ�忪�ţ��벻Ҫ��д<BR>���κ��û�����Ч�ģ���������Ա</font></td>
               <td bgcolor=#FFFFFF>
               <textarea name="allowusers" rows=6 cols=40 readonly=true>$allowusers</textarea><br><input type=button value=��� OnClick="AddAllow();">��<input type=button value=ɾ�� OnClick="DeleteAllow();">��<input type=button value=��� OnClick="ClearAllow();"></td>
               </tr>~;

		$tempoutput = "<select name=\"forumallowcount\">\n<option value=\"yes\">���뷢����\n<option value=\"no\">�����뷢����\n</select>\n";
              	$tempoutput =~ s/value=\"$forumallowcount\"/value=\"$forumallowcount" selected/;

		print qq~
		<tr>
              	<td bgcolor=#FFFFFF colspan=2>
              	<font color=#333333>���淢���Ƿ�������߷�����</font></td>
              	<td bgcolor=#FFFFFF>
              	$tempoutput</td>
              	</tr>
		~;

		$tempoutput = "<select name=\"forumreplyallowcount\">\n<option value=\"yes\">����ظ���\n<option value=\"no\">������ظ���\n</select>\n";
              	$tempoutput =~ s/value=\"$forumreplyallowcount\"/value=\"$forumreplyallowcount" selected/;

		print qq~
		<tr>
              	<td bgcolor=#FFFFFF colspan=2>
              	<font color=#333333>����ظ��Ƿ�������߻ظ���</font></td>
              	<td bgcolor=#FFFFFF>
              	$tempoutput</td>
              	</tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>������̳����С������<BR>С�ڴ������ģ����ܽ��룬ע�⣺������ֱ����Ǵ��� 0 �ġ�</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="enterminweiwang" value="$enterminweiwang" size=3 maxlength=3>��ע���ð�ǣ�ǰ��Ҫ�пո��粻�����ƣ������ջ��� 0 ��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>������̳����С��Ǯ��<BR>С�ڴ˽�Ǯ�ģ����ܽ��룬ע�⣺������ֱ����Ǵ��� 0 �ġ�</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="enterminmony" value="$enterminmony" size=10 maxlength=10>��ע���ð�ǣ�ǰ��Ҫ�пո��粻�����ƣ������ջ��� 0��</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>������̳����С������<BR>С�ڴ˻��ֵģ����ܽ��룬ע�⣺������ֱ����Ǵ��� 0 �ġ�</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="enterminjf" value="$enterminjf" size=10 maxlength=10>��ע���ð�ǣ�ǰ��Ҫ�пո��粻�����ƣ������ջ��� 0��</td>
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
                <font color=#333333><b>����̳������������</b>(���û��������)<br>�����뱳���������ƣ���������<BR>Ӧ�ϴ��� non-cgi/midi Ŀ¼�¡�<br><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=20 name="midiaddr" value="$midiaddr">~;
                $midiabsaddr = "$imagesdir" . "midi/$midiaddr";
                print qq~��<EMBED src="$imagesurl/midi/$midiaddr" autostart="false" width=70 height=25 loop="true" align=absmiddle>~ if ((-e "$midiabsaddr")&&($midiaddr ne ""));
                print qq~
                </td>
<tr>
              <td bgcolor=#EEEEEE align=center colspan=3>
              <font color=#990000><b><center>�������Ȩ�޹���</center></b>
              </td></tr>

              <tr>
              <td bgcolor=#FFFFFF>
              <font face=���� color=#333333><b>���������̳�ĳ�Ա��</b><br>�������Ҫ������ܣ���ȫ����Ҫѡ��(����ȫ��ѡ��Ч��һ��)��</font></td>
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
                </tr>
                <td bgcolor=#FFFFFF align=center colspan=3>
                <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
                ~;

}

sub dostyle {
    $filerequire = "$lbdir" . "data/style${inforum}.cgi";
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

        if ($_ eq "footmark" || $_ eq "headmark" || $_ eq "adfoot" || $_ eq "adscript") {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g;
	}


	${$_} = $theparam;
	
        if (($_ ne 'action')&&($_ ne 'forum')&&($_ ne 'yxz')&&($theparam ne "")) {
        	$_ =~ s/[\a\f\n\e\0\r]//isg;
        	$theparam =~ s/[\a\f\n\e\0\r]//isg;
            $printme .= "\$" . "$_ = \"$theparam\"\;\n" if (($_ ne "")&&($theparam ne ""));
        }
    }
    $endprint = "1\;\n";
    open(FILE,">$filerequire");

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
    print FILE $endprint;
    close(FILE);

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata1 = grep(/^forumstoptopic$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumshead$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumstitle$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumstopic$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^plcache$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }

    if (-e $filerequire && -w $filerequire) {
        print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>��ӭ������̳�������� / ����̳����趨</b></td></tr>
<tr><td bgcolor=#EEEEEE colspan=2><font color=#333333><center><b>������Ϣ�Ѿ��ɹ�����</b><br><br>
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
        print $printme;
        print qq~</td></tr></table></td></tr></table>~;
    }
    else {
	print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>��ӭ������̳�������� / ����̳����趨</b></td></tr>
<tr><td bgcolor=#EEEEEE align=center colspan=2>
<font color=#333333><b>������Ϣû�б���</b><br>�ļ�����Ŀ¼����д<br>������� data Ŀ¼�� styles*.cgi �ļ������ԣ�
</td></tr></table></td></tr></table>
~;
    }
}
