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
use ExifTool;
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;

require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
	$boardurltemp =$boardurl;
	$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
	$cookiepath = $boardurltemp;
	$cookiepath =~ s/\/$//;
#	$cookiepath =~ tr/A-Z/a-z/;
}

$inforum	= $query -> param('forum');
$intopic	= $query -> param('topic');
$inreply	= $query -> param('reply');
$intype		= $query -> param('ftype');
$inname		= $query -> param('fname');
$inname =~ s/\.\.//sg;
$inname =~ s/\///sg;
$inname =~ s/\\//sg;
$inname = substr($inname,0,32) if (length($inname)>32);

$out = "";
$out = "�ϴ󣬱��Һ��ҵĳ���ѽ��1"  if ($inreply ne "" && $inname ne "");
$out = "�ϴ󣬱��Һ��ҵĳ���ѽ��2"  if ($inreply ne "" && $inname ne "");
$out = "�ϴ󣬱��Һ��ҵĳ���ѽ��3" if ($inreply !~ /^[0-9]+$/ && $inreply ne "");
$out = "�ϴ󣬱��Һ��ҵĳ���ѽ��4" if (($inforum !~ /^[0-9]+$/)||($intopic !~ /^[0-9]+$/));
$out = "�ϴ󣬱��Һ��ҵĳ���ѽ����" unless (($intype eq "gif")||($intype eq "jpg")||($intype eq "jpe")||($intype eq "jpeg")||($intype eq "tif")||($intype eq "png")||($intype eq "bmp"));

if ($out eq "") {

if ($inreply ne "") {
$inreply --;
if ($inreply eq 0) { $img= "${imagesdir}$usrdir/$inforum/$inforum\_$intopic\.$intype"; } else { $img= "${imagesdir}$usrdir/$inforum/$inforum\_$intopic\_$inreply\.$intype"; }
$inreply ++;
$dispinfo = $inreply;
}
else {
     $tmptopic = $intopic%100;
     $img= "${imagesdir}$usrdir/$inforum/$tmptopic/$inname\.$intype";
     $dispinfo = $inname;
}
my $tags = ExifTool::ImageInfo("$img");

$name{"Make"} ="����";
$name{"Model"} ="�ͺ�";
$name{"Artist"} ="����";
$name{"DateTimeOriginal"} ="����ʱ��";
$name{"CreateDate"} ="����ʱ��";
$name{"DateTimeDigitized"} ="���ֻ�ʱ��";
$name{"ModifyDate"} ="�޸�ʱ��";
$name{"FileSize"} ="�ļ���С";
$name{"FileSource"} ="�ļ���Դ";
$name{"Software"} ="���";
$name{"ExifImageWidth"} ="����ֱ��ʿ�";
$name{"ExifImageLength"} ="����ֱ��ʸ�";
$name{"ImageWidth"} ="ͼ����";
$name{"ImageHeight"} ="ͼ��߶�";
$name{"ImageSize"} ="ͼ���С";
$name{"ExposureTime"} ="�ع�ʱ��";
$name{"ShutterSpeed"} ="����";
$name{"ShutterSpeedValue"} ="����ֵ";
$name{"FNumber"} ="FNumber ��Ȧ";
$name{"Aperture"} ="Aperture ��Ȧ";
$name{"ApertureValue"} ="��Ȧֵ";
$name{"MaxApertureValue"} ="����Ȧֵ";
$name{"FocalLength"} ="����";
$name{"FocalLengthIn35mmFormat"} ="35mm ����";
$name{"FocalLength35efl"} ="35mm ����";
$name{"DigitalZoomRatio"} ="����佹��";
$name{"FocusMode"} ="�佹ģʽ";
$name{"ExposureMode"} ="�ع�ģʽ";
$name{"ExposureCompensation"} ="�عⲹ��";
$name{"ExposureIndex"} ="�ع�ָ��";
$name{"ExposureProgram"} ="�ع����";
$name{"BrightnessValue"} ="����";
$name{"ISO"} ="ISO �й��";
$name{"Sharpness"} ="���";
$name{"Contrast"} ="�Աȶ�";
$name{"Saturation"} ="���Ͷ�";
$name{"LightSource"} ="��Դ";
$name{"ColorSpace"} ="ɫ϶";
$name{"Flash"} ="�����";
$name{"Slowsync"} ="�����ģʽ";
$name{"WhiteBalance"} ="��ƽ��";
$name{"MeteringMode"} ="���ģʽ";
$name{"CustomRendered"} ="�Զ��岹��";
$name{"ComponentsConfiguration"} ="�ɷֹ���";
$name{"YCbCrPositioning"} ="ɫ�ඨλ";
$name{"SceneType"} ="��������";
$name{"Orientation"} ="����";
$name{"Compression"} ="ѹ����ʽ";
$name{"CompressedBitsPerPixel"} ="ѹ����";
$name{"Quality"} ="ѹ������";
$name{"XResolution"} ="X ����ֱ���";
$name{"YResolution"} ="Y ����ֱ���";
$name{"ResolutionUnit"} ="�ֱ��ʵ�λ";
$name{"FlashPixVersion"} ="FlashPix �汾";
$name{"ExifVersion"} ="Exif �汾";
$name{"Macro"} ="��ָ��";
$name{"Version"} ="����汾";
$name{"Comment"} ="���˵��";

foreach ("Make","Model","Artist","DateTimeOriginal","CreateDate","DateTimeDigitized","ModifyDate","FileSize","FileSource","Software","ExifImageWidth","ExifImageLength","ImageWidth","ImageHeight","ImageSize","ExposureTime","ShutterSpeed","ShutterSpeedValue","FNumber","Aperture","ApertureValue","MaxApertureValue","FocalLength","FocalLengthIn35mmFormat","FocalLength35efl","DigitalZoomRatio","FocusMode","ExposureMode","ExposureCompensation","ExposureIndex","ExposureProgram","BrightnessValue","ISO","Sharpness","Contrast","Saturation","LightSource","ColorSpace","Flash","Slowsync","WhiteBalance","MeteringMode","CustomRendered","ComponentsConfiguration","YCbCrPositioning","SceneType","Orientation","Compression","CompressedBitsPerPixel","Quality","XResolution","YResolution","ResolutionUnit","FlashPixVersion","ExifVersion","Macro","Version","Comment") {
    next if (($tags->{$_} eq "")||(length($tags->{$_}) > 30));
    $outfontcolor = "$postfontcolorone" if ($outfontcolor eq "$postfontcolortwo");
    $out .= "<font color=$outfontcolor>&nbsp;&nbsp;&nbsp;&nbsp;$name{$_}";
    $spaceit="&nbsp;" x (26-length($name{$_}));
    $out .= "$spaceit$tags->{$_}</font><BR>";
}

foreach (sort (keys %$tags)) {
    next if (($_ eq "MakerNoteUnknown")||($_ eq "FileName"));
    next if (length($tags->{$_}) > 30);
    next if ($name{$_} ne "");
    next if (($tags->{$_} eq "")||($tags->{$_} eq " ")||($tags->{$_} eq "  ")||($tags->{$_} eq "  "));
    $outfontcolor = "$postfontcolorone" if ($outfontcolor eq "$postfontcolortwo");
    $out .= "<font color=$outfontcolor>&nbsp;&nbsp;&nbsp;&nbsp;$_";
    $spaceit="&nbsp;" x (26-length($_));
    $out .= "$spaceit$tags->{$_}</font><BR>";
}
$out =~ s/\n//g;
$out =~ s/\'/\\\'/g;
}
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print <<"HTML";
<html>
<head> 
<title>ͼƬ��Ϣ</title>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
</head>
<body>
<SCRIPT>
<!--
//��ʼ������ֵ
parent.followTd$dispinfo.innerHTML='$out';
//�Ѷ�ȡ
parent.document.images.followImg$dispinfo.loaded='yes';
-->
</SCRIPT>
</body>
</html>
HTML

exit;
