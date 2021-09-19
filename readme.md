# How this segmentation tool works
## Segmentation: 
### 1. Current char marks the end of a quote? 
If the preceding char is in [".","!","?"], mark the end of the current sentence. 
e.g. 
>Et l'on me recevait: "Mon père, par-ci ; mon cher père, par-là."
### 2. Current char marks the start of a quote? 
Separate current char from the immediately following char. 
### 3. Current char is a space char? 
Immediately ends the preceding word.
### 4. Non-alnum non-space char? 
Immediately ends the preceding word except for the following scenarios: 
- Char is the first char. 
- The preceding char is a space char. 
- The preceding char is clitic.
- Decimal separator.
### 5. Default (Alphanumeric char)? 
Add it to current word cache without ending the word.
### Postwork
Remove null tokens from parsed text. 
## Glossing:
- match a token to an existing entry in the library of mapper class, or use an empty string. Auto cap at start of sentences.



