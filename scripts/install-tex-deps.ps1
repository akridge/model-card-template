# PowerShell script for installing minimal TeX packages
# Must be run after installing TinyTeX

Write-Host "Installing minimal TeX packages..."
$packages = @(
    "xelatex",
    "geometry",
    "fancyhdr",
    "graphicx",
    "xcolor",
    "tcolorbox",
    "fontspec",
    "helvetic"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..."
    tlmgr install $package
}

Write-Host "Installation complete!"
