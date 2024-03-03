import trie

# Create a TrieNode instance
trie_root = trie.TrieNode()

# Insert words into the trie
trie_root.insert_trie("banana")
trie_root.insert_trie("orange")

# Search for words in the trie
print("Searching for 'apple':", trie_root.search_trie("apple"))
print("Searching for 'banana':", trie_root.search_trie("banana"))
print("Searching for 'grape':", trie_root.search_trie("grape"))

# Print the trie
print("Printing the trie:")
trie_root.print_trie()
