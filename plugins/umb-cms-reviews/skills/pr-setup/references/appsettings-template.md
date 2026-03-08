# Unattended Install Configuration Template

## appsettings.Development.json

Write this file to `src/Umbraco.Web.UI/appsettings.Development.json` in the worktree. It configures Umbraco for unattended install with SQLite and the admin credentials used for testing.

```json
{
  "ConnectionStrings": {
    "umbracoDbDSN": "Data Source=|DataDirectory|/Umbraco.sqlite.db;Cache=Shared;Foreign Keys=True;Pooling=True",
    "umbracoDbDSN_ProviderName": "Microsoft.Data.Sqlite"
  },
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "Microsoft.Hosting.Lifetime": "Information",
        "System": "Warning"
      }
    }
  },
  "Umbraco": {
    "CMS": {
      "Unattended": {
        "InstallUnattended": true,
        "UnattendedUserName": "Test Admin",
        "UnattendedUserEmail": "admin@test.com",
        "UnattendedUserPassword": "TestPassword1234!"
      },
      "Content": {
        "Notifications": {
          "Email": "admin@test.com"
        }
      },
      "Global": {
        "DefaultUILanguage": "en-us",
        "HideTopLevelNodeFromPath": true,
        "TimeOut": "00:20:00",
        "UseHttps": false
      },
      "Hosting": {
        "Debug": true
      },
      "Security": {
        "KeepUserLoggedIn": true,
        "UsernameIsEmail": true,
        "UserPassword": {
          "RequiredLength": 10,
          "RequireNonLetterOrDigit": false,
          "RequireDigit": false,
          "RequireLowercase": false,
          "RequireUppercase": false,
          "MaxFailedAccessAttemptsBeforeLockout": 50
        }
      },
      "ModelsBuilder": {
        "ModelsMode": "InMemoryAuto"
      }
    }
  }
}
```

## Key Settings Explained

| Setting | Value | Why |
|---------|-------|-----|
| `InstallUnattended` | `true` | Skip the installer wizard, auto-create database |
| `UnattendedUserEmail` | `admin@test.com` | The login email for browser testing |
| `UnattendedUserPassword` | `TestPassword1234!` | Must be 10+ chars (matches `RequiredLength`) |
| `KeepUserLoggedIn` | `true` | Prevents session timeouts during testing |
| `MaxFailedAccessAttemptsBeforeLockout` | `50` | Prevents lockout during automated testing |
| `Debug` | `true` | Better error messages for debugging |
| `UseHttps` | `false` | Simpler for local testing, avoids cert issues |
| `PackageMigrationsUnattended` | (default: true) | Not set explicitly because the default is already `true` — this allows the Clean Starter Kit to install its content automatically |

## Starter Kit

A starter kit is optionally installed as a NuGet package reference (see Step 3 in the main skill). On first startup with `PackageMigrationsUnattended: true`, it runs its package migrations which create content types, templates, sample content, and media.

After a starter kit installs, you may need to publish the root content node for the frontend to work. The backoffice is fully functional regardless.

If no starter kit is selected, Umbraco starts with an empty content tree — just the backoffice shell.

## Database

SQLite is used because:
- Zero configuration — no external database server needed
- Self-contained in the worktree — easy to clean up
- Fast for single-user testing scenarios
- The database file lives at `src/Umbraco.Web.UI/umbraco/Data/Umbraco.sqlite.db`

To reset: delete the `umbraco/Data/` directory and restart.
