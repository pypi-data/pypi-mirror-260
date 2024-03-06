import re

# GPT-4	8K	$0.03/1000Tokens Prompt	$0.06/1000 Tokens Completion
# Prompt would be what you send to the chat completion model, and completion would be the output that is sent back.
# So think of it as �Prompt=input/question� �Completion=output/answer�
RATE_PROMPT = 0.03 # Per 1000 Token
RATE_COMPLETION = 0.06 # Per 1000 Token

def calculate_price(token_in_prompt, token_in_completion):
    result = ((token_in_prompt * RATE_PROMPT) + (token_in_completion * RATE_COMPLETION)) / 1000
    print("Charges: $ " +str(round(result, 3)))
    return round(result, 3)

def count_test(testcase, framework):
    count = 0
    if framework.lower() =="junit":
        count = len(re.findall("@Test", testcase))
    elif framework.lower() == "nunit":
        count = testcase.count("[Test]")
    elif framework.lower() == "mstest":
        count = len(re.findall("TestMethod", testcase))
    print("No. of Test Cases Generated :"+str(count))
    return count

if __name__=="__main__":
    metrics = f"Hello," \
                      f"Who," \
                      f"@Test," \
                      f"[Test]," \
                      f"@Test," \
                      f"TestMethod," \
                      f"[Test]," \
                      f"[Test]," \
                      f"[Test]," \
                      f"@Test"
    count_test(metrics,"nunit")