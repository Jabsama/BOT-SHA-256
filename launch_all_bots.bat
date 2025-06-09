@echo off
echo 🚀 Lancement de 3 bots VoltageGPU...


if exist "bot1\final_optimized_bot.py" (
    cd bot1
    start /B python final_optimized_bot.py
    echo ✅ Bot 1 lancé
    cd ..
) else (
    echo ❌ Bot 1 non trouvé
)

if exist "bot2\final_optimized_bot.py" (
    cd bot2
    start /B python final_optimized_bot.py
    echo ✅ Bot 2 lancé
    cd ..
) else (
    echo ❌ Bot 2 non trouvé
)

if exist "bot3\final_optimized_bot.py" (
    cd bot3
    start /B python final_optimized_bot.py
    echo ✅ Bot 3 lancé
    cd ..
) else (
    echo ❌ Bot 3 non trouvé
)

echo 🎉 Tous les bots sont lancés !
echo 💰 Vos 3 bots génèrent maintenant des revenus 24/7 !
pause
