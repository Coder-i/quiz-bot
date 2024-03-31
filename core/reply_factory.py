
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
  """
  Validates and stores the answer for the current question to the Django session.
  """

  # Implement your answer validation logic here (e.g., check for answer length, format, etc.)
  if len(answer) < 1:
    return False, "Please provide an answer."

  # Update session with answer for the current question
  session.message_history.append({
    "type": "user_answer",
    "question_id": current_question_id,
    "text": answer,
  })
  session.save()

  return True, ""

def get_next_question(current_question_id):
  """
  Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
  """

  question_index = PYTHON_QUESTION_LIST.index(current_question_id) + 1
  if question_index < len(PYTHON_QUESTION_LIST):
    return PYTHON_QUESTION_LIST[question_index]["question_text"], question_index
  else:
    return None, None

def generate_final_response(session):
  """
  Creates a final result message including a score based on the answers
  by the user for questions in the PYTHON_QUESTION_LIST.
  """

  score = calculate_score(session.message_history)  # Calculate score based on answers
  return "Your final score is: {}. Thanks for taking the quiz!".format(score)

def calculate_score(message_history):
  """
  This function calculates the score based on the user's answers in the message_history.
  Implement your scoring logic here (e.g., assign points for correct answers).
  """

  # Placeholder - Replace with your scoring logic
  score = 0
  for entry in message_history:
    if entry["type"] == "user_answer" and entry["text"] == get_answer_by_question_id(entry["question_id"]):
      score += 1

  return score

def get_answer_by_question_id(question_id):
  """
  This function retrieves the correct answer for a given question ID from PYTHON_QUESTION_LIST.
  """

  for question in PYTHON_QUESTION_LIST:
    if question["question_text"] == question_id:
      return question["answer"]
  return None