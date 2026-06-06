# update_architecture.ps1

"========== APP ==========" | Set-Content file_architecture.txt
tree app /F /A | Add-Content file_architecture.txt

"" | Add-Content file_architecture.txt
"========== SRC ==========" | Add-Content file_architecture.txt
tree src /F /A | Add-Content file_architecture.txt

"" | Add-Content file_architecture.txt
"========== TESTS ==========" | Add-Content file_architecture.txt
tree tests2 /F /A | Add-Content file_architecture.txt