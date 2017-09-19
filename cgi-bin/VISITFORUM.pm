#####################################################
#  LEO SuperCool BBS / LeoBBS X / �װ����ᳬ����̳  #
#####################################################
# ����ɽӥ(��)������ȱ������ LB5000 XP 2.30 ��Ѱ�  #
#   �°�������� & ��Ȩ����: �װ��Ƽ� (C)(R)2004    #
#####################################################
#      ��ҳ��ַ�� http://www.LeoBBS.com/            #
#      ��̳��ַ�� http://bbs.LeoBBS.com/            #
#####################################################

package VISITFORUM;
use strict;

use vars qw(@ISA @EXPORT);
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(getlastvisit setlastvisit);

sub getlastvisit {
    my $lv = $main::query->cookie("templastvisit");
    unless ($lv) {
	$lv = $main::query->cookie("lastvisit");
	$lv = "${main::inforum}-${main::currenttime}--" unless ($lv);
	$main::tempvisitcookie = main::cookie(-name=>"templastvisit", -path=>"${main::cookiepath}/", -expires=>"+30d", -value=>$lv);
    }
    my @pairs = split(/\--/, $lv);
    foreach (@pairs) {
	my ($n, $val) = split(/\-/, $_);
	$main::lastvisitinfo{$n} = $val;
    }
    return;
}

sub setlastvisit {
    my $tinfo = shift;
    my ($tid, $tv, $mv) = split(/\,/, $tinfo);
    my @newv = ();
    my $u = "0";
    my @pairs = split(/\--/, $main::query->cookie("lastvisit"));
    foreach (@pairs) {
	my ($n, $val) = split(/\-/, $_);
	if ($tid eq $n) {
	    $u = "1";
	    $val = $tv;
	}
	push(@newv, "$n-$val--");
    }

    push(@newv,"$tid-$tv--") if ($u eq "0" && $tinfo ne "");
    my $nfo = join("", @newv);
    $main::permvisitcookie = main::cookie(-name=>"lastvisit", -value=>$nfo, -path=>"${main::cookiepath}/", -expires => "+30d");
    $main::tempvisitcookie = main::cookie(-name=>"templastvisit", -value =>$nfo, -expires =>"+30d", -path=>"${main::cookiepath}/") if ($mv eq "1");
    return;
}

1;