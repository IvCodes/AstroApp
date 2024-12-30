# AstroApp
Simple Astrology Application

## Environment Variables

The application uses environment variables for configuration. To get started:

1. Copy `.env.example` to `.env`
   ```bash
   cp Backend/.env.example Backend/.env
   ```

2. Modify the `.env` file with your specific settings:

   | Variable | Description | Default |
   |----------|-------------|---------|
   | `PORT` | Port the server runs on | `8000` |
   | `HOST` | Host address | `0.0.0.0` |
   | `APP_TITLE` | Application title | `Birth Time Estimator` |
   | `APP_DESCRIPTION` | Description shown on the form | `Estimate your birth time based on Lagna` |
   | `ENABLE_DARK_MODE` | Toggle dark mode | `false` |

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python Backend/run.py
```

**Note:** Never commit your actual `.env` file to version control. Use `.env.example` as a template.
