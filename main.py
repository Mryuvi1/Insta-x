from instagrapi import Client

username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
target_username = "TARGET_USERNAME"  # <-- the person you want to DM

try:
    cl = Client()
    cl.login(username, password)
    print("✅ Login successful")

    user_id = cl.user_id_from_username(target_username)
    print("✅ Got user ID:", user_id)

    response = cl.direct_send("🔥 Test message from bot 🔥", [user_id])
    print("📨 DM Response:", response)

except Exception as e:
    print("❌ ERROR:", e)
