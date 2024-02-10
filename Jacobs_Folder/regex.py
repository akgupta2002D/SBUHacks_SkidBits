import re
from collections import Counter

# Your sample text
sample_text = """
Um, I just want to say ah, that, um, this is like, basically, a demo of how so, you know, filler words can, um, 
make a speech less impactful. And like, when we repeat words, repeat words in a sentence, it's not effective. Yes Yes.
"""

# Your patterns
#crutch_words_pattern = r'\b(um|uh|ah|like|so|actually|basically|seriously|literally|okay|right|you know)\b'
crutch_words_pattern = r'\b(um|uh|ah|like|so|actually|basically|seriously|literally|okay|right|you\s*,*\s*know|honestly|' \
                           r'nevertheless|essentially|moreover|nonetheless|furthermore|consequently|i\s*mean|in\s*a\s*sense|' \
                           r'to\s*be\shonest|to\stell\s*you\sthe\struth|as\s*i\swas\ssaying|the\s*thing\sis|' \
                           r'at\s*the\send\sof\sthe\s*day|as\s*a\smatter\sof\s*fact|if\sy|will|as\s*far\s*as\s*i\s*know|' \
                           r'believe\s*me|to\s*be\s*fair|as\s*a\s*result|on\s*the\sother\shand|' \
                           r'to\s*put\s*it\sdifferently|to\s*some\s*extent|needless\s*to\s*say|in\s*any\s*case|' \
                           r'all\s*things\s*considered|to\s*my\s*knowledge|in\s*a\smanner\sof\sspeaking|mmm|hmm|uh-huh|mm-hmm|uh-oh|' \
                           r'huh|hmm-mm|uh-uh|erm|ahem|uhh|well,\s*you\s*see|oh|ooh|aha|duh|yikes)\b'
repetition_pattern = r'\b(\w+)\s+\1\b'

# Finding matches
expanded_crutch_words_found = re.findall(crutch_words_pattern, sample_text.lower())
direct_repetitions_found = re.findall(repetition_pattern, sample_text.lower())

# Count all word occurrences (this was missing)
words = re.findall(r'\b\w+\b', sample_text.lower()) # Find all whole words
word_counts = Counter(words) # Count occurrences of each word

# Filter for overused words (more than 2 occurrences)
overused_words = {word: count for word, count in word_counts.items() if count > 2}

# Results display
print("Expanded Crutch Words Found:")
for word in set(expanded_crutch_words_found):
    print(f"- '{word}' appeared {expanded_crutch_words_found.count(word)} times.")

print("\nDirect Repetitions Found:")
if direct_repetitions_found:
    for word in set(direct_repetitions_found):
        print(f"- '{word}' repeated directly.")
else:
    print("- No direct repetitions were found.")

print("\nOverused Words (more than 2 occurrences):")
for word, count in overused_words.items():
    print(f"- '{word}' appeared {count} times.")
