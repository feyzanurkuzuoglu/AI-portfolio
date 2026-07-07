import locale
import sys
locale.setlocale(locale.LC_ALL, "en_US")

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    name1 = sys.argv[1]
    output_file = sys.argv[2]
    name = name1.split(".")[0]

    try:
        with open(name1, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{name1}' not found.")
        sys.exit(1)


    text = text.lower()

    punctuation = ".,!?;:'\"()[]{}<>-_+=|\\^~`*/"

    # remove punctuations and "'s" and replace with a space
    cleaned_text = []
    words = text.split()
    for word in words:
        if word.endswith("'s"):  # Remove "'s"
            word = word[:-2]
        cleaned_text.append(''.join([char if char not in punctuation else ' ' for char in word]))

    # Join the cleaned words and split into final words
    cleaned_text = ' '.join(cleaned_text)
    words = cleaned_text.split()


# using search algorithm to find shortest and longest word
    shortest_word = words[0]
    longest_word = words[0]

    for word in words:
        # if the new word is shorter, change it
        if len(word) < len(shortest_word):
            shortest_word = word
        if len(word) > len(longest_word):
            longest_word = word


# counting words and adding to dictionary
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

# to find frequency
    shortest_word_count = words.count(shortest_word)
    longest_word_count = words.count(longest_word)

# the number of times each word occurs to find frequency
    summ=[]
    for a ,b in word_counts.items():
        summ.append(b)
    m = sum(summ)

# to find number of all characters
    characters = []
    for word in text:
        for w in word:
            characters.append(w)

# to count words remove spaces and every word becomes a list element
    cleaned_text2 = "".join(cleaned_text.split())

    # number of sentences
    sentences = []
    sentence_count = 0
    end = ".!?"
    start = 0
    for i, e in enumerate(text):
        if e in end:
            sentence_count += 1
            sentence = text[start:i + 1].strip()
            sentences.append(sentence)
            start = i + 1

# Calculating Average Number of Words per Sentence
    list =[]
    for sen in sentences:
        wordss = sen.split()
        wordcount = len(wordss)
        list.append(wordcount)
    average = sum(list) / len(list)



    print(f"""Statistics about {name}:
    #Words                  : {len(word_counts)}
    #Sentences              : {sentence_count}
    #Words/#Sentences       : {average:.2f}
    #Characters             : {len(characters)}
    #Characters (Just Words): {len(cleaned_text2)}
    The Shortest Word       : {shortest_word}                                   {word_counts[shortest_word] / m:.4f}
    The Longest Word        : {longest_word}                        {word_counts[longest_word] / m:.4f}\n""")
    for word, count in sorted(word_counts.items(), key=lambda item: item[1], reverse=True):
        print('{}: {:.4f}'.format(word, int(count)/m))



    with open(output_file, "w",encoding="utf-8") as file:
        file.write(f"""Statistics about {name}:
    #Words                  : {len(word_counts)}
    #Sentences              : {sentence_count}
    #Words/#Sentences       : {average:.2f}
    #Characters             : {len(characters)}
    #Characters (Just Words): {len(cleaned_text2)}
    The Shortest Word       : {shortest_word}                                      {word_counts[shortest_word] / m:.4f}
    The Longest Word        : {longest_word}                        {word_counts[longest_word] / m:.4f}\n""")
        for word, count in sorted(word_counts.items(), key=lambda item: item[1], reverse=True):
            file.write('{}: {:.4f}\n'.format(word, int(count) / m))

if __name__ == "__main__":
    main()




