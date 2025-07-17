# PowerShell script to consolidate scattered files
Write-Host "========================================" -ForegroundColor Green
Write-Host "Consolidating scattered files to archive" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Create archive directories
$archiveOldDocs = "archive\old_docs"
$archiveOldScripts = "archive\old_scripts"

if (!(Test-Path $archiveOldDocs)) {
    New-Item -ItemType Directory -Path $archiveOldDocs -Force
    Write-Host "Created $archiveOldDocs" -ForegroundColor Yellow
}

if (!(Test-Path $archiveOldScripts)) {
    New-Item -ItemType Directory -Path $archiveOldScripts -Force
    Write-Host "Created $archiveOldScripts" -ForegroundColor Yellow
}

# Rename README_NEW.md to README.md
if (Test-Path "README_NEW.md") {
    if (Test-Path "README.md") {
        Move-Item "README.md" "$archiveOldDocs\README_old.md" -Force
        Write-Host "Moved old README.md to archive" -ForegroundColor Yellow
    }
    Rename-Item "README_NEW.md" "README.md"
    Write-Host "Renamed README_NEW.md to README.md" -ForegroundColor Green
}

# List of documentation files to move
$docsToMove = @(
    "API_CONFIGURATION_FIXES.md",
    "BOOMI_IFLOW_TESTING_GUIDE.md", 
    "BOOMI_IMPLEMENTATION_README.md",
    "BOOMI_IMPLEMENTATION_TEST_PLAN.md",
    "Context_current_status.md",
    "GEMMA3_INTEGRATION_LOG.md",
    "IFlow_e6d0c653_Issue_Analysis.md",
    "MULE2IS_DOCUMENTATION.md",
    "OData_RequestReply_Issues_and_Fixes.md",
    "PROJECT_CHANGES_LOG.md",
    "PROJECT_README.md",
    "SAP_DEPLOYER_USAGE_GUIDE.md",
    "SFTP_RequestReply_Fix_Summary.md",
    "boomi-to-sap-integration-flow.md",
    "cf_commands_reference.md"
)

# List of script files to move
$scriptsToMove = @(
    "auto_git_push_daily.bat",
    "deploy_fix.bat",
    "fix_api_deployment.bat", 
    "restart_frontend.bat",
    "test_api_routing.bat"
)

# Move documentation files
Write-Host "`nMoving documentation files..." -ForegroundColor Cyan
foreach ($file in $docsToMove) {
    if (Test-Path $file) {
        Move-Item $file $archiveOldDocs -Force
        Write-Host "Moved $file" -ForegroundColor Green
    }
}

# Move script files  
Write-Host "`nMoving script files..." -ForegroundColor Cyan
foreach ($file in $scriptsToMove) {
    if (Test-Path $file) {
        Move-Item $file $archiveOldScripts -Force
        Write-Host "Moved $file" -ForegroundColor Green
    }
}

# Clean up the consolidation script itself
if (Test-Path "consolidate_files.bat") {
    Move-Item "consolidate_files.bat" $archiveOldScripts -Force
    Write-Host "Moved consolidate_files.bat" -ForegroundColor Green
}

Write-Host "`n✅ File consolidation complete!" -ForegroundColor Green
Write-Host "`n📁 New clean structure:" -ForegroundColor Yellow
Write-Host "  README.md              - Main project overview" -ForegroundColor White
Write-Host "  HOW_TO_RUN_GUIDE.md    - Complete usage instructions" -ForegroundColor White  
Write-Host "  PROJECT_DOCS.md        - Technical details and architecture" -ForegroundColor White
Write-Host "  manage-project.bat     - Consolidated management script" -ForegroundColor White

Write-Host "`n📦 Archived files:" -ForegroundColor Yellow
Write-Host "  archive\old_docs\      - Old documentation files" -ForegroundColor White
Write-Host "  archive\old_scripts\   - Old script files" -ForegroundColor White

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
