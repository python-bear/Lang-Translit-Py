import questionary as que
from itertools import product
import json
import sys

from ipa_charts import *
from verbosity import *


def clean_ipa(ipa_text: str, replace_rs: bool = True) -> str:
    ipa = ipa_text.strip()

    if replace_rs:
        ipa = ipa.replace("ɹ", "ɾ").replace("ɹ̠", "ɾ").replace("ɻ", "ɽ")

    if ipa[0] in ipa_chart.containers:
        ipa = ipa[1:]

    if ipa[-1] in ipa_chart.containers:
        ipa = ipa[:-1]

    s.speak(f"stripped down ipa: {ipa_text}\t->\t{ipa}", "info")

    final_ipa = ipa
    for key, value in cleaning_dict.items():
        final_ipa = final_ipa.replace(key, value)

    s.speak(f"cleaned out the clutter: {ipa}\t->\t{final_ipa}", "info")

    return final_ipa


def process_ipa(ipa: str, db) -> list:
    s.speak(f"PROCESSING IPA TEXT: {ipa}", "title")

    replace_r = que.select(
        f"Do you want to replace all 'ɹ's with 'ɾ's and 'ɻ's with 'ɽ's? (will yield more accurate results for most "
        f"languages)",
        choices=["Yes", "No"],
    ).ask()

    ipa = clean_ipa(ipa, True if replace_r == "Yes" else False)

    s.speak(f"language database calibrated: {db}", "info")

    key_lens = max([len(key) for key in db])
    key_lens = [key_lens - i for i in range(key_lens)]
    s.speak(f"all key lengths have been found: {key_lens}", "info")
    coord_ipa = ipa_chart.ipa_to_coords(ipa, key_lens[0])

    s.speak(f"converted into IPA phonemes: {coord_ipa}", "info")

    i = 0
    translit = []
    while i < len(coord_ipa[0]):
        if is_punctuation_or_whitespace(coord_ipa[0][i]):
            if coord_ipa[0][i] in db.keys():
                match = db[coord_ipa[0][i]]
            else:
                match = coord_ipa[0][i]

            if math is None:
                match = coord_ipa[0][i]

            s.speak(f"for i = {i}, viewport = {coord_ipa[0][i]}| resorting match for {fr.BLUE}{coord_ipa[0][i]}"
                    f"{fr.WHITE}: {fr.BLUE}{match}{fr.WHITE}")
            translit.append([match])
            i += 1
            continue

        not_found = True

        for l in key_lens:
            if coord_ipa[0][i][0] == "ˈ":
                yon = 1
                deyon = 1
            else:
                yon = 0
                deyon = 0

            try:
                s.speak(f"for i = {i}, viewport = {fr.BLUE}{''.join(coord_ipa[0][i:i + yon + l])}{fr.WHITE}|\tchecking "
                        f"if yon is applicable:\t{fr.BLUE}{''.join(coord_ipa[0][i:i + yon + l])}{fr.WHITE}{bk.BLUE}"
                        f"{''.join(coord_ipa[0][i + yon + l:i + yon + 1 + l])}", end="")
                if "".join(coord_ipa[0][i + 1 + yon]) in ipa_chart.extras and "".join(coord_ipa[0][i + 1 + yon]) != "ˈ":
                    yon += 1
                    s.speak(f"\t... it is")
                else:
                    s.speak(f"\t... it isn't")
            except IndexError:
                s.speak(f"\t... it isn't")

            viewport = "".join(coord_ipa[0][i:i + l + yon - deyon])
            if viewport[-1] == "ˈ":
                evade = 1
            else:
                evade = 0
            viewport = "".join(coord_ipa[0][i:i + l + yon - evade - deyon])

            for key in db.keys():
                if len(key) == l + deyon and not_found:
                    try:
                        s.speak(f"for i = {i}, viewport = {fr.BLUE}{viewport}{fr.WHITE}|\tl = {l}\tyon = {yon}\tkey = "
                                f"{key}")
                    except IndexError:
                        continue

                    if key == viewport:
                        s.speak(f"for i = {i}, viewport = {fr.BLUE}{viewport}{fr.WHITE}|\tfound possible match for "
                                f"{viewport}: ", end="")

                        phoneme = [db[key]] if not isinstance(db[key], list) else db[key]
                        translit.append(phoneme)
                        s.speak(f"\t... successful ({coord_ipa[0][i:i + l + yon - deyon]} -> {phoneme})")
                        i += l + yon - deyon
                        not_found = False

                        # if type(db[key]) == str:
                        #     chars = db[key]
                        #     translit, not_found, next_i = check_form(ipa, chars, translit, l, yon, i)
                        #
                        #     if not not_found:
                        #         s.speak(f"\t... successful ({ipa[i:i + l + yon]} -> {translit.split('|')[-1]})")
                        #     else:
                        #         s.speak(f"\t... unsuccessful")
                        # else:
                        #     s.speak(f", rotating :")
                        #     for form in range(len(db[key])):
                        #         s.speak(f"for i = {i}, {ipa[i]}|\trotation: {form})", end="")
                        #         chars = db[key][form]
                        #         translit, not_found, next_i = check_form(ipa, chars, translit, l, yon, i)
                        #
                        #         if not not_found:
                        #             s.speak(f"\t... successful ({ipa[i:i + l + yon]} -> {translit.split('|')[-1]})")
                        #             break
                        #         else:
                        #             s.speak(f"\t... unsuccessful")
                        # i = next_i

        if not_found:
            viewport = "".join(coord_ipa[0][i:i + yon + 1 - deyon])
            s.speak(f"for i = {i}, viewport = {fr.BLUE}{viewport}{fr.WHITE}|\tno perfect match was found for "
                    f"{viewport}")
            closest_seq = ""
            last_distance = float("inf")
            for l in key_lens.__reversed__():
                if coord_ipa[0][i][0] == "ˈ":
                    yon = 1
                    deyon = 1
                else:
                    yon = 0
                    deyon = 0

                try:
                    s.speak(
                        f"for i = {i}, viewport = {fr.BLUE}{''.join(coord_ipa[0][i:i + yon + l])}{fr.WHITE}|\tchecking "
                        f"if yon is applicable:\t{fr.BLUE}{''.join(coord_ipa[0][i:i + yon + l])}{fr.WHITE}{bk.BLUE}"
                        f"{''.join(coord_ipa[0][i + yon + l:i + yon + 1 + l])}", end="")
                    if "".join(coord_ipa[0][i + 1 + yon]) in ipa_chart.extras and "".join(
                            coord_ipa[0][i + 1 + yon]) != "ˈ":
                        yon += 1
                        s.speak(f"\t... it is")
                    else:
                        s.speak(f"\t... it isn't")
                except IndexError:
                    s.speak(f"\t... it isn't")

                viewport = "".join(coord_ipa[0][i:i + l + yon - deyon])
                if viewport[-1] == "ˈ":
                    evade = 1
                else:
                    evade = 0
                viewport = "".join(coord_ipa[0][i:i + l + yon - evade - deyon])

                s.speak(f"for i = {i}, viewport = {fr.BLUE}{viewport}{fr.WHITE}|\t", end="")
                seq, distance = ipa_chart.get_closest_in_pool(viewport, [k for k in db.keys()], True)

                if seq is None or distance is None:
                    continue

                s.speak(f"for i = {i}, viewport = {fr.BLUE}{viewport}{fr.WHITE}|\tfound closest match for "
                        f"{viewport}: {seq}, distance = {distance}, last distance = {last_distance}")

                if distance < last_distance:
                    last_distance = distance
                    closest_seq = seq

            if closest_seq != "":
                if coord_ipa[0][i][0] == "ˈ":
                    yon = 1
                    deyon = 1
                else:
                    yon = 0
                    deyon = 0

                l = len(ipa_chart.strip_extras(closest_seq))

                try:
                    s.speak(
                        f"for i = {i}, yon = {yon}, deyon = {deyon}, l = {l}, viewport = {fr.BLUE}"
                        f"{''.join(coord_ipa[0][i:i + yon + l])}{fr.WHITE}|\tchecking "
                        f"if yon is applicable:\t{fr.BLUE}{''.join(coord_ipa[0][i:i + yon + l])}{fr.WHITE}{bk.BLUE}"
                        f"{''.join(coord_ipa[0][i + yon + l:i + yon + 1 + l])}", end="")
                    if "".join(coord_ipa[0][i + 1 + yon]) in ipa_chart.extras and \
                            "".join(coord_ipa[0][i + 1 + yon]) != "ˈ":
                        yon += 1
                        s.speak(f"\t... it is")
                    else:
                        s.speak(f"\t... it isn't")
                except IndexError:
                    s.speak(f"\t... it isn't")

                viewport = "".join(coord_ipa[0][i:i + l + yon - deyon])
                if viewport[-1] == "ˈ":
                    evade = 1
                else:
                    evade = 0
                viewport = "".join(coord_ipa[0][i:i + l + yon - evade - deyon])

                s.speak(f"for i = {i}, viewport = {fr.BLUE}{viewport}{fr.WHITE}|\tfound possible match for "
                        f"{viewport}: ", end="")
                translit.append([db["".join(seq for seq in closest_seq)]] if not
                                isinstance(db["".join(seq for seq in closest_seq)], list) else
                                db["".join(seq for seq in closest_seq)])
                s.speak(f"\t... successful ({viewport} -> {translit[-1]})")
                i += yon + l - deyon

                # s.speak(f"for i = {i}, viewport = {fr.BLUE}{viewport}{fr.WHITE}|\tfound possible match for "
                #         f"{viewport}: ", end="")
                # if type(db[closest_seq]) == str:
                #     chars = db[closest_seq]
                #     translit, not_found, next_i = check_form(ipa, chars, translit, 1, yon, i, True)
                #
                #     if not not_found:
                #         s.speak(f"\t... successful ({viewport} -> {translit.split('|')[-1]})")
                #     else:
                #         s.speak(f"\t... unsuccessful")
                #         sys.exit()
                # else:
                #     s.speak(f", rotating :")
                #     for form in range(len(db[closest_seq])):
                #         s.speak(f"for i = {i}, viewport = {fr.BLUE}{viewport}{fr.WHITE}|\trotation: {form})", end="")
                #         chars = db[closest_seq][form]
                #         translit, not_found, next_i = check_form(ipa, chars, translit, 1, yon, i, True)
                #
                #         if not not_found:
                #             s.speak(f"\t... successful ({viewport} -> {translit.split('|')[-1]})")
                #             break
                #         else:
                #             s.speak(f"\t... unsuccessful")
                #             sys.exit()
                # i = next_i
    full_translit = [[db.get("<", "")], *[db.get(" ", " ") if phoneme == " " else phoneme for phoneme in translit],
                     [db.get(">", "")]]

    return best_form(full_translit, db), full_translit


def best_form(translit: list, db) -> str:
    final_translit = ["" for _ in range(len(translit))]

    for i, chars in enumerate(translit):
        if len(translit[i]) == 1:
            final_translit[i] = clean_phoneme(chars[0])

    for i, chars in enumerate(translit):
        if len(translit[i]) != 1:
            found = False
            for j in range(len(translit[i])):
                test_translit = [phoneme if y != i else chars[j] for y, phoneme in enumerate(final_translit)]
                if verify_form(test_translit, db, i) is not None and not found:
                    final_translit[i] = clean_phoneme(chars[j])
                    found = True
            if not found:
                final_translit[i] = chars[0]
    return "".join(phoneme for phoneme in final_translit)


def clean_phoneme(phoneme: str) -> str:
    phoneme = phoneme.split("|")[0].split("$")[0].split("%")[0].split("&")[0].split("*")[0].split("#")[0].split("!")[0]
    phoneme = phoneme.split("@")[0].split("}")[0].split(">")[0].split("{")[0].split("<")[0]
    return phoneme


def verify_form(ipa: tuple|list, db, index: int, weakness: int = 0):
    try:
        for i, phoneme in enumerate(ipa):
            if "|" in phoneme:
                phoneme = phoneme.split("|")
                try:
                    if (ipa[i + 1].isspace() or ipa[i - 1].isspace()) or weakness:
                        i += 1
                        phoneme = phoneme[-1]
                        continue
                    else:
                        return False
                except IndexError:
                    i += 1
                    phoneme = phoneme[-1]
                    continue

            elif "$" in phoneme:
                phoneme = phoneme.split("$")
                try:
                    if (is_punctuation_or_whitespace(ipa[i + 1]) or i == len(ipa)) or weakness:
                        i += 1
                        phoneme = phoneme[-1]
                        continue
                    else:
                        return False
                except IndexError:
                    i += 1
                    phoneme = phoneme[-1]
                    continue

            elif "%" in phoneme:
                phoneme = phoneme.split("%")
                targets = phoneme[-1].split("/")
                try:
                    if not (get_key_from_value(db, ipa[i - 1]) in targets) or weakness:
                        i += 1
                        phoneme = phoneme[0]
                        continue
                    else:
                        return False
                except IndexError:
                    i += 1
                    phoneme = phoneme[0]
                    continue

            elif "&" in phoneme:
                phoneme = phoneme.split("&")
                targets = phoneme[-1].split("/")
                try:
                    if (get_key_from_value(db, ipa[i - 1]) in targets) or weakness:
                        i += 1
                        phoneme = phoneme[0]
                        continue
                    else:
                        return False
                except IndexError:
                    return False

            elif "*" in phoneme:
                phoneme = phoneme.split("*")
                targets = phoneme[-1].split("/")
                try:
                    if not (ipa[i + 1] in targets) or weakness:
                        i += 1
                        phoneme = phoneme[0]
                        continue
                    else:
                        return False
                except IndexError:
                    i += 1
                    phoneme = phoneme[0]
                    continue

            elif "#" in phoneme:
                phoneme = phoneme.split("#")
                targets = phoneme[-1].split("/")
                try:
                    if (ipa[i + 1] in targets) or weakness:
                        i += 1
                        phoneme = phoneme[0]
                        continue
                    else:
                        return False
                except IndexError:
                    return False

            elif "!" in phoneme:
                phoneme = phoneme.split("!")
                targets = phoneme[-1].split("/")
                try:
                    if not (ipa[i - 1] in targets) or weakness:
                        i += 1
                        phoneme = phoneme[0]
                        continue
                    else:
                        return False
                except IndexError:
                    i += 1
                    phoneme = phoneme[0]
                    continue

            elif "@" in phoneme:
                phoneme = phoneme.split("@")
                targets = phoneme[-1].split("/")
                try:
                    if (ipa[i - 1] in targets) or weakness:
                        i += 1
                        phoneme = phoneme[0]
                        continue
                    else:
                        return False
                except IndexError:
                    return False

            elif "}" in phoneme:
                phoneme = phoneme.split("}")
                try:
                    if not (is_punctuation_or_whitespace(ipa[i + 1]) or i == len(ipa)) or weakness:
                        i += 1
                        phoneme = phoneme[0]
                        continue
                    else:
                        return False
                except IndexError:
                    i += 1
                    phoneme = phoneme[0]
                    continue

            elif ">" in phoneme:
                phoneme = phoneme.split(">")
                try:
                    if (is_punctuation_or_whitespace(ipa[i + 1]) or i == len(ipa)) or weakness:
                        i += 1
                        phoneme = phoneme[0]
                        continue
                    else:
                        return False
                except IndexError:
                    i += 1
                    phoneme = phoneme[0]
                    continue

            if "{" in phoneme:
                phoneme = phoneme.split("{")
                try:
                    if not (is_punctuation_or_whitespace(ipa[i - 1]) or i == 0) or weakness:
                        i += 1
                        phoneme = phoneme[0]
                        continue
                    else:
                        return False
                except IndexError:
                    i += 1
                    phoneme = phoneme[0]
                    continue

            elif "<" in phoneme:
                phoneme = phoneme.split("<")
                try:
                    if (is_punctuation_or_whitespace(ipa[i - 1]) or i == 0) or weakness:
                        i += 1
                        phoneme = phoneme[0]
                        continue
                    else:
                        return False
                except IndexError:
                    i += 1
                    phoneme = phoneme[0]
                    continue

            if i == index:
                return phoneme
        return phoneme
    except IndexError:
        return False


with open("ipa-to-lang.json", "r", encoding="utf-8") as f:
    lang_db = json.load(f)

while True:
    que.print("IPA to process:", style="bold fg:#ffff00")
    ipa_to_process = que.text(">").ask().lower()

    db_langs = sorted([l for l in lang_db])
    db_langs.remove("__comment")

    lang = que.select(
        f"What language do you want to use?",
        choices=db_langs,
    ).ask()

    db_scripts = sorted([s for s in lang_db[lang]])

    script = que.select(
        f"What script do you want to use?",
        choices=db_scripts,
    ).ask()

    db_addons = sorted([a for a in lang_db[lang][script]])
    if "main" in db_addons:
        db_addons.remove("main")

        if len(db_addons) == 0:
            que.print(f"! No addons are available")
            addon = []
        else:
            addon = que.checkbox(
                f"What addons do you want to use?",
                choices=db_addons,
            ).ask()

        addon.append("main")
    else:
        addon = []
        while not addon:
            addon = que.checkbox(
                f"What addons do you want to use?",
                choices=db_addons,
            ).ask()
            if not addon:
                que.print(f"! You must choose at least one addon for this script")

    combined_db = {}
    if "main" in addon:
        combined_db.update(lang_db[lang][script]["main"])
    for name in addon:
        if name != "main":
            combined_db.update(lang_db[lang][script][name])

    combined_db = {key: value for key, value in combined_db.items() if value != []}

    translit_txt, other_possibilities = process_ipa(ipa_to_process, combined_db)
    s.speak("IPA TO TRANSLITERATION PROCESS COMPLETE", "title")

    que.print(f"Processed IPA:\n! > {translit_txt}\n", style="bold fg:#33ee33")
    que.print(f"Other Possibilities:\n! > {other_possibilities}\n", style="bold fg:#33ee33")
