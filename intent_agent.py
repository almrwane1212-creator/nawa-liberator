class NawaAgent:
    def __init__(self, user_name):
        self.user_name = user_name

    def ask_intent(self):
        print(f"\n--- مرحباً {self.user_name} في واحة 'نوى' ---")
        print("أنا وكيلك الشخصي، وظيفتي حمايتك من التشتت.")
        
        intent = input("ما هي نيتك الآن؟ (تعلم / ترفيه / إلهام): ")
        duration = input("كم دقيقة تخصص لهذا النشاط؟: ")
        
        print(f"\n✅ تم تفعيل 'وضع السيادة'.")
        print(f"سأقوم الآن بتنقية المحتوى ليركز فقط على ({intent}) لمدة {duration} دقيقة.")
        print("تذكر: أنت القائد، والخوارزمية في خدمتك.")

if __name__ == "__main__":
    agent = NawaAgent("المبدع")
    agent.ask_intent()
  
