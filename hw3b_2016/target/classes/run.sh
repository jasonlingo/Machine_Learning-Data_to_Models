# Q3
printf "Q3\n"
./collapsed-sampler input-train.txt input-test.txt collapsed-output-5-0.5-0.1.txt 5 0.5 0.1 0.01 1100 1000
./collapsed-sampler input-train.txt input-test.txt collapsed-output-5-0.8-0.1.txt 5 0.8 0.1 0.01 1100 1000
./collapsed-sampler input-train.txt input-test.txt collapsed-output-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
./collapsed-sampler input-train.txt input-test.txt collapsed-output-25-0.2-0.1.txt 25 0.2 0.1 0.01 1100 1000
./collapsed-sampler input-train.txt input-test.txt collapsed-output-25-0.5-1.0.txt 25 0.5 1.0 0.01 1100 1000

# Q4 
printf "Q4\n"
./blocked-sampler input-train.txt input-test.txt blocked-output-5-0.5-0.1.txt 5 0.5 0.1 0.01 1100 1000
./blocked-sampler input-train.txt input-test.txt blocked-output-5-0.8-0.1.txt 5 0.8 0.1 0.01 1100 1000
./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.2-0.1.txt 25 0.2 0.1 0.01 1100 1000
./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.5-1.0.txt 25 0.5 1.0 0.01 1100 1000


# Q5-2
printf "Q5-2\n"
./blocked-sampler input-train.txt input-test.txt blocked-output-5-0.5-0.1.txt 5 0.5 0.1 0.01 1100 1000
./blocked-sampler input-train.txt input-test.txt blocked-output-5-0.8-0.1.txt 5 0.8 0.1 0.01 1100 1000
./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.2-0.1.txt 25 0.2 0.1 0.01 1100 1000
./blocked-sampler input-train.txt input-test.txt blocked-output-25-0.5-1.0.txt 25 0.5 1.0 0.01 1100 1000

# Q5-3
printf "Q5-3-collapse\n"
./timed-collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-3-5-0.5-0.1.txt 5 0.5 0.1 0.01 1100 1000
./timed-collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-3-5-0.8-0.1.txt 5 0.8 0.1 0.01 1100 1000
./timed-collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-3-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
./timed-collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-3-25-0.2-0.1.txt 25 0.2 0.1 0.01 1100 1000
./timed-collapsed-sampler input-train.txt input-test.txt timed-collapsed-output-Q5-3-25-0.5-1.0.txt 25 0.5 1.0 0.01 1100 1000
printf "Q5-3-blocked\n"
./timed-blocked-sampler input-train.txt input-test.txt timed-block-output-Q5-3-5-0.5-0.1.txt 5 0.5 0.1 0.01 1100 1000
./timed-blocked-sampler input-train.txt input-test.txt timed-block-output-Q5-3-5-0.8-0.1.txt 5 0.8 0.1 0.01 1100 1000
./timed-blocked-sampler input-train.txt input-test.txt timed-block-output-Q5-3-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
./timed-blocked-sampler input-train.txt input-test.txt timed-block-output-Q5-3-25-0.2-0.1.txt 25 0.2 0.1 0.01 1100 1000
./timed-blocked-sampler input-train.txt input-test.txt timed-block-output-Q5-3-25-0.5-1.0.txt 25 0.5 1.0 0.01 1100 1000


