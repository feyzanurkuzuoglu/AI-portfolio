from sys import argv
import locale
import string
locale.setlocale(locale.LC_ALL, "en_US")
def number_of_words(text1):
# cleaning list from punctuation
    punctuation = [".", ",", "!", ":", ";", "(", ")", "[", "]", "?", "{", "}"]
    cleanlist1 = []
    for character in text1:
        if character in punctuation:
            continue
        else:
            cleanlist1.append(character)
    cleantext = ''.join(cleanlist1)
# seperating words from each other to count number os words
    words = cleantext.split()
    return len(words)

def number_of_sentences(text2):
    sentences_in_text = 0
    nocare =["!", "?", "."]
    for harf in text2:
        if harf in nocare:
            sentences_in_text += 1
    sentences_in_text -= text2.count("...")*2
    return sentences_in_text

def average_word_number(text3):
    return number_of_words(text3) / number_of_sentences(text3)


def character_number(text4):
    return len(text4)


def number(text5):
    sonhal=[]
    all_letters=string.ascii_letters
    all_numbers=["0","1","2","3","4","5","6","7","8","9"]
    sayilacaklar= list(all_letters)+all_numbers+["'","-"]
    a=text5.count("' ")
    for i in text5:
        if i in sayilacaklar:
            sonhal.append(i)
    return len(sonhal)-a


def sirala(arg10):
    noktalama=[".", ",", "!", ":", ";", "(", ")", "[", "]", "?", "{", "}", "' ",'"']
    temizliste = []
    for character in arg10:
        if character in noktalama:
            continue
        else:
            temizliste.append(character)
    temizmetin = ''.join(temizliste)
    text8 = temizmetin.split()
    longestword = [" "]
    shortestword= [text8[0]]
    for kelime in text8:
        if len(kelime) < len(shortestword[0]):
            shortestword = [kelime]
        elif len(kelime) == len(shortestword[0]) and kelime not in shortestword:
            shortestword.append(kelime)
        if len(kelime)>len(longestword[0]):
            longestword = [kelime]
        elif len(kelime) == len(longestword[0]) and kelime not in longestword:
            longestword.append(kelime)
    dict_shortest={word:text8.count(word)/len(text8) for word in shortestword}
    dict_longest = {word: text8.count(word)/len(text8) for word in longestword}
    shortest_result=sorted(dict_shortest.items(), key=lambda x:(-x[1], x[0]))
    longest_result=sorted(dict_longest.items(), key=lambda y:(-y[1], y[0]))

    return shortest_result,longest_result

def frequency_of_words(text11):
    dict1 = {}
    noktalama = [".", ",", "!", ":", ";", "(", ")", "[", "]", "?", "{", "}",'"']
    temizliste = []
    for character in text11:
        if character in noktalama:
            continue
        else:
            temizliste.append(character)
    temizmetin = ''.join(temizliste)
    temizmetin=temizmetin.lower()
    text11 = temizmetin.split()
    dict1={}
    for word in text11:
        if word.endswith("'"):
            word1 = word[:-1]
            text11.remove(word)
            text11.append(word1)
        if word not in dict1:
            dict1[word] = text11.count(word)/len(text11)
    sortedfrequencies=sorted(dict1.items(), key=lambda x:(-x[1],x[0]))
    return [(word,text11.count(word)/len(text11)) for word, count in sortedfrequencies]


def main():
    f_in=open(argv[1],"r")
    content= f_in.read()
    words="#Words:"
    a=str(number_of_words(content))
    f_out=open(argv[2],"w")
    f_out.write(f"{words:24}{a}\n")
    sentences="#Sentences"
    b=str(number_of_sentences(content))
    f_out.write(f"{sentences:24}{b}\n")
    wordsentences="#Words/Sentences:"
    c=average_word_number(content)
    f_out.write(f"{wordsentences:24}{float(c):.2f}\n")
    characters="#Characters:"
    d= str(character_number(content))
    f_out.write(f"{characters:24}{d}\n")
    charactersjustwords= "#Characters(Just Words):"
    e=str(number(content))
    f_out.write(f"{charactersjustwords:24}{e}\n")
    f_out.write("Shortest Words:\n")
    shortest_result,longest_result=sirala(content)
    for word,frequency in shortest_result:
        f_out.write(f"{word:24}{frequency:.4f}\n")
    f_out.write("Longest Words:\n")
    for word,frequency in longest_result:
        f_out.write(f"{word:24}{frequency:.4f}\n")
    frequencies=frequency_of_words(content)
    for word,frequency in frequencies:
        f_out.write(f"{word:24}{frequency:.4f}\n")

main()