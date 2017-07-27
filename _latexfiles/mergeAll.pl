#!/usr/bin/perl
use open      qw(:std :utf8);    # undeclared streams in UTF-8

################################################################################
# description
################################################################################

# It combines the below given bib files and the file translations.txt in the
# bibs folder to one bib file
# stored in bibs/all-eng.bib and bibs/all-ger.bib

################################################################################
# packages
################################################################################

use strict;
use IO::Handle;

################################################################################
# global constants
################################################################################

my $programname = $0;
$programname =~ s,\\,\/,g; # necessary for windows
my $programpath = $programname;
$programpath =~ s,[^\/]*$,,;
$programname =~ s,.*\/,,;

# the bib files to include into all.bib
my $book    = "bibs/book.bib";
my $incol   = "bibs/incollection.bib";
my $proc    = "bibs/proceedings.bib";
my $inproc  = "bibs/inproceedings.bib";
my $article = "bibs/article.bib";
my $manual  = "bibs/manual.bib";
my $dipl    = "bibs/mastersthesis.bib";
my $misc    = "bibs/misc.bib";
my $phd     = "bibs/phdthesis.bib";
my $tech    = "bibs/techreport.bib";
my $res     = "bibs/researchreport.bib";
my $unpub   = "bibs/unpublished.bib";

# the outfile names of the bib files
# to which translations will be prepended
my @outfiles = (
                "bibs/all-eng.bib",
                "bibs/all-ger.bib",
               );

# the bst files
my @bst = ("styles/template_ivt-eng.bst",
           "styles/template_ivt-ger.bst",
           "styles/template_ivt-cv-eng.bst",
           "styles/template_ivt-cv-ger.bst",
           "styles/template_ivt-reflist-eng.bst",
           "styles/template_ivt-comment-eng.bst",
           "styles/template_ivt-comment-ger.bst",
           "styles/template_ivt-unsrt-eng.bst",
           "styles/template_ivt-unsrt-ger.bst",
           "styles/template_plain-unsrt-eng.bst",
           "styles/template_plain-unsrt-ger.bst",
           "styles/template_etc-eng.bst",
           "styles/template_elsart-harv-eng.bst");

# the files with the language specific keywords
my @tfiles = (
                "bibs/translations.txt",
                "bibs/journal.txt",
                "bibs/publisher.txt",
                "bibs/author.txt",
                "bibs/special.txt",
               );

my $tmpfile = "tmp.bst";

my %latin1 = (
	chr(128) => "\\texteuro",
	chr(130) => "\\quotesinglbase",
	chr(131) => "\\textflorin",
	chr(132) => "\\quotedblbase",
	chr(133) => "\\dots",
	chr(134) => "\\dag",
	chr(135) => "\\ddag",
	chr(136) => "\\^{}",
	chr(137) => "\\textperthousand",
	chr(138) => "\\v S",
	chr(139) => "\\guilsinglleft",
	chr(140) => "\\OE",
	chr(142) => "\\v Z",
	chr(145) => "\\textquoteleft",
	chr(146) => "\\textquoteright",
	chr(147) => "\\textquotedblleft",
	chr(148) => "\\textquotedblright",
	chr(149) => "\\textbullet",
	chr(150) => "\\textendash",
	chr(151) => "\\textemdash",
	chr(152) => "\\~{}",
	chr(153) => "\\texttrademark",
	chr(154) => "\\v s",
	chr(155) => "\\guilsinglright",
	chr(156) => "\\oe",
	chr(158) => "\\v z",
	chr(159) => "\\\"Y",
	chr(160) => "\\nobreakspace",
	chr(161) => "\\textexclamdown",
	chr(162) => "\\textcent",
	chr(163) => "\\pounds",
	chr(164) => "\\textcurrency",
	chr(165) => "\\textyen",
	chr(166) => "\\textbrokenbar",
	chr(167) => "\\S",
	chr(168) => "\\\"{}",
	chr(169) => "\\copyright",
	chr(170) => "\\textordfeminine",
	chr(171) => "\\guillemotleft",
	chr(172) => "\\ensuremath{\\lnot}",
	chr(173) => "\\-",
	chr(174) => "\\textregistered",
	chr(175) => "\\={}",
	chr(176) => "\\textdegree",
	chr(177) => "\\ensuremath{\\pm}",
	chr(178) => "\\ensuremath{\\mathtwosuperior}",
	chr(179) => "\\ensuremath{\\maththreesuperior}",
	chr(180) => "\\'{}",
	chr(181) => "\\ensuremath{\\mu}",
	chr(182) => "\\P",
	chr(183) => "\\textperiodcentered",
	chr(184) => "\\c\\ ",
	chr(185) => "\\ensuremath{\\mathonesuperior}",
	chr(186) => "\\textordmasculine",
	chr(187) => "\\guillemotright",
	chr(188) => "\\textonequarter",
	chr(189) => "\\textonehalf",
	chr(190) => "\\textthreequarters",
	chr(191) => "\\textquestiondown",
	chr(192) => "\\`A",
	chr(193) => "\\'A",
	chr(194) => "\\^A",
	chr(195) => "\\~A",
	chr(196) => "\\\"A",
	chr(197) => "\\r A",
	chr(198) => "\\AE",
	chr(199) => "\\c C",
	chr(200) => "\\`E",
	chr(201) => "\\'E",
	chr(202) => "\\^E",
	chr(203) => "\\\"E",
	chr(204) => "\\`I",
	chr(205) => "\\'I",
	chr(206) => "\\^I",
	chr(207) => "\\\"I",
	chr(208) => "\\DH",
	chr(209) => "\\~N",
	chr(210) => "\\`O",
	chr(211) => "\\'O",
	chr(212) => "\\^O",
	chr(213) => "\\~O",
	chr(214) => "\\\"O",
	chr(215) => "\\ensuremath{\\times}",
	chr(216) => "\\O",
	chr(217) => "\\`U",
	chr(218) => "\\'U",
	chr(219) => "\\^U",
	chr(220) => "\\\"U",
	chr(221) => "\\'Y",
	chr(222) => "\\TH",
	chr(223) => "\\ss",
	chr(224) => "\\`a",
	chr(225) => "\\'a",
	chr(226) => "\\^a",
	chr(227) => "\\~a",
	chr(228) => "\\\"a",
	chr(229) => "\\r a",
	chr(230) => "\\ae",
	chr(231) => "\\c c",
	chr(232) => "\\`e",
	chr(233) => "\\'e",
	chr(234) => "\\^e",
	chr(235) => "\\\"e",
	chr(236) => "\\`\\i",
	chr(237) => "\\'\\i",
	chr(238) => "\\^\\i",
	chr(239) => "\\\"\\i",
	chr(240) => "\\dh",
	chr(241) => "\\~n",
	chr(242) => "\\`o",
	chr(243) => "\\'o",
	chr(244) => "\\^o",
	chr(245) => "\\~o",
	chr(246) => "\\\"o",
	chr(247) => "\\ensuremath{\\div}",
	chr(248) => "\\o",
	chr(249) => "\\`u",
	chr(250) => "\\'u",
	chr(251) => "\\^u",
	chr(252) => "\\\"u",
	chr(253) => "\\'y",
	chr(254) => "\\th",
	chr(255) => "\\\"y",
);

################################################################################
# global variables
################################################################################

my $entrycnt = 0;

my %dict;

################################################################################
# functions:
################################################################################

################################################################################
sub setHeaderToBstFiles {
	foreach my $curr_file (@bst) {
		# remove 'template_' from curr_file
		$curr_file =~ s/template_//g;

		print "  unlinking unneeded $curr_file...\n";

		unlink($curr_file);

		print "  done.\n";
	}
}
################################################################################

################################################################################
sub setHeaderToBibFiles {
	foreach my $curr_file (@outfiles) {
    print "merging bib files into $curr_file...\n";

    open (OUT, ">$programpath$curr_file") || die "Could not open \"$programpath$curr_file\"!\n\n";
    print OUT "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n";
    print OUT "% The combination of the given bib files.\n";
    print OUT "% Generated with $programname\n";
    print OUT "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n";
    print OUT "\n";

		print "  setting language specific header to $curr_file...\n";

		my $index = 0; # set the index of the column (eng = 1, ger = 2)
		if ($curr_file =~ /^.*eng\.bib$/) { $index = 1; }
		elsif ($curr_file =~ /^.*ger\.bib$/) { $index = 2; }
		else { die "$curr_file does not have the right ending (eng,ger)!\n\n"; }
		
		%dict = ();

  	foreach my $tfile (@tfiles) {
		  # write the heading part (the translations) into the final file (input file w/o 'template_')
		  open (IN, "$programpath$tfile") || die "Could not open \"$programpath$tfile\"!\n\n";

		  while(<IN>) {
			  # ignore lines without at least one tab
			  if (!($_ =~ /^%|^[^\t]*$/)) {

				  # how the input file looks like:
				  #
				  # head:    key  eng   ger
				  # Example: mar  Mar.  März
				  # index:   0    1     2

				  my @entries = split(/[\t|\n]/, $_);
				
				  # substitute English entry if native (German) entry not available
				  # (English entry is available by default)
				  if ($entries[$index] =~ /^$/) {
					  $entries[$index] = $entries[1]
				  }

				  # do not surround "forthcoming" with braces, this breaks the .bst key assignment
				  # if more than one forthcoming paper has the same authors
				  my $okey = $entries[0];
				  $okey =~ s/ //g;
				  my $key = (lc $okey);
				  if (exists $dict{$key}) {
				    die "Duplicate key in $tfile: $okey (defined elsewhere as $dict{$key})"
				  }
				  if ($key =~ /^forth$/) {
					  $dict{$key} = "{$entries[$index]\\xspace}";
				  }
				  else {
					  $dict{$key} = "{$entries[$index]}";
				  }
			  }
		  }
		  close(IN);
		}

	  print OUT "%%%%%%%%%%%%%%%\n";
	  print OUT "% End of macros\n";
	  print OUT "%%%%%%%%%%%%%%%\n\n";
		close(OUT);

    $entrycnt = 0;
    
    appendWithoutComments($book,$curr_file);
    appendWithoutComments($article,$curr_file);
    appendWithoutComments($manual,$curr_file);
    appendWithoutComments($dipl,$curr_file);
    appendWithoutComments($misc,$curr_file);
    appendWithoutComments($phd,$curr_file);
    appendWithoutComments($tech,$curr_file);
    appendWithoutComments($res,$curr_file);
    appendWithoutComments($unpub,$curr_file);
    appendAndResolveWithoutComments($incol,$book,$curr_file,"INCOLLECTION");
    appendAndResolveWithoutComments($inproc,$proc,$curr_file,"INPROCEEDINGS");

    print "  Total $entrycnt entries appended.\n";

		print "  done.\n";
	}
}
################################################################################

################################################################################
sub replaceValueStrings {
	my $in  = $_[0];
	my $out = $in;
	if ($in =~ /[ \t]*=[ \t]*/) { # key-value
		# This splits the line at the first =
		my @line = split(/[ \t]*=[ \t]*/, $_, 2);
		# This looks for all words and replaces them with their corresponding
		# entries in %dict. This is case-insensitive, so we are looking for the
		# lowercase variant of the key.
		$line[1] =~ s/([A-Za-z][A-Za-z0-9-]*)([ \t]*(?:#|,[ \t]*$))/$dict{(lc $1)}$2/g;
		$line[1] =~ s/"([A-Za-z][A-Za-z0-9-]*)"/\{$dict{(lc $1)}\}/g;
	
		# Join strings separated by hash (#)
		$line[1] =~ s/\} *\# *\{//g;

		# Replace non-ASCII characters by their LaTeX equivalent
		# (derived from cp1252.def)
		my $re = join '|', keys %latin1;
		$line[1] =~ s/($re)/\{$latin1{$1}\}/g;

		# Forcefully append a comma to the entry
		$out = "$line[0] = $line[1]";
		$out =~ s/,* *$/,/;
	}
	else {
		$out = $in;
	}
	
	return $out;
}
################################################################################

################################################################################
sub appendWithoutComments {
	my $in  = $_[0];
	my $out = $_[1];

	my $cnt = 0;

	print "  appending $in to $out...\n";

	open (OUT, ">>$programpath$out") || die "Could not open \"$programpath$out\"!\n\n";
	print OUT "\n";
	print OUT "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n";
	print OUT "% $in\n";
	print OUT "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n";
	print OUT "\n";

	open (IN, "$programpath$in") || die "Could not open \"$programpath$in\"!\n\n";
	while (<IN>) {
		if (!($_ =~ /^%.*$/)) {
			if ($_ =~ /^\@[A-Z]+{.*$/) { # an entry line
				$cnt++;
			}
			print OUT replaceValueStrings($_);
		}
	}
	close(IN);

	print OUT "\n";
	close(OUT);

	print "    $cnt entries appended.\n";
	$entrycnt += $cnt;

	print "  done.\n";
}

################################################################################

################################################################################
sub replaceCrossref {
	my $crossref = $_[0];
	my $file     = $_[1];

	my $str = "";

	my $found = 0;

	print "      replacing $crossref by using $file...\n";

	open (FILE, "$programpath$file") || die "Could not open \"$programpath$file\"!\n\n";
	while (<FILE>) {
		if ($_ =~ /^\@[A-Z]+{$crossref,.*$/) { # the crossref found
			$found = 1;
			$_ = <FILE>; # read the next line
			while (!($_ =~ /^ *}.*$/)) { # write that lines until "}" reached
				$_ =~ s/TITLE.*=/BOOKTITLE =/g; # substitute TITLE with BOOKTITLE
				$str = $str.replaceValueStrings($_);
				$_ = <FILE>;
			}
		}
	}
	close(FILE);

	if ($found == 0) {
		print "        !!!CROSSREF NOT FOUND! CONTINUING ANYWAY!!!\n";
	}
	print "      done.\n";

	return $str;
}
################################################################################

################################################################################
sub appendAndResolveWithoutComments {
	my $in   = $_[0];
	my $ref  = $_[1];
	my $out  = $_[2];
	my $type = $_[3];

	my $cnt = 0;
	my $crcnt = 0;

	print "  appending $in (entry type = $type) to $out\n";
	print "  (crossrefs replaced by $ref)...\n";

	open (OUT, ">>$programpath$out") || die "Could not open \"$programpath$out\"!\n\n";
	print OUT "\n";
	print OUT "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n";
	print OUT "% $in (crossref solved by using $ref)\n";
	print OUT "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n";
	print OUT "\n";

	my @fullentry = ();
	my $substitute = '';
	open (IN, "$programpath$in") || die "Could not open \"$programpath$in\"!\n\n";
	while (<IN>) {
		if (!($_ =~ /^%.*$/)) { # read all lines except comments
			if ($_ =~ /^\@${type}{.*$/i) { # an entry line -> write it down
				$cnt++;
				my $entry = $_;
				$entry =~ s/^.*{(.+),.*$/$1/g;
				chomp($entry);
				print "    appending entry = $entry\n";
				push(@fullentry, $_);
			}
			elsif ($_ =~ /^.*CROSSREF.*$/) { # a crossref line -> replace it
				$crcnt++;
				if ($crcnt != $cnt) {
					print "    ERROR: CROSSREF outside of entry! Check the following entry in $in:\n";
					print "@fullentry\n";
					die;
				}
				# extract the crossref
				my $crossref = $_;
				$crossref =~ s/^.*{(.+)}.*$/$1/g;
				chomp($crossref);
				print "    with crossref = $crossref\n";
				$substitute = replaceCrossref($crossref,$ref);
			}
			elsif ($_ =~ /^ *}/) { # end of entry -> flush
				my $key;
				foreach $key(("url", "comment", "volume")) { # filter out double URLs and comments
					if (grep(/^ *$key *=/i, @fullentry)) { # is there another item of this type in the entry?
						$substitute =~ s/^ *$key *=.*\n//im; # remove it!
					}
				}
				if ($substitute) {
					push(@fullentry, $substitute);
				}
				push(@fullentry, $_);
				print OUT join('', @fullentry);
				@fullentry = ();
				$substitute = '';
				if ($crcnt != $cnt) {
					print "    WARNING: no CROSSREF for entry! Continuing.\n";
					$crcnt = $cnt;
				}
			}
			elsif ($_ =~ /^[ \t]*$/) { # end of entry -> flush
				push(@fullentry, $_);
			}
			else { # everything else -> write it down
				my $replaced = replaceValueStrings($_);
				push(@fullentry, $replaced);
			}
		}
	}
	close(IN);

	print OUT "\n";
	close(OUT);

	print "    $cnt entries appended.\n";
	$entrycnt += $cnt;

	print "  done.\n";
}
################################################################################

################################################################################
# main
################################################################################

if ($#ARGV != -1) {
	print STDERR "USAGE: $programname\n",
	             "       \n\n";
	exit 1;
}

print "setting language specific keywords to bib files...\n";

setHeaderToBibFiles();

print "done.\n";

print "setting language specific keywords to bst files...\n";

setHeaderToBstFiles();

print "done.\n";

