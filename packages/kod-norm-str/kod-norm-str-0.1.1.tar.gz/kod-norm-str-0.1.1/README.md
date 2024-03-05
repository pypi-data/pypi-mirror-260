
# k.o.d. String Normalization
(a better way to normalize strings into unique identifiers)

![k.o.d. String Normalization](assets/simple.webp)

## Overview

I created this tool to address the challenge of linking information together. 
Although strings may appear identical to the human eye, differences in encoding formats, 
such as UTF-8, mean they are technically distinct. This tool offers a solution by identifying 
the unique values within a string and marking them accordingly. As a result, if strings are visually identical, 
they are also identical in their normalization.
<br />

This utility provides a comprehensive approach to processing strings, particularly focusing on the decomposition of accents,
Hangul syllables, and normalization of strings (including accent removal and special character handling), and appending 
a unique hash to the normalized string.
<br />

It leverages Python's standard libraries such as `re` for regular expression operations, `hashlib` for generating hashes, and `unicodedata` for Unicode character processing.

### Key Features

1. **Accents and Special Characters Removal**: Removes accents and special characters from strings, making it easier to perform case-insensitive comparisons or searches.
2. **Hangul Syllable Decomposition**: Decomposes Korean Hangul syllables into their constituent components. This is crucial for linguistic analysis, search indexing, and educational applications where understanding the base components of syllables is necessary.
3. **String Normalization**: Removes accents and special characters from strings, making it easier to perform case-insensitive comparisons or searches. This process is vital for applications involving user input where consistency and predictability of the input data are essential.
4. **Unique Hash Generation**: Appends a unique hash to the normalized string, facilitating the identification of strings and ensuring that even if two inputs are normalized to the same value, they can still be distinguished by their hash.

### Benefits

- **Improved Search Efficiency**: By normalizing strings, including the decomposition of Hangul syllables, search algorithms can more easily match equivalent strings regardless of their original form, improving the user experience in search functionalities.

- **Data Consistency**: Normalization ensures that data is stored in a consistent format, reducing the complexity of data processing and manipulation down the line. This is particularly important in multi-lingual applications where text input might vary widely.

- **Enhanced Security**: The addition of a unique hash to normalized strings can help mitigate certain types of security risks by making it harder to predict the outcome of the normalization process and by providing a method to verify the integrity of the data.

- **Accessibility and Inclusivity**: By handling special characters and decomposing syllables, the utility makes content more accessible to diverse user groups, including those using screen readers or other assistive technologies that may not handle original, unnormalized text effectively.

### Importance of Usage

Using this utility is crucial in scenarios where text data comes from varied sources and requires standardization for processing, storage, or comparison. Applications that benefit from this utility include:

- **Content Management Systems (CMS)**: Where user-generated content needs to be searchable and free of accidental homoglyphs or variants caused by accents and special characters.

- **Educational Software**: Especially for languages with complex syllabic structures like Korean, providing learners with decomposed syllables can aid in understanding and pronunciation.

- **Data Analytics**: When analyzing textual data, normalization ensures that variations in input do not skew the results, leading to more accurate and reliable insights.

- **Security Applications**: Generating a unique hash for strings can be used in various security protocols, including data integrity checks and ensuring non-repudiation.

## Implementation Details

This utility consists of one main function:

- `normalize(custom_str)`: Combines normalization and hash generation to produce a final, normalized string with an appended hash for uniqueness.


It also includes the following helper functions:

- `process_normalization(input_str)`: Helper function that normalizes the input string by removing accents, handling special characters, and making other modifications to ensure a consistent output format.

- `decompose_hangul(syllable)`: Helper function that takes a single Hangul syllable and returns its constituent components.


### Usage Example

```python
original_string = "my string 안녕하세요"
normalized_string = normalize(original_string)
print(normalized_string)
```

This code snippet will decompose the Hangul syllables, normalize the string by removing any special characters or accents, and append a unique hash to the result.

## Conclusion

The k.o.d. String Normalization utility is a powerful tool for standardizing and normalizing text data, 
particularly in multi-lingual applications. By removing accents, handling special characters, and decomposing 
Hangul syllables, it ensures that strings are consistently represented and can be compared or searched efficiently. 
The addition of a unique hash to the normalized string further enhances its utility by providing a method to 
distinguish between visually identical strings. This utility is a valuable addition to any application that 
deals with text data from diverse sources and requires a consistent and predictable format for processing, 
storage, or comparison.