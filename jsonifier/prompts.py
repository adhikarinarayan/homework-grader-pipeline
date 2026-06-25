def prompt_segregation(qp):
  prompt = (
    "You are a physics expert. You are given a Question Paper and a Text. Your task is to segregate the given Text into different answer numbers based on the Question Paper.\n"
    "If you are unsure about the answer number for a particular part of the text, reason based on the Question Paper to find the correct answer number.\n"
    "If you find any misnumbered answers in the provided Text based on the Question Paper, correct the answer number.\n"
    "If the text contains parts that do not have answer numbers, reason based on the Question Paper to assign the correct answer number to those parts.\n"
    "If the text for some subpart of a question is missing, it can be inside other subparts of questions (e.g., 2a contains the answer for 2b, 2c, etc.). Ensure that these parts are correctly identified and segregated.\n"
    "Do not create any subparts that are not in the Question Paper.\n"
    "Do not make any corrections to the text. Do not modify or remove the Text content; segregate it as it is.\n"
    "Return a JSON object mapping answer numbers to their corresponding answers.\n"
    f"#Question Paper:\n{qp}\n\n#Text: "
)
  return prompt


def prompt_schema(schema):
    prompt=(
f"Please fill the given Text in the following JSON Schema. \nStrict Rules:"
f"1.Schema Compliance: The output must adhere exactly to the provided schema. Do not add or modify any fields beyond what is specified."
f"2.Do not add/remove anything to 'Text' content. Ensure the full text, including any JSON content within the 'Text' section, is mapped correctly to the corresponding Questions in the JSON Schema reply."
f"""3.Subparts should always be within a "subparts" array, even if there's only one."""
f"4.Do not create subparts that are not explicitly mentioned in the input text.\n"
f"#JSON Schema: {schema}\n\n# Text:\n")

    
    return prompt