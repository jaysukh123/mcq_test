console.log("Exam Center Loaded!");

// Example: Show an alert when clicking a navbar item
document.querySelectorAll(".navbar-item").forEach(item => {
    item.addEventListener("click", () => {
        alert("You clicked " + item.textContent);
    });
});

function toggleMenu() {
    const menu = document.querySelector(".navbar-right");
    menu.style.display = menu.style.display === "flex" ? "none" : "flex";
}

// Dark Mode Toggle
document.getElementById("darkModeToggle").addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
});
function fetchYears(category) {
    fetch(`/get-years/${category}/`)
        .then(response => response.json())
        .then(data => {
            let yearList = document.getElementById("yearList");
            yearList.innerHTML = "";

            data.years.forEach(year => {
                let button = `<button class="year-button" onclick="fetchPapers('${category}', ${year})">${year}</button>`;
                yearList.innerHTML += button;
            });
        })
        .catch(error => console.error("Error fetching years:", error));
}

function fetchPapers(category, year) {
    fetch(`/get-papers/${category}/${year}/`)
        .then(response => response.json())
        .then(data => {
            let paperList = document.getElementById("paperList");
            paperList.innerHTML = "";

            data.papers.forEach(paper => {
                let button = `<button class="paper-button" onclick="fetchMCQs('${category}', ${year}, '${paper}')">${paper}</button>`;
                paperList.innerHTML += button;
            });
        })
        .catch(error => console.error("Error fetching papers:", error));
}

function fetchMCQs(category, year, paper) {
    fetch(`/fetch-mcqs/${category}/${year}/${paper}/`)
        .then(response => response.json())
        .then(data => {
            let mcqList = document.getElementById("mcqList");
            mcqList.innerHTML = "";

            data.mcqs.forEach(mcq => {
                let questionHTML = `
                    <div class="mcq">
                        <p><b>${mcq.question}</b></p>
                        <ul>
                            <li>A) ${mcq.option_a}</li>
                            <li>B) ${mcq.option_b}</li>
                            <li>C) ${mcq.option_c}</li>
                            <li>D) ${mcq.option_d}</li>
                        </ul>
                    </div>`;
                mcqList.innerHTML += questionHTML;
            });
        })
        .catch(error => console.error("Error fetching MCQs:", error));
}
