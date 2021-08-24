# Find and replace the dates in a Canvas JSON file
# JSON input is via standard input
#
# Parameters:
#  $1 - File containing a 3 column tab-delimited spreadsheet
#         column 1 = description of assignment/group (not used for anything)
#         column 2 = previous due date, e.g. "2021-01-15 23:59:00"
#         column 3 = new due date, e.g. "2021-09-07 23:59:00"
#         first line in file is assumed to be a header
# 
# Example usage: perl UpdateDates.pl dates.txt < schedule.json > new.json

use strict;

if (@ARGV < 1)
{
    print "$0 <date file>\n";
    exit;
}

open(IN, $ARGV[0]);

# Skip the header line
my $line;
$line = <IN>;

my @oldDate;
my @newDate;

while ($line = <IN>)
{
    $line =~ s/[\n\r]//g;

    my @cols = split(/\t/, $line);
    if (@cols == 3)
    {
        my $desc;
        my $old;
        my $new;
        ($desc, $old, $new) = @cols;

        push @oldDate, $old;
        push @newDate, $new;
#        print $desc . " ". $old . " " . $new . "\n";
    }
}
close(IN);

while ($line = <STDIN>)
{
    if ($line =~ /due_at/)
    {
        my $i = 0;
        while ($i < @oldDate)
        {
            my $old = $oldDate[$i];

            if (index($line, $old) != -1)
            {
                my $new = $newDate[$i];
                $line =~ s/$old/$new/;
                last;
            }
            else
            {
                $i++;
            }
        }
        print $line;
    }
    else
    {
        print $line;
    }
}
