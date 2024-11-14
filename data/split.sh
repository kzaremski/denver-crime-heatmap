#!/bin/bash
# Konstantin Zaremski
#   November 14, 2024
#   
#   This file takes the 90+megabyte CSV file for all crime and splits it into
#   a series of smaller, 10,000-line CSV files that are more easily managed by
#   git and GitHub (and get around file size limitations).
#

# Delete all previously split crime files
for i in $(find crime_split_*)
do
    rm $i
    echo "Deleted old file: $i"
done

# Split the crime data into 10,000-lined parts
split -l 10000 -d crime.csv crime_split_

# Add the ".csv" extension to the end of the split files
for i in $(find crime_split_*)
do
    mv $i "$i.csv"
    echo "Renamed $i --> $i.csv"
done

# Add the CSV header to each of the split files from the first one
#   This assumes that there will not be more than 100 files (original data has less than 1 million lines excluding header)
for i in $(find . -type f -name "crime_split_*.csv" -not -name "crime_split_00.csv");
    do echo "$(head -1 crime_split_00.csv)\n$(cat $i)" > $i;
    echo "Added CSV header to $i"
done

echo "*** Data split completed. Note that the CSV header remains on the first line of the first file numerically."
