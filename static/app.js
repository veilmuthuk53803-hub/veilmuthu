const taskElement =
    document.getElementById("task");

const inputElement =
    document.getElementById("inputText");

const submitButton =
    document.getElementById("submitButton");

const clearButton =
    document.getElementById("clearButton");

const resultSection =
    document.getElementById("resultSection");

const resultElement =
    document.getElementById("result");

const statusElement =
    document.getElementById("status");


const endpoints = {
    qa: "/qa",
    explain: "/explain",
    quiz: "/quiz",
    summarize: "/summarize",
    learn: "/learn/recommendations"
};


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function showResult() {

    resultSection.classList.remove("hidden");
}


function setLoading(isLoading) {

    submitButton.disabled = isLoading;

    if (isLoading) {

        submitButton.textContent =
            "Generating...";

        statusElement.textContent =
            "Working";

    } else {

        submitButton.textContent =
            "Generate";

        statusElement.textContent =
            "Ready";
    }
}


function renderText(text) {

    resultElement.innerHTML = `
        <div class="result-text">
            ${escapeHtml(text)}
        </div>
    `;
}


function renderQuiz(data) {

    let html = "";

    data.questions.forEach(
        (question, index) => {

            html += `
                <div class="quiz-question">

                    <h3>
                        ${index + 1}. 
                        ${escapeHtml(question.question)}
                    </h3>
            `;


            question.options.forEach(
                option => {

                    const isCorrect =
                        option === question.correct_answer;

                    html += `
                        <div class="quiz-option ${
                            isCorrect
                                ? "correct-answer"
                                : ""
                        }">
                            ${escapeHtml(option)}
                        </div>
                    `;
                }
            );


            html += `
                    <div class="answer-box">

                        <strong>
                            Correct answer:
                        </strong>

                        ${escapeHtml(
                            question.correct_answer
                        )}

                        <br><br>

                        <strong>
                            Explanation:
                        </strong>

                        ${escapeHtml(
                            question.explanation
                        )}

                    </div>

                </div>
            `;
        }
    );


    resultElement.innerHTML = html;
}


function renderLearningPath(data) {

    let html = `

        <div class="learning-overview">

            <h3>
                ${escapeHtml(data.topic)}
            </h3>

            <p>
                ${escapeHtml(data.overview)}
            </p>

            <strong>
                Estimated timeline:
            </strong>

            ${escapeHtml(
                data.estimated_timeline
            )}

        </div>
    `;


    data.steps.forEach(
        (step, index) => {

            html += `

                <div class="learning-step">

                    <h3>
                        Step ${index + 1}:
                        ${escapeHtml(step.topic)}
                    </h3>

                    <p>
                        <strong>Level:</strong>
                        ${escapeHtml(step.level)}
                    </p>

                    <p>
                        ${escapeHtml(
                            step.description
                        )}
                    </p>

                    <strong>
                        Suggested resources:
                    </strong>

                    <ul class="resources">
            `;


            step.suggested_resources.forEach(
                resource => {

                    html += `
                        <li>
                            ${escapeHtml(resource)}
                        </li>
                    `;
                }
            );


            html += `
                    </ul>

                </div>
            `;
        }
    );


    resultElement.innerHTML = html;
}


async function submitTask() {

    const task =
        taskElement.value;

    const text =
        inputElement.value.trim();


    if (!text) {

        showResult();

        resultElement.innerHTML = `
            <div class="error">
                Please enter a question or some content.
            </div>
        `;

        return;
    }


    const endpoint =
        endpoints[task];


    setLoading(true);

    showResult();


    resultElement.innerHTML = `
        <div class="loading">
            EduGenie is thinking...
        </div>
    `;


    try {

        const response =
            await fetch(endpoint, {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            });


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Something went wrong."
            );
        }


        if (task === "qa") {

            renderText(data.answer);

        } else if (task === "explain") {

            renderText(data.explanation);

        } else if (task === "summarize") {

            renderText(data.summary);

        } else if (task === "quiz") {

            renderQuiz(data);

        } else if (task === "learn") {

            renderLearningPath(data);
        }


        statusElement.textContent =
            "Completed";

    } catch (error) {

        resultElement.innerHTML = `
            <div class="error">
                <strong>Error:</strong>
                ${escapeHtml(error.message)}
            </div>
        `;

        statusElement.textContent =
            "Error";

    } finally {

        setLoading(false);
    }
}


submitButton.addEventListener(
    "click",
    submitTask
);


clearButton.addEventListener(
    "click",
    () => {

        inputElement.value = "";

        resultElement.innerHTML = "";

        resultSection.classList.add(
            "hidden"
        );

        statusElement.textContent =
            "Ready";
    }
);
