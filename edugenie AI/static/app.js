const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const inputLabel = document.getElementById("inputLabel");
const submitBtn = document.getElementById("submitBtn");
const result = document.getElementById("result");
const copyBtn = document.getElementById("copyBtn");
const status = document.getElementById("status");

const levelRow = document.getElementById("level-row");
const level = document.getElementById("level");
const hours = document.getElementById("hours");


function updateUI() {

    if (task.value === "recommendations") {

        levelRow.classList.remove("hidden");

        inputLabel.textContent = "What do you want to learn?";

        inputText.placeholder =
            "Example: Python Programming";

    } else {

        levelRow.classList.add("hidden");

        if (task.value === "qa") {

            inputLabel.textContent = "Your Question";

            inputText.placeholder =
                "Example: What is machine learning?";

        } else if (task.value === "explain") {

            inputLabel.textContent = "Topic";

            inputText.placeholder =
                "Example: Explain photosynthesis";

        } else if (task.value === "quiz") {

            inputLabel.textContent = "Study Content";

            inputText.placeholder =
                "Paste your study material here...";

        } else if (task.value === "summarize") {

            inputLabel.textContent = "Text to Summarize";

            inputText.placeholder =
                "Paste your text here...";
        }
    }
}


task.addEventListener("change", updateUI);


async function generateResult() {

    const text = inputText.value.trim();

    if (!text) {
        alert("Please enter some text.");
        return;
    }

    submitBtn.disabled = true;
    copyBtn.disabled = true;

    status.textContent = "Generating...";

    result.classList.remove("empty");
    result.textContent = "EduGenie is thinking...";


    let endpoint = "";

    let body = {
        text: text
    };


    if (task.value === "qa") {

        endpoint = "/qa";

    } else if (task.value === "explain") {

        endpoint = "/explain";

    } else if (task.value === "quiz") {

        endpoint = "/quiz";

    } else if (task.value === "summarize") {

        endpoint = "/summarize";

    } else if (task.value === "recommendations") {

        endpoint = "/learn/recommendations";

        body.level = level.value;

        body.hours_per_week =
            Number(hours.value);
    }


    try {

        const response = await fetch(
            endpoint,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(body)
            }
        );


        // Read response as text first
        const rawResponse =
            await response.text();


        // Try to convert response to JSON
        let data;

        try {

            data = JSON.parse(rawResponse);

        } catch (jsonError) {

            throw new Error(
                "Backend Error (" +
                response.status +
                "): " +
                rawResponse
            );
        }


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Something went wrong."
            );
        }


        if (task.value === "qa") {

            result.textContent =
                data.answer;

        } else if (task.value === "explain") {

            result.textContent =
                data.explanation;

        } else if (task.value === "quiz") {

            displayQuiz(data.quiz);

        } else if (task.value === "summarize") {

            result.textContent =
                data.summary;

        } else if (
            task.value === "recommendations"
        ) {

            result.textContent =
                data.recommendations;
        }


        status.textContent = "Ready";

        copyBtn.disabled = false;


    } catch (error) {

        result.textContent =
            error.message;

        status.textContent = "Error";

        console.error(error);

    } finally {

        submitBtn.disabled = false;
    }
}


function displayQuiz(quiz) {

    result.innerHTML = "";

    quiz.forEach(
        (item, index) => {

            const question =
                document.createElement("div");

            question.style.marginBottom =
                "25px";


            const title =
                document.createElement("h3");

            title.textContent =
                `${index + 1}. ${item.question}`;


            question.appendChild(title);


            item.options.forEach(
                option => {

                    const p =
                        document.createElement("p");

                    p.textContent =
                        "• " + option;

                    question.appendChild(p);
                }
            );


            const answer =
                document.createElement("p");

            answer.textContent =
                "Correct Answer: " +
                item.correct_answer;

            question.appendChild(answer);


            const explanation =
                document.createElement("p");

            explanation.textContent =
                "Explanation: " +
                item.explanation;

            question.appendChild(
                explanation
            );
        }
    );
}


copyBtn.addEventListener(
    "click",
    async () => {

        await navigator.clipboard.writeText(
            result.innerText
        );

        copyBtn.textContent =
            "Copied!";

        setTimeout(
            () => {

                copyBtn.textContent =
                    "Copy";

            },
            1500
        );
    }
);


submitBtn.addEventListener(
    "click",
    generateResult
);


updateUI();