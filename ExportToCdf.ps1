<#
    .SYNOPSIS
    This script attempts to parse a JSON file in the swccg-card-json repo to the approximate format of a Holotable CDF file.

    .DESCRIPTION
    This script attempts to parse a JSON file in the swccg-card-json repo to the approximate format of a Holotable CDF file.

    The resulting output is sorted by card type, subtype and title.

    .PARAMETER JsonPath
    The path to the input JSON file.

    .PARAMETER CdfPath
    The path to the output CDF file.

    .PARAMETER Set
    The set to parse.  Valid values can be found in the input JSFON file "set" properties.

    .EXAMPLE
    PS> ./ExportToCdf.ps1 -JsonPath ./Dark.json -CdfPath ./Dark.cdf -Set "Virtual Set 13"

    .EXAMPLE
    PS> ./ExportToCdf.ps1 -JsonPath ./Light.json -CdfPath ./Light.cdf -Set "Virtual Set 13"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]
    $JsonPath,

    [Parameter(Mandatory)]
    [string]
    $CdfPath,

    [Parameter(Mandatory)]
    [string]
    $Set
)

if (-not (Test-Path -Path $JsonPath)) {
    Write-Error "Cannot find $JsonPath" -ErrorAction Stop
}

if (Test-Path -Path $CdfPath) {
    Remove-Item -Path $CdfPath
}

$json = Get-Content $JsonPath | ConvertFrom-Json

$json.cards |
Where-Object { $_.set -eq $Set } |
ForEach-Object {
    Write-Verbose "Parsing id = $($_.id), title = $($_.front.title)..."

    $ability = $_.front.ability
    $armor = $_.front.armor
    $deploy = $_.front.deploy
    $destiny = $_.front.destiny
    $forfeit = $_.front.forfeit
    $gametext = $_.front.gametext.Replace("Dark:  ", "DARK ($($_.front.darkSideIcons)): ").Replace("Light:  ", "LIGHT ($($_.front.lightSideIcons)): ").Replace("’", "'")
    $hyperspeed = $_.front.hyperspeed
    $icons = "" ; foreach ($icon in $_.front.icons) { $icons = $icons + "$icon, " } ; $icons = $icons.Trim().Trim(",")
    $img = $_.front.imageUrl.Replace("https://res.starwarsccg.org/cards/Images-HT", "").Replace("large/", "t_").Replace(".gif", "").Replace("?raw=true", "")
    $landspeed = $_.front.landspeed
    $lore = $_.front.lore
    $power = $_.front.power
    $rarity = $_.rarity
    $set = $_.set
    $side = $_.side
    $subType = $_.front.subType
    $title = $_.front.title.Replace("<>", "").Replace("•", "�")
    $type = $_.front.type
    $uniqueness = $_.front.uniqueness

    $line =
    switch ($type) {
        "Admiral's Order" {
            "card `"$img`" `"$title ($destiny)\n$side $type [$rarity]\nSet: $set\n\nText: $gametext`""
        }
        "Character" {
            "card `"$img`" `"$title ($destiny)\n$side $type - $subType [$rarity]\nSet: $set\nPower: $power Ability: $ability\nDeploy: $deploy Forfeit: $forfeit\nIcons: $icons\n\nLore: $lore\n\nText: $gametext`""
        }
        "Creature" {
            Write-Warning "Type = $Type, Title = $Title, Warning = Add creature defense value."
            "card `"$img`" `"$title ($rarity)\n$side $type- $subType [$rarity]\nSet: $set\nPower: $power {TODO: ADD DEFENSE VALUE}\nDeploy: $deploy Forfeit: $forfeit\nIcons: $icons\n\nLore: $lore\n\nText: $gametext`""
        }
        "Defensive Shield" {
            "card `"/$img`" `"$title ($destiny)\n$side $type [$rarity]\nSet: $set\n\nLore: $lore\n\nText: $gametext`""
        }
        "Device" {
            "card `"$img`" `"$title ($rarity)\n$side $type [$rarity]\nSet: $set\n\nLore: $lore\n\nText: $gametext`""
        }
        "Effect" {
            "card `"$img`" `"$title ($destiny)\n$side $type [$rarity]\nSet: $set\n\nLore: $lore\n\nText: $gametext`""
        }
        "Epic Event" {
            "card `"$img`" `"$title ($destiny)\n$side $type [$rarity]\nSet: $set\n\nText: $gametext`""
        }
        "Game Aid" {
            "GAME AID UNSUPPORTED"
        }
        "Interrupt" {
            "card `"$img`" `"$title ($destiny)\n$side $type - $subtype [$rarity]\nSet: $set\n\nLore: $lore\n\nText: $gametext`""
        }
        "Location" {
            Write-Warning "Type = $Type, Title = $Title, Warning = Add \n\n between LIGHT and DARK text."
            "card `"$img`" `"$uniqueness$title ($destiny)\n$side $type - $subType [$rarity]\nSet: $set\nIcons: $icons\n\nText:\n{TODO: EDIT GAME TEXT}$gametext`""
        }
        "Objective" {
            Write-Warning "Type = $Type, Title = $Title, Warning = Add \n\n between FRONT and BACK text."
            "card `"/TWOSIDED$img`" `"$title (0/7)\n$side $type [$rarity]\nSet: $set\nIcons: $icons\n{TODO: EDIT GAME TEXT}$gametext`""
        }
        "Starship" {
            "card `"$img`" `"$title ($destiny)\n$side $type - $subType [$rarity]\nSet: $set\nPower: $power Armor: $armor Hyperspeed: $hyperspeed\nDeploy: $deploy Forfeit: $forfeit\nIcons: $icons\n\nLore: $lore\n\nText: $gametext`""
        }
        "Vehicle" {
            "card `"$img`" `"$title ($destiny)\n$side $type - $subType [$rarity]\nSet: $set\nPower: $power Armor: $armor Landspeed: $landspeed\nDeploy: $deploy Forfeit: $forfeit\nIcons: $icons\n\nLore: $lore\n\nText: $gametext`""
        }
        "Weapon" {
            "card `"$img`" `"$title ($destiny)\n$side $type - $subType [$rarity]\nSet: $set\nDeploy: $deploy Forfeit: $forfeit\n\nLore: $lore\n\nText: $gametext`""
        }
        default {
            Write-Error "Title = $title, Type = $type"
            Write-Error "Type = $Type, Title = $Title, Error = Card type not supported."
        }
    }
    $cdf = [PSCustomObject]@{
        Type    = $type
        SubType = $subType
        Line    = $line
    }
    Write-Output $cdf
} |
Sort-Object -Property "Type", "SubType", "Title" |
Select-Object -ExpandProperty "Line" |
Set-Content -Path $CdfPath
