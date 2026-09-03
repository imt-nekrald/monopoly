call "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat"
call devenv monopoly.sln /Build Release

call conda activate

cd x64
cd Release

if not exist export-general\evaluation-minimal.json (
    call schedule_and_price.exe --instances minimal --approaches static rollout nested estimator --calls genetic gurobi  --report export-general\evaluation-minimal.json
    move *.log logs\
    move logs export-general\logs-minimal
)
if not exist export-general\evaluation-small.json (
    call schedule_and_price.exe --instances small --approaches static rollout nested estimator --calls genetic gurobi  --report export-general\evaluation-small.json
    move *.log logs\
    move logs export-general\logs-small
)
if not exist export-general\evaluation-medium.json (
    call schedule_and_price.exe --instances medium --approaches static rollout nested estimator --calls genetic gurobi  --report export-general\evaluation-medium.json
    move *.log logs\
    move logs export-general\logs-medium
)
call python ..\..\organize-general --directory-root export-general 

if not exist export-exact-one\ (
    call fully_dynamic.exe
    call python ..\..\organize-one-exact.py --directory-root export-exact-one
)

if not exist export-exact-two\ (
    call dp-two-machines.exe
    call python ..\..\organize-two-exact.py --json-path results.json --export-dir export-exact-two
    move results.json export-exact-two\results.json
)

cd ..\..
echo "Results are available in x64\Release"
