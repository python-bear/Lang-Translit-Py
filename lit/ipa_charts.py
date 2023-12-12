import math
import emoji
import string
import unicodeblock.blocks

from verbosity import *


cleaning_dict = {
    "w̃": "w",
    "h̪͆": "x",
    "h̃": "h",
    "j̃": "j",
    "t̪ʙ̥": "t",
    "ɥ": "j",
    "ʍ": "hw",
    "g": "ɡ",
    "ɚ": "əɹ",
    "ɝ": "ɜɹ",
    "ɻ̍": "ɹ",
    "ʴ": "ɹ",
    "ᶏ": "aɹ",
    "ᶕ": "əɹ",
    "ᶒ": "eɹ",
    "ᶗ": "ɔɹ",
    "˞": "ɹ",
    ":": "ː",
    "ˌ": "",
    ".": "",
    "͜": "",
    "͝": "",
    "͡": "",
    "̞": ""
}


def get_key_from_value(dictionary, target_value):
    for key, value in dictionary.items():
        if target_value in value:
            return key
    return None


def coord_distance(coord1: tuple, coord2: tuple):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def is_punctuation_or_whitespace(char):
    try:
        return unicodeblock.blocks.of(char) in ["GENERAL_PUNCTUATION", "CURRENCY_SYMBOLS", "LETTERLIKE_SYMBOLS",
                                                "NUMBER_FORMS", "ARROWS", "MATHEMATICAL_OPERATORS",
                                                "CONTROL_PICTURES", "MISCELLANEOUS_TECHNICAL", "ENCLOSED_ALPHANUMERICS",
                                                "BOX_DRAWING", "BLOCK_ELEMENTS", "DINGBATS", "MISCELLANEOUS_SYMBOLS"] \
               or char in [*string.punctuation, *string.digits, *emoji.EMOJI_DATA.keys()] or char.isspace() or char in \
               "⟨⟩¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿×˙"
    except TypeError:
        for chr in char:
            result = unicodeblock.blocks.of(chr) in ["GENERAL_PUNCTUATION", "CURRENCY_SYMBOLS", "LETTERLIKE_SYMBOLS",
                                                      "NUMBER_FORMS", "ARROWS", "MATHEMATICAL_OPERATORS",
                                                      "CONTROL_PICTURES", "MISCELLANEOUS_TECHNICAL",
                                                      "ENCLOSED_ALPHANUMERICS", "BOX_DRAWING", "BLOCK_ELEMENTS",
                                                      "DINGBATS", "MISCELLANEOUS_SYMBOLS"] \
                     or chr in [*string.punctuation, *string.digits, *emoji.EMOJI_DATA.keys()] or chr.isspace() or \
                     chr in "⟨⟩¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿×˙"
            if result:
                return True
        return False


def find_closest_coordinate(target_coords: list, coordinates: list) -> tuple:
    if isinstance(target_coords[0], (tuple, list)):
        min_distance = float('inf')
        closest_pair = None

        for i in range(len(coordinates)):
            total_distance = []
            for j in range(len(target_coords)):
                total_distance.append(coord_distance(target_coords[j], coordinates[i][j]))

            total_distance = sum(total_distance) / len(total_distance)

            if total_distance < min_distance:
                min_distance = total_distance
                closest_pair = coordinates[i]

        return closest_pair, min_distance
    else:
        min_distance = float('inf')
        closest_coord = None

        for coord in coordinates:
            distance = coord_distance(target_coords[0], coord)
            if distance < min_distance:
                min_distance = distance
                closest_coord = coord

        return closest_coord, min_distance


def remove_none_entries(pool):
    cleaned_list1 = []
    cleaned_list2 = []

    for item1, item2 in zip(pool[0], pool[1]):
        if item2 is not None:
            cleaned_list1.append(item1)
            cleaned_list2.append(item2)

    return [cleaned_list1, cleaned_list2]


class IPAChart:
    def __init__(self):
        self.containers = "[]/{}()⸨⸩⟦⟧⫽|‖⟨⟩⟪⟫'\""
        self.vowel_list = ["i", "y", "ɨ", "ʉ", "ɯ", "u", "ɪ", "ʏ", "ʊ", "e", "ø", "ɘ", "ɵ", "ɤ", "o", "e̞", "ø̞", "ə",
                           "ə", "ɤ̞", "o̞", "ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ", "æ", "ɐ", "ɐ", "a", "ɶ", "ä", "", "ɑ", "ɒ"]
        self.layer_correction = {
            0: 0,
            1: 21,
            2: 41,
            3: 45,
            4: 50,
            5: 59,
            6: 65,
            7: 77,
            8: 84,
            9: 93,
        }
        self.special_replacement = {
            "w": "ʋ",
            "ɫ": "l",
            "ɥ": "ɣ",
            "ɥ̊": "ɣ",
            "ʜ": "ʀ",
            "ʢ": "ʕ",
            "ʡ": "ʔ",
            "ɺ": "ɭ",
            "ɧ": "x",
            "ɕ": "ʃ",
            "ʑ": "ʒ",
            "ᵻ": "ɨ"
        }
        self.fillers = "~!@#$%^&*()_+`1234567890-={}|[]\\:\";'<>?,./'"
        self.extras = ["ʰ", "ː", "ʼ", "̃", "ʷ", "ˠ", "ʰ", "ʲ", "ˤ", "ˑ", "ˣ", "ᶿ", "ᵊ", "ˡ", "ⁿ", "̞", "̆", "̃", "ˈ"]
        self.vowels = [
            [  # close
                "u", "ɯ", "", "", "", "ʉ", "ɨ", "", "", "", "y", "i"],
            [  # near-close
                "", "", "ʊ", "", "", "", "", "", "ʏ", "ɪ", "", ""],
            [  # close-mid
                "o", "ɤ", "", "", "ɵ", "ɘ", "", "", "ø", "e"],
            [  # mid
                "o̞", "ɤ̞", "", "", "ə", "ə", "", "ø̞", "e̞"],
            [  # open-mid
                "ɔ", "ʌ", "", "ɞ", "ɜ", "", "œ", "ɛ"],
            [  # near-open
                "", "", "", "ɐ", "ɐ", "", "", "æ"],
            [  # open
                "ɒ", "ɑ", "", "ä", "ɶ", "a"],
        ]
        self.pulmonic_consonants = [
            [  # nasal
                "m̥", "m", "", "ɱ", "", "n̼", "n̥", "n", "n̥", "n", "n̥", "n", "ɳ̊", "ɳ", "ɲ̊", "ɲ", "ŋ̊", "ŋ", "ɴ̥", "ɴ", "",
                "", "", ""],
            [  # sibilant fricative
                "", "", "", "", "", "", "s", "z", "s", "z", "ʃ", "ʒ", "ʂ", "ʐ", "ɕ", "ʑ", "", "", "", "", "", "", "",
                ""],
            [  # plosive
                "p", "b", "p̪", "b̪", "t̼", "d̼", "t", "d", "t", "d", "t", "d", "ʈ", "ɖ", "c", "ɟ", "k", "ɡ", "q", "ɢ",
                "ʡ", "", "ʔ", ""],
            [  # non-sibilant fricative
                "ɸ", "β", "f", "v", "θ̼", "ð̼", "θ", "ð", "θ̠", "ð̠", "ɹ̠̊˔", "ɹ̠˔", "ɻ̊˔", "ɻ˔", "ç", "ʝ", "x", "ɣ", "χ",
                "ʁ", "ħ", "ʕ", "h", "ɦ"],
            [  # approximant
                "", "β̞", "", "ʋ", "", "", "", "ð̞", "", "ɹ", "", "ɹ̠", "", "ɻ", "", "j", "", "ɰ", "", "", "", "", "", "ʔ̞"],
            [  # tap/flap
                "", "ⱱ̟", "", "ⱱ", "", "ɾ̼", "ɾ̥", "ɾ", "ɾ̥", "ɾ", "ɾ̥", "ɾ", "ɽ̊", "ɽ", "", "", "", "", "", "ɢ̆", "", "ʡ̆",
                "", ""],
            [  # trill
                "ʙ̥", "ʙ", "", "", "", "", "r̥", "r", "r̥", "r", "r̥", "r", "", "", "", "", "", "", "ʀ̥", "ʀ", "ʜ", "ʢ",
                "", ""],
            [  # lateral fricative
                "", "", "", "", "", "", "ɬ", "ɮ", "ɬ", "ɮ", "ɬ", "ɮ", "ꞎ", "𝼅", "𝼆", "ʎ̝", "𝼄", "ʟ̝", "", "", "", "", "",
                ""],
            [  # lateral approximant
                "", "", "", "", "", "", "", "l", "", "l", "", "l", "", "ɭ", "", "ʎ", "", "ʟ", "", "ʟ̠", "", "", "", ""],
            [  # lateral tap/flap
                "", "", "", "", "", "", "ɺ̥", "ɺ", "ɺ̥", "ɺ", "ɺ̥", "ɺ", "𝼈̥", "𝼈", "", "ʎ̆", "", "ʟ̆", "", "", "", "", "",
                ""],
        ]

    def split_with_extras(self, ipa: str) -> list:
        split_ipa = []
        i = 0

        while i < len(ipa):
            remaining_length = len(ipa[i:]) + 1
            found = False

            if is_punctuation_or_whitespace(ipa[i]):
                split_ipa.append(ipa[i])
                i += 1
                continue

            else:
                if ipa[i] == "ˈ":
                    yon = 1
                else:
                    yon = 0

                try:
                    if ipa[i + 1 + yon] in ipa_chart.extras and ipa[i + 1 + yon] != "ˈ":
                        yon += 1
                except IndexError:
                    split_ipa.append(ipa[i:])
                    break

                viewport = ipa[i:i + 1 + yon]
                if viewport[-1] == "ˈ":
                    evade = 1
                else:
                    evade = 0
                viewport = ipa[i:i + 1 + yon - evade]

                split_ipa.append(viewport)
                i += 1 + yon - evade

        return split_ipa

    def vowel_pattern(self, text: str) -> str:
        vowel_pattern = ""
        for char in text:
            vowel_pattern += "v" if self.is_vowel(char) else "c" if self.is_consonant(char) else ""
        return vowel_pattern

    def get_closest_in_pool(self, target_ipa: str, possibility: list, return_distance: bool = False):
        if is_punctuation_or_whitespace(target_ipa[-1]):
            s.speak(f"getting closest for {target_ipa} in the pool: INAPPLICABLE")
            return None, None

        cleaned_ipa = target_ipa
        for extra in self.extras:
            cleaned_ipa = cleaned_ipa.replace(extra, "")

        ipa = [[target_ipa] if len(cleaned_ipa) == 1 else self.split_with_extras(target_ipa), []]
        vowel_pattern = self.vowel_pattern(target_ipa)

        pool = [self.split_with_extras(char) for char in possibility if self.vowel_pattern(char) == vowel_pattern and
                not is_punctuation_or_whitespace(char) and self.split_with_extras(char)[0] not in self.extras]
        pool = [pool, [[] for _ in range(len(pool))]]

        for y, seq in enumerate(pool[0]):
            for i in range(len(seq)):
                pool[1][y].append(self.iter_pool_find(seq[i], True if vowel_pattern[i] == "v" else False))

        pool = remove_none_entries(pool)

        for i in range(len(ipa[0])):
            ipa[1].append(self.iter_pool_find(ipa[0][i], True if vowel_pattern[i] == "v" else False))

        if ipa[1] is None:
            s.speak(ipa[1])
            return ""

        try:
            if pool == [[], []]:
                raise UnboundLocalError

            s.speak(f"getting closest for {ipa} ({vowel_pattern}) in the pool: {pool}")

            try:
                closest_seq, distance = find_closest_coordinate(ipa[1], pool[1])
            except TypeError:
                raise UnboundLocalError

            # is_long = ""
            #
            # for seq in pool[0]:
            #     for extra in self.extras:
            #         if f"{pool[0][pool[1].index(closest_seq)]}{extra}" == seq:
            #             is_long = extra
            #
            # found = False
            #
            # for extra in self.extras:
            #     if extra not in target_ipa:
            #         found = True
            #
            # if found:
            #     is_long = ""

            if return_distance:
                if closest_seq is None:
                    s.speak(f"getting closest for {ipa} ({vowel_pattern}) in the pool: INAPPLICABLE")
                    return None, None
                else:
                    return "".join(seq for seq in pool[0][pool[1].index(closest_seq)]), distance
            else:
                if closest_seq is None:
                    s.speak(f"getting closest for {ipa} ({vowel_pattern}) in the pool: INAPPLICABLE")
                    return None
                else:
                    return "".join(seq for seq in pool[0][pool[1].index(closest_seq)])
        except UnboundLocalError:
            s.speak(f"getting closest for {ipa} ({vowel_pattern}) in the pool: INAPPLICABLE")
            if return_distance:
                return None, None
            else:
                return None

    def is_vowel(self, target: str):
        if target in self.extras or is_punctuation_or_whitespace(target):
            return False

        found_consonant = False

        for char in self.strip_extras(target):
            if char not in self.vowel_list:
                found_consonant = True

        return not found_consonant

    def is_consonant(self, target: str):
        if target in self.extras or is_punctuation_or_whitespace(target):
            return False

        found_vowel = False

        for char in self.strip_extras(target):
            if char in self.vowel_list:
                found_vowel = True

        return not found_vowel

    def iter_pool_find(self, target: str, is_vowel: bool):
        if target in ["∅", *self.extras, *[char for char in self.containers]] or is_punctuation_or_whitespace(target):
            return None

        elif target in self.special_replacement.keys():
            return self.iter_pool_find(self.special_replacement[target], is_vowel)

        coord = None

        for j, manner in enumerate(self.pulmonic_consonants):
            for i, char in enumerate(manner):
                if char == self.strip_extras(target):
                    if is_vowel:
                        coord = (j, i)
                    else:
                        coord = (self.layer_correction[j], i)

        if coord is None:
            for j, manner in enumerate(self.vowels):
                for i, char in enumerate(manner):
                    if char == self.strip_extras(target):
                        if is_vowel:
                            coord = (j, i)
                        else:
                            coord = (self.layer_correction[j], i)

        return coord

    def strip_extras(self, ipa: list | str) -> list | str:
        if isinstance(ipa, str):
            for extra in self.extras:
                ipa = ipa.replace(extra, "")
            return ipa
        else:
            final_ipa = []
            for phoneme in ipa:
                for extra in self.extras:
                    final_ipa.append(phoneme.replace(extra, ""))
            return final_ipa

    def ipa_to_coords(self, ipa: str, longest_length: int) -> list[list[str], list[tuple]]:
        s.speak("CONVERTING IPA INTO PHONEME COORDINATE LIST", "heading")
        i = 0
        coords = [[], []]

        while i < len(ipa):
            remaining_length = len(ipa[i:]) + 1
            found = False
            print(f"{ipa[i]} was found to be: {is_punctuation_or_whitespace(ipa[i])}")
            if ipa[i] in ["<", ">"] or is_punctuation_or_whitespace(ipa[i]):
                s.speak(f"for i = {i}, viewport = {fr.BLUE}{ipa[i]}{fr.WHITE}|\tresorting match for {ipa[i]}: {None}")
                coords[0].append(ipa[i])
                coords[1].append(None)
                i += 1

            else:
                length_to_go_through = longest_length if remaining_length > longest_length else remaining_length
                for l in range(length_to_go_through).__reversed__():
                    if not found:
                        if ipa[i] == "ˈ":
                            yon = 1
                        else:
                            yon = 0

                        try:
                            s.speak(f"for i = {i}, viewport = {fr.BLUE}{ipa[i:i + l + yon]}{fr.WHITE}|\tchecking if "
                                    f"yon is applicable:\t{fr.BLUE}{ipa[i:i + yon + 1]}{fr.WHITE}{bk.BLUE}"
                                    f"{ipa[i + yon + 1:i + yon + 2]}", end="")
                            if ipa[i + 1 + yon] in ipa_chart.extras and ipa[i + 1 + yon] != "ˈ":
                                yon += 1
                                s.speak(f"\t... it is")
                            else:
                                s.speak(f"\t... it isn't")
                        except IndexError:
                            s.speak(f"for i = {i}, viewport = {fr.BLUE}{ipa[i:i + l + yon]}{fr.WHITE}|\tchecking if "
                                    f"yon is applicable:\t{fr.BLUE}{ipa[i:i + yon + 1]}{fr.WHITE}{bk.BLUE}"
                                    f"{ipa[i + yon + 1:i + yon + 2]}\t... it isn't", "info")

                        viewport = ipa[i:i + l + yon]
                        if viewport[-1] == "ˈ":
                            evade = 1
                        else:
                            evade = 0
                        viewport = ipa[i:i + l + yon - evade]

                        potential_coord = self.iter_pool_find(viewport, self.is_vowel(viewport))

                        s.speak(f"for i = {i}, viewport = {fr.BLUE}{viewport}{fr.WHITE}|\tl = {l}\tyon = {yon}\t"
                                f"potential = {potential_coord}")

                        if potential_coord is not None:
                            s.speak(f"for i = {i}, viewport = {fr.BLUE}{viewport}{fr.WHITE}|\tfound match for "
                                    f"{viewport}: {potential_coord}")
                            coords[0].append(viewport)
                            coords[1].append(potential_coord)
                            found = True
                            i += l + yon - evade

        return coords

ipa_chart = IPAChart()

# self.pulmonic_consonants = [
#             [  # nasal
#                 "m̥", "m", "", "ɱ", "", "n̼", "n̥", "n", "n̥", "n", "n̥", "n", "ɳ̊", "ɳ", "ɲ̊", "ɲ", "ŋ̊", "ŋ", "ɴ̥", "ɴ", "",
#                 "", "", ""],
#             [  # plosive
#                 "p", "b", "p̪", "b̪", "t̼", "d̼", "t", "d", "t", "d", "t", "d", "ʈ", "ɖ", "c", "ɟ", "k", "ɡ", "q", "ɢ",
#                 "ʡ", "", "ʔ", ""],
#             [  # sibilant affricate
#                 "", "", "", "", "", "", "ts", "dz", "ts", "dz", "tʃ", "dʒ", "tʂ", "dʐ", "tɕ", "dʑ", "", "", "", "", "",
#                 "", "", ""],
#             [  # non-sibilant affricate
#                 "pɸ", "bβ", "p̪f", "b̪v", "", "", "t̪θ", "d̪ð", "tɹ̝̊", "dɹ̝", "t̠ɹ̠̊˔", "d̠ɹ̠˔", "", "", "cç", "ɟʝ", "kx", "ɡɣ",
#                 "qχ", "ɢʁ", "ʡʜ", "ʡʢ", "ʔh", ""],
#             [  # sibilant fricative
#                 "", "", "", "", "", "", "s", "z", "s", "z", "ʃ", "ʒ", "ʂ", "ʐ", "ɕ", "ʑ", "", "", "", "", "", "", "",
#                 ""],
#             [  # non-sibilant fricative
#                 "ɸ", "β", "f", "v", "θ̼", "ð̼", "θ", "ð", "θ̠", "ð̠", "ɹ̠̊˔", "ɹ̠˔", "ɻ̊˔", "ɻ˔", "ç", "ʝ", "x", "ɣ", "χ",
#                 "ʁ", "ħ", "ʕ", "h", "ɦ"],
#             [  # approximant
#                 "", "", "", "ʋ", "", "", "", "ɹ", "", "ɹ", "", "ɹ", "", "ɻ", "", "j", "", "ɰ", "", "", "", "", "", "ʔ̞"],
#             [  # tap/flap
#                 "", "ⱱ̟", "", "ⱱ", "", "ɾ̼", "ɾ̥", "ɾ", "ɾ̥", "ɾ", "ɾ̥", "ɾ", "ɽ̊", "ɽ", "", "", "", "", "", "ɢ̆", "", "ʡ̆",
#                 "", ""],
#             [  # trill
#                 "ʙ̥", "ʙ", "", "", "", "", "r̥", "r", "r̥", "r", "r̥", "r", "", "", "", "", "", "", "ʀ̥", "ʀ", "ʜ", "ʢ",
#                 "", ""],
#             [  # lateral affricate
#                 "", "", "", "", "", "", "tɬ", "dɮ", "tɬ", "dɮ", "tɬ", "dɮ", "tꞎ", "d𝼅", "c𝼆", "ɟʎ̝", "k𝼄", "ɡʟ̝", "", "",
#                 "", "", "", ""],
#             [  # lateral fricative
#                 "", "", "", "", "", "", "ɬ", "ɮ", "ɬ", "ɮ", "ɬ", "ɮ", "ꞎ", "𝼅", "𝼆", "ʎ̝", "𝼄", "ʟ̝", "", "", "", "", "",
#                 ""],
#             [  # lateral approximant
#                 "", "", "", "", "", "", "", "l", "", "l", "", "l", "", "ɭ", "", "ʎ", "", "ʟ", "", "ʟ̠", "", "", "", ""],
#             [  # lateral tap/flap
#                 "", "", "", "", "", "", "ɺ̥", "ɺ", "ɺ̥", "ɺ", "ɺ̥", "ɺ", "𝼈̥", "𝼈", "", "ʎ̆", "", "ʟ̆", "", "", "", "", "",
#                 ""],
#         ]

# self.layer_correction = {
#             0: 0,
#             1: 18,
#             2: 28,
#             3: 29,
#             4: 34,
#             5: 35,
#             6: 39,
#             7: 40,
#             8: 41,
#             9: 47,
#             10: 53,
#             11: 60,
#             12: 69,
#         }
