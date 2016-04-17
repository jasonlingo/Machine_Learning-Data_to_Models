# Q3
printf "Q3"
./collapsed-sampler input-train.txt input-test.txt collapsed-output-5-0.5-0.1.txt 5 0.5 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-5-0.8-0.1.txt 5 0.8 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-25-0.2-0.1.txt 25 0.2 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-25-0.5-1.0.txt 25 0.5 1.0 0.01 1100 1000
printf "\n"

# Q4 
printf "Q4"
./blocked-sampler input-train.txt input-test.txt blocked-output-5-0.5-0.1.txt 5 0.5 0.1 0.01 1100 1000
printf "."
./blocked-sampler input-train.txt input-test.txt blocked-output-5-0.8-0.1.txt 5 0.8 0.1 0.01 1100 1000
printf "."
./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
printf "."
./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.2-0.1.txt 25 0.2 0.1 0.01 1100 1000
printf "."
./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.5-1.0.txt 25 0.5 1.0 0.01 1100 1000
printf "\n"


# Q5-2
# printf "Q5-2\n"
# ./blocked-sampler input-train.txt input-test.txt blocked-output-5-0.5-0.1.txt 5 0.5 0.1 0.01 1100 1000
# ./blocked-sampler input-train.txt input-test.txt blocked-output-5-0.8-0.1.txt 5 0.8 0.1 0.01 1100 1000
# ./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
# ./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.2-0.1.txt 25 0.2 0.1 0.01 1100 1000
# ./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.5-1.0.txt 25 0.5 1.0 0.01 1100 1000

# Q5-3
printf "Q5-3-collapse"
./timed-collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-3-5-0.5-0.1.txt 5 0.5 0.1 0.01 1100 1000
printf "."
./timed-collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-3-5-0.8-0.1.txt 5 0.8 0.1 0.01 1100 1000
printf "."
./timed-collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-3-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
printf "."
./timed-collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-3-25-0.2-0.1.txt 25 0.2 0.1 0.01 1100 1000
printf "."
./timed-collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-3-25-0.5-1.0.txt 25 0.5 1.0 0.01 1100 1000
printf "\n"

printf "Q5-3-blocked\n"
./timed-blocked-sampler input-train.txt input-test.txt timed-block-output-Q5-3-5-0.5-0.1.txt 5 0.5 0.1 0.01 1100 1000
printf "."
./timed-blocked-sampler input-train.txt input-test.txt timed-block-output-Q5-3-5-0.8-0.1.txt 5 0.8 0.1 0.01 1100 1000
printf "."
./timed-blocked-sampler input-train.txt input-test.txt timed-block-output-Q5-3-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
printf "."
./timed-blocked-sampler input-train.txt input-test.txt timed-block-output-Q5-3-25-0.2-0.1.txt 25 0.2 0.1 0.01 1100 1000
printf "."
./timed-blocked-sampler input-train.txt input-test.txt timed-block-output-Q5-3-25-0.5-1.0.txt 25 0.5 1.0 0.01 1100 1000
printf "\n"

printf "Q5-4"
./collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-4-10-0.5-0.1.txt 10 0.5 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-4-20-0.5-0.1.txt 20 0.5 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-4-30-0.5-0.1.txt 30 0.5 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-4-40-0.5-0.1.txt 40 0.5 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-4-50-0.5-0.1.txt 50 0.5 0.1 0.01 1100 1000
printf "\n"

printf "Q5-5"
./collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-5-25-0.0-0.1.txt 25 0.0 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-5-25-0.25-0.1.txt 25 0.25 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-5-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-5-25-0.75-0.1.txt 25 0.75 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-5-25-1.0-0.1.txt 25 1.0 0.1 0.01 1100 1000
printf "\n"

