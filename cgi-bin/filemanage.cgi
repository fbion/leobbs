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
$LBCGI::POST_MAX = 1024 * 800;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 0;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";

$|++;
$thisprog = "filemanage.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$inmembername = cookie("adminname");
$inpassword   = cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
$data = $query->param('data');

&getadmincheck;
&getmember($inmembername);
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {
print qq~<tr><td bgcolor=#2159C9 colspan=2><font face=����  color=#FFFFFF>
<b>��ӭ������̳�������� / �ļ�������</b>
</td></tr>~;

&user_error ("����, Ϊ����̳�İ�ȫ, �˹�����δ����, <br>�����Ҫ����, ���޸� filemanage.cgi �ļ�,<br> �ѵ� 51 ��(&user_error ��ͷ��)ɾ��, Ȼ���ϴ����Ǽ���!", "");

#�������ļ���չ������Ӧ��ͼ���ļ��Ĺ������顣��Ҫ���ģ���ʽ�ճ���
%icons = (
           'ace'         => 'ace.gif',
           'class'       => 'applet.gif',
           'arj'         => 'arj.gif',
           'asp'         => 'asp.gif',
           'bmp'         => 'bmp.gif',
           'cab'         => 'cab.gif',
           'cgi'         => 'cgi.gif',
           'dll'         => 'dll.gif',
           'doc'         => 'doc.gif',
           'xls'         => 'excel.gif',
           'exe'         => 'exe.gif',
           'gif'         => 'gif.gif',
           'htm'         => 'htm.gif',
           'html'        => 'html.gif',
           'hwp'         => 'hwp.gif',
           'tif ico'     => 'img.gif',
           'jpg'         => 'jpg.gif',
           'jpeg'        => 'jpeg.gif',
           'mid'         => 'mid.gif',
           'fla swf'     => 'mov.gif',
           'mov'         => 'movie.gif',
           'mp3'         => 'mp3.gif',
           'mpeg'        => 'mpeg.gif',
           'mpg'         => 'mpg.gif',
           'pdf'         => 'pdf.gif',
           'pl'          => 'pl.gif',
           'png'         => 'png.gif',
           'ppt'         => 'ppt.gif',
           'ra rm'       => 'ra.gif',
           'rtf'         => 'rtf.gif',
           'js'          => 'script.gif',
           'wav'         => 'wav.gif',
           'sql'         => 'sql.gif',
           'tar'         => 'tar.gif',
           'txt'         => 'txt.gif',
           'torrent'     => 'torrent.gif',
           'gz'          => 'uuencoded.gif',
           'shtm shtml'  => 'html.gif',
           'au mod'      => 'sound1.gif',
           'zip'         => 'zip.gif',
           'vso'         => 'visio.gif',
           'rar'         => 'rar.gif',
           folder        => 'folder.gif',
           parent        => 'back.gif',
           unknown       => 'unknow.gif'
);

&main;

sub main {
        $working_dir = $query->param('wd');
        $filename    = $query->param('fn');
        $name        = $query->param('name');
        $newname     = $query->param('newname');
        $directory   = $query->param('dir');
        $newperm     = $query->param('newperm');
        $action      = $query->param('action');

        my ($error);
        ($working_dir, $error) = &is_valid_dir  ($working_dir); $error and &user_error ("��Ч��Ŀ¼: '$working_dir'. ԭ��: $error", "$lbdir/$working_dir");
        ($filename,    $error) = &is_valid_file ($filename);    $error and &user_error ("��Ч���ļ���: '$filename'. ԭ��: $error", "$lbdir/$working_dir");
        ($name,        $error) = &is_valid_file ($name);        $error and &user_error ("��Ч������: '$name'. ԭ��: $error", "$lbdir/$working_dir");
        ($newname,     $error) = &is_valid_file ($newname);     $error and &user_error ("��Ч���ļ���: '$newname'. ԭ��: $error", "$lbdir/$working_dir");
        ($newperm,     $error) = &is_valid_perm ($newperm);     $error and &user_error ("��Ч��Ȩ��: '$newperm'. ԭ��: $error", "$lbdir/$working_dir");

        ($directory, $error)   = &is_valid_dir  ($directory);   $error and &user_error ("��Ч��Ŀ¼: '$directory'. ԭ��: $error", "$lbdir/$working_dir");
        ($directory, $error)   = &is_valid_file ($directory);   $error and &user_error ("��Ч��Ŀ¼: '$directory'. ԭ��: $error", "$lbdir/$working_dir");

        my ($dir, $url);
        if ($working_dir) {
            $dir   = "$lbdir/$working_dir";
            $url   = "$boardurl/$working_dir";
        } else {
            $dir   = $lbdir;
            $url   = $boardurl;
        }

        my $javascript = qq~
<script language="Javascript">
<!-- Hide from old browsers
function validateFileEntry(validString, field) {
var isCharValid = true;
var inValidChar;
for (i=0 ; i < validString.length ; i++) {
  if (validString.charAt(0) == '.') {
    isCharValid = false;
    i=validString.length;
  }
  if (validateCharacter(validString.charAt(i)) == false) {
    isCharValid = false;
    inValidChar = validString.charAt(i);
    i=validString.length;
  }
}           
if (i < 1) { return false; }           
if (isCharValid == false) {
  if (inValidChar) { alert("��Ч���ļ���. ���ܺ��� '" + inValidChar + "'.");        }
  else             { alert("��Ч���ļ���. ����������."); }
  if (field)       { field.focus(); field.select(); }
    return false;
  }
  return true;
}

function validateCharacter(character) {
  if (character != '/' && character != '\') return true;
    else return false;
  }

function isNum(passedVal) {
  if (!passedVal) { return false }
  for (i=0; i<passedVal.length; i++) {
    if (passedVal.charAt(i) < "0") { return false }
    if (passedVal.charAt(i) > "7") { return false }
  }
  return true
}

function renameFile ( name ) {
  var newname = window.prompt("���� '" + name + "' Ϊ: ",'')
  if (newname != null) {
    if (validateFileEntry(newname)) {
      window.location.href = "filemanage.cgi?action=rename&name=" + name + "&newname=" + newname +"&wd=$working_dir"
    }
  }
}

function deleteFile ( name ) {
  if (window.confirm("�������ɾ���ļ�'" + name + "'��?")) {
    window.location.href = "filemanage.cgi?action=delete&fn=" + name + "&wd=$working_dir"
  }
}

function deleteDir ( name ) {        
  if (window.confirm("�������ɾ��Ŀ¼'" + name + "'��?")) {
    window.location.href = "filemanage.cgi?action=removedir&dir=" + name + "&wd=$working_dir"
  }
}        

function changePermissions ( name ) {
  var newperm = window.prompt("�ı��ļ�'" + name + "' ��Ȩ��Ϊ: ",'')
  if (newperm == null) {  return;  }
  if (!isNum(newperm) || (newperm == "") || (length.newperm > 2)) {
    alert ("ֻ��Ҫ��������! ����˽��Ƶ�Ȩ������. �� 755.")
  } else {
    window.location.href = "filemanage.cgi?action=permissions&name=" + name + "&newperm=" + newperm +"&wd=$working_dir"
  }
}
        
function serverFileName() {
  var fileName = window.document.Upload.data.value.toLowerCase();
  window.document.Upload.fn.value = fileName.substring(fileName.lastIndexOf("\\\\") + 1,fileName.length);
}
// -->
</script>
~;                

        my $nojavascript = qq~        
<noscript>
<table bgcolor="#FFFFFF" cellpadding=5 cellspacing=3 width=100% valign=top><tr><td><font color="red"><B>ע��:&nbsp;&nbsp; </B></font><FONT COLOR="black">��������Ŀǰ <font color="red"><b>�ر��� JavaScript ����</b></font> -- �ļ������� ����ʹ�� JavaScript.���������Ĳ���ѡ����, Ȼ�� <b>���� JavaScript ����</b>. ����԰� <b>ˢ��</b> ��ť������ʹ�� �ļ�������.</FONT></td></tr></table>
</noscript>
~;

        print qq~
<html>
<head>
<title>�ļ�������</title>
$javascript
</head>
<body bgcolor="#DDDDDD">
<center>

<table border="0" bgcolor="#FFFFFF" cellpadding="2" cellspacing="1" width="98%" align="center" valign="top">
<tr><td>
~;

        my ($result);
        CASE: {
                ($action eq 'write')           and do {
                                                         $result = &write ($dir, $filename, $data, $url);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'delete')          and do {
                                                         $result = &delete ($dir, $filename);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'makedir')         and do {
                                                         $result = &makedir    ($dir, $directory);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'removedir')       and do {
                                                         $result = &removedir  ($dir, $directory);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'rename')          and do {
                                                         $result = &rename_file ($dir, $name, $newname);
                                                         &list_files   ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'edit')            and do {
                                                         &edit ($dir, $filename, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'upload')          and do {
                                                         my $file_space;
                                                         ($file_space, $result) = &upload ($dir, $data, $filename);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                ($action eq 'permissions')     and do {
                                                         $result = &change_perm ($dir, $name, $newperm);
                                                         &list_files ($result, $working_dir, $url);
                                                         last CASE;
                                                      };
                do {
                      print $nojavascript;
                      &list_files ('�г��ļ���Ŀ¼.', $working_dir, $url);
                };
        };
        print qq~</td></tr></table>
  </body>
</html>
~;
}

sub list_files {
        my ($message, $working_dir, $url) = @_;
        my ($directory)   = "$lbdir/$working_dir";

        print qq~
                <P>
                <table bgcolor="#FFFFFF" cellpadding=5 cellspacing=3 width=100% valign=top>
                        <tr>
                                <td><B>Ŀ¼��Ӧ:&nbsp;&nbsp; <a href="$url"><FONT COLOR="blue">$url</font></A></B></td>
                                <td align="right"><a href="filemanage.cgi">���� CGI ��Ŀ¼</a>&nbsp;&nbsp;&nbsp;&nbsp;</td><td>&nbsp;</td>
                        </tr>
                        <tr>
                                <td>����: <font color=red><B>$message</B></font><br></td><td><br></td>
                                <td align="right"></td>
                        </tr>
                </table>
        </td></tr>
        <tr><td>
                <P>
                <table bgcolor="#FFFFFF" cellpadding=5 cellspacing=3 width=100% valign=top>
        ~;

        opendir (DIR, $directory);
        my @ls = readdir(DIR);
        closedir (DIR);

        my (%directory, %text, %graphic);
        my ($temp_dir, $newdir, @nest, $fullfile, $filesize, $filedate, $fileperm, $fileicon, $file);

        FILE: foreach $file (@ls) {
                next FILE if  ($file eq '.');
                next FILE if (($file eq '..') and ($directory eq "$lbdir/"));

                $fullfile = "$directory/$file";
                ($filesize, $filedate, $fileperm) = (stat($fullfile))[7,9,2];
                $fileperm = &print_permissions ($fileperm);
                $filesize = &print_filesize    ($filesize);
                $filedate = &get_date($filedate);

                if (-d $fullfile ) {
                        if ($file eq '..') {
                                @nest = split (/\//, $working_dir);
                                (pop (@nest)) ? 
                                        ($newdir = "filemanage.cgi?wd=" . join ("/", @nest)) :
                                        ($newdir = "filemanage.cgi");                                
                        }
                        else {
                                $working_dir ? ($temp_dir = "$working_dir%2F$file") : ($temp_dir = "$file");
                                $newdir   = "filemanage.cgi?wd=$temp_dir";
                        }
                        $newdir = $query->uri_escape($newdir);
                        if ($file eq '..') {
                                $fileicon = "$imagesurl/icon/$icons{'parent'}";
                                $directory{$file}  = qq~ <tr>\n~;
                                $directory{$file} .= qq~     <td><b><a href="$newdir"><img src="$fileicon" align=middle border=0></a></td> \n~;
                                $directory{$file} .= qq~     <td><a href="$url/$file"><font color=blue>$file</font></a></b></td> \n~;
                                $directory{$file} .= qq~     <td><font color="gray">$fileperm</font></td> \n~;
                                $directory{$file} .= qq~     <td>$filedate</td> \n~;
                                $directory{$file} .= qq~     <td></td>~;
                                $directory{$file} .= qq~     <td><b><a href="$newdir"><font color=black>��һ��</font></a></B></td>
                                                                                         <td><br></td></tr>
                                                                        ~;                        
                        }
                        else {
                                $fileicon = "$imagesurl/icon/$icons{'folder'}";
                                $directory{$file}  = qq~ <tr>\n~;
                                $directory{$file} .= qq~     <td><b><a href="$newdir"><img src="$fileicon" align=middle border=0></a></td> \n~;
                                $directory{$file} .= qq~     <td><a href="$newdir"><font color=blue>$file</font></a></td> \n~;
                                $directory{$file} .= qq~     <td><a href="javascript:changePermissions('$file')"><font color="gray">$fileperm</font></a></td> \n~;
                                $directory{$file} .= qq~     <td>$filedate</td> \n~;
                                $directory{$file} .= qq~     <td></td>~;
                                $directory{$file} .= qq~     <td>&nbsp;</td>\n~;
                                $directory{$file} .= qq~     <td><a href="javascript:deleteDir('$file')"><font color=red>ɾ��</font></A></td><td><a href="javascript:renameFile('$file')"><font color=purple>����</font></a></td>\n~;
                                $directory{$file} .= qq~ </tr>\n~;                                
                        }
                }
                elsif (-T $fullfile) {
                        $fileicon = &get_icon($fullfile);
                        $text{$file}  = qq~  <tr>\n~;
                        $text{$file} .= qq~      <td><b><a href="$url/$file"><img src="$fileicon" align=middle border=0></a></td> \n~;
            		$text{$file} .= qq~      <td><a href="$url/$file"><font color=blue>$file</font></a></td> \n~;
                        $text{$file} .= qq~      <td><a href="javascript:changePermissions('$file')"><font color="gray">$fileperm</font></a></td> \n~;
                        $text{$file} .= qq~      <td>$filedate</td> \n~;
                        $text{$file} .= qq~      <td><b>$filesize</font></b></td> \n~;
                        $text{$file} .= qq~      <td><a href="filemanage.cgi?action=edit&fn=$file&wd=$working_dir"><font color=green>�༭</font></a></td>~;
                        $text{$file} .= qq~      <td><a href="javascript:deleteFile('$file')"><font color=red>ɾ��</font></a></td>
                                                 <td><a href="javascript:renameFile('$file')"><font color=purple>����</font></a></td></tr>
                        		~;
                }
                else {
                        $fileicon = &get_icon($fullfile);
                        $graphic{$file}  = qq~  <tr>\n~;
                        $graphic{$file} .= qq~      <td><b><a href="$url/$file"><img src="$fileicon" align=middle border=0></a></td> \n~;
                        $graphic{$file} .= qq~      <td><a href="$url/$file"><font color=blue>$file</font></a></td>              \n~;
                        $graphic{$file} .= qq~      <td><a href="javascript:changePermissions('$file')"><font color="gray">$fileperm</font></a></td> \n~;
                        $graphic{$file} .= qq~      <td><i>$filedate</font></i></td> \n~;
                        $graphic{$file} .= qq~      <td><b>$filesize</font></b></td> \n~;
                        $graphic{$file} .= qq~      <td><br></td>
                                                    <td><a href="javascript:deleteFile('$file')"><font color=red>ɾ��</font></a></td>
                                                    <td><a href="javascript:renameFile('$file')"><font color=purple>����</font></a></td></tr>
                        		   ~;
                }
        }
        foreach (sort keys %directory) {
                print $directory{$_};
        }
        foreach (sort keys %text) {
                print $text{$_};
        }
        foreach (sort keys %graphic) {
                print $graphic{$_};
        }

               print qq~
                        </table>
                </td></tr>
                <tr><td>                        
                        <table cellpadding=5 cellspacing=3 width=80% valign=top>
                                <tr><td align="left" valign="top" width=50%>
                                        <form method=post action="filemanage.cgi" name="createfile">
                                                <input type=hidden name="action" value="edit">
                                                <input type=hidden name="wd"     value="$working_dir">
                                                <font color="black"><B>����һ�����ĵ�:</B><br>�ļ���: <input type=text name="fn" onBlur="validateFileEntry(this.value, this)" >
                                                <input type=submit value="�����ļ�"></font>
                                        </form>
                                </td><td align="left" rowspan=2 valign="top" width=50%>
                                        <form method=post action="filemanage.cgi">
                                                <input type=hidden name="action" value="makedir">
                                                <input type=hidden name="wd"     value="$working_dir">
                                                <font color="black"><B>����һ����Ŀ¼:</B><br>Ŀ¼��: <input type=text name="dir" onBlur="validateFileEntry(this.value, this)" >
                                                <input type=submit value="����Ŀ¼"></font>
                                        </form>
                                </td></tr><tr><td valign="top" align="left">
                                        <form method=post action="filemanage.cgi" NAME="Upload" ENCTYPE="multipart/form-data">
                                                <input type=hidden name="wd"     value="$working_dir">
                                                <input type=hidden name="action" value="upload">
                                                <font color="black"><B>�ϴ�һ���ļ�:</B><br>
                                                        �����ļ���: <INPUT NAME="data" TYPE="file" onBlur="serverFileName()"><br>
                                                        Զ���ļ���: <INPUT NAME="fn" onFocus="select()" onBlur="validateFileEntry(this.value, this)">
                                                <input type="submit" value="�ϴ�"></font>
                                        </form>
                                </td></tr>
                        </table>
                ~;

}

sub delete {
        my ($directory, $filename) = @_;
        my ($fullfile);

        (!$filename) and return "ɾ���ļ�: û�������ļ���!";

        ($directory =~ m,/$,) ? ($fullfile = "$directory$filename") : ($fullfile = "$directory/$filename");

        if (&exists($fullfile)) {
                unlink ($fullfile) ?
                        return "ɾ���ļ�: '$filename' �ѱ�ɾ��." :
                        return "ɾ���ļ�: '$filename' ���ܱ�ɾ��. �����ļ�����.";
        }
        else {
                return "ɾ���ļ�: '$filename' ���ܱ�ɾ��. �Ҳ����ļ�.";
        }
}

sub edit {
        my ($directory, $filename, $working_dir, $url) = @_;
        my ($lines, $fullfile, $full_url);

        (!$filename) and return "�༭�ļ�: û�������ļ���!";

        ($directory =~ m,/$,) ? ($fullfile = "$directory$filename") : ($fullfile = "$directory/$filename");
        $full_url   = "$url/$filename";

        if (&exists($fullfile)) {
                open (DATA, "<$fullfile");
                $lines = join ("", <DATA>);
                $lines =~ s/<\/TEXTAREA/<\/TEXT-AREA/ig;
                close DATA;
                print qq!<p>�༭ <a href="$full_url"><B>$filename</B></A> ����Ҫ�޸ĵĲ���:</p>!;
        }
        else {
                $lines = qq~
<HTML>
<HEAD>
<TITLE></TITLE>
</HEAD>
        
<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#FF0000" VLINK="#800000" ALINK="#FF00FF">
        
</BODY>
</HTML>
                ~;
                print "<p>����һ�����ļ�. �������������HTML����:</p>";
        }

        print qq~
                <p><blockquote>
                        ��ɱ༭��, ѡ�� "�����ĵ�" ������ <B>$filename</B> ���������˵�
                        .
                </blockquote></p>

                <form method=post action="filemanage.cgi">
                <textarea name="data" rows=40 cols=60 wrap=virtual>$lines</textarea>

                <p>���Ϊ�ļ���:
                           <input type=text name="fn" value="$filename"><br>
                                (��������һ���ļ������᲻�ı� <B>$filename</B>
                                �����ݣ�������������ݽ��ᱣ��Ϊ�������������ļ���. ע�⣬�����������ļ�Ҳ���ڵĻ�, �����ᱻ����.)<P>
                        <input type=hidden name="action" value="write">
                        <input type=hidden name="wd"     value="$working_dir">
                        <input type=submit               value="�����ĵ�">
                </form>
                </p>                
        ~;
}

sub write {
        my ($directory, $filename, $data, $url) = @_;
        my ($fullfile, $new);

        (!$filename) and return "�༭�ļ�: û�������ļ���!";        

        ($directory =~ m,/$,) ? ($fullfile = "$directory$filename") : ($fullfile = "$directory/$filename");

        $new = 1;
        (&exists($fullfile)) and ($new = 0);

        $data =~ s,</TEXT-AREA,</TEXTAREA,ig;

        open(FILE,">$fullfile");
                print FILE $data;
        close(FILE);

        if (&exists($fullfile)) {
                ($new eq 'yes') ?
                        return ("�༭�ļ�: '$filename' �ѱ�����.") :
                        return ("�༭�ļ�: '$filename' �ѱ��༭.");
        }
        else {
                return  ("�༭�ļ�: ���ܱ��� '$filename'. ����Ȩ��.");
        }
}

sub upload {
        my ($directory, $data, $filename) = @_;
        my ($bytesread, $buffer, $fullfile, $file_size);

        if (!$filename) {
             $filename = $data =~ m|([^/:\\]+)$|;
	}
        ($directory =~ m,/$,) ?
                ($fullfile = "$directory$filename") :
                ($fullfile = "$directory/$filename");
        $file_size = 0;

	my $buffer;
        open    (OUTFILE, ">$fullfile");
        binmode (OUTFILE);        # For those O/S that care.
        binmode ($data); #ע��
        while (read($data,$buffer,4096)) {
                print OUTFILE $buffer;
                $file_size += 4096;
        }
        close OUTFILE;
        close ($data); #ע��
        &exists($fullfile) ?
                return (int($file_size / 1000), "�ϴ��ļ�: '$filename' ���ϴ�.") :
                return (int($file_size / 1000), "�ϴ��ļ�: �����ϴ� '$filename'. ����Ȩ��.");
}

sub makedir {
        my ($root, $new) = @_;
        my ($fulldir);

        (!$new) and return "����Ŀ¼: ����������Ŀ¼����!";

        ($root =~ m,/$,) ? ($fulldir = "$root$new") : ($fulldir = "$root/$new");

        if (&exists($fulldir)) {
                return "����Ŀ¼: '$new' �Ѿ�����.";
        }
        else {
                mkdir ($fulldir, 0755) ?
                        return "����Ŀ¼: '$new' Ŀ¼�ѽ���." :
                        return "����Ŀ¼: ���ܽ���Ŀ¼. ����Ȩ��.";
        }
}

sub removedir {
        my ($root, $new) = @_;
        my ($fulldir);

        (!$new) and return "ɾ��Ŀ¼: û������Ŀ¼��!";

        ($root =~ m,/$,) ? ($fulldir = "$root$new") : ($fulldir = "$root/$new");

        if (!&exists($fulldir)) {
                return "ɾ��Ŀ¼: '$new' ������.";
        }
        else {
                rmdir($fulldir) ?
                        return "ɾ��Ŀ¼: '$new' �ѱ�ɾ��." :
                        return "ɾ��Ŀ¼: '$new' <B>����</B> ɾ��. ���Ŀ¼�Ƿ�Ϊ��.";
        }
}

sub rename_file {
        my ($directory, $oldfile, $newfile) = @_;

        (!$oldfile or !$newfile) and return "����: ԭ�ļ�����Ŀ���ļ�������������!";

        my ($full_oldfile, $full_newfile);
        ($directory =~ m,/$,) ?
                ($full_oldfile = "$directory$oldfile"  and $full_newfile = "$directory$newfile") :
                ($full_oldfile = "$directory/$oldfile" and $full_newfile = "$directory/$newfile");

        (&exists($full_oldfile)) or  return "����: ԭ�ļ� '$oldfile' ������.";
        (&exists($full_newfile)) and return "����: ���ļ� '$newfile' �Ѵ���.";

        rename ($full_oldfile, $full_newfile);
        return "����: '$oldfile' �ѱ�����Ϊ '$newfile'.";
}

sub change_perm {
        my ($directory, $file, $newperm) = @_;
        my ($full_filename, $octal_perm);
        
        (!$file)    and return "�ı�Ȩ��: û�������ļ���!";
        (!$newperm) and        return "�ı�Ȩ��: û�������µ�Ȩ��!";

        $full_filename = "$directory/$file";
        (&exists($full_filename)) or return "�ı�Ȩ��: '$file' ������.";

        $octal_perm = oct($newperm);
        chmod ($octal_perm, $full_filename);
        return "�ı�Ȩ��: '$file' Ȩ���ѱ��ı�.";
}

sub print_permissions {
        my $octal  = shift;
        my $string = sprintf "%lo", ($octal & 07777);
        my $result = '';
        foreach (split(//, $string)) {
                if    ($_ == 7) { $result .= "rwx "; }
                elsif ($_ == 6) { $result .= "rw- "; }
                elsif ($_ == 5) { $result .= "r-x "; }
                elsif ($_ == 4) { $result .= "r-- "; }
                elsif ($_ == 3) { $result .= "-wx "; }
                elsif ($_ == 2) { $result .= "-w- "; }
                elsif ($_ == 1) { $result .= "--x "; }
                elsif ($_ == 0) { $result .= "--- "; }
                else            { $result .= "unkown '$_'!"; }
        }
        return $result;
}

sub print_filesize {
        
        my $size = shift;
        my $formatted_size = int($size / 1000) . " KB";
        $formatted_size == 0 ?
                return "$size Byte" :
                return $formatted_size;
}

sub exists {
        return -e shift;
}

sub get_icon {
        my ($file) = lc(shift);
        my ($ext)  = $file =~ /\.([^.]+)$/;
        if (!$ext) { return "$imagesurl/icon/$icons{'unknown'}"; }
        foreach (keys %icons) {
                next if (/folder/);
                next if (/unknown/);
                next if (/parent/);
                ($_ =~ /$ext/i) and return "$imagesurl/icon/$icons{$_}";
        }
        return "$imagesurl/icon/$icons{'unknown'}";
}

sub get_date {
        my $time = shift;
        $time or ($time = time);
        my @months = qw!1 2 3 4 5 6 7 8 9 10 11 12!;

        my ($min, $hr, $day, $mon, $yr) = (localtime($time))[1,2,3,4,5];
        $yr = $yr + 1900;
        ($min < 10) and ($min = "0$min");
        ($hr  < 10) and ($hr  = "0$hr");
        ($day < 10) and ($day = "0$day");

        return "$yr-$months[$mon]-$day $hr:$min";

}

sub is_valid_file {
        my ($file, $okfile) = "";
        $file = shift;
	$okfile = $file;
        if ($file =~ m/[\/|\\]/) { return ($dir, "�ļ������зǷ��ַ�. ����ʹ�� ������ �� С����."); }

        ($file =~ m,\.\.,)   and return ($file, "����������������С�������ļ����� .");
        ($file =~ m,^\.,)    and return ($file, "С���㲻�����ļ�����ͷ��.");
        (length($file) > 20) and return ($file, "�ļ���̫��. �뱣���� 20 ���ַ�����.");

        return ($okfile, "");
}

sub is_valid_dir {
        my ($dir, $okdir, $last_dir) = "";
        $dir = shift;

        my (@size) = split (/\//, $dir);
        $last_dir  = pop (@size);
	$okdir = $dir;
        if ($dir =~ m/[\/|\\]/) { return ($dir, "Ŀ¼�����зǷ��ַ�. ����ʹ�� ������ �� С����."); }

        ($dir =~ m,\.\.,)   and return ($dir, "����������������С�������ļ����� .");
        ($dir =~ m,^/,)                  and return ($dir, "Ŀ¼��ǰ������ / ��.");
        ($dir =~ m,/$,)                  and return ($dir, "Ŀ¼�������� / ��.");
        ($#size > 4)                     and return ($dir, "Ŀ¼��̫��.");
        (length($last_dir) > 25) and return ($dir, "Ŀ¼��̫��. �뱣���� 25 ���ַ�����.");

        return ($okdir, "");
}

sub is_valid_perm {
        my ($perm) = shift;
        (!$perm)                                             and return ($perm, "");
        ($perm =~ /^([0-7][0-7][0-7])$/) or return ($perm, "Ȩ��ֵֻ��Ϊ��λ����, 0 to 7.");        
        return ($1, "");
}

sub user_error {
        my ($error, $wd) = @_;

        print qq~
<html>
<head>
        <title>�ļ�������</title>
</head>

<body bgcolor="#DDDDDD">
        <center>
             <table bgcolor="#FFFFFF" cellpadding=2 cellspacing=1 width="630" align=center valign=top>
                        <tr><td colspan=3>
                                <p><b>����!</b> �������д���: </p>
                                <p><blockquote><font color=red><b>$error</b></font></blockquote></p>
                                <p>�밴��������� <a href="javascript:history.go(-1)">����</a> �����ز���������.</p>
                        </td></tr>
                        <tr><td colspan=3>
                        </td></tr>
                </table>
        </center>
</body>
</html>
        ~;
        exit;
}

} else {
    &adminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;
