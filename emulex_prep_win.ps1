# Start of command #########
cd "c:\Program Files\Emulex\Util\OCManager"
$a = .\HbaCmd.exe ListHBAs | Select-String -Pattern '(Port WWN       : )(\b\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\:\S{2}\b)'
$b = New-Object System.Collections.ArrayList
$c = New-Object System.Collections.ArrayList
Foreach ($item in $a.Matches) {$b.Add($item.groups[2].toString())}
Foreach ($item in $b) {$c.Add('.\HbaCmd.exe HbaAttributes ' + $item + ' | Select-String -Pattern "Host Name","Driver Version","Boot Code"');$c.Add('.\HbaCmd.exe PortAttributes ' + $item + ' | Select-String -Pattern "Port State","Port Speed","Function Type"');$c.Add('.\HbaCmd.exe EnableBootCode ' + $item + ' d');$c.Add('.\HbaCmd.exe GetXcvrData ' + $item + ' 1 | Select-String -Pattern "TxPower:","RxPower:"'); }
# Output below to ticket
powermt version
hostname
.\HbaCmd.exe version
Foreach ($item in $c) {Invoke-Expression $item}
Foreach ($item in $a.Matches) { 'WWN: ' + $item.groups[2].toString()}
# End of command #########

