if ($args[0])
{
    $newName = $args[0]
}
else
{
    $newName = "$Env:USERNAME-PC"
}

#echo $newName
rename-computer -NewName $newName -Force
