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
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setcss.cgi";

$query = new LBCGI;

$action              = $query -> param('action');
$oldmembersdir       = $query -> param('oldmembersdir');
$membersdir          = $query -> param('membersdir');

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");


if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

    print qq~
<script language='Javascript'>
 function do_css() {
    var theForm = document.css_form;
    var theName = theForm.NAME.value;
    var theFont = theForm.FONT.value;
    var theSize = theForm.SIZE.value;
    var theSizeT = theForm.SIZE_TYPE.value;
    var theWeight = theForm.WEIGHT.value;
    var theColor  = theForm.COLOUR.value;
    var theBG     = theForm.BGCOLOUR.value;
    var theBW     = theForm.BWEIGHT.value;
    var theBC     = theForm.BCOLOUR.value;
    var theSpace  = theForm.SPACE.value;
    var theSpaceT = theForm.SPACING.value;
    var theLSpace = theForm.LSPACE.value;
    var tmp_style = \"solid\";
    var tmp_col   = \"black\";
    var tmp_thick = \"1px\";
    var msg = \"\";
    
    if (theName == \"\") { msg = \"�����Ҫдһ�� CSS ������\"; }
    if (msg != \"\") {
        alert(msg);
        return;
    }
    var thecss = \"#\" + theName + \" {\\n\";
    if (theFont != \"\") {
     thecss += \"\t font-family: \" + theFont + \";\\n\";
    }
    if (theSize != \"\") {
     thecss += \"\t font-size: \" + theSize + theSizeT + \";\\n\";
    }
    if (theWeight != \"normal\") {
     thecss += \"\t font-weight: \" +  theWeight + \";\\n\";
    }
    if (theColor != \"\") {
     thecss += \"\t color: \" +  theColor + \";\\n\";
    }
    if (theBG != \"\") {
     thecss += \"\t background-color: \" +  theBG + \";\\n\";
    }
    if (theBW != \"\") {
     tmp_thick    = theBW + \"px\";
    }
    if (theBC != \"\") {
     tmp_col  = theBC;
    }
    if (theBW != \"\" && theBC != \"\") {
     thecss += \"\t border: \" + tmp_style + \" \" + tmp_col + \" \" + tmp_thick + \";\\n\";
    }
    if (theSpace != \"\") {
     thecss += \"\t line-height: \" + theSpace + theSpaceT + \";\\n\";
    }
    if (theLSpace != \"\") {
     thecss += \"\t letter-spacing: \" + theLSpace + \"px;\\n\";
    }
    thecss += \"}\";
    
    theForm.CSS.value = thecss;
    return;
    
   }
    function preview() {
       var theCSS = document.css_form.CSS.value;
       var theID  = document.css_form.NAME.value;
       var Template = \"<html><head><title>testing CSS</title><style type=\\"text/css\\">\"+theCSS+\"</style></head>\\n<body bgcolor='#FFFFFF'>\\n\";
       Template += \"<span id='\"+theID+\"'>���ᳬ����̳ LeoBBS ��<br>CSS Ԥ��......</span>\";
       Template += \"\\n</body></html>\";
       var newWin = window.open( '', 'PREVIEW', 'width=500,height=200,top=0,left=0,resizable=1,scrollbars=1,location=no,directories=no,status=no,menubar=no,toolbar=no');
       newWin.document.write(Template);
   }    
 </script>
                     <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                    <b>��ӭ������̳�������� / �û� CSS �Զ�����</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2><font face=���� color=#333333>
  <br><br>
 <form name='css_form'>
 <table width='95%' align='center' border='0' bgcolor='#000000' cellspacing='1' cellpadding='0'>
 <tr>
  <td>
   <table width='100%' align='center' border='0' bgcolor='#EFEFEF' cellspacing='0' cellpadding='4'>
   <tr>
    <td width='40%'><b>Ҫ���ɵ� CSS ������?</b></td>
    <td width='60%'><input type='text' name='NAME'></td>
   </tr>
   <tr>
    <td width='40%'><b>�������� (�����������ö��Ÿ���)</b></td>
    <td width='60%'><input type='text' name='FONT'></td>
   </tr>
   <tr>
    <td width='40%'><b>�����С</b></td>
    <td width='60%'><input type='text' name='SIZE' size='5'>&nbsp;<select name='SIZE_TYPE'><option value='px'>����<option value='pt'>��<option value='em'>em</select></td>
   </tr>
   <tr>
    <td width='40%'><b>������</b></td>
    <td width='60%'><select name='WEIGHT'><option value='normal'>����<option value='bold'>����<option value='bolder'>����</select></td>
   </tr>
   <tr>
    <td width='40%'><b>������ɫ</b></td>
    <td width='60%'><input type='text' name='COLOUR'></td>
   </tr>
   <tr>
    <td width='40%'><b>������ɫ</b></td>
    <td width='60%'><input type='text' name='BGCOLOUR'></td>
   </tr>
   <tr>
    <td width='40%'><b>�߿�</b></td>
    <td width='60%'>���<input type='text' name='BWEIGHT' size='5'>&nbsp;&nbsp;&nbsp;��ɫ<input type='text' name='BCOLOUR' size='15'></td>
   </tr>
   <tr>
    <td width='40%'><b>�м��</b></td>
    <td width='60%'><input type='text' name='SPACE' size='5'>&nbsp;<select name='SPACING'><option value='px'>����<option value='pt'>��<option value='%'>%</select></td>
   </tr>
   <tr>
    <td width='40%'><b>��ĸ���</b></td>
    <td width='60%'><input type='text' name='LSPACE' size='5'>&nbsp;��</td>
   </tr>
   <tr>
   <td colspan='2' align='center'><input type='button' onClick='do_css();' value='�Զ�������Ӧ�� CSS ����'></td>
   </tr>
 </table>
</td>
</tr>
</table>

<br><br><br><center>���ɵ� CSS �������£�<br><textarea name='CSS' rows='10' cols='70' wrap='soft'></textarea><BR><BR>
<input type='button' onClick='preview();' value='���Ԥ��'></center>
</form>
                ~;

            }
            else {
                 &adminlogin;
                 }

print qq~</td></tr></table></body></html>~;
exit;
