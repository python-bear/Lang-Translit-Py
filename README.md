# Lang-Translit-Py
Basic transliteration/transcription from IPA into a range of other languages, with choice of script and dialects.

It's pretty self explanatory, if you encounter any errors then you may want to go into verbosity.py and set line 43, which is ```s = Speaker(False)``` by default to ```s = Speaker(True)```, which will turn on verbosity. If you still can't figure out what's wrong it's probably that there are characters in your input that are confusing the program, such as non-ASCII punctuation or characters that aren't in the IPA, so remove those and try again before going on to debug the code at all.

If you want to make your own language for the transliteration menu you'll need to add it to ```ipa-to-lang.json```, you should be able to figure it out. But here is the basics of the structure:
```
{
  "__comment": {
    "msg 1": "this part shows all of the special rules you can add to characters, if you choose to add them, add them at the end of the character.",
    "msg 2": "For example, Greek Sigma is _"s": "σ$ς"_. The _$_ means that the sound _s_ is usually _σ_, except at the end of a word, where it becomes",
    "msg 3": "_ς_. When a list of possible transcriptions is provided the one who's rules, starting from the first, will be checked, and the first one",
    "msg 4": "that is followed properly is chosen. These special characters can therefore not be used in the actual transcription."
  },
  "language_name": {
    "script_one": {
      "main": {
        "m": "ḿ",
        "l": ["b<", "ḃ@ā/ï", "d"],
  
        "ab": "ğ",
        
        "ɔ": "ā",
        "e": "ï"
      },
      "extended-vowels": {
        "l": ["b<", "ḃ@ā/ï/ẏ", "d"],

        "ə": "ę",
        "ɪ": "ẏ"
      }
    }
    "script_two": {
      "main": {
        "m": "μ",
        "l": ["β<", "δ"],
  
        "ab": "γ",
        
        "ɔ": "ɑ̄",
        "e": "ι"
      },
      "extended-vowels": {
        "ə": "ę",
        "ɪ": "ẏ"
      }
      "pre-1900": {
        "m": "ν",
        "p": "φ",

        "ab": []  # this removes the "ab" check, so gets rid of it
      }
    }
  }
}
```

The above is an example of how to structure a language. Take note that a ```"main"``` section is not required, however each language needs to have at least one vowel and one consonant. So, if you're making an abjad (alphabet without vowels) then just add something like ```"ə": ""``` (the vowel can be any). You can also specify, say, ```" ": "-"```, which will make all spaces into dashes. You can also define ```"<"``` and ```">"```, to define a character to start and a character to go at the end of the text. Below is the list of special character you can use:
```
 < : Only at start of word.
 { : Only not at the start of word.

 > : Only at end of word.
 } : Only not at the end of word.

 @ : Only after the following character(s).
 ! : Only not after the following character(s).

 # : Only before the following character(s).
 * : Only not before the following character(s).

 & : Only after the following phonetic value(s).
 % : Only not after the following phonetic value(s).

 $ : Becomes the following char if at the end of a word.
 | : Only at the start of end of word.
```

You have to write them in the order that they appear above, like this: ```"ə": "e{#a/n/j"```, not like ```"ə": "e#a/n/j{"```.

Pretty much all of the languages and dialects and such are based off of information I could find on Wikipedia pages and Omniglot. The transcriptions are not perfect, but I'm 90% confident in them (10% of the time might not work, or around that). Specifically the Canadian Syllabics didn't turn out very well, just because of how it's not really a syllabus or an alphabet and also because of what I decided in the code was more important to get the best result (which works better with true alphabet, abjads, and syllabics). Also, this is far from the cleanest code I've ever written, it was meant to take me a couple of hours, but ended up taking a lot longer than that, so I wasn't bothered cleaning it up, so sorry to anyone who finds a need to look through it.

If you encounter any problems, want me to add anything, or have something to say feel free to email me at ```pythonbear@proton.me```.
