from agent import MyOfficeAgent
 
 
def main():
    agent = MyOfficeAgent()
    print("Office Assistant ready. Type 'quit' to exit.\n")
    while True:
        user = input("You: ").strip()
        if user.lower() in {"quit", "exit"}:
            break
        if user:
            try:

                print(f"\nAssistant: {agent.chat(user)}\n")
            except Exception as e:
                print(f"Error: {e}\n")

 
 
if __name__ == "__main__":
    main()