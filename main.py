from research_agent import run_research

def main():
    question = input("Enter your research question: ").strip()
    if not question:
        print("Please enter a question.")
        return
    result = run_research(question)
    print("\n" + "=" * 70)
    print(result["report"])
    print("=" * 70)
    print(f"\nSaved: {result['path']}")

if __name__ == "__main__":
    main()
