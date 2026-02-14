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

// ================= DISPLAY RANKED CANDIDATES =================

function displayRankedCandidates(candidates) {
    const modal = document.createElement("div");
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        overflow-y: auto;
        padding: 20px;
    `;

    const content = document.createElement("div");
    content.style.cssText = `
        background: white;
        padding: 40px;
        border-radius: 16px;
        max-width: 1000px;
        width: 100%;
        max-height: 90vh;
        overflow-y: auto;
    `;

    function getVerdictColor(verdict) {
        if (verdict.includes('Strong')) return '#10B981';
        if (verdict.includes('Moderate')) return '#F59E0B';
        return '#EF4444';
    }

    let html = `
        <h2 style="margin-bottom: 20px;">🏆 Ranked Candidates</h2>
        <div style="display: grid; gap: 20px;">
    `;

    if (!candidates || candidates.length === 0) {
        html += '<p>No candidates found.</p>';
    } else {
        candidates.forEach((c, index) => {
            const md = c.match_details || {}; // fallback if missing
            html += `
                <div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 20px; background: #F9FAFB;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0;">${index + 1}. ${c.name}</h3>
                        <span style="background: #4ECDC4; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 600;">Score: ${c.final_score}</span>
                    </div>
                    <p style="margin: 10px 0; color: #6B7280;">${c.branch} · Year ${c.year}</p>
                    
                    <!-- Structured match details -->
                    <div style="margin: 15px 0;">
                        <span style="background: ${getVerdictColor(md.verdict)}; padding: 6px 16px; border-radius: 20px; color: white; font-weight: 600; display: inline-block; margin-bottom: 12px;">
                            ${md.verdict || 'N/A'}
                        </span>
                        <p><strong>Fit Summary:</strong> ${md.fit_summary || 'No summary'}</p>
                        <p><strong>Technical Alignment:</strong> ${md.technical_alignment || 'N/A'}</p>
                        <p><strong>DSA Strength:</strong> ${md.dsa_strength || 'N/A'}</p>
                        <p><strong>Gaps:</strong> ${md.gaps || 'None identified'}</p>
                    </div>

                    <p><strong>Skills:</strong> ${c.skills.join(', ')}</p>
                    
                    <div style="margin: 10px 0;">
                        <details>
                            <summary style="cursor: pointer; color: #4ECDC4;">GitHub Stats</summary>
                            <p>Repos: ${c.github_stats.repos} · Stars: ${c.github_stats.stars}<br>Languages: ${c.github_stats.languages.join(', ')}</p>
                        </details>
                        <details>
                            <summary style="cursor: pointer; color: #4ECDC4;">LeetCode Stats</summary>
                            <p>Solved: ${c.leetcode_stats.total} (E:${c.leetcode_stats.easy} M:${c.leetcode_stats.medium} H:${c.leetcode_stats.hard})<br>Rating: ${c.leetcode_stats.contest_rating}</p>
                        </details>
                    </div>

                    <div style="display: flex; gap: 8px; margin-top: 12px;">
                        <a href="${c.github_profile}" target="_blank" style="background: #333; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px;">GitHub</a>
                        <a href="${c.leetcode_profile}" target="_blank" style="background: #FFA116; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px;">LeetCode</a>
                        <a href="http://localhost:8000${c.resume_url}" target="_blank" style="background: #4ECDC4; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px;">Resume</a>
                        <a href="http://localhost:8000${c.linkedin_url}" target="_blank" style="background: #0077B5; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px;">LinkedIn</a>
                    </div>
                </div>
            `;
        });
    }

    html += `</div><button id="closeRankModal" style="margin-top: 20px; padding: 10px 20px; background: #E5E7EB; border: none; border-radius: 6px; cursor: pointer;">Close</button>`;
    content.innerHTML = html;
    modal.appendChild(content);
    document.body.appendChild(modal);

    document.getElementById("closeRankModal").addEventListener("click", () => modal.remove());
    modal.addEventListener("click", (e) => { if (e.target === modal) modal.remove(); });
}
