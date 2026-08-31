call "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat"
call devenv monopoly.sln /Build Release

call conda activate

call cd x64
call cd Release

if exist export-general\ (
    call echo "Folder export-general already exists."
) else (
    if exist evaluation-minimal.json (
        call echo "File evaluation-minimal.json already exists."
    ) else ( 
        call schedule_and_price.exe --instances minimal --approaches static rollout nested estimator --calls genetic gurobi  --report evaluation-minimal.json
    )
    if exist evaluation-small.json (
        call echo "File evaluation-small.json already exists."
    ) else (
        call schedule_and_price.exe --instances small --approaches static rollout nested estimator --calls genetic gurobi  --report evaluation-small.json
    )
    if exist evaluation-medium.json (
        call echo "File evaluation-medium.json already exists."
    ) else (
        call schedule_and_price.exe --instances medium --approaches static rollout nested estimator --calls genetic gurobi  --report evaluation-medium.json
    )
    call mkdir export-general
    call move evaluation-minimal.json export-general\evaluation-minimal.json
    call move evaluation-small.json export-general\evaluation-small.json
    call move evaluation-medium.json export-general\evaluation-medium.json
)

if exist export-exact-one\ (
    call echo "Folder export-exact-one already exists."
) else (
    call fully_dynamic.exe
    call python ..\..\organize-one-exact.py --directory-root export-exact-one
)

if exist export-exact-two\ (
    call echo "Folder export-exact-two already exists."
) else (
    call dp-two-machines.exe
    call python ..\..\organize-two-exact.py --json-path results.json --export-dir export-exact-two
    call move results.json export-exact-two/results.json
)

call cd ..\..
call echo "Results are availabe in x64/Release"
