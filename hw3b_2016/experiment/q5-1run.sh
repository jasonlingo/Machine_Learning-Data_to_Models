# Q5-1
printf "Q5-1"
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-1-1.txt 25 0.5 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-1-2.txt 25 0.5 0.1 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-1-3.txt 25 0.5 0.1 0.01 1100 1000
printf "\n"
