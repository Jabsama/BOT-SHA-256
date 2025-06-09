# Script de lancement multi-bots VoltageGPU
Write-Host "🚀 Lancement de 3 bots VoltageGPU..." -ForegroundColor Green


# Lancement Bot 1
if (Test-Path "bot1/final_optimized_bot.py") {
    Set-Location "bot1"
    Start-Process python -ArgumentList "final_optimized_bot.py" -WindowStyle Hidden
    Write-Host "✅ Bot 1 lancé" -ForegroundColor Green
    Set-Location ".."
} else {
    Write-Host "❌ Bot 1 non trouvé" -ForegroundColor Red
}

# Lancement Bot 2
if (Test-Path "bot2/final_optimized_bot.py") {
    Set-Location "bot2"
    Start-Process python -ArgumentList "final_optimized_bot.py" -WindowStyle Hidden
    Write-Host "✅ Bot 2 lancé" -ForegroundColor Green
    Set-Location ".."
} else {
    Write-Host "❌ Bot 2 non trouvé" -ForegroundColor Red
}

# Lancement Bot 3
if (Test-Path "bot3/final_optimized_bot.py") {
    Set-Location "bot3"
    Start-Process python -ArgumentList "final_optimized_bot.py" -WindowStyle Hidden
    Write-Host "✅ Bot 3 lancé" -ForegroundColor Green
    Set-Location ".."
} else {
    Write-Host "❌ Bot 3 non trouvé" -ForegroundColor Red
}

Write-Host "🎉 Tous les bots sont lancés !" -ForegroundColor Green
Write-Host "📊 Vérification des processus..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue

Write-Host "💰 Vos 3 bots génèrent maintenant des revenus 24/7 !" -ForegroundColor Cyan
Read-Host "Appuyez sur Entrée pour continuer"
