#!/usr/bin/perl

############################################
# Discus �û����� --> LeoBBS �û�����ת����#
############################################

$discusmember = "/path/to/UBB members dir/";   	# ���� Discus �û��������ڵ�Ŀ¼�ľ���·�������Ҫ��© / ��
$leobbsmember = "/path/to/leobbs members dir/"; # ������ LeoBBS �û��������ڵ�Ŀ¼�ľ���·�������Ҫ��© / ��ע������ 777 ���ԡ�

$date = time();
print "Content-Type: text/html\n\n";
print "<html><body>";
print "<center><h1><b><u>�û�ת�� ��Discus --> LeoBBS��</u></b></h1><br><br><br><br><br><br><br><center><h2><b>��ʼ����</b></h2>";
open(DATEI,"${discusmember}user.txt") || die "Discus �û���û���ҵ�";
@memberlist=<DATEI>;
close(DATEI);
mkdir(newmember,0777);
$i=0;
$point=0;
foreach $zeile (@memberlist)
{
$i++;
$point++;
print "<b>.<b>";
if ($point > 100)
{
print "<br>";
$point = 0
}
$zeile =~ tr/[:]/[|]/;
@member = split(/\|/,$zeile);
$name = @member[0];
$passwort = @member[1];
$email = @member[2];
$filenames = $name;
$filenames =~ s/ /_/gi;
$filenames =~ tr/A-Z/a-z/;

$memberarray = "$name\t$passwort\tMember\tme\t0|0\t$email\tno\t\thttp://\t\t\t\t\t$date\tNot Posted\t\t\t\tnoavatar\t";
@memberarray = ($memberarray);
open(MEMBERDATEI,">${leobbsmember}$filenames.cgi");
print MEMBERDATEI "@memberarray";
close(MEMBERDATEI);
}
print "<BR><BR>�ܹ�ת���� $i ���û���<BR><BR>\n";
exit;
