import re
import hashlib
import unicodedata

# Let's do some Decomposition of Hangul syllables into Jamo characters
def decompose_hangul(syllable):
    # Hangul syllable decomposition
    SBase = 0xAC00
    LBase = 0x1100
    VBase = 0x1161
    TBase = 0x11A7
    NCount = 588
    TCount = 28

    # Decompose the syllable
    syllable_code = ord(syllable) - SBase
    L = LBase + syllable_code // NCount
    V = VBase + (syllable_code % NCount) // TCount
    T = TBase + syllable_code % TCount

    return [L, V, T if T != TBase else 0]


# Todo: We need to refactor this function to make it more readable and maintainable
def process_normalization(input_str):
    """Remove accents from a string and count removed accents and special characters."""
    # Initialize a counter for accents and modifications.
    modifications_count = 0
    # Initialize an empty string to hold the modified input string without accents.
    modified_str = ""
    # TODO: Move these to a seperate file and give detail on why they are needed
    special_char = {"`", " ́", "¨", "^", "˜", "¯", "˘", "ˇ", "ˆ", "˙", "˚",
                    "¸", "˛", "˝", "˛", "˝", "˛", "˝", "˛", "˝", "˛", "˝", "˛", "˝", "˛", "˝", "˛", "˝", "˛", "˝"}
    translate_sym_ord = {769: ' ́', 768: '`', 776: '¨', 770: '^', 771: '˜', 772: '¯', 728: '˘', 711: 'ˇ', 710: 'ˆ',
                         729: '˙', 184: '¸', 733: '˝', 697: '˛', 807: '˛', 697: '˝', 697: '˛', 697: '˝', 697: '˛'}
    translate_letters = {101: 'e', 97: 'a', 105: 'i', 111: 'o', 117: 'u', 99: 'c', 110: 'n', 65: 'A', 69: 'E', 73: 'I',
                         79: 'O', 85: 'U', 67: 'C', 78: 'N'}
    roman_numerals_map = {'Ⅰ': 1, 'Ⅱ': 2, 'Ⅲ': 3, 'Ⅳ': 4, 'Ⅴ': 5, 'Ⅵ': 6, 'Ⅶ': 7, 'Ⅷ': 8, 'Ⅸ': 9, 'Ⅹ': 10,
                          'Ⅺ': 11, 'Ⅻ': 12, 'Ⅼ': 50, 'Ⅽ': 100, 'Ⅾ': 500, 'Ⅿ': 1000}
    latin_chars_translate = {225: 'a', 224: 'a', 226: 'a', 227: 'a', 228: 'a', 229: 'a', 233: 'e', 232: 'e', 234: 'e',
                                235: 'e', 237: 'i', 236: 'i', 238: 'i', 239: 'i', 243: 'o', 242: 'o', 244: 'o', 245: 'o',
                                246: 'o', 250: 'u', 249: 'u', 251: 'u', 252: 'u', 231: 'c', 241: 'n', 193: 'A', 201: 'E',
                                205: 'I', 211: 'O', 214: 'O', 218: 'U', 199: 'C', 209: 'N'}

    # we need to check for modifications that may need to be made to the string
    sterialized_str = input_str
    char_position = 0
    string_len_record = 0 # this will replace our string length as it will be modified
    char_mod_mean = 0 # char mod mean is the position of the char being modified
    char_ascii_mean = 0
    pre_pos_mod = 0 # here we track how many positions we removed from he string
    special_char_mean = 0
    special_position = 0   # this will be used to track the position of the special char
    for char in sterialized_str:
        # print(f"Char: {char} + {ord(char)}")
        if char in roman_numerals_map:
            modifications_count += 1
            # print(f"Found roman numeral: {char}")
            char = str(roman_numerals_map[char])
            # print(f"Converted to: {char}")
        decomposed_char = unicodedata.normalize('NFKD', char)
        if len(decomposed_char) > 1:
            # mod need
            # print(f"Decomposed char: {decomposed_char} {len(decomposed_char) > 1} {ord(char)}")
            # print(f"{len(decomposed_char[0])}")
            modified_str += decomposed_char[0]  # Keep the base character.
            string_len_record += 1
            modifications_count += len(decomposed_char) - 1  # Count each additional character as a modification.
            char_mod_mean += (char_position - pre_pos_mod)
            # print(f"Char Mod Mean: {char_mod_mean}, Char Position: {char_position}")
            if len(char) == 1:
                # print(f"Char: {char} + {ord(char)}")
                if(ord(char) in latin_chars_translate):
                    # print(f"Added latin char: {latin_chars_translate[ord(char)]} + {ord(latin_chars_translate[ord(char)])}")
                    char_ascii_mean += 1
                    char = latin_chars_translate[ord(char)]
                elif (ord(char)  > 40004 and ord(char) < 58005):
                    check_dec = decompose_hangul(char)
                    # print(f"Decomposed char: {check_dec}")
                    for dec in check_dec:
                        if dec != 0:
                            # print(f"Char: {chr(dec)} + {dec}")
                            # if the last char is decomposed_char[0] then we remove it from modified_str
                            if decomposed_char[0] == modified_str[-1]:
                                modified_str = modified_str[:-1]
                                string_len_record -= 2
                                modifications_count += 1
                                char_ascii_mean -= ord(decomposed_char[0])

                            #     print(f"Removed last char: {decomposed_char[0]} + {ord(decomposed_char[0])}")
                            # modified_str += chr(dec)
                            special_char_mean += dec
                            special_position += 1

                            string_len_record += 1
                            # char = high_unicode_translate[dec]
                    # print(f"Added high unicode char: {high_unicode_translate[ord(char)]} + {ord(high_unicode_translate[ord(char)])}")
                    char_ascii_mean += 1
                    # char = high_unicode_translate[ord(char)]
                    string_len_record += 1
                char_ascii_mean += ord(char)
            elif len(char) > 1:
                # print(f"Char: {char} + {ord(char)} .. has more than 1 char")
                # go through each character in the decomposed string and add their ascii values
                for c in char:
                    if(ord(c) in latin_chars_translate):
                        char_ascii_mean += 1
                        c = latin_chars_translate[ord(c)]
                    char_ascii_mean += ord(c)
        else:
            # If the character is not decomposed, append it as is.
            # if len(char) > 1:
            # print(f"Char: {char} + {ord(char)}")
            # here we detect if the char is a special char
            if char in special_char or ord(char) in translate_sym_ord:
                # print(f"Found special char: {char} + {ord(char)}")
                previous_char = ""
                if (sterialized_str[char_position - 1] == " "):
                    previous_char = sterialized_str[char_position - 2]
                    pre_pos_mod += 2
                else:
                    previous_char = sterialized_str[char_position - 1]
                    pre_pos_mod += 1

                # print(f"Previous char: {previous_char} + {ord(previous_char)}")

                # now we check if the char is a latin char
                if(ord(previous_char) in translate_letters):
                    # char_ascii_mean += 1
                    string_len_record -= 1
                    char_mod_mean += (char_position-pre_pos_mod)
                    # print(f"Char Mod Mea*: {char_mod_mean}, Char Positio*: {char_position-pre_pos_mod}")
                    char_ascii_mean += ord(previous_char)
                    char_ascii_mean += 1
                string_len_record += 1
                modifications_count += 1
            elif (ord(char) > 4004 and ord(char) < 5005):
                # print(f"Found high unicode char: {char} + {ord(char)}")
                string_len_record += 1
                modifications_count += 1
                # char_mod_mean += char_position
                char_ascii_mean += ord(char)
                # modified_str += char
                special_char_mean += ord(char)
            else:
                modified_str += char
                string_len_record += 1
        char_position += 1

    if modifications_count == 0:
        return modified_str
    print(f"Special Char Mean: {special_char_mean}")
    # Append the modifications count to the modified string.

    # used for debugging
    # return f"{modified_str}_mods_len_{string_len_record}_modCount_{modifications_count}_charModMean_{char_mod_mean}_charAsciiMean_{char_ascii_mean}"

    return f"{modified_str}_mods_{string_len_record}{modifications_count}{char_mod_mean}{char_ascii_mean}"


def normalize(custom_str):
    """Normalize the string for searching, including removing accents and appending a unique hash."""
    no_accents = process_normalization(custom_str)
    # next we apply some simple normalization to the string
    normalized = no_accents.lower()
    normalized = re.sub(r'\s+', '', normalized)
    normalized = re.sub(r'[^\w\s]', '', normalized)

    # Generate a short hash of the processed custom_str
    hash_suffix = hashlib.blake2b(process_normalization(custom_str).encode('utf-8'), digest_size=4).hexdigest()

    # Append the unique hash to the normalized string
    normalized_with_hash = f"{normalized}_{hash_suffix}"
    return normalized_with_hash

