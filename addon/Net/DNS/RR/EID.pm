package Net::DNS::RR::EID;

# $Id: EID.pm,v 1.2 2002/02/13 03:53:59 ctriv Exp $

use strict;
use vars qw(@ISA);

use Net::DNS::Packet;

@ISA = qw(Net::DNS::RR);

sub new {
	my ($class, $self, $data, $offset) = @_;
	return bless $self, $class;
}

1;
__END__

=head1 NAME

Net::DNS::RR::EID - DNS EID resource record

=head1 SYNOPSIS

C<use Net::DNS::RR>;

=head1 DESCRIPTION

Class for DNS Endpoint Identifier (EID) resource records.

=head1 METHODS

=head2 rdlength

    print "rdlength = ", $rr->rdlength, "\n";

Returns the length of the record's data section.

=head2 rdata

    $rdata = $rr->rdata;

Returns the record's data section as binary data.

=head1 COPYRIGHT

Copyright (c) 1997-1998 Michael Fuhr.  All rights reserved.  This
program is free software; you can redistribute it and/or modify it
under the same terms as Perl itself. 

=head1 SEE ALSO

L<perl(1)>, L<Net::DNS>, L<Net::DNS::Resolver>, L<Net::DNS::Packet>,
L<Net::DNS::Header>, L<Net::DNS::Question>, L<Net::DNS::RR>,
draft-ietf-nimrod-dns-I<xx>.txt

=cut