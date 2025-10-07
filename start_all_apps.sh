#!/bin/bash
echo "Starting MDR Management System - All Three Applications"
echo "========================================================"
echo ""
echo "App 1: Portfolio Manager will run on http://localhost:5001"
echo "App 2: Scheduler will run on http://localhost:5002"
echo "App 3: Discipline Dashboard will run on http://localhost:5003"
echo ""
echo "Press Ctrl+C in each terminal to stop the apps"
echo ""

# Start App 1 in new terminal
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "cd app1_portfolio_manager && python app.py; exec bash"
    sleep 2
    gnome-terminal -- bash -c "cd app2_scheduler && python app.py; exec bash"
    sleep 2
    gnome-terminal -- bash -c "cd app3_discipline_dashboard && python app.py; exec bash"
elif command -v xterm &> /dev/null; then
    xterm -e "cd app1_portfolio_manager && python app.py" &
    sleep 2
    xterm -e "cd app2_scheduler && python app.py" &
    sleep 2
    xterm -e "cd app3_discipline_dashboard && python app.py" &
else
    echo "Please open three separate terminals and run:"
    echo "  Terminal 1: cd app1_portfolio_manager && python app.py"
    echo "  Terminal 2: cd app2_scheduler && python app.py"
    echo "  Terminal 3: cd app3_discipline_dashboard && python app.py"
fi

echo "All apps started!"

