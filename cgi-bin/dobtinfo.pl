#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

    $addme = qq~<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&type=.$up_ext><img src=$imagesurl/icon/$filetype.gif border=0 width=16><a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&type=.$up_ext>��������һ�� BitTorrent ��ʽ���ļ�����������</a> (�� $fileinfo[7] �ֽ�)<br>~;

    open(FILE, "${imagesdir}$usrdir/$inforum/$up_name.$up_ext.btfile");
    sysread(FILE, $btinfo,(stat(FILE))[7]);
    close(FILE);
    $btinfo =~ s/\r//isg;

    chomp($btinfo);

    if (length($btinfo) <= 50) {
	eval("use BTINFO;");
	if ($@ eq "") {
		$/ = "";
		open(FILE, "${imagesdir}$usrdir/$inforum/$up_name.$up_ext");
		binmode(FILE);
		my $bufferall = <FILE>;
		close(FILE);
		$/ = "\n";
		my $btfileinfo = process_file($bufferall);
		my (undef, $hash, $announce) = split(/\n/, $btfileinfo);
		open(FILE, ">${imagesdir}$usrdir/$inforum/$up_name.$up_ext.btfile");
		print FILE "$btfileinfo\|$seedinfo";
		close(FILE);
		$btinfo = "$btfileinfo\|$seedinfo";
	}
    }
    
    my ($btfileinfo, $hash, $seedinfo) = split(/\n/, $btinfo);
    ($announce, $seeds, $leeches, $downloaded) = split (/\|/, $seedinfo);
    if ($seeds eq "") {
	$seeds = "δ֪";
	$leeches = "δ֪";
	$downloaded = "δ֪";
    }

my @btfileinfo = split (/\t/, $btfileinfo);
$addme .= qq~
<script>
function ShowMore(){
for (var i = 0; i < AFILE.length; i++){var e = AFILE[i];e.style.display = "";}
var _S = BFILE;
_S.style.display = "none";
}
</script>
<ul><table cellSpacing=1 cellPadding=4 bgColor=$tablebordercolor width=280><tr bgColor=$titlecolor><td align=middle nowrap><font color=$titlefontcolor>�ļ���</td><td align=middle nowrap><font color=$titlefontcolor>�ļ���С</td></tr>~;

my $allfilelength = 0;
my $counters = 0;
foreach (@btfileinfo) {
    next if ($_ eq "");
    $counters++;
    if ($counters % 2 == 1) {
	$postbackcolor1 = $postcolorone;
	$postfontcolor1 = $postfontcolorone;
    } else {
	$postbackcolor1 = $postcolortwo;
	$postfontcolor1 = $postfontcolortwo;
    }
    my ($filename, $filelength) = split (/\|/, $_);
    $allfilelength += $filelength;

    $lbsd = 'Bytes';
    if ($filelength > 1024) {
	$filelength /= 1024;
	$lbsd = 'KB';
    }
    if($filelength > 1024) {
	$filelength /= 1024;
	$lbsd = 'MB';
    }
    if($filelength > 1024) {
	$filelength /= 1024;
	$lbsd = 'GB';
    }
    $filelength = sprintf("%6.2f",$filelength) . " $lbsd";

    if ($counters eq 8 ) { $addme1 .= qq~ id=AFILE style=display:none~; }

    $addme .= qq~<tr bgColor=$postbackcolor1 $addme1><td align=middle nowrap><font color=$postfontcolor1>$filename</td><td align=middle nowrap><font color=$postfontcolor1>$filelength</td></tr>~;
}
if ($counters >= 8 ) { $addme .= qq~<tr bgColor=$postbackcolor1 id=BFILE style=display:""><td align=right nowrap colspan=2><span style=CURSOR:hand onclick=ShowMore()><font color=$postfontcolor1 title=��ʾ�����ļ�>����...</font></span>&nbsp;</td></tr>~; }

($announce, $seeds, $leeches, $downloaded) = split (/\|/, $seedinfo);
if ($seeds eq "") {
    $seeds      = "δ֪";
    $leeches    = "δ֪";
    $downloaded = "δ֪";
}
$lbsd = 'Bytes';
if ($allfilelength > 1024) {
    $allfilelength /= 1024;
    $lbsd = 'KB';
}
if($allfilelength > 1024) {
    $allfilelength /= 1024;
    $lbsd = 'MB';
}
if($allfilelength > 1024) {
    $allfilelength /= 1024;
    $lbsd = 'GB';
}
$allfilelength = sprintf("%6.2f",$allfilelength) . " $lbsd";

$addme .= qq~<tr bgColor=$titlecolor><td align=right nowrap colspan=2>��������$seeds��&nbsp;��������$leeches��&nbsp;�������$downloaded&nbsp;<BR>[<a href=getbtinfo.cgi?forum=$inforum&filename=$up_name target=_blank title="���˿ɻ�ü�ʱ���������ݣ������ʾ����\n�����������ǶԷ��������޷����ӡ�">��ҳ�����ݲ��Ǽ�ʱ������Ҫ��ʱ��Ϣ�밴����</a>]&nbsp;<br>�ܹ��� $counters ���ļ������ݹ��� $allfilelength&nbsp;<br>URL: $announce&nbsp;<br></td></tr></table></ul>~;
1;
