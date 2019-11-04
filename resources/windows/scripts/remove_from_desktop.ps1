function SilentlyRemove-File($path)
{
    if ( [System.IO.File]::Exists($path))
    {
        Remove-Item "$path"
    }
}


function SilentlyRemove-DesktopFile([string[]]$names)
{
    $UserDesktop = [Environment]::GetFolderPath("Desktop")
    $PublicDesktop = ([Environment]::GetEnvironmentVariable("Public")) + "\Desktop"

    foreach ($name in $names)
    {
        SilentlyRemove-File("$UserDesktop\" + $name)
        SilentlyRemove-File("$PublicDesktop\" + $name)
    }
}

SilentlyRemove-DesktopFile($args)
