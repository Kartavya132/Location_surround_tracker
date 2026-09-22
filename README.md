# Location_surround_tracker

A small Python app for calculating the distance between two coordinate points and checking whether the distance falls below an alarm threshold.

## Run it without an IDE

1. Open the project folder in File Explorer.
2. Double-click the file named `start_app.bat`.
3. The application window will open and you can enter coordinates and compute the distance.

## Manual run

If you prefer the terminal, run:

```powershell
python main.py
```

## Files in this project

- `main.py` – command-line version
- `app.py` – desktop application interface
- `start_app.bat` – Windows shortcut for launching the app without an IDE
- `func/request.py` – coordinate and CSV logic
- `func/function.py` – input and alarm helpers

