import re

def separate_choices(text):
  """
  This function separates the choices from a given text string and stores the introductory text.

  Args:
      text: The text string containing the choices.

  Returns:
      A tuple containing two elements:
      - introductory_text: The text before the choices.
      - choices: A list of strings, where each string represents a choice description.
  """
  choices = []
  introductory_text = ""
  # Regex pattern to match lines starting with "Choice n" (modify if needed)
  choice_pattern = r"(Choice \d+:\s?(.*?))(?=\n|$)"

  match = re.finditer(choice_pattern, text, re.DOTALL)  # Find all matches (use DOTALL for multiline)
  if match:
    for m in match:
      introductory_text = text[:m.start()]  # Capture text before the first choice
      choices.append(m.group(2).strip())  # Extract and strip choice description (group 2)

  return introductory_text, choices
