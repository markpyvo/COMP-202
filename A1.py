# This program determines whether an online message comes from a human or a bot
# It asks the user about response time, word count, typos, and a final 'eeooeotetto' test

# 2. Write your program here:

# String constant for efficient printing
bot = "You just talked to a bot"
human = "You just talked to a fellow human"

print("Bot or Human? Let's figure this out!")

# Check if response was at unusual hour
response_hour = float(input("When did you receive your response (type a float between 0 and 24)? "))

if (2 <= response_hour <= 5):
    print(bot)

else: 
    # Check if response time was very short (less than 0.15min ≈ 9 seconds)
    response_time = float(input("How long did it take to get your response (in min)? "))

    if (response_time < 0.15):
        print(bot)

    else:
        # Calculate WPM from word count and response time
        word_count = float(input("How many words in your response? "))

        if ((word_count / response_time) < 66):
            print(human)
        else:
            # Checks for amount of typos in response (bots do not make typos)
            typos = int(input("How many typos in the response (grammatical errors, misspelled words, etc.)? "))

            if (typos >= 1):
                print(human)

            else:
                # Run the Wang et al. test: check if responder counts 't' correctly in "eeooeotetto"
                t_count = int(input(
                "Ask the responder how many 't' there are in 'eeooeotetto' and type their answer? "))
                
                if (t_count == 3):
                    print(human)
                else:
                    print(bot)