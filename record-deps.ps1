# record-deps.ps1
cd C:\Users\benke\devEnv\disruption
$commit = git rev-parse HEAD
"disruption: $commit (https://github.com/claravdw/disruption.git)" | Out-File -FilePath C:\Users\benke\devEnv\llmproc\src\DEPENDENCIES.txt
cd C:\Users\benke\devEnv\llmproc
git add .\src\DEPENDENCIES.txt