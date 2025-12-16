# Play Store release (V1)

## 1) Choose package id

It must look like a domain name and be unique, e.g.:

- `ug.ac.umu.umuapp` (recommended)

## 2) Set the package id in Flutter

Update `mobile/mobile_app/android/app/build.gradle.kts`:

- `namespace = "ug.ac.umu.umuapp"`
- `applicationId = "ug.ac.umu.umuapp"`

Then run:

- `flutter clean`
- `flutter pub get`

## 3) Create signing key (upload key)

Run in `mobile/mobile_app`:

- `keytool -genkeypair -v -keystore umuapp-upload.jks -keyalg RSA -keysize 2048 -validity 10000 -alias umuapp`

Keep the `.jks` safe (backup).

## 4) Configure release signing

Create `mobile/mobile_app/android/key.properties` (do not commit) with:

```
storePassword=YOUR_STORE_PASSWORD
keyPassword=YOUR_KEY_PASSWORD
keyAlias=umuapp
storeFile=../umuapp-upload.jks
```

`mobile/mobile_app/android/app/build.gradle.kts` is already wired to use `key.properties`.

## 5) Build AAB

- `flutter build appbundle --release --dart-define=API_BASE_URL=https://YOUR_RENDER_API/api/v1`

## 6) Upload to Google Play

- Start with **Internal testing**
- Add testers
- Verify login/chat/news/video in release build
- Then rollout to Production
