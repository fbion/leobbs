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

$thisprog = "settemplate.cgi";

$query = new LBCGI;
#&ipbanned; #��ɱһЩ ip

$process = $query ->param("process");
$action  = $query ->param("action");

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

if ($process ne "preview template") {
   &admintitle;
}

&getmember("$inmembername","no");
        
        
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
   print qq(
   <tr><td bgcolor=#2159C9><font face=���� color=#FFFFFF>
   <b>��ӭ������̳�������� / �༭��̳ģ��</b>
   </td></tr>);

unless(defined($process)) {

   $templatefile = "$lbdir" . "data/template/$skin.cgi";

   if (-e $templatefile) {
      open (TEMPLATE, "$templatefile");
      local $/ = undef;
      $template_data = <TEMPLATE>;
      close (TEMPLATE);
      }
      else {
         print qq(<tr><td><font face="����" color="#FF0000">
                  <b>���ܹ��ҵ�ģ���ļ�</b><br>
                  ��ȷ���ļ� '$skin.cgi' �� *.cgi ����Ŀ¼�µ� 'data/template' Ŀ¼�У�
                  </td></tr></table></td></tr></table></body></html>);
         exit;
         } # end is it there

   unless (-w $templatefile) {
         print qq(<tr><td><font face="����" color="#FF0000">
                  <b>���ܹ�д��ģ���ļ�</b><br><br>
                  ��ȷ�� 'data/template/$skin.cgi' �ļ����������ó��� 666 ��
                  </td></tr></table></td></tr></table></body></html>);
         exit;
         }
      

   # If we're here, lets print out the template....

   ($non_editable, $user_editable) = split(/\<!--end Java-->/, $template_data);

   $non_editable =~ s/</&lt;/g;
   $non_editable =~ s/>/&gt;/g;
   $non_editable =~ s/\"/&quot;/g;
   $non_editable =~ s/\n\n/\n/ig;
   $non_editable =~ s/[\f\n\r]+/\n/ig;
   $non_editable =~ s/[\r \n]+$/\n/ig;
   $non_editable =~ s/^[\r\n ]+/\n/ig;
   $non_editable =~ s/\s+$//ig;

   $user_editable =~ s/</&lt;/g;
   $user_editable =~ s/>/&gt;/g;
   $user_editable =~ s/\"/&quot;/g;
   $user_editable =~ s/\n\n/\n/ig;
   $user_editable =~ s/[\f\n\r]+/\n/ig;
   $user_editable =~ s/[\r \n]+$/\n/ig;
   $user_editable =~ s/^[\r\n ]+/\n/ig;
   $user_editable =~ s/\s+$//ig;

   print qq(
   <tr>
   <td colspan=2>
   <form action="$thisprog" method=POST name="the_form">
   <input type="hidden" name="non_editable" value="$non_editable">
   <input type="hidden" name=process value="true">
   <textarea name="template_info" wrap="soft" cols="85" rows="20">
   $user_editable
   </textarea>
   <br><br>
   <input type="submit" value="ģ��Ԥ��" onclick="preview_template();">
   <input type="submit" value="����ģ��" onclick="save_changes();">
   </form>
   <br><hr color=#000000>
   <font face="����" color="#000000">
   <b>�༭ģ���ļ�����</b><br>
   ������������༭ģ���ļ������������CSS���벻Ҫ�Ķ�������ʹ�� <a href=setcss.cgi>��̳ CSS ��������</a>��   
   <br>
   ���� '\$lbboard_main' ��������ʾ��̳���ݣ� ��ͷ��һֱ��ҳ�װ�Ȩ��Ϣ���ӡ�
   ����԰� '\$lbboard_main' ����һ������ڣ����벻Ҫ�ı��������֣�
   <br><br>
   �������Ԥ����������� 'Ԥ��' ��ť��
   <br>
   <b>�뱣֤��û��ɾ�� &lt;/head&gt;,&lt;/body&gt; and &lt;/html&gt; ��ǩ��</b><br>
    ���û�� &lt;html&gt; ��ǩ����ô���������ͷ���Զ�������
   </td>
   </tr>
   );
   } # end if def(process)

   else {

      $template_info = $query -> param("template_info");
      $header_info   = $query -> param("non_editable");

      $header_info =~ s/&lt;/</g;
      $header_info =~ s/&gt;/>/g;
      $header_info =~ s/&quot;/\"/g;
      $header_info =~ s/\n\n/\n/ig;
      $header_info =~ s/[\f\n\r]+/\n/ig;
      $header_info =~ s/[\r\n ]+$/\n/ig;
      $header_info =~ s/^[\r\n ]+/\n/ig;
      $header_info =~ s/\s+$//ig;

      $template_info =~ s/&lt;/</g;
      $template_info =~ s/&gt;/>/g;
      $template_info =~ s/&quot;/\"/g;
      $template_info =~ s/\n\n/\n/ig;
      $template_info =~ s/[\f\n\r]+/\n/ig;
      $template_info =~ s/[\r \n]+$/\n/ig;
      $template_info =~ s/^[\r\n ]+/\n/ig;
      $template_info =~ s/\s+$//ig;

      if ($process eq "preview template") {

         print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

	 &title;

         $temp_board = qq(
         <table width=$tablewidth border=1 align=center><tr><td>
         $output
         <br><br><br><br><br>
         <font face="����" color=#000000>
         <center><h1>LeoBBS ��Ԥ�����</h1>
         ��ע�����û�û�д��룡<br>
         Ҫ����ģ�����ã��뷵�ع������ĵ�� '����ģ��'��
         <br><br>
         �����ϣ���༭��̳�Ŀ�ȣ������������ĵ� "���ṹ" �е� "�����ɫ" ģ�飬<BR>
         �޸� "���б����" ���ɣ���Ҳ���Խ������óɰٷֱ�(���磺90%)��<br>
         ������ٻص� "�༭��̳ģ��"������Ԥ����</center>
         <br><br><br><br><br><br><br>
         <table width=80% align=center cellpadding=3 cellspacing=0>
         <tr><td align=center valign=middle>
         <font face=���� color=#000000>
         <a href="http://www.leobbs.com" target=_blank>�װ��Ƽ�</a><br>&copy; 2000 LeoBBS.com
         </font></td></tr></table>
         <p></td></tr></table></body></html>);

         $template_info =~ s/\$lbboard_main/$temp_board\n/sg;

         print $header_info;
         print $template_info;

      }

      else {

         $templatefile = "$lbdir" . "data/template/$skin.cgi";

        &winlock($templatefile) if ($OS_USED eq "Nt");
         open (TEMPLATE, ">$templatefile");
         flock (TEMPLATE, 2) if ($OS_USED eq "Unix");
         print TEMPLATE "$header_info\n";
         print TEMPLATE "<!--end Java-->\n";
         print TEMPLATE $template_info;
         close (TEMPLATE);
        &winunlock($templatefile) if ($OS_USED eq "Nt");

         
         print "<tr><td><font face=����><b>����ģ����Ϣ�Ѿ�д��</b></font></td></tr>";
         }

      }


   } # end if logged in

   else {
      &adminlogin;
      }
                
   print qq(</table></td></tr></table></td></tr></table></body></html>) if ($process ne "preview template");
   exit;
