package Net::DNS::RR::CNAME;

# $Id: CNAME.pm,v 1.3 2002/10/23 21:36:08 ctriv Exp $

use strict;
use vars qw(@ISA);

use Net::DNS::Packet;

@ISA = qw(Net::DNS::RR);

sub new {
	my ($class, $self, $data, $offset) = @_;

	if ($self->{"rdlength"} > 0) {
		my($cname) = Net::DNS::Packet::dn_expand($data, $offset);
		$self->{"cname"} = $cname;
	}

	return bless $self, $class;
}

sub new_from_string {
	my ($class, $self, $string) = @_;

	if ($string) {
		$string =~ s/\.+$//;
		$self->{"cname"} = $string;
	}

	return bless $self, $class;
}

sub rdatastr {
	my $self = shift;

	return exists $self->{"cname"} && $self->{"cname"}
	       ? "$self->{cname}."
	       : "; no data";
}

sub rr_rdata {
	my ($self, $packet, $offset) = @_;
	my $rdata = "";

	if (exists $self->{"cname"}) {
		$rdata = $packet->dn_comp($self->{"cname"}, $offset);
	}

	return $rdata;
}

# rdata contains a compressed domainname... we should not have that.
sub _canonicalRdata {	
	my ($self) = @_;

	return $self->_name2wire($self->{"cname"});
}

1;
__END__

=head1 NAME

Net::DNS::RR::CNAME - DNS CNAME resource record

=head1 SYNOPSIS

C<use Net::DNS::RR>;

=head1 DESCRIPTION

Class for DNS Canonical Name (CNAME) resource records.

=head1 METHODS

=head2 cname

    print "cname = ", $rr->cname, "\n";

Returns the RR's canonical name.

=head1 COPYRIGHT

Copyright (c) 1997-1998 Michael Fuhr.  All rights reserved.  This
program is free software; you can redistribute it and/or modify it
under the same terms as Perl itself. 

=head1 SEE ALSO

L<perl(1)>, L<Net::DNS>, L<Net::DNS::Resolver>, L<Net::DNS::Packet>,
L<Net::DNS::Header>, L<Net::DNS::Question>, L<Net::DNS::RR>,
RFC 1035 Section 3.3.1

=cut