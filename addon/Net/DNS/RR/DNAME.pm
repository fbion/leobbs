package Net::DNS::RR::DNAME;

# $Id: DNAME.pm,v 1.1 2002/06/30 14:41:34 ctriv Exp $

use strict;
use vars qw(@ISA);

use Net::DNS::Packet;

@ISA = qw(Net::DNS::RR);

sub new {
	my ($class, $self, $data, $offset) = @_;

	if ($self->{"rdlength"} > 0) {
		my($dname) = Net::DNS::Packet::dn_expand($data, $offset);
		$self->{"dname"} = $dname;
	}

	return bless $self, $class;
}

sub new_from_string {
	my ($class, $self, $string) = @_;

	if ($string) {
		$string =~ s/\.+$//;
		$self->{"dname"} = $string;
	}

	return bless $self, $class;
}

sub rdatastr {
	my $self = shift;

	return exists $self->{"dname"} && $self->{"dname"}
	       ? "$self->{dname}."
	       : "; no data";
}

sub rr_rdata {
	my ($self, $packet, $offset) = @_;
	my $rdata = "";

	if (exists $self->{"dname"}) {
		$rdata = $packet->dn_comp($self->{"dname"}, $offset);
	}

	return $rdata;
}

1;
__END__

=head1 NAME

Net::DNS::RR::DNAME - DNS DNAME resource record

=head1 SYNOPSIS

C<use Net::DNS::RR>;

=head1 DESCRIPTION

Class for DNS Non-Terminal Name Redirection (DNAME) resource records.

=head1 METHODS

=head2 dname

    print "dname = ", $rr->dname, "\n";

Returns the DNAME target.

=head1 COPYRIGHT

Copyright (c) 1997-2001 Michael Fuhr.  All rights reserved.  This
program is free software; you can redistribute it and/or modify it
under the same terms as Perl itself. 

=head1 SEE ALSO

L<perl(1)>, L<Net::DNS>, L<Net::DNS::Resolver>, L<Net::DNS::Packet>,
L<Net::DNS::Header>, L<Net::DNS::Question>, L<Net::DNS::RR>,
RFC 2672

=cut