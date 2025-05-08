import random

import streamlit as st
from streamlit.components.v1 import html
from sumchef import (
    Equal,
    IsDivisibleBy,
    IsGreaterThan,
    IsLessThan,
    Lit,
    Multiply,
    expression_string,
    gen_bindings,
    variables,
)

st.set_page_config(page_title="Quiz time!", page_icon="⚽", layout="wide")


var_names = ["x", "y", "z"]
x, y, z = variables(var_names)

vars = {
    "x": x,
    "y": y,
    "z": z,
}

lhs = Multiply(x, y)
rhs = z

constraints = [
    IsGreaterThan(x, Lit(10)),
    IsDivisibleBy(x, Lit(10)),
    IsLessThan(y, Lit(10)),
    Equal(lhs, rhs),
]
domains = {var_name: list(range(1, 1000)) for var_name in var_names}
bindings = gen_bindings(var_names, domains, constraints)


def get_next_problem():
    return next(bindings)


def main():
    if "problem" not in st.session_state:
        st.session_state.problem = get_next_problem()
        st.session_state.hold_out = z.name
        st.session_state.correct_answer = False

    if st.session_state.correct_answer:
        display_text = (
            expression_string(
                lhs, st.session_state.problem, underline=vars[st.session_state.hold_out]
            )
            + " = "
            + expression_string(
                rhs, st.session_state.problem, underline=vars[st.session_state.hold_out]
            )
        )
    else:
        display_text = (
            expression_string(
                lhs, st.session_state.problem, hold_out=vars[st.session_state.hold_out]
            )
            + " = "
            + expression_string(
                rhs, st.session_state.problem, hold_out=vars[st.session_state.hold_out]
            )
        )

    st.markdown(
        f"<div style='font-size: 100px; text-align: center;'>{display_text}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<br/>" * 2, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])

    with col2:
        if not st.session_state.correct_answer:
            with st.form(key="guess_form"):
                user_guess = st.text_input(
                    "Enter your guess (press Enter to submit):", key="user_guess_input"
                )
                submit_button = st.form_submit_button(
                    "Submit", use_container_width=True
                )

                if (
                    submit_button or user_guess
                ):  # This will trigger on Enter key or button click
                    try:
                        user_guess = int(user_guess)
                        if user_guess == vars[st.session_state.hold_out].evaluate(
                            st.session_state.problem
                        ):
                            st.session_state.correct_answer = True
                            st.success(
                                "Well done! Press Enter to move to the next question."
                            )
                            st.rerun()
                        else:
                            st.error("Try again!")
                    except ValueError:
                        st.error("Invalid input. Try again!")
        else:
            with st.form(key="next_question_form"):
                c1, c2 = st.columns([1, 10])
                with c1:
                    user_guess = st.text_input("", key="user_guess_input")
                with c2:
                    if st.form_submit_button(
                        "Next Question (Press Enter)", use_container_width=True
                    ):
                        st.session_state.problem = get_next_problem()
                        st.session_state.hold_out = random.choice([x, y, z]).name
                        st.session_state.correct_answer = False
                        st.rerun()

    js_code = """
    <script>
    function focusInput() {
        const inputs = window.parent.document.querySelectorAll('input[type="text"]');
        console.log(inputs)
        if (inputs.length > 0) {
            inputs[0].focus();
        }
    }
    
    // Initial focus
    focusInput();
    
    // Focus after each Streamlit rerun
    window.parent.addEventListener('DOMContentLoaded', focusInput);
    </script>
    """
    html(js_code)


if __name__ == "__main__":
    main()
