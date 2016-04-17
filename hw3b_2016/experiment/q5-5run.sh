printf "Q5-5"
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-5-25-0.0-0.1.txt 25 0.0 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-5-25-0.25-0.1.txt 25 0.25 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-5-25-0.5-0.1.txt 25 0.5 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-5-25-0.75-0.1.txt 25 0.75 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-5-25-1.0-0.1.txt 25 1.0 0.1 0.01 1100 1000
printf "\n"