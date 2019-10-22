function SilentlyDelete-File($path)
{
    if ( [System.IO.File]::Exists($path))
    {
        Remove-Item "$path"
    }
}


function SilentlyDelete-DesktopFile([string[]]$names)
{
    $UserDesktop = [Environment]::GetFolderPath("Desktop")
    $PublicDesktop = ([Environment]::GetEnvironmentVariable("Public")) + "\Desktop"

    foreach ($name in $names)
    {
        SilentlyDelete-File("$UserDesktop\" + $name)
        SilentlyDelete-File("$PublicDesktop\" + $name)
    }
}

SilentlyDelete-DesktopFile($args)
