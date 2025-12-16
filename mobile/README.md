# Mobile App (Flutter)

This repo is set up to use Flutter for a single codebase that builds for:

- Android (Google Play)
- iOS (Apple App Store)

## Prereqs

- Install Flutter SDK: https://docs.flutter.dev/get-started/install
- Android Studio (Android SDK + emulator)
- For iOS builds: macOS + Xcode (required by Apple)

## Create the app project

From repo root:

- `flutter create mobile_app`

Then we will wire it to the backend in `backend/`.

## UI code (already prepared)

After `flutter create mobile_app`, copy:

- `mobile/overlay/lib/` → `mobile/mobile_app/lib/`

and merge dependencies from:

- `mobile/overlay/pubspec_additions.yaml`
