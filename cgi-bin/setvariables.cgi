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

$thisprog = "setvariables.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;');

$query = new LBCGI;
#&ipbanned; #��ɱһЩ ip

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);

        if (($_ eq 'adfoot')||($_ eq 'adscript')||($_ eq 'adscriptmain')||($_ eq 'adlinks')||($_ eq 'topicad')) {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g
	}
	$theparam = &unHTML("$theparam");

	$theparam  = sprintf("%02d",$theparam) if (($_ eq 'createmon')||($_ eq 'createday'));
	if ($_ eq 'createyear') { $theparam = sprintf("%02d", $theparam); $theparam = 1900+$theparam if ($theparam<100); }

	${$_} = $theparam;
        if ($_ ne 'action') {
            $theparam =~ s/[\a\f\n\e\0\r]//isg;
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
        
$maxweiwang = 5 if (($maxweiwang < 5)||($maxweiwang eq ""));

if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {

    if ($action eq "process") {

        
        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/boardinfo.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

$lbdirbak = $lbdir ;

eval{ require "data/boardinfo.cgi"; };
if ($@) {

    open(FILE,"${lbdirbak}data/boardinfobak.cgi");
    my @ddd = <FILE>;
    close(FILE);
    open(FILE,">${lbdirbak}data/boardinfo.cgi");
    foreach (@ddd) {
    	chomp $_;
        print FILE "$_\n";
    }
    close(FILE);

                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                    <b>��ӭ������̳�������� / ��������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=���� color=#333333><b>������Ϣû�б���</b><br>������������У��з����������ݣ��������ݳ������Ų飡
                    </td></tr></table></td></tr></table>
                    ~;
		print qq~</td></tr></table></body></html>~;
		exit;
}

        $filetomake = "$lbdir" . "data/boardinfobak.cgi";
        open(FILE,">$filetomake");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);

    opendir (DIRS, "${lbdir}cache/id");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	$_ =~ s/\.cgi//isg;
    	unlink ("${lbdir}cache/id/$_\.cgi");
    }

        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / �����ṹ</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=���� color=#333333><center><b>������Ϣ�Ѿ��ɹ�����</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                $printme =~ s/\\\'/\'/g;
                print $printme;
                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                    <b>��ӭ������̳�������� / ��������</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=���� color=#333333><b>������Ϣû�б���</b><br>�ļ�����Ŀ¼����д<br>������� data Ŀ¼�� boardinfo.cgi �ļ������ԣ�
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=���� color=#FFFFFF>
                <b>��ӭ������̳�������� / ��������</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>��̳��������</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                <input type=hidden name="noads" value="$noads">
                <input type=hidden name="regerid" value="$regerid">
                ~;
                $tempoutput1 = "<select name=\"mainoff\">\n<option value=\"0\">��̳����\n<option value=\"1\">��̳�ر�\n<option value=\"2\">�Զ����ڿ���\n</select>\n";
                $tempoutput1 =~ s/value=\"$mainoff\"/value=\"$mainoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333 ><b>��̳״̬</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1</td>
                </tr>
                ~;
	$tempoutput1 = "<select name=\"mainauto\">\n<option value=\"day\">ÿ��\n<option value=\"week\">ÿ����\n<option value=\"month\">ÿ��\n</select>\n";
        $tempoutput1 =~ s/value=\"$mainauto\"/value=\"$mainauto\" selected/;
      	print qq~
              <tr>
              <td bgcolor=#FFFFFF width=40%>
              <font face=���� color=#333333 ><b>�Զ�������̳��</b><br>(ֻ��ѡ���Զ����ڿ��Ŵ�����Ч)</font></td>
              <td bgcolor=#FFFFFF>
              $tempoutput1 <input name=mainautovalue value="$mainautovalue" size=8><br>ע: ����ʹ�õ�һ���ֻ��Ƿ�Χ����ÿ��6, ÿ��0-6, ÿ����6, ÿ��10-15</td>
              </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333 ><b>ά��˵��</b> (֧�� HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="line1" cols="40">$line1</textarea><BR><BR></td>
                </tr>
                ~;
                $tempoutput1 = "<select name=\"regonoff\">\n<option value=\"0\">�����û�ע��\n<option value=\"1\">�������û�ע��\n<option value=\"2\">�Զ����ڿ���\n</select>\n";
                $tempoutput1 =~ s/value=\"$regonoff\"/value=\"$regonoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333 ><b>�Ƿ������û�ע��</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1<BR><BR></td>
                </tr>
                ~;
		$tempoutput1 = "<select name=\"regauto\">\n<option value=\"day\">ÿ��\n<option value=\"week\">ÿ����\n<option value=\"month\">ÿ��\n</select>\n";
		$tempoutput1 =~ s/value=\"$regauto\"/value=\"$regauto\" selected/;
		print qq~
               <tr>
               <td bgcolor=#FFFFFF width=40%>
               <font face=���� color=#333333 ><b>�Զ�����ע����</b><br>(ֻ������ѡ���Զ����ڿ��Ŵ������Ч)</font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput1 <input name=regautovalue value="$regautovalue" size=8><br>ע: ����ʹ�õ�һ���ֻ��Ƿ�Χ����ÿ��6, ÿ��0-6, ÿ����6, ÿ��10-15</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333 ><b>������ע��˵��</b> (֧�� HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="noregwhynot" cols="40">$noregwhynot</textarea><BR><BR></td>
                </tr>
                ~;
                $tempoutput1 = "<select name=\"regdisptime\">\n<option value=\"15\">15\n<option value=\"1\">1\n<option value=\"3\">3\n<option value=\"5\">5\n<option value=\"8\">8\n<option value=\"10\">10\n<option value=\"12\">12\n<option value=\"17\">17\n<option value=\"20\">20\n<option value=\"25\">25\n<option value=\"30\">30\n<option value=\"40\">40\n<option value=\"45\">45\n<option value=\"50\">50\n<option value=\"60\">60\n<option value=\"90\">90\n<option value=\"120\">120\n<option value=\"150\">150\n<option value=\"200\">200\n</select> ��\n";
                $tempoutput1 =~ s/value=\"$regdisptime\"/value=\"$regdisptime\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333 ><b>ע������ʱ����ʾ����������ȷ��</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1<BR><BR></td>
                </tr>
                ~;

                $tempoutput1 = "<select name=\"regpuonoff\">\n<option value=\"ontop\">��ҳ����\n<option value=\"oneach\">ÿҳ����\n<option value=\"off\">������\n</select>\n";
                $tempoutput1 =~ s/value=\"$regpuonoff\"/value=\"$regpuonoff\" selected/;
                if(!$popupmsg){$popupmsg=qq~����ע���Ա�����Ӵ�����~;}
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333 ><b>�Ƿ񵯳�����ע���Ӵ�</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1<BR><BR></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333 ><b>���ѷÿ�ע���Ӵ�����</b> (֧Ԯ HTML,����Ҫע�ử�������)<BR><BR></font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="popupmsg" cols="40">$popupmsg</textarea><BR><BR></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳����</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boardname" value="$boardname"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳����</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boarddescription" value="$boarddescription"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳ LOGO</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boardlogos" value="$boardlogos"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳ URL ��ַ</b><br>��β��Ҫ�� "/"������Ҫ�� leobbs.cgi ֮���Ŷ</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boardurl" value="$boardurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ҳ����</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="homename" value="$homename"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��Ȩ��Ϣ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="copyrightinfo" value="$copyrightinfo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳������Ϣ��ֻ�������žͿ��ԣ�<BR>��Ҫ��������������ݣ����û�������գ�</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=18 name="beian" value="$beian" maxlength=18> ���磺��ICP��05023323��</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳״̬����ʾ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="statusbar" value="$statusbar"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ҳ��ַ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="homeurl" value="$homeurl"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>ͼƬĿ¼ URL</b><br>�ڽ�β��Ҫ�� "/images"</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="imagesurl" value="$imagesurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>ͼƬ����·��</b><br>��β�� "/"</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="imagesdir" value="$imagesdir"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�������·��</b><br>��β�� "/"</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="lbdir" value="$lbdir"></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emoticons\">\n<option value=\"off\">��ʹ��\n<option value=\"on\">ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$emoticons\"/value=\"$emoticons\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ�ñ����ַ�ת����</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"canchgfont\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$canchgfont\"/value=\"$canchgfont\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ����������ת����</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"avatars\">\n<option value=\"off\">��ʹ��\n<option value=\"on\">ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$avatars\"/value=\"$avatars\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ�ø���ͼƬ</b><br>ʹ�ø��Ի�ͼƬ��ÿ���û���ӵ�����Լ���ɫ��ͷ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳�ؼ���</b><br>���������̳��صĹؼ��֣�ÿ���ؼ���֮����Ӣ�ĵĶ��Ÿ��� ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newkeywords" value="$newkeywords" size=40 maxlength=100></td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>����Ϣ����</b>
                </font></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"allowusemsg\">\n<option value=\"on\">ʹ��\n<option value=\"off\">��ʹ��\n</select>";
                $tempoutput =~ s/value=\"$allowusemsg\"/value=\"$allowusemsg\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�����̳����Ϣ���ܣ�</b><br>��������Ϣ���ܣ���ʹ�������Ļ�Ա���ڻ��๵ͨ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>һ��Ⱥ��ѶϢ�������</font></b><br>�粻���ƣ�������</td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="maxsend" value="$maxsend" maxlength=3> �˹��ܶ԰�����̳����Ч</td>
                </tr>                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>����Ϣ�ռ�����Ϣ��������</font></b><br>�粻���ƣ�������</td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="maxmsgno" value="$maxmsgno" maxlength=3> �˹��ܶ԰�����̳����Ч</td>
                </tr>                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>ÿҳ��ʾ���ٶ���Ϣ</font></b></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="maxthread" value="$maxthread" maxlength=3> Ĭ��: 9 </td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Զ�ˢ�¶���Ϣ����ʱ��</font></b></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="infofreshtime" value="$infofreshtime" maxlength=3> ��(����Ϊ����Ҫ)</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"allowmsgattachment\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>";
                $tempoutput =~ s/value=\"$allowmsgattachment\"/value=\"$allowmsgattachment\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�����̳����Ϣ�������ܣ�</b><br>������� 60KB�������衣</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>�ʼ�����</b>
                </font></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emailfunctions\">\n<option value=\"off\">��ʹ��\n<option value=\"on\">ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$emailfunctions\"/value=\"$emailfunctions\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ���ʼ����ܣ�</b><br>�Ƽ���ʹ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
		$sendmailprog = mailprogram();

                $tempoutput = "<select name=\"emailtype\">\n<option value=\"smtp_mail\">SMTP\n<option value=\"esmtp_mail\">ESMTP\n<option value=\"directmail\">94cool �ؿ�ר��\n<option value=\"send_mail\">Sendmail\n<option value=\"blat_mail\">Blat\n</select>\n";
                $tempoutput =~ s/value=\"$emailtype\"/value=\"$emailtype\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ѡ��һ������ʹ�õ��ʼ�Э��</b><br>�Ƽ�ʹ�� SMTP������ͬʱ�� NT �� UNIX ��ʹ�á��� SENDMAIL ֻ���� UNIX ���ã�Blat ֻ���� NT ���á���Ҳ������ 94cool �ؿ�ר�ݣ�������ֱ�Ӱ��ż��ύ���Է����䣬���� Foxmail ���ؿ�ר�ݣ��ٶ��൱��(ע����ǣ���������������ƣ����ܻ��޷�ʹ�øù��ܣ�����Ժ���ȷ��)��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�����ʼ�����λ��</b><br>�����ʹ�õĲ��� Sendmail���벻Ҫ��д</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=30 name="SEND_MAIL" value="$SEND_MAIL"> ���Խ����$sendmailprog</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>SMTP ��λ��</b><br>�����ʹ�õĲ��� SMTP���벻Ҫ��д��һ����д�� ISP �ṩ�ķ��ŷ�������ַ</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="SMTP_SERVER" value="$SMTP_SERVER"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>SMTP �Ķ˿�</b><br>�����ʹ�õĲ��� SMTP���벻Ҫ��д��Ĭ��Ϊ 25</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=6 name="SMTP_PORT" value="$SMTP_PORT" maxlength=6></td>
                </tr>
				
				<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>ESMTP ���û���</b><br>�����ʹ�õĲ��� ESMTP���벻Ҫ��д</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="SMTPUSER" value="$SMTPUSER"></td>
                </tr>

                <tr>
				<td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>ESMTP ������</b><br>�����ʹ�õĲ��� ESMTP���벻Ҫ��д</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="SMTPPASS" value="$SMTPPASS"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>̳�������ʼ�ʹ�õ�����</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adminemail_in" value="$adminemail_in"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>̳�������ʼ�ʹ�õ�����</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adminemail_out" value="$adminemail_out"></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"passwordverification\">\n<option value=\"no\">��\n<option value=\"yes\">��\n</select>\n";
                $tempoutput =~ s/value=\"$passwordverification\"/value=\"$passwordverification\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ����ʼ�֪ͨ�û����룿</b><br>���鲻ʹ�á���Ҫʹ�ã���ȷ����������ġ��Ƿ�ʹ���ʼ����ܣ���������֤�㷢���ʼ���û������ġ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"adminverification\">\n<option value=\"no\">��\n<option value=\"yes\">��\n</select>\n";
                $tempoutput =~ s/value=\"$adminverification\"/value=\"$adminverification\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>���û�ע�ᣬ�Ƿ�������Ա��֤��</b><br>���鲻ʹ�á���Ҫʹ�ã�1,��ȷ����������ġ��Ƿ�ʹ���ʼ����ܣ���������֤�㷢���ʼ���û������ġ�2,ȷ���Ѿ���������ʼ�֪ͨ�û�����!</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"newusernotify\">\n<option value=\"no\">��\n<option value=\"yes\">��\n</select>\n";
                $tempoutput =~ s/value=\"$newusernotify\"/value=\"$newusernotify\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�����û�ע���Ƿ����ʼ�֪ͨ����</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"oneaccountperemail\">\n<option value=\"no\">��\n<option value=\"yes\">��\n</select>\n";
                $tempoutput =~ s/value=\"$oneaccountperemail\"/value=\"$oneaccountperemail\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>һ�� Email ֻ��ע��һ���˺ţ�</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>���ѡ��</b>
                </font></td>
                </tr>
		~;
	$adscript   =~ s/\[br\]/\n/isg;
	$adscriptmain   =~ s/\[br\]/\n/isg;
	$adfoot   =~ s/\[br\]/\n/isg;

               $tempoutput = "<select name=\"useadscript\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useadscript\"/value=\"$useadscript\" selected/; 
               print qq~ 

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳ���������д(���û�У�������)</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adscriptmain" rows="5" cols="40">$adscriptmain</textarea>
                </td>
                </tr>

               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=���� color=#333333><b>�Ƿ�ʹ����̳��ҳ���</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳ�����д</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adscript" rows="5" cols="40">$adscript</textarea>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"useadfoot\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useadfoot\"/value=\"$useadfoot\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=���� color=#333333><b>�Ƿ�ʹ����̳��ҳβ������</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳβ��������д</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adfoot" rows="5" cols="40">$adfoot</textarea><BR><BR>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"useimagead\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimagead\"/value=\"$useimagead\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=���� color=#333333><b>�Ƿ�ʹ����̳��ҳ�������</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳ�������ͼƬ(Flash) URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage" value="$adimage"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳ�����������Ŀ����ַ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink" value="$adimagelink"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳ�������ͼƬ���</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth" value="$adimagewidth" maxlength=3>&nbsp;����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳ�������ͼƬ�߶�</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight" value="$adimageheight" maxlength=3>&nbsp;����</td>
                </tr>
                ~;
                
               $tempoutput = "<select name=\"useimageadforum\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimageadforum\"/value=\"$useimageadforum\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=���� color=#333333><b>����̳�Ƿ�ʹ�ô˸������</b><BR>�������̳���Զ���ĸ�����棬<BR>��ô��ѡ����Ч</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput<BR><BR></td> 
               </tr>
		~;
               
               $tempoutput = "<select name=\"useimagead1\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimagead1\"/value=\"$useimagead1\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=���� color=#333333><b>�Ƿ�ʹ����̳��ҳ���¹̶����</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳ���¹̶����ͼƬ(Flash) URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage1" value="$adimage1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳ���¹̶��������Ŀ����ַ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink1" value="$adimagelink1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳ���¹̶����ͼƬ���</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth1" value="$adimagewidth1" maxlength=3>&nbsp;����</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳ���¹̶����ͼƬ�߶�</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight1" value="$adimageheight1" maxlength=3>&nbsp;����</td>
                </tr>
                ~;
                
               $tempoutput = "<select name=\"useimageadforum1\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimageadforum1\"/value=\"$useimageadforum1\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=���� color=#333333><b>����̳�Ƿ�ʹ�ô����¹̶����</b><BR>�������̳���Զ�������¹̶���棬<BR>��ô��ѡ����Ч</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=���� color=#990000><b>����ѡ��</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>֧���ϴ��ĸ�������</b><br>��,�ָ�</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="addtype" value="$addtype"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>���ÿ���ϴ���������</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=2 name="maxaddnum" value="$maxaddnum"> ���鲻Ҫ����10��</td>
                </tr>
                
                ~;
                $tempoutput = "<select name=\"COOKIE_USED\">\n<option value=\"0\">����·��ģʽ\n<option value=\"1\">��Ŀ¼ģʽ\n<option value=\"2\">�̶�ģʽ\n</select>\n";
                #<option value=\"0\">�Զ����Ŀ¼ģʽ\n
                $tempoutput =~ s/value=\"$COOKIE_USED\"/value=\"$COOKIE_USED\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ѡ�� Cookie ʹ�÷�ʽ��</B><br>Ĭ��ʹ������·��ģʽ������㷢����̳<BR>�û���¼���ǿ��˵Ļ�����ʹ��<BR>��Ŀ¼ģʽ��̶�ģʽ(�̶�ģʽ�����������һ������ʹ��)��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>Cookie �̶�ģʽ����</b><br>����̶���������·����ֻ�е�����ѡ������Ϊ�̶�ģʽ����Ч</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=20 name="mycookiepath" value="$mycookiepath"> <BR>(����ǰ��Ҫ�� http://�����Ҫ�� / �ţ����磺www.abc.com )</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"EXP_MODE\">\n<option value=\"\">��׼ģʽ\n<option value=\"0\">��ǿģʽ\n</select>\n";
                $tempoutput =~ s/value=\"$EXP_MODE\"/value=\"$EXP_MODE\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ѡ��ҳ����·�ʽ��</B><br>Ĭ��ʹ�ñ�׼ģʽ������㷢����̳˽��������ʱ��<BR>������ȷ����󻹱���ˢ�µĻ������޸�Ϊ��ǿģʽ��<BR>���������Ϊ��ǿģʽ����һЩ��ֵ�������Ļأ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"CACHE_MODES\">\n<option value=\"\">����ģʽ\n<option value=\"no\">�ܾ�ģʽ\n</select>\n";
                $tempoutput =~ s/value=\"$CACHE_MODES\"/value=\"$CACHE_MODES\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ѡ��ҳ���Ƿ񱣳ֻ��棡</B><br>Ĭ��ʹ�ÿ���ģʽ�����������̳������ֵĻ�������<BR>�����ֹ�ˢ�²��ܽ���Ļ������޸�Ϊ�ܾ�ģʽ��<BR>���������Ϊ�ܾ�ģʽ����һЩ��ֵ�������Ļأ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

    unless (WebGzip::getStatus()) {
	$gzipfunc = qq~Gzip ģ�����ʹ��~;
    }
    else {
    	$e = WebGzip::getStatus();
    	$gzipfunc = qq~<BR><font color=#FF0000>Gzip ģ�鲻���ã�</font> $e~ 
    }

                $tempoutput = "<select name=\"usegzip\">\n<option value=\"no\">�ر�\n<option value=\"yes\">��\n</select>\n ���Խ����$gzipfunc";
                $tempoutput =~ s/value=\"$usegzip\"/value=\"$usegzip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ѡ���Ƿ����Gzipѹ����</B><br>Ĭ�Ͽ��ţ�Gzip ������Ч��ѹ�������ҳ�棬��ҳ�洫��ĸ��죬��Ҳ������Ĳ�����Դ����������ԴҪ����ϣ���ô��ѡ��رգ�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"complevel\">\n<option value=\"9\">9\n<option value=\"8\">8\n<option value=\"7\">7\n<option value=\"6\">6\n<option value=\"5\">5\n<option value=\"4\">4\n<option value=\"3\">3\n<option value=\"2\">2\n<option value=\"1\">1\n</select>\n";
                $tempoutput =~ s/value=\"$complevel\"/value=\"$complevel\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ѡ��Gzipѹ������</B><br>9 ��ʾѹ������ߣ�1��ʾѹ������ͣ��������ѡ��ʹ�ã�</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"OS_USED\">\n<option value=\"Nt\">Windows ϵ��\n<option value=\"Unix\">Unix ϵ��\n<option value=\"No\">������\n</select>\n";
                $tempoutput =~ s/value=\"$OS_USED\"/value=\"$OS_USED\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ѡ�����ϵͳƽ̨�����ļ�����</b><BR>��ǧ��Ҫѡ������㲻��ȷ������ѡ�� Windows ϵ�У���<BR>�ļ�����������Ч�ķ�ֹ�������ݶ�ʧ�����⣬����Ӱ���ٶȣ����Լ�������<br></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"canotherlink\">\n<option value=\"no\">�������ⲿ����\n<option value=\"yes\">�����ⲿ����\n</select>\n";
                $tempoutput =~ s/value=\"$canotherlink\"/value=\"$canotherlink\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ��ֹ�ⲿ���ӳ������̳����</b><BR>�򿪵Ļ�������Ч��ֹ�ⲿ���ӵĳ����ˮ��ը����ɧ�ţ����п��ܻ�ͷ���ǽ��ͻ<br></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"useverify\">\n<option value=\"no\">������ʹ��\n<option value=\"yes\">����ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$useverify\"/value=\"$useverify\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ����֤��У��</b><br></font></td>
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
                $tempoutput = "<select name=\"verifyusegd\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$verifyusegd\"/value=\"$verifyusegd\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ�� GD ����ʾ��֤��</b><br></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
} else {
	print qq~<input type=hidden name="verifyusegd" value="no">~;
}

                $tempoutput = "<select name=\"floodcontrol\">\n<option value=\"off\">��\n<option value=\"on\">��\n</select>\n";
                $tempoutput =~ s/value=\"$floodcontrol\"/value=\"$floodcontrol\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ��ˮԤ�����ƣ�</b><br>ǿ���Ƽ�ʹ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�û����������ʱ��</b><br>��ˮԤ�����Ʋ���Ӱ�쵽̳�������</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=5 name="floodcontrollimit" value="$floodcontrollimit" maxlength=4> �� (һ������ 30 ����)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>ͬ IP ��ע����С���ʱ��</b><br>������Ч��ֹ��ˮע���</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=5 name="regcontrollimit" value="$regcontrollimit" maxlength=4> �� (һ������ 30 ����)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ʾ�༭��������Сʱ��</b><br>�ڸ�ʱ���ڶ����ӵı༭������</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=6 name="noaddedittime" value="$noaddedittime" maxlength=5> �� (Ĭ�� 60 ��)</td>
                </tr>
                
               <tr>
               <td bgcolor=#FFFFFF width=40%>
               <font face=���� color=#333333><b>��������Сʱ�����Ӳ������ٱ༭</b><br>�������ϼ�������</font></td>
               <td bgcolor=#FFFFFF>
               <input type=text size=3 name="noedittime" value="$noedittime" maxlength=2> Сʱ (���ղ�����)</td>
               </tr>
               
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>ɾ�����ڶ������ϵĻ�Ա��������������</b><br>���趨����Ӱ�쵽̳�������</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="deletepercent" value="$deletepercent" maxlength=3> % (һ������ 20% ���ң����������ƣ������� 0 ��հ�)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳����������������</b><br>���Կ��Ʒ���������Դʹ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=6 name="arrowonlinemax" value="$arrowonlinemax" maxlength=5> �� (һ���� 500 ���ң����������ƣ������� 99999)</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"timezone\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\">0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
                $tempoutput =~ s/value=\"$timezone\"/value=\"$timezone\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>������ʱ��</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>���ڵ�ʱ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="basetimes" value="$basetimes"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�û����������٣�</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=4 name="maxweiwang" value="$maxweiwang" maxlength=3> Ĭ��: 10(����С��5)</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�ڶ�����������ͬ���ӾͲ�⣿</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=4 name="maxadpost" value="$maxadpost" maxlength=3> Ĭ��: 4(����С��3)�����Ҫȡ���������� 999</td>
                </tr>
                ~;
		
		$tempoutput = "<select name=\"coolclickdisp\">\n<option value=\"0\">��ʹ��\n<option value=\"1\">ʹ��\n</select>\n";
		$tempoutput =~ s/value=\"$coolclickdisp\"/value=\"$coolclickdisp\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF width=40%>
		<font face=���� color=#333333><b>�Ƿ�ʹ�� LeoBBS ������ʹ�õĻ��������������ʾһ����������</font></td>
		<td bgcolor=#FFFFFF>
		$tempoutput</td>
		</tr>
		~;
		
		$tempoutput = "<select name=\"friendonlinepop\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
		$tempoutput =~ s/value=\"$friendonlinepop\"/value=\"$friendonlinepop\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF width=40%>
		<font face=���� color=#333333><b>���������Ƿ�֪ͨ��</font></td>
		<td bgcolor=#FFFFFF>
		$tempoutput</td>
		</tr>
		~;

		$tempoutput = "<select name=\"cpudisp\">\n<option value=\"0\">����ʾ\n<option value=\"1\">��ʾ\n</select>\n";
		$tempoutput =~ s/value=\"$cpudisp\"/value=\"$cpudisp\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF width=40%>
		<font face=���� color=#333333><b>�Ƿ���ʾ��̳ CPU ռ��ʱ�䡣(�����ö�̳����Ч)</font></td>
		<td bgcolor=#FFFFFF>
		$tempoutput</td>
		</tr>
		
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ʾ��̳ CPU ռ��ʱ���������ɫ</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=8 maxlength=7 name="cpudispcolor" value="$cpudispcolor"> Ĭ�ϣ�#c0c0c0</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"useemote\">\n<option value=\"no\">��ʹ��\n<option value=\"yes\">ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$useemote\"/value=\"$useemote\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ�� EMOTE ��ǩ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"announcements\">\n<option value=\"yes\">ʹ��\n<option value=\"no\">��ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$announcements\"/value=\"$announcements\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�ʹ����̳����</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
		
                $tempoutput = "<select name=\"refreshurl\">\n<option value=\"0\">�Զ����ص�ǰ��̳\n<option value=\"1\">�Զ����ص�ǰ����\n</select>\n";
                $tempoutput =~ s/value=\"$refreshurl\"/value=\"$refreshurl\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�����ظ����Ӻ��Զ�ת�Ƶ���</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"dispboardonline\">\n<option value=\"no\">����ʾ\n<option value=\"yes\">��ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispboardonline\"/value=\"$dispboardonline\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�����ҳ��ʾ����̳��ϸ�������</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"adminstyle\">\n<option value=\"2\">�����˵���ʾ\n<option value=\"1\">ƽ����ʾ\n<option value=\"3\">�Զ��ж�\n</select>\n";
                $tempoutput =~ s/value=\"$adminstyle\"/value=\"$adminstyle\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳������ʾ��ʽ</b><BR>���ѡ��ƽ����ʾ��ֻ����ʾǰ�������������ú���Ҫ��ջ���һ��</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"disphideboard\">\n<option value=\"no\">����ʾ\n<option value=\"yes\">��ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$disphideboard\"/value=\"$disphideboard\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ת��̳�����Ƿ���ʾ������̳</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispchildjump\">\n<option value=\"no\">����ʾ\n<option value=\"yes\">��ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispchildjump\"/value=\"$dispchildjump\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ת��̳�����Ƿ���ʾ����̳</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispboardsm\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispboardsm\"/value=\"$dispboardsm\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�����������ʾ��̳����</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"dispborn\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n<option value=\"auto\">�в���ʾ��������ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispborn\"/value=\"$dispborn\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ҳ�Ƿ���ʾ���������û�</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"sendtobirthday\">\n<option value=\"no\">������\n<option value=\"yes\">����\n</select>\n";
                $tempoutput =~ s/value=\"$sendtobirthday\"/value=\"$sendtobirthday\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�����������û�����ף����Ϣ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
		$tempoutput = "<select name=\"usetodaypostreply\">\n<option value=\"yes\">�ǵģ���¼\n<option value=\"no\">��������¼\n</select>\n";
                $tempoutput =~ s/value=\"$usetodaypostreply\"/value=\"$usetodaypostreply\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�ѻظ�Ҳ��¼��ÿ�շ�������</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"dispinfos\">\n<option value=\"yes\">��ʾ\n<option value=\"no\">����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispinfos\"/value=\"$dispinfos\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ҳ�Ƿ���ʾ����״̬���߿��ٵ�¼</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"displink\">\n<option value=\"no\">����ʾ\n<option value=\"yes\">��ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$displink\"/value=\"$displink\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ҳ�Ƿ���ʾ��ҳ����</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"displinkaddr\">\n<option value=\"1\">��ҳ�·�\n<option value=\"2\">��ҳ�Ϸ�\n</select>\n";
                $tempoutput =~ s/value=\"$displinkaddr\"/value=\"$displinkaddr\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ʾ��ҳ���ӵ�λ��</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��ҳ����</b><br>�� HTML �﷨��д��</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="links" cols="40" rows="6">$links</textarea><BR>
                </td>
                </tr>
                ~;

	$adlinks   =~ s/\[br\]/\n/isg;

		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳�����</b><br>�� HTML �﷨��д��</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adlinks" cols="40" rows="10">$adlinks</textarea><BR>
                </td>
                </tr>
                ~;


	$topicad   =~ s/\[br\]/\n/isg;

		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>���������</b><br>�� HTML �﷨��д��</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="topicad" cols="40" rows="10">$topicad</textarea><BR>
                </td>
                </tr>
                ~;

		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳����������</b><BR>����д�����������ղ���ȱ�κ�һ����</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="createyear" value="$createyear" size=4>��<input type=text name="createmon" value="$createmon" size=2>��<input type=text name="createday" value="$createday" size=2>�ա�(���ñ�׼�����ո�ʽ��������λ��ʾ)</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"dispprofile\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$dispprofile\"/value=\"$dispprofile\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ�������˲鿴�û�����</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"forumnamedisp\">\n<option value=\"0\">����ʾ\n<option value=\"1\">��ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$forumnamedisp\"/value=\"$forumnamedisp\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳��ҳ�Ƿ���ʾֱ�ӷ�����ť</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"canhidden\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$canhidden\"/value=\"$canhidden\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳�Ƿ������û�����</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispguest\">\n<option value=\"1\">��ϵͳ���ɶ���\n<option value=\"2\">��Զ��ʾ\n<option value=\"3\">��Զ����ʾ\n</select>\n";
                $tempoutput =~ s/value=\"$dispguest\"/value=\"$dispguest\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�����б����Ƿ���ʾ���ˣ�</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"userincert\">\n<option value=\"yes\">����\n<option value=\"no\">������\n</select>\n";
                $tempoutput =~ s/value=\"$userincert\"/value=\"$userincert\" selected/;
                print qq~

		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>������̳����������(��������Ŀ�Ŀ��˽�����ע��ſ��Է��ʡ��򿪴˹��ܺ󣬼ǵ���Ĭ�Ϸ�������аѡ��Ƿ�������������ֱ�ӷ��ʣ������ţ���������������ܻ���Ϊ���������������޷�������̳������ȷ������)</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=4 maxlength=4 name="maxguests" value="$maxguests"> �粻��Ҫ�˹��ܣ�������Ϊ�ջ�0</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��֤��̳�Ƿ�������ͨ�û����룿</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispmememail\">\n<option value=\"yes\">�����û�����Ҫ�������ʾ\n<option value=\"no\">ǿ�Ʋ���ʾ���е� Email ��ַ\n</select>\n";
                $tempoutput =~ s/value=\"$dispmememail\"/value=\"$dispmememail\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>��̳���Ƿ������е��û� Email ��</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"flashavatar\">\n<option value=\"no\">��֧��\n<option value=\"yes\">֧��\n</select>\n";
                $tempoutput =~ s/value=\"$flashavatar\"/value=\"$flashavatar\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�ϴ�ͷ���Ƿ�֧�� FLASH ��ʽ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�ϴ�ͷ���ļ���������ֵ(��λ��KB)</b><br>Ĭ��������� 200KB ��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxuploadava" value="$maxuploadava" size=5 maxlength=5>����Ҫ�� KB�����鲻Ҫ���� 200</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333><b>��̳��ҳ��������</b>(���û��������)<br>�����뱳���������ƣ���������<BR>Ӧ�ϴ��� non-cgi/midi Ŀ¼�¡�<br><b>��Ҫ���� URL ��ַ�����·����</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=20 name="midiaddr2" value="$midiaddr2">~;
                $midiabsaddr = "$imagesdir" . "midi/$midiaddr2";
                print qq~��<EMBED src="$imagesurl/midi/$midiaddr2" autostart="false" width=70 height=25 loop="true" align=absmiddle>~ if ((-e "$midiabsaddr")&&($midiaddr2 ne ""));
                print qq~
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>ֻ���������̳�ĵ���</b><br>����������� IP ���޷�������̳���������õ�����̳�ڲ��� IP ��ַ�⣬�����жϵĿ����ԣ�<B>���Ҵ�ѡ��� IP ��ֹ��Լ��</B>��</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="arrowformwhere" value="$arrowformwhere" size=20>����������ö��Ÿ��������л�ʡΪ��λ</td>
                </tr>
		~;

                $tempoutput = "<select name=\"usefake\">\n<option value=\"no\">��ʹ��\n<option value=\"yes\">ʹ��\n</select>\n";
                $tempoutput =~ s/value=\"$usefake\"/value=\"$usefake\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=���� color=#333333><b>�Ƿ����α��̬��ʽ�����忴˵������������֧�ֵĻ���ǧ��Ҫ�ã�</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput <a href=leobbs.htm target=_blank>���˲���</a>������ܿ�����̳��ҳ��˵��������������ȷ��<BR>����ʾ�ļ�û���ҵ����Ǿ�˵��δ������ȷ����ο�˵���ĵ��������ã�</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="�� ��"></form></td></tr></table></td></tr></table>
                ~;
                
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;

# ���� SENDMAIL ·��
sub mailprogram
{
    $mailprogram='/usr/sbin/sendmail';
    if (!(-e $mailprogram)) {$mailprogram='/usr/bin/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/bin/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/lib/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/usr/slib/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/usr/lib/sendmail';};
    if (!(-e $mailprogram)) {$mailprogram='perlmail';}; 
    if (!(-e $mailprogram)) {$mailprogram="Unknow";};
    return $mailprogram;
}
