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
$LBCGI::POST_MAX=50000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
$query = new LBCGI;

require "admin.lib.pl";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "newstyles.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
	$theparam =~ s/\\/\\\\/g;
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/"//g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
        	$_ =~ s/[\n\r]//isg;
        	$theparam =~ s/[\n\r]//isg;
            $printme .= "\$" . "$_ = \'$theparam\'\;\n" if ($_ ne "");
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
            
    if ($action eq "delstyle") {
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>���棡��</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>��ɾ������ѡ��������Ϊ <b>$skinname</b> ����̳��񣬲��ɻָ�<p>
        <p>
        >> <a href="$thisprog?action=delstyleok&skinname=$skinname">ȷ��ɾ��</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
    }
    elsif ($action eq "delstyleok") {
        $filetomake = "$lbdir" . "data/skin/$skinname.cgi";
    	unlink $filetomake;
                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>��ӭ������̳�������� / ���ɾ��</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>������Ϣ�Ѿ�����</b><br>�÷���Ѿ���ȫɾ����
                    </td></tr></table></td></tr></table>
                    ~;

    }

    elsif ($action eq "process") {

        $savename=$query->param('savename');
        if ($savename eq "") {$savename=$query->param('skin')}

        $printme .= "1\;\n";
	$printme =~ s/\$skin.+?\n/\$skin = \"$savename\";\n/isg;

        $filetomake = "$lbdir" . "data/skin/$savename.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳�������� / �������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE colspan=2>
                <font color=#333333><center><b>���������Ѿ��ɹ����棡</b><br><br>
                </center></td></tr></table></td></tr></table>~;
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
                if ($action ne ""){
                $stylefile = "$lbdir" . "data/skin/$action.cgi";
                if (-e $stylefile) {
         	require $stylefile;
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
        $myskin =~ s/value=\"$action\"/value=\"$action\" selected/;
                $inmembername =~ s/\_/ /g;
	$skinname=$query->param('action');
                print qq~
                <tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF>
                <b>��ӭ������̳�������� / �������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#333333><b>�½��趨���</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>����ϵͳ�Դ��ķ��</b><br>��ѡ�����Ҫ��ʽȷ�����ò���Ч</font></td>
                <td bgcolor=#FFFFFF>
                <form action="$thisprog" method="post" name=skin>
                <select name="action">
                <option value="">Ĭ�Ϸ��$myskin
                </select>
                <input type=submit value="�� ��">��<input type=button value="ɾ ��" onclick="location.href='$thisprog?action=delstyle&skinname=$skinname'">
                </form>
                </td></tr>
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                <input type=hidden name="skin" value=$skinname>
<tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>��ɫ����</font></td><td bgcolor=#FFFFFF><input type=text name="cssname" size=10 value="$cssname"></td></tr><tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>��ɫ����</font></td><td bgcolor=#FFFFFF><input type=text name="cssmaker" size=10 value="$cssmaker"></td></tr><tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>��ɫ���</font></td><td bgcolor=#FFFFFF><textarea cols=40 name="cssreadme" rows=2>$cssreadme</textarea>
</td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>��̳BODY��ǩ</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>����������̳���ı�����ɫ���߱���ͼƬ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lbbody" size=40 value="$lbbody"><br>Ĭ�ϣ�bgcolor=#FFFFFF  alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=0</td>
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
                <font color=#333333>�˵�������ͼƬ</font><BR>������ͼƬ���ƣ���ͼ������ myimages Ŀ¼��</td>
                <td background=$imagesurl/myimages/$menubackpic  width=12>��</td>
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
                $tempoutput = "<select name=\"font\">\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"��Բ\">��Բ\n</select><p>\n";
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
                $tempoutput = "<select name=\"posternamefont\">\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"����\">����\n<option value=\"��Բ\">��Բ\n</select><p>\n";
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
                <font color=#333333>�����������ɫ</font></td>
                <td bgcolor=$catback  width=12 id=catback2>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catback" value="$catback" size=7 maxlength=7 onclick="javascript:selcolor(this,catback2)" style="cursor:hand">��Ĭ�ϣ�#ebebFF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>����������ͼƬ</font><BR>������ͼƬ���ƣ���ͼ������ myimages Ŀ¼��</td>
                <td background=$imagesurl/myimages/$catbackpic  width=12>��</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catbackpic" value="$catbackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>���������ͼƬ</font><BR>������ͼƬ���ƣ���ͼ������ myimages Ŀ¼��</td>
                <td background=$imagesurl/myimages/$catsbackpicinfo  width=12>��</td>
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
<b>���Ϊ�������</b> <input type=text name=savename size=16> (�粻��д��Ϊ�޸ĸ���ɫ)<br>
                <input type=submit value="ȷ ��">��<input type=button value="ȡ ��"></td></form></tr></table></td></tr></table>
                ~;
                }
                }
                else {
                    &adminlogin;
                    }
        
print qq~</td></tr></table></body></html>~;
exit;
