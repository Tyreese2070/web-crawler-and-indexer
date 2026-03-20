from src.indexer import Indexer
from src.crawler import crawl
from src.search import print_word, find_query

def main():
    print("Commands: build, load, print <word>, find <query>, exit")

    search_engine = Indexer()

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting")
            break

        command_parts = user_input.split(maxsplit=1)
        command = command_parts[0].lower()

        # Build command
        if command == "build":
            print("Crawling and building index")
            crawled_data = crawl("https://quotes.toscrape.com/")

            if crawled_data:
                print("Building index")
                search_engine.index = {}
                search_engine.build(crawled_data)
                search_engine.save()
                print("Built and saved index")
            else:
                print("Failed to crawl")

        # Load command
        elif command == "load":
            search_engine.load()
            if search_engine.index:
                print("Index loaded")
            else:
                print("Failed to load index, run build first")

        # Print command
        elif command == "print":
            if len(command_parts) < 2:
                print("Usage: print <word>")
            elif not search_engine.index:
                print("Index not loaded, run build or load first")
            else:
                print_word(search_engine, command_parts[1])
        
        # Find command
        elif command == "find":
            if len(command_parts) < 2:
                print("Usage: find <query>")
            elif not search_engine.index:
                print("Index not loaded, run build or load first")
            else:
                find_query(search_engine, command_parts[1])
        
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()