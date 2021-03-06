#!/usr/bin/perl
#############################################################
#
#  多附件上传 For LeoBBS (主文件)
#           
#  主页地址: http://www.CGIer.com/      
#  BY 路杨(Easun Studio) 20040401
#############################################################
BEGIN {
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

#   $ENV{'TMP'}="$LBPATH/lock"; #如果你不能上传，请去掉前面的#
#   $ENV{'TEMP'}="$LBPATH/lock";#如果你不能上传，请去掉前面的#
#   $ENV{'TMPDIR'}="$LBPATH/lock";#如果你不能上传，请去掉前面的#

use LBCGI;
$LBCGI::POST_MAX=40000000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;

require "data/boardinfo.cgi";
require "data/styles.cgi";

require "bbs.lib.pl";
require "dopost.pl"; ###自定义的pl /BY 路杨

$|++;
$thisprog = "upfile.cgi"; 

$query = new LBCGI;
&ipbanned; #封杀一些 ip

if ($COOKIE_USED eq 1) {$cookiepath ="";}
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}

$inmembername   = $query->cookie("amembernamecookie");
$inpassword     = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
  

$addme=$query->param('addme');
$forum=$query->param('forum');
$topic=$query->param('topic');
$inforum       = $forum;
$intopic       = $topic;

if ($intopic ne "") {$tmpurl="&topic=$intopic";}
$gourl1=qq~<meta http-equiv="refresh" content="3; url=$thisprog?action=uppic&forum=$forum$tmpurl"> [ <a href=$thisprog?action=uppic&forum=$forum$tmpurl>3 秒钟自动返回</a> ]~;
$gourl=qq~ [ <a href=$thisprog?action=uppic&forum=$forum$tmpurl>按此返回</a> ]~;

print header(-charset=>gb2312);

if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }
$maxupload = 300 if ($maxupload eq "");

if (($intopic) && ($intopic !~ /^[0-9]+$/)) {&thisout("<b>请以正确的方式访问本程序1！</b>") ;}
if ($inforum ne "" && $inforum !~ /^[0-9]+$/) {&thisout("<b>请以正确的方式访问本程序2！</b>");};

if (!(-e "${lbdir}boarddata/listno$inforum.cgi")) { &thisout ("<b>对不起，此分论坛不存在！如果确定分论坛号码没错，那么请进入管理区修复此分论坛一次！</b>"); }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&thisout("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($inmembername eq "" || $inmembername eq "客人" ) {
    $inmembername = "客人";
    $userregistered = "no";
    &thisout("<b>请先登陆才能上传文件！</b>")
} else {
    
    &getmember("$inmembername");
    &thisout("<b>普通错误,此用户根本不存在！</b>") if ($inpassword ne "" && $userregistered eq "no");
     if ($inpassword ne $password && $userregistered ne "no") {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &thisout("<b>密码与用户名不相符，请重新登录</b>！");
     }
}

$action=$query->param('action');

my %Mode = (
    'uppic'       => \&uppic,
    'doupfile'    => \&doupfile,
    'delup'    => \&delup,
);

    if ($Mode{$action}) { $Mode{$action}->(); }
    else { &thisout("<b>请以正确的方式访问本程序3！</b>"); }

exit;

##该功能只做iframe调用，呵呵：）_BY 路杨

sub uppic #界面
{
  $addtypedisp = $addtype;
  $addtypedisp =~ s/\, /\,/gi;
  $addtypedisp =~ s/ \,/\,/gi;
  $addtypedisp =~ tr/A-Z/a-z/;
  my @addtypedisp = split(/\,/, $addtypedisp);
  $addtypedisp = "<select><option value=#>支持类型：</option><option value=#>----------</option>";
  foreach (@addtypedisp)
  {
     chomp $_;
     next if ($_ eq "");
     $addtypedisp .= qq~<option>$_</option>~;
  }
  $addtypedisp .= qq~</select>~;

$thisoutput = qq~
<form action="$thisprog" method="post" enctype="multipart/form-data" name=UPFORM>
<input type=hidden name="action" value="doupfile">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<input type="file" size=26 name="addme" > <input type=submit value="立 即 上 传"> 　　$addtypedisp~;
&thisout("$thisoutput");
exit;
}

sub doupfile #上传
{
  # $addme=$query->upload('addme'); #如果CGI.pm版本>2.47，推荐使用
  $addme=$query->param('addme'); #如果CGI.pm版本<2.47，用他替换上句
  $forum=$query->param('forum');
  $topic=$query->param('topic');
  $inforum       = $forum;
  $intopic       = $topic;

  &moderator($inforum); #获得权限

  my $thispath=&getusrdir; #临时目录

  &thisout("<b>目前您未被发布的附件临时文件已经有$filesno个，达到了论坛设置的最大数目($maxaddnum)，<BR>请不要一次上传太多附件，谢谢配合与合作!</b>$gourl") if ($thispath eq 'ERR');

    opendir (DIRS, "${lbdir}");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^CGItemp/i, @files);
    my $ci = 0;
    foreach (@files) {
    	unlink ("${lbdir}$_") if ((-M "${lbdir}$_") *86400 > 3600);
    	$ci ++;
    	last if ($ci > 20);
    }
        $mypath= ${lbdir};
        $mypath=~ s/\/$//isg;
        $mypath=substr($mypath,0,rindex($mypath,"/"));
        $mypath=~ s/\\/\//g;

    opendir (DIRS, "$mypath");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^CGItemp/i, @files);
    my $ci = 0;
    foreach (@files) {
    	unlink ("$mypath/$_") if ((-M "$mypath/$_") *86400 > 3600);
    	$ci ++;
    	last if ($ci > 20);
    }
        $mypath=~ s/\/$//isg;
        $mypath=substr($mypath,0,rindex($mypath,"/"));
        $mypath=~ s/\\/\//g;

    opendir (DIRS, "$mypath");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^CGItemp/i, @files);
    my $ci = 0;
    foreach (@files) {
    	unlink ("$mypath/$_") if ((-M "$mypath/$_") *86400 > 3600);
    	$ci ++;
    	last if ($ci > 20);
    }

  if (($addme)&&(($arrowupload ne 'off')||($membercode eq 'ad')||($membercode eq 'smo')||($inmembmod eq 'yes'))) {
           $uploadreqire = 0 if ($uploadreqire < 0);
           if (($membercode ne 'ad')&&($membercode ne 'smo')&&($membercode ne 'amo')&&($membercode ne 'cmo')&&($membercode ne 'mo')&&($membercode !~ /^rz/)&&($inmembmod ne 'yes')&&(($numberofposts+$numberofreplys) < $uploadreqire)) {
               &thisout("上传出错，你必须发帖总数达到 <B>$uploadreqire</B> 才能在本区上传！$gourl");
           }


          my ($tmpfilename) = $addme =~ m|([^/:\\]+)$|; #注意,获取文件名字的形式变化
    #     $tmpfilename =~s/([^\w.-])/_/g;
    #     $tmpfilename =~s/(^[-.]+)//;
          my @filename = split(/\./,$tmpfilename); #注意
          $up_name = $filename[0];
          $up_ext = $filename[-1];
          $up_ext = lc($up_ext);

           my $checkadd=0;
           for (split(/\,\s*/,$addtype)){
               $checkadd=1,last if ($up_ext eq lc($_));
           }
           &thisout("上传出错，为了安全，不支持你所上传的附件，请重新选择！$gourl") if ($up_ext eq "exe"||$up_ext eq "com"||$up_ext eq "pl"||$up_ext eq "cgi"||$up_ext eq "asp"||$up_ext eq "php"||$up_ext eq "php3"||$up_ext eq "phtml"||$up_ext eq "jsp"||$up_ext eq "cfml"||$up_ext eq "dll");
           &thisout("上传出错，不支持你所上传的附件或者图片，请重新选择！$gourl") if ($checkadd==0);
           my $filesize=0;
           my $bufferall;

           my $tmpfilename=&gettmpname(${up_name}); #注意
            open (FILE,">$thispath/$tmpfilename.$up_ext");
           binmode ($addme); #注意
           binmode (FILE);
           while (((read($addme,$buffer,4096)))&&!(($filesize>$maxupload)&&($membercode ne "ad"))) {
               if ($up_ext eq "txt"||$up_ext eq "cgi"||$up_ext eq "pl"||$up_ext eq "php3"||$up_ext eq "phtm"||$up_ext eq "phtml"||$up_ext eq "htm"||$up_ext eq "html"||$up_ext eq "asp"||$up_ext eq "php"||$up_ext eq "shtml"||$up_ext eq "phtml"||$up_ext eq "jsp"){
                   $buffer=~s/\.cookie/\&\#46\;cookie/isg;
                   $buffer =~ s/on(mouse|exit|error|click|key)/\&\#111\;n$1/isg;
                   $buffer=~s/script/scri\&\#112\;t/isg;
                   $buffer =~ s/style/\&\#115\;tyle/isg;
               }
               print FILE $buffer;
               $bufferall .= $buffer if ($up_ext eq 'torrent');
               $filesize=$filesize+4;
           }
           close (FILE);
          close ($addme); #注意

        #############torrent分析################
	    if ($up_ext eq "torrent") {
	    	if (($bufferall !~ /announce/i)||($bufferall !~ /length/i)||($bufferall !~ /info/i)||($bufferall !~ /^d/i)) {
	    	    unlink ("$thispath/$tmpfilename.$up_ext");
	    	    &thisout("上传出错，你上传的这个文件不是 .torrent 文件格式$bufferall，请查实后重新上传！$gourl");
	    	}
	    	else {
		    eval("use BTINFO;");
		    if ($@ eq "") {
			my $btfileinfo = process_file($bufferall);
			my (undef, $hash, $announce) = split(/\n/, $btfileinfo);
			if ($hash eq "" || $announce eq "") {
			    unlink ("$thispath/$tmpfilename.$up_ext");
	    		    &thisout("上传出错，你上传的这个文件不是 .torrent 文件格式，请查实后重新上传！$gourl");
			}
			my $seedinfo = output_torrent_data($hash, $announce);
                        open (FILE,">$thispath/$tmpfilename.$up_ext.btfile");
			print FILE "$btfileinfo\|$seedinfo";
			close(FILE);
		    }
		    else { &thisout("上传出错，$@！");}
		}
	    }
       #######################################################################

        #############利用##use Image::Info qw(image_info);################
        if ($up_ext eq "gif"||$up_ext eq "jpg"||$up_ext eq "bmp"||$up_ext eq "jpeg"||$up_ext eq "png"||$up_ext eq "ppm"||$up_ext eq "svg"||$up_ext eq "xbm"||$up_ext eq "xpm") {
          eval("use Image::Info qw(image_info);"); 
          if ($@ eq "") 
          {
    	    my $info = image_info("$thispath/$tmpfilename.$up_ext");
	    if ($info->{error} eq "Unrecognized file format"){
                unlink ("$thispath/$tmpfilename.$up_ext");
                &thisout("上传出错，上传文件不是图片文件，请上传标准的图片文件！$gourl"); 
            }
            undef $info;
          }
       }  
       #######################################################################

    if (($filesize>$maxupload)&&($membercode ne "ad")) {
        unlink ("$thispath/$tmpfilename.$up_ext");
        &thisout("上传出错，上传文件大小超过$maxupload KB，请重新选择！$gourl");
    }

       $delurl =qq~$thisprog?action=delup&name=$tmpfilename&ext=${up_ext}&forum=$inforum~;   
       $addit2span = qq~ <div id=${tmpfilename}_${up_ext}>附件:$up_name.$up_ext [<span style=cursor:hand onClick=\\"jsupfile('$tmpfilename.$up_ext');FORM.inpost.focus()\\">再次插入帖子</span>]</div>~;
       $thisoutput .= qq~<b>上传成功</b> $gourl1<SCRIPT> var p_showupfile= parent.document.getElementById("showupfile"); var s = p_showupfile.innerHTML; s+="$addit2span"; p_showupfile.innerHTML =s; var p_inpost= parent.document.FORM.inpost; var upname='[UploadFile$imgslt=$tmpfilename.$up_ext]';var o_value=p_inpost.value; o_value += upname; p_inpost.value = o_value;</SCRIPT>~;

   }else {$thisoutput .= qq~<b>您没有上传文件，请上传文件！$gourl</b>~;}

    &thisout("$thisoutput");
    exit;

}



sub delup #删除
{

   # exit if (;)
   $forum=$query->param('forum');
   $inforum  = $forum;
   my $thispath = &getusrdir(1);

   opendir (DIRS, "$thispath");
   my @files = readdir(DIRS);
   closedir (DIRS);

   foreach (@files) {
       chomp $_;
       unlink ("$thispath/$_");
   }

$js=qq~<SCRIPT>parent.showupfile.innerHTML ="";</SCRIPT>~;

   $thisoutput .= qq~<b>你已经上传的，但还尚未发布的附件临时文件已经全部删除</b>!$gourl1 $js~;
   &thisout("$thisoutput");
   exit;   

}
sub thisout { ##不用模版的print函数

eval { close ($addme); }; #注意
$templatefile = "${lbdir}data/template/$skin.cgi";
if (-e $templatefile) {
    open (TEMPLATE, "<$templatefile");
    local $/ = undef;
    $template_data = <TEMPLATE>;
    close (TEMPLATE);
    ($non_editable, $user_editable) = split(/\<!--end Java-->/, $template_data);
    ($pastcss, $other_editable) = split(/\<!--end css info-->/, $user_editable);
    $pastcss =~ s/\$imagesurl/${imagesurl}\/images/isg;
} else {
    $pastcss="
<style>
BODY {BACKGROUND-ATTACHMENT: fixed; }
td { FONT-SIZE: 9pt}
p {FONT-SIZE: 9pt}
textarea, select {border-width: 1; font-size: 9pt; font-style: bold;}
A:link {COLOR: #000000; TEXT-DECORATION: none}
A:visited {COLOR: #000000; TEXT-DECORATION: none}
A:hover {COLOR: #333333; TEXT-DECORATION: underline}
table {FONT-SIZE: 9pt}
</style>";
}

my $lockjs=qq~
<script>
if(top==self) {
var parent1 = "leobbs.cgi";
var appVer = navigator.appVersion;
var NS = (navigator.appName == 'Netscape') && ((appVer.indexOf('3') != -1) || (appVer.indexOf('4') != -1));
var MSIE = (appVer.indexOf('MSIE 4') != -1);
if (NS || MSIE)
location.replace(parent1);
else
location.href = parent1;
}
</script>
~;

    my $tmpoutput=qq~<head><title>$skin $title</title><meta http-equiv="Content-Type" content="text/html; charset=gb2312">$pastcss$lockjs</head><body alink=#333333 vlink=#333333 link=#333333 leftmargin=0 topmargin=0><!-- oncontextmenu="return false;" ondragstart="return false;" onselectstart ="return false" --><table cellspacing=0 cellpadding=0 border=0 width=100% height=100%><tr><td bgcolor=$miscbackone>$_[0]  </td></tr></table>~;print $tmpoutput; exit;
}
