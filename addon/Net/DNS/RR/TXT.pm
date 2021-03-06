package Net::DNS::RR::TXT;

# $Id: TXT.pm,v 1.5 2003/06/11 10:36:29 ctriv Exp $

use strict;
use vars qw(@ISA);

use Net::DNS::Packet;
use Text::ParseWords;

@ISA = qw(Net::DNS::RR);

sub new {
	my ($class, $self, $data, $offset) = @_;
	
	my $rdlength = $self->{'rdlength'} or return bless $self, $class;
	my $end = $offset + $rdlength;
	while ( $offset < $end ) {
		my $strlen = unpack("\@$offset C", $$data );
		++$offset ;
		my $char_str = substr($$data, $offset, $strlen);
		$offset += $strlen;
		push( @{ $self->{'char_str_list'} }, $char_str );
	}

	return bless $self, $class;
}

sub new_from_string {
    my ( $class, $self, $rdata_string ) = @_ ;
    
    bless $self, $class;
        
    $self->_build_char_str_list($rdata_string);

    return $self ;
}

sub txtdata {
	my $self = shift;
	return join(' ',  $self->char_str_list()  );
}

sub rdatastr {
	my $self = shift;
	return defined $self->txtdata()
		? join(' ', map { my $str = $_;  
				$str =~ s/"/\\"/g ;  
				q("). $str. q(") 
				}  @{ $self->{'char_str_list'} }  )
		: "; no data";
}

sub _build_char_str_list {
	my ( $self, $rdata_string ) = @_;
	
	my @words = shellwords($rdata_string);

	$self->{'char_str_list'} = [];

	if (@words) {
		foreach my $string ( @words ) {
		    $string =~ s/\\"/"/g;
		    push(@{$self->{'char_str_list'}}, $string);
		}
	}
}

sub char_str_list {
	my $self = shift;
	
	# Unfortunately, RR->new_from_hash() breaks encapsulation 
	# of data in child objects.
	if ( not defined $self->{'char_str_list'} ) {
		$self->_build_char_str_list( $self->{'txtdata'} );
	}

	return @{ $self->{'char_str_list'} };	# unquoted strings
}

sub rr_rdata {
	my $self = shift;
	my $rdata = "";

	foreach my $string ( $self->char_str_list() ) {
	    $rdata .= pack("C", length $string );
	    $rdata .= $string;
	}

	return $rdata;
}

1;
__END__

=head1 NAME

Net::DNS::RR::TXT - DNS TXT resource record

=head1 SYNOPSIS

C<use Net::DNS::RR>;

=head1 DESCRIPTION

Class for DNS Text (TXT) resource records.

=head1 METHODS

=head2 txtdata

    print "txtdata = ", $rr->txtdata, "\n";

Returns the descriptive text as a single string, regardless of actual 
number of <character-string> elements.  Of questionable value.  Should 
be deprecated.  

Use C<TXT-E<gt>rdatastr()> or C<TXT-E<gt>char_str_list()> instead.

=head2 char_str_list

    print "Individual <character-string> list: \n\t", \
		    join ( "\n\t", $rr->char_str_list() );

Returns a list of the individual <character-string> elements, 
as unquoted strings.  Used by TXT->rdatastr and TXT->rr_rdata.

=head1 COPYRIGHT

Copyright (c) 1997-1998 Michael Fuhr.  All rights reserved.  This
program is free software; you can redistribute it and/or modify it
under the same terms as Perl itself. 

=head1 SEE ALSO

L<perl(1)>, L<Net::DNS>, L<Net::DNS::Resolver>, L<Net::DNS::Packet>,
L<Net::DNS::Header>, L<Net::DNS::Question>, L<Net::DNS::RR>,
RFC 1035 Section 3.3.14

=cut