printf "Q5-6"
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-6-25-0.5-0.001-0.01.txt 25 0.5 0.001 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-6-25-0.5-10.0-0.01.txt 25 0.5 10.0 0.01 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-6-25-0.5-0.1-0.001.txt 25 0.5 0.1 0.001 1100 1000
printf "."
./collapsed-sampler input-train.txt input-test.txt collapsed-output-Q5-6-25-0.5-0.1-10.0.txt 25 0.5 0.1 10.0 1100 1000
printf "\n"
