#!/usr/bin/env bash


cd dp-one-machine
rm -rf build
mkdir -p build
cd build
cmake ..
make -j 8
cd ../

cd dp-two-machines
rm -rf build
mkdir -p build
cd build
cmake ..
make -j 8
cd ../..

cd price-and-schedule
rm -rf build
mkdir -p build
cd build
cmake ..
make -j 8
cd ../..


rm -rf x64
mkdir -p x64/Release
cd x64/Release
ln -sf ../../price-and-schedule/build/research
ln -sf ../../dp-one-machine/build/fully_dynamic
ln -sf ../../dp-two-machines/build/dp_two_machines


if [ ! -f export-general/evaluation-minimal.json ]; then
    schedule_and_price --instances minimal --approaches static rollout nested estimator --calls genetic gurobi  --report export-general/evaluation-minimal.json
    mv *.log logs/
    mv logs export-general/logs-minimal
fi

if [ ! -f export-general/evaluation-small.json ]; then
    schedule_and_price --instances small --approaches static rollout nested estimator --calls genetic gurobi  --report export-general/evaluation-small.json
    mv *.log logs/
    mv logs export-general/logs-small
fi

if [ ! -f export-general/evaluation-medium.json ]; then
    schedule_and_price --instances medium --approaches static rollout nested estimator --calls genetic gurobi  --report export-general/evaluation-medium.json
    mv *.log logs/
    mv logs export-general/logs-medium
fi


if [ ! -d export-exact-one ]; then
    fully_dynamic
    python ../../organize-one-exact.py --directory-root export-exact-one
fi

if [ ! -d export-exact-two ]; then
    dp_two_machines
    python ../../organize-two-exact.py --json-path results.json --export-dir export-exact-two
    mv results.json export-exact-two/results.json
fi


cd ../..
echo "Results are available in x64/Release"

