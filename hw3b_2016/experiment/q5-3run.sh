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

printf "Q5-3-blocked"
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