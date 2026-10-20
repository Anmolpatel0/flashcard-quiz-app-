import streamlit as st

# Initialize session state for flashcards if not exists
if "flashcards" not in st.session_state:
  st.session_state.flashcards = [
      {
          "question": "What is the capital of France?",
          "answer": "Paris",
      },
      {
          "question": "What does HTML stand for?",
          "answer": "HyperText Markup Language",
      },
      {
          "question": "What is 5 * 8?",
          "answer": "40",
      },
  ]

if "current_index" not in st.session_state:
  st.session_state.current_index = 0

if "show_answer" not in st.session_state:
  st.session_state.show_answer = False

st.title("📚 Flashcard Quiz App")
st.write("Study, navigate, and customize your flashcards easily!")

# Sidebar for Management (Add, Edit, Delete)
st.sidebar.header("🛠️ Manage Flashcards")

# Add Card
with st.sidebar.expander("Add New Card"):
  new_q = st.text_input("Question", key="new_q")
  new_a = st.text_input("Answer", key="new_a")
  if st.button("Add Flashcard"):
    if new_q and new_a:
      st.session_state.flashcards.append({"question": new_q, "answer": new_a})
      st.success("Flashcard added!")
      st.rerun()
    else:
      st.warning("Please fill in both fields.")

# Edit / Delete Existing Cards
if st.session_state.flashcards:
  with st.sidebar.expander("Edit or Delete Card"):
    card_options = [
        f"{i+1}: {card['question']}"
        for i, card in enumerate(st.session_state.flashcards)
    ]
    selected_card_label = st.selectbox(
        "Select card to modify", card_options
    )
    selected_idx = card_options.index(selected_card_label)

    edit_q = st.text_input(
        "Edit Question",
        value=st.session_state.flashcards[selected_idx]["question"],
        key="edit_q",
    )
    edit_a = st.text_input(
        "Edit Answer",
        value=st.session_state.flashcards[selected_idx]["answer"],
        key="edit_a",
    )

    col_edit1, col_edit2 = st.columns(2)
    with col_edit1:
      if st.button("Update Card"):
        st.session_state.flashcards[selected_idx] = {
            "question": edit_q,
            "answer": edit_a,
        }
        st.success("Card updated!")
        st.rerun()
    with col_edit2:
      if st.button("Delete Card"):
        st.session_state.flashcards.pop(selected_idx)
        if (
            st.session_state.current_index
            >= len(st.session_state.flashcards)
            and len(st.session_state.flashcards) > 0
        ):
          st.session_state.current_index = (
              len(st.session_state.flashcards) - 1
          )
        st.success("Card deleted!")
        st.rerun()

# Main Quiz Section
if not st.session_state.flashcards:
  st.warning("No flashcards available! Add some using the sidebar.")
else:
  if st.session_state.current_index >= len(st.session_state.flashcards):
    st.session_state.current_index = 0

  total_cards = len(st.session_state.flashcards)
  current_card = st.session_state.flashcards[st.session_state.current_index]

  st.markdown(
      f"### Card {st.session_state.current_index + 1} of {total_cards}"
  )

  # Flashcard Display Box
  st.info(f"**Question:**\n\n### {current_card['question']}")

  if st.session_state.show_answer:
    st.success(f"**Answer:**\n\n### {current_card['answer']}")

  # Show/Hide Answer Button
  button_text = (
      "Hide Answer" if st.session_state.show_answer else "Show Answer"
  )
  if st.button(button_text):
    st.session_state.show_answer = not st.session_state.show_answer
    st.rerun()

  st.write("")  # spacing

  # Navigation Buttons
  col1, col2, col3 = st.columns(3)

  with col1:
    if st.button("⬅️ Previous"):
      if st.session_state.current_index > 0:
        st.session_state.current_index -= 1
      else:
        st.session_state.current_index = total_cards - 1
      st.session_state.show_answer = False
      st.rerun()

  with col2:
    if st.button("🔄 Reset Quiz"):
      st.session_state.current_index = 0
      st.session_state.show_answer = False
      st.rerun()

  with col3:
    if st.button("Next ➡️"):
      if st.session_state.current_index < total_cards - 1:
        st.session_state.current_index += 1
      else:
        st.session_state.current_index = 0
      st.session_state.show_answer = False
      st.rerun()
