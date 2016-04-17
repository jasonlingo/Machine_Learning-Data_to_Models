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
