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
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "misc.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$UIN     = $query -> param('UIN');
$UIN     = &cleaninput("$UIN");
$UIN =~ s/[^0-9]//isg;
$action  = $query -> param('action');
$action  = &cleaninput("$action");

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("��ͨ����&�ϴ󣬱��Һ��ҵĳ���ѽ��") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "����" ) { $inmembername = "����"; }
if ($action eq "showsmilies") {
    $output = qq~ 
<p>
<SCRIPT>valigntop()</SCRIPT>
    <table width=$tablewidth cellpadding=0 cellspacing=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <table width=100% cellpadding=5 cellspacing=1>
            <tr>
                <td bgcolor=$miscbackone $catbackpic align=center colspan=2>
                    <font color=$titlefontcolor><b>$boardname - ����ת��</b></font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbacktwo align=center>
                    <font color="$fontcolormisc">����</font>
                </td>
                    <td bgcolor=$miscbacktwo align=center>
                    <font color=$fontcolormisc>ת����</font>
                </td>
                </tr>
    ~;
    
        open (FILE, "$lbdir/data/lbemot.cgi");
	my @emoticondata = <FILE>;
	close (FILE);
	chomp @emoticondata;
        
    foreach $picture (@emoticondata) {
	$smileyname = $picture;
	$smileyname =~ s/\.gif//g;
	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone align=center>
	<font color=$fontcolormisc>:$smileyname:</font>
	</td>
	<td bgcolor=$miscbackone align=center>
	<img src=$imagesurl/emot/$picture>
	</td>
	</tr>
	~;
    }
    $output .= qq~
	</table>
	</td></tr>
	</table><SCRIPT>valignend()</SCRIPT>
	</body>
	</html>
    ~;
}
elsif ($action eq "showmagicface") {
    $CountLength = 0;
    opendir(DIR,"$imagesdir/MagicFace/gif/");
    @files = readdir(DIR);
    closedir(DIR);
    @numbers = grep(/\.gif$/i,@files);
    $CountLength = @numbers;
    
    $output = qq~ 
<script>
function MM_showHideLayers() {
	var i,p,v,obj,args=MM_showHideLayers.arguments;
	obj=document.getElementById("MagicFace");
	for (i=0; i<(args.length-2); i+=3) if (obj) { v=args[i+2];if (obj.style) { obj=obj.style; v=(v=='show')?'visible':(v=='hide')?'hidden':v; }obj.visibility=v; }
}
function ShowMagicFace(MagicID){var MagicFaceUrl = "$imagesurl/MagicFace/swf/" + MagicID + ".swf";document.getElementById("MagicFace").innerHTML = '<object codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,29,0" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="500" height="350"><param name="movie" value="'+ MagicFaceUrl +'"><param name="menu" value="false"><param name="quality" value="high"><param name="play" value="false"><param name="wmode" value="transparent"><embed src="' + MagicFaceUrl +'" wmode="transparent" quality="high" pluginspage="http://www.macromedia.com/go/getflashplayer" type="application/x-shockwave-flash" width="500" height="350"></embed></object>';document.getElementById("MagicFace").style.top = (document.body.scrollTop+((document.body.clientHeight-300)/2))+"px";document.getElementById("MagicFace").style.left = (document.body.scrollLeft+((document.body.clientWidth-480)/2))+"px";document.getElementById("MagicFace").style.visibility = 'visible';MagicID += Math.random();setTimeout("MM_showHideLayers('MagicFace','','hidden')",8000);var NowMeID = MagicID;}
function ShowForum_Emot(page){
	var CountLength = $CountLength;
	var page_size = 25
	var showlist = ''
	var pagelist = ''
	var Page_Max = CountLength/page_size
	if ((CountLength % page_size)>0)Page_Max = Math.floor(Page_Max+1);
	for (i=page*page_size-page_size+1;i<=page*page_size;i++)
	{
		Audibles_ID = i;
		Audibles_Url = "$imagesurl/MagicFace/gif/"+Audibles_ID + ".gif";
		if (i<=CountLength)
		{
			showlist = showlist + '<tr><td width=33% align=center bgcolor=$miscbackone>��'+i+'������</td><td width=34% bgcolor=$miscbackone align=center><img src="'+ Audibles_Url +'" onclick="ShowMagicFace('+Audibles_ID+');"  style="cursor:hand;"></td>'
			showlist = showlist + '<td width=33% align=center bgcolor=$miscbackone><input type=button value=" ���� "  onclick="InnerAudibles(\\'' + Audibles_ID + '\\')"><\\/td><\\/tr>'
		}
	}
	for (i=1;i<=Page_Max;i++)pagelist += (i==page)? '<font color=gray>['+i+']</font> ':'<A href="javascript:ShowForum_Emot('+i+')">['+i+']</A> '
	showlist = showlist + '<tr><td bgcolor=$miscbacktwo align=center colspan=3>'+ pagelist +'</TD></TR><tr><td bgcolor=$miscbacktwo align=center colspan=3><font color=blue>���ͼƬԤ�����鶯����ÿ��ֻ��һ��.</font></TD></tr>'
	showlist = '<tr><td><table width=100% cellpadding=5 cellspacing=1>' + showlist + '</table></td></tr>'
	document.getElementById("AudiblesShow").innerHTML = showlist ;
}

function InnerAudibles(id)
{
	opener.FORM.inpost.value +='[MagicFace='+id+']';
	self.close();
}
</script>
<DIV id=MagicFace style="Z-INDEX: 99; VISIBILITY: hidden; POSITION: absolute"></DIV>
<SCRIPT>valigntop()</SCRIPT>
<table width=$tablewidth cellpadding=0 cellspacing=0 align=center bgcolor=$tablebordercolor>
<TD id="AudiblesShow"></TD></table><SCRIPT>valignend()</SCRIPT>
<script>ShowForum_Emot(1)</script>

~;

}
elsif ($action eq "icq") {
    $output = qq~
<p>
<SCRIPT>valigntop()</SCRIPT>
    <table width=$tablewidth cellpadding=0 cellspacing=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <form action="http://wwp.mirabilis.com/scripts/WWPMsg.dll" method="post">
        <input type="hidden" name="subject" value="���� - $boardname"><input type="hidden" name="to" value="$UIN">
        <table width=100% cellpadding=5 cellspacing=1>
            <tr>
                <td bgcolor=$miscbackone align=center colspan=2>
                    <font color=$titlefontcolor><b>$boardname - ICQ Ѱ��</b><br>����һ����Ϣ�� $UIN</font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbacktwo valign=top>
                    <font color=$fontcolormisc>��������������</font>
                </td>
                    <td bgcolor=$miscbacktwo>
                    <input type="text" name="from" size="20" maxlength="40">
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone valign=top>
                    <font color=$fontcolormisc>���������� Email</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <input type="text" name="fromemail" size="20" maxlength="40">
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone valign=top>
                    <font color=$fontcolormisc>Ҫ���͵���Ϣ</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <textarea name="body" rows="3" cols="30" wrap="Virtual"></textarea>
                </td>
                </tr>
                <tr>
                <td bgcolor=$miscbacktwo align=center colspan=2>
                <input type="submit" name="Send" value="������Ϣ"></form>
                </td>
                </tr>
            </table>
        </td></tr>
    </table><SCRIPT>valignend()</SCRIPT>
    </body>
    </html>
    ~;
}
elsif ($action eq "lbcode") {
    $output = qq~<p>
<SCRIPT>valigntop()</SCRIPT>
    <table width=$tablewidth cellpadding=0 cellspacing=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <table width=100% cellpadding=5 cellspacing=1>
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=2>
                    <font color=$titlefontcolor><b>LeoBBS ��ǩ</b>
                    <br>LeoBBS ��ǩ���� HTML ��ǩ������ HTML ��ǩ��ȫ������Բ��������ֲ��еĸ�ʽ��ʹ������
                    </font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone><ul>
                    <font color=$fontcolormisc>
                    <font color=$fonthighlight>[quote]</font>�����ǩ��������Ϊ���������õģ��������ʲô�����������Ա�ĵط�������������ǩ��<font color=$fonthighlight>[/quote]</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><hr noshade color=$fonthighlight><blockquote>�����ǩ��������Ϊ���������õģ��������ʲô�����������Ա�ĵط�������������ǩ��</blockquote><hr noshade color=$fonthighlight></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone><UL>
                    <font color=$fontcolormisc>
                    <font color=$fonthighlight>[code]</font>
                    	<BR>unless ( eq "$authenticateme") {
			<BR>print "����Ĺ�������";
			<BR>&unlock;
			<BR>exit;
			<BR>}<BR>
			<font color=$fonthighlight>[/code]</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc>
			<BLOCKQUOTE>���룺<hr noshade color=$fonthighlight>
			unless ( eq "$authenticateme") { <BR>
			print "����Ĺ�������"; <BR>
			&unlock; <BR>
			exit; <BR>
			}<hr noshade color=$fonthighlight></FONT></BLOCKQUOTE>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[html]</font>&lt;font size=5&gt;HTML �� JS ����֧��&lt;/font&gt;<font color=$fonthighlight>[/html]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><SPAN><IMG src=$imagesurl/images/code.gif align=absBottom> HTML ����Ƭ������:<BR><TEXTAREA style="WIDTH: 94%; BACKGROUND-COLOR: #f7f7f7" name=textfield rows=4>&lt;font size=5&gt;HTML �� JS ����֧��&lt;/font&gt;<\/TEXTAREA><BR><INPUT onclick=runEx() type=button value=���д˴��� name=Button> [Ctrl+A ȫ��ѡ��   ��ʾ:������޸Ĳ��ִ��룬�ٰ�����]</SPAN><BR></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[url]</font>http://www.LeoBBS.com<font color=$fonthighlight>[/url]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="http://www.LeoBBS.com">http://www.LeoBBS.com</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[url=http://www.LeoBBS.com]</font>�װ��Ƽ�<font color=$fonthighlight>[/url]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="http://www.LeoBBS.com">�װ��Ƽ�</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[email=webmaster\@leobbs.com]</font>д�Ÿ���<font color=$fonthighlight>[/email]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="mailto:webmaster\@leobbs.com">д�Ÿ���</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[email]</font>webmaster\@leobbs.com<font color=$fonthighlight>[/email]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="mailto:webmaster\@leobbs.com">webmaster\@leobbs.com</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[b]</font>���ּӴ���Ч��<font color=$fonthighlight>[/b]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><b>���ּӴ���Ч��</b></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[i]</font>���ּ���бЧ��<font color=$fonthighlight>[/i]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><i>���ּ���бЧ��</i></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[u]</font>���ּ��»���Ч��<font color=$fonthighlight>[/u]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><u>���ּ��»���Ч��</u></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[size=4]</font>�ı����ִ�С<font color=$fonthighlight>[/size]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font size=4>�ı����ִ�С</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[font=impact]</font>�ı�����<font color=$fonthighlight>[/font]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font face=impact>�ı�����</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[color=red]</font>�ı�������ɫ<font color=$fonthighlight>[/color]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=red>�ı�������ɫ</font>
                </td>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[s]</font>�����ϼ�ɾ����<font color=$fonthighlight>[/s]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><s>�����ϼ�ɾ����</s></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sup]</font>�ϱ�����<font color=$fonthighlight>[/sup]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><sup>�ϱ�����</sup></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sub]</font>�±�����<font color=$fonthighlight>[/sub]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><sub>�±�����</sub></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[FLIPH]</font>���ҵߵ�����<font color=$fonthighlight>[/FLIPH]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:flipH">���ҵߵ�����</table></FLIPH>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[FLIPV]</font>���µߵ�����<font color=$fonthighlight>[/FLIPV]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:flipV">���µߵ�����</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[INVERT]</font>��ƬЧ��<font color=$fonthighlight>[/INVERT]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:invert"><img src="$imagesurl/images/leobbs8831.gif" border=0></table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[XRAY]</font>�ع�Ч��<font color=$fonthighlight>[/XRAY]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:xray"><img src="$imagesurl/images/logo.gif" border=0></table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[shadow=���ֿ��,��ɫ,�߽��С]</font>��Ӱ����<font color=$fonthighlight>[/shadow]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:shadow\(color=#f000ff\, direction=1)">��Ӱ����</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[GLOW=���ֿ��,��ɫ,�߽��С]</font>��������<font color=$fonthighlight>[/GLOW]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:glow\(color=#00f0ff\, strength=1)">��������</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[BLUR=���ֿ��,����,Ũ��]</font>ģ������<font color=$fonthighlight>[/BLUR]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:blur\(Add=0, direction=6\, strength=2)">ģ������</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[list]</font>��ʼ�б�<br><font color=$fonthighlight>[*]</font>�б���Ŀ<br><font color=$fonthighlight>[/list]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><ul>��ʼ�б�<br><li>�б���Ŀ</ul></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[img]</font>http://bbs.LeoBBS.com/non-cgi/myimages/mainlogo.gif<font color=$fonthighlight>[/img]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><img src="$imagesurl/images/mainlogo.gif" border=0></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[fly]</font>����������Ч<font color=$fonthighlight>[/fly]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><marquee width=90% behavior=alternate scrollamount=3>����������Ч<\/marquee></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[move]</font>����������Ч<font color=$fonthighlight>[/move]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><marquee width=90% scrollamount=3>����������Ч<\/marquee></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[swf]</font>http://www.micromedia.com/demo.swf<font color=$fonthighlight>[/swf]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����һ�� FLASH �ļ�(�Զ����ƴ�С)</font>
                </td> 
                </tr> 
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[flash=���,�߶�]</font>http://www.micromedia.com/demo.swf<font color=$fonthighlight>[/flash]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����һ�� FLASH �ļ�(�ֶ����ô�С)</font>
                </td> 
                </tr> 
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sound]</font>http://www.LeoBBS.com/demo.wav<font color=$fonthighlight>[/sound]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����һ�����������ļ�(*.mid,*.wav)</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[mms]</font>mms://www.microsoft.com/demo.asf<font color=$fonthighlight>[/mms]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����һ�� WM ��ʽ������</font>
                </td> 
                </tr> 
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[rtsp]</font>rtsp://www.real.com/demo.ram<font color=$fonthighlight>[/rtsp]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����һ�� Real ��ʽ������</font>
                </td> 
                </tr> 
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[ra]</font>http://www.LeoBBS.com/demo.ra<font color=$fonthighlight>[/ra]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����Real Player������Ƶ�ļ�(*.mp3,*.ra)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[rm]</font>http://www.LeoBBS.com/demo.rm<font color=$fonthighlight>[/rm]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����Real Player������Ƶ�ļ�(*.rm)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[real=���,�߶�]</font>http://www.LeoBBS.com/demo.rm<font color=$fonthighlight>[/real]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����Real Player������Ƶ�ļ�(*.rm)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[wmv]</font>http://www.LeoBBS.com/demo.wmv<font color=$fonthighlight>[/wmv]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����Windows Media Player������Ƶ�ļ�(*.wmv)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[wma]</font>http://www.LeoBBS.com/demo.wma<font color=$fonthighlight>[/wma]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����Windows Media Player������Ƶ�ļ�(*.wma)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[wm=���,�߶�]</font>http://www.LeoBBS.com/demo.wmv<font color=$fonthighlight>[/wm]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>����Windows Media Player������Ƶ�ļ�(*.wmv)</font>
                </td>
                </tr>
				<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[hide]</font>��������<font color=$fonthighlight>[/hide]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><blockquote><font face=$font>���� : <hr noshade size=1><font color=red>�����������Ѿ����أ�����ظ��󣬲��ܲ鿴<\/font><hr noshade size=1><\/blockquote><\/font><\/blockquote></font>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[post=1000]</font>��������<font color=$fonthighlight>[/post]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><blockquote><font face=$font>�������� : <hr noshade size=1><font color=red>�������ѱ����� , ������������1000���ܲ鿴<\/font><hr noshade size=1><\/font><\/blockquote></font>
                </td>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[jf=1000]</font>��������<font color=$fonthighlight>[/jf]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><blockquote><font face=$font>�������� : <hr noshade size=1><font color=red>�������ѱ����� , ���ִﵽ 1000 ���ܲ鿴<\/font><hr noshade size=1><\/font><\/blockquote></font>
                </td>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[watermark]</font>��ˮӡ����<font color=$fonthighlight>[/watermark]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><blockquote><font face=$font>�������� : <hr noshade size=1><font color=$miscbackone>72!*1</font><font color=red>�������ѱ���ˮӡ���������ѡ�п�����<\/font><font color=$miscbackone>(:9!*1</font><hr noshade size=1><\/font><\/blockquote></font>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[equote]</font>�ر���ʽ�����ã�Ч������ġ�<font color=$fonthighlight>[/equote]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><TABLE cellSpacing=0 cellPadding=0><TR><TD><IMG src=$imagesurl\/images\/top_l.gif><\/TD><TD background=$imagesurl\/images\/top_c.gif><\/TD><TD><IMG src=$imagesurl\/images\/top_r.gif><\/TD><\/TR><TR><TD vAlign=top background=$imagesurl\/images\/center_l.gif><\/TD><TD bgcolor=#fffff1>�ر���ʽ�����ã�Ч������ġ�<TD vAlign=top background=$imagesurl\/images\/center_r.gif><\/TD><\/TR><TR><TD vAlign=top><IMG src=$imagesurl\/images\/foot_l1.gif ><\/TD><TD background=$imagesurl\/images\/foot_c.gif><IMG src=$imagesurl\/images\/foot_l3.gif><\/TD><TD align=right><IMG src=$imagesurl\/images\/foot_r.gif><\/TD><\/TR><\/TABLE></font>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[fquote]</font>����һ���ر���ʽ�����ã�Ч������ġ�<font color=$fonthighlight>[/fquote]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table cellSpacing=0 cellPadding=0 width=100%><tr><td><table style=word-break: break-all cellSpacing=0 cellPadding=0><tr><td><img src=$imagesurl/images/top1_l.gif width=83 height=39></td><td width=100% background=$imagesurl/images/top1_c.gif>��</td><td><img src=$imagesurl/images/top1_r.gif width=7 height=39></td></tr><tr><td colSpan=3><table cellSpacing=0 cellPadding=0 width=100%><tr><td vAlign=top background=$imagesurl/images/center1_l.gif><img src=$imagesurl/images/top1_l2.gif width=11 height=1></td><td vAlign=center width=100% bgColor=#fffff1>����һ���ر���ʽ�����ã�Ч������ġ�</td><td vAlign=top background=$imagesurl/images/center1_r.gif><img src=$imagesurl/images/top1_r2.gif width=7 height=2></td></tr></table></td></tr><tr><td colSpan=3><table cellSpacing=0 cellPadding=0 width=100%><tr><td vAlign=top><img src=$imagesurl/images/foot1_l1.gif width=12 height=18></td><td width=100% background=$imagesurl/images/foot1_c.gif><img src=$imagesurl/images/foot1_l3.gif width=1 height=18></td><td align=right><img src=$imagesurl/images/foot1_r.gif width=8 height=18></td></tr></table></td></tr></table></td></tr></table>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[curl=http://www.LeoBBS.com/]</font></font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>�������в����������</font>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[buyexege]�������ӵ�����ע��[/buyexege]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>�������ӵ�����ע�⣬ֻ������ʱ����ʹ�ã�ע�����ݶ��κ��˶��ǿɼ��ġ�</font>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[iframe]</font>http://www.LeoBBS.com/<font color=$fonthighlight>[/iframe]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>�������в�����ҳ</font>
                </td>
                </tr>

            </table>
        </td></tr>
    </table><SCRIPT>valignend()</SCRIPT>
    </body>
    </html>
    ~;
}

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

    &output("$boardname - ����",\$output,"msg");
exit;
