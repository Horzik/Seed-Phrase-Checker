# **Seed Phrase Checker**

A simple script to check if Bitcoin seed phrases are an actual Bitcoin
address, and if they have any transaction history.

## Execution and Description

Add the seed phrases to the **"seeds.txt"** file located in the **"/data"** directory.
I have provided some phrases as an example. The vast majority of them are not an actual address.

You can notice there are also Bitcoin addresses in the **"seeds.txt"**, that's 
because you can use this script to also check for activity of addresses directly.

To run the script simply call the **"checker.py"**. If you want to check addresses instead of seed phrases,
use the "-a" flag like this:

> checker.py -a

The script will now go through all the addresses in the **"seeds.txt"**. To exit mid-run use:

> ctrl + c

After the script finishes or gets interrupted, there is a short summary log:

>Checked 234 seed phrases <br>
>Found 5 valid and 0 active addresses <br>
>The search took 6.57 seconds <br>
>0 failed to be checked

The results are located and written in respective files inside the **"/data"** directory. <br>

Valid Addresses => **"addies.txt"** <br>
Addresses with a history => **"777adds.txt"** <br>
Addresss that have failed to be checked => **"fail.txt"**

You can change the names in the **"config.py"** file. <br>

There is also the **"START"** option in the config, which indicates on which line of the
**"seeds.txt"** should the checker start.

If the script finds any addresses written in the **"addies.txt"**, it will prompt the user if they want to
continue to search from the last address in the file, OR if the check should start from the **"START"** constant.

The script uses **"blockstream.info"** API, because it allows practically unlimited calls. <br>
You can change the API inside the **"checker.py"** file in the **"check_address_activity"** function, along 
with the maximum amount of **retries** (if the API times out for example), and the **delay**  between each retry.

The **"full_requirements"** includes all the current dependencies that
are installed along with the ones from **"requirements"**. I have included both for clarity.

## Afterword

This is one of the first real Python projects I have ever written, so there are likely some mistakes in
either design/structure/logic.

However I have found it to work well and reasonably fast (the speed depends mostly on the API).

I am more than open for any possible changes or additions, please let me know if you have any feedback.
