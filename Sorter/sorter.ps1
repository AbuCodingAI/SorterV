# Sorter PowerShell Module
# Usage: .\sorter.ps1 -Folder "C:\path" -Keyword "backup" -Action list

param(
    [Parameter(Mandatory=$true)]
    [string]$Folder,
    
    [Parameter(Mandatory=$true)]
    [string]$Keyword,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("list", "delete", "copy", "move")]
    [string]$Action = "list",
    
    [Parameter(Mandatory=$false)]
    [string]$Destination,
    
    [Parameter(Mandatory=$false)]
    [switch]$CaseSensitive,
    
    [Parameter(Mandatory=$false)]
    [switch]$NoPlural
)

# Validate folder exists
if (-not (Test-Path $Folder)) {
    Write-Error "Folder not found: $Folder"
    exit 1
}

# Generate search keywords
function Get-SearchKeywords {
    param([string]$Keyword, [bool]$CaseSensitive, [bool]$IncludePlural)
    
    $keywords = @($Keyword)
    
    if (-not $CaseSensitive) {
        $keywords += $Keyword.ToLower()
        $keywords += $Keyword.ToUpper()
        $keywords += (Get-Culture).TextInfo.ToTitleCase($Keyword.ToLower())
    }
    
    if ($IncludePlural -and $Keyword.EndsWith('s')) {
        $base = $Keyword.Substring(0, $Keyword.Length - 1)
        $keywords += $base
        if (-not $CaseSensitive) {
            $keywords += $base.ToLower()
            $keywords += $base.ToUpper()
            $keywords += (Get-Culture).TextInfo.ToTitleCase($base.ToLower())
        }
    }
    
    return $keywords | Select-Object -Unique
}

# Search for matching files
function Find-MatchingFiles {
    param([string]$Folder, [string[]]$Keywords)
    
    $results = @()
    $items = Get-ChildItem -Path $Folder -Recurse -Force -ErrorAction SilentlyContinue
    
    foreach ($item in $items) {
        foreach ($keyword in $Keywords) {
            if ($item.Name -like "*$keyword*") {
                $results += $item.FullName
                break
            }
        }
    }
    
    return $results
}

# Main execution
$includePlural = -not $NoPlural
$keywords = Get-SearchKeywords -Keyword $Keyword -CaseSensitive $CaseSensitive -IncludePlural $includePlural
$matchingFiles = Find-MatchingFiles -Folder $Folder -Keywords $keywords

Write-Host "Found $($matchingFiles.Count) item(s) matching '$Keyword'" -ForegroundColor Cyan

if ($matchingFiles.Count -eq 0) {
    exit 0
}

# Display results
Write-Host "`nResults:" -ForegroundColor Green
$matchingFiles | ForEach-Object { Write-Host "  $_" }

# Perform action
switch ($Action) {
    "list" {
        Write-Host "`nAction: List (default)" -ForegroundColor Yellow
    }
    
    "delete" {
        $confirm = Read-Host "`nDelete $($matchingFiles.Count) item(s)? (yes/no)"
        if ($confirm -eq "yes") {
            $deleted = 0
            foreach ($file in $matchingFiles) {
                try {
                    Remove-Item -Path $file -Recurse -Force -ErrorAction Stop
                    $deleted++
                    Write-Host "Deleted: $file" -ForegroundColor Green
                } catch {
                    Write-Host "Error deleting $file : $_" -ForegroundColor Red
                }
            }
            Write-Host "`nDeleted $deleted item(s)" -ForegroundColor Green
        } else {
            Write-Host "Cancelled" -ForegroundColor Yellow
        }
    }
    
    "copy" {
        if (-not $Destination) {
            Write-Error "Destination required for copy action"
            exit 1
        }
        
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
        $copied = 0
        
        foreach ($file in $matchingFiles) {
            try {
                $destPath = Join-Path $Destination (Split-Path $file -Leaf)
                Copy-Item -Path $file -Destination $destPath -Recurse -Force
                $copied++
                Write-Host "Copied: $file" -ForegroundColor Green
            } catch {
                Write-Host "Error copying $file : $_" -ForegroundColor Red
            }
        }
        Write-Host "`nCopied $copied item(s) to $Destination" -ForegroundColor Green
    }
    
    "move" {
        if (-not $Destination) {
            Write-Error "Destination required for move action"
            exit 1
        }
        
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
        $moved = 0
        
        foreach ($file in $matchingFiles) {
            try {
                $destPath = Join-Path $Destination (Split-Path $file -Leaf)
                Move-Item -Path $file -Destination $destPath -Force
                $moved++
                Write-Host "Moved: $file" -ForegroundColor Green
            } catch {
                Write-Host "Error moving $file : $_" -ForegroundColor Red
            }
        }
        Write-Host "`nMoved $moved item(s) to $Destination" -ForegroundColor Green
    }
}
