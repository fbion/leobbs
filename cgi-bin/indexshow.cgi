#!/usr/bin/perl
#####################################################
#  ��ҳJs������
#  By maiweb 2005-08-05
#  leobbs-vip.com
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

$thisprog = "indexshow.cgi";

$query = new LBCGI;

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
          
    &getmember("$inmembername","no");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
    	for('allnews','news','newsjh','mainlogin','showmem','info','getanc','getanc2')
    	{
    		if(!(-e "${lbdir}$_.cgi")){$$_=0;}else{$$_=1;}
    	$a.="var $_ = $$_;\n";
    	}
    	
    	require "${lbdir}data/outputbutton.pl" if (-e "${lbdir}data/outputbutton.pl");
		$outputbutton =~ s/\<\!\-\-h (.+?) \-\-\>/$1/isg;
		$outputbutton =~ s/\<\!\-\-c (.+?) \-\-\>/$1/isg;
    	$outputbutton =~s/"//isg;
    	$outputbutton =~s/\n//isg;
print qq~<script>
var realurl = '';
$a
	function selcolor(obj2){
		var arr = showModalDialog("$imagesurl/editor/selcolor.html", "", "dialogWidth:18.5em; dialogHeight:17.5em; status:0");
		arr = arr.replace(/#/g,"");
		obj2.value=arr;
	}
	function nextstep(){
		FORM.outScript.value='';
		var aad = eval(FORM.D1.value);
		if(aad==0){
		ts.innerHTML ='<font color=red>����Ҫ���õĹ���ȱ���ļ���������ڹٷ����ص�����ѹ���������addonĿ¼�����<b><u>'+FORM.D1.value+'.cgi</u></b>�ļ��ϴ���cgi-binĿ¼���棬Ȼ��<b>ˢ��</b>��ҳ������</font>';
		formshow.innerHTML ='';
		FORM.tj.disabled = true;
		return false;
		}else{
		ts.innerHTML ='���������Ĳ���һ�������У�';
		FORM.tj.disabled = false;
		}
		
		if(FORM.D1.value =='news'||FORM.D1.value =='newsjh'){
			formshow.innerHTML ='2��ѡ��Ҫ���õİ��<br><br><select size="1" name="forum"><option value="">ѡ��Ҫ���õİ��$outputbutton</select><br><br>';
		}
		else if(FORM.D1.value =='allnews'){
			formshow.innerHTML ='2�����Ӻ����Ƿ���ʾ����<br><br><select size="1" name="name"><option value="">���Ӻ����Ƿ���ʾ����<option value=1>��ʾ������<option value=0>����ʾ������</select><br><br>';
		}
		else if(FORM.D1.value =='getanc'){
		formshow.innerHTML ='2��������õĹ��泤��<br><br><input type=text size=4 name=max><br><br>';return;
		}
		else if(FORM.D1.value =='showmem'){
		formshow.innerHTML ='2��������õĻ�Ա��Ŀ<br><br><input type=text size=4 name=show><br><br>';return;
		}
		else if(FORM.D1.value =='getanc2'){
		formshow.innerHTML ='2��ѡ��Ҫ���õİ��<br><br><select size="1" name="forum"><option value="">ѡ��Ҫ���õİ��$outputbutton</select><br><br>3������ı��ⳤ��<br><br><input type=text size=2 name=maxlength><br><br>4����ʾ�Ĺ�������<br><br><input type=text size=2 name=max><br><br>';return;
		}
		else{
			formshow.innerHTML ='';return;
		}
			formshow.innerHTML +='3��������õ�����:<input type=text size=4 name=max>';
			formshow.innerHTML +=' 4�����ӱ��ⳤ��:<input type=text size=4 name=maxlength><br><br>';
			formshow.innerHTML +='5�����Ӻ����Ƿ���ʾ����ʱ��<br><br><select size="1" name="display"><option value=1>��ʾ����ʱ��<option value=0>����ʾ����ʱ��</select><br><br>';
			formshow.innerHTML +='6����ģʽ<br><br><select size="1" name="mode"><option value=view>����ģʽ<option value=topic>��̳ģʽ</select><br><br>';
			formshow.innerHTML +='7����ɫ<br><br>�����ӵ���ɫ:<input type=text size=6 name=link  onclick="javascript:selcolor(link)"> �ѷ��ʹ��ĳ�����:<input type=text size=6 name=vlink  onclick="javascript:selcolor(vlink)"> ��ǰ������:<input type=text size=6 name=alink  onclick="javascript:selcolor(alink)"><br><br>';
	}
	function checkForm(thisform){
		var baseurl = '$boardurl/'+thisform.D1.value+'.cgi';
		realurl = baseurl;
		if(thisform.D1.value=='news'||thisform.D1.value=='newsjh'||thisform.D1.value=='getanc2'){
		if(thisform.forum.value==''){
		alert('�����ѡ����õİ�飡');
		thisform.forum.focus();
		return false;
		}
		else{
		realurl +='?forum='+ thisform.forum.value;}
		}
		if(thisform.D1.value=='allnews'){
		if(thisform.name.value==''){
		alert('�����ѡ������Ƿ�ѡ�������ߣ�');
		thisform.name.focus();
		return false;
		}else{
		realurl +='?name='+ thisform.name.value;}
		}
		if(thisform.D1.value=='getanc2'){
		if(thisform.maxlength.value==''){
		alert('�����������õĹ�����ⳤ�ȣ��� 30');
		thisform.maxlength.focus();
		return false;
		}else{
		realurl +='?maxlength='+thisform.maxlength.value;
		}
		if(thisform.max.value==''){
		alert('�����������õĹ��������� �� 10');
		thisform.max.focus();
		return false;
		}else{
		realurl +='&show='+thisform.max.value;
		}
		}
		if(thisform.D1.value!='mainlogin'&&thisform.D1.value!='getanc2'&&thisform.D1.value!='info'){
		if(thisform.D1.value=='showmem'){
		if(thisform.show.value==''){
		alert('�����������õĻ�Ա��Ŀ���� 10');
		thisform.show.focus();
		return false;
		}else{
		realurl +='?show='+thisform.show.value;
		}}else{
		if(thisform.D1.value=='getanc'){
		if(thisform.max.value==''){
		alert('�����������õĹ��泤�ȣ��� 500');
		thisform.max.focus();
		return false;
		}else{
		realurl +='?max='+thisform.max.value;
		}
		}else{
		if(thisform.max.value==''){
		alert('�����������õ������������� 10');
		thisform.max.focus();
		return false;
		}else{
		realurl +='&max='+thisform.max.value;
		}
		if(thisform.maxlength.value==''){
		alert('�����������õ����ӳ��ȣ��� 30');
		thisform.maxlength.focus();
		return false;
		}else{
		realurl +='&maxlength='+thisform.maxlength.value;
		}
		realurl +='&display='+thisform.display.value;
		realurl +='&mode='+thisform.mode.value;
		if(thisform.link.value !=''){
		realurl +='&link='+thisform.link.value;
		}
		if(thisform.vlink.value !=''){
		realurl +='&vlink='+thisform.vlink.value;
		}
		if(thisform.alink.value !=''){
		realurl +='&alink='+thisform.alink.value;
		}}
		}
		}
		var tmp = '<scr';
		tmp += 'ipt type="text/javasc';
		tmp += 'ript" src="'+realurl+'"></s';
		tmp += 'cript>';
		realurl = tmp; 
		thisform.outScript.value = realurl; return false;
	} 
	function HighlightAll(theField) {
		var tempval=eval("document."+theField)
		tempval.select()
		therange=tempval.createTextRange()
		therange.execCommand("Copy")
		alert('Copy ok!')
	}
</SCRIPT>
	<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>��ӭ������̳��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>	<form onsubmit="return checkForm(this);" method=post name=FORM>
    <b>��ʾ��</b><br><span id=ts>���������Ĳ���һ�������У�</span><p>
   1����ѡ����Ҫ���õ����ͣ�<p>
                <select size="1" name="D1" onchange="if(this.options[this.selectedIndex].value!=''){nextstep();}">
  <option selected value=''>ѡ����Ҫ���õ����</option>
  <option value="allnews">ȫ��̳�������ӵ���</option>
  <option value="news">����̳�������ӵ���</option>
  <option value="newsjh">����̳�������ӵ���</option>
  <option value="mainlogin">��̳��½�����</option>
  <option value="getanc">��̳���¹������</option>
  <option value="getanc2">����̳���¹������</option>
  <option value="info">��̳������Ϣ����</option>
  <option value="showmem">��̳��������</option></p>
  &nbsp;
</select><p><span id=formshow></span><textarea rows="5" name="outScript" cols="28" readonly disabled></textarea><br>
<br>
<button type=submit name=tj disabled>���ɴ���</button> <button name=copy onClick=HighlightAll('FORM.outScript')>��������</button>
</form><p><br><br></p><p align=center>&copy CopyRight By Maiweb 2005-08-05</p></td></tr>~;
	}
	else {
	    &adminlogin;
	}
print qq~</td></tr></table></body></html>~;
exit;
