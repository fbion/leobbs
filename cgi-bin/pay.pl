#&getoneforum("$inforum");

    if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    	&error("����&��Ļ���Ϊ $jifen��������ֻ̳�л��ִ��ڵ��� $postminjf �Ĳ��ܷ��ԣ�") if ($postminjf > 0 && $jifen < $postminjf);
    }

    if ($startnewthreads eq "onlysub") {&error("����&�Բ��������Ǵ�����̳�����������ԣ�"); }
    $tempaccess = "forumsallowed". "$inforum";
    $testentry = $query->cookie("$tempaccess");

    if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("����&�Բ�����û���ڴ���̳�з����Ȩ����"); }

    if ($postopen eq "no") { &error("��������&�Բ��𣬱���̳�����������⣡"); }

    if ($payopen eq "no") { &error("��������&�Բ��𣬱���̳��������������"); }

    if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $inmembmod ne "yes") {
	&error("��������&�Բ������ɾ���ʳ�����<b>$deletepercent</b>%������Ա�������㷢��������") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
    }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") { &whosonline("$inmembername\t$forumname\tnone\t��������\t"); }
                       else { &whosonline("$inmembername\t$forumname(��)\tnone\t�����µı��ܽ�����\t"); }
    }
    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     {  $onlinetime = $onlinetime + $onlinetimeadd; &error("��������&�Բ��𣬱���̳����������ʱ������ $onlinepost ����û�������������Ŀǰ�Ѿ����� $onlinetime �룡"); }

    &mischeader("��������");

    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>�лظ�ʱʹ���ʼ�֪ͨ����<br>~;
    }

    if ($startnewthreads eq "no")        { $startthreads = "�ڴ���̳���µĽ����������ӻظ�ֻ����̳������������"; }
    elsif ($startnewthreads eq "follow") { $startthreads = "�ڴ���̳���µĽ�����ֻ����̳��������������ͨ��Աֻ���Ը�����"; }
    elsif ($startnewthreads eq "all")    { $startthreads = "�κ��˾����Է���ͻظ���������δע���û��������������գ�"; }
    elsif ($startnewthreads eq "cert")   { $startthreads = "�ڴ���̳���µĽ�����ֻ����̳������������֤�Ļ�Ա����"; }
    else { $startthreads = "����ע���Ա�����Է���ͻظ���������"; }

    $startthreads .= " <B>(�����ڱ��������)</B>" if ($mastpostatt eq "yes");

    if ($emoticons eq "on") {
	$emoticonslink = qq~<li><a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">����<B>ʹ��</B>�����ַ�ת��</a>~;
	$emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>���Ƿ�ϣ��<b>ʹ��</b>�����ַ�ת�������������У�<br>~;
    }

    if ($emoticons eq "on") {
	$output .= qq~<script language="javascript">function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}</script>~;
    }
    if ($htmlstate eq "on")     { $htmlstates = "����"; }     else { $htmlstates = "������"; }
    if ($idmbcodestate eq "on") { $idmbcodestates = "����"; $canlbcode =qq~<input type=checkbox name="uselbcode" value="yes" checked>ʹ�� LeoBBS ��ǩ��<br>~; } else { $idmbcodestates = "������"; $canlbcode= "";}
    if ($useemote eq "no")      { $emotestates = "������"; }  else { $emotestates = "����"; }

    $intopictitle =~ s/^����������//;
    $output .= qq~<script>
var autoSave = false;
function storeCaret(textEl) {if (textEl.createTextRange) textEl.caretPos = document.selection.createRange().duplicate();if (autoSave)savePost();}
function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
function DoTitle(addTitle) {
var revisedTitle;var currentTitle = document.FORM.intopictitle.value;revisedTitle = addTitle+currentTitle;document.FORM.intopictitle.value=revisedTitle;document.FORM.intopictitle.focus();
return;}
</script>
<form action=$thisprog method=post name="FORM" enctype="multipart/form-data">
<input type=hidden name=action value=addnewpay>
<input type=hidden name=forum value=$inforum>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor><b>˭���Է���</b> $startthreads������֧�����ľ���˵������� <a href=http://www.alipay.com/ target=_blank>http://www.alipay.com/</a></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�������</b></font>��
<select name=font onchange=DoTitle(this.options[this.selectedIndex].value)>
<OPTION selected value="">ѡ����</OPTION> <OPTION value=[ԭ��]>[ԭ��]</OPTION><OPTION value=[ת��]>[ת��]</OPTION><OPTION value=[��ˮ]>[��ˮ]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[�Ƽ�]>[�Ƽ�]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[ע��]>[ע��]</OPTION><OPTION value=[��ͼ]>[��ͼ]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[����]>[����]</OPTION><OPTION value=[����]>[����]</OPTION>
</SELECT></td><td bgcolor=$miscbackone><input type=text size=60 maxlength=80 name="intopictitle" value="$intopictitle">�����ó��� 40 ������</td></tr>$nowaterpost
    ~;
        $output .= qq~<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>��Ŀǰ������ǣ� <font color=$fonthighlight><B><u>$inmembername</u></B></font> ��Ҫʹ�������û���ݣ��������û��������롣δע������������������������ա�</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>�����������û���</font></td><td bgcolor=$miscbackone><input type=text name="membername">   <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">��û��ע�᣿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>��������������</font></td><td bgcolor=$miscbackone><input type=password name="password">   <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">�������룿</a></font></td></tr>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>��ǰ����</b><br><li>���������ӵ�ǰ��<BR></font></td><td bgcolor=$miscbackone valign=top>
~;
    open (FILE, "${lbdir}data/lbpost.cgi");
    my @posticondata = <FILE>;
    close (FILE);
    chomp @posticondata;
    my $tempiconnum=1;
    foreach (@posticondata) {
if ($tempiconnum > 12) {
    $tempiconnum = 1;
    $output .= qq~<BR>~;
}
$output .= qq~<input type=radio value="$_" name="posticon"><img src=$imagesurl/posticons/$_ $defaultsmilewidth $defaultsmileheight> ~;
$tempiconnum ++;
}

    if (($arrowupload ne "off")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
    $uploadreqire = "" if ($uploadreqire <= 0);
    $uploadreqire = "<BR>������Ҫ���� <B>$uploadreqire</B> ƪ(��֤�û�����)" if ($uploadreqire ne "");
	$output .= qq~<script language="javascript">function jsupfile(upname) {upname='[UploadFile$imgslt='+upname+']';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? upname + ' ' : upname;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=upname;document.FORM.inpost.focus();}}</script>~;
        $output .= qq~<tr><td bgcolor=$miscbackone><b>�ϴ�������ͼƬ</b> (������� <B>$maxupload</B>KB)$uploadreqire</td><td bgcolor=$miscbackone> <iframe id="upframe" name="upframe" src="upfile.cgi?action=uppic&forum=$inforum&topic=$intopic" width=100% height=40 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=NO></iframe><br><font color=$fonthighlight>Ŀǰ����:(�粻��Ҫĳ��������ֻ��ɾ�������е���Ӧ [UploadFile$imgslt ...] ��ǩ����)  [<a href=upfile.cgi?action=delup&forum=$inforum target=upframe title=ɾ������δ�������ĸ�����ʱ�ļ� OnClick="return confirm('ȷ��ɾ������δ�������ĸ�����ʱ�ļ�ô��');">ɾ��</a>] </font></font><SPAN id=showupfile name=showupfile></SPAN></td></tr>~;
    }

    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�ҵ�֧�����˺�</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="alipayid" value="$emailaddress">�����û�У�����д��ȷ���ʼ���ַ</td></tr>~;
$output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��Ʒ����</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="warename">��û�����ƣ������ô����?</td></tr>~;
$output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��Ʒչʾ��ַ</b></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="wareurl">�����ͻ�������ϸ�Ľ���</td></tr>~;
    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>��Ʒ�۸�</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="wareprice">������д��ȷ�ļ۸�</td></tr>~;
    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>�ʷѳе���ѡ��</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone>
<input onclick="document.FORM.postage_mail.disabled=true; document.FORM.postage_express.disabled=true; document.FORM.postage_ems.disabled=true" type="radio" CHECKED value="s" name="transport"> ���ҳе��ʷ�<br>
<input onclick="document.FORM.postage_mail.disabled=false; document.FORM.postage_express.disabled=false; document.FORM.postage_ems.disabled=false" type="radio" value="b" name="transport"> ��ҳе��ʷ�<br>
ͨ����������ѡ��ע���ý������������ķ��е��˷ѡ�<br>
�������ҳе��˷ѣ���ѡ������ṩ��������ʽ�Լ���Ӧ���á�<br>
ƽ�� <input disabled size="3" name="postage_mail"> Ԫ (�����������ṩƽ��)<br>
��� <input disabled size="3" name="postage_express"> Ԫ (�����������ṩ���)<br>
EMS&nbsp; <input disabled size="3" name="postage_ems"> Ԫ (�����������ṩ EMS)<br>
</td></tr>
~;
    $maxpoststr = "(������������ <B>400</B> ���ַ�)" ;
    
    $output .= qq~</td></tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>��Ʒ����</b> <font color=$fonthighlight>(*)</font>��$maxpoststr<p>�ڴ���̳�У�<li>HTML ����ǩ: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE����ǩ</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS ��ǩ</a>: <b>$idmbcodestates</b><li>��ͼ��ǩ ��: <b>$postpicstates</b><li>Flash ��ǩ : <b>$postflashstates</b><li>���ֱ�ǩ ��: <b>$postsoundstates</b><li>���ִ�С ��: <b>$postfontsizestates</b><li>������ǩ ��: <b>$postjfstates</b><li>���ֱ�ǩ ��: <b>$jfmarkstates</b><li>���ܱ�ǩ ��: <b>$hidejfstates</b>$emoticonslink</font></td><td bgcolor=$miscbackone>$insidejs<TEXTAREA cols=80 name=inpost id=inpost rows=12 wrap="soft" onkeydown=ctlent() onselect="storeCaret(this);" onclick="storeCaret(this);" onkeyup="storeCaret(this);">$inpost</TEXTAREA><br>
  ģʽ:<input type="radio" name="mode" value="help" onClick="thelp(1)">������<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">��ȫ��<input type="radio" name="mode" value="basic"  onClick="thelp(0)">��������>> <a href=javascript:HighlightAll('FORM.inpost')>���Ƶ�������</a> | <a href=javascript:checklength(document.FORM);>�鿴����</a> | <span style=cursor:hand onclick="document.getElementById('inpost').value += trans()">ת�������峬�ı�</spn><SCRIPT>rtf.document.designMode="On";</SCRIPT> <<
</td></tr></tr>~;
    
    if ($emoticons eq "on") {
$output .= qq~<tr><td bgcolor=$miscbackone valign=top colspan=2><font color=$fontcolormisc><b>�������ͼ�����������м�����Ӧ�ı���</B></font><br> ~;
if (open (FILE, "${lbdir}data/lbemot.cgi")) {
    @emoticondata = <FILE>;
    close (FILE);
    chomp @emoticondata;
    $emoticondata = @emoticondata;
}
$maxoneemot = 16 if ($maxoneemot <= 5);
if ($maxoneemot > $emoticondata) {
           foreach (@emoticondata) {
my $smileyname = $_;
$smileyname =~ s/\.gif$//ig;
$output .= qq~<img src=$imagesurl/emot/$_ border=0 onClick="smilie('$smileyname');FORM.inpost.focus()" style="cursor:hand"> ~;
    }
} else {
    my $emoticondata = "'" . join ("', '", @emoticondata) . "'";
    $output .= qq~
<table><tr><td id=emotbox></td></tr></table>
<script>
var emotarray=new Array ($emoticondata);
var limit=$maxoneemot;
var eofpage=ceil(emotarray.length/limit);
var page=0;
function ceil(x){return Math.ceil(x)}
function emotpage(topage){
var beginemot=(page+topage-1)*limit;
var endemot=(page+topage)*limit ;
var out='';
page=page+topage;
if (page != 1) { out += '<span style=cursor:hand onclick="emotpage(-1)" title=��һҳ><font face=webdings size=+1>7</font></span> '; }
for (var i=beginemot;i<emotarray.length && i < endemot ;i++){out += ' <img src=$imagesurl/emot/' + emotarray[i] + ' border=0 onClick="smilie(\\'' + emotarray[i].replace(".gif", "") + '\\');FORM.inpost.focus()" style=cursor:hand> ';}
if (page != eofpage){ out += ' <span style=cursor:hand onclick="emotpage(1)" title=��һҳ><font face=webdings size=+1>8</font></span>'; }
out += '  �� '+ page+' ҳ���ܹ� '+ eofpage+ ' ҳ���� '+emotarray.length+' ��';
out += '  <B><span style=cursor:hand onclick="showall()" title="��ʾ���б���ͼʾ">[��ʾ����]</span></B>';
emotbox.innerHTML=out;
}
emotpage (1);
function showall (){var out ='';for (var i=0;i<emotarray.length;i++){out += ' <img src=$imagesurl/emot/' + emotarray[i] + ' border=0 onClick="smilie(\\'' + emotarray[i].replace(".gif", "") + '\\');FORM.inpost.focus()" style=cursor:hand> ';}emotbox.innerHTML=out;}
</script>
~;
}
    $output .= qq~</td></tr>~;
    }
    $output .= qq~<tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>ѡ��</b><p>$helpurl</font></td>
<td bgcolor=$miscbacktwo><font color=$fontcolormisc>$canlbcode
<input type=checkbox name="inshowsignature" value="yes" checked>�Ƿ���ʾ����ǩ����<br>
$requestnotify$emoticonsbutton$fontpost$weiwangoptionbutton
</font><BR></td></tr><tr><td bgcolor=$miscbacktwo colspan=2 align=center>
<input type=Submit value="�� ��" name=Submit onClick="return clckcntr();">����<input type=button value='Ԥ ��' name=Button onclick=gopreview()>����<input type="reset" name="Clear" value="�� ��"></td></form></tr></table></tr></td></table>
<SCRIPT>valignend()</SCRIPT>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$inforum"></form>
<script>
function gopreview(){
document.preview.body.value=document.FORM.inpost.value;
var popupWin = window.open('', 'preview_page', 'scrollbars=yes,width=600,height=400');
document.preview.submit()
}
</script>
    ~;
1;
