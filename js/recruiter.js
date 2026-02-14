document.addEventListener("DOMContentLoaded", () => {

    const jobDescInput = document.getElementById("jobDesc");
    const rankBtn = document.getElementById("rankBtn");
    const sampleBtn = document.getElementById("sampleBtn");
    const resultsDiv = document.getElementById("results");
    const topKInput = document.getElementById("topK");

    // ================= SAMPLE BUTTON =================

    sampleBtn.addEventListener("click", () => {
        jobDescInput.value = `
Senior Backend Developer

We are looking for a developer experienced in:
- FastAPI
- MongoDB
- REST APIs
- Docker
- GitHub collaboration
- Strong Data Structures & Algorithms

Nice to have:
- Cloud deployment (AWS)
- Kubernetes
        `;
    });

    // ================= RANK BUTTON =================

    rankBtn.addEventListener("click", async () => {

        const jobDescription = jobDescInput.value.trim();
        const topK = parseInt(topKInput.value) || 10;

        if (!jobDescription) {
            alert("Please enter a job description.");
            return;
        }

        // Loading state
        rankBtn.disabled = true;
        rankBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...`;
        resultsDiv.innerHTML = `
            <div style="text-align:center; padding:40px;">
                <i class="fa-solid fa-spinner fa-spin" style="font-size:28px;"></i>
                <p>AI is ranking candidates...</p>
            </div>
        `;

        try {

            const response = await fetch(`http://localhost:8000/rank?top_k=${topK}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    job_description: jobDescription
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Ranking failed");
            }

            displayResults(data.ranked_students);

        } catch (error) {

            resultsDiv.innerHTML = `
                <div style="color:red; text-align:center; padding:40px;">
                    ❌ ${error.message}
                </div>
            `;

        } finally {
            rankBtn.disabled = false;
            rankBtn.innerHTML = `Find Candidates <i class="fa-solid fa-magnifying-glass"></i>`;
        }

    });

    // ================= DISPLAY RESULTS =================

    function displayResults(candidates) {

        if (!candidates || candidates.length === 0) {
            resultsDiv.innerHTML = `
                <div style="text-align:center; padding:40px;">
                    No suitable candidates found.
                </div>
            `;
            return;
        }

        let html = `<h2 style="margin-top:40px;">Ranked Candidates</h2>`;
        html += `<div class="candidates-grid">`;

        candidates.forEach((candidate, index) => {

            html += `
                <div class="candidate-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3>#${index + 1} ${candidate.name}</h3>
                        <span style="font-weight:600; color:#4ECDC4;">
                            Score: ${candidate.final_score}
                        </span>
                    </div>

                    <p>${candidate.branch} · Year ${candidate.year}</p>

                    <p><strong>Skills:</strong> ${candidate.skills.join(", ")}</p>

                    <div style="margin-top:10px;">
                        <p><strong>Semantic Match:</strong> ${candidate.semantic_similarity}</p>
                        <p><strong>GitHub Score:</strong> ${candidate.github_score}</p>
                        <p><strong>LeetCode Score:</strong> ${candidate.leetcode_score}</p>
                    </div>

                    <div style="margin-top:10px;">
                        <p><strong>LeetCode Stats:</strong> 
                        Easy: ${candidate.leetcode_stats.easy}, 
                        Medium: ${candidate.leetcode_stats.medium}, 
                        Hard: ${candidate.leetcode_stats.hard}</p>
                    </div>

                    <div style="margin-top:12px; display:flex; gap:10px;">
                        <a href="${candidate.github_profile}" target="_blank"
                            style="background:#333; padding:6px 12px; border-radius:6px; color:white; text-decoration:none;">
                            <i class="fa-brands fa-github"></i> GitHub
                        </a>

                        <a href="${candidate.leetcode_profile}" target="_blank"
                            style="background:#f59e0b; padding:6px 12px; border-radius:6px; color:white; text-decoration:none;">
                            <i class="fa-solid fa-code"></i> LeetCode
                        </a>

                        <a href="${candidate.resume_url}" target="_blank"
                            style="background:#374151; padding:6px 12px; border-radius:6px; color:white; text-decoration:none;">
                            <i class="fa-solid fa-file-pdf"></i> Resume
                        </a>
                    </div>

                    <div style="margin-top:15px; padding:12px; background:#f9fafb; border-radius:8px;">
                        <strong>AI Explanation:</strong>
                        <p style="margin-top:6px; font-size:14px;">
                            ${candidate.match_explanation}
                        </p>
                    </div>

                </div>
            `;
        });

        html += `</div>`;
        resultsDiv.innerHTML = html;
    }

});
