from identity_engine import generate_nawa_did
from intent_agent import NawaAgent

def start_nawa_session():
    print("--- 🛡️ نظام نـوى (NAWA) للتحرر الرقمي ---")
    
    # 1. إنشاء الهوية اللامركزية (السيادة)
    user_secret = input("أدخل جملة سرية لتأمين هويتك: ")
    user_did = generate_nawa_did(user_secret)
    print(f"✅ تم تفعيل هويتك اللامركزية: {user_did}")
    
    # 2. تشغيل الوكيل الذكي (القيادة)
    user_name = input("\nما هو اسمك المستعار؟: ")
    agent = NawaAgent(user_name)
    
    # 3. بدء جلسة النية
    agent.ask_intent()
    
    print("\n--- 🏁 نهاية الجلسة.. شكراً لكونك سيد قرارك! ---")

if __name__ == "__main__":
    start_nawa_session()
  
