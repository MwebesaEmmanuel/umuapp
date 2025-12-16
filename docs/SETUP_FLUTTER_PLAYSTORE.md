# Step-by-step: Flutter (Android + Web) + Play Store

## 1) Install Flutter (Windows)

1. Download Flutter SDK (stable) and unzip, e.g. `C:\src\flutter`
2. Add `C:\src\flutter\bin` to your Windows PATH
3. Open PowerShell and run:
   - `flutter doctor`

## 2) Android Studio requirements

1. Install Android Studio
2. In Android Studio → SDK Manager:
   - Install **Android SDK Platform** (latest stable)
   - Install **Android SDK Build-Tools**
   - Install **Android SDK Command-line Tools**
3. Accept licenses:
   - `flutter doctor --android-licenses`
4. Re-check:
   - `flutter doctor`

## 3) Enable Flutter Web

- `flutter config --enable-web`

## 4) Create the Flutter app project in this repo

From repo root (`C:\umuapp`):

- `cd mobile`
- `flutter create mobile_app`

This will create `mobile/mobile_app/` (Android + Web targets included).

## 4b) Apply the prepared UI overlay

Copy:

- `mobile/overlay/lib/` → `mobile/mobile_app/lib/`

Then merge dependencies from:

- `mobile/overlay/pubspec_additions.yaml`

into:

- `mobile/mobile_app/pubspec.yaml`

Then run:

- `cd mobile\mobile_app`
- `flutter pub get`

## 5) Run locally

### Backend API

From repo root:

- `cd backend`
- `python -m venv .venv`
- `.\.venv\Scripts\Activate.ps1`
- `pip install -r requirements.txt`
- `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

Open: `http://localhost:8000/docs`

### Flutter (Android emulator or phone)

From repo root:

- `cd mobile\mobile_app`
- `flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000/api/v1`

V1 note: Google Maps is deferred (no billing needed yet).

### Flutter (Web)

- `flutter run -d chrome --dart-define=API_BASE_URL=http://localhost:8000/api/v1`

## 6) Build for Play Store (AAB)

1. Create a signing key (keep it safe):
   - `keytool -genkeypair -v -keystore umuapp-upload.jks -keyalg RSA -keysize 2048 -validity 10000 -alias umuapp`
2. Configure signing in `mobile/mobile_app/android/` (we will do this once the Flutter project exists)
3. Build the App Bundle:
   - `flutter build appbundle`
4. Upload `build/app/outputs/bundle/release/app-release.aab` to Google Play Console

## 7) Deploy Web

1. Build web:
   - `flutter build web`
2. Host the `build/web` folder (Firebase Hosting is the simplest)

## Next

After you run `flutter create mobile_app`, tell me and I’ll:

- Wire the Flutter UI to the backend endpoints
- Add Google Maps (offices + navigation)
- Add QR scanner (attendance)
- Add WebViews for `applications.umu.ac.ug`, UMU website, library, course evaluation
- Add “Community chat” screens + clubs
