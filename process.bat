call "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat"
call devenv monopoly.sln /Build Release

call conda activate

cd x64
cd Release

if exist export-general\ (
    echo "Folder export-general already exists."
) else (
    if exist export-general\evaluation-minimal.json (
        echo "File evaluation-minimal.json already exists."
    ) else ( 
        call schedule_and_price.exe --instances minimal --approaches static rollout nested estimator --calls genetic gurobi  --report export-general/evaluation-minimal.json
		move *.log logs/
		move logs export-general\logs-minimal
    )
    if exist export-general\evaluation-small.json (
        echo "File evaluation-small.json already exists."
    ) else (
        call schedule_and_price.exe --instances small --approaches static rollout nested estimator --calls genetic gurobi  --report export-general/evaluation-small.json
		move *.log logs/
		move logs export-general\logs-small
    )
    if exist export-general\evaluation-medium.json (
        echo "File evaluation-medium.json already exists."
    ) else (
        call schedule_and_price.exe --instances medium --approaches static rollout nested estimator --calls genetic gurobi  --report export-general/evaluation-medium.json
		move *.log logs/
		move logs export-general\logs-medium
    )
)

if exist export-exact-one\ (
    echo "Folder export-exact-one already exists."
) else (
    call fully_dynamic.exe
    call python ..\..\organize-one-exact.py --directory-root export-exact-one
)

if exist export-exact-two\ (
    echo "Folder export-exact-two already exists."
) else (
    call dp-two-machines.exe
    call python ..\..\organize-two-exact.py --json-path results.json --export-dir export-exact-two
    move results.json export-exact-two\results.json
)

cd ..\..
echo "Results are available in x64\Release"
