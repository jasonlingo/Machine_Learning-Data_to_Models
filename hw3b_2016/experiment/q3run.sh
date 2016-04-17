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
