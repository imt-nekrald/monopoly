call "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat"
call devenv monopoly.sln /Build Release

call conda activate

call cd x64
call cd Release

call schedule_and_price.exe --instances minimal --approaches static rollout nested estimator --calls genetic gurobi  --report evaluation-minimal.json
call schedule_and_price.exe --instances small --approaches static rollout nested estimator --calls genetic gurobi  --report evaluation-small.json
call schedule_and_price.exe --instances medium --approaches static rollout nested estimator --calls genetic gurobi  --report evaluation-medium.json

mkdir export-general
move evaluation-minimal.json export-general/evaluation-minimal.json
move evaluation-small.json export-general/evaluation-small.json
move evaluation-medium.json export-general/evaluation-medium.json

call "fully_dynamic.exe"
python ../../organize-one-exact --directory-root "export-exact-one"
call "dp-two-machines.exe"
call python ../../organize-two-exact.py --json-path results.json --export-dir export-two-exact
move results.json export-two-exact/results.json
